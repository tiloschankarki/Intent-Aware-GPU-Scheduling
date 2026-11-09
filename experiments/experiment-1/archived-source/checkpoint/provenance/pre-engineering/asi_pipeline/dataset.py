"""Bounded streaming construction with immutable source-row split assignments."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import time
import duckdb
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from .safety import assign_workload


def sha256(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for chunk in iter(lambda:f.read(8*1024*1024),b''): h.update(chunk)
 return h.hexdigest()


def protocol_hash(p):
 return hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()


def random_split(ordinal,p):
 payload=json.dumps([p['split']['seed'],int(ordinal)],separators=(',',':')).encode()
 value=int.from_bytes(hashlib.sha256(payload).digest()[:8],'big')/2**64
 a,b,_=p['split']['fractions']
 return 'train' if value<a else 'validation' if value<a+b else 'test'


def build_dataset(source,output,p,limit=None):
 source,output=Path(source).resolve(),Path(output).resolve()
 if limit is None and not p['execution_permissions']['full_model_training']: raise PermissionError('Full dataset construction requires next checkpoint approval')
 if limit is not None and (limit<=0 or limit>p['dry_run']['max_source_rows']): raise ValueError('Dry run source-row bound exceeded')
 if output.exists(): raise FileExistsError(output)
 pf=pq.ParquetFile(source)
 actual={f.name:str(f.type) for f in pf.schema_arrow}
 if actual!=p['dataset']['schema'] or pf.metadata.num_rows!=p['dataset']['expected_rows']: raise ValueError('Source schema/row count differs from frozen protocol')
 start=time.monotonic(); fingerprint=sha256(source); stat=source.stat()
 output.mkdir(parents=True);(output/'data').mkdir()
 rows=0; kept=0; categories=Counter(); excluded=Counter(); paths=[]
 cols=list(dict.fromkeys([c for values in p['feature_groups'].values() for c in values]+[p['target']]))
 try:
  for batch in pf.iter_batches(batch_size=100000,columns=cols):
   if limit is not None: batch=batch.slice(0,min(len(batch),limit-rows))
   if not len(batch): break
   df=batch.to_pandas(); n=len(df)
   durations=df[p['target']].to_numpy(dtype=float)
   if not np.isfinite(durations).all() or (durations<=0).any(): raise ValueError('Invalid duration in source batch')
   if df.job_type_public.isna().any() or set(df.job_type_public)-set(p['dataset']['expected_lifecycle_counts']): raise ValueError('Unexpected lifecycle label')
   if np.isinf(df.gpu_request.to_numpy(dtype=float)).any(): raise ValueError('Infinite resource request')
   categories.update(df.job_type_public.tolist())
   df['row_ordinal']=np.arange(rows,rows+n,dtype=np.int64)
   df['random_split']=[random_split(i,p) for i in df.row_ordinal]
   df['grouped_split']=[None if pd.isna(x) else assign_workload(x,p) for x in df.workload_id]
   keep=df.job_type_public.isin(p['primary_lifecycle_categories'])
   excluded.update(df.loc[~keep,'job_type_public'].tolist());df=df.loc[keep].copy()
   rows+=n;kept+=len(df)
   if len(df):
    path=output/'data'/f'part-{len(paths):05d}.parquet'
    pq.write_table(pa.Table.from_pandas(df,preserve_index=False),path,compression='zstd');paths.append(path)
   if limit is not None and rows>=limit: break
  if not kept: raise ValueError('No primary lifecycle rows retained')
  con=duckdb.connect(':memory:');con.execute("SET memory_limit='1GB'");con.execute('SET threads=2')
  con.read_parquet([str(x) for x in paths]).create_view('base')
  if con.execute('SELECT count(*) FROM (SELECT workload_id FROM base WHERE workload_id IS NOT NULL GROUP BY workload_id HAVING count(DISTINCT grouped_split)>1)').fetchone()[0]: raise ValueError('Workload split contamination')
  if con.execute('SELECT count(*)-count(DISTINCT row_ordinal) FROM base').fetchone()[0]:raise ValueError('Duplicate physical row locator')
  counts={}
  for population in ['broad','finite']:
   pred='TRUE' if population=='broad' else "job_type_public IN ('training','offline_inference')"
   counts[population]={}
   for evaluation,col in [('workload_disjoint','grouped_split'),('random_execution','random_split')]:
    counts[population][evaluation]=dict(con.execute(f'SELECT {col},count(*) FROM base WHERE {pred} AND {col} IS NOT NULL GROUP BY {col}').fetchall())
  nulls=con.execute('SELECT count(*) FROM base WHERE workload_id IS NULL').fetchone()[0]
  con.close()
  if source.stat().st_size!=stat.st_size or source.stat().st_mtime_ns!=stat.st_mtime_ns:raise RuntimeError('Source changed during construction')
  manifest={'status':'success','dry_run':limit is not None,'scientific_interpretation':False if limit is not None else None,'timestamp_utc':datetime.now(timezone.utc).isoformat(),'protocol_content_sha256':protocol_hash(p),'source':str(source),'source_sha256':fingerprint,'source_schema':actual,'source_total_rows':pf.metadata.num_rows,'source_rows_read':rows,'sampling':'first physical rows' if limit else 'all source rows','retained_rows':kept,'excluded_categories':dict(excluded),'observed_categories':dict(categories),'retained_null_workload_rows':nulls,'counts':counts,'split_seed':p['split']['seed'],'split_disjoint':True,'row_locator':'physical source ordinal; not execution identifier/predictor','files':[{'path':str(x.relative_to(output)),'sha256':sha256(x),'bytes':x.stat().st_size} for x in paths],'elapsed_seconds':time.monotonic()-start,'versions':{x:importlib.metadata.version(x) for x in ['duckdb','pyarrow','numpy']}}
  (output/'manifest.json').write_text(json.dumps(manifest,indent=2,allow_nan=False)+'\n')
  return manifest
 except Exception as e:
  (output/'failure.json').write_text(json.dumps({'error':str(e),'source_rows_read':rows,'elapsed_seconds':time.monotonic()-start},indent=2));raise

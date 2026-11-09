"""Exact source/population gates and lossless primary artifact preparation."""
import json
import os
from pathlib import Path
import time
import urllib.request
import zipfile
from datetime import datetime,timezone
import duckdb
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from .dataset import sha256,protocol_hash
from .safety import assign_workload
from .checkpoints import freeze_json,code_state,versions

SOURCE_URL='https://tre-clusterdata.oss-cn-hangzhou.aliyuncs.com/cluster-trace-gpu-v2026/data/asi_opensource_job_execution_summary.zip'
EXPECTED={'rows':4709624,'workloads':473265,'null_workloads':0,'overlapping_workloads':0,
 'splits':{
  'train':{'rows':3339542,'workloads':331486,'lifecycle':{'training':2091126,'offline_inference':764755,'online_inference':465571,'dev':18090}},
  'validation':{'rows':658761,'workloads':71074,'lifecycle':{'training':426146,'offline_inference':131683,'online_inference':95598,'dev':5334}},
  'test':{'rows':711321,'workloads':70705,'lifecycle':{'training':442275,'offline_inference':134873,'online_inference':128791,'dev':5382}}}}

def connection(spill):
    con=duckdb.connect(':memory:');con.execute("SET memory_limit='512MB'");con.execute('SET threads=2')
    con.execute('SET preserve_insertion_order=false')
    Path(spill).mkdir(parents=True,exist_ok=True)
    con.execute('SET temp_directory=?',[str(Path(spill).resolve())]);con.execute("SET max_temp_directory_size='16GB'")
    return con

def acquire(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    manifest=output/'source-manifest.json';archive=output/'execution-summary.zip';source=output/'part-000.parquet'
    if manifest.exists():
        m=json.loads(manifest.read_bytes())
        if m['url']!=SOURCE_URL or sha256(archive)!=m['archive_sha256'] or sha256(source)!=m['source_sha256']:raise ValueError('Source identity changed')
        return m
    if archive.exists() or source.exists():raise ValueError('Incomplete acquisition; preserve files and select a fresh source directory')
    started=datetime.now(timezone.utc).isoformat();temp=output/'execution-summary.zip.partial'
    if temp.exists():raise ValueError('Partial archive exists; not a complete source')
    with urllib.request.urlopen(SOURCE_URL,timeout=60) as response,temp.open('xb') as stream:
        if response.status!=200:raise ValueError('Unexpected download HTTP status')
        expected=response.headers.get('Content-Length');received=0
        for chunk in iter(lambda:response.read(1024**2),b''):
            stream.write(chunk);received+=len(chunk)
        stream.flush();os.fsync(stream.fileno())
        if expected is not None and received!=int(expected):raise ValueError('Truncated archive')
    os.rename(temp,archive)
    with zipfile.ZipFile(archive) as z:
        members=[i for i in z.infolist() if Path(i.filename).name=='part-000.parquet' and not i.is_dir()]
        if len(members)!=1:raise ValueError('Expected exactly one execution summary Parquet')
        info=members[0]
        with z.open(info) as src,(output/'part-000.parquet.partial').open('xb') as dst:
            for chunk in iter(lambda:src.read(1024**2),b''):dst.write(chunk)
            dst.flush();os.fsync(dst.fileno())
        os.rename(output/'part-000.parquet.partial',source)
    result={'url':SOURCE_URL,'download_started_utc':started,'download_completed_utc':datetime.now(timezone.utc).isoformat(),
            'archive_bytes':archive.stat().st_size,'archive_sha256':sha256(archive),'member':info.filename,
            'source_bytes':source.stat().st_size,'source_sha256':sha256(source)}
    freeze_json(manifest,result)
    # Byte hashes remain the authority; read-only attributes discourage accidental writes.
    import stat
    os.chmod(source,stat.S_IREAD);os.chmod(archive,stat.S_IREAD)
    return result

def check_source_summary(summary,p):
    for key,expected in [('rows',p['dataset']['expected_rows']),('schema',p['dataset']['schema']),('lifecycle',p['dataset']['expected_lifecycle_counts'])]:
        if summary.get(key)!=expected:raise ValueError('SOURCE REPRODUCTION FAILED: '+key)

def audit_source(source,config,output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True);p=json.loads(Path(config).read_bytes())
    pf=pq.ParquetFile(source)
    summary={'rows':pf.metadata.num_rows,'schema':{f.name:str(f.type) for f in pf.schema_arrow},'source_sha256':sha256(source)}
    if summary['rows']!=p['dataset']['expected_rows'] or summary['schema']!=p['dataset']['schema']:raise ValueError('SOURCE SCHEMA/ROW GATE FAILED')
    con=connection(output/'spill')
    try:
        con.read_parquet(str(source)).create_view('source')
        summary['lifecycle']=dict(con.execute('SELECT job_type_public,count(*) FROM source GROUP BY 1').fetchall())
        check_source_summary(summary,p)
        summary['unique_pods']=con.execute('SELECT count(*) FROM (SELECT pod_id FROM source GROUP BY pod_id)').fetchone()[0]
        summary['unique_workloads']=con.execute('SELECT count(*) FROM (SELECT workload_id FROM source WHERE workload_id IS NOT NULL GROUP BY workload_id)').fetchone()[0]
        summary['non_null_workload_rows']=con.execute('SELECT count(workload_id) FROM source').fetchone()[0]
        row=con.execute('SELECT count(*) FILTER (WHERE duration_hours IS NULL OR NOT isfinite(duration_hours) OR duration_hours<=0), quantile_cont(duration_hours,[0.5,0.95,0.99]),max(duration_hours) FROM source').fetchone()
        summary.update(invalid_duration_rows=row[0],duration_quantiles=row[1],maximum_duration=row[2])
        if (summary['unique_pods'],summary['unique_workloads'],summary['non_null_workload_rows'],row[0],row[2])!=(36685018,501183,4792402,0,1824):raise ValueError('SOURCE CRITICAL VALUES FAILED: '+json.dumps(summary))
        freeze_json(output/'source-audit.json',summary)
        return summary
    finally:con.close()

def summarize(con,view):
    rows,workloads,nulls=con.execute(f'SELECT count(*),count(DISTINCT workload_id),count(*) FILTER(WHERE workload_id IS NULL) FROM {view}').fetchone()
    overlap=con.execute(f'SELECT count(*) FROM (SELECT workload_id FROM {view} GROUP BY workload_id HAVING count(DISTINCT split)>1)').fetchone()[0]
    result={'rows':rows,'workloads':workloads,'null_workloads':nulls,'overlapping_workloads':overlap,'splits':{}}
    for split,n,w in con.execute(f'SELECT split,count(*),count(DISTINCT workload_id) FROM {view} GROUP BY split').fetchall():
        result['splits'][split]={'rows':n,'workloads':w,'lifecycle':dict(con.execute(f'SELECT job_type_public,count(*) FROM {view} WHERE split=? GROUP BY 1',[split]).fetchall())}
    return result

def audit_population(source,config,output):
    output=Path(output);p=json.loads(Path(config).read_bytes());con=connection(output/'spill')
    try:
        con.read_parquet(str(source)).create_view('source')
        con.execute("CREATE VIEW primary_rows AS SELECT * FROM source WHERE workload_id IS NOT NULL AND job_type_public IN ('training','offline_inference','online_inference','dev')")
        count=con.execute('SELECT count(*),count(DISTINCT workload_id) FROM primary_rows').fetchone()
        if count!=(4709624,473265):raise ValueError('PRIMARY POPULATION GATE FAILED: '+str(count))
        ids=[r[0] for r in con.execute('SELECT DISTINCT workload_id FROM primary_rows ORDER BY workload_id').fetchall()]
        mapping=pa.table({'workload_id':ids,'split':[assign_workload(w,p) for w in ids]})
        path=output/'split-map.parquet'
        if path.exists():raise FileExistsError(path)
        pq.write_table(mapping,path,compression='zstd');con.register('mapping',mapping)
        con.execute('CREATE VIEW assigned AS SELECT p.*,m.split FROM primary_rows p JOIN mapping m USING(workload_id)')
        result=summarize(con,'assigned')
        if result!=EXPECTED:raise ValueError('EXACT SPLIT REPRODUCTION FAILED: '+json.dumps(result))
        freeze_json(output/'population-split-audit.json',{'counts':result,'split_seed':p['split']['seed'],
                     'split_map_sha256':sha256(path),'source_sha256':sha256(source),'protocol_sha256':sha256(config)})
        return result
    finally:con.close()

def build_primary(source,output,config):
    output=Path(output)
    if output.exists():raise FileExistsError(output)
    p=json.loads(Path(config).read_bytes());output.mkdir(parents=True);(output/'data').mkdir()
    columns=['workload_id','duration_hours','gpu_request','gpu_spec_public','priority_class','model_type_public','is_genai_request','job_type_public']
    writer=None;rows_read=0;cache={};start=time.monotonic()
    try:
        with pq.ParquetFile(source) as pf:
            canonical_schema=pa.schema([pf.schema_arrow.field(c) for c in columns]+[
                pa.field('row_ordinal',pa.int64()),pa.field('split',pa.string()),pa.field('grouped_split',pa.string())])
            for batch in pf.iter_batches(batch_size=100000,columns=columns):
                frame=batch.to_pandas();n=len(frame)
                frame['row_ordinal']=np.arange(rows_read,rows_read+n,dtype=np.int64);rows_read+=n
                frame=frame[frame.workload_id.notna()&frame.job_type_public.isin(p['primary_lifecycle_categories'])].copy()
                if frame.empty:continue
                for w in frame.workload_id.unique():
                    if w not in cache:cache[w]=assign_workload(w,p)
                frame['split']=frame.workload_id.map(cache);frame['grouped_split']=frame['split']
                table=pa.Table.from_pandas(frame,schema=canonical_schema,preserve_index=False)
                if writer is None:writer=pq.ParquetWriter(output/'data/primary.parquet',table.schema,compression='zstd',use_dictionary=True)
                writer.write_table(table,row_group_size=100000)
    finally:
        if writer:writer.close()
    if writer is None:raise ValueError('Empty primary population')
    # No completion manifest: a fresh process must reopen and validate first.
    freeze_json(output/'construction.json',{'source':str(Path(source).resolve()),'source_sha256':sha256(source),
         'source_rows_read':rows_read,'protocol_sha256':sha256(config),'protocol_content_sha256':protocol_hash(p),
         'preparation_script_sha256':sha256(__file__),'code':code_state(),'construction_seconds':time.monotonic()-start})

def inspect_primary(path,expected=None):
    path=Path(path);con=connection(path.parent.parent/'validation-spill')
    try:
        con.read_parquet(str(path)).create_view('canonical')
        result=summarize(con,'canonical')
        bad=con.execute('SELECT count(*) FROM canonical WHERE split IS NULL OR grouped_split IS DISTINCT FROM split OR duration_hours IS NULL OR NOT isfinite(duration_hours) OR duration_hours<=0').fetchone()[0]
        duplicate=con.execute('SELECT count(*)-count(DISTINCT row_ordinal) FROM canonical').fetchone()[0]
        if bad or duplicate:raise ValueError('Invalid canonical target/split/row locator')
        if expected is not None and result!=expected:raise ValueError('Canonical exact-count validation failed: '+json.dumps(result))
        return result
    finally:con.close()

def verify_assignments(path,p,split_map=None):
    con=connection(Path(path).parent.parent/'validation-spill')
    try:
        con.read_parquet(str(path)).create_view('canonical')
        for workload,split in con.execute('SELECT DISTINCT workload_id,split FROM canonical').fetchall():
            if assign_workload(workload,p)!=split:raise ValueError('Canonical workload assignment differs from frozen function')
        if split_map is not None:
            con.read_parquet(str(split_map)).create_view('original_map')
            bad=con.execute('SELECT count(*) FROM (SELECT DISTINCT workload_id,split FROM canonical) c FULL JOIN original_map m USING(workload_id) WHERE c.split IS DISTINCT FROM m.split').fetchone()[0]
            if bad:raise ValueError('Canonical workload mapping differs from independent source split audit')
    finally:con.close()

def verify_lossless(source,canonical,p):
    """Compare every retained value and ordinal, streaming in physical source order."""
    import pyarrow.compute as pc
    columns=['workload_id','duration_hours','gpu_request','gpu_spec_public','priority_class','model_type_public','is_genai_request','job_type_public']
    with pq.ParquetFile(source) as raw,pq.ParquetFile(canonical) as model:
        reader=iter(model.iter_batches(batch_size=100000,columns=columns+['row_ordinal']))
        tail=None;offset=0
        for batch in raw.iter_batches(batch_size=100000,columns=columns):
            table=pa.Table.from_batches([batch]);n=len(table)
            table=table.append_column('row_ordinal',pa.array(np.arange(offset,offset+n,dtype=np.int64)));offset+=n
            keep=pc.and_(pc.is_valid(table['workload_id']),pc.is_in(table['job_type_public'],value_set=pa.array(p['primary_lifecycle_categories'])))
            expected=table.filter(keep);need=len(expected);parts=[]
            while need:
                if tail is None or not len(tail):
                    next_batch=next(reader,None)
                    if next_batch is None:raise ValueError('Canonical truncated during lossless comparison')
                    tail=pa.Table.from_batches([next_batch])
                take=min(need,len(tail));parts.append(tail.slice(0,take));tail=tail.slice(take);need-=take
            if parts and not pa.concat_tables(parts).equals(expected,check_metadata=False):raise ValueError('Canonical values/row order differ from source')
        if (tail is not None and len(tail)) or next(reader,None) is not None:raise ValueError('Canonical contains extra rows')

def finalize_primary(output,config,protocol_doc,split_audit):
    output=Path(output);config=Path(config);p=json.loads(config.read_bytes());path=output/'data/primary.parquet'
    prep=json.loads((output/'construction.json').read_bytes());audit=json.loads(Path(split_audit).read_bytes())
    if prep['protocol_sha256']!=sha256(config) or prep['source_sha256']!=audit['source_sha256']:raise ValueError('Canonical provenance mismatch')
    if sha256(prep['source'])!=prep['source_sha256']:raise ValueError('Raw source changed')
    split_map=Path(split_audit).parent/'split-map.parquet'
    if sha256(split_map)!=audit['split_map_sha256']:raise ValueError('Independent split map changed')
    counts=inspect_primary(path,EXPECTED)
    verify_assignments(path,p,split_map)
    verify_lossless(prep['source'],path,p)
    split_manifest={'counts':counts,'source_sha256':prep['source_sha256'],'protocol_sha256':sha256(config),
                    'seed':p['split']['seed'],'algorithm':p['split']['algorithm'],'independent_split_audit_sha256':sha256(split_audit)}
    freeze_json(output/'split-manifest.json',split_manifest)
    pf=pq.ParquetFile(path)
    result={'status':'success','dry_run':False,'primary_only':True,'protocol_content_sha256':protocol_hash(p),
            'protocol_sha256':sha256(config),'protocol_doc_sha256':sha256(protocol_doc),'source_sha256':prep['source_sha256'],
            'source_rows_read':prep['source_rows_read'],'retained_rows':counts['rows'],'counts':counts,
            'split_manifest_sha256':sha256(output/'split-manifest.json'),
            'files':[{'path':'data/primary.parquet','sha256':sha256(path),'bytes':path.stat().st_size}],
            'schema':str(pf.schema_arrow),'compression':sorted({pf.metadata.row_group(i).column(j).compression for i in range(pf.metadata.num_row_groups) for j in range(pf.metadata.num_columns)}),
            'row_groups':[pf.metadata.row_group(i).num_rows for i in range(pf.metadata.num_row_groups)],
            'preparation_script_sha256':prep['preparation_script_sha256'],'code':code_state(),'versions':versions(),
            'fresh_process_validation_pid':os.getpid(),'timestamp_utc':datetime.now(timezone.utc).isoformat()}
    freeze_json(output/'manifest.json',result);return result

"""Shared native LightGBM selection path for paired M0 and M1 models."""
from datetime import datetime, timezone
import gc
import importlib.metadata
import json
from pathlib import Path
import hashlib
import time
import duckdb
import numpy as np
import pandas as pd
from .dataset import sha256,protocol_hash
from .safety import validate_features


def feature_columns(p,comparison,role,evaluation):
 if role not in ['m0','m1']:raise ValueError('Invalid role')
 groups=comparison.split('+')
 if evaluation=='workload_disjoint' and 'W' in groups:raise ValueError('Workload identity is forbidden in primary predictors')
 allowed=['+'.join(x['m0']) for x in p['paired_ablations']]
 if comparison not in allowed:raise ValueError('Comparison not enabled in required experiment')
 cols=[c for g in groups for c in p['feature_groups'][g]]
 if role=='m1':cols+=p['feature_groups']['O']
 validate_features(cols,p)
 return cols


def fit_encoding(train,columns,p):
 return {c:sorted(train[c].dropna().astype(str).unique().tolist()) for c in columns if c in p['encoding']['native_categorical']}


def encode(frame,columns,encoding,p):
 validate_features(columns,p)
 x=pd.DataFrame(index=frame.index)
 for c in columns:
  if c in p['encoding']['native_categorical']:
   values=frame[c].map(lambda v:None if pd.isna(v) else str(v))
   x[c]=values.map({v:i for i,v in enumerate(encoding[c])}).fillna(-1).astype('int32')
  else:x[c]=frame[c].astype('float64')
 return x


def load_split(dataset,p,population,evaluation,split):
 if population not in ['broad','finite'] or evaluation not in ['workload_disjoint','random_execution'] or split not in ['train','validation','test']:raise ValueError('Unknown population/evaluation/split')
 col='grouped_split' if evaluation=='workload_disjoint' else 'random_split'
 pred='TRUE' if population=='broad' else "job_type_public IN ('training','offline_inference')"
 con=duckdb.connect(':memory:');con.execute("SET memory_limit='1GB'");con.execute('SET threads=2')
 try:return con.execute(f'SELECT * FROM read_parquet(?) WHERE {pred} AND {col}=? ORDER BY row_ordinal',[str(Path(dataset)/'data/*.parquet'),split]).fetchdf()
 finally:con.close()


def row_hash(frame):return hashlib.sha256(np.asarray(frame.row_ordinal,dtype='<i8').tobytes()).hexdigest()


def train_one(dataset,output,config,population,evaluation,comparison,seed,role):
 import lightgbm as lgb
 dataset,output,config=map(Path,(dataset,output,config))
 raw=config.read_bytes();config_sha=hashlib.sha256(raw).hexdigest();p=json.loads(raw)
 dm=json.loads((dataset/'manifest.json').read_text())
 if dm['protocol_content_sha256']!=protocol_hash(p):raise ValueError('Dataset/protocol mismatch')
 if seed not in p['model']['seeds']:raise ValueError('Unfrozen model seed')
 if not dm['dry_run'] and not p['execution_permissions']['full_model_training']:raise PermissionError('Full training is disabled')
 if dm['dry_run'] and (dm['source_rows_read']>p['dry_run']['max_source_rows'] or comparison not in p['dry_run']['comparisons']):raise ValueError('Dry-run scope exceeds frozen bounds')
 if output.exists():raise FileExistsError(output)
 for f in dm['files']:
  if sha256(dataset/f['path'])!=f['sha256']:raise ValueError('Dataset file hash mismatch')
 features=feature_columns(p,comparison,role,evaluation)
 start=time.monotonic();output.mkdir(parents=True)
 try:
  train=load_split(dataset,p,population,evaluation,'train');valid=load_split(dataset,p,population,evaluation,'validation')
  if train.empty or valid.empty:raise ValueError('Empty training/validation split')
  if evaluation=='workload_disjoint' and set(train.workload_id)&set(valid.workload_id):raise ValueError('Train/validation workload contamination')
  enc=fit_encoding(train,features,p);x=encode(train,features,enc,p);v=encode(valid,features,enc,p)
  y=np.log1p(train.duration_hours.to_numpy());yv=np.log1p(valid.duration_hours.to_numpy())
  categorical=[c for c in features if c in enc]
  candidates=p['model']['hyperparameter_grid']
  if len(candidates)!=12 or len({json.dumps(c,sort_keys=True) for c in candidates})!=12:raise ValueError('Expected twelve distinct frozen candidates')
  best=None;best_score=float('inf');records=[];best_record=None
  for candidate in candidates:
   params={**p['model']['parameters'],**{k:v for k,v in candidate.items() if k!='candidate_id'},'seed':seed,'bagging_seed':seed,'feature_fraction_seed':seed,'data_random_seed':seed}
   ds=lgb.Dataset(x,label=y,categorical_feature=categorical,free_raw_data=True)
   vs=lgb.Dataset(v,label=yv,categorical_feature=categorical,reference=ds,free_raw_data=True)
   model=lgb.train(params,ds,num_boost_round=p['model']['num_boost_round'],valid_sets=[vs],valid_names=['validation'],callbacks=[lgb.early_stopping(p['model']['early_stopping_rounds'],verbose=False),lgb.log_evaluation(0)])
   pred=model.predict(v,num_iteration=model.best_iteration,num_threads=2)
   score=float(np.abs(yv-pred).mean())
   record={'candidate_id':candidate['candidate_id'],'validation_log_mae':score,'best_iteration':model.best_iteration,'parameters':params};records.append(record)
   if score<best_score:
    best_score=score;best_record=record;best=model.model_to_string(num_iteration=model.best_iteration)
   del model,ds,vs;gc.collect()
  # Only after selection is immutable do we read held-out test rows.
  model=lgb.Booster(model_str=best)
  test=load_split(dataset,p,population,evaluation,'test')
  if test.empty:raise ValueError('Empty test split')
  if evaluation=='workload_disjoint' and (set(test.workload_id)&(set(train.workload_id)|set(valid.workload_id))):raise ValueError('Test workload contamination')
  prediction=model.predict(encode(test,features,enc,p),num_threads=2)
  if not np.isfinite(prediction).all():raise ValueError('Nonfinite test prediction')
  if hashlib.sha256(config.read_bytes()).hexdigest()!=config_sha:raise RuntimeError('Config changed during training')
  model.save_model(str(output/'model.txt'))
  (output/'encoding.json').write_text(json.dumps(enc,indent=2)+'\n')
  (output/'candidates.json').write_text(json.dumps(records,indent=2,allow_nan=False)+'\n')
  predictions=test[['row_ordinal','workload_id','job_type_public','duration_hours']].copy();predictions['prediction']=prediction;predictions.to_parquet(output/'predictions.parquet',index=False)
  manifest={'status':'success','timestamp_utc':datetime.now(timezone.utc).isoformat(),'dry_run':dm['dry_run'],'scientific_interpretation':False if dm['dry_run'] else None,'dataset_manifest_sha256':sha256(dataset/'manifest.json'),'protocol_sha256':config_sha,'protocol_content_sha256':protocol_hash(p),'source_sha256':dm['source_sha256'],'population':population,'evaluation':evaluation,'comparison':comparison,'model_seed':seed,'split_seed':p['split']['seed'],'role':role,'features':features,'categorical_features':categorical,'encoding_fit':'train_only','candidate_count':len(records),'candidate_list':candidates,'selection_metric':'validation LogMAE','test_used_for_selection':False,'selected_candidate':best_record,'train_rows':len(train),'validation_rows':len(valid),'test_rows':len(test),'test_row_hash':row_hash(test),'predictions_sha256':sha256(output/'predictions.parquet'),'model_sha256':sha256(output/'model.txt'),'encoding_sha256':sha256(output/'encoding.json'),'elapsed_seconds':time.monotonic()-start,'versions':{s:importlib.metadata.version(s) for s in ['lightgbm','numpy','pandas','scipy','PyYAML']}}
  (output/'manifest.json').write_text(json.dumps(manifest,indent=2,allow_nan=False)+'\n')
  return manifest
 except Exception as e:
  (output/'failure.json').write_text(json.dumps({'error':str(e),'elapsed_seconds':time.monotonic()-start},indent=2));raise

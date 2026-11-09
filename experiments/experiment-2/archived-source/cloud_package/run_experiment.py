#!/usr/bin/env python3
"""Post-hoc internal split sensitivity. Selection bundle contains NO test data."""
import argparse,hashlib,json,sys,time,gc,os,platform,resource,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'pipeline'))
import numpy as np,pandas as pd,pyarrow.parquet as pq,duckdb,lightgbm,importlib.metadata
from asi_pipeline import modeling,execution

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8*1024**2),b''):h.update(b)
 return h.hexdigest()
def write(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(v,f,indent=2,allow_nan=False)
def versions():return {'python':platform.python_version(),'platform':platform.platform(),'machine':platform.machine(),**{x:importlib.metadata.version(x) for x in ['lightgbm','numpy','pandas','pyarrow','duckdb','scipy','PyYAML']}}
def peak():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
def frozen(out):
 p=json.loads((P/'protocol_20261020.json').read_text());f=json.loads((out/'FREEZE.json').read_text());assert f['roles']==['m0','m1'] and f['test_used_for_selection'] is False
 assert f['configuration_sha256']==sha(P/'protocol_20261020.json')
 for rel,h in f['artifacts'].items():assert sha(out/rel)==h, f'Frozen artifact modified: {rel}'
 for role in f['roles']:
  m=json.loads((out/role/'selection.json').read_text());records=m['records'];assert len(records)==12 and [r['candidate_id'] for r in records]==list(range(1,13))
  assert m['selected']==min(records,key=lambda r:(r['validation_log_mae'],r['candidate_id']))
  assert m['test_used_for_selection'] is False
  assert m['features']==modeling.feature_columns(p,'R+P+A',role,'workload_disjoint')
  for r,candidate in zip(records,p['model']['hyperparameter_grid']):assert r['parameters']==execution.parameters(p,candidate,20260927)
  assert sha(out/role/'model.txt')==sha(out/role/'candidates'/f"{m['selected']['candidate_id']:02d}"/'model.txt')
 return f
def load(s):
 con=duckdb.connect(':memory:');con.execute("SET memory_limit='1GB'");con.execute('SET threads=2')
 try:return con.execute('SELECT * FROM read_parquet(?) ORDER BY row_ordinal',[str(P/'selection_inputs'/f'{s}.parquet')]).fetchdf()
 finally:con.close()
def select(out,p,a):
 assert not out.exists(),'Use a fresh output directory; never overwrite a partial/complete run.'
 assert not list(P.rglob('test.parquet')),'Test data must not be deployed with selection inputs.'
 assert lightgbm.__version__=='4.7.0';assert len(p['model']['hyperparameter_grid'])==12;assert p['model']['num_boost_round']==200 and p['model']['early_stopping_rounds']==30 and p['model']['parameters']['num_threads']==2
 assert p['split']['seed']==20261020 and p['target_transform']=='log1p'
 for s in ['train','validation']:assert sha(P/'selection_inputs'/f'{s}.parquet')==a['splits'][s]['sha256']
 out.mkdir(parents=True);write(out/'environment.json',versions());write(out/'binding.json',{'label':'post-hoc internal split-sensitivity, not external replication','model_seed':20260927,'split_seed':20261020,'configuration_sha256':sha(P/'protocol_20261020.json'),'runner_sha256':sha(__file__),'source_hashes':{str(f.relative_to(P)):sha(f) for f in sorted((P/'pipeline').rglob('*.py'))},'inputs':{s:a['splits'][s]['sha256'] for s in ['train','validation']}})
 for role in ['m0','m1']:
  dest=out/role;dest.mkdir();cols=modeling.feature_columns(p,'R+P+A',role,'workload_disjoint');train=load('train');valid=load('validation')
  assert len(train)==a['splits']['train']['rows'] and len(valid)==a['splits']['validation']['rows'];assert not set(train.workload_id)&set(valid.workload_id)
  enc=modeling.fit_encoding(train,cols,p);x=modeling.encode(train,cols,enc,p);v=modeling.encode(valid,cols,enc,p);y=np.log1p(train.duration_hours.to_numpy());yv=np.log1p(valid.duration_hours.to_numpy());del train,valid;gc.collect();records=[]
  for candidate in p['model']['hyperparameter_grid']:
   start=time.monotonic();r,text,timing=execution.fit_candidate(x,y,v,yv,list(enc),p,candidate,20260927);records.append(r);d=dest/'candidates'/f"{r['candidate_id']:02d}";d.mkdir(parents=True);(d/'model.txt').write_text(text);write(d/'result.json',{'result':r,'timing':timing,'peak_rss_bytes':peak(),'elapsed_seconds':time.monotonic()-start});print(json.dumps({'role':role,**r,**timing}),flush=True)
  best=min(records,key=lambda r:(r['validation_log_mae'],r['candidate_id']));shutil.copyfile(dest/'candidates'/f"{best['candidate_id']:02d}"/'model.txt',dest/'model.txt');write(dest/'encoding.json',enc);write(dest/'selection.json',{'features':cols,'records':records,'selected':best,'test_used_for_selection':False,'encoding_fit':'train_only'})
  del x,y,v,yv;gc.collect()
 artifacts={str(f.relative_to(out)):sha(f) for f in sorted(out.rglob('*')) if f.is_file()};write(out/'FREEZE.json',{'roles':['m0','m1'],'test_used_for_selection':False,'configuration_sha256':sha(P/'protocol_20261020.json'),'artifacts':artifacts,'frozen_at_unix':time.time()})
 for f in out.rglob('*'):
  if f.is_file():f.chmod(0o444)
 frozen(out);print('BOTH SELECTIONS FROZEN. Test data have not been accessed.',flush=True)
def evaluate(out,test,p,a):
 freeze=frozen(out) # MUST validate both selections before even opening the test file.
 assert test is not None;assert sha(test)==a['splits']['test']['sha256'];ev=out/'evaluation';assert not ev.exists();ev.mkdir()
 d=pd.read_parquet(test).sort_values('row_ordinal').reset_index(drop=True);assert len(d)==a['splits']['test']['rows'] and d.row_ordinal.is_unique;assert d.workload_id.nunique()==a['splits']['test']['workloads'];assert (d['split']=='test').all()
 ids=set(d.workload_id)
 for s in ['train','validation']:
  assert sha(P/'selection_inputs'/f'{s}.parquet')==a['splits'][s]['sha256'];assert not ids&set(pd.read_parquet(P/'selection_inputs'/f'{s}.parquet',columns=['workload_id']).workload_id)
 y=np.log1p(d.duration_hours.to_numpy());loss={}
 for role in ['m0','m1']:
  dest=out/role;m=json.loads((dest/'selection.json').read_text());enc=json.loads((dest/'encoding.json').read_text());model=lightgbm.Booster(model_file=str(dest/'model.txt'));pr=model.predict(modeling.encode(d,m['features'],enc,p),num_threads=2);assert np.isfinite(pr).all();loss[role]=abs(y-pr);f=d[['row_ordinal','workload_id','job_type_public','duration_hours']].copy();f['prediction']=pr;f.to_parquet(ev/f'{role}_predictions.parquet',index=False)
 g=pd.DataFrame({'workload_id':d.workload_id,'n':1,**loss}).groupby('workload_id').sum();z=g[['m0','m1']].to_numpy();n=g.n.to_numpy();rng=np.random.default_rng(p['uncertainty']['seed']);B=p['uncertainty']['replicates'];boots=np.empty((B,2,4))
 for b in range(B):
  ix=rng.integers(0,len(n),size=len(n))
  for j,t in enumerate([z[ix].sum(axis=0)/n[ix].sum(),(z[ix]/n[ix,None]).mean(axis=0)]):boots[b,j]=[*t,t[0]-t[1],100*(t[0]-t[1])/t[0]]
 result={'label':'post-hoc internal split-sensitivity, not independent external replication','rows':len(d),'workloads':len(g),'bootstrap_replicates':B,'bootstrap_seed':p['uncertainty']['seed'],'conditional_on_one_fitted_model_seed':20260927,'split_seed':20261020,'freeze_sha256':sha(out/'FREEZE.json'),'test_sha256':sha(test),'environment':versions(),'metrics':{}}
 for j,(tag,t) in enumerate([('execution',z.sum(axis=0)/n.sum()),('equal_workload',(z/n[:,None]).mean(axis=0))]):
  result['metrics'][tag]={'m0':t[0],'m1':t[1],'absolute_improvement':t[0]-t[1],'relative_improvement_percent':100*(t[0]-t[1])/t[0],'absolute_improvement_ci95':np.quantile(boots[:,j,2],[.025,.975]).tolist(),'relative_improvement_ci95':np.quantile(boots[:,j,3],[.025,.975]).tolist()}
 frozen(out);write(ev/'results.json',result);write(ev/'artifacts.json',{f.name:sha(f) for f in ev.iterdir() if f.is_file()});print(json.dumps(result,indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['select','verify-freeze','evaluate']);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--test',type=Path);args=ap.parse_args();p=json.loads((P/'protocol_20261020.json').read_text());a=json.loads((P/'split_audit.json').read_text())
 if args.phase=='select':select(args.out,p,a)
 elif args.phase=='verify-freeze':frozen(args.out);print('Both model selections and all frozen artifact hashes verified.')
 else:evaluate(args.out,args.test,p,a)

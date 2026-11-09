import importlib.util,json,sys,tempfile
from pathlib import Path
import numpy as np,pandas as pd
sys.path.insert(0,str(Path.cwd()));sys.path.insert(0,str(Path.cwd()/'tests'))
from test_engineering import fixture
from asi_pipeline import modeling
from asi_pipeline.dataset import sha256
oldpath=Path(r'C:\Users\agraj\Documents\Codex\2026-10-06\files-pasted-by-the-user-you\work\engineering-baseline\asi_pipeline\modeling.py')
spec=importlib.util.spec_from_file_location('asi_pipeline.legacy_modeling_probe',oldpath)
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
results=[]
with tempfile.TemporaryDirectory() as d:
 root=Path(d);p,cfg=fixture(root)
 dm=json.loads((root/'data/manifest.json').read_bytes())
 for item in dm['files']:
  path=root/'data'/item['path'];f=pd.read_parquet(path)
  f['gpu_request']=(f.row_ordinal%5+1).astype(float)
  f['gpu_spec_public']=f.row_ordinal.map(lambda i:'gpu'+str(i%3))
  f['model_type_public']=f.row_ordinal.map(lambda i:None if i%7==0 else 'model'+str(i%4))
  f.to_parquet(path,index=False);item['sha256']=sha256(path)
 (root/'data/manifest.json').write_text(json.dumps(dm))
 for role in ('m0','m1'):
  args=(root/'data',root/('old-'+role),cfg,'broad','workload_disjoint','R+P+A',20260927,role)
  a=old.train_one(*args)
  b=modeling.train_one(root/'data',root/('new-'+role),cfg,'broad','workload_disjoint','R+P+A',20260927,role)
  original=json.loads((root/('old-'+role)/'candidates.json').read_bytes())
  revised=json.loads((root/('new-'+role)/'selection/manifest.json').read_bytes())['record']['records']
  assert original==revised
  x=pd.read_parquet(root/('old-'+role)/'predictions.parquet');y=pd.read_parquet(root/('new-'+role)/'predictions.parquet')
  assert x.equals(y)
  assert a['selected_candidate']==b['selected_candidate']
  results.append({'role':role,'all_12_candidate_records_identical':True,'test_predictions_exactly_identical':True,'selected_candidate_identical':True})
output=Path(r'C:\Users\agraj\Documents\Codex\2026-10-06\files-pasted-by-the-user-you\outputs\scientific-invariance-probe.json')
output.write_text(json.dumps({'fixture_only':True,'seed':20260927,'results':results},indent=2))
print(output.read_text())

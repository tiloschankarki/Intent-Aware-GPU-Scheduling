import json, tempfile, unittest
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from asi_pipeline import dataset, modeling
ROOT=Path(__file__).resolve().parents[1]

class ModelingTests(unittest.TestCase):
 def setUp(self): self.p=json.loads((ROOT/'config/protocol.yaml').read_text())
 def test_train_only_categories_and_no_workload_predictor(self):
  train=pd.DataFrame({'gpu_request':[1.,2.], 'gpu_spec_public':['a','b']})
  enc=modeling.fit_encoding(train,['gpu_request','gpu_spec_public'],self.p)
  x=modeling.encode(pd.DataFrame({'gpu_request':[3.], 'gpu_spec_public':['heldout']}),['gpu_request','gpu_spec_public'],enc,self.p)
  self.assertEqual(x['gpu_spec_public'].tolist(),[-1])
  with self.assertRaises(ValueError): modeling.feature_columns(self.p,'R+P+A+W','m0','workload_disjoint')
 def test_pair_adds_only_lifecycle(self):
  a=modeling.feature_columns(self.p,'R+P+A','m0','workload_disjoint');b=modeling.feature_columns(self.p,'R+P+A','m1','workload_disjoint')
  self.assertEqual(b,a+['job_type_public']);self.assertNotIn('workload_id',b)
 def test_model_seed_cannot_change_membership(self):
  a=[dataset.random_split(i,self.p) for i in range(100)]
  self.p['model']['seeds']=[999]
  self.assertEqual(a,[dataset.random_split(i,self.p) for i in range(100)])
 def test_stream_builder_exclusions_fixed_rows_and_full_gate(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);cols={}
   for name,kind in self.p['dataset']['schema'].items():
    typ={'string':pa.string(),'bool':pa.bool_(),'double':pa.float64(),'int64':pa.int64()}[kind]
    vals=['a']*4 if kind=='string' else [True]*4 if kind=='bool' else [1]*4
    cols[name]=pa.array(vals,type=typ)
   cols['job_type_public']=pa.array(['training','unknown','offline_inference','dev'])
   cols['workload_id']=pa.array(['w1','w2',None,'w1'])
   source=root/'source.parquet';pq.write_table(pa.table(cols),source,row_group_size=2)
   self.p['dataset']['expected_rows']=4
   result=dataset.build_dataset(source,root/'dataset',self.p,limit=4)
   frame=pq.read_table(root/'dataset/data').to_pandas()
   self.assertEqual(result['source_rows_read'],4);self.assertEqual(result['retained_rows'],3)
   self.assertEqual(frame['row_ordinal'].tolist(),[0,2,3])
   self.assertEqual(frame.iloc[0]['grouped_split'],frame.iloc[2]['grouped_split'])
   self.assertTrue(pd.isna(frame.iloc[1]['grouped_split']))
   with self.assertRaises(PermissionError): dataset.build_dataset(source,root/'full',self.p,limit=None)
   with self.assertRaises(FileExistsError): dataset.build_dataset(source,root/'dataset',self.p,limit=4)

class TrainingIntegrationTests(unittest.TestCase):
 def test_real_training_pair_and_no_test_label_selection(self):
  from asi_pipeline.modeling import train_one
  from asi_pipeline.dataset import sha256
  import hashlib
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p=json.loads((ROOT/'config/protocol.yaml').read_text());n=600;p['dataset']['expected_rows']=n
   rng=np.random.default_rng(9);cols={}
   for name,kind in p['dataset']['schema'].items():
    typ={'string':pa.string(),'bool':pa.bool_(),'double':pa.float64(),'int64':pa.int64()}[kind]
    vals=['x']*n if kind=='string' else [True]*n if kind=='bool' else [1]*n
    cols[name]=pa.array(vals,type=typ)
   cols['job_type_public']=pa.array(['training' if i%2 else 'offline_inference' for i in range(n)])
   cols['workload_id']=pa.array(['w'+str(i//2) for i in range(n)])
   cols['duration_hours']=pa.array(rng.uniform(.1,5,size=n));cols['gpu_request']=pa.array(rng.integers(1,5,size=n).astype(float))
   pq.write_table(pa.table(cols),root/'source.parquet');config=root/'protocol.yaml';config.write_text(json.dumps(p))
   dataset.build_dataset(root/'source.parquet',root/'data',p,limit=n)
   a=train_one(root/'data',root/'m0',config,'broad','workload_disjoint','R+P+A',20260927,'m0')
   b=train_one(root/'data',root/'m1',config,'broad','workload_disjoint','R+P+A',20260927,'m1')
   self.assertEqual(a['candidate_list'],b['candidate_list']);self.assertEqual(a['candidate_count'],12)
   self.assertEqual(a['test_row_hash'],b['test_row_hash']);self.assertFalse(a['test_used_for_selection'])
   self.assertEqual(a['features']+['job_type_public'],b['features'])
   files=list((root/'data/data').glob('*.parquet'))
   for f in files:
    frame=pq.read_table(f).to_pandas();frame.loc[frame.grouped_split=='test','duration_hours']=999999.
    frame.to_parquet(f,index=False)
   manifest=json.loads((root/'data/manifest.json').read_text())
   for item in manifest['files']:item['sha256']=sha256(root/'data'/item['path'])
   (root/'data/manifest.json').write_text(json.dumps(manifest))
   altered=train_one(root/'data',root/'altered_m0',config,'broad','workload_disjoint','R+P+A',20260927,'m0')
   self.assertEqual(a['selected_candidate'],altered['selected_candidate'])

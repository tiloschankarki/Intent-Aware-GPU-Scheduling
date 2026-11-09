import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import pyarrow as pa
import pyarrow.parquet as pq

ROOT=Path(__file__).resolve().parents[1]

class PrimaryDataTests(unittest.TestCase):
    def test_primary_data_api_exists(self):
        self.assertIsNotNone(importlib.util.find_spec('asi_pipeline.primary_data'))

    def test_canonical_filter_roundtrip_and_count_rejection(self):
        from asi_pipeline.primary_data import build_primary, inspect_primary
        from asi_pipeline.safety import assign_workload
        from asi_pipeline.dataset import sha256
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=json.loads((ROOT/'config/protocol.yaml').read_bytes())
            n=100;cols={}
            for name,kind in p['dataset']['schema'].items():
                typ={'string':pa.string(),'bool':pa.bool_(),'double':pa.float64(),'int64':pa.int64()}[kind]
                cols[name]=pa.array(['x']*n if kind=='string' else [True]*n if kind=='bool' else [1]*n,type=typ)
            ids=['w'+str(i) for i in range(n)];ids[0]=None
            cols['workload_id']=pa.array(ids);labels=['training']*n;labels[1]='unknown';cols['job_type_public']=pa.array(labels)
            pq.write_table(pa.table(cols),root/'source.parquet')
            config=root/'config.json';config.write_text(json.dumps(p))
            build_primary(root/'source.parquet',root/'canonical',config)
            result=inspect_primary(root/'canonical/data/primary.parquet')
            self.assertEqual(result['rows'],98);self.assertEqual(result['workloads'],98)
            frame=pq.read_table(root/'canonical/data/primary.parquet').to_pandas()
            self.assertEqual(frame.row_ordinal.tolist(),list(range(2,100)))
            self.assertEqual(frame['split'].tolist(),[assign_workload(w,p) for w in ids[2:]])
            self.assertEqual(result['overlapping_workloads'],0)
            bad=copy.deepcopy(result);bad['rows']=99
            with self.assertRaises(ValueError):inspect_primary(root/'canonical/data/primary.parquet',expected=bad)

    def test_source_gate_rejects_lifecycle_schema_and_rows(self):
        from asi_pipeline.primary_data import check_source_summary
        p=json.loads((ROOT/'config/protocol.yaml').read_bytes())
        summary={'rows':p['dataset']['expected_rows'],'schema':p['dataset']['schema'],'lifecycle':p['dataset']['expected_lifecycle_counts']}
        check_source_summary(summary,p)
        for key in ('rows','schema','lifecycle'):
            bad=copy.deepcopy(summary);bad[key]=0 if key=='rows' else {}
            with self.assertRaises(ValueError):check_source_summary(bad,p)

    def test_count_preserving_split_and_value_changes_rejected(self):
        from asi_pipeline.primary_data import verify_lossless,verify_assignments
        from test_engineering import fixture
        from asi_pipeline.primary_data import build_primary
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p,cfg=fixture(root)
            build_primary(root/'source.parquet',root/'canonical',cfg)
            path=root/'canonical/data/primary.parquet'
            verify_lossless(root/'source.parquet',path,p)
            verify_assignments(path,p)
            frame=pq.read_table(path).to_pandas();frame.loc[0,'gpu_request']=99
            frame.to_parquet(path,index=False)
            with self.assertRaises(ValueError):verify_lossless(root/'source.parquet',path,p)
            frame.loc[0,'split']='invalid';frame.loc[0,'grouped_split']='invalid';frame.to_parquet(path,index=False)
            with self.assertRaises(ValueError):verify_assignments(path,p)

import json
import argparse
import importlib.util
from unittest.mock import patch
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq

ROOT=Path(__file__).resolve().parents[1]

class LocalValidationTests(unittest.TestCase):
    def run_fixture(self, bad_schema=False, mutate_config=False):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); output=root/'output'; config=json.loads((ROOT/'config/protocol.yaml').read_text())
            config['dataset']['expected_rows']=3
            (root/'config').mkdir()
            config_path=root/'config/protocol.yaml'; config_path.write_text(json.dumps(config))
            cols={}
            for name,kind in config['dataset']['schema'].items():
                typ={'string':pa.string(),'bool':pa.bool_(),'double':pa.float64(),'int64':pa.int64()}[kind]
                values=['x','y','z'] if kind=='string' else [True]*3 if kind=='bool' else [1,2,3]
                cols[name]=pa.array(values,type=typ)
            cols['pod_id']=pa.array(['a','b','b']);cols['job_type_public']=pa.array(['training','dev','dev'])
            cols['workload_id']=pa.array(['w1','w2','w2'])
            if bad_schema: del cols['duration_hours']
            pq.write_table(pa.table(cols),root/'part-000.parquet')
            pq.write_table(pa.table({'pod_id':['a','b'],'first_seen_day':pa.array([109,109],pa.int16()),'first_seen_hour':pa.array([0,0],pa.int8())}),root/'temporal_map.parquet')
            if mutate_config:
                spec=importlib.util.spec_from_file_location('local_validator',ROOT/'scripts/validate_local.py')
                module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
                original=module.verify_legacy
                def change_after_verification(*args,**kwargs):
                    result=original(*args,**kwargs)
                    changed=json.loads(config_path.read_text()); changed['split']['seed']=999
                    config_path.write_text(json.dumps(changed))
                    return result
                with patch.object(module,'verify_legacy',side_effect=change_after_verification):
                    with self.assertRaisesRegex(RuntimeError,'[Cc]onfig'):
                        module.run(argparse.Namespace(root=root,config=config_path,output_root=output))
                self.assertFalse((output/'artifacts/temporal/d109h00_eligible.parquet').exists())
                return
            result=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/validate_local.py'),'--root',str(root),'--config',str(config_path),'--output-root',str(output)],capture_output=True,text=True)
            if bad_schema:
                self.assertNotEqual(result.returncode,0)
                self.assertFalse((output/'artifacts/temporal/d109h00_eligible.parquet').exists())
                failure=list((output/'results/audits').glob('failure-*.json'))
                self.assertEqual(len(failure),1,result.stderr)
                self.assertEqual(json.loads(failure[0].read_text())['status'],'failed')
            else:
                self.assertEqual(result.returncode,0,result.stderr)
                manifest=json.loads((output/'results/audits/local_validation.json').read_text())
                self.assertEqual(manifest['temporal']['eligible_pods'],1)
                self.assertEqual(manifest['temporal']['excluded_repeated_pods'],1)
                self.assertEqual(manifest['source']['rows'],3)
                self.assertEqual(pq.read_table(output/'artifacts/temporal/d109h00_eligible.parquet')['pod_id'].to_pylist(),['a'])
                again=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/validate_local.py'),'--root',str(root),'--config',str(config_path),'--output-root',str(output)],capture_output=True,text=True)
                self.assertNotEqual(again.returncode,0)
                self.assertEqual(json.loads((output/'results/audits/local_validation.json').read_text()),manifest)
    def test_end_to_end_manifest_and_no_overwrite(self): self.run_fixture()
    def test_schema_failure_logged_without_artifact(self): self.run_fixture(True)

    def test_config_change_during_run_stops_before_publication(self): self.run_fixture(mutate_config=True)

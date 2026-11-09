import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from asi_pipeline import dataset, modeling

ROOT = Path(__file__).resolve().parents[1]

def fixture(root):
    p = json.loads((ROOT/'config/protocol.yaml').read_text(encoding='utf-8'))
    n = 300
    p['dataset']['expected_rows'] = n
    cols = {}
    for name, kind in p['dataset']['schema'].items():
        typ = {'string': pa.string(), 'bool': pa.bool_(), 'double': pa.float64(), 'int64': pa.int64()}[kind]
        vals = ['x']*n if kind == 'string' else [True]*n if kind == 'bool' else [1]*n
        cols[name] = pa.array(vals, type=typ)
    cols['workload_id'] = pa.array(['w'+str(i//2) for i in range(n)])
    cols['job_type_public'] = pa.array(['training' if i%2 else 'offline_inference' for i in range(n)])
    cols['duration_hours'] = pa.array(np.random.default_rng(9).uniform(.1,5,n))
    pq.write_table(pa.table(cols), root/'source.parquet')
    config = root/'config.json'; config.write_text(json.dumps(p), encoding='utf-8')
    dataset.build_dataset(root/'source.parquet', root/'data', p, limit=n)
    return p, config

class CheckpointTests(unittest.TestCase):
    def test_checkpoint_api_exists(self):
        self.assertIsNotNone(importlib.util.find_spec('asi_pipeline.checkpoints'))

    def test_partial_stale_and_modified_artifacts_rejected(self):
        from asi_pipeline.checkpoints import publish_unit, read_unit
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); binding={'protocol':'a','seed':20260927}
            partial=root/'partial'; partial.mkdir(); (partial/'model.txt').write_text('partial')
            with self.assertRaises(ValueError): read_unit(partial,binding)
            publish_unit(root/'unit',binding,{'candidate':6},{'model.txt':b'model'})
            self.assertEqual(read_unit(root/'unit',binding)['record']['candidate'],6)
            with self.assertRaises(ValueError): read_unit(root/'unit',dict(binding,seed=99))
            with self.assertRaises(FileExistsError): publish_unit(root/'unit',binding,{}, {})
            (root/'unit/model.txt').write_text('changed')
            with self.assertRaises(ValueError): read_unit(root/'unit',binding)

class SelectionTests(unittest.TestCase):
    def test_selection_api_exists(self):
        self.assertIsNotNone(importlib.util.find_spec('asi_pipeline.execution'))

    def test_candidate_resume_and_freeze_gate(self):
        from asi_pipeline.execution import select_model, predict_selected
        import lightgbm as lgb
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p,cfg=fixture(root)
            args=(root/'data',root/'model',cfg,'broad','workload_disjoint','R+P+A',20260927,'m0')
            with self.assertRaises((ValueError, FileNotFoundError)):
                predict_selected(*args)
            original_load=modeling.load_split
            def no_test(*a,**kw):
                if a[4]=='test': raise AssertionError('test accessed during selection')
                return original_load(*a,**kw)
            actual_train=lgb.train; calls=[]
            def interrupted(*a,**kw):
                calls.append(1)
                if len(calls)==3: raise RuntimeError('simulated interruption')
                return actual_train(*a,**kw)
            with patch.object(modeling,'load_split',side_effect=no_test), patch.object(lgb,'train',side_effect=interrupted):
                with self.assertRaisesRegex(RuntimeError,'interruption'): select_model(*args)
            self.assertTrue((root/'model/candidates/01/manifest.json').exists())
            self.assertFalse((root/'model/selection/manifest.json').exists())
            fitted=[]
            def counted(*a,**kw): fitted.append(1); return actual_train(*a,**kw)
            with patch.object(modeling,'load_split',side_effect=no_test), patch.object(lgb,'train',side_effect=counted):
                selected=select_model(*args)
            self.assertEqual(len(fitted),10)
            self.assertEqual(len(selected['records']),12)
            self.assertTrue((root/'model/selection/manifest.json').exists())
            with patch.object(lgb,'train',side_effect=AssertionError('refit on resume')):
                self.assertEqual(select_model(*args),selected)
            result=predict_selected(*args)
            self.assertTrue(result['selection_manifest_sha256'])
            self.assertEqual(predict_selected(*args),result)
            before=cfg.read_bytes();p['model']['seeds'].append(99);cfg.write_text(json.dumps(p))
            with self.assertRaises(ValueError): predict_selected(*args)
            cfg.write_bytes(before)
            (root/'model/selection/model.txt').write_text('tampered')
            with self.assertRaises(ValueError): predict_selected(*args)

    def test_low_level_test_loader_requires_freeze(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p,cfg=fixture(root)
            with self.assertRaisesRegex(ValueError,'selection'):
                modeling.load_split(root/'data',p,'broad','workload_disjoint','test')

    def test_evaluation_rejects_missing_freeze_before_reading_predictions(self):
        from asi_pipeline.execution import require_prediction_selection
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): require_prediction_selection(Path(d),{}, {})

    def test_full_science_requires_passing_matching_feasibility(self):
        from asi_pipeline.execution import context
        from asi_pipeline.dataset import sha256
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p,cfg=fixture(root)
            dm=json.loads((root/'data/manifest.json').read_bytes());dm['dry_run']=False
            (root/'data/manifest.json').write_text(json.dumps(dm))
            auth=root/'authorization.json';auth.write_text(json.dumps({'full_execution_authorized':True,'protocol_sha256':sha256(cfg)}))
            with self.assertRaisesRegex((ValueError,PermissionError),'feasibility'):
                context(root/'data',cfg,'broad','workload_disjoint','R+P+A',20260927,'m0',auth)

    def test_global_freeze_requires_all_frozen_experiment_units(self):
        from asi_pipeline.scientific_run import experiment_units,freeze_experiment
        p=json.loads((ROOT/'config/protocol.yaml').read_bytes())
        units=experiment_units(p)
        self.assertEqual(len(units),36)
        self.assertEqual({u['comparison'] for u in units},{'R','R+P','R+P+A'})
        self.assertEqual({u['population'] for u in units},{'broad','finite'})
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):freeze_experiment(Path(d),p,{},units)

    def test_unlisted_parquet_rejected(self):
        from asi_pipeline.execution import context
        import shutil
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p,cfg=fixture(root)
            source=next((root/'data/data').glob('*.parquet'))
            shutil.copyfile(source,root/'data/data/stale.parquet')
            with self.assertRaisesRegex(ValueError,'inventory'):
                context(root/'data',cfg,'broad','workload_disjoint','R+P+A',20260927,'m0')

    def test_global_freeze_guard_rejects_missing_and_wrong_membership(self):
        from asi_pipeline.execution import require_global_freeze
        from asi_pipeline.checkpoints import publish_unit
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);binding={'protocol_sha256':'p','dataset_manifest_sha256':'d','code':{},
                                'population':'broad','comparison':'R+P+A','model_seed':20260927,'role':'m0'}
            auth=root/'auth.json';auth.write_text(json.dumps({'experiment_freeze':str(root/'freeze')}))
            with self.assertRaises(ValueError):require_global_freeze(root/'model',binding,auth)
            publish_unit(root/'freeze',{k:binding[k] for k in ('protocol_sha256','dataset_manifest_sha256','code')},{'selections':[]},{})
            with self.assertRaises(ValueError):require_global_freeze(root/'model',binding,auth)

class MonitorTests(unittest.TestCase):
    def test_monitor_api_exists(self):
        self.assertIsNotNone(importlib.util.find_spec('asi_pipeline.windows_monitor'))

    def test_hard_and_sustained_pressure(self):
        from asi_pipeline.windows_monitor import SafetyPolicy
        good={'available_physical':5*2**30,'commit_available':5*2**30,'commit_limit':20*2**30,'worker_rss':0,'page_reads_per_sec':0}
        policy=SafetyPolicy()
        self.assertIsNone(policy.check(good,0))
        self.assertIsNotNone(policy.check(dict(good,available_physical=500*2**20),1))
        policy=SafetyPolicy()
        soft=dict(good,available_physical=int(1.5*2**30))
        self.assertIsNone(policy.check(soft,0))
        self.assertIsNotNone(policy.check(soft,20))
        policy=SafetyPolicy()
        self.assertIsNotNone(policy.check(dict(good,commit_available=500*2**20),0))
        policy=SafetyPolicy();paging=dict(good,page_reads_per_sec=2000)
        self.assertIsNone(policy.check(paging,0))
        self.assertIsNotNone(policy.check(paging,16))

    def test_monitor_preflight_blocks_worker_without_mutating_command(self):
        from asi_pipeline.windows_monitor import supervise
        import sys
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); marker=root/'ran'; cmd=[sys.executable,'-c',f'from pathlib import Path; Path({str(marker)!r}).touch()']
            original=copy.deepcopy(cmd)
            low=lambda pid=None:{'available_physical':100,'commit_available':100,'commit_limit':20*2**30,'worker_rss':0,'page_reads_per_sec':None}
            result=supervise(cmd,root/'monitor',snapshot_fn=low)
            self.assertEqual(result['status'],'FAILED')
            self.assertFalse(marker.exists());self.assertEqual(cmd,original)

    def test_monitor_captures_exit_failure_and_success(self):
        from asi_pipeline.windows_monitor import supervise
        import sys
        good=lambda pid=None:{'available_physical':5*2**30,'commit_available':5*2**30,'commit_limit':20*2**30,'worker_rss':0,'page_reads_per_sec':None}
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            a=supervise([sys.executable,'-c','raise SystemExit(3)'],root/'a',snapshot_fn=good,poll_seconds=.01)
            b=supervise([sys.executable,'-c','print("done")'],root/'b',snapshot_fn=good,poll_seconds=.01)
            self.assertEqual(a['status'],'FAILED');self.assertEqual(a['exit_code'],3)
            self.assertEqual(b['status'],'PASSED');self.assertEqual(b['exit_code'],0)

    def test_safety_termination_and_monitor_error_fail_closed(self):
        from asi_pipeline.windows_monitor import supervise
        import sys
        good={'available_physical':5*2**30,'commit_available':5*2**30,'commit_limit':20*2**30,'worker_rss':0,'page_reads_per_sec':None}
        def drops(pid=None):return dict(good,commit_available=100) if pid else good
        def fails(pid=None):
            if pid:raise RuntimeError('sensor failed')
            return good
        with tempfile.TemporaryDirectory() as d:
            cmd=[sys.executable,'-c','import time; time.sleep(60)']
            a=supervise(cmd,Path(d)/'a',snapshot_fn=drops,poll_seconds=.01)
            b=supervise(cmd,Path(d)/'b',snapshot_fn=fails,poll_seconds=.01)
            self.assertEqual(a['status'],'FAILED');self.assertTrue(a['safety_terminated'])
            self.assertEqual(b['status'],'FAILED');self.assertIn('sensor failed',b['reason'])

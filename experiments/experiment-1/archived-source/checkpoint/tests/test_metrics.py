import json
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from asi_pipeline.metrics import paired_report, pair_predictions, bootstrap_replicates

P = json.loads((Path(__file__).parents[1] / 'config/protocol.yaml').read_text())

def fixture():
    d=np.array([1., 6., 24.])
    return pd.DataFrame(dict(row_ordinal=[0,1,2],workload_id=['a','b','b'],job_type_public=['training','dev','offline_inference'],duration_hours=d,pred_m0=np.log1p(d)+[1,2,4],pred_m1=np.log1p(d)+[0,1,2]))

class MetricsTests(unittest.TestCase):
    def test_aggregate_matches_explicit_duplicate_rows(self):
        f=fixture(); draws=np.array([[0,0],[0,1],[1,0],[1,1]])
        reps=bootstrap_replicates(f,4,1,draws=draws)
        for rep,draw in zip(reps,draws):
            rows=pd.concat([f[f.workload_id==['a','b'][i]] for i in draw])
            a=np.abs(np.log1p(rows.duration_hours)-rows.pred_m0).mean()
            b=np.abs(np.log1p(rows.duration_hours)-rows.pred_m1).mean()
            self.assertAlmostEqual(rep['absolute_gain'],a-b)
            self.assertAlmostEqual(rep['relative_gain_percent'],100*(a-b)/a)
    def test_boundaries_and_random_no_ci(self):
        r=paired_report(fixture(),P,'random_execution')
        self.assertIsNone(r['bootstrap'])
        self.assertEqual([s['n'] for s in r['tail']], [0,1,1,1,0,0,0,0])
        self.assertEqual(r['finite']['n'],2)
    def test_zero_error_null_relative_and_json_safe(self):
        f=fixture(); f.pred_m0=np.log1p(f.duration_hours);f.pred_m1=f.pred_m0
        r=paired_report(f,P,'workload_disjoint')
        self.assertIsNone(r['overall']['relative_gain_percent'])
        self.assertEqual(r['bootstrap']['relative_valid_replicates'],0)
        json.dumps(r,allow_nan=False)
    def test_invalid_inputs(self):
        for col,value in [('row_ordinal',[1,1,2]),('duration_hours',[1,0,2]),('pred_m0',[1,np.nan,2]),('workload_id',['a',None,'b'])]:
            f=fixture(); f[col]=value
            with self.assertRaises(ValueError): paired_report(f,P,'workload_disjoint')
        with self.assertRaises(ValueError): paired_report(fixture(),P,'invalid')
    def test_pairing_rejects_overlap_only_and_metadata_mismatch(self):
        f=fixture(); a=f.drop(columns=['pred_m1']).rename(columns={'pred_m0':'prediction'}); b=a.copy()
        self.assertEqual(len(pair_predictions(a,b)),3)
        b.row_ordinal=[0,1,4]
        with self.assertRaises(ValueError): pair_predictions(a,b)
        b=a.copy(); b.loc[0,'duration_hours']=9
        with self.assertRaises(ValueError): pair_predictions(a,b)

if __name__=='__main__': unittest.main()

class EvaluationCliTests(unittest.TestCase):
    def test_manifest_and_output_validation(self):
        import hashlib
        import importlib.util
        import tempfile
        spec=importlib.util.spec_from_file_location('evaluation_cli',Path(__file__).parents[1]/'scripts/06_generalization.py')
        cli=importlib.util.module_from_spec(spec);spec.loader.exec_module(cli)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);config=root/'config.json';config.write_text(json.dumps(P))
            f=fixture()
            for role in ('m0','m1'):
                d=root/role;d.mkdir()
                pred=f[METADATA_FOR_TEST+[f'pred_{role}']].rename(columns={f'pred_{role}':'prediction'})
                pred.to_parquet(d/'predictions.parquet',index=False)
                manifest=dict(dataset_manifest_sha256='source',protocol_sha256=cli.sha256(config),population='broad',evaluation='workload_disjoint',comparison='R',model_seed=20260927,test_row_hash=hashlib.sha256(np.asarray(f.row_ordinal,dtype='<i8').tobytes()).hexdigest(),dry_run=True,role=role,features=['gpu_request','gpu_spec_public']+(['job_type_public'] if role=='m1' else []),predictions_sha256=cli.sha256(d/'predictions.parquet'))
                # Fixture now supplies the mandatory freeze; original assertions remain unchanged.
                from asi_pipeline.checkpoints import publish_unit, code_state, versions
                from asi_pipeline.execution import parameters
                binding={k:manifest[k] for k in ('protocol_sha256','dataset_manifest_sha256','population','evaluation','comparison','model_seed','role','features')}
                binding.update(code=code_state(),versions=versions())
                records=[{'candidate_id':c['candidate_id'],'validation_log_mae':1.,'parameters':parameters(P,c,20260927)} for c in P['model']['hyperparameter_grid']]
                publish_unit(d/'selection',binding,{'records':records,'selected_candidate':records[0],'test_used_for_selection':False},{})
                manifest['selection_manifest_sha256']=cli.sha256(d/'selection/manifest.json')
                (d/'manifest.json').write_text(json.dumps(manifest))
            report=cli.evaluate(root/'m0',root/'m1',config,root/'out')
            self.assertEqual(len(pd.read_parquet(root/'out/bootstrap.parquet')),1000)
            self.assertNotIn('samples',report['bootstrap'])
            self.assertTrue(report['dry_run'])
            self.assertFalse(report['scientific_interpretation'])
            with self.assertRaises(FileExistsError): cli.evaluate(root/'m0',root/'m1',config,root/'out')
            manifest['model_seed']=99;(root/'m1/manifest.json').write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):cli.evaluate(root/'m0',root/'m1',config,root/'rejected')
            self.assertFalse((root/'rejected').exists())
            # Publication interruption cannot leave an apparently complete evaluation.
            manifest['model_seed']=20260927;(root/'m1/manifest.json').write_text(json.dumps(manifest))
            from unittest.mock import patch
            with patch.object(cli,'publish_unit',side_effect=RuntimeError('publication interrupted')):
                with self.assertRaisesRegex(RuntimeError,'publication interrupted'):
                    cli.evaluate(root/'m0',root/'m1',config,root/'interrupted')
            self.assertFalse((root/'interrupted').exists())
            cli.evaluate(root/'m0',root/'m1',config,root/'interrupted')
            self.assertTrue((root/'interrupted/manifest.json').is_file())

METADATA_FOR_TEST=['row_ordinal','workload_id','job_type_public','duration_hours']

"""Engineering-only candidate-6 feasibility; no test labels or effect reporting."""
import json
import os
from pathlib import Path
import sys
import time
from .checkpoints import freeze_json,code_state
from .dataset import sha256
from .execution import context,prepare,fit_candidate
from .primary_data import EXPECTED,inspect_primary
from .windows_monitor import snapshot,supervise,check_stop

def worker(dataset,output,config,authorization,role):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    p,dm,b=context(dataset,config,'broad','workload_disjoint','R+P+A',20260927,role,authorization,purpose='feasibility')
    if dm.get('counts')!=EXPECTED or not dm.get('primary_only'):raise ValueError('Feasibility requires exact primary canonical population')
    if p['model']['parameters']['num_threads']!=2:raise ValueError('Frozen two-thread requirement')
    candidate=next(c for c in p['model']['hyperparameter_grid'] if c['candidate_id']==6)
    if candidate!={'candidate_id':6,'num_leaves':31,'min_data_in_leaf':20,'feature_fraction':1.0}:raise ValueError('Frozen candidate 6 mismatch')
    check_stop();start=time.monotonic();before=snapshot(os.getpid())
    x,y,v,yv,enc,counts=prepare(dataset,p,'broad','workload_disjoint',b['features'])
    prepared=snapshot(os.getpid());prep_seconds=time.monotonic()-start
    check_stop()
    ignored,model,timing=fit_candidate(x,y,v,yv,[c for c in b['features'] if c in enc],p,candidate,20260927)
    check_stop();(output/'model.txt').write_text(model,encoding='utf-8')
    result={'status':'complete','engineering_only':True,'predictive_comparison':False,'role':role,'candidate':candidate,
            'seed':20260927,'threads':2,'features':b['features'],'canonical_rows':EXPECTED['rows'],**counts,
            'preparation_seconds':prep_seconds,'preparation_peak_rss':prepared['worker_peak_rss'],
            'baseline_rss':before['worker_rss'],**timing,'prediction_population':'validation only; test remains untouched',
            'worker_peak_rss':snapshot(os.getpid())['worker_peak_rss'],'model_bytes':(output/'model.txt').stat().st_size,
            'binding':b}
    freeze_json(output/'manifest.json',result)
    return result

def run(dataset,output,config,authorization):
    output=Path(output)
    if output.exists():raise FileExistsError('Feasibility is exactly once per role; existing run must be reviewed')
    output.mkdir(parents=True)
    inspect_primary(Path(dataset)/'data/primary.parquet',EXPECTED)
    report={'status':'FAILED','engineering_only':True,'workers':{},'protocol_sha256':sha256(config),
            'dataset_manifest_sha256':sha256(Path(dataset)/'manifest.json'),'code':code_state()}
    script=Path(__file__).resolve().parents[1]/'scripts/windows_feasibility.py'
    try:
        for role in ('m0','m1'):
            cmd=[sys.executable,'-B',str(script),'worker','--dataset',str(Path(dataset).resolve()),
                 '--output',str((output/role).resolve()),'--config',str(Path(config).resolve()),
                 '--authorization',str(Path(authorization).resolve()),'--role',role]
            monitored=supervise(cmd,output/(role+'-monitor'),spill=Path(dataset)/'spill')
            report['workers'][role]={'monitor':monitored}
            if monitored['status']!='PASSED':
                report['reason']='WINDOWS FULL WORKLOAD-DISJOINT NOT FEASIBLE';return report
            record=json.loads((output/role/'manifest.json').read_bytes())
            if record['role']!=role or record['canonical_rows']!=EXPECTED['rows']:raise ValueError('Feasibility worker result mismatch')
            report['workers'][role]['resources']=record
        report['status']='PASSED';report['reason']='Both exact workers completed safely'
        return report
    finally:freeze_json(output/'manifest.json',report)

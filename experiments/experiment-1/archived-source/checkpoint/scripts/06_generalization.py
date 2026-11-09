#!/usr/bin/env python3
"""Evaluate an already-trained matched pair without fitting or selecting models."""
import argparse
import hashlib
import json
import time
from datetime import datetime,timezone
import numpy as np
import importlib.metadata
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pandas as pd
from asi_pipeline.metrics import pair_predictions, paired_report
from asi_pipeline.execution import require_prediction_selection
from asi_pipeline.checkpoints import publish_unit

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def evaluate(m0_dir,m1_dir,config,output_dir):
    m0_dir,m1_dir,config,output_dir=map(Path,(m0_dir,m1_dir,config,output_dir))
    if output_dir.exists(): raise FileExistsError('Refusing to overwrite output directory')
    started=time.monotonic();config_bytes=config.read_bytes();config_hash=hashlib.sha256(config_bytes).hexdigest()
    protocol=json.loads(config_bytes); manifests=[]; frames=[]
    for role,directory in [('m0',m0_dir),('m1',m1_dir)]:
        manifest=json.loads((directory/'manifest.json').read_text()); path=directory/'predictions.parquet'
        if manifest['role']!=role: raise ValueError('Manifest role mismatch')
        if manifest['protocol_sha256']!=config_hash: raise ValueError('Protocol hash mismatch')
        require_prediction_selection(directory,manifest,protocol)
        if manifest['predictions_sha256']!=sha256(path): raise ValueError('Predictions hash mismatch')
        manifests.append(manifest);frames.append(pd.read_parquet(path))
    a,b=manifests
    for key in ('dataset_manifest_sha256','protocol_sha256','population','evaluation','comparison','model_seed','test_row_hash','dry_run'):
        if a[key]!=b[key]: raise ValueError('Paired manifest mismatch: '+key)
    if a['features']+['job_type_public']!=b['features'] or 'job_type_public' in a['features']:
        raise ValueError('M1 must add only job_type_public to M0')
    paired=pair_predictions(*frames)
    if hashlib.sha256(np.asarray(paired.row_ordinal,dtype='<i8').tobytes()).hexdigest()!=a['test_row_hash']:
        raise ValueError('Test row locator hash mismatch')
    report=paired_report(paired,protocol,a['evaluation'])
    report.update(dry_run=a['dry_run'],scientific_interpretation=False if a['dry_run'] else None,timestamp_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-started,versions={x:importlib.metadata.version(x) for x in ['numpy','pandas']})
    samples=report['bootstrap'].pop('samples') if report['bootstrap'] else []
    report['provenance']={'m0_manifest_sha256':sha256(m0_dir/'manifest.json'),'m1_manifest_sha256':sha256(m1_dir/'manifest.json'),**{k:a[k] for k in ('dataset_manifest_sha256','protocol_sha256','population','evaluation','comparison','model_seed','test_row_hash')}}
    # All validation precedes directory creation; create exclusively.
    if config.read_bytes()!=config_bytes:raise RuntimeError('Protocol changed during evaluation')
    import tempfile
    output_dir.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='evaluation-partial-',dir=output_dir.parent) as temporary:
        artifacts={}
        if samples:
            bootstrap=Path(temporary)/'bootstrap.parquet'
            pd.DataFrame(samples).to_parquet(bootstrap,index=False)
            report['bootstrap']['artifact']='bootstrap.parquet'
            report['bootstrap']['artifact_sha256']=sha256(bootstrap)
            artifacts['bootstrap.parquet']=bootstrap
        artifacts['evaluation.json']=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode()
        publish_unit(output_dir,report['provenance'],{'status':'success'},artifacts)
    return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('m0-dir','m1-dir','config','output-dir'): parser.add_argument('--'+name,required=True)
    args=parser.parse_args()
    evaluate(args.m0_dir,args.m1_dir,args.config,args.output_dir)

if __name__=='__main__': main()

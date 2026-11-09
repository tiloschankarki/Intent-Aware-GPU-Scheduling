#!/usr/bin/env python3
"""Local-only schema/split smoke checks and source-backed D109H00 eligibility.

No installs, network access or training. Existing outputs are never overwritten.
A success manifest is the completion marker; a Parquet without one is incomplete.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import sys
import tempfile
import time
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pyarrow.parquet as pq
from asi_pipeline.safety import assign_workload, assert_disjoint, publish_new, validate_features
from asi_pipeline.temporal import verify_legacy


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b''): h.update(chunk)
    return h.hexdigest()


def write_json_new(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=path.parent) as temporary:
        staged=Path(temporary)/'manifest.json'
        staged.write_text(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+'\n')
        publish_new(staged,path)


def run(args):
    started=time.monotonic()
    root=args.root.resolve(); output=(args.output_root or root).resolve()
    config_path=args.config.resolve()
    config_bytes=config_path.read_bytes()
    config_sha256=hashlib.sha256(config_bytes).hexdigest()
    protocol=json.loads(config_bytes)
    source=root/protocol['dataset']['path']; legacy=root/protocol['temporal']['legacy_map']
    destination=output/protocol['temporal']['validated_map']
    manifest_path=output/'results/audits/local_validation.json'
    if destination.exists() or manifest_path.exists():
        raise FileExistsError('Validation output already exists; select a fresh output root to rerun without overwriting')
    # Hash once up front, then again after processing to verify preservation.
    original_paths=[p for p in root.iterdir() if p.is_file()]
    before={p.name:digest(p) for p in original_paths}
    pf=pq.ParquetFile(source)
    actual={field.name:str(field.type) for field in pf.schema_arrow}
    if actual != protocol['dataset']['schema']:
        raise ValueError(f'Unexpected source schema: {actual}')
    if pf.metadata.num_rows != protocol['dataset']['expected_rows']:
        raise ValueError(f'Unexpected source row count: {pf.metadata.num_rows}')
    sample=next(pf.iter_batches(batch_size=protocol['local_validation']['sample_rows'],columns=['workload_id','job_type_public','duration_hours']))
    values=sample.to_pydict()
    if any(x is None or not math.isfinite(x) or x<=0 for x in values['duration_hours']):
        raise ValueError('Invalid target in smoke sample')
    known=set(protocol['primary_lifecycle_categories']+protocol['excluded_primary_categories'])
    if set(values['job_type_public'])-known:
        raise ValueError('Unexpected lifecycle category in smoke sample')
    assignments={key:[] for key in ['train','validation','test']}
    for workload in values['workload_id']:
        if workload is not None:
            assignments[assign_workload(workload,protocol)].append(workload)
    assert_disjoint(assignments)
    features=[]
    for pair in protocol['paired_ablations']+[protocol['seen_workload_optional_pair']]:
        for side in ['m0','m1']:
            cols=[c for group in pair[side] for c in protocol['feature_groups'][group]]
            validate_features(cols,protocol);features.append(cols)
    table,temporal=verify_legacy(source,legacy,protocol['temporal']['stratification_categories'],protocol['local_validation']['memory_limit'],protocol['local_validation']['threads'])
    if digest(config_path) != config_sha256:
        raise RuntimeError('Config changed during validation')
    after={p.name:digest(p) for p in original_paths}
    if before != after: raise RuntimeError('Historical input changed during validation')
    destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as temporary:
        staged=Path(temporary)/'eligible.parquet'
        pq.write_table(table,staged,compression='zstd')
        check=pq.read_table(staged)
        if not check.equals(table): raise RuntimeError('Output round-trip failed')
        publish_new(staged,destination)
    versions={'python':platform.python_version()}
    for package in ['duckdb','pyarrow','pandas','numpy','lightgbm','scipy','scikit-learn','PyYAML']:
        try: versions[package]=importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError: versions[package]=None
    manifest={
        'status':'success','timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'protocol_path':str(config_path),'protocol_sha256':config_sha256,
        'source':{'path':str(source),'sha256':before[source.name],'rows':pf.metadata.num_rows,'row_groups':pf.metadata.num_row_groups,'schema':actual,'independent_version_metadata':None},
        'legacy':{'path':str(legacy),'sha256':before[legacy.name],'schema':str(pq.ParquetFile(legacy).schema_arrow)},
        'temporal':temporal,'output':{'path':str(destination),'sha256':digest(destination),'bytes':destination.stat().st_size,'schema':str(table.schema)},
        'smoke':{'rows':sample.num_rows,'sample_method':'first Arrow batch, not representative research sample','lifecycle_categories':sorted(set(values['job_type_public'])),'positive_finite_target':True,'seed':protocol['split']['seed'],'workload_groups_by_split':{k:len(set(v)) for k,v in assignments.items()},'null_workload_sample_rows':sum(x is None for x in values['workload_id']),'group_disjoint':True,'validated_feature_sets':features},
        'preservation':{'all_original_root_files_sha256':before,'identical_after_validation':True},
        'software_versions':versions,'elapsed_seconds':time.monotonic()-started,'remote_bytes_transferred':0,'models_trained':0,
        'warnings':['No independent dataset release metadata; handoff attribution only.','Full duration/workload audits not rerun.','Legacy map is preserved, not eligible by itself.','Missing dependencies remain uninstalled.','Range helper is not a completed remote downloader.']}
    # Manifest is written last; downstream consumers must require it.
    write_json_new(manifest_path,manifest)
    print(json.dumps({'status':'success','temporal':temporal,'manifest':str(manifest_path),'elapsed_seconds':manifest['elapsed_seconds']},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--config',type=Path,default=Path(__file__).resolve().parents[1]/'config/protocol.yaml')
    parser.add_argument('--output-root',type=Path)
    args=parser.parse_args()
    try: run(args)
    except Exception as error:
        failure=(args.output_root or args.root).resolve()/'results/audits'/f'failure-{uuid.uuid4().hex}.json'
        write_json_new(failure,{'status':'failed','timestamp_utc':datetime.now(timezone.utc).isoformat(),'error':str(error),'exception':type(error).__name__,'root':str(args.root),'config':str(args.config)})
        print(f'{type(error).__name__}: {error}; failure manifest: {failure}',file=sys.stderr)
        sys.exit(1)

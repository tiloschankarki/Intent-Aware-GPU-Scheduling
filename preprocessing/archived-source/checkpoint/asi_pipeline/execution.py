"""Restartable validation selection followed by separately gated test prediction."""
import gc
import json
import time
from pathlib import Path
import numpy as np
from . import modeling
from .dataset import sha256, protocol_hash
from .checkpoints import publish_unit, read_unit, digest, versions, code_state

def context(dataset,config,population,evaluation,comparison,seed,role,authorization=None,*,purpose='science'):
    dataset,config=Path(dataset),Path(config)
    p=json.loads(config.read_bytes());dm=json.loads((dataset/'manifest.json').read_bytes())
    if dm['protocol_content_sha256']!=protocol_hash(p): raise ValueError('Dataset/protocol mismatch')
    if seed not in p['model']['seeds']: raise ValueError('Unfrozen seed')
    if not dm['dry_run']:
        if authorization is None: raise PermissionError('Full execution needs separate authorization manifest')
        auth=json.loads(Path(authorization).read_bytes())
        if auth.get('protocol_sha256')!=sha256(config) or auth.get('full_execution_authorized') is not True:
            raise ValueError('Execution authorization mismatch')
        if purpose=='science':
            gate=Path(auth.get('feasibility_manifest','__missing_feasibility__'))
            if not gate.is_file():raise PermissionError('Passing feasibility manifest required before science')
            feasibility=json.loads(gate.read_bytes())
            if (feasibility.get('status')!='PASSED' or feasibility.get('protocol_sha256')!=sha256(config)
                or feasibility.get('dataset_manifest_sha256')!=sha256(dataset/'manifest.json') or feasibility.get('code')!=code_state()):
                raise ValueError('Failed or incompatible feasibility gate')
        elif purpose!='feasibility':raise ValueError('Unknown execution purpose')
    if dm['dry_run'] and (dm['source_rows_read']>p['dry_run']['max_source_rows'] or comparison not in p['dry_run']['comparisons']):
        raise ValueError('Dry-run scope exceeds frozen bounds')
    listed={(dataset/f['path']).resolve() for f in dm['files']}
    if listed!={f.resolve() for f in (dataset/'data').glob('*.parquet')}:raise ValueError('Dataset file inventory mismatch')
    for f in dm['files']:
        if sha256(dataset/f['path'])!=f['sha256']: raise ValueError('Dataset file hash mismatch')
    if dm.get('split_manifest_sha256'):
        if sha256(dataset/'split-manifest.json')!=dm['split_manifest_sha256']: raise ValueError('Split manifest mismatch')
    feats=modeling.feature_columns(p,comparison,role,evaluation)
    binding={'source_sha256':dm['source_sha256'],'canonical_dataset_sha256':digest(dm['files']),
             'dataset_manifest_sha256':sha256(dataset/'manifest.json'),'protocol_sha256':sha256(config),
             'split_manifest_sha256':dm.get('split_manifest_sha256',digest({'files':dm['files'],'split':p['split']})),
             'code':code_state(),'versions':versions(),'population':population,'evaluation':evaluation,
             'comparison':comparison,'model_seed':seed,'role':role,'features':feats,
             'authorization_sha256':sha256(authorization) if authorization else None}
    if binding['versions']['lightgbm']!='4.7.0': raise ValueError('LightGBM must be exactly 4.7.0')
    return p,dm,binding

def parameters(p,candidate,seed):
    return {**p['model']['parameters'],**{k:v for k,v in candidate.items() if k!='candidate_id'},
            'seed':seed,'bagging_seed':seed,'feature_fraction_seed':seed,'data_random_seed':seed}

def fit_candidate(x,y,v,yv,categorical,p,candidate,seed):
    """Unchanged native Dataset/train/early-stopping/predict sequence."""
    import lightgbm as lgb
    from .windows_monitor import check_stop
    check_stop()
    def stop_callback(env): check_stop()
    stop_callback.order=0
    params=parameters(p,candidate,seed)
    ds=lgb.Dataset(x,label=y,categorical_feature=categorical,free_raw_data=True)
    vs=lgb.Dataset(v,label=yv,categorical_feature=categorical,reference=ds,free_raw_data=True)
    start=time.monotonic()
    model=lgb.train(params,ds,num_boost_round=p['model']['num_boost_round'],valid_sets=[vs],valid_names=['validation'],
                    callbacks=[lgb.early_stopping(p['model']['early_stopping_rounds'],verbose=False),lgb.log_evaluation(0),stop_callback])
    train_seconds=time.monotonic()-start;start=time.monotonic()
    pred=model.predict(v,num_iteration=model.best_iteration,num_threads=2)
    prediction_seconds=time.monotonic()-start
    score=float(np.abs(yv-pred).mean())
    if not np.isfinite(score): raise ValueError('Nonfinite validation score')
    record={'candidate_id':candidate['candidate_id'],'validation_log_mae':score,
            'best_iteration':model.best_iteration,'parameters':params}
    text=model.model_to_string(num_iteration=model.best_iteration)
    del model,ds,vs;gc.collect()
    return record,text,{'training_seconds':train_seconds,'prediction_seconds':prediction_seconds}

def prepare(dataset,p,population,evaluation,features):
    train=modeling.load_split(dataset,p,population,evaluation,'train')
    valid=modeling.load_split(dataset,p,population,evaluation,'validation')
    if train.empty or valid.empty: raise ValueError('Empty training/validation split')
    if evaluation=='workload_disjoint' and set(train.workload_id)&set(valid.workload_id): raise ValueError('Train/validation overlap')
    enc=modeling.fit_encoding(train,features,p)
    x=modeling.encode(train,features,enc,p);v=modeling.encode(valid,features,enc,p)
    y=np.log1p(train.duration_hours.to_numpy());yv=np.log1p(valid.duration_hours.to_numpy())
    counts={'train_rows':len(train),'validation_rows':len(valid)}
    del train,valid;gc.collect()
    return x,y,v,yv,enc,counts

def validate_selection(path,binding,p):
    unit=read_unit(path,binding);r=unit['record']
    grid=p['model']['hyperparameter_grid'];records=r['records']
    if [x['candidate_id'] for x in records]!=[x['candidate_id'] for x in grid]: raise ValueError('Incomplete selection candidates')
    for result,candidate in zip(records,grid):
        if result['parameters']!=parameters(p,candidate,binding['model_seed']): raise ValueError('Candidate parameters changed')
        if not np.isfinite(result['validation_log_mae']): raise ValueError('Invalid selection score')
    expected=min(records,key=lambda x:(x['validation_log_mae'],x['candidate_id']))
    if r['selected_candidate']!=expected: raise ValueError('Selection rule mismatch')
    if r['test_used_for_selection'] is not False: raise ValueError('Selection is not validation-only')
    return r

def select_model(dataset,output,config,population,evaluation,comparison,seed,role,authorization=None):
    output=Path(output)
    p,dm,binding=context(dataset,config,population,evaluation,comparison,seed,role,authorization)
    selection=output/'selection'
    if selection.exists(): return validate_selection(selection,binding,p)
    output.mkdir(parents=True,exist_ok=True)
    x,y,v,yv,enc,counts=prepare(dataset,p,population,evaluation,binding['features'])
    categorical=[c for c in binding['features'] if c in enc];records=[]
    grid=p['model']['hyperparameter_grid']
    if len(grid)!=12 or len({digest(c) for c in grid})!=12: raise ValueError('Expected 12 candidates')
    for candidate in grid:
        unitpath=output/'candidates'/f"{candidate['candidate_id']:02d}"
        cb={**binding,'candidate':candidate,'candidate_id':candidate['candidate_id']}
        if unitpath.exists(): unit=read_unit(unitpath,cb)
        else:
            result,model_text,timing=fit_candidate(x,y,v,yv,categorical,p,candidate,seed)
            if sha256(config)!=binding['protocol_sha256'] or code_state()!=binding['code']: raise ValueError('Code/protocol changed during fit')
            unit=publish_unit(unitpath,cb,{'result':result,'timing':timing},{'model.txt':model_text.encode()})
        records.append(unit['record']['result'])
    selected=min(records,key=lambda r:(r['validation_log_mae'],r['candidate_id']))
    record={'records':records,'selected_candidate':selected,'candidate_list':grid,'test_used_for_selection':False,
            'categorical_features':categorical,**counts}
    publish_unit(selection,binding,record,{
        'model.txt':output/'candidates'/f"{selected['candidate_id']:02d}"/'model.txt',
        'encoding.json':json.dumps(enc,indent=2).encode()})
    return validate_selection(selection,binding,p)

def predict_selected(dataset,output,config,population,evaluation,comparison,seed,role,authorization=None):
    import lightgbm as lgb
    output=Path(output);start=time.monotonic()
    p,dm,binding=context(dataset,config,population,evaluation,comparison,seed,role,authorization)
    selection=output/'selection';r=validate_selection(selection,binding,p)
    if not dm['dry_run']:require_global_freeze(output,binding,authorization,p)
    selection_hash=sha256(selection/'manifest.json');tb={**binding,'selection_manifest_sha256':selection_hash}
    if (output/'test').exists():
        result=read_unit(output/'test',tb)['record'];publish_legacy_outputs(output,result);return result
    # load_split itself checks the freeze; this call cannot bypass it.
    test=modeling.load_split(dataset,p,population,evaluation,'test',selection=selection,binding=binding)
    if test.empty: raise ValueError('Empty test split')
    # Dataset construction verifies global disjointness; verify again against held-out IDs.
    import duckdb
    con=duckdb.connect(':memory:')
    try:
        con.execute("SET memory_limit='512MB'");con.execute('SET threads=2')
        if evaluation=='workload_disjoint':
            bad=con.execute('SELECT count(*) FROM (SELECT workload_id FROM read_parquet(?) WHERE workload_id IS NOT NULL GROUP BY workload_id HAVING count(DISTINCT grouped_split)>1)',[str(Path(dataset)/'data/*.parquet')]).fetchone()[0]
            if bad: raise ValueError('Test workload contamination')
    finally: con.close()
    enc=json.loads((selection/'encoding.json').read_bytes())
    model=lgb.Booster(model_file=str(selection/'model.txt'))
    prediction=model.predict(modeling.encode(test,binding['features'],enc,p),num_threads=2)
    if not np.isfinite(prediction).all(): raise ValueError('Nonfinite test prediction')
    if sha256(config)!=binding['protocol_sha256'] or sha256(selection/'manifest.json')!=selection_hash: raise ValueError('Selection/config changed')
    pred=test[['row_ordinal','workload_id','job_type_public','duration_hours']].copy();pred['prediction']=prediction
    import uuid
    staged=output/('predictions.partial-'+uuid.uuid4().hex+'.parquet');pred.to_parquet(staged,index=False)
    result={'status':'success','dry_run':dm['dry_run'],'scientific_interpretation':False if dm['dry_run'] else None,
            'dataset_manifest_sha256':binding['dataset_manifest_sha256'],'protocol_sha256':binding['protocol_sha256'],
            'source_sha256':dm['source_sha256'],'protocol_content_sha256':protocol_hash(p),
            'population':population,'evaluation':evaluation,'comparison':comparison,'model_seed':seed,'split_seed':p['split']['seed'],
            'role':role,'features':binding['features'],'categorical_features':r['categorical_features'],'encoding_fit':'train_only',
            'candidate_count':len(r['records']),'candidate_list':r['candidate_list'],'selected_candidate':r['selected_candidate'],
            'test_used_for_selection':False,'selection_metric':'validation LogMAE','selection_manifest_sha256':selection_hash,
            'train_rows':r['train_rows'],'validation_rows':r['validation_rows'],'test_rows':len(test),'test_row_hash':modeling.row_hash(test),
            'predictions_sha256':sha256(staged),'model_sha256':sha256(selection/'model.txt'),'encoding_sha256':sha256(selection/'encoding.json'),
            'versions':binding['versions'],'elapsed_seconds':time.monotonic()-start}
    result['authorization_path']=str(Path(authorization).resolve()) if authorization else None
    publish_unit(output/'test',tb,result,{'predictions.parquet':staged})
    staged.unlink()
    publish_legacy_outputs(output,result)
    return result

def compatibility_train(*args,**kwargs):
    """Original smoke-call interface; scientific driver uses two separate phases."""
    select_model(*args,**kwargs);result=predict_selected(*args,**kwargs)
    return result

def publish_legacy_outputs(output,result):
    from .checkpoints import freeze_json
    output=Path(output)
    # Preserve legacy file locations for existing consumers, without overwriting.
    import os
    for source,name in [(output/'selection/model.txt','model.txt'),(output/'selection/encoding.json','encoding.json'),
                        (output/'test/predictions.parquet','predictions.parquet')]:
        if (output/name).exists():
            if sha256(output/name)!=sha256(source):raise ValueError('Legacy output hash mismatch')
        else:os.link(source,output/name)
    if (output/'manifest.json').exists():
        if json.loads((output/'manifest.json').read_bytes())!=result:raise ValueError('Legacy manifest mismatch')
    else:freeze_json(output/'manifest.json',result)

def require_prediction_selection(directory,manifest,protocol):
    selection=Path(directory)/'selection'
    if not manifest.get('selection_manifest_sha256') or not (selection/'manifest.json').is_file():
        raise ValueError('Valid frozen selection required before test evaluation')
    if sha256(selection/'manifest.json')!=manifest['selection_manifest_sha256']: raise ValueError('Selection hash mismatch')
    unit=read_unit(selection);binding=unit['binding']
    for key in ('protocol_sha256','dataset_manifest_sha256','population','evaluation','comparison','model_seed','role','features'):
        if binding.get(key)!=manifest.get(key):raise ValueError('Selection context mismatch: '+key)
    if binding.get('code')!=code_state() or binding.get('versions')!=versions():raise ValueError('Selection code/version mismatch')
    if not manifest.get('dry_run',False):
        authorization=manifest.get('authorization_path')
        if not authorization or sha256(authorization)!=binding['authorization_sha256']:raise ValueError('Evaluation authorization mismatch')
        require_global_freeze(directory,binding,authorization,protocol)
    return validate_selection(selection,binding,protocol)

def require_global_freeze(output,binding,authorization,p=None):
    """Every full-data prediction entry point must validate the whole experiment."""
    auth=json.loads(Path(authorization).read_bytes())
    path=Path(auth.get('experiment_freeze','__missing_experiment_freeze__'))
    global_binding={k:binding[k] for k in ('protocol_sha256','dataset_manifest_sha256','code')}
    frozen=read_unit(path,global_binding)
    if p is None:raise ValueError('Protocol required for global selection validation')
    from .scientific_run import experiment_units,freeze_experiment,location
    units=experiment_units(p)
    if len(frozen['record'].get('selections',[]))!=len(units):raise ValueError('Incomplete global selection freeze')
    freeze_experiment(path.parent,p,global_binding,units)
    u={'population':binding['population'],'comparison':binding['comparison'],'seed':binding['model_seed'],'role':binding['role']}
    if Path(output).resolve()!=location(path.parent,u).resolve():raise ValueError('Test output is not a member of frozen experiment')
    expected={'unit':u,'selection_sha256':sha256(Path(output)/'selection/manifest.json')}
    if expected not in frozen['record']['selections']:raise ValueError('Selection absent from global freeze')

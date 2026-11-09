"""Experiment 3: validation-only restricted-population split robustness."""
from pathlib import Path
import argparse, collections, contextlib, gc, hashlib, importlib.metadata, json
import math, os, platform, shutil, sys, threading, time, uuid
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import lightgbm as lgb
import psutil
import frozen_reference as ref
BASE = Path(__file__).resolve().parent
GIB = 1024**3

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(8*1024**2), b''): h.update(b)
    return h.hexdigest()

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def digest(value): return hashlib.sha256(canonical(value)).hexdigest()

def load_protocol(): return json.loads((BASE/'original_protocol.json').read_text())

def save_unit(path, binding, result, files):
    """Publish commit marker last. Incomplete attempts are retained, never overwritten."""
    path = Path(path)
    if path.exists(): raise FileExistsError(path)
    path.mkdir(parents=True)
    payload = {'result.json': canonical(result), **files}
    for name, data in payload.items():
        if Path(name).name != name: raise ValueError('Invalid artifact name')
        with (path/name).open('xb') as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
    record = {'binding': binding, 'sha256': {n: sha(path/n) for n in payload}}
    with (path/'COMMIT.json').open('xb') as f:
        f.write(canonical(record)); f.flush(); os.fsync(f.fileno())
    read_unit(path, binding)

def read_unit(path, binding):
    path = Path(path)
    m = json.loads((path/'COMMIT.json').read_text())
    if m['binding'] != binding: raise ValueError(f'Checkpoint binding mismatch: {path}')
    for name, h in m['sha256'].items():
        if Path(name).name != name or sha(path/name) != h:
            raise ValueError(f'Checkpoint corruption: {path}/{name}')
    return json.loads((path/'result.json').read_text())

def recover_partial(path):
    path = Path(path)
    if path.exists() and not (path/'COMMIT.json').exists():
        path.rename(path.with_name(path.name+'.incomplete-'+uuid.uuid4().hex))

def exclusion_union(maps):
    if len(maps) != 2: raise ValueError('Two historical maps required')
    universes=[]; tests=[]
    for d in maps:
        if set(d.columns) != {'workload_id','split'}: raise ValueError('ID-only split map required')
        if d.workload_id.isna().any() or d.workload_id.duplicated().any(): raise ValueError('Bad IDs')
        if not d.workload_id.map(lambda x:isinstance(x,str) and bool(x)).all(): raise ValueError('Bad ID type')
        if not set(d.split).issubset({'train','validation','test'}): raise ValueError('Bad split')
        universes.append(set(d.workload_id)); tests.append(set(d.loc[d.split=='test','workload_id']))
    if universes[0] != universes[1]: raise ValueError('Historical workload universes differ')
    excluded=tests[0] | tests[1]
    return excluded, {'historical_test_workloads':[len(x) for x in tests],
        'overlap_workloads':len(tests[0]&tests[1]), 'excluded_union_workloads':len(excluded),
        'original_workloads':len(universes[0]), 'eligible_workloads':len(universes[0])-len(excluded)}

def loss_metrics(y, prediction, ids):
    loss=np.abs(np.asarray(y)-np.asarray(prediction))
    if not len(loss) or not np.isfinite(loss).all(): raise ValueError('Invalid losses')
    codes,unique=pd.factorize(ids,sort=False)
    totals=np.bincount(codes,weights=loss);n=np.bincount(codes)
    return {'execution_logmae':float(loss.mean()),
        'equal_workload_logmae':float(np.mean(totals/n)), 'rows':len(loss),'workloads':len(unique)}

def concentration(ids):
    n=pd.Series(ids).value_counts().to_numpy();s=n/n.sum()
    return {'rows':int(n.sum()),'workloads':len(n),'top1_execution_share':float(s[0]),
        'top1pct_execution_share':float(s[:max(1,math.ceil(.01*len(n)))].sum()),
        'hhi':float(np.sum(s*s)),'effective_workloads':float(1/np.sum(s*s))}

def profile_support(train, valid):
    # Exact full encoded-profile comparison, no hashing approximation.
    counts=train.value_counts(dropna=False,sort=False)
    ix=pd.MultiIndex.from_frame(valid)
    if len(valid.columns)==1: ix=pd.Index(valid.iloc[:,0])
    if len(valid.columns)==1 and isinstance(counts.index,pd.MultiIndex): counts.index=counts.index.get_level_values(0)
    support=counts.reindex(ix,fill_value=0).to_numpy()
    return {'train_unique_profiles':len(counts),'validation_unique_profiles':len(valid.drop_duplicates()),
        'unseen_validation_execution_fraction':float(np.mean(support==0)),
        'train_support_rows_quantiles_for_validation_executions':np.quantile(support,[0,.25,.5,.75,1]).tolist()}

class Resources:
    def __init__(self, rss_limit, reserve):
        self.rss_limit=rss_limit;self.reserve=reserve;self.peak=0;self.minimum=10**30
        self.stop=threading.Event();self.thread=None
    def sample(self):
        rss=psutil.Process().memory_info().rss
        self.peak=max(self.peak,rss);self.minimum=min(self.minimum,psutil.virtual_memory().available)
    def guard(self, env=None):
        self.sample()
        if self.peak>self.rss_limit or self.minimum<self.reserve:
            raise MemoryError('Pre-registered resource limit reached; no reduced-data fallback')
    def __enter__(self):
        self.guard()
        def loop():
            while not self.stop.wait(.25): self.sample()
        self.thread=threading.Thread(target=loop,daemon=True);self.thread.start();return self
    def __exit__(self,*args):
        self.stop.set();self.thread.join();self.sample()
    def result(self): return {'peak_rss_bytes_sampled':self.peak,'minimum_available_bytes_sampled':self.minimum,'sample_interval_seconds':.25}

def verify_bundle(bundle):
    bundle=Path(bundle);manifest=json.loads((bundle/'bundle_manifest.json').read_text())
    for name,h in manifest['files'].items():
        p=bundle/name
        if not p.resolve().is_relative_to(bundle.resolve()) or sha(p)!=h: raise ValueError('Bundle hash mismatch: '+name)
    return manifest

def environment():
    return {'python':platform.python_version(),'platform':platform.platform(),
        'packages':{k:importlib.metadata.version(k) for k in ['lightgbm','numpy','pandas','pyarrow','psutil']},
        'ram_bytes':psutil.virtual_memory().total,'logical_cpus':psutil.cpu_count()}

def preregister(bundle, out):
    bundle=Path(bundle);out=Path(out);verify_bundle(bundle)
    if lgb.__version__!='4.7.0': raise ValueError('LightGBM must be exactly 4.7.0')
    p=load_protocol()
    spec={'study':'new restricted-population robustness study; not full-population replication',
        'split_seeds':[20261028,20261029,20261030,20261031,20261101,20261102,20261103,20261104,20261105,20261106], 'model_seed':20260927,
        'historical_split_seeds':[20260927,20261020],
        'seed_interpretation':'10 split seeds; one fixed model seed, as in experiment 2',
        'population':json.loads((bundle/'population_audit.json').read_text()),
        'bundle_manifest_sha256':sha(bundle/'bundle_manifest.json'),
        'package_versions':environment()['packages'],
        'runner_sha256':sha(BASE/'exp3_runner.py'),'reference_sha256':sha(BASE/'frozen_reference.py'),
        'protocol_sha256':sha(BASE/'original_protocol.json'),
        'grid':p['model']['hyperparameter_grid'],'base_parameters':p['model']['parameters'],
        'num_boost_round':200,'early_stopping_rounds':30,
        'selection':'minimum validation execution LogMAE; lowest candidate_id breaks ties',
        'secondary_metric':'equal-workload validation LogMAE, never used for selection',
        'feature_processing':'verbatim archived feature_columns, fit_encoding, encode; train only',
        'target':'numpy.log1p(duration_hours), no clipping or inverse transform',
        'test_policy':'historical holdouts excluded; new per-seed test outcomes never loaded or evaluated',
        'pilot_seed':20261028,'pilot_fits':24,'rss_limit_bytes':8*GIB,'reserve_bytes':2*GIB,
        'pilot_gate':'all 24 candidates and both winners committed; sampled RSS <= 8 GiB; sampled available >= 2 GiB',
        'failure_policy':'stop on resource/data/protocol failure; keep partial checkpoints and all seed statuses; no seed replacement, no grid/data changes',
        'analysis':'report every seed, candidates, rounds, both validation metrics, unweighted seed delta summaries; no independent-seed significance claim',
        'confirmatory_tests':'untouched; no confirmatory test results in this study notebook'}
    binding={'spec_sha256':digest(spec)}
    if out.exists() and any(out.iterdir()) and not (out/'PREREGISTRATION').exists():
        raise ValueError('Nonempty run directory without preregistration')
    out.mkdir(parents=True,exist_ok=True);unit=out/'PREREGISTRATION';recover_partial(unit)
    if unit.exists():
        saved=read_unit(unit,binding)
        return saved['spec'],digest(spec)
    save_unit(unit,binding,{'spec':spec,'environment_at_registration':environment(),'registered_unix':time.time()}, {})
    return spec,digest(spec)

def active_spec(bundle,out):
    spec,h=preregister(bundle,out)
    # Repeat bindings at each invocation, including resumption.
    if sha(BASE/'exp3_runner.py')!=spec['runner_sha256']: raise ValueError('Runner changed')
    return spec,h

def fit_candidate(x,y,v,yv,enc,p,candidate,model_seed,monitor):
    # Same Dataset/train/early_stopping/predict sequence as archived execution.fit_candidate.
    params=ref.parameters(p,candidate,model_seed)
    ds=lgb.Dataset(x,label=y,categorical_feature=list(enc),free_raw_data=True)
    vs=lgb.Dataset(v,label=yv,categorical_feature=list(enc),reference=ds,free_raw_data=True)
    def resource_callback(env): monitor.guard(env)
    resource_callback.order=0
    start=time.monotonic()
    model=lgb.train(params,ds,num_boost_round=p['model']['num_boost_round'],valid_sets=[vs],valid_names=['validation'],
        callbacks=[lgb.early_stopping(p['model']['early_stopping_rounds'],verbose=False),lgb.log_evaluation(0),resource_callback])
    train_seconds=time.monotonic()-start;start=time.monotonic()
    pred=model.predict(v,num_iteration=model.best_iteration,num_threads=2)
    score=float(np.abs(yv-pred).mean())
    if not np.isfinite(score): raise ValueError('Nonfinite validation score')
    r={'candidate_id':candidate['candidate_id'],'validation_log_mae':score,
        'best_iteration':model.best_iteration,'parameters':params,
        'training_seconds':train_seconds,'prediction_seconds':time.monotonic()-start}
    text=model.model_to_string(num_iteration=model.best_iteration)
    del model,ds,vs;gc.collect()
    return r,text,pred

def load_seed(bundle,seed,p):
    path=Path(bundle)/'eligible.parquet'
    membership=pq.read_table(path,columns=['workload_id','row_ordinal']).to_pandas()
    if not membership.row_ordinal.is_unique: raise ValueError('Duplicate row ordinals')
    ids=membership.workload_id.drop_duplicates().tolist();q={**p,'split':{**p['split'],'seed':seed}}
    assignment={w:ref.assign_workload(w,q) for w in ids}
    counts={s:{'workloads':sum(v==s for v in assignment.values()),
        'rows':int(membership.workload_id.map(assignment).eq(s).sum())} for s in ['train','validation','test']}
    del membership,ids;gc.collect()
    features=ref.feature_columns(p,'R+P+A','m1','workload_disjoint')
    frames={}
    for s in ['train','validation']:
        allowed=[w for w,t in assignment.items() if t==s]
        # Test membership computed using IDs only; test outcomes excluded by scanner predicate.
        d=pq.read_table(path,columns=['workload_id','row_ordinal','duration_hours']+features,
            filters=[('workload_id','in',allowed)]).to_pandas().sort_values('row_ordinal').reset_index(drop=True)
        if len(d)!=counts[s]['rows'] or set(d.workload_id)!=set(allowed): raise ValueError('Split mismatch')
        if not np.isfinite(d.duration_hours).all() or not (d.duration_hours>0).all(): raise ValueError('Invalid eligible labels')
        frames[s]=d
    if set(frames['train'].workload_id)&set(frames['validation'].workload_id): raise ValueError('Workload leakage')
    del assignment;gc.collect()
    return frames,counts


def verify_seed(path,binding,spec):
    """Verify every completed unit, including unselected models, without data reads."""
    path=Path(path);summary=read_unit(path/'SUMMARY',binding);p=load_protocol()
    for role in ['m0','m1']:
        selected=read_unit(path/role/'SELECTION',{**binding,'role':role})
        cols=ref.feature_columns(p,'R+P+A',role,'workload_disjoint')
        if selected['features']!=cols or selected['test_used'] is not False:
            raise ValueError('Selection feature/test policy changed')
        if set(selected['encoding'])!={c for c in cols if c in p['encoding']['native_categorical']}:
            raise ValueError('Selection vocabulary columns changed')
        records=[]
        for candidate in p['model']['hyperparameter_grid']:
            cp=path/role/f"candidate_{candidate['candidate_id']:02d}"
            cb={**binding,'role':role,'candidate':candidate,'encoding_sha256':digest(selected['encoding'])}
            record=read_unit(cp,cb)
            if record['parameters']!=ref.parameters(p,candidate,spec['model_seed']):
                raise ValueError('Candidate parameters changed')
            records.append(record)
        best=min(records,key=lambda z:(z['validation_log_mae'],z['candidate_id']))
        if records!=selected['all_candidates'] or best!=selected['selected']:
            raise ValueError('Selection does not match committed candidates')
        winner_model=path/role/f"candidate_{best['candidate_id']:02d}"/'model.txt'
        if sha(winner_model)!=sha(path/role/'SELECTION'/'model.txt'):
            raise ValueError('Selected model differs from winning candidate')
        winner=summary['winners'][role]
        if winner['candidate_id']!=best['candidate_id'] or winner['best_iteration']!=best['best_iteration']:
            raise ValueError('Summary winner mismatch')
        if abs(winner['execution_logmae']-best['validation_log_mae'])>1e-12:
            raise ValueError('Summary validation score mismatch')
    return summary

def seed_run(bundle,out,seed):
    out=Path(out);spec,h=active_spec(bundle,out)
    if seed not in spec['split_seeds']: raise ValueError('Unregistered split seed')
    if seed!=spec['pilot_seed']: verify_pilot(out,h,spec)
    seedpath=out/'seeds'/str(seed);binding={'preregistration':h,'split_seed':seed}
    recover_partial(seedpath/'SUMMARY')
    if (seedpath/'SUMMARY').exists():
        result=verify_seed(seedpath,binding,spec)
        if seed==spec['pilot_seed']: publish_pilot(out,h,spec,result)
        return result
    started=time.monotonic();p=load_protocol()
    with Resources(spec['rss_limit_bytes'],spec['reserve_bytes']) as monitor:
        frames,counts=load_seed(bundle,seed,p);monitor.guard()
        diagnostics={'counts':counts,'test_outcomes_accessed':False,'roles':{},
            'concentration':{s:concentration(d.workload_id) for s,d in frames.items()},
            'lifecycle_execution_counts':{s:d.job_type_public.value_counts(dropna=False).to_dict() for s,d in frames.items()}}
        y=np.log1p(frames['train'].duration_hours.to_numpy());yv=np.log1p(frames['validation'].duration_hours.to_numpy())
        validids=frames['validation'].workload_id.to_numpy();winners={};winner_preds={};all_records=[]
        for role in ['m0','m1']:
            cols=ref.feature_columns(p,'R+P+A',role,'workload_disjoint')
            enc=ref.fit_encoding(frames['train'],cols,p)
            x=ref.encode(frames['train'],cols,enc,p);v=ref.encode(frames['validation'],cols,enc,p)
            diagnostics['roles'][role]={'features':cols,'profile_support':profile_support(x,v),
                'unknown_category_validation_fraction':{c:float((v[c]==-1).mean()) for c in enc}}
            records=[]
            for candidate in p['model']['hyperparameter_grid']:
                cp=seedpath/role/f"candidate_{candidate['candidate_id']:02d}"
                cb={**binding,'role':role,'candidate':candidate,'encoding_sha256':digest(enc)}
                recover_partial(cp)
                if cp.exists(): r=read_unit(cp,cb)
                else:
                    monitor.guard();r,text,pred=fit_candidate(x,y,v,yv,enc,p,candidate,spec['model_seed'],monitor)
                    r['validation_metrics']=loss_metrics(yv,pred,validids);r['resources_so_far']=monitor.result()
                    save_unit(cp,cb,r,{'model.txt':text.encode()})
                    del pred
                records.append(r);all_records.append(r)
                old=r['resources_so_far']
                monitor.peak=max(monitor.peak,old['peak_rss_bytes_sampled'])
                monitor.minimum=min(monitor.minimum,old['minimum_available_bytes_sampled'])
                print(json.dumps({'seed':seed,'role':role,'candidate':r['candidate_id'],
                    'validation_logmae':r['validation_log_mae'],'rounds':r['best_iteration']}),flush=True)
            best=min(records,key=lambda r:(r['validation_log_mae'],r['candidate_id']))
            selected=seedpath/role/'SELECTION';sb={**binding,'role':role};recover_partial(selected)
            selected_result={'features':cols,'encoding':enc,'selected':best,'all_candidates':records,'test_used':False}
            if selected.exists():
                if read_unit(selected,sb)!=selected_result: raise ValueError('Selection mismatch')
            else:
                source=seedpath/role/f"candidate_{best['candidate_id']:02d}"/'model.txt'
                save_unit(selected,sb,selected_result,{'model.txt':source.read_bytes()})
            model=lgb.Booster(model_file=str(selected/'model.txt'))
            prediction=model.predict(v,num_iteration=best['best_iteration'],num_threads=2)
            actual=loss_metrics(yv,prediction,validids)
            if abs(actual['execution_logmae']-best['validation_log_mae'])>1e-12: raise ValueError('Winner score mismatch')
            winners[role]={**actual,'candidate_id':best['candidate_id'],'best_iteration':best['best_iteration']}
            winner_preds[role]=prediction
            del x,v,enc,model;gc.collect();monitor.guard()
        errors={k:np.abs(yv-z) for k,z in winner_preds.items()}
        codes,ids=pd.factorize(validids,sort=False);n=np.bincount(codes)
        sums={k:np.bincount(codes,weights=z) for k,z in errors.items()}
        order=np.argsort(-n);top=order[:max(1,math.ceil(.01*len(n)))];benefit=sums['m0']-sums['m1']
        diagnostics['error_concentration']={'top1pct_by_execution_frequency':{
            k:float(z[top].sum()/z.sum()) if z.sum()>0 else None for k,z in sums.items()},
            'net_m0_minus_m1_loss_sum':float(benefit.sum()),
            'top1pct_by_execution_frequency_net_loss_difference':float(benefit[top].sum()),
            'positive_workload_loss_difference_sum':float(benefit[benefit>0].sum()),
            'negative_workload_loss_difference_sum':float(benefit[benefit<0].sum())}
        by_workload=pd.DataFrame({'workload_id':ids,'executions':n,'m0_loss_sum':sums['m0'],'m1_loss_sum':sums['m1']})
        import io
        buf=io.BytesIO();by_workload.to_parquet(buf,index=False)
        result={'split_seed':seed,'model_seed':spec['model_seed'],'label':'VALIDATION ONLY; selected on these validation outcomes',
            'winners':winners,'diagnostics':diagnostics,'elapsed_seconds':time.monotonic()-started,
            'candidate_compute_seconds':sum(z['training_seconds']+z['prediction_seconds'] for z in all_records),
            'elapsed_note':'wall time for current invocation only; candidate_compute_seconds includes resumed completed candidates'}
        for key in ['execution_logmae','equal_workload_logmae']:
            a=winners['m0'][key];b=winners['m1'][key]
            result[key+'_m0_minus_m1']=a-b
            result[key+'_relative_improvement_percent']=100*(a-b)/a if a else None
    monitor.guard()
    result['resources']=monitor.result()
    save_unit(seedpath/'SUMMARY',binding,result,{'validation_workload_loss_sums.parquet':buf.getvalue()})
    if seed==spec['pilot_seed']: publish_pilot(out,h,spec,result)
    return result

def publish_pilot(out,h,spec,result):
    gp=Path(out)/'PILOT';recover_partial(gp)
    if gp.exists():
        gate=read_unit(gp,{'preregistration':h})
    else:
        gate={'passed':result['resources']['peak_rss_bytes_sampled']<=spec['rss_limit_bytes'] and
            result['resources']['minimum_available_bytes_sampled']>=spec['reserve_bytes'],
            'seed':spec['pilot_seed'],'candidate_fits':24,'elapsed_seconds':result['elapsed_seconds'],
            'candidate_compute_seconds':result['candidate_compute_seconds'],
            'resources':result['resources'],'estimated_total_candidate_compute_seconds':10*result['candidate_compute_seconds'],
            'estimate_caveat':'one seed; excludes input preparation, diagnostics, Drive and scheduling overhead',
            'environment':environment()}
        save_unit(gp,{'preregistration':h},gate,{})
    if not gate['passed']: raise MemoryError('Pilot failed; remaining seeds prohibited')
    return gate

def verify_pilot(out,h,spec):
    gate=read_unit(Path(out)/'PILOT',{'preregistration':h})
    pilot=verify_seed(Path(out)/'seeds'/str(spec['pilot_seed']),{'preregistration':h,'split_seed':spec['pilot_seed']},spec)
    if not gate['passed'] or gate['candidate_fits']!=24: raise ValueError('Pilot did not pass')
    if gate['environment']['ram_bytes']!=psutil.virtual_memory().total: raise ValueError('Runtime RAM changed; use a new run and pilot')
    return gate

def report(bundle,out):
    out=Path(out);spec,h=active_spec(bundle,out);rows=[];candidates=[];diagnostics={};failure_history=[]
    for file in sorted(out.glob('FAILURE_*.json')):
        failure_history.append(json.loads(file.read_text()))
    for seed in spec['split_seeds']:
        path=out/'seeds'/str(seed);cp=path/'SUMMARY';base={'split_seed':seed}
        if not (cp/'COMMIT.json').exists():
            failures=[f for f in failure_history if f.get('seed')==seed]
            row={**base,'status':'failed' if failures else ('partial' if path.exists() else 'not_started')}
            if failures: row['last_error']=failures[-1]['error']
            rows.append(row)
            for role in ['m0','m1']:
                for candidate in load_protocol()['model']['hyperparameter_grid']:
                    unit=path/role/f"candidate_{candidate['candidate_id']:02d}"
                    if not (unit/'COMMIT.json').exists():continue
                    try:
                        cb=json.loads((unit/'COMMIT.json').read_text())['binding']
                        if any(cb.get(k)!=v for k,v in {'preregistration':h,'split_seed':seed,'role':role,'candidate':candidate}.items()):raise ValueError('Candidate binding mismatch')
                        c=read_unit(unit,cb);candidates.append({**base,'role':role,**c})
                    except Exception as e: row['status']='corrupt';row['last_error']=str(e)
            continue
        try:
            z=verify_seed(path,{'preregistration':h,'split_seed':seed},spec);row={**base,'status':'complete','elapsed_seconds':z['elapsed_seconds']}
            diagnostics[str(seed)]={'diagnostics':z['diagnostics'],'resources':z['resources']}
            for role in ['m0','m1']:
                for k,v in z['winners'][role].items(): row[role+'_'+k]=v
                selection=read_unit(path/role/'SELECTION',{'preregistration':h,'split_seed':seed,'role':role})
                for c in selection['all_candidates']:candidates.append({**base,'role':role,**c})
            for k,v in z.items():
                if k.endswith('_m0_minus_m1') or k.endswith('_relative_improvement_percent'):row[k]=v
            rows.append(row)
        except Exception as e: rows.append({**base,'status':'corrupt','error':str(e)})
    frame=pd.DataFrame(rows);dest=out/'reports';dest.mkdir(exist_ok=True)
    # Reports are derived snapshots; immutable numbered files, never overwrite an earlier report.
    name='report_'+str(time.time_ns());frame.to_csv(dest/(name+'.csv'),index=False)
    complete=frame[frame.status=='complete'];summary={'label':'VALIDATION ONLY; restricted-population robustness',
        'confirmatory_tests':'untouched and unevaluated','seed_status_counts':frame.status.value_counts().to_dict(),
        'all_ten_complete':len(complete)==10,'seed_outcomes':rows,'candidate_outcomes':candidates,
        'completed_seed_diagnostics':diagnostics,'failure_history':failure_history,
        'warning':'Overlapping split samples are dependent; validation winners are optimistically selected. No confirmatory or independent-seed p-value claim.'}
    for metric in ['execution_logmae','equal_workload_logmae']:
        key=metric+'_m0_minus_m1'
        if key in complete:
            a=complete[key].dropna().to_numpy()
            summary[metric+'_seed_summary']={'n':len(a),'mean':float(a.mean()),'median':float(np.median(a)),
                'min':float(a.min()),'max':float(a.max()),'sample_sd':float(np.std(a,ddof=1)) if len(a)>1 else None,
                'm1_better_seeds':int(np.sum(a>0)),'tied_seeds':int(np.sum(a==0)),'m0_better_seeds':int(np.sum(a<0))}
    (dest/(name+'.json')).write_bytes(canonical(summary))
    print(frame.to_string(index=False));print('Saved',dest/name,flush=True)
    return summary

def main():
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['register','seed','report'])
    ap.add_argument('--bundle',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--seed',type=int);args=ap.parse_args()
    try:
        if args.phase=='register': preregister(args.bundle,args.out)
        elif args.phase=='seed': seed_run(args.bundle,args.out,args.seed)
        else: report(args.bundle,args.out)
    except Exception as e:
        args.out.mkdir(parents=True,exist_ok=True)
        failure={'phase':args.phase,'seed':args.seed,'error_type':type(e).__name__,'error':str(e),'unix':time.time()}
        (args.out/('FAILURE_'+str(time.time_ns())+'.json')).write_bytes(canonical(failure))
        raise
if __name__=='__main__': main()

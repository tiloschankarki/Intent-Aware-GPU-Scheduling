"""Paired descriptive metrics and execution-weighted workload bootstrap."""
import numpy as np
import pandas as pd

METADATA = ['row_ordinal', 'workload_id', 'job_type_public', 'duration_hours']

def pair_predictions(m0, m1):
    """Require identical ordered physical rows and metadata; never join/drop rows."""
    for f in (m0,m1):
        if not set(METADATA+['prediction']).issubset(f.columns):
            raise ValueError('Missing prediction columns')
        if f.row_ordinal.isna().any() or f.row_ordinal.duplicated().any():
            raise ValueError('Null or duplicate physical row ordinal')
    a=m0.reset_index(drop=True); b=m1.reset_index(drop=True)
    if not a[METADATA].equals(b[METADATA]):
        raise ValueError('Prediction row IDs/order or paired metadata differ')
    out=a[METADATA].copy(); out['pred_m0']=a.prediction; out['pred_m1']=b.prediction
    return out

def _validate(frame, evaluation):
    if evaluation not in ('workload_disjoint','random_execution'):
        raise ValueError('Unsupported evaluation')
    if not set(METADATA+['pred_m0','pred_m1']).issubset(frame.columns) or frame.empty:
        raise ValueError('Missing columns or empty paired evaluation')
    if frame.row_ordinal.isna().any() or frame.row_ordinal.duplicated().any():
        raise ValueError('Null or duplicate physical row ordinal')
    if not np.isfinite(frame[['duration_hours','pred_m0','pred_m1']].to_numpy(dtype=float)).all() or (frame.duration_hours<=0).any():
        raise ValueError('Duration must be finite positive; predictions finite')
    if evaluation=='workload_disjoint' and frame.workload_id.isna().any():
        raise ValueError('Grouped evaluation requires non-null workload IDs')

def _spearman(y,p):
    if len(y)<2 or np.ptp(y)==0 or np.ptp(p)==0: return None
    # Average ranks are the definition of Spearman, including ties.
    r=float(np.corrcoef(pd.Series(y).rank(),pd.Series(p).rank())[0,1])
    return r if np.isfinite(r) else None

def _summary(f):
    result={'n':len(f)}
    if not len(f):
        return dict(result,m0=None,m1=None,absolute_gain=None,relative_gain_percent=None)
    y=np.log1p(f.duration_hours.to_numpy(dtype=float)); maes=[]
    for role in ('m0','m1'):
        p=f['pred_'+role].to_numpy(dtype=float); mae=float(np.mean(np.abs(y-p)));maes.append(mae)
        with np.errstate(over='ignore',invalid='ignore'):
            errors=np.abs(np.expm1(np.maximum(p,0))-f.duration_hours.to_numpy(dtype=float))
        finite=bool(np.isfinite(errors).all())
        with np.errstate(over='ignore'):
            mean=float(errors.mean()) if finite else None
        result[role]={'log_mae':mae,'spearman':_spearman(y,p),'runtime_mae_hours':mean if mean is not None and np.isfinite(mean) else None,'runtime_median_absolute_error_hours':float(np.median(errors)) if finite else None,'runtime_overflow_rows':int((~np.isfinite(errors)).sum())}
    result['absolute_gain']=maes[0]-maes[1]
    result['relative_gain_percent']=100*(maes[0]-maes[1])/maes[0] if maes[0]!=0 else None
    return result

def bootstrap_replicates(frame, replicates, seed, *, draws=None):
    """Aggregate sums/counts, then sample K workload IDs K times each replicate."""
    _validate(frame,'workload_disjoint')
    y=np.log1p(frame.duration_hours.to_numpy(dtype=float))
    agg=pd.DataFrame({'workload_id':frame.workload_id.to_numpy(),'e0':np.abs(y-frame.pred_m0.to_numpy()),'e1':np.abs(y-frame.pred_m1.to_numpy()),'n':1}).groupby('workload_id',sort=True)[['e0','e1','n']].sum().to_numpy()
    rng=np.random.default_rng(seed); k=len(agg); out=[]
    if draws is not None and np.asarray(draws).shape!=(replicates,k): raise ValueError('Invalid bootstrap draws shape')
    for i in range(replicates):
        ix=rng.integers(0,k,size=k) if draws is None else draws[i]
        sums=agg[ix].sum(axis=0); a,b=sums[:2]/sums[2]
        out.append({'replicate':i,'m0_log_mae':float(a),'m1_log_mae':float(b),'absolute_gain':float(a-b),'relative_gain_percent':float(100*(a-b)/a) if a!=0 else None,'sampled_execution_rows':int(sums[2])})
    return out

def paired_report(frame, protocol, evaluation):
    _validate(frame,evaluation)
    bins=protocol['metrics']['tail_bins_hours']; labels=protocol['metrics']['tail_labels']
    out={'evaluation':evaluation,'overall':_summary(frame),'lifecycle':{},'tail':[],'finite':_summary(frame[frame.job_type_public.isin(protocol['finite_categories'])]),'bootstrap':None}
    for label in protocol['primary_lifecycle_categories']:
        out['lifecycle'][label]=_summary(frame[frame.job_type_public==label])
    for lo,hi,label in zip(bins,bins[1:],labels):
        f=frame[(frame.duration_hours>=lo)&(True if hi is None else frame.duration_hours<hi)]
        out['tail'].append(dict(label=label,lower_hours=lo,upper_hours=hi,**_summary(f)))
    if evaluation=='workload_disjoint':
        u=protocol['uncertainty']; reps=bootstrap_replicates(frame,u['replicates'],u['seed'])
        absolute=[r['absolute_gain'] for r in reps]; relative=[r['relative_gain_percent'] for r in reps if r['relative_gain_percent'] is not None]
        out['bootstrap']={'unit':'workload_id','weighting':'execution_rows','seed':u['seed'],'replicates':u['replicates'],'confidence_level':0.95,'method':'percentile','absolute_ci95':np.percentile(absolute,[2.5,97.5]).tolist(),'relative_ci95':np.percentile(relative,[2.5,97.5]).tolist() if relative else None,'absolute_valid_replicates':len(absolute),'relative_valid_replicates':len(relative),'relative_undefined_replicates':len(reps)-len(relative),'samples':reps}
    return out

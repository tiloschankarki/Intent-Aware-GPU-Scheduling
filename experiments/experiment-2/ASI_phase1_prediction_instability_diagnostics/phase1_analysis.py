"""Exploratory Phase 1 diagnostics. Saved models only; no training or test data.
Run: /opt/homebrew/Caskroom/miniconda/base/bin/python phase1_analysis.py
Then: python build_findings.py to regenerate the narrative and final manifest.
"""
from pathlib import Path
import datetime,gc,hashlib,itertools,json,math,platform,sys,time
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import lightgbm as lgb
from scipy.stats import spearmanr

ROOT=Path(__file__).resolve().parent
PRIOR=ROOT.parent/'ASI_instability_mitigation'
RECOVERY=ROOT.parent/'ASI_recovery_20260927'
SEEDS=[20260927,20261020]
TYPES=['training','online_inference','offline_inference','dev']
FEATS=['job_type_public','gpu_spec_public','model_type_public','gpu_request','priority_class','is_genai_request']
M0=['gpu_request','gpu_spec_public','priority_class','model_type_public','is_genai_request']
TRIPLES=[('job_type_public','gpu_spec_public','model_type_public'),('job_type_public','gpu_spec_public','gpu_request'),('job_type_public','model_type_public','gpu_request')]
FAMILIES=[(c,) for c in FEATS]+list(itertools.combinations(FEATS,2))+TRIPLES
POP_FAMILIES=[(),('gpu_spec_public',),('model_type_public',),('gpu_spec_public','model_type_public')]
INPUT_LOG={}

def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write_json(p,x):Path(p).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def close(a,b,atol=1e-9):assert np.isclose(a,b,rtol=1e-9,atol=atol),(a,b)
def checked(p,expected=None):
 p=Path(p);h=sha(p)
 if expected:assert h==expected,(str(p),h,expected)
 INPUT_LOG[str(p.resolve())]={'sha256':h,'bytes':p.stat().st_size};return p

def workload_table(d):
 z=d[['workload_id','y','p0','p1']].copy()
 z['r0']=z.y-z.p0;z['r1']=z.y-z.p1;z['e0']=abs(z.r0);z['e1']=abs(z.r1);z['delta']=z.e1-z.e0
 w=z.groupby('workload_id',sort=False,observed=True).agg(executions=('y','size'),mean_log_duration=('y','mean'),median_log_duration=('y','median'),residual_m0=('r0','mean'),residual_m1=('r1','mean'),mae_m0=('e0','mean'),mae_m1=('e1','mean'),mean_delta=('delta','mean'),delta_sum=('delta','sum')).reset_index()
 w['workload_id']=w.workload_id.astype(str)
 n=w.executions.sum();nw=len(w)
 w['frequency_duration_tilt']=(w.executions/n-1/nw)*w.mean_log_duration
 w['duration_mass']=w.executions*w.mean_log_duration/n
 w['frequency_rank']=0;w.loc[w.sort_values(['executions','workload_id'],ascending=[False,True]).index,'frequency_rank']=np.arange(1,nw+1)
 w['excess_rank']=0;w.loc[w.sort_values(['delta_sum','workload_id'],ascending=[False,True]).index,'excess_rank']=np.arange(1,nw+1)
 w['absolute_tilt_rank']=0;w.loc[w.assign(a=abs(w.frequency_duration_tilt)).sort_values(['a','workload_id'],ascending=[False,True]).index,'absolute_tilt_rank']=np.arange(1,nw+1)
 return w

def overlap(a,b):
 a=set(a);b=set(b)
 return {'intersection':len(a&b),'jaccard':len(a&b)/len(a|b) if a|b else 0.,'fraction_of_first':len(a&b)/len(a) if a else 0.}

def symmetric_decomposition(t,v):
 x=t.merge(v,on='cell',how='outer',suffixes=('_t','_v'))
 common=x.mu_t.notna()&x.mu_v.notna()
 composition=((x.loc[common,'q_v']-x.loc[common,'q_t'])*(x.loc[common,'mu_v']+x.loc[common,'mu_t'])/2).sum()
 within=((x.loc[common,'mu_v']-x.loc[common,'mu_t'])*(x.loc[common,'q_v']+x.loc[common,'q_t'])/2).sum()
 unmatched=(x.loc[~common,'q_v'].fillna(0)*x.loc[~common,'mu_v'].fillna(0)-x.loc[~common,'q_t'].fillna(0)*x.loc[~common,'mu_t'].fillna(0)).sum()
 return {'composition':float(composition),'within_cell':float(within),'unmatched':float(unmatched)}

def population_cells(d,keys):
 z=d.copy(deep=False)
 if not keys:z=z.assign(_all='ALL');keys=['_all']
 z=z.assign(_weight=1/z.groupby('workload_id',observed=True).y.transform('size'))
 z['_weighted_y']=z._weight*z.y
 spec={'executions':('y','size'),'workloads':('workload_id','nunique'),'execution_mean':('y','mean'),'execution_median':('y','median'),'weight_mass':('_weight','sum'),'weighted_y_sum':('_weighted_y','sum')}
 if 'delta' in z:
  spec.update({'mae_m0':('e0','mean'),'mae_m1':('e1','mean'),'delta_mean':('delta','mean'),'delta_sum':('delta','sum'),'residual_m0':('r0','mean'),'residual_m1':('r1','mean')})
 g=z.groupby(list(keys),observed=True,sort=False,dropna=False).agg(**spec).reset_index()
 g['cell']=[json.dumps(list(map(str,row)),separators=(',',':')) for row in g[list(keys)].itertuples(index=False,name=None)]
 g['q']=g.weight_mass/d.workload_id.nunique();g['p']=g.executions/len(d);g['mu']=g.weighted_y_sum/g.weight_mass
 close(g.q.sum(),1.)
 close((g.p*g.execution_mean).sum(),d.y.mean())
 close((g.q*g.mu).sum(),d.groupby('workload_id',observed=True).y.mean().mean())
 return g.drop(columns=list(keys)+['weight_mass','weighted_y_sum'])

def split_membership(ids,seed):
 values=np.array([int.from_bytes(hashlib.sha256(json.dumps([seed,str(w)],ensure_ascii=False,separators=(',',':')).encode()).digest()[:8],'big')/2**64 for w in ids])
 return np.where(values<.7,'train',np.where(values<.85,'validation','sealed'))

def canonicalize(d):
 d=d.copy()
 for c in FEATS:
  if c=='gpu_request':d[c]=d[c].map(lambda x:'<MISSING>' if pd.isna(x) else format(float(x),'.15g'))
  else:d[c]=d[c].astype(object).map(lambda x:'<MISSING>' if pd.isna(x) else str(x))
  d[c]=d[c].astype('category')
 return d

def encode(d,features,enc):
 x=pd.DataFrame(index=d.index)
 for col in features:
  if col in enc:x[col]=d[col].astype(object).map(lambda v:None if pd.isna(v) else str(v)).map({v:i for i,v in enumerate(enc[col])}).fillna(-1).astype('int32')
  else:x[col]=d[col].astype('float64')
 return x

def bootstrap(w,replicates=1000):
 count=w.executions.to_numpy(dtype=float);s0=count*w.mae_m0;s1=count*w.mae_m1;n=len(w);rng=np.random.default_rng(20261027)
 out=np.empty((replicates,4))
 for i in range(replicates):
  idx=rng.integers(0,n,size=n);den=count[idx].sum();b0=s0.iloc[idx].sum()/den;b1=s1.iloc[idx].sum()/den;e0=w.mae_m0.iloc[idx].mean();e1=w.mae_m1.iloc[idx].mean();out[i]=[b1-b0,100*(b1-b0)/b0,e1-e0,100*(e1-e0)/e0]
 vals=[(count*(w.mae_m1-w.mae_m0)).sum()/count.sum(),100*(s1.sum()-s0.sum())/s0.sum(),w.mae_m1.mean()-w.mae_m0.mean(),100*(w.mae_m1.mean()-w.mae_m0.mean())/w.mae_m0.mean()]
 return {k:{'point':float(v),'ci_low':float(np.quantile(out[:,i],.025)),'ci_high':float(np.quantile(out[:,i],.975))} for i,(k,v) in enumerate(zip(['execution_delta','execution_deterioration_percent','equal_workload_delta','equal_workload_deterioration_percent'],vals))}

def subgroup_table(d,keys,seed):
 g=d.groupby(list(keys),observed=True,dropna=False,sort=False)
 r=g.agg(executions=('y','size'),workloads=('workload_id','nunique'),mae_m0=('e0','mean'),mae_m1=('e1','mean'),delta_mean=('delta','mean'),delta_sum=('delta','sum'),residual_m0=('r0','mean'),residual_m1=('r1','mean'),positive_row_delta_sum=('positive_delta','sum')).reset_index()
 sub=d.groupby(list(keys)+['workload_id'],observed=True,dropna=False,sort=False)[['e0','e1']].mean().groupby(level=list(range(len(keys))),observed=True).mean().rename(columns={'e0':'equal_workload_mae_m0','e1':'equal_workload_mae_m1'})
 r=r.merge(sub,on=list(keys),how='left',validate='one_to_one')
 r['split_seed']=seed;r['family']=' × '.join(keys);r['dimensions']=len(keys);r['cell']=[json.dumps(list(map(str,v)),separators=(',',':')) for v in r[list(keys)].itertuples(index=False,name=None)]
 r['supported']=(r.executions>=1000)&(r.workloads>=50)
 r['global_net_share']=r.delta_sum/d.delta.sum();r['global_mae_gap_contribution']=r.delta_sum/len(d);r['global_positive_row_excess_share']=r.positive_row_delta_sum/d.positive_delta.sum();r['execution_coverage']=r.executions/len(d);r['workload_coverage']=r.workloads/d.workload_id.nunique()
 close(r.executions.sum(),len(d));close(r.delta_sum.sum(),d.delta.sum())
 return r

def concentration(w,seed,scope,global_n,global_delta,global_gross):
 rows=[];n=len(w);positive=w.delta_sum.clip(lower=0).sum();den=w.delta_sum.sum();tilt=w.frequency_duration_tilt.sum();duration=w.duration_mass.sum()
 for fraction in [.01,.05,.1]:
  k=math.ceil(fraction*n)
  sets={rank:set(w.loc[w[col]<=k,'workload_id']) for rank,col in [('frequency','frequency_rank'),('excess_error','excess_rank'),('absolute_duration_tilt','absolute_tilt_rank')]}
  for rank,ids in sets.items():
   z=w[w.workload_id.isin(ids)];delta=z.delta_sum.sum();o=overlap(sets['frequency'],sets['excess_error']);ot=overlap(sets['absolute_duration_tilt'],sets['excess_error'])
   rows.append({'split_seed':seed,'scope':scope,'ranking':rank,'fraction_workloads_requested':fraction,'selected_workloads':len(z),'scope_workloads':n,'selected_executions':int(z.executions.sum()),'scope_execution_share':z.executions.sum()/w.executions.sum(),'global_execution_share':z.executions.sum()/global_n,'m0_mae_selected':np.average(z.mae_m0,weights=z.executions),'m1_mae_selected':np.average(z.mae_m1,weights=z.executions),'delta_sum':delta,'global_mae_gap_contribution':delta/global_n,'scope_net_delta_share':delta/den if den else None,'global_net_delta_share':delta/global_delta,'scope_positive_workload_excess_share':z.delta_sum.clip(lower=0).sum()/positive if positive else None,'global_gross_error_mass_signed_share':delta/global_gross,'selected_duration_mass':z.duration_mass.sum(),'scope_duration_mass_share':z.duration_mass.sum()/duration if duration else None,'selected_frequency_duration_tilt':z.frequency_duration_tilt.sum(),'scope_frequency_duration_tilt':tilt,'frequency_error_overlap_workloads':o['intersection'],'frequency_error_jaccard':o['jaccard'],'frequency_error_overlap_fraction':o['fraction_of_first'],'tilt_error_overlap_workloads':ot['intersection'],'tilt_error_jaccard':ot['jaccard'],'tilt_error_overlap_fraction':ot['fraction_of_first']})
 return rows

def population_comparison(t,v,seed,scope,family,global_n,global_delta):
 x=t.merge(v,on='cell',how='outer',suffixes=('_train','_validation'),validate='one_to_one');common=x.mu_train.notna()&x.mu_validation.notna()
 qt=x.q_train.fillna(0);qv=x.q_validation.fillna(0);mt=x.mu_train.fillna(0);mv=x.mu_validation.fillna(0)
 x['equal_workload_composition_component']=np.where(common,(qv-qt)*(mv+mt)/2,0.)
 x['within_observed_cell_component']=np.where(common,(mv-mt)*(qv+qt)/2,0.)
 x['unmatched_cell_component']=np.where(~common,qv*mv-qt*mt,0.)
 pt=x.p_train.fillna(0);pv=x.p_validation.fillna(0);et=x.execution_mean_train.fillna(0);ev=x.execution_mean_validation.fillna(0)
 x['frequency_duration_association_component']=(pv*ev-qv*mv)-(pt*et-qt*mt)
 x['duration_mean_gap_contribution']=pv*ev-pt*et
 x['conditional_execution_mean_shift']=np.where(common,ev-et,np.nan);x['conditional_fractional_workload_mean_shift']=np.where(common,mv-mt,np.nan)
 x['delta_sum']=x.delta_sum.fillna(0);x['global_error_gap_contribution']=x.delta_sum/global_n;x['global_net_error_share']=x.delta_sum/global_delta
 x['supported_both']=(x.executions_train.fillna(0)>=1000)&(x.executions_validation.fillna(0)>=1000)&(x.workloads_train.fillna(0)>=50)&(x.workloads_validation.fillna(0)>=50)
 x['common_cell']=common;x['split_seed']=seed;x['scope']=scope;x['family']=family
 components=['equal_workload_composition_component','within_observed_cell_component','unmatched_cell_component','frequency_duration_association_component']
 close(x[components].sum().sum(),x.duration_mean_gap_contribution.sum(),atol=1e-10)
 close(x.delta_sum.sum(),v.delta_sum.sum())
 return x

def plots(workloads,concentration_frame,features,pop):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':160})
 fig,axes=plt.subplots(1,3,figsize=(12,3.7))
 for ax,scope in zip(axes,['ALL','online_inference','offline_inference']):
  for seed,color in zip(SEEDS,['#3569a8','#cf5f37']):
   w=workloads[(workloads.split_seed==seed)&(workloads.scope==scope)].sort_values('frequency_rank');ax.plot(np.arange(1,len(w)+1)/len(w)*100,np.cumsum(w.executions)/w.executions.sum()*100,label=str(seed),color=color)
  ax.plot([0,100],[0,100],color='0.7',linestyle=':');ax.set(xlim=(0,10),ylim=(0,100),xlabel='Top workloads by execution count (%)',title=scope.replace('_',' '));ax.grid(alpha=.15)
 axes[0].set_ylabel('Executions covered (%)');axes[0].legend();fig.tight_layout();fig.savefig(ROOT/'workload_frequency_concentration.png');plt.close(fig)
 # Contributions, not net percentage shares: positive bars mean M1 worse.
 f=features[features.family=='job_type_public'];fig,axes=plt.subplots(1,2,figsize=(10,3.8),sharey=True)
 for ax,seed in zip(axes,SEEDS):
  z=f[f.split_seed==seed].set_index('job_type_public').reindex(TYPES);ax.barh([x.replace('_',' ') for x in TYPES],z.global_mae_gap_contribution,color=['#c65742' if v>0 else '#39846a' for v in z.global_mae_gap_contribution]);ax.axvline(0,color='0.3',linewidth=.7);ax.set_title(str(seed));ax.set_xlabel('Contribution to M1 − M0 validation LogMAE');ax.grid(axis='x',alpha=.15)
 fig.tight_layout();fig.savefig(ROOT/'workload_type_error_contributions.png');plt.close(fig)
 fig,axes=plt.subplots(1,2,figsize=(11,4),sharey=True)
 for ax,seed in zip(axes,SEEDS):
  z=pop[(pop.split_seed==seed)&(pop.family=='type_only')&(pop.scope!='ALL')].set_index('scope').reindex(TYPES)
  y=np.arange(4);eq=z.equal_workload_composition_component+z.within_observed_cell_component+z.unmatched_cell_component;freq=z.frequency_duration_association_component
  ax.barh(y-.18,eq,height=.32,label='Equal-workload population mean change',color='#3569a8');ax.barh(y+.18,freq,height=.32,label='Frequency-duration association change',color='#cf5f37');ax.axvline(0,color='.3',lw=.7);ax.set_yticks(y,[v.replace('_',' ') for v in TYPES]);ax.set_title(str(seed));ax.set_xlabel('Validation − training mean log-duration');ax.grid(axis='x',alpha=.15)
 axes[0].legend(loc='lower left',fontsize=8);fig.tight_layout();fig.savefig(ROOT/'duration_shift_decomposition.png');plt.close(fig)


def main():
 started=utc();start=time.monotonic();assert not (ROOT/'workload_error_attribution.csv').exists(),'Refuse to overwrite completed diagnostics'
 audit=json.loads(checked(PRIOR/'phase_a_verification.json').read_text());old=json.loads(checked(PRIOR/'run_manifest.json').read_text())
 assert lgb.__version__=='4.7.0'
 recovery=json.loads(checked(RECOVERY/'verification.json').read_text())
 canonical=checked(RECOVERY/'primary.parquet','10a3a86c977701c3c26f0bdce231aeb294676d71fef772b96309ceab3d21b0a0')
 pf=pq.ParquetFile(canonical);assert pf.metadata.num_rows==4709624
 # No canonical row data is read; footer and opaque digest suffice to locate and identify it.
 checks={'canonical_path':str(canonical),'canonical_rows':pf.metadata.num_rows,'canonical_schema':str(pf.schema_arrow),'canonical_content_rows_read':0,'models':{},'splits':{},'historical_metric_reconciliation':{}}
 all_work=[];all_con=[];all_feature=[];all_pop=[];uncertainty=[];train_pop={};correlations=[];profiles=[]
 for seed in SEEDS:
  print(utc(),'verify/analyze',seed,flush=True);tr=audit['inputs'][str(seed)]['train'];va=audit['inputs'][str(seed)]['validation']
  p=checked(tr['path'],tr['sha256']);d=pq.read_table(p).to_pandas(categories=['workload_id','job_type_public','gpu_spec_public','model_type_public','priority_class']).sort_values('row_ordinal').reset_index(drop=True)
  assert len(d)==tr['rows'] and d.workload_id.nunique()==tr['workloads'] and d.workload_id.notna().all() and d.row_ordinal.is_unique
  ids=d.workload_id.cat.categories.astype(str);assert (split_membership(ids,seed)=='train').all();train_ids=set(ids)
  train_ord=np.sort(d.row_ordinal.to_numpy());assert d.grouped_split.eq('train').all()
  d['y']=np.log1p(d.duration_hours);assert np.isfinite(d.y).all();d=canonicalize(d)
  for scope in ['ALL']+TYPES:
   part=d if scope=='ALL' else d[d.job_type_public==scope]
   for keys in POP_FAMILIES:train_pop[(scope,keys)]=population_cells(part,list(keys))
  del d;gc.collect()
  p=checked(va['path'],va['sha256']);d=pq.read_table(p).to_pandas(categories=['workload_id','job_type_public','gpu_spec_public','model_type_public','priority_class']).sort_values('row_ordinal').reset_index(drop=True)
  assert len(d)==va['rows'] and d.workload_id.nunique()==va['workloads'] and d.workload_id.notna().all() and d.row_ordinal.is_unique
  ids=d.workload_id.cat.categories.astype(str);assert (split_membership(ids,seed)=='validation').all();assert not train_ids&set(ids);assert not np.isin(d.row_ordinal,train_ord).any();assert d.grouped_split.eq('validation').all()
  checks['splits'][str(seed)]={'train':tr,'validation':va,'workload_overlap':0,'row_ordinal_overlap':0,'all_unique_workload_SHA256_memberships_verified':True,'grouped_split_labels_verified':True}
  predpath=checked(PRIOR/f'validation_predictions_{seed}.parquet',old['outputs'][f'validation_predictions_{seed}.parquet']['sha256']);pred=pq.read_table(predpath).to_pandas()
  assert np.array_equal(d.row_ordinal,pred.row_ordinal) and np.array_equal(d.workload_id.astype(str),pred.workload_id.astype(str)) and np.array_equal(d.job_type_public.astype(str),pred.job_type_public.astype(str))
  d['y']=np.log1p(d.duration_hours.to_numpy());assert np.isfinite(d.y).all()
  for role in ['m0','m1']:
   rd=PRIOR/'artifacts'/str(seed)/role;b=audit['baselines'][f'{seed}_{role}']
   mp=checked(rd/'model.txt',b['model_sha256']);ep=checked(rd/'encoding.json',old['outputs'][str((rd/'encoding.json').relative_to(PRIOR))]['sha256'])
   metadata=checked(rd/('manifest.json' if seed==20260927 else 'selection.json'),old['outputs'][str((rd/('manifest.json' if seed==20260927 else 'selection.json')).relative_to(PRIOR))]['sha256'])
   enc=json.loads(ep.read_text());assert enc==b['encoding'];model=lgb.Booster(model_file=str(mp));assert model.feature_name()==M0+(['job_type_public'] if role=='m1' else []) and model.num_trees()==b['trees']
   regenerated=model.predict(encode(d,model.feature_name(),enc),num_threads=2);assert np.isfinite(regenerated).all();maxdiff=float(np.max(abs(regenerated-pred[role].to_numpy())));assert maxdiff<1e-12
   d['p0' if role=='m0' else 'p1']=pred[role].to_numpy();mae=float(np.mean(abs(d.y-regenerated)));assert abs(mae-b['reference'])<1e-10
   checks['models'][f'{seed}_{role}']={'path':str(mp),'encoding_path':str(ep),'selection_metadata_path':str(metadata),'trees':model.num_trees(),'features':model.feature_name(),'regenerated_cached_prediction_max_abs_diff':maxdiff,'validation_LogMAE':mae,'reference_LogMAE':b['reference'],'encoding':enc}
   print(seed,role,'verified',mae,'trees',model.num_trees(),'prediction maxdiff',maxdiff,flush=True);del model
  d=canonicalize(d);d['r0']=d.y-d.p0;d['r1']=d.y-d.p1;d['e0']=abs(d.r0);d['e1']=abs(d.r1);d['delta']=d.e1-d.e0;d['positive_delta']=d.delta.clip(lower=0)
  global_delta=d.delta.sum();gross=abs(d.delta).sum();N=len(d)
  for scope in ['ALL']+TYPES:
   z=d if scope=='ALL' else d[d.job_type_public==scope];w=workload_table(z);w['split_seed']=seed;w['scope']=scope
   w['global_net_contribution']=w.delta_sum/global_delta;w['global_mae_gap_contribution']=w.delta_sum/N;w['scope_absolute_workload_delta_normalized']=w.delta_sum/abs(w.delta_sum).sum();w['scope_positive_excess_share']=w.delta_sum.clip(lower=0)/w.delta_sum.clip(lower=0).sum()
   close(w.executions.sum(),len(z));close(w.delta_sum.sum(),z.delta.sum());close(np.average(w.mae_m0,weights=w.executions),z.e0.mean());close(np.average(w.mae_m1,weights=w.executions),z.e1.mean())
   all_work.append(w);all_con.extend(concentration(w,seed,scope,N,global_delta,gross));bs=bootstrap(w)
   # Profile top-1% selected workloads using observed feature combinations, not cross-split ID matching.
   k=math.ceil(.01*len(w))
   for rank,col in [('frequency','frequency_rank'),('excess_error','excess_rank'),('absolute_duration_tilt','absolute_tilt_rank')]:
    selected=set(w.loc[w[col]<=k,'workload_id']);subset=z[z.workload_id.isin(selected)]
    g=subset.groupby(['job_type_public','gpu_spec_public','model_type_public'],observed=True,sort=False).agg(executions=('y','size'),workloads=('workload_id','nunique'),mean_log_duration=('y','mean'),mae_m0=('e0','mean'),mae_m1=('e1','mean'),delta_sum=('delta','sum')).reset_index()
    g['split_seed']=seed;g['scope']=scope;g['ranking']=rank;g['selected_fraction']=.01;g['execution_share_in_selected']=g.executions/len(subset);g['global_error_gap_contribution']=g.delta_sum/N;profiles.append(g)
   for metric,values in bs.items():uncertainty.append({'split_seed':seed,'scope':scope,'metric':metric,**values})
   correlations.append({'split_seed':seed,'scope':scope,'spearman_execution_count_vs_delta_sum':float(spearmanr(w.executions,w.delta_sum).statistic),'spearman_execution_count_vs_mean_delta':float(spearmanr(w.executions,w.mean_delta).statistic),'spearman_abs_duration_tilt_vs_positive_workload_excess':float(spearmanr(abs(w.frequency_duration_tilt),w.delta_sum.clip(lower=0)).statistic),'execution_mean_log_duration':float(z.y.mean()),'equal_workload_mean_log_duration':float(w.mean_log_duration.mean()),'frequency_duration_association':float(w.frequency_duration_tilt.sum())})
   for keys in POP_FAMILIES:
    v=population_cells(z,list(keys));family='type_only' if not keys else 'type × '+' × '.join(keys)
    all_pop.append(population_comparison(train_pop[(scope,keys)],v,seed,scope,family,N,global_delta))
   if scope=='ALL':
    for role,metric in [('m0','mae_m0'),('m1','mae_m1')]:close(w[metric].mean(),audit['baselines'][f'{seed}_{role}']['equal_workload'],atol=1e-10)
  for keys in FAMILIES:all_feature.append(subgroup_table(d,keys,seed))
  checks['historical_metric_reconciliation'][str(seed)]={'m0':float(d.e0.mean()),'m1':float(d.e1.mean()),'delta':float(d.delta.mean()),'delta_sum':float(global_delta),'workload_sum_reconciled':True,'all_subgroup_families_sum_reconciled':True}
  del d,pred,train_ids,train_ord;train_pop.clear();gc.collect()
 work=pd.concat(all_work,ignore_index=True);con=pd.DataFrame(all_con);feature=pd.concat(all_feature,ignore_index=True);pop=pd.concat(all_pop,ignore_index=True)
 # Three-way support selection uses counts only; omitted cells are reported in an explicit coverage table.
 support=feature.groupby(['family','cell'],observed=True).supported.any();feature['supported_either_split']=[bool(support.loc[(a,b)]) for a,b in zip(feature.family,feature.cell)]
 keep=(feature.dimensions<3)|feature.supported_either_split
 coverage=[]
 for (seed,family),z in feature.groupby(['split_seed','family'],sort=False):
  k=keep.loc[z.index];coverage.append({'split_seed':seed,'family':family,'dimensions':int(z.dimensions.iloc[0]),'all_cells':len(z),'retained_cells':int(k.sum()),'total_executions':int(z.executions.sum()),'retained_executions':int(z.loc[k,'executions'].sum()),'omitted_executions':int(z.loc[~k,'executions'].sum()),'execution_coverage':float(z.loc[k,'executions'].sum()/z.executions.sum()),'total_delta_sum':float(z.delta_sum.sum()),'retained_delta_sum':float(z.loc[k,'delta_sum'].sum()),'omitted_delta_sum':float(z.loc[~k,'delta_sum'].sum())})
 # Add cross-split comparisons without pretending that the underlying workloads are paired.
 metrics=['supported','executions','workloads','delta_mean','global_mae_gap_contribution','mae_m0','mae_m1']
 cross=feature.pivot(index=['family','cell'],columns='split_seed',values=metrics);cross.columns=[f'{a}_{b}' for a,b in cross.columns];cross=cross.reset_index();cross['supported_both']=cross.supported_20260927.eq(True)&cross.supported_20261020.eq(True)
 cross['direction']=np.where(cross.delta_mean_20260927.gt(0)&cross.delta_mean_20261020.gt(0),'M1_worse_both',np.where(cross.delta_mean_20260927.lt(0)&cross.delta_mean_20261020.lt(0),'M1_better_both',np.where(cross.delta_mean_20260927.notna()&cross.delta_mean_20261020.notna(),'sign_reversal','absent_one_split')))
 work.to_csv(ROOT/'workload_error_attribution.csv',index=False);con.to_csv(ROOT/'workload_concentration.csv',index=False);feature.loc[keep].to_csv(ROOT/'feature_combination_errors.csv',index=False);pd.DataFrame(coverage).to_csv(ROOT/'subgroup_coverage.csv',index=False);cross.to_csv(ROOT/'cross_split_subgroup_comparison.csv',index=False);pop.to_csv(ROOT/'duration_shift_vs_error.csv',index=False);pd.DataFrame(uncertainty).to_csv(ROOT/'workload_cluster_uncertainty.csv',index=False);pd.DataFrame(correlations).to_csv(ROOT/'frequency_duration_error_associations.csv',index=False)
 pd.concat(profiles,ignore_index=True).to_csv(ROOT/'ranked_population_profiles.csv',index=False)
 write_json(ROOT/'verification_results.json',checks)
 plots(work,con,feature,pop)
 for p,z in INPUT_LOG.items():assert sha(p)==z['sha256'],'Source changed during analysis'
 manifest={'analysis_started_utc':started,'analysis_completed_utc':utc(),'elapsed_seconds':time.monotonic()-start,'status':'analysis_complete_reports_pending','inputs':INPUT_LOG,'canonical_identity_scope':'opaque hash and footer only; no canonical rows read','verification':checks,'software':{'python':sys.version,'platform':platform.platform(),'lightgbm':lgb.__version__,'numpy':np.__version__,'pandas':pd.__version__,'pyarrow':pa.__version__},'split_seeds':SEEDS,'bootstrap_seed':20261027,'bootstrap_replicates':1000,'models_retrained':False,'test_artifacts_accessed':False,'aborted_feasibility_file_accessed':False,'protocol_sha256':sha(ROOT/'analysis_protocol.md'),'analysis_code_sha256':sha(ROOT/'phase1_analysis.py'),'outputs':{}}
 for p in sorted(ROOT.iterdir()):
  if p.is_file() and p.name!='run_manifest.json':manifest['outputs'][p.name]={'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
 write_json(ROOT/'run_manifest.json',manifest)
 print('PHASE 1 NUMERICAL ANALYSIS VERIFIED',len(work),'workload rows;',len(feature.loc[keep]),'subgroup rows;',len(pop),'population cells',flush=True)

if __name__=='__main__':main()

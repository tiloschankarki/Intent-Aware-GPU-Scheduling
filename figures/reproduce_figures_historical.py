import os, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(Path(tempfile.gettempdir())/'asi-manuscript-mpl')
import json, hashlib, shutil
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
OUT=ROOT; DATA=OUT/'data'; FIG=OUT/'figures'
for p in [DATA,FIG]: p.mkdir(parents=True,exist_ok=True)
report=json.loads((ROOT/'data/exp3_report_original.json').read_text())
rows=pd.DataFrame(report['seed_outcomes']).sort_values('split_seed')
assert len(rows)==10 and len(report['candidate_outcomes'])==240
for role in ['m0','m1']:
 for _,r in rows.iterrows():
  candidates=[c for c in report['candidate_outcomes'] if c['split_seed']==r.split_seed and c['role']==role]
  assert len(candidates)==12
  winner=min(candidates,key=lambda c:(c['validation_log_mae'],c['candidate_id']))
  assert winner['candidate_id']==r[f'{role}_candidate_id']
  for metric in ['execution','equal_workload']:
   assert abs(winner['validation_metrics'][metric+'_logmae']-r[f'{role}_{metric}_logmae'])<1e-12
for metric in ['execution','equal_workload']:
 d=rows[f'm0_{metric}_logmae']-rows[f'm1_{metric}_logmae']
 assert np.max(np.abs(d-rows[f'{metric}_logmae_m0_minus_m1']))<1e-12
 assert abs(d.mean()-report[f'{metric}_logmae_seed_summary']['mean'])<1e-12
rows.to_csv(DATA/'exp3_selected_validation.csv',index=False)
pd.DataFrame([{k:v for k,v in c.items() if k in ['split_seed','role','candidate_id','best_iteration','validation_log_mae']} for c in report['candidate_outcomes']]).to_csv(DATA/'exp3_candidate_records.csv',index=False)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','axes.titleweight':'bold','savefig.facecolor':'white'})
BLUE='#0072B2'; ORANGE='#D55E00'; GREY='#60666D'
def save(fig,name):
 for ext in ['pdf','svg','png']: fig.savefig(FIG/f'{name}.{ext}',dpi=300,bbox_inches='tight',pad_inches=.08)
 plt.close(fig)
# Historical report values only; seeds vary fitting randomness on one fixed split.
exp1=pd.DataFrame({'model_seed':[20260927,20260928,20260929], 'resource_priority_gain_percent':[5.949393,5.844247,5.848031], 'strong_control_gain_percent':[.9461680302805315,.8146718638233289,1.3786733005941791], 'strong_ci_low':[-1.1556693288810944,-1.3238907068013972,-.7554450700737221], 'strong_ci_high':[2.5580923336846935,2.402525207340963,3.014961178061143]})
exp1.to_csv(DATA/'exp1_historical_report_values.csv',index=False)
fig,axs=plt.subplots(1,2,figsize=(7.1,2.7),layout='constrained')
for j,(_,r) in enumerate(exp1.iterrows()):
 axs[0].plot([0,1],[r.resource_priority_gain_percent,r.strong_control_gain_percent],color=GREY,alpha=.6,lw=1)
 axs[0].scatter([0,1],[r.resource_priority_gain_percent,r.strong_control_gain_percent],color=[BLUE,ORANGE],s=25,zorder=3)
axs[0].set(xticks=[0,1],xticklabels=['Resource + priority','+ application controls'],ylabel='M1 LogMAE improvement (%)',title='(a) Baseline dependence',xlim=(-.2,1.2),ylim=(-.3,6.7))
y=np.arange(3)
axs[1].errorbar(exp1.strong_control_gain_percent,y,xerr=[exp1.strong_control_gain_percent-exp1.strong_ci_low,exp1.strong_ci_high-exp1.strong_control_gain_percent],fmt='o',color=ORANGE,capsize=3)
axs[1].set(yticks=y,yticklabels=exp1.model_seed.astype(str),xlabel='Strong-control improvement (%)',title='(b) Historical conditional 95% intervals')
axs[1].axvline(0,color=GREY,lw=.8);axs[1].invert_yaxis()
save(fig,'fig01_historical_test')
fig,ax=plt.subplots(figsize=(7.1,3.5),layout='constrained');y=np.arange(10)
ax.axvline(0,color=GREY,lw=.8)
for metric,off,col,marker,label in [('execution',-.13,BLUE,'o','Execution weighted'),('equal_workload',.13,ORANGE,'s','Equal workload')]:
 vals=rows[f'{metric}_logmae_relative_improvement_percent'].to_numpy()
 ax.scatter(vals,y+off,color=col,marker=marker,s=27,label=label,zorder=3)
 for x,yy in zip(vals,y+off):ax.annotate(f'{x:+.2f}',(x,yy),xytext=(5 if x>=0 else -5,0),textcoords='offset points',ha='left' if x>=0 else 'right',va='center',fontsize=7)
ax.set(yticks=y,yticklabels=rows.split_seed.astype(str),xlabel='Selected-validation M1 LogMAE improvement (%)',ylabel='Partition seed (identifier)',xlim=(-7.8,6),title='Experiment 3: ranking depends on partition and weighting')
ax.invert_yaxis();ax.legend(loc='lower left',frameon=False,fontsize=8);ax.grid(axis='x',alpha=.15)
save(fig,'fig02_partition_weighting')
diagnostics=[]
for _,r in rows.iterrows():
 d=report['completed_seed_diagnostics'][str(int(r.split_seed))]['diagnostics'];e=d['error_concentration'];n=r.m0_rows
 diagnostics.append({'split_seed':r.split_seed,'top1pct_execution_share_percent':100*d['concentration']['validation']['top1pct_execution_share'],'top1pct_gain_contribution':e['top1pct_by_execution_frequency_net_loss_difference']/n,'remaining_gain_contribution':(e['net_m0_minus_m1_loss_sum']-e['top1pct_by_execution_frequency_net_loss_difference'])/n})
diag=pd.DataFrame(diagnostics);diag.to_csv(DATA/'exp3_concentration_attribution.csv',index=False)
fig,axs=plt.subplots(1,2,figsize=(7.1,3.0),layout='constrained')
axs[0].scatter(diag.top1pct_execution_share_percent,rows.execution_logmae_relative_improvement_percent,c=BLUE,s=27)
for i in [0,4,5]:axs[0].annotate(str(int(rows.iloc[i].split_seed)),(diag.iloc[i].top1pct_execution_share_percent,rows.iloc[i].execution_logmae_relative_improvement_percent),xytext=(4,4),textcoords='offset points',fontsize=7)
axs[0].axhline(0,color=GREY,lw=.8);axs[0].set(xlabel='Executions in frequency-top 1% (%)',ylabel='M1 improvement (%)',title='(a) Concentration does not fix the sign')
ids=[20261028,20261101,20261102];sub=diag.set_index('split_seed').loc[ids]
for off,key,c,label in [(-.17,'top1pct_gain_contribution',BLUE,'Frequency-top 1%'),(.17,'remaining_gain_contribution',ORANGE,'Remaining workloads')]:
 axs[1].bar(np.arange(3)+off,sub[key],width=.32,color=c,label=label)
axs[1].axhline(0,color=GREY,lw=.8);axs[1].set(xticks=np.arange(3),xticklabels=[str(x) for x in ids],ylabel='Contribution to M0 − M1 LogMAE',title='(b) Signed attribution (selected cases)');axs[1].tick_params(axis='x',labelsize=7);axs[1].legend(frameon=False,fontsize=7)
save(fig,'fig03_concentration_attribution')
fig,axs=plt.subplots(1,2,figsize=(7.1,3),layout='constrained')
for role,col,mark in [('m0',BLUE,'o'),('m1',ORANGE,'s')]:
 axs[0].scatter(rows[f'{role}_best_iteration'],np.arange(10),color=col,marker=mark,s=24,label=role.upper())
axs[0].set(yticks=np.arange(10),yticklabels=rows.split_seed.astype(str),xlabel='Selected boosting rounds',title='(a) Selected complexity varies',xlim=(-5,210));axs[0].invert_yaxis();axs[0].legend(frameon=False,fontsize=8)
cs=pd.DataFrame(report['candidate_outcomes']);focus=20261101
for role,col,marker in [('m0',BLUE,'o'),('m1',ORANGE,'s')]:
 c=cs[(cs.split_seed==focus)&(cs.role==role)].sort_values('candidate_id')
 axs[1].scatter(c.candidate_id,c.validation_log_mae,color=col,marker=marker,s=24,label=role.upper())
axs[1].set(xlabel='Candidate ID',ylabel='Execution-weighted validation LogMAE',title=f'(b) All candidates, seed {focus}',xticks=[1,4,8,12]);axs[1].legend(frameon=False,fontsize=8)
save(fig,'fig04_selection_context')
fig,ax=plt.subplots(figsize=(7.1,2.1));ax.set_axis_off()
labels=[('Experiment 1','Historical test','One group split; three model seeds','Baseline-dependent increment'),('Experiment 2','Selected validation','Two group splits; fixed model seed','Localize reversal; mechanism unresolved'),('Experiment 3','Selected validation','Ten restricted-population\ngroup splits','Partition and weighting sensitivity')]
for i,(title,level,design,claim) in enumerate(labels):
 x=.015+i*.335
 ax.add_patch(FancyBboxPatch((x,.12),.30,.78,boxstyle='round,pad=0.012',facecolor='#F2F5F7',edgecolor=BLUE,lw=.9,transform=ax.transAxes))
 ax.text(x+.15,.77,title,ha='center',weight='bold',transform=ax.transAxes)
 ax.text(x+.15,.60,level,ha='center',color=ORANGE,transform=ax.transAxes)
 ax.text(x+.15,.42,design.replace('; ',';\n'),ha='center',va='center',fontsize=7.6,transform=ax.transAxes)
 ax.text(x+.15,.23,claim.replace('; ',';\n'),ha='center',va='center',fontsize=7.2,transform=ax.transAxes)
save(fig,'fig05_evidence_map')
exp2=pd.DataFrame({'partition_seed':[20260927,20261020], 'execution_gain_percent':[2.083576,-4.906626], 'equal_workload_gain_percent':[3.664494,-2.754915], 'shared_m0_logmae':[.854011,.839569], 'shared_m1_logmae':[.850717,.860921]})
exp2.to_csv(DATA/'exp2_reported_validation_values.csv',index=False)
fig,axs=plt.subplots(1,2,figsize=(7.1,2.8),layout='constrained')
for key,off,col,marker,label in [('execution_gain_percent',-.09,BLUE,'o','Execution weighted'),('equal_workload_gain_percent',.09,ORANGE,'s','Equal workload')]:
 axs[0].scatter(exp2[key],[0+off,1+off],c=col,marker=marker,s=30,label=label)
axs[0].axvline(0,color=GREY,lw=.8);axs[0].set(yticks=[0,1],yticklabels=exp2.partition_seed.astype(str),xlabel='Selected-validation M1 improvement (%)',title='(a) Two historical partitions',ylim=(1.5,-.5));axs[0].legend(frameon=False,fontsize=7,loc='lower left')
for key,off,col,marker,label in [('shared_m0_logmae',-.08,BLUE,'o','M0'),('shared_m1_logmae',.08,ORANGE,'s','M1')]:
 axs[1].scatter(exp2[key],[0+off,1+off],c=col,marker=marker,s=30,label=label)
axs[1].set(yticks=[0,1],yticklabels=['Original saved pair','Second saved pair'],xlabel='Shared-record LogMAE (lower is better)',title='(b) Same 100,221 validation records',ylim=(1.5,-.5));axs[1].legend(frameon=False,fontsize=7,loc='lower left')
save(fig,'fig06_historical_validation')
manifest={str(p.relative_to(OUT)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='manifest.json'}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(OUT/'verification.json').write_text(json.dumps({'seed_rows':10,'candidate_records':240,'selected_winners_match_minimum':20,'selected_metrics_reconciled':40,'new_training':False,'prediction_files_read':False,'holdout_files_read':False,'source':'original consolidated report, historical checkpoint, phase-one report','limits':'Aggregate arithmetic verification only; no new validation-loss parquet reconstruction.'},indent=2)+'\n')
print('Created six figures in PDF/SVG/PNG; verified all 20 selected winners and 40 selected metrics against saved candidate records.')

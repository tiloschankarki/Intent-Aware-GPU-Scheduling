"""One-time preparation. Saved ID maps supply exclusion only; never open historical test data."""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path('outputs/Experiment3').resolve()))
sys.path.insert(0,'/Users/tiloschan/Downloads/asi_robustness_20261020/dependencies')
import duckdb,pyarrow as pa,pyarrow.parquet as pq
import exp3_runner as r
O=Path('outputs/Experiment3');D=O/'inputs';D.mkdir(exist_ok=True)
R=Path('/Users/tiloschan/Documents/Codex/2026-10-26/referenced-chatgpt-conversation-this-is-an-5/outputs/ASI_recovery_20260927')
map_paths=[R/'split-map.parquet',Path('/Users/tiloschan/Downloads/asi_robustness_20261020/split_map.parquet')]
map_hashes=['222d5c8464ccb48e9a507a81fd838728cee5707e380254340a9c0917426cbaf1','e06c43ec87176849b1073c73912eceb454b4094824531ae945b16d7847510c09']
source_paths=[R/'train_20260927.parquet',R/'validation_20260927.parquet']
source_hashes=['18f6cbc9e7c12caf23e3f3ee2591aed608be773b114f4e19e8de9a2abd9a3e2a','ced84beb3cebfb1faee3321e243965b35a042288f30fe40aeafe960dec56f8dd']
for p,h in zip(map_paths+source_paths,map_hashes+source_hashes):
 if r.sha(p)!=h: raise ValueError('Prior input changed: '+str(p))
maps=[pq.read_table(p,columns=['workload_id','split']).to_pandas() for p in map_paths]
excluded,audit=r.exclusion_union(maps)
eligible=set(maps[0].workload_id)-excluded
# Row counts use membership columns only. Excluded IDs serve no other purpose.
source_counts=[];eligible_executions=0
for p in source_paths:
 d=pq.read_table(p,columns=['workload_id']).to_pandas();mask=~d.workload_id.isin(excluded)
 if not set(d.loc[mask,'workload_id']).issubset(eligible):raise ValueError('Universe mismatch')
 n=int(mask.sum());eligible_executions+=n
 source_counts.append({'path':str(p),'rows':len(d),'eligible_rows':n,'excluded_rows':len(d)-n});del d,mask
# Drop excluded identities before selecting any feature/outcome columns.
del excluded,maps
con=duckdb.connect(':memory:');con.execute("SET memory_limit='1GB'");con.execute('SET threads=2')
con.register('eligible_ids',pa.table({'workload_id':sorted(eligible)}))
features=r.ref.feature_columns(r.load_protocol(),'R+P+A','m1','workload_disjoint')
columns=['row_ordinal','workload_id','duration_hours']+features
path=D/'eligible.parquet'
if path.exists():raise FileExistsError(path)
query='SELECT '+','.join('s.'+c for c in columns)+' FROM read_parquet(?) s INNER JOIN eligible_ids e USING(workload_id) ORDER BY row_ordinal'
destination="'"+str(path).replace("'", "''")+"'"
con.execute("COPY ("+query+") TO "+destination+" (FORMAT PARQUET, COMPRESSION ZSTD)",[[str(p) for p in source_paths]])
counts=con.execute('SELECT count(*),count(DISTINCT workload_id),count(DISTINCT row_ordinal) FROM read_parquet(?)',[str(path)]).fetchone()
assert counts==(eligible_executions,len(eligible),eligible_executions),counts
con.close()
audit.update({'historical_partition_seeds':[20260927,20261020],'original_executions':4709624,
 'eligible_executions':eligible_executions,'excluded_union_executions':4709624-eligible_executions,
 'original_population_source':'saved archival metadata: 4,709,624 rows / 473,265 workloads',
 'eligible_workload_fraction':len(eligible)/473265,'eligible_execution_fraction':eligible_executions/4709624,
 'label':'new restricted-population robustness study; not direct full-population replication',
 'source_train_validation_counts':source_counts,
 'historical_test_files_opened':False,'historical_test_outcomes_inspected':False,
 'historical_ids_use':'only exclusion membership and exclusion counts; not exported',
 'eligible_selection':'inner join original seed-20260927 train/validation to eligible IDs before returning any features/outcomes',
 'maps':[{'seed':s,'path':str(p),'sha256':h,'columns':['workload_id','split']} for s,p,h in zip([20260927,20261020],map_paths,map_hashes)],
 'source_inputs':[{'path':str(p),'sha256':h} for p,h in zip(source_paths,source_hashes)],
 'feature_target_processing':'copied original features and duration_hours; no re-cleaning, target transform applied at fit time',
 'prior_inputs_unchanged':all(r.sha(p)==h for p,h in zip(map_paths+source_paths,map_hashes+source_hashes))})
(D/'population_audit.json').write_text(json.dumps(audit,indent=2))
(O/'population_audit.json').write_text(json.dumps(audit,indent=2))
print(json.dumps({k:v for k,v in audit.items() if k not in ['maps','source_inputs','source_train_validation_counts']},indent=2))

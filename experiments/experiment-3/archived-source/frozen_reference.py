"""Functions extracted verbatim from archived source; see source_provenance.json."""
import json, hashlib
import numpy as np
import pandas as pd

def validate_features(columns, protocol):
    allowed = {c for group in protocol['feature_groups'].values() for c in group}
    forbidden = set(protocol['blacklisted_predictors'])
    bad = set(columns) - allowed | (set(columns) & forbidden)
    if bad or not columns or len(columns) != len(set(columns)):
        raise ValueError(f'Invalid feature matrix columns: {sorted(bad)}')

def assign_workload(workload_id, protocol):
    if not isinstance(workload_id, str) or not workload_id:
        raise ValueError('Primary grouping requires a non-null, nonempty workload ID')
    fractions = protocol['split']['fractions']
    if len(fractions) != 3 or any(x <= 0 for x in fractions) or abs(sum(fractions)-1) > 1e-12:
        raise ValueError('Invalid split fractions')
    payload = json.dumps([protocol['split']['seed'], workload_id], ensure_ascii=False, separators=(',', ':')).encode()
    value = int.from_bytes(hashlib.sha256(payload).digest()[:8], 'big') / 2**64
    return 'train' if value < fractions[0] else 'validation' if value < sum(fractions[:2]) else 'test'

def feature_columns(p,comparison,role,evaluation):
 if role not in ['m0','m1']:raise ValueError('Invalid role')
 groups=comparison.split('+')
 if evaluation=='workload_disjoint' and 'W' in groups:raise ValueError('Workload identity is forbidden in primary predictors')
 allowed=['+'.join(x['m0']) for x in p['paired_ablations']]
 if comparison not in allowed:raise ValueError('Comparison not enabled in required experiment')
 cols=[c for g in groups for c in p['feature_groups'][g]]
 if role=='m1':cols+=p['feature_groups']['O']
 validate_features(cols,p)
 return cols

def fit_encoding(train,columns,p):
 return {c:sorted(train[c].dropna().astype(str).unique().tolist()) for c in columns if c in p['encoding']['native_categorical']}

def encode(frame,columns,encoding,p):
 validate_features(columns,p)
 x=pd.DataFrame(index=frame.index)
 for c in columns:
  if c in p['encoding']['native_categorical']:
   values=frame[c].map(lambda v:None if pd.isna(v) else str(v))
   x[c]=values.map({v:i for i,v in enumerate(encoding[c])}).fillna(-1).astype('int32')
  else:x[c]=frame[c].astype('float64')
 return x

def parameters(p,candidate,seed):
    return {**p['model']['parameters'],**{k:v for k,v in candidate.items() if k!='candidate_id'},
            'seed':seed,'bagging_seed':seed,'feature_fraction_seed':seed,'data_random_seed':seed}


"""Shared native LightGBM selection path for paired M0 and M1 models."""
from datetime import datetime, timezone
import gc
import importlib.metadata
import json
from pathlib import Path
import hashlib
import time
import duckdb
import numpy as np
import pandas as pd
from .dataset import sha256,protocol_hash
from .safety import validate_features


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


def load_split(dataset,p,population,evaluation,split,*,selection=None,binding=None):
 if split=='test':
  if selection is None or binding is None: raise ValueError('Valid frozen selection required before test access')
  from .execution import validate_selection
  validate_selection(selection,binding,p)
 if population not in ['broad','finite'] or evaluation not in ['workload_disjoint','random_execution'] or split not in ['train','validation','test']:raise ValueError('Unknown population/evaluation/split')
 col='grouped_split' if evaluation=='workload_disjoint' else 'random_split'
 pred='TRUE' if population=='broad' else "job_type_public IN ('training','offline_inference')"
 con=duckdb.connect(':memory:');con.execute("SET memory_limit='1GB'");con.execute('SET threads=2')
 try:return con.execute(f'SELECT * FROM read_parquet(?) WHERE {pred} AND {col}=? ORDER BY row_ordinal',[str(Path(dataset)/'data/*.parquet'),split]).fetchdf()
 finally:con.close()


def row_hash(frame):return hashlib.sha256(np.asarray(frame.row_ordinal,dtype='<i8').tobytes()).hexdigest()


def train_one(dataset,output,config,population,evaluation,comparison,seed,role):
 from .execution import compatibility_train
 return compatibility_train(dataset,output,config,population,evaluation,comparison,seed,role)

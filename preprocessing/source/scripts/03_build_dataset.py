#!/usr/bin/env python3
"""Build immutable prospective features/splits; defaults to bounded dry run."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from asi_pipeline.dataset import build_dataset,sha256

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--source',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
 parser.add_argument('--config',type=Path,default=Path(__file__).resolve().parents[1]/'config/protocol.yaml')
 parser.add_argument('--limit',type=int,default=10000);parser.add_argument('--full',action='store_true')
 args=parser.parse_args();raw=args.config.read_bytes();p=json.loads(raw)
 result=build_dataset(args.source,args.output,p,None if args.full else args.limit)
 if args.config.read_bytes()!=raw:raise RuntimeError('Config changed during construction')
 print(json.dumps({k:result[k] for k in ['source_rows_read','retained_rows','counts','dry_run']},indent=2))
if __name__=='__main__':main()

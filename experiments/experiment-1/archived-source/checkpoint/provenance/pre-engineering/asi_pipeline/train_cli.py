"""Identical command-line controls for each side of a lifecycle comparison."""
import argparse,json
from pathlib import Path
from .modeling import train_one

def main(role):
 parser=argparse.ArgumentParser()
 parser.add_argument('--dataset',type=Path,required=True);parser.add_argument('--output-root',type=Path,required=True)
 parser.add_argument('--config',type=Path,default=Path(__file__).resolve().parents[1]/'config/protocol.yaml')
 parser.add_argument('--population',choices=['broad','finite'],default='broad')
 parser.add_argument('--evaluation',choices=['workload_disjoint','random_execution'],default='workload_disjoint')
 parser.add_argument('--comparison',choices=['R','R+P','R+P+A'],default='R+P+A')
 args=parser.parse_args();p=json.loads(args.config.read_text())
 for seed in p['model']['seeds']:
  dest=args.output_root/args.evaluation/args.population/args.comparison/str(seed)/role
  if (dest/'manifest.json').exists():
   # Completed runs are immutable; do not silently reuse without validation.
   raise FileExistsError(f'Completed output already exists: {dest}; choose fresh output root')
  result=train_one(args.dataset,dest,args.config,args.population,args.evaluation,args.comparison,seed,role)
  print(json.dumps({'status':result['status'],'seed':seed,'role':role,'population':args.population,'evaluation':args.evaluation,'dry_run':result['dry_run']}),flush=True)

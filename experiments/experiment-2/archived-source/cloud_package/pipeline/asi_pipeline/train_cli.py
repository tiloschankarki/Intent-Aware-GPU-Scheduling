"""Identical command-line controls for each side of a lifecycle comparison."""
import argparse,json
from pathlib import Path
from .execution import select_model,predict_selected,compatibility_train

def main(role):
 parser=argparse.ArgumentParser()
 parser.add_argument('--dataset',type=Path,required=True);parser.add_argument('--output-root',type=Path,required=True)
 parser.add_argument('--config',type=Path,default=Path(__file__).resolve().parents[1]/'config/protocol.yaml')
 parser.add_argument('--population',choices=['broad','finite'],default='broad')
 parser.add_argument('--evaluation',choices=['workload_disjoint','random_execution'],default='workload_disjoint')
 parser.add_argument('--comparison',choices=['R','R+P','R+P+A'],default='R+P+A')
 parser.add_argument('--phase',choices=['select','test'],default='select')
 parser.add_argument('--authorization',type=Path)
 args=parser.parse_args();p=json.loads(args.config.read_text())
 for seed in p['model']['seeds']:
  dest=args.output_root/args.evaluation/args.population/args.comparison/str(seed)/role
  call=select_model if args.phase=='select' else predict_selected
  call(args.dataset,dest,args.config,args.population,args.evaluation,args.comparison,seed,role,args.authorization)
  print(json.dumps({'status':'complete','phase':args.phase,'seed':seed,'role':role,'population':args.population,'evaluation':args.evaluation}),flush=True)

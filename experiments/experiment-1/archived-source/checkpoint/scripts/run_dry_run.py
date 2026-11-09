#!/usr/bin/env python3
"""Bounded integration run; reports mechanics/resources, never scientific gains."""
import argparse,importlib.util,json,resource,sys,time,platform
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from asi_pipeline.dataset import build_dataset,sha256
from asi_pipeline.modeling import train_one

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--source',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
 parser.add_argument('--config',type=Path,default=Path(__file__).resolve().parents[1]/'config/protocol.yaml')
 args=parser.parse_args();raw=args.config.read_bytes();p=json.loads(raw)
 if args.output.exists():raise FileExistsError(args.output)
 args.output.mkdir(parents=True);started=time.monotonic()
 spec=importlib.util.spec_from_file_location('generalization',Path(__file__).with_name('06_generalization.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 records=[]
 try:
  dm=build_dataset(args.source,args.output/'dataset',p,p['dry_run']['max_source_rows'])
  for evaluation in p['dry_run']['evaluations']:
   for population in p['dry_run']['populations']:
    for comparison in p['dry_run']['comparisons']:
     for seed in p['model']['seeds']:
      parent=args.output/'models'/evaluation/population/comparison/str(seed)
      for role in ['m0','m1']:
       m=train_one(args.output/'dataset',parent/role,args.config,population,evaluation,comparison,seed,role)
       records.append({'evaluation':evaluation,'population':population,'comparison':comparison,'seed':seed,'role':role,'elapsed_seconds':m['elapsed_seconds'],'train_rows':m['train_rows'],'validation_rows':m['validation_rows'],'test_rows':m['test_rows']})
      module.evaluate(parent/'m0',parent/'m1',args.config,args.output/'evaluations'/evaluation/population/comparison/str(seed))
      print(json.dumps({'completed_pair':len(records)//2,'evaluation':evaluation,'population':population,'seed':seed,'scientific_interpretation':False}),flush=True)
  if args.config.read_bytes()!=raw:raise RuntimeError('Protocol changed during dry run')
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
  report={'status':'success','dry_run':True,'scientific_interpretation':False,'timestamp_utc':datetime.now(timezone.utc).isoformat(),'protocol_sha256':sha256(args.config),'dataset_manifest_sha256':sha256(args.output/'dataset/manifest.json'),'source_rows_read':dm['source_rows_read'],'retained_rows':dm['retained_rows'],'counts':dm['counts'],'model_fits':len(records)*len(p['model']['hyperparameter_grid']),'selected_models':len(records),'paired_evaluations':len(records)//2,'elapsed_seconds':time.monotonic()-started,'peak_process_rss_bytes':peak if platform.system()=='Darwin' else peak*1024,'peak_measurement':'ru_maxrss, process high-water mark including native allocations; excludes OS cache and other processes','artifact_bytes':sum(x.stat().st_size for x in args.output.rglob('*') if x.is_file()),'runs':records,'remote_dataset_bytes':0}
  (args.output/'dry_run_report.json').write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps({k:v for k,v in report.items() if k!='runs'},indent=2))
 except Exception as exc:
  (args.output/'failure.json').write_text(json.dumps({'status':'failed','error':repr(exc),'elapsed_seconds':time.monotonic()-started,'completed_models':len(records)},indent=2));raise
if __name__=='__main__':main()

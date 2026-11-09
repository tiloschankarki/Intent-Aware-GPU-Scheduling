import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from asi_pipeline.feasibility import run,worker

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['run','worker'])
    for key in ('dataset','output','config','authorization'):p.add_argument('--'+key,type=Path,required=True)
    p.add_argument('--role',choices=['m0','m1']);a=p.parse_args()
    if a.phase=='worker':result=worker(a.dataset,a.output,a.config,a.authorization,a.role)
    else:result=run(a.dataset,a.output,a.config,a.authorization)
    print(json.dumps(result,indent=2))
    if result.get('status')=='FAILED':sys.exit(2)

import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from asi_pipeline.scientific_run import run
from asi_pipeline.execution import select_model,predict_selected

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['run','select','test'])
    for key in ('dataset','output','config','authorization'):p.add_argument('--'+key,type=Path,required=True)
    p.add_argument('--population',choices=['broad','finite']);p.add_argument('--comparison',choices=['R','R+P','R+P+A'])
    p.add_argument('--seed',type=int);p.add_argument('--role',choices=['m0','m1']);a=p.parse_args()
    if a.phase=='run':run(a.dataset,a.output,a.config,a.authorization)
    else:
        call=select_model if a.phase=='select' else predict_selected
        call(a.dataset,a.output,a.config,a.population,'workload_disjoint',a.comparison,a.seed,a.role,a.authorization)
    print(json.dumps({'status':'complete','phase':a.phase}))

"""Staged acquisition/audit/build/reopen commands; no scientific training."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from asi_pipeline.primary_data import acquire,audit_source,audit_population,build_primary,finalize_primary

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['acquire','audit-source','audit-population','build','validate'])
    parser.add_argument('--source',type=Path);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--config',type=Path,default=Path('config/protocol.yaml'))
    parser.add_argument('--split-audit',type=Path);parser.add_argument('--protocol-doc',type=Path,default=Path('docs/protocol.md'))
    a=parser.parse_args()
    if a.phase=='acquire':result=acquire(a.output)
    elif a.phase=='audit-source':result=audit_source(a.source,a.config,a.output)
    elif a.phase=='audit-population':result=audit_population(a.source,a.config,a.output)
    elif a.phase=='build':result=build_primary(a.source,a.output,a.config)
    else:result=finalize_primary(a.output,a.config,a.protocol_doc,a.split_audit)
    print(json.dumps(result,indent=2))

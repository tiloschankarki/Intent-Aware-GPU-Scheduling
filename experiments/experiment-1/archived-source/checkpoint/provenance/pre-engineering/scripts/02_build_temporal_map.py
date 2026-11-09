#!/usr/bin/env python3
"""Remote mode is fail-closed; --fixture-zip exercises only a local fixture."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from asi_pipeline.remote_temporal import run

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',default='config/protocol.yaml')
    parser.add_argument('--source',default='part-000.parquet')
    parser.add_argument('--output',default='artifacts/temporal/window_d108_d110')
    parser.add_argument('--fixture-zip')
    parser.add_argument('--verified-map')
    args=parser.parse_args()
    cfg=json.loads(Path(args.config).read_text())
    verified=args.verified_map
    if not args.fixture_zip and verified is None:
        verified=cfg['temporal']['validated_map']
    print(json.dumps(run(cfg,args.source,args.output,fixture_zip=args.fixture_zip,verified_map=verified),indent=2))

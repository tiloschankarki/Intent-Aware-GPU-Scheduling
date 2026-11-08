"""Atomic, hash-verified execution units; scientific configuration is read-only."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import uuid
from datetime import datetime, timezone
from .dataset import sha256

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()

def versions():
    return {'python':platform.python_version(), **{p:importlib.metadata.version(p) for p in
            ['lightgbm','numpy','pandas','pyarrow','duckdb','scipy','PyYAML']}}

def code_state():
    root=Path(__file__).resolve().parents[1]
    files={str(p.relative_to(root)).replace('\\','/'):sha256(p)
           for folder in ('asi_pipeline','scripts') for p in sorted((root/folder).glob('*.py'))}
    return {'sha256':digest(files),'files':files}

def write_synced(path, data):
    with Path(path).open('xb') as stream:
        stream.write(data);stream.flush();os.fsync(stream.fileno())

def publish_unit(path, binding, record, artifacts):
    """Publish a complete directory once. Abandoned .partial siblings are never reused."""
    path=Path(path)
    if path.exists(): raise FileExistsError(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    stage=path.with_name(path.name+'.partial-'+uuid.uuid4().hex)
    stage.mkdir()
    hashes={}
    for name,content in artifacts.items():
        if Path(name).name!=name: raise ValueError('Artifact name must be a basename')
        if isinstance(content,Path):
            with content.open('rb') as src,(stage/name).open('xb') as dst:
                shutil.copyfileobj(src,dst,8*1024**2);dst.flush();os.fsync(dst.fileno())
        else: write_synced(stage/name,content)
        hashes[name]=sha256(stage/name)
    manifest={'status':'complete','timestamp_utc':datetime.now(timezone.utc).isoformat(),
              'binding':binding,'record':record,'artifacts':hashes}
    manifest['seal']=digest(manifest)
    write_synced(stage/'manifest.json',json.dumps(manifest,indent=2,allow_nan=False).encode())
    # Windows rename fails if destination exists. This pipeline has one writer per unit.
    os.rename(stage,path)
    return manifest

def read_unit(path,binding=None):
    path=Path(path)
    if not (path/'manifest.json').is_file(): raise ValueError('Partial or missing checkpoint: '+str(path))
    result=json.loads((path/'manifest.json').read_text(encoding='utf-8'))
    raw=dict(result);seal=raw.pop('seal',None)
    if seal!=digest(raw) or result.get('status')!='complete': raise ValueError('Invalid checkpoint seal')
    if binding is not None and result['binding']!=binding: raise ValueError('Incompatible checkpoint binding')
    for name,expected in result['artifacts'].items():
        if Path(name).name!=name or not (path/name).is_file() or sha256(path/name)!=expected:
            raise ValueError('Checkpoint artifact mismatch: '+name)
    return result

def freeze_json(path,value):
    """Exclusive JSON publication with flush and atomic hard link."""
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    stage=path.with_name(path.name+'.partial-'+uuid.uuid4().hex)
    write_synced(stage,json.dumps(value,indent=2,allow_nan=False).encode())
    os.link(stage,path);stage.unlink()

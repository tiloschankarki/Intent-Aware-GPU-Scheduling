"""Verify archived payload hashes. Standard library only; no scientific execution."""
import hashlib
from pathlib import Path
import sys

def verify(root):
    root=Path(root).resolve(); count=0
    for line in (root/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'):continue
        expected,relative=line.split('  ',1)
        path=(root/relative).resolve()
        if not path.is_relative_to(root):raise ValueError('Unsafe manifest path: '+relative)
        h=hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda:stream.read(1024**2),b''):h.update(chunk)
        if h.hexdigest()!=expected:raise ValueError('SHA-256 mismatch: '+relative)
        count+=1
    if count==0:raise ValueError('Empty checksum manifest')
    print(f'Verified {count} archived payload files; no training or artifact writes performed.')
    return count

if __name__=='__main__':verify(sys.argv[1] if len(sys.argv)>1 else '.')

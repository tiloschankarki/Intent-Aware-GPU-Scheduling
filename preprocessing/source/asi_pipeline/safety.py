"""Fail-closed local safeguards; this module never opens a network connection."""
import hashlib
import json
import os
import re
from pathlib import Path


def validate_features(columns, protocol):
    allowed = {c for group in protocol['feature_groups'].values() for c in group}
    forbidden = set(protocol['blacklisted_predictors'])
    bad = set(columns) - allowed | (set(columns) & forbidden)
    if bad or not columns or len(columns) != len(set(columns)):
        raise ValueError(f'Invalid feature matrix columns: {sorted(bad)}')


def assign_workload(workload_id, protocol):
    if not isinstance(workload_id, str) or not workload_id:
        raise ValueError('Primary grouping requires a non-null, nonempty workload ID')
    fractions = protocol['split']['fractions']
    if len(fractions) != 3 or any(x <= 0 for x in fractions) or abs(sum(fractions)-1) > 1e-12:
        raise ValueError('Invalid split fractions')
    payload = json.dumps([protocol['split']['seed'], workload_id], ensure_ascii=False, separators=(',', ':')).encode()
    value = int.from_bytes(hashlib.sha256(payload).digest()[:8], 'big') / 2**64
    return 'train' if value < fractions[0] else 'validation' if value < sum(fractions[:2]) else 'test'


def assert_disjoint(split_ids):
    seen = set()
    for name, ids in split_ids.items():
        current = set(ids)
        if None in current or '' in current or current & seen:
            raise ValueError(f'Null or contaminated workload split: {name}')
        seen.update(current)


def parse_member(path, protocol):
    match = re.fullmatch(r'asi_opensource_pod_hourly/day=(\d+)/hour=(\d{2})/part-000\.parquet', path)
    if not match:
        raise ValueError('Unexpected ZIP member path')
    day, hour = map(int, match.groups())
    if day not in protocol['temporal']['days'] or not 0 <= hour <= 23:
        raise ValueError('Member outside approved temporal bounds')
    return day, hour


def read_range(response, start, end, object_size, max_bytes):
    """Validate response before any body read; reject short/overlong bodies.

    Caller owns transport, timeout, response closing and transfer accounting.
    This helper does not implement the future remote downloader.
    """
    length = end - start + 1
    if not (0 <= start <= end < object_size) or not 0 < length <= max_bytes:
        raise ValueError('Invalid or oversized range')
    if response.status != 206:
        raise ValueError('Range ignored: refusing response body')
    if response.headers.get('Content-Range') != f'bytes {start}-{end}/{object_size}':
        raise ValueError('Unexpected Content-Range')
    if response.headers.get('Content-Encoding', 'identity') != 'identity':
        raise ValueError('Encoded response forbidden')
    stated = response.headers.get('Content-Length')
    if stated is not None and int(stated) != length:
        raise ValueError('Unexpected Content-Length')
    chunks = []
    received = 0
    while received < length + 1:
        chunk = response.read(length + 1 - received)
        if not chunk:
            break
        chunks.append(chunk)
        received += len(chunk)
    if received != length:
        raise ValueError('Truncated or oversized range body')
    return b''.join(chunks)


def publish_new(staged, destination):
    """Atomically create a new same-filesystem artifact; never replace one."""
    staged, destination = Path(staged), Path(destination)
    with staged.open('rb') as stream:
        os.fsync(stream.fileno())
    os.link(staged, destination)  # atomic, fails if destination already exists
    fd = os.open(destination.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)

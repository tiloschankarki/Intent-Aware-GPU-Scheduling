"""Bounded selective ZIP reads and transactionally checkpointed temporal feasibility.

DuckDB is the authoritative map/diagnostics checkpoint. The small SQLite ledger
reserves transfer *before* requests, conservatively charging failed requests too.
Historical transfer is unknown and is never included as a fabricated zero.
"""
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import sqlite3
import time
import urllib.request
import zipfile
import duckdb
import pyarrow.parquet as pq
from .safety import parse_member, read_range


class RangeFile(io.RawIOBase):
    def __init__(self, size, chunk, transport, reserve, received=None):
        self.size, self.chunk = size, min(chunk, 8*1024**2)
        self.transport, self.reserve, self.position = transport, reserve, 0
        self.received=received or (lambda n:None)
        if self.chunk < 1 or size < 1:
            raise ValueError('Invalid range limits')
    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.position
    def seek(self, offset, whence=0):
        position = offset + (0 if whence == 0 else self.position if whence == 1 else self.size)
        if not 0 <= position <= self.size: raise ValueError('Seek outside object')
        self.position = position
        return position
    def read(self, n=-1):
        n = self.size-self.position if n < 0 else min(n, self.size-self.position)
        # zipfile may ask for central directory in one read. Bound its allocation.
        if n > 64*1024**2: raise ValueError('ZIP metadata/read exceeds 64 MiB bound')
        parts=[]
        while n:
            length=min(n,self.chunk); start=self.position; end=start+length-1
            self.reserve(length+1)  # includes safety helper's one-byte overrun probe
            response=self.transport(start,end)
            try:
                class Counted:
                    status=response.status
                    headers=response.headers
                    def read(inner,n):
                        chunk=response.read(n)
                        self.received(len(chunk))
                        return chunk
                data=read_range(Counted(),start,end,self.size,self.chunk)
            finally: response.close()
            parts.append(data);self.position+=length;n-=length
        return b''.join(parts)


def identity(path):
    path=Path(path).resolve(); stat=path.stat(); digest=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(8*1024**2),b''):digest.update(chunk)
    return {'path':str(path),'bytes':stat.st_size,'mtime_ns':stat.st_mtime_ns,'sha256':digest.hexdigest()}


def summarize_hours(hours):
    """Descriptive adjacent-hour changes; no threshold or scientific decision."""
    return [{'previous_day':a['day'],'previous_hour':a['hour'],
             'day':b['day'],'hour':b['hour'],
             'previous_matched':a.get('matched_eligible_pods'),
             'current_matched':b.get('matched_eligible_pods'),
             'delta_matched':b['matched_eligible_pods']-a['matched_eligible_pods']}
            for a,b in zip(hours,hours[1:])
            if 'matched_eligible_pods' in a and 'matched_eligible_pods' in b]


def run(config, source, output, *, fixture_zip=None, verified_map=None, transport=None):
    temporal=config['temporal']; fixture=fixture_zip is not None
    if not fixture and not (config.get('execution_permissions',{}).get('remote_transfer') is True
                            and temporal.get('remote_execution_enabled') is True):
        raise PermissionError('Remote transfer requires both frozen execution gates enabled')
    if not fixture and temporal.get('days') != [108,109,110]:
        raise ValueError('Only D108-D110 are approved')
    if fixture and pq.ParquetFile(source).metadata.num_rows>config.get('dry_run',{}).get('max_source_rows',10000):
        raise ValueError('Local temporal fixtures must use a small synthetic source')
    start=time.monotonic(); output=Path(output);output.mkdir(parents=True,exist_ok=True)
    fingerprint=hashlib.sha256(json.dumps(config,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    source=Path(source).resolve(); stat=source.stat()
    ledger=sqlite3.connect(output/'transfer.sqlite');ledger.execute('PRAGMA synchronous=FULL')
    ledger.execute('CREATE TABLE IF NOT EXISTS budget (id INTEGER PRIMARY KEY, binding TEXT, reserved INTEGER)')
    ledger.execute('CREATE TABLE IF NOT EXISTS received (id INTEGER PRIMARY KEY, bytes INTEGER)')
    ledger.execute('INSERT OR IGNORE INTO received VALUES (1,0)');ledger.commit()
    binding=json.dumps({'config':fingerprint,'object':str(Path(fixture_zip).resolve()) if fixture else temporal['remote_url'],
                        'size':Path(fixture_zip).stat().st_size if fixture else temporal['expected_object_bytes']},sort_keys=True)
    row=ledger.execute('SELECT binding,reserved FROM budget WHERE id=1').fetchone()
    if row and row[0]!=binding:ledger.close();raise ValueError('Resume config/object binding differs')
    if not row:ledger.execute('INSERT INTO budget VALUES (1,?,0)',[binding]);ledger.commit()
    def reserve(amount):
        with ledger:
            spent=ledger.execute('SELECT reserved FROM budget WHERE id=1').fetchone()[0]
            if spent+amount>min(temporal.get('max_transfer_bytes',7*1024**3),7*1024**3):raise ValueError('Total transfer budget exhausted')
            ledger.execute('UPDATE budget SET reserved=reserved+? WHERE id=1',[amount])
    def received(amount):
        with ledger:ledger.execute('UPDATE received SET bytes=bytes+? WHERE id=1',[amount])
    con=duckdb.connect(str(output/'temporal.duckdb'))
    try:
        local=config.get('local_validation',{})
        con.execute('SET memory_limit=?',[local.get('memory_limit','1GB')]);con.execute('SET threads=?',[local.get('threads',2)])
        con.execute('CREATE TABLE IF NOT EXISTS metadata (key VARCHAR PRIMARY KEY, value VARCHAR)')
        old=con.execute("SELECT value FROM metadata WHERE key='source'").fetchone()
        if old:
            saved=json.loads(old[0])
            if saved['path']!=str(source) or saved['bytes']!=stat.st_size or saved['mtime_ns']!=stat.st_mtime_ns:
                raise ValueError('Source identity changed since eligibility build')
        else:
            saved=identity(source)
            con.execute('BEGIN')
            con.execute('''CREATE TABLE eligibility AS SELECT pod_id,min(job_type_public) job_type_public
                FROM read_parquet(?) GROUP BY pod_id HAVING count(*)=1 AND pod_id IS NOT NULL''',[str(source)])
            invalid=con.execute('SELECT count(*) FROM eligibility WHERE job_type_public IS NULL OR job_type_public NOT IN (SELECT unnest(?))',[temporal['stratification_categories']]).fetchone()[0]
            if invalid:raise ValueError('Unrecognized lifecycle in unique source population')
            con.execute('INSERT INTO metadata VALUES (?,?)',['source',json.dumps(saved)])
            con.execute('COMMIT')
        con.execute('CREATE TABLE IF NOT EXISTS temporal_map (pod_id VARCHAR PRIMARY KEY, first_seen_day INTEGER, first_seen_hour INTEGER, job_type_public VARCHAR)')
        con.execute('CREATE TABLE IF NOT EXISTS hours (member VARCHAR PRIMARY KEY, day INTEGER, hour INTEGER, diagnostics VARCHAR)')
        con.execute('CREATE TABLE IF NOT EXISTS failures (recorded_at TIMESTAMP DEFAULT current_timestamp, error VARCHAR)')
        # Import an already verified, preserved artifact instead of fetching D109H00.
        legacy=Path(verified_map) if verified_map else None
        if legacy and not con.execute('SELECT 1 FROM hours WHERE day=109 AND hour=0').fetchone():
            con.execute('CREATE OR REPLACE TEMP TABLE legacy AS SELECT * FROM read_parquet(?)',[str(legacy)])
            bad=con.execute('''SELECT count(*) FROM legacy l LEFT JOIN eligibility e USING(pod_id)
                WHERE e.pod_id IS NULL OR l.job_type_public IS DISTINCT FROM e.job_type_public
                OR l.first_seen_day IS DISTINCT FROM 109 OR l.first_seen_hour IS DISTINCT FROM 0''').fetchone()[0]
            if bad or con.execute('SELECT count(*)-count(DISTINCT pod_id) FROM legacy').fetchone()[0]:raise ValueError('Invalid verified legacy artifact')
            con.execute('BEGIN')
            con.execute('INSERT INTO temporal_map SELECT * FROM legacy')
            provenance={'day':109,'hour':0,'kind':'imported_verified_D109H00','artifact':identity(legacy),'hour_unique_pods':1489134,
                        'historic_transfer_bytes':None,'caveat':'Historical extraction was not a checkpointed remote hour; hourly count is handoff-reported.'}
            con.execute('INSERT INTO hours VALUES (?,109,0,?)',['asi_opensource_pod_hourly/day=109/hour=00/part-000.parquet',json.dumps(provenance)])
            con.execute('COMMIT');con.execute('CHECKPOINT')
        if fixture:
            archive_path=Path(fixture_zip)
            class LocalResponse:
                status=206
                def __init__(self,a,b):
                    self.file=archive_path.open('rb');self.file.seek(a);self.remaining=b-a+1
                    self.headers={'Content-Range':f'bytes {a}-{b}/{archive_path.stat().st_size}'}
                def read(self,n):
                    data=self.file.read(min(n,self.remaining));self.remaining-=len(data);return data
                def close(self):self.file.close()
            opener=lambda a,b:LocalResponse(a,b);size=archive_path.stat().st_size
        else:
            size=temporal['expected_object_bytes']
            opener=transport or (lambda a,b:urllib.request.urlopen(urllib.request.Request(temporal['remote_url'],headers={'Range':f'bytes={a}-{b}','Accept-Encoding':'identity'}),timeout=60))
        remote=RangeFile(size,temporal.get('max_range_bytes',8*1024**2),opener,reserve,received)
        with zipfile.ZipFile(remote) as archive:
            members=[]
            for item in archive.infolist():
                try:day,hour=parse_member(item.filename,config)
                except ValueError:continue
                if day not in [108,109,110]:raise ValueError('Outside approved days')
                members.append((day,hour,item))
            if len({i.filename for _,_,i in members})!=len(members):raise ValueError('Duplicate ZIP member names')
            if not fixture and len(members)!=72:raise ValueError('Expected exactly 72 bounded hourly members')
            for day,hour,item in sorted(members,key=lambda entry:entry[:2]):
                if con.execute('SELECT 1 FROM hours WHERE member=?',[item.filename]).fetchone():continue
                if item.compress_type!=zipfile.ZIP_STORED or item.flag_bits & 1:raise ValueError('Only unencrypted ZIP_STORED supported')
                if item.file_size>min(temporal.get('max_transfer_bytes',7*1024**3),7*1024**3):raise ValueError('Oversized member')
                raw=output/f'd{day}h{hour:02}.raw.parquet';before=ledger.execute('SELECT reserved FROM budget').fetchone()[0];received_before=ledger.execute('SELECT bytes FROM received WHERE id=1').fetchone()[0]
                with raw.open('wb') as dest,archive.open(item) as member:
                    for data in iter(lambda:member.read(remote.chunk),b''):dest.write(data)
                    dest.flush();os.fsync(dest.fileno()) # ZipExtFile validates CRC before publication
                con.execute('CREATE OR REPLACE TEMP TABLE hourly AS SELECT DISTINCT pod_id FROM read_parquet(?) WHERE pod_id IS NOT NULL',[str(raw)])
                con.execute('CREATE OR REPLACE TEMP TABLE matched AS SELECT e.* FROM eligibility e JOIN hourly h USING(pod_id)')
                unique=con.execute('SELECT count(*) FROM hourly').fetchone()[0]
                matched=con.execute('SELECT count(*) FROM matched').fetchone()[0]
                new=con.execute('SELECT count(*) FROM matched ANTI JOIN temporal_map USING(pod_id)').fetchone()[0]
                con.execute('BEGIN')
                con.execute('''INSERT INTO temporal_map SELECT pod_id,?,?,job_type_public FROM matched
                    ON CONFLICT(pod_id) DO UPDATE SET first_seen_day=excluded.first_seen_day,first_seen_hour=excluded.first_seen_hour
                    WHERE excluded.first_seen_day*24+excluded.first_seen_hour < temporal_map.first_seen_day*24+temporal_map.first_seen_hour''',[day,hour])
                diagnostics={'day':day,'hour':hour,'hour_unique_pods':unique,'matched_eligible_pods':matched,'new_eligible_pods':new,
                    'cumulative_eligible_pods':con.execute('SELECT count(*) FROM temporal_map').fetchone()[0],
                    'reserved_bytes':ledger.execute('SELECT reserved FROM budget').fetchone()[0]-before,
                    'received_body_bytes':ledger.execute('SELECT bytes FROM received WHERE id=1').fetchone()[0]-received_before,
                    'lifecycle_matched':dict(con.execute('SELECT job_type_public,count(*) FROM matched GROUP BY 1').fetchall()),'crc32':item.CRC,'status':'complete'}
                con.execute('INSERT INTO hours VALUES (?,?,?,?)',[item.filename,day,hour,json.dumps(diagnostics)])
                con.execute('COMMIT');con.execute('CHECKPOINT');raw.unlink()
        report={'config_sha256':fingerprint,'source':saved,'fixture_mode':fixture,
            'mapped_pods':con.execute('SELECT count(*) FROM temporal_map').fetchone()[0],
            'completed_hours':con.execute('SELECT count(*) FROM hours').fetchone()[0],
            'reserved_transfer_bytes':ledger.execute('SELECT reserved FROM budget').fetchone()[0],
            'received_body_bytes':ledger.execute('SELECT bytes FROM received WHERE id=1').fetchone()[0],
            'historic_transfer_bytes':None,'elapsed_seconds':time.monotonic()-start,
            'versions':{'python':platform.python_version(),'duckdb':duckdb.__version__},
            'per_day_first_observations':dict(con.execute('SELECT first_seen_day,count(*) FROM temporal_map GROUP BY 1').fetchall()),
            'lifecycle_coverage':con.execute('SELECT e.job_type_public,count(*),count(m.pod_id) FROM eligibility e LEFT JOIN temporal_map m USING(pod_id) GROUP BY 1').fetchall(),
            'hours':[json.loads(row[0]) for row in con.execute('SELECT diagnostics FROM hours ORDER BY day,hour').fetchall()],
            'projected_window_transfer_gib':temporal.get('estimated_transfer_gib'),
            'interpretation':'Earliest observation within scanned window, not submission/start time; chronological evaluation remains disabled.'}
        report['adjacent_hour_changes']=summarize_hours(report['hours'])
        report['failures']=[{'at':str(at),'error':error} for at,error in con.execute('SELECT * FROM failures').fetchall()]
        report['transfer_accounting']='received_body_bytes records observed response body bytes (includes metadata and failed reads); reserved_transfer_bytes is a conservative upper bound incl. one-byte probes; historical transfer unknown; HTTP/TLS overhead excluded.'
        staged=output/'manifest.json.tmp'
        with staged.open('w') as f:json.dump(report,f,indent=2);f.flush();os.fsync(f.fileno())
        os.replace(staged,output/'manifest.json')
        return report
    except Exception as exc:
        try:con.execute('ROLLBACK')
        except duckdb.Error:pass
        try:con.execute('INSERT INTO failures(error) VALUES (?)',[repr(exc)]);con.execute('CHECKPOINT')
        except duckdb.Error:pass
        raise
    finally:con.close();ledger.close()

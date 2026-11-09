"""Windows worker supervision. Resource policy never changes scientific inputs."""
import ctypes
from ctypes import wintypes as w
import json
import os
from pathlib import Path
import subprocess
import time
from .checkpoints import freeze_json

GIB=2**30

class SafetyPolicy:
    def __init__(self): self.pressure_since=None
    def check(self,s,elapsed):
        if s['available_physical']<GIB: return 'available physical memory below 1 GiB'
        if s['commit_available']<GIB: return 'commit headroom below 1 GiB'
        paging=s.get('page_reads_per_sec')
        pressure=(s['available_physical']<2*GIB or s['commit_available']<2*GIB or
                  (paging is not None and (paging>1000 or (paging>200 and s['available_physical']<3*GIB))))
        if pressure:
            if self.pressure_since is None:self.pressure_since=elapsed
            if elapsed-self.pressure_since>=15:return 'sustained memory/commit/paging pressure for 15 seconds'
        else:self.pressure_since=None
        return None

class Memory(ctypes.Structure):
    _fields_=[('length',w.DWORD),('load',w.DWORD)]+[(n,ctypes.c_ulonglong) for n in
        ['total','available','commit_limit','commit_available','virtual_total','virtual_available','extended']]

class ProcessMemory(ctypes.Structure):
    _fields_=[('cb',w.DWORD),('page_faults',w.DWORD)]+[(n,ctypes.c_size_t) for n in
        ['peak_rss','rss','peak_paged_pool','paged_pool','peak_nonpaged_pool','nonpaged_pool','commit','peak_commit','private']]

class PagingCounter:
    """PDH English counter counts disk reads needed to resolve hard page faults."""
    def __init__(self):
        self.pdh=ctypes.WinDLL('pdh');self.query=w.HANDLE();self.counter=w.HANDLE()
        self.pdh.PdhOpenQueryW.argtypes=[w.LPCWSTR,ctypes.c_size_t,ctypes.POINTER(w.HANDLE)]
        self.pdh.PdhAddEnglishCounterW.argtypes=[w.HANDLE,w.LPCWSTR,ctypes.c_size_t,ctypes.POINTER(w.HANDLE)]
        self.pdh.PdhCollectQueryData.argtypes=[w.HANDLE]
        if self.pdh.PdhOpenQueryW(None,0,ctypes.byref(self.query))!=0:raise RuntimeError('PDH query unavailable')
        if self.pdh.PdhAddEnglishCounterW(self.query,r'\Memory\Page Reads/sec',0,ctypes.byref(self.counter))!=0:raise RuntimeError('PDH hard-paging counter unavailable')
        if self.pdh.PdhCollectQueryData(self.query)!=0:raise RuntimeError('PDH initial sampling failed')
        self.started=time.monotonic()
    def read(self):
        if time.monotonic()-self.started<.1:return None
        class ValueUnion(ctypes.Union):_fields_=[('number',ctypes.c_double),('large',ctypes.c_longlong)]
        class Value(ctypes.Structure):_fields_=[('status',w.DWORD),('value',ValueUnion)]
        self.pdh.PdhGetFormattedCounterValue.argtypes=[w.HANDLE,w.DWORD,ctypes.c_void_p,ctypes.POINTER(Value)]
        if self.pdh.PdhCollectQueryData(self.query)!=0:raise RuntimeError('PDH collection failed')
        v=Value();status=self.pdh.PdhGetFormattedCounterValue(self.counter,0x200,None,ctypes.byref(v))
        if status!=0 or v.status not in (0,1):raise RuntimeError('PDH formatted paging counter failed')
        return v.value.number

_paging=None

def snapshot(pid=None):
    global _paging
    if os.name!='nt': raise RuntimeError('Windows monitor requires Windows')
    k=ctypes.WinDLL('kernel32',use_last_error=True);ps=ctypes.WinDLL('psapi',use_last_error=True)
    mem=Memory();mem.length=ctypes.sizeof(mem)
    if not k.GlobalMemoryStatusEx(ctypes.byref(mem)): raise ctypes.WinError(ctypes.get_last_error())
    out={'available_physical':mem.available,'total_physical':mem.total,'commit_limit':mem.commit_limit,
         'commit_available':mem.commit_available,'system_commit':mem.commit_limit-mem.commit_available,
         'worker_rss':0,'worker_peak_rss':0,'worker_commit':0,'worker_page_fault_count':None,
         'page_reads_per_sec':None,'pagefile_use_bytes':None,
         'paging_note':'PDH Memory/Page Reads/sec measures hard-fault disk reads; process faults include soft faults; direct pagefile usage unavailable.'}
    if _paging is None:_paging=PagingCounter()
    out['page_reads_per_sec']=_paging.read()
    if pid is not None:
        k.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];k.OpenProcess.restype=w.HANDLE
        k.CloseHandle.argtypes=[w.HANDLE]
        ps.GetProcessMemoryInfo.argtypes=[w.HANDLE,ctypes.c_void_p,w.DWORD]
        handle=k.OpenProcess(0x410,False,pid)
        if not handle: raise ctypes.WinError(ctypes.get_last_error())
        try:
            pm=ProcessMemory();pm.cb=ctypes.sizeof(pm)
            if not ps.GetProcessMemoryInfo(handle,ctypes.byref(pm),pm.cb): raise ctypes.WinError(ctypes.get_last_error())
            out.update(worker_rss=pm.rss,worker_peak_rss=pm.peak_rss,worker_commit=pm.commit,
                       worker_page_fault_count=pm.page_faults)
        finally:k.CloseHandle(handle)
    return out

def job_guard(process):
    """Kill worker if supervising process exits unexpectedly; no resource-limit alteration."""
    if os.name!='nt':return None
    class Basic(ctypes.Structure):
        _fields_=[('process_time',ctypes.c_longlong),('job_time',ctypes.c_longlong),('flags',w.DWORD),
                  ('min_ws',ctypes.c_size_t),('max_ws',ctypes.c_size_t),('active',w.DWORD),
                  ('affinity',ctypes.c_size_t),('priority',w.DWORD),('scheduling',w.DWORD)]
    class IO(ctypes.Structure): _fields_=[(n,ctypes.c_ulonglong) for n in ['read','write','other','read_bytes','write_bytes','other_bytes']]
    class Extended(ctypes.Structure):
        _fields_=[('basic',Basic),('io',IO)]+[(n,ctypes.c_size_t) for n in ['process_memory','job_memory','peak_process','peak_job']]
    k=ctypes.WinDLL('kernel32',use_last_error=True)
    k.CreateJobObjectW.argtypes=[ctypes.c_void_p,w.LPCWSTR];k.CreateJobObjectW.restype=w.HANDLE
    k.SetInformationJobObject.argtypes=[w.HANDLE,ctypes.c_int,ctypes.c_void_p,w.DWORD]
    k.AssignProcessToJobObject.argtypes=[w.HANDLE,w.HANDLE];k.CloseHandle.argtypes=[w.HANDLE]
    job=k.CreateJobObjectW(None,None);info=Extended();info.basic.flags=0x2000
    if not job:raise ctypes.WinError(ctypes.get_last_error())
    if not k.SetInformationJobObject(job,9,ctypes.byref(info),ctypes.sizeof(info)) or not k.AssignProcessToJobObject(job,w.HANDLE(int(process._handle))):
        k.CloseHandle(job);raise ctypes.WinError(ctypes.get_last_error())
    return lambda:k.CloseHandle(job)

def directory_bytes(path):
    return sum(p.stat().st_size for p in Path(path).rglob('*') if p.is_file()) if path and Path(path).exists() else 0

def supervise(command,output,*,snapshot_fn=snapshot,poll_seconds=1,spill=None,cwd=None):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    stop=output/'STOP';policy=SafetyPolicy();start=time.monotonic();process=None;close_job=None
    report={'status':'FAILED','command':list(command),'exit_code':None,'reason':None,'safety_terminated':False,
            'peak_worker_rss':0,'min_available_physical':None,'min_commit_available':None,
            'spill_peak_bytes':0,'limits':{'hard_available_GiB':1,'hard_commit_GiB':1,'soft_GiB':2,'soft_seconds':15,
                                          'preflight_physical_GiB':3,'preflight_commit_GiB':3},
            'paging_observable':'worker page-fault counts (soft/hard combined); commit headroom; direct pagefile use unavailable'}
    def record(s,log):
        s={**s,'elapsed_seconds':time.monotonic()-start,'spill_bytes':directory_bytes(spill)}
        report['peak_worker_rss']=max(report['peak_worker_rss'],s.get('worker_peak_rss',0),s['worker_rss'])
        report['spill_peak_bytes']=max(report['spill_peak_bytes'],s['spill_bytes'])
        for key,field in [('min_available_physical','available_physical'),('min_commit_available','commit_available')]:
            report[key]=s[field] if report[key] is None else min(report[key],s[field])
        log.write(json.dumps(s)+'\n');log.flush()
        return s
    try:
        with (output/'resources.jsonl').open('x',encoding='utf-8') as log,(output/'stdout.txt').open('xb') as stdout,(output/'stderr.txt').open('xb') as stderr:
            initial=record(snapshot_fn(),log)
            if initial['available_physical']<3*GIB or initial['commit_available']<3*GIB:
                report['reason']='Preflight requires at least 3 GiB physical and commit headroom';return report
            env=os.environ.copy();env['ASI_STOP_FILE']=str(stop.resolve());env['PYTHONUTF8']='1'
            process=subprocess.Popen(list(command),stdout=stdout,stderr=stderr,cwd=cwd,env=env,
                                     creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            if process.poll() is None:close_job=job_guard(process)
            while process.poll() is None:
                try:s=record(snapshot_fn(process.pid),log)
                except OSError:
                    if process.poll() is not None:break
                    raise
                reason=policy.check(s,time.monotonic()-start)
                if reason:
                    report.update(reason=reason,safety_terminated=True)
                    stop.write_text(reason,encoding='utf-8')
                    try:process.wait(timeout=5)
                    except subprocess.TimeoutExpired:process.terminate();process.wait(timeout=10)
                    break
                time.sleep(poll_seconds)
            report['exit_code']=process.wait()
            if report['reason'] is None:
                report['status']='PASSED' if process.returncode==0 else 'FAILED'
                report['reason']='completed' if process.returncode==0 else 'worker exited unsuccessfully'
    except BaseException as error:
        report['reason']='Monitor failure: '+repr(error)
        if process and process.poll() is None:
            stop.write_text(report['reason'],encoding='utf-8');process.terminate();process.wait(timeout=10)
        if process:report['exit_code']=process.returncode
        if isinstance(error,KeyboardInterrupt):raise
    finally:
        if close_job:close_job()
        report['elapsed_seconds']=time.monotonic()-start
        freeze_json(output/'manifest.json',report)
    return report

def check_stop(env=None):
    stop=(env or os.environ).get('ASI_STOP_FILE')
    if stop and Path(stop).exists():raise RuntimeError('Worker stopped by safety supervisor')

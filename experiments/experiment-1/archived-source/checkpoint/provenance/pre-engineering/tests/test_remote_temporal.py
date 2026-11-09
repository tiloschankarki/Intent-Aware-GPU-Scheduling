import copy
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq

class RemoteTests(unittest.TestCase):
    def test_disabled_before_transport(self):
        from asi_pipeline.remote_temporal import run
        with self.assertRaises(PermissionError):
            run({'execution_permissions':{'remote_transfer':False},'temporal':{}},'absent','absent')

    def test_fixture_resume_and_unique_eligibility(self):
        from asi_pipeline.remote_temporal import run
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)
            pq.write_table(pa.table({'pod_id':['a','b','b','c'],'job_type_public':['training']*4}),p/'source.parquet')
            buf=io.BytesIO(); pq.write_table(pa.table({'pod_id':['a','b','a','missing']}),buf)
            with zipfile.ZipFile(p/'fixture.zip','w') as z:
                z.writestr('asi_opensource_pod_hourly/day=108/hour=00/part-000.parquet',buf.getvalue())
            config={'execution_permissions':{'remote_transfer':False},'temporal':{'days':[108,109,110], 'stratification_categories':['training'], 'max_range_bytes':8388608,'max_transfer_bytes':1000000},'local_validation':{'memory_limit':'128MB','threads':1}}
            result=run(config,p/'source.parquet',p/'out',fixture_zip=p/'fixture.zip')
            self.assertEqual(result['mapped_pods'],1)
            before=result['reserved_transfer_bytes']
            result=run(config,p/'source.parquet',p/'out',fixture_zip=p/'fixture.zip')
            self.assertEqual(result['completed_hours'],1)
            self.assertGreaterEqual(result['reserved_transfer_bytes'],before)
            changed=copy.deepcopy(config);changed['temporal']['days']=[108]
            with self.assertRaises(ValueError):run(changed,p/'source.parquet',p/'out',fixture_zip=p/'fixture.zip')

    def test_ignored_range_no_body_read(self):
        from asi_pipeline.remote_temporal import RangeFile
        class Response:
            status=200;headers={}
            def read(self,n):raise AssertionError('body consumed')
            def close(self):pass
        obj=RangeFile(100,8,lambda a,b:Response(),lambda n:None)
        with self.assertRaises(ValueError):obj.read(4)

    def test_crc_failure_keeps_raw_and_no_completion(self):
        from asi_pipeline.remote_temporal import run
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)
            pq.write_table(pa.table({'pod_id':['a'],'job_type_public':['training']}),p/'source.parquet')
            with zipfile.ZipFile(p/'f.zip','w') as z:z.writestr('asi_opensource_pod_hourly/day=108/hour=00/part-000.parquet',b'not parquet')
            raw=bytearray((p/'f.zip').read_bytes());raw[raw.index(b'not parquet')]=120;(p/'f.zip').write_bytes(raw)
            cfg={'execution_permissions':{},'temporal':{'days':[108,109,110],'stratification_categories':['training'],'max_transfer_bytes':1000000}}
            with self.assertRaises(zipfile.BadZipFile):run(cfg,p/'source.parquet',p/'out',fixture_zip=p/'f.zip')
            self.assertTrue(list((p/'out').glob('*.raw.parquet')))

    def test_import_verified_hour_skips_corrupt_remote_member(self):
        from asi_pipeline.remote_temporal import run
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)
            pq.write_table(pa.table({'pod_id':['a'],'job_type_public':['training']}),p/'source.parquet')
            pq.write_table(pa.table({'pod_id':['a'],'first_seen_day':[109],'first_seen_hour':[0],'job_type_public':['training']}),p/'verified.parquet')
            with zipfile.ZipFile(p/'f.zip','w') as z:z.writestr('asi_opensource_pod_hourly/day=109/hour=00/part-000.parquet',b'invalid but skipped')
            cfg={'execution_permissions':{},'temporal':{'days':[108,109,110],'stratification_categories':['training'],'max_transfer_bytes':1000000}}
            result=run(cfg,p/'source.parquet',p/'out',fixture_zip=p/'f.zip',verified_map=p/'verified.parquet')
            self.assertEqual(result['mapped_pods'],1)
            self.assertIsNone(result['hours'][0]['historic_transfer_bytes'])

    def test_budget_exhausted_before_transport(self):
        from asi_pipeline.remote_temporal import RangeFile
        requests=[]
        def reserve(n):raise ValueError('budget')
        stream=RangeFile(100,8,lambda a,b:requests.append((a,b)),reserve)
        with self.assertRaisesRegex(ValueError,'budget'):stream.read(4)
        self.assertEqual(requests,[])

    def test_per_hour_diagnostics_include_abrupt_change_review(self):
        from asi_pipeline.remote_temporal import summarize_hours
        report=summarize_hours([{'day':108,'hour':0,'matched_eligible_pods':100},{'day':108,'hour':1,'matched_eligible_pods':5}])
        self.assertEqual(report[0]['previous_matched'],100)
        self.assertEqual(report[0]['current_matched'],5)

    def test_received_bytes_count_body_not_reservation(self):
        from asi_pipeline.remote_temporal import RangeFile
        received=[];reserved=[]
        class Response(io.BytesIO):
            status=206
            headers={'Content-Range':'bytes 0-3/10'}
        stream=RangeFile(10,8,lambda a,b:Response(b'abcd'),reserved.append,received.append)
        self.assertEqual(stream.read(4),b'abcd')
        self.assertEqual(sum(received),4)
        self.assertEqual(sum(reserved),5)

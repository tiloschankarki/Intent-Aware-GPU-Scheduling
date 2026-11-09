import io
import json
import tempfile
import unittest
from pathlib import Path
from asi_pipeline import safety

CONFIG = Path(__file__).resolve().parents[1] / 'config/protocol.yaml'

class Response(io.BytesIO):
    def __init__(self, body=b'abcd', status=206, headers=None):
        super().__init__(body)
        self.status = status
        self.headers = headers or {'Content-Range':'bytes 2-5/10', 'Content-Length':'4'}
        self.read_attempted = False
    def read(self, n=-1):
        self.read_attempted = True
        return super().read(n)

class SafetyTests(unittest.TestCase):
    def setUp(self):
        self.p = json.loads(CONFIG.read_text())
    def test_helpers_exist(self):
        for name in ['validate_features','assign_workload','assert_disjoint','parse_member','read_range','publish_new']:
            self.assertTrue(callable(getattr(safety,name,None)), name)
    def test_outcomes_and_unknown_features_rejected(self):
        for col in self.p['blacklisted_predictors'] + ['avg_gpu_sm_util', 'invented_user_id']:
            with self.subTest(col=col), self.assertRaises(ValueError):
                safety.validate_features(['gpu_request',col],self.p)
        safety.validate_features(['gpu_request','job_type_public'],self.p)
    def test_group_assignment_order_independent_and_no_null_group(self):
        ids=['w'+str(i) for i in range(1000)]
        a={x:safety.assign_workload(x,self.p) for x in ids}
        b={x:safety.assign_workload(x,self.p) for x in reversed(ids)}
        self.assertEqual(a,b)
        self.assertEqual(set(a.values()),{'train','validation','test'})
        with self.assertRaises(ValueError): safety.assign_workload(None,self.p)
    def test_split_contamination_fails(self):
        safety.assert_disjoint({'train':['a','a'],'validation':['b'],'test':['c']})
        with self.assertRaises(ValueError): safety.assert_disjoint({'train':['a'],'test':['a']})
        with self.assertRaises(ValueError): safety.assert_disjoint({'train':[None]})
    def test_member_bounds_and_path(self):
        self.assertEqual(safety.parse_member('asi_opensource_pod_hourly/day=109/hour=00/part-000.parquet',self.p),(109,0))
        for path in ['asi_opensource_pod_hourly/day=111/hour=00/part-000.parquet','asi_opensource_pod_hourly/day=109/hour=24/part-000.parquet','../day=109/hour=00/part-000.parquet']:
            with self.assertRaises(ValueError): safety.parse_member(path,self.p)
    def test_range_ignored_or_wrong_headers_rejected_before_body(self):
        cases=[Response(status=200),Response(headers={'Content-Range':'bytes 2-5/11'}),Response(headers={'Content-Range':'bytes 0-3/10'}),Response(headers={'Content-Range':'bytes 2-5/10','Content-Length':'999'}),Response(headers={'Content-Range':'bytes 2-5/10','Content-Encoding':'gzip'})]
        for response in cases:
            with self.subTest(headers=response.headers),self.assertRaises(ValueError):
                safety.read_range(response,2,5,10,8)
            self.assertFalse(response.read_attempted)
    def test_range_exact_short_long_and_oversized(self):
        self.assertEqual(safety.read_range(Response(),2,5,10,8),b'abcd')
        for body in [b'abc',b'abcde']:
            with self.assertRaises(ValueError): safety.read_range(Response(body),2,5,10,8)
        response=Response()
        with self.assertRaises(ValueError): safety.read_range(response,2,5,10,3)
        self.assertFalse(response.read_attempted)
    def test_publish_never_overwrites(self):
        with tempfile.TemporaryDirectory() as d:
            src=Path(d)/'stage';dst=Path(d)/'artifact'
            src.write_bytes(b'new'); dst.write_bytes(b'historical')
            with self.assertRaises(FileExistsError): safety.publish_new(src,dst)
            self.assertEqual(dst.read_bytes(),b'historical')
            dst2=Path(d)/'new_artifact'; safety.publish_new(src,dst2)
            self.assertEqual(dst2.read_bytes(),b'new')

if __name__=='__main__': unittest.main()

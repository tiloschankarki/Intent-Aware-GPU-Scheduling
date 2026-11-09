import json
import tempfile
import unittest
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
from asi_pipeline import temporal

class TemporalTests(unittest.TestCase):
    def test_verifier_exists(self):
        self.assertTrue(callable(getattr(temporal,'verify_legacy',None)))
    def fixture(self,root,ids,labels,mapids):
        source=root/'source.parquet'; legacy=root/'legacy.parquet'
        pq.write_table(pa.table({'pod_id':ids,'job_type_public':labels}),source)
        pq.write_table(pa.table({'pod_id':mapids,'first_seen_day':[109]*len(mapids),'first_seen_hour':[0]*len(mapids)}),legacy)
        return source,legacy
    def test_source_counts_not_assumed_from_legacy_or_duplicate_table(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);source,legacy=self.fixture(root,['a','b','b','c'],['training','dev','dev','unknown'],['a','b','c'])
            table,report=temporal.verify_legacy(source,legacy,['training','dev','unknown'])
            self.assertEqual(table['pod_id'].to_pylist(),['a','c'])
            self.assertEqual(table['job_type_public'].to_pylist(),['training','unknown'])
            self.assertEqual(report['excluded_repeated_pods'],1)
            self.assertEqual(report['eligible_pods'],2)
    def test_missing_source_or_invalid_label_stops(self):
        for sourceids,labels in [(['a'],['training']),(['a','b'],['training',None]),(['a','b'],['training','offline'])]:
            with self.subTest(labels=labels),tempfile.TemporaryDirectory() as d:
                source,legacy=self.fixture(Path(d),sourceids,labels,['a','b'])
                with self.assertRaises(ValueError): temporal.verify_legacy(source,legacy,['training','dev','unknown'])
    def test_duplicate_legacy_id_stops(self):
        with tempfile.TemporaryDirectory() as d:
            source,legacy=self.fixture(Path(d),['a'],['training'],['a','a'])
            with self.assertRaises(ValueError): temporal.verify_legacy(source,legacy,['training'])
    def test_wrong_legacy_hour_stops(self):
        with tempfile.TemporaryDirectory() as d:
            source,legacy=self.fixture(Path(d),['a'],['training'],['a'])
            pq.write_table(pa.table({'pod_id':['a'],'first_seen_day':[108],'first_seen_hour':[0]}),legacy)
            with self.assertRaises(ValueError): temporal.verify_legacy(source,legacy,['training'])

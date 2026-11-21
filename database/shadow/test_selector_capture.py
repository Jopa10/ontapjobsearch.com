import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from selector_capture import Capture, MODULES

SOURCE = '''def helper(x):
    return x+1

def main():
    outputs={"test":[]}
    for _, row in feed.iterrows():
        helper(1)
        keep, reason = row["keep"], "actual reason"
        if not keep:
            continue
        outputs["test"].append({"job_id": row["/Job/DisplayReference"]})
    return outputs

def keep_job(job, lookup):
    return False, "actual QA reason"
'''


class CaptureTests(unittest.TestCase):
    def load(self, root, name, source=SOURCE):
        for module in MODULES:
            (root / (module + '.py')).write_text(source)
        spec=importlib.util.spec_from_file_location('sample',root/(name+'.py'))
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_actual_gate_and_candidate_evidence_without_global_tracing(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            module=self.load(root,'finance_accounts_pipeline')
            class Feed:
                def iterrows(self):
                    return iter(enumerate([{'/Job/DisplayReference':'1','keep':False},{'/Job/DisplayReference':'2','keep':True}]))
            module.feed=Feed()
            expected=module.main()
            with Capture(root,[module.main]) as observed:
                self.assertIsNone(sys.gettrace())
                self.assertEqual(sys.monitoring.get_events(observed.tool_id),0)
                self.assertEqual(sys.monitoring.get_local_events(observed.tool_id,module.helper.__code__),0)
                self.assertEqual(module.main(),expected)
            self.assertEqual(observed.records[('finance_accounts','1')]['reason'],'actual reason')
            self.assertEqual(observed.records[('finance_accounts','2')]['decision'],'exclude')
            self.assertIsNone(sys.monitoring.get_tool(observed.tool_id))

    def test_actual_sales_qa_return_reason(self):
        with tempfile.TemporaryDirectory() as d:
            module=self.load(Path(d),'customer_sales_production_refine')
            with Capture(d,[module.keep_job]) as observed:
                self.assertEqual(module.keep_job({'job_id':'3'},[]),(False,'actual QA reason'))
            self.assertEqual(observed.records[('customer_sales','3')],{'decision':'exclude','reason':'actual QA reason','gate':'production Customer Sales QA'})

    def test_monitoring_is_removed_when_selector_raises(self):
        with tempfile.TemporaryDirectory() as d:
            module=self.load(Path(d),'finance_accounts_pipeline','def main():\n    raise ValueError("selector failed")\n')
            observer=Capture(d,[module.main])
            with self.assertRaisesRegex(ValueError,'selector failed'):
                with observer:module.main()
            self.assertIsNone(sys.gettrace())
            self.assertIsNone(sys.monitoring.get_tool(observer.tool_id))


if __name__ == '__main__':
    unittest.main()

import importlib.util
from pathlib import Path
import tempfile
import unittest
from selector_capture import Capture


class CaptureTests(unittest.TestCase):
    def test_observer_records_executed_gate_without_changing_result(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = '''def main():
    feed = Feed()
    outputs = {"test": []}
    for _, row in feed.iterrows():
        keep, reason = row["keep"], "actual reason"
        if not keep:
            continue
        outputs["test"].append({"job_id": row["/Job/DisplayReference"]})
    for job in outputs["test"]:
        if job:
            continue
    return outputs
'''
            from selector_capture import MODULES
            for name in MODULES:
                (root / (name + '.py')).write_text(source)
            spec = importlib.util.spec_from_file_location('sample', root / 'finance_accounts_pipeline.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            class Feed:
                def iterrows(self):
                    return iter(enumerate([{'/Job/DisplayReference': '1', 'keep': False}, {'/Job/DisplayReference': '2', 'keep': True}]))
            module.Feed = Feed
            expected = module.main()
            with Capture(root) as observed:
                self.assertEqual(module.main(), expected)
            self.assertEqual(observed.records[('finance_accounts', '1')]['reason'], 'actual reason')
            self.assertEqual(observed.records[('finance_accounts', '2')]['decision'], 'exclude')


if __name__ == '__main__':
    unittest.main()

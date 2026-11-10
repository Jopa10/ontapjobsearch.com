import unittest
from pathlib import Path

from run_selector_parity import resolve_source_request


class FreshSourceRequestTests(unittest.TestCase):
    def test_accepts_owner_pinned_three_november_metadata(self):
        request_path = Path(__file__).with_name('fresh-integration-prep-checkpoint-2026-11-03.json')
        resolved = resolve_source_request(request_path)

        self.assertEqual(resolved['feedDate'], '2026-11-03')
        self.assertEqual(resolved['sizeBytes'], 35_800_056)
        self.assertEqual(resolved['sourceRows'], 44_432)
        self.assertEqual(resolved['cleanRecords'], 44_430)
        self.assertEqual(resolved['conflictingIdsHeld'], ['1401786160'])

    def test_accepts_owner_pinned_four_november_fingerprint_without_assumed_counts(self):
        request_path = Path(__file__).with_name('fresh-integration-prep-checkpoint-2026-11-04.json')
        resolved = resolve_source_request(request_path)

        self.assertEqual(resolved['feedDate'], '2026-11-04')
        self.assertEqual(resolved['sizeBytes'], 35_216_405)
        self.assertEqual(resolved['archiveSha256'],
                         'd691ee876b6f93d1518ee6019fb28f8e036cad9e9d7d0eb9fb12330e08d78b06')
        self.assertIsNone(resolved['sourceRows'])
        self.assertIsNone(resolved['cleanRecords'])
        self.assertIsNone(resolved['conflictingIdsHeld'])

if __name__ == '__main__':
    unittest.main()

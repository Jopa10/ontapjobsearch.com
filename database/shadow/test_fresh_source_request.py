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


if __name__ == '__main__':
    unittest.main()

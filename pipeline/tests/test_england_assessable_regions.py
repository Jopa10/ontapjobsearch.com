from __future__ import annotations

import json
import unittest
from pathlib import Path


PIPELINE_ROOT = Path(__file__).resolve().parents[1]
ASSESSABLE = PIPELINE_ROOT / "config" / "england_assessable_regions.json"
OPERATIONAL = PIPELINE_ROOT / "config" / "job_slice_catalog.json"


class EnglandAssessableRegionTests(unittest.TestCase):
    def test_reconciled_universe_is_55_and_contains_known_omissions(self) -> None:
        data = json.loads(ASSESSABLE.read_text(encoding="utf-8"))
        regions = data["regions"]
        self.assertEqual(data["region_count"], 55)
        self.assertEqual(len(regions), 55)
        self.assertIn("Merseyside - Liverpool", regions)
        self.assertIn("Leicestershire", regions)
        self.assertIn("Bedfordshire", regions)
        self.assertIn("Derbyshire", regions)
        self.assertIn("Suffolk", regions)

    def test_old_operational_33_is_a_strict_subset_of_assessable_universe(self) -> None:
        assessable = json.loads(ASSESSABLE.read_text(encoding="utf-8"))["regions"]
        operational = json.loads(OPERATIONAL.read_text(encoding="utf-8"))["regions"]
        operational_england = {
            name for name in operational if name != "Northern Ireland - East"
        }
        self.assertEqual(len(operational_england), 33)
        self.assertTrue(operational_england < set(assessable))
        self.assertEqual(len(set(assessable) - operational_england), 22)

    def test_north_east_rollup_covers_all_three_lookup_components(self) -> None:
        data = json.loads(ASSESSABLE.read_text(encoding="utf-8"))
        self.assertEqual(
            data["detail_rollups"],
            {
                "North East - Tyneside, Wearside & Northumberland": "North East",
                "North East - County Durham & Darlington/Hartlepool": "North East",
                "North East - Tees Valley": "North East",
            },
        )


if __name__ == "__main__":
    unittest.main()

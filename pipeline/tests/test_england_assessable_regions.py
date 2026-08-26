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

    def test_configured_england_markets_must_be_inside_assessable_universe(self) -> None:
        assessable = set(json.loads(ASSESSABLE.read_text(encoding="utf-8"))["regions"])
        operational = json.loads(OPERATIONAL.read_text(encoding="utf-8"))["regions"]
        approved_non_england = {
            "Northern Ireland - East",
            "Scotland Central - Edinburgh & Lothians",
            "Scotland West - Glasgow",
        }
        configured_england = set(operational) - approved_non_england
        self.assertTrue(configured_england <= assessable)

        immediate_live_additions = {
            "Leicestershire",
            "Cheshire - Warrington & Halton",
            "Cornwall",
            "Suffolk",
            "Derbyshire",
            "Cheshire - East",
            "Lincolnshire",
            "Merseyside - Liverpool",
            "Shropshire",
            "Greater Manchester - Wigan & Bolton",
            "West Midlands - Black Country",
            "Cheshire - West",
            "Worcestershire",
        }
        self.assertTrue(immediate_live_additions <= configured_england)

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

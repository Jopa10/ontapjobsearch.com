from __future__ import annotations

import json
import unittest
from pathlib import Path


PIPELINE_ROOT = Path(__file__).resolve().parents[1]
UK_ASSESSABLE = PIPELINE_ROOT / "config" / "uk_assessable_regions.json"
ENGLAND_ASSESSABLE = PIPELINE_ROOT / "config" / "england_assessable_regions.json"
OPERATIONAL = PIPELINE_ROOT / "config" / "job_slice_catalog.json"


class UKAssessableRegionTests(unittest.TestCase):
    def test_uk_universe_is_73_and_contains_all_four_nations(self) -> None:
        data = json.loads(UK_ASSESSABLE.read_text(encoding="utf-8"))
        regions = data["regions"]
        self.assertEqual(data["region_count"], 73)
        self.assertEqual(len(regions), 73)
        self.assertIn("London", regions)
        self.assertIn("Scotland West - Glasgow", regions)
        self.assertIn("Wales South - Cardiff & Vale", regions)
        self.assertIn("Northern Ireland - East", regions)
        self.assertIn("Northern Ireland - West", regions)

    def test_all_55_england_markets_are_preserved(self) -> None:
        uk = set(json.loads(UK_ASSESSABLE.read_text(encoding="utf-8"))["regions"])
        england = set(json.loads(ENGLAND_ASSESSABLE.read_text(encoding="utf-8"))["regions"])
        self.assertEqual(len(england), 55)
        self.assertTrue(england <= uk)
        self.assertEqual(len(uk - england), 18)

    def test_every_configured_public_market_is_assessable(self) -> None:
        uk = set(json.loads(UK_ASSESSABLE.read_text(encoding="utf-8"))["regions"])
        configured = set(json.loads(OPERATIONAL.read_text(encoding="utf-8"))["regions"])
        self.assertTrue(configured <= uk)

    def test_safe_detail_aliases_roll_up_to_canonical_markets(self) -> None:
        data = json.loads(UK_ASSESSABLE.read_text(encoding="utf-8"))
        rollups = data["detail_rollups"]
        expected = {
            "North East - Tyneside, Wearside & Northumberland": "North East",
            "North East - County Durham & Darlington/Hartlepool": "North East",
            "North East - Tees Valley": "North East",
            "Flintshire": "North Wales - East",
            "Caerphilly": "Wales South - Valleys",
            "Wales South -gwent": "Wales South - Gwent",
            "South Lanarkshire": "Scotland West - Lanarkshire",
        }
        for source, target in expected.items():
            self.assertEqual(rollups.get(source), target)


if __name__ == "__main__":
    unittest.main()

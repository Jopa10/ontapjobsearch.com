from __future__ import annotations

import json
import unittest
from pathlib import Path


PIPELINE_ROOT = Path(__file__).resolve().parents[1]
UK_ASSESSABLE = PIPELINE_ROOT / "config" / "uk_assessable_regions.json"
ENGLAND_ASSESSABLE = PIPELINE_ROOT / "config" / "england_assessable_regions.json"
OPERATIONAL = PIPELINE_ROOT / "config" / "job_slice_catalog.json"


class UKAssessableRegionTests(unittest.TestCase):
    def test_uk_universe_is_78_and_contains_all_four_nations(self) -> None:
        data = json.loads(UK_ASSESSABLE.read_text(encoding="utf-8"))
        regions = data["regions"]
        self.assertEqual(data["region_count"], 78)
        self.assertEqual(len(regions), 78)
        self.assertIn("London", regions)
        self.assertIn("Scotland West - Glasgow", regions)
        self.assertIn("Wales South - Cardiff & Vale", regions)
        self.assertIn("Northern Ireland - East", regions)
        self.assertIn("Northern Ireland - West", regions)
        self.assertIn("Lancashire - West", regions)
        self.assertIn("Merseyside - Sefton", regions)
        self.assertIn("Merseyside - St Helens & Knowsley", regions)
        self.assertIn("Scotland - Borders", regions)
        self.assertIn("Wales - Mid", regions)

    def test_historic_55_england_subset_is_preserved(self) -> None:
        uk = set(json.loads(UK_ASSESSABLE.read_text(encoding="utf-8"))["regions"])
        england = set(json.loads(ENGLAND_ASSESSABLE.read_text(encoding="utf-8"))["regions"])
        self.assertEqual(len(england), 55)
        self.assertTrue(england <= uk)
        self.assertEqual(len(uk - england), 23)

    def test_every_configured_public_market_is_assessable(self) -> None:
        uk = set(json.loads(UK_ASSESSABLE.read_text(encoding="utf-8"))["regions"])
        configured = set(json.loads(OPERATIONAL.read_text(encoding="utf-8"))["regions"])
        self.assertTrue(configured <= uk)

        approved_non_england_service_admin_markets = {
            "Northern Ireland - East",
            "Scotland Central - Edinburgh & Lothians",
            "Scotland West - Glasgow",
        }
        self.assertTrue(approved_non_england_service_admin_markets <= configured)

    def test_safe_detail_aliases_roll_up_to_canonical_markets(self) -> None:
        data = json.loads(UK_ASSESSABLE.read_text(encoding="utf-8"))
        rollups = data["detail_rollups"]
        expected = {
            "North East - Tyneside, Wearside & Northumberland": "North East",
            "North East - County Durham & Darlington/Hartlepool": "North East",
            "North East - Tees Valley": "North East",
            "devon": "Devon",
            "West Sussex": "Sussex",
            "Aberdeenshire": "North Scotland",
            "Highland": "North Scotland",
            "Highlands & Islands": "North Scotland",
            "Dumfries & Galloway, Scotland": "Scotland - Borders",
            "Clackmannanshire": "Scotland Central - Falkirk & Stirling",
            "Midlothian": "Scotland Central - Edinburgh & Lothians",
            "West Lothian": "Scotland Central - Edinburgh & Lothians",
            "South Lanarkshire": "Scotland West - Lanarkshire",
            "Flintshire": "North Wales - East",
            "Gwynedd": "North Wales - West",
            "Isle of Anglesey": "North Wales - West",
            "Carmarthenshire": "Wales - West",
            "Caerphilly": "Wales South - Valleys",
            "Monmouthshire": "Wales South - Gwent",
            "Vale of Glamorgan": "Wales South - Cardiff & Vale",
            "Wales South -gwent": "Wales South - Gwent",
        }
        for source, target in expected.items():
            self.assertEqual(rollups.get(source), target)

    def test_ambiguous_or_non_uk_clusters_are_not_forced(self) -> None:
        data = json.loads(UK_ASSESSABLE.read_text(encoding="utf-8"))
        excluded = set(data["excluded_non_market_clusters"])
        self.assertTrue({"Channel Islands", "unknown", "East Midlands", "East of England", "South West", "West Midlands"} <= excluded)
        self.assertNotIn("South West", data["detail_rollups"])
        self.assertNotIn("West Midlands", data["detail_rollups"])


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

from scripts.build_daily_region_overview import FAMILIES, _live_count_for_market


class LiveRegionalRollupTests(unittest.TestCase):
    def test_overview_includes_all_six_governed_families(self) -> None:
        self.assertEqual(
            [family["label"] for family in FAMILIES],
            ["Service admin", "Support worker", "Sales advisor", "Paralegal", "Marketing", "HR / Recruitment"],
        )
        self.assertEqual(FAMILIES[3]["published_slug"], "paralegal-jobs")
        self.assertEqual(FAMILIES[4]["published_slug"], "marketing-jobs")
        self.assertEqual(FAMILIES[5]["published_slug"], "hr-recruitment-jobs")

    def test_canonical_market_includes_direct_and_detail_alias_counts(self) -> None:
        category = "Admin/Service – Office Support"
        counts = {
            ("North East", category): 29,
            ("North East - Tyneside, Wearside & Northumberland", category): 49,
            ("North East - County Durham & Darlington/Hartlepool", category): 8,
            ("North East - Tees Valley", category): 3,
            ("Yorkshire - West", category): 48,
        }
        rollups = {
            "North East - Tyneside, Wearside & Northumberland": "North East",
            "North East - County Durham & Darlington/Hartlepool": "North East",
            "North East - Tees Valley": "North East",
        }

        self.assertEqual(
            _live_count_for_market(counts, rollups, "North East", category),
            89,
        )

    def test_unrelated_aliases_do_not_leak_into_market(self) -> None:
        category = "Support Worker – Wide"
        counts = {
            ("North East", category): 6,
            ("Yorkshire - West", category): 2,
        }
        rollups = {
            "North East - Tyneside, Wearside & Northumberland": "North East",
        }

        self.assertEqual(
            _live_count_for_market(counts, rollups, "North East", category),
            6,
        )


if __name__ == "__main__":
    unittest.main()

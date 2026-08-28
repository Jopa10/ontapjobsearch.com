from __future__ import annotations

import unittest

from scripts.build_daily_region_overview import (
    FAMILIES,
    _live_count_for_market,
    _site_inventory_summary,
)
from scripts.live_job_source_counter import LiveInventory, LiveJob, LivePlacement


class LiveRegionalRollupTests(unittest.TestCase):
    def test_overview_includes_all_eight_governed_families(self) -> None:
        self.assertEqual(
            [family["label"] for family in FAMILIES],
            ["Service admin", "Support worker", "Sales advisor", "Paralegal", "Marketing", "Finance / Accounts", "HR / Recruitment", "CS / Contact centre"],
        )
        self.assertEqual(FAMILIES[3]["published_slug"], "paralegal-jobs")
        self.assertEqual(FAMILIES[4]["published_slug"], "marketing-jobs")
        self.assertEqual(FAMILIES[5]["published_slug"], "finance-accounts-jobs")
        self.assertEqual(FAMILIES[6]["published_slug"], "hr-recruitment-jobs")
        self.assertEqual(FAMILIES[7]["published_slug"], "customer-service-jobs")

    def test_sitewide_inventory_reconciles_unique_jobs_and_slice_placements(self) -> None:
        jobs = [
            LiveJob("j1", "Administrator", "Leeds", "Yorkshire - West", "Admin", "JobG8", "https://example/j1", "app/west-yorkshire/service-administrator-jobs.json"),
            LiveJob("j2", "NHS Administrator", "Leeds", "Yorkshire - West", "Unspecified", "NHS Jobs", "https://example/j2", "app/west-yorkshire/service-administrator-jobs.json"),
            LiveJob("j3", "Future role", "Leeds", "Yorkshire - West", "Admin", "WhatJobs", "https://example/j3", "app/west-yorkshire/service-administrator-jobs.json"),
        ]
        placements = [
            LivePlacement("j1", "j1", "Yorkshire - West", "Admin", "JobG8", "app/west-yorkshire/service-administrator-jobs.json"),
            LivePlacement("j1", "j1", "Yorkshire - West", "Finance / Accounts", "JobG8", "app/_city-pages/configured-slices/west-yorkshire/finance-accounts-jobs.json"),
            LivePlacement("j2", "j2", "Yorkshire - West", "Unspecified", "NHS Jobs", "app/west-yorkshire/service-administrator-jobs.json"),
            LivePlacement("j3", "j3", "Yorkshire - West", "Admin", "WhatJobs", "app/west-yorkshire/service-administrator-jobs.json"),
        ]
        summary = _site_inventory_summary(
            LiveInventory(jobs, placements, 2, 1, 1),
            report_date="2026-08-28",
            rollups={},
            statuses={
                ("Yorkshire - West", "admin_service"): "LIVE",
                ("Yorkshire - West", "finance_accounts"): "LIVE",
            },
        )

        self.assertEqual(summary.unique_live_jobs, 3)
        self.assertEqual(summary.unique_jobg8_jobs, 1)
        self.assertEqual(summary.unique_external_jobs, 2)
        self.assertEqual(summary.slice_placements, 4)
        self.assertEqual(summary.jobs_on_multiple_slices, 1)
        self.assertEqual(summary.extra_slice_placements, 1)
        self.assertEqual(summary.jobs_outside_governed_slices, 0)
        self.assertEqual(summary.provider_counts["WhatJobs"], 1)
        self.assertEqual(summary.provider_duplicate_jobs["JobG8"], 1)

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

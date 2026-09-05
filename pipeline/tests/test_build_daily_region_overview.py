from __future__ import annotations

import unittest
from unittest.mock import patch

from scripts.build_daily_region_overview import (
    FAMILIES,
    _live_count_for_market,
    _city_opportunity_rows,
    _load_jobg8_category_profile,
    _load_family_coverage_date,
    _published_page_inventory,
    _site_inventory_summary,
)
from scripts.live_job_source_counter import LiveInventory, LiveJob, LivePlacement


class LiveRegionalRollupTests(unittest.TestCase):
    def test_city_opportunities_count_all_unique_live_roles_once(self) -> None:
        from pathlib import Path
        import json
        import tempfile
        from openpyxl import Workbook

        jobs = [
            LiveJob("j1", "Administrator", "Lincoln", "Lincolnshire", "Admin", "JobG8", "https://example/j1", "app/a.json"),
            LiveJob("j2", "Marketing Executive", "Lincoln", "Lincolnshire", "Marketing", "JobG8", "https://example/j2", "app/b.json"),
            LiveJob("j3", "Support Worker", "Lincolnshire", "Lincolnshire", "Support", "NHS Jobs", "https://example/j3", "app/c.json"),
        ]
        inventory = LiveInventory(jobs, [], 3, 0, 0)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            geo = root / "geo.xlsx"
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Sheet1"
            sheet.append(["Area", "Cluster"])
            sheet.append(["Lincoln", "Lincolnshire"])
            sheet.append(["Lincolnshire", "Lincolnshire"])
            workbook.save(geo)
            register = root / "cities.json"
            register.write_text(json.dumps([]), encoding="utf-8")
            rows, mapped_jobs, unmapped_jobs = _city_opportunity_rows(
                inventory, geo_lookup_path=geo, city_register_path=register
            )

        self.assertEqual([(row.locality, row.live_jobs) for row in rows], [("Lincoln", 2)])
        self.assertEqual(mapped_jobs, 2)
        self.assertEqual(unmapped_jobs, 1)

    def test_page_inventory_reconciles_and_expands_london_routes(self) -> None:
        rows, counts = _published_page_inventory()
        self.assertEqual(
            counts["Total"],
            counts["Individual job"] + counts["Regional/category"] + counts["City"] + counts["Core"],
        )
        routes = {row[4] for row in rows if row[0] == "Detail"}
        london_admin_routes = {
            "/london/service-administrator-jobs",
            "/london/central-service-administrator-jobs",
            "/london/north-service-administrator-jobs",
            "/london/east-service-administrator-jobs",
            "/london/south-service-administrator-jobs",
            "/london/west-service-administrator-jobs",
        }
        self.assertTrue(london_admin_routes.issubset(routes))
        self.assertTrue({"/nottingham/jobs", "/wakefield/jobs", "/salford/jobs"}.issubset(routes))
        self.assertEqual(counts["City"], 35)

    def test_family_coverage_requires_one_feed_date(self) -> None:
        from pathlib import Path
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            coverage = Path(directory) / "reports-daily" / "daily-family-coverage.csv"
            coverage.parent.mkdir()
            coverage.write_text(
                "feed_date,region,family,selected_count\n"
                "2026-09-02,London,service_admin,2\n"
                "2026-09-02,Kent,service_admin,1\n",
                encoding="utf-8",
            )
            with patch("scripts.build_daily_region_overview.PIPELINE_ROOT", Path(directory)):
                self.assertEqual(_load_family_coverage_date(), "2026-09-02")

    def test_jobg8_profile_reconciles_category_counts(self) -> None:
        from pathlib import Path
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            profile = Path(directory) / "profile.csv"
            profile.write_text(
                "feed_date,total_jobs,published_jobg8_jobs,jobg8_category,count,published_count\n"
                "2026-09-01,5354,1308,I.T. & Communications,2547,684\n"
                "2026-09-01,5354,1308,Administration,2807,624\n",
                encoding="utf-8",
            )
            with patch("scripts.build_daily_region_overview.JOBG8_CATEGORY_PROFILE", profile):
                loaded = _load_jobg8_category_profile()
        self.assertEqual(loaded.total_jobs, 5354)
        self.assertEqual(loaded.published_jobs, 1308)
        self.assertEqual(loaded.counts[0], ("I.T. & Communications", 2547, 684))

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

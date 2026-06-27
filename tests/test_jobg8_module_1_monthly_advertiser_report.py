import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "pipeline" / "scripts" / "jobg8_module_1_monthly_advertiser_report.py"
spec = importlib.util.spec_from_file_location("jobg8_module_1_monthly_advertiser_report", SCRIPT)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


ADVERTISER_COLUMNS = [
    "month", "advertiser", "advertiser_type", "advertiser_type_source", "unique_job_ids", "feed_appearances", "new_jobs_first_seen",
    "current_live_jobs", "unique_role_count", "unique_roles", "unique_location_count",
    "unique_locations", "unique_region_count", "unique_regions", "first_day_seen", "last_day_seen",
    "days_active", "average_feed_appearances_per_active_day", "peak_daily_live_jobs",
    "top_roles", "top_regions", "campaign_trend", "first_five_day_live_average",
    "last_five_day_live_average", "first_vs_last_five_day_change_pct",
]

ROLE_COLUMNS = [
    "month", "normalised_title", "slice", "example_live_titles", "total_adverts", "days_active",
    "first_day_seen", "last_day_seen", "average_adverts_per_active_day", "peak_daily_count",
    "unique_advertisers", "unique_regions", "unique_locations", "top_advertisers", "top_regions",
    "first_five_day_average", "last_five_day_average", "first_vs_last_five_day_change_pct",
    "trend_label", "top_advertiser_share_pct",
]


def row(date, job_id, title, advertiser, location, region, slices):
    return {
        "month_date": date,
        "job_id": job_id,
        "title": title,
        "normalised_title": module.norm_key(title) or "unknown title",
        "advertiser": advertiser,
        "advertiser_type": "Direct",
        "location": location,
        "raw_location": location,
        "lookup_region": region,
        "source_file": f"{date}.xlsx",
        "slices": slices,
    }


def count_sum(top_list):
    total = 0
    if not top_list:
        return total
    for part in top_list.split("; "):
        total += int(part.rsplit("(", 1)[1].rstrip(")"))
    return total


class Module1AdvertiserReportTests(unittest.TestCase):
    def test_outputs_have_required_columns_and_no_old_summary_columns(self):
        advertiser_campaigns, role_trends, advertiser_type_summary = module.build_reports(
            [row("2026-06-01", "1", "Support Worker", "Alpha Care", "Leeds", "Yorkshire - West", ["support_worker"])],
            ["2026-06-01"],
            "2026-06",
        )

        self.assertEqual(list(advertiser_campaigns[0]), ADVERTISER_COLUMNS)
        self.assertEqual(list(role_trends[0]), ROLE_COLUMNS)
        old_columns = {"region", "region_scope", "category", "total_jobs", "feed_days", "days_seen", "top_titles", "total_adverts", "average_adverts_per_active_day", "peak_daily_adverts"}
        self.assertTrue(old_columns.isdisjoint(advertiser_campaigns[0]))

    def test_advertiser_totals_are_not_inflated_by_multi_slice_expansion_and_one_row_per_advertiser(self):
        rows = [
            row("2026-06-01", "1", "Support Worker", "Alpha Care", "Leeds", "Yorkshire - West", ["support_worker", "admin_service"]),
            row("2026-06-01", "2", "Support Worker", "Alpha Care", "Bradford", "Yorkshire - West", ["support_worker"]),
            row("2026-06-02", "3", "Finance Assistant", "Alpha Care", "Durham", "North East - County Durham & Darlington/Hartlepool", ["finance_accounts"]),
            row("2026-06-02", "4", "Picker", "Beta Logistics", "Leeds", "Yorkshire - West", ["warehouse_logistics"]),
        ]

        advertiser_campaigns, _, _ = module.build_reports(rows, ["2026-06-01", "2026-06-02"], "2026-06")
        by_advertiser = {campaign["advertiser"]: campaign for campaign in advertiser_campaigns}

        self.assertEqual(len(advertiser_campaigns), 2)
        self.assertEqual(by_advertiser["Alpha Care"]["unique_job_ids"], 3)
        self.assertEqual(by_advertiser["Alpha Care"]["feed_appearances"], 3)
        self.assertEqual(by_advertiser["Alpha Care"]["days_active"], 2)
        self.assertEqual(by_advertiser["Alpha Care"]["peak_daily_live_jobs"], 2)
        self.assertEqual(count_sum(by_advertiser["Alpha Care"]["top_roles"]), 3)
        self.assertEqual(count_sum(by_advertiser["Alpha Care"]["top_regions"]), 3)

    def test_repeated_same_job_across_ten_feeds_separates_unique_jobs_from_feed_appearances(self):
        dates = [f"2026-06-{day:02d}" for day in range(1, 11)]
        rows = [row(date, "job-1", "Support Worker", "Repeat Care", "Leeds", "Yorkshire - West", ["support_worker"]) for date in dates]

        advertiser_campaigns, _, _ = module.build_reports(rows, dates, "2026-06")
        campaign = advertiser_campaigns[0]

        self.assertEqual(campaign["unique_job_ids"], 1)
        self.assertEqual(campaign["feed_appearances"], 10)
        self.assertEqual(campaign["days_active"], 10)

    def test_current_live_jobs_uses_latest_feed_date_only_and_new_jobs_are_distinct(self):
        rows = [
            row("2026-06-01", "job-1", "Support Worker", "Alpha Care", "Leeds", "Yorkshire - West", ["support_worker"]),
            row("2026-06-02", "job-1", "Support Worker", "Alpha Care", "Leeds", "Yorkshire - West", ["support_worker"]),
            row("2026-06-02", "job-2", "Care Assistant", "Alpha Care", "Durham", "North East", ["support_worker"]),
            row("2026-06-03", "job-2", "Care Assistant", "Alpha Care", "Durham", "North East", ["support_worker"]),
        ]

        advertiser_campaigns, _, _ = module.build_reports(rows, ["2026-06-01", "2026-06-02", "2026-06-03"], "2026-06")
        campaign = advertiser_campaigns[0]

        self.assertEqual(campaign["unique_job_ids"], 2)
        self.assertEqual(campaign["new_jobs_first_seen"], 2)
        self.assertEqual(campaign["current_live_jobs"], 1)

    def test_top_roles_and_regions_count_distinct_job_ids_not_daily_repeats(self):
        rows = [
            *[row(f"2026-06-{day:02d}", "job-1", "Support Worker", "Alpha Care", "Leeds", "Yorkshire - West", ["support_worker"]) for day in range(1, 6)],
            row("2026-06-01", "job-2", "Care Assistant", "Alpha Care", "Durham", "North East", ["support_worker"]),
            row("2026-06-01", "job-3", "Care Assistant", "Alpha Care", "Durham", "North East", ["support_worker"]),
        ]

        advertiser_campaigns, _, _ = module.build_reports(rows, [f"2026-06-{day:02d}" for day in range(1, 6)], "2026-06")
        campaign = advertiser_campaigns[0]

        self.assertIn("care assistant (2)", campaign["top_roles"])
        self.assertIn("support worker (1)", campaign["top_roles"])
        self.assertIn("North East (2)", campaign["top_regions"])
        self.assertIn("Yorkshire - West (1)", campaign["top_regions"])

    def test_sustained_high_volume_campaign_is_not_labelled_spike(self):
        dates = [f"2026-06-{day:02d}" for day in range(1, 27)]
        rows = []
        for date in dates[:5]:
            rows.extend(row(date, f"early-{index}", "Support Worker", "Sustained Care", "Leeds", "Yorkshire - West", ["support_worker"]) for index in range(20))
        for date in dates[5:21]:
            rows.extend(row(date, f"steady-{date}-{index}", "Support Worker", "Sustained Care", "Leeds", "Yorkshire - West", ["support_worker"]) for index in range(10))
        for date in dates[21:]:
            rows.extend(row(date, f"late-{index}", "Support Worker", "Sustained Care", "Leeds", "Yorkshire - West", ["support_worker"]) for index in range(8))

        advertiser_campaigns, _, _ = module.build_reports(rows, dates, "2026-06")

        self.assertNotEqual(advertiser_campaigns[0]["campaign_trend"], "spike")

    def test_role_output_is_one_row_per_normalised_title_and_slice_with_unclassified(self):
        rows = [
            row("2026-06-01", "1", "Support Worker", "Alpha Care", "Leeds", "Yorkshire - West", ["support_worker", "admin_service"]),
            row("2026-06-02", "2", "Support Worker", "Beta Care", "Bradford", "Yorkshire - West", ["support_worker"]),
            row("2026-06-02", "3", "Mystery Role", "Beta Care", "Durham", "North East", ["unclassified"]),
            row("2026-06-03", "4", "Mystery Role", "Gamma Care", "Durham", "North East", ["unclassified"]),
        ]

        _, role_trends, _ = module.build_reports(rows, ["2026-06-01", "2026-06-02", "2026-06-03"], "2026-06")
        keys = [(role["normalised_title"], role["slice"]) for role in role_trends]

        self.assertEqual(len(keys), len(set(keys)))
        self.assertIn(("support worker", "support_worker"), keys)
        self.assertIn(("support worker", "admin_service"), keys)
        self.assertIn(("mystery role", "unclassified"), keys)

        support_admin = next(role for role in role_trends if (role["normalised_title"], role["slice"]) == ("support worker", "admin_service"))
        self.assertEqual(support_admin["total_adverts"], 1)
        self.assertEqual(support_admin["days_active"], 1)
        self.assertEqual(support_admin["peak_daily_count"], 1)
        self.assertEqual(count_sum(support_admin["top_advertisers"]), 1)
        self.assertEqual(count_sum(support_admin["top_regions"]), 1)
        self.assertEqual(float(support_admin["top_advertiser_share_pct"]), 100.0)

        mystery = next(role for role in role_trends if (role["normalised_title"], role["slice"]) == ("mystery role", "unclassified"))
        self.assertEqual(mystery["total_adverts"], 2)
        self.assertEqual(mystery["days_active"], 2)
        self.assertEqual(mystery["peak_daily_count"], 1)
        self.assertEqual(count_sum(mystery["top_advertisers"]), 2)

    def test_load_register_uses_register_csv_without_fallback_discovery(self):
        with tempfile.TemporaryDirectory() as tempdir:
            register_path = Path(tempdir) / "support_worker_title_classification_register.csv"
            with register_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["title", "classification"])
                writer.writeheader()
                writer.writerow({"title": "Support Worker", "classification": "HIGH_CONFIDENCE"})

            register = module.load_register(register_path)

            self.assertEqual(register, {"support worker": "HIGH_CONFIDENCE"})


if __name__ == "__main__":
    unittest.main()

class Module1AdvertiserTypeTests(unittest.TestCase):
    def test_lookup_overrides_contradictory_feed_and_mars_is_lookup_direct_employer(self):
        rows = [row("2026-06-01", "1", "Support Worker", "Mars", "Leeds", "Yorkshire - West", ["support_worker"])]
        rows[0]["advertiser_type"] = "Recruiter"
        campaigns, _, _ = module.build_reports(rows, ["2026-06-01"], "2026-06", {"mars": "direct_employer"})
        self.assertEqual(campaigns[0]["advertiser_type"], "direct_employer")
        self.assertEqual(campaigns[0]["advertiser_type_source"], "lookup")

    def test_recognised_feed_fallback_and_consistent_feed_source(self):
        rows = [
            row("2026-06-01", "1", "Support Worker", "Feed Care", "Leeds", "Yorkshire - West", ["support_worker"]),
            row("2026-06-02", "2", "Support Worker", "Feed Care", "Leeds", "Yorkshire - West", ["support_worker"]),
        ]
        for item in rows:
            item["advertiser_type"] = "Recruitment Agency"
        campaigns, _, _ = module.build_reports(rows, ["2026-06-01", "2026-06-02"], "2026-06", {})
        self.assertEqual(campaigns[0]["advertiser_type"], "recruitment_agency")
        self.assertEqual(campaigns[0]["advertiser_type_source"], "feed")

    def test_mixed_recognised_feed_values_use_feed_majority(self):
        rows = [
            row("2026-06-01", "1", "Support Worker", "Mixed Care", "Leeds", "Yorkshire - West", ["support_worker"]),
            row("2026-06-02", "2", "Support Worker", "Mixed Care", "Leeds", "Yorkshire - West", ["support_worker"]),
            row("2026-06-03", "3", "Support Worker", "Mixed Care", "Leeds", "Yorkshire - West", ["support_worker"]),
        ]
        rows[0]["advertiser_type"] = "Direct"
        rows[1]["advertiser_type"] = "Recruiter"
        rows[2]["advertiser_type"] = "Recruiter"
        campaigns, _, _ = module.build_reports(rows, ["2026-06-01", "2026-06-02", "2026-06-03"], "2026-06", {})
        self.assertEqual(campaigns[0]["advertiser_type"], "recruitment_agency")
        self.assertEqual(campaigns[0]["advertiser_type_source"], "feed_majority")

    def test_missing_or_unusable_feed_values_become_unknown_unavailable(self):
        rows = [row("2026-06-01", "1", "Support Worker", "Unknown Care", "Leeds", "Yorkshire - West", ["support_worker"])]
        rows[0]["advertiser_type"] = "not classified"
        campaigns, _, _ = module.build_reports(rows, ["2026-06-01"], "2026-06", {})
        self.assertEqual(campaigns[0]["advertiser_type"], "unknown")
        self.assertEqual(campaigns[0]["advertiser_type_source"], "unavailable")

    def test_lookup_values_are_loaded_not_hard_coded_and_conflicts_fail(self):
        with tempfile.TemporaryDirectory() as tempdir:
            lookup_path = Path(tempdir) / "advertiser_type_lookup.csv"
            lookup_path.write_text("advertiser,advertiser_type,source_note\nCustom Employer,direct_employer,test\n", encoding="utf-8")
            self.assertEqual(module.load_advertiser_type_lookup(lookup_path), {"custom employer": "direct_employer"})
            lookup_path.write_text("advertiser,advertiser_type,source_note\nAcme,direct_employer,a\n acme ,recruitment_agency,b\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                module.load_advertiser_type_lookup(lookup_path)

    def test_advertiser_type_summary_totals_reconcile_exactly(self):
        rows = [
            row("2026-06-01", "1", "Support Worker", "Direct Co", "Leeds", "Yorkshire - West", ["support_worker"]),
            row("2026-06-01", "2", "Support Worker", "Agency Co", "Leeds", "Yorkshire - West", ["support_worker"]),
            row("2026-06-02", "2", "Support Worker", "Agency Co", "Leeds", "Yorkshire - West", ["support_worker"]),
            row("2026-06-02", "3", "Support Worker", "Mystery Co", "Leeds", "Yorkshire - West", ["support_worker"]),
        ]
        rows[0]["advertiser_type"] = "Direct"
        rows[1]["advertiser_type"] = "Recruiter"
        rows[2]["advertiser_type"] = "Recruiter"
        rows[3]["advertiser_type"] = ""
        campaigns, _, summary = module.build_reports(rows, ["2026-06-01", "2026-06-02"], "2026-06", {})
        self.assertEqual([item["advertiser_type"] for item in summary], module.REPORT_ADVERTISER_TYPES)
        self.assertEqual(sum(item["advertiser_count"] for item in summary), len(campaigns))
        for field in ["unique_job_ids", "feed_appearances", "new_jobs_first_seen", "current_live_jobs"]:
            self.assertEqual(sum(item[field] for item in summary), sum(campaign[field] for campaign in campaigns))

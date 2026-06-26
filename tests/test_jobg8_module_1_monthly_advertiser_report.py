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
    "month", "advertiser", "total_adverts", "unique_role_count", "unique_roles",
    "unique_location_count", "unique_locations", "unique_region_count", "unique_regions",
    "first_day_seen", "last_day_seen", "days_active", "average_adverts_per_active_day",
    "peak_daily_adverts", "top_roles", "top_regions", "campaign_trend",
    "first_five_day_average", "last_five_day_average", "first_vs_last_five_day_change_pct",
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
        advertiser_campaigns, role_trends = module.build_reports(
            [row("2026-06-01", "1", "Support Worker", "Alpha Care", "Leeds", "Yorkshire - West", ["support_worker"])],
            ["2026-06-01"],
            "2026-06",
        )

        self.assertEqual(list(advertiser_campaigns[0]), ADVERTISER_COLUMNS)
        self.assertEqual(list(role_trends[0]), ROLE_COLUMNS)
        old_columns = {"region", "region_scope", "category", "total_jobs", "feed_days", "days_seen", "top_titles"}
        self.assertTrue(old_columns.isdisjoint(advertiser_campaigns[0]))
        self.assertTrue(old_columns.isdisjoint(role_trends[0]))

    def test_advertiser_totals_are_not_inflated_by_multi_slice_expansion_and_one_row_per_advertiser(self):
        rows = [
            row("2026-06-01", "1", "Support Worker", "Alpha Care", "Leeds", "Yorkshire - West", ["support_worker", "admin_service"]),
            row("2026-06-01", "2", "Support Worker", "Alpha Care", "Bradford", "Yorkshire - West", ["support_worker"]),
            row("2026-06-02", "3", "Finance Assistant", "Alpha Care", "Durham", "North East - County Durham & Darlington/Hartlepool", ["finance_accounts"]),
            row("2026-06-02", "4", "Picker", "Beta Logistics", "Leeds", "Yorkshire - West", ["warehouse_logistics"]),
        ]

        advertiser_campaigns, _ = module.build_reports(rows, ["2026-06-01", "2026-06-02"], "2026-06")
        by_advertiser = {campaign["advertiser"]: campaign for campaign in advertiser_campaigns}

        self.assertEqual(len(advertiser_campaigns), 2)
        self.assertEqual(by_advertiser["Alpha Care"]["total_adverts"], 3)
        self.assertEqual(by_advertiser["Alpha Care"]["days_active"], 2)
        self.assertEqual(by_advertiser["Alpha Care"]["peak_daily_adverts"], 2)
        self.assertEqual(count_sum(by_advertiser["Alpha Care"]["top_roles"]), 3)
        self.assertEqual(count_sum(by_advertiser["Alpha Care"]["top_regions"]), 3)

    def test_role_output_is_one_row_per_normalised_title_and_slice_with_unclassified(self):
        rows = [
            row("2026-06-01", "1", "Support Worker", "Alpha Care", "Leeds", "Yorkshire - West", ["support_worker", "admin_service"]),
            row("2026-06-02", "2", "Support Worker", "Beta Care", "Bradford", "Yorkshire - West", ["support_worker"]),
            row("2026-06-02", "3", "Mystery Role", "Beta Care", "Durham", "North East", ["unclassified"]),
            row("2026-06-03", "4", "Mystery Role", "Gamma Care", "Durham", "North East", ["unclassified"]),
        ]

        _, role_trends = module.build_reports(rows, ["2026-06-01", "2026-06-02", "2026-06-03"], "2026-06")
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

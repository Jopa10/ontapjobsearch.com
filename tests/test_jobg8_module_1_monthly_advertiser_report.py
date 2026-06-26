import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

import csv

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "pipeline" / "scripts" / "jobg8_module_1_monthly_advertiser_report.py"
spec = importlib.util.spec_from_file_location("jobg8_module_1_monthly_advertiser_report", SCRIPT)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class Module1AdvertiserReportTests(unittest.TestCase):
    def test_role_trends_only_include_top_advertiser_share_concentration_metric(self):
        rows = [
            {
                "month_date": "2026-06-01",
                "job_id": "1",
                "title": "Support Worker",
                "title_key": "support worker",
                "advertiser": "Alpha Care",
                "advertiser_type": "Direct",
                "location": "Leeds",
                "raw_location": "Leeds",
                "lookup_region": "Yorkshire - West",
                "source_file": "2026-06-01.xlsx",
                "category": "support_worker",
            },
            {
                "month_date": "2026-06-01",
                "job_id": "2",
                "title": "Support Worker",
                "title_key": "support worker",
                "advertiser": "Alpha Care",
                "advertiser_type": "Direct",
                "location": "Leeds",
                "raw_location": "Leeds",
                "lookup_region": "Yorkshire - West",
                "source_file": "2026-06-01.xlsx",
                "category": "support_worker",
            },
            {
                "month_date": "2026-06-02",
                "job_id": "3",
                "title": "Support Worker",
                "title_key": "support worker",
                "advertiser": "Beta Care",
                "advertiser_type": "Agency",
                "location": "Bradford",
                "raw_location": "Bradford",
                "lookup_region": "Yorkshire - West",
                "source_file": "2026-06-02.xlsx",
                "category": "support_worker",
            },
        ]

        advertiser_campaigns, role_trends = module.build_reports(rows, ["2026-06-01", "2026-06-02"], "2026-06")

        self.assertIn("top_advertiser_share_pct", role_trends[0].keys())
        self.assertNotIn("advertiser_concentration_top_2_pct", role_trends[0].keys())
        self.assertNotIn("advertiser_concentration_hhi", role_trends[0].keys())
        self.assertEqual(float(role_trends[0]["top_advertiser_share_pct"]), 66.7)
        self.assertIn("advertiser", advertiser_campaigns[0].keys())

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

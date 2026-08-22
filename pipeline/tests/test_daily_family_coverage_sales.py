from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import assess_daily_family_coverage as coverage
from scripts import daily_family_coverage_history as history


class DailyFamilyCoverageSalesTests(unittest.TestCase):
    def test_apply_existing_populates_nonlive_rolling_metrics_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            register = root / "region_category_slice_register.csv"
            overview = root / "daily-region-overview.md"
            history_path = root / "daily-family-coverage-history.json"

            register.write_text(
                "region,category,status\n"
                "London,customer_sales,LIVE\n"
                "Yorkshire - North,customer_sales,NOT LIVE\n"
                "Cumbria - North,customer_sales,NOT LIVE\n",
                encoding="utf-8",
            )
            overview.write_text(
                "# Ontap daily regional overview\n\n"
                "> LIVE Service Admin and Support Worker counts reconcile to `today.csv` on `main`. NOT LIVE old wording.\n\n"
                "## NOT LIVE\n\n"
                "| Region | Service admin | Support worker | Sales advisor |\n"
                "|---|---:|---:|---:|\n"
                "| Cumbria - North | 3 | 6 | — |\n"
                "| London |  |  |  |\n"
                "| Yorkshire - North |  | 5 | — |\n\n"
                "## HEADLINE\n",
                encoding="utf-8",
            )
            history_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "window_days": 14,
                        "threshold": 6,
                        "snapshots": [
                            {
                                "feed_date": "2026-08-21",
                                "counts": {
                                    "Cumbria - North": {
                                        "service_admin": 1,
                                        "support_worker": 4,
                                        "customer_sales": 3,
                                    },
                                    "London": {
                                        "service_admin": 90,
                                        "support_worker": 8,
                                        "customer_sales": 18,
                                    },
                                    "Yorkshire - North": {
                                        "service_admin": 6,
                                        "support_worker": 7,
                                        "customer_sales": 6,
                                    },
                                },
                            },
                            {
                                "feed_date": "2026-08-22",
                                "counts": {
                                    "Cumbria - North": {
                                        "service_admin": 3,
                                        "support_worker": 6,
                                        "customer_sales": 2,
                                    },
                                    "London": {
                                        "service_admin": 100,
                                        "support_worker": 10,
                                        "customer_sales": 20,
                                    },
                                    "Yorkshire - North": {
                                        "service_admin": 4,
                                        "support_worker": 5,
                                        "customer_sales": 8,
                                    },
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            admin = {"Cumbria - North": 3, "London": 100, "Yorkshire - North": 4}
            support = {"Cumbria - North": 6, "London": 10, "Yorkshire - North": 5}
            sales = {"Cumbria - North": 2, "London": 20, "Yorkshire - North": 8}

            with mock.patch.object(coverage, "REGISTER_PATH", register), mock.patch.object(
                coverage, "OVERVIEW_PATH", overview
            ), mock.patch.object(history, "HISTORY_PATH", history_path):
                # load_history's default parameter is bound at definition time, so
                # route the call explicitly through the test path.
                with mock.patch.object(
                    coverage.coverage_history,
                    "load_history",
                    side_effect=lambda: history.load_history(history_path),
                ):
                    coverage._apply_to_overview("2026-08-22", admin, support, sales)

            text = overview.read_text(encoding="utf-8")
            self.assertIn("| Cumbria - North | 3 / 2.0 / 0/2 | 6 / 5.0 / 1/2 | 2 / 2.5 / 0/2 |", text)
            self.assertIn("| Yorkshire - North | 4 / 5.0 / 1/2 | 5 / 6.0 / 1/2 | 8 / 7.0 / 2/2 |", text)
            self.assertIn("| London | 100 / 95.0 / 2/2 | 10 / 9.0 / 2/2 |  |", text)
            self.assertIn("today / 14d avg / 6+ days", text)
            self.assertIn("Sales diagnostic counts are evidence only", text)
            self.assertNotIn("NOT LIVE Sales Advisor remains `—`", text)

    def test_history_replaces_same_date_and_retains_latest_14_dates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "history.json"
            regions = {"Region": {"slug": "region"}}

            for day in range(1, 16):
                feed_date = f"2026-08-{day:02d}"
                history.record_snapshot(
                    feed_date,
                    regions,
                    {"Region": day},
                    {"Region": day + 1},
                    {"Region": day + 2},
                    path=path,
                )

            saved = history.load_history(path)
            self.assertEqual(len(saved["snapshots"]), 14)
            self.assertEqual(saved["snapshots"][0]["feed_date"], "2026-08-02")
            self.assertEqual(saved["snapshots"][-1]["feed_date"], "2026-08-15")

            history.record_snapshot(
                "2026-08-15",
                regions,
                {"Region": 99},
                {"Region": 98},
                {"Region": 97},
                path=path,
            )
            saved = history.load_history(path)
            self.assertEqual(len(saved["snapshots"]), 14)
            self.assertEqual(saved["snapshots"][-1]["counts"]["Region"]["service_admin"], 99)

    def test_legacy_two_family_coverage_is_readable_until_next_full_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = root / "job_slice_catalog.json"
            report = root / "daily-family-coverage.csv"
            regions = {f"Region {index}": {"slug": f"region-{index}"} for index in range(33)}
            catalog.write_text(json.dumps({"regions": regions}), encoding="utf-8")

            with report.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["feed_date", "region", "family", "selected_count"],
                    lineterminator="\n",
                )
                writer.writeheader()
                for region in regions:
                    writer.writerow({
                        "feed_date": "2026-08-22",
                        "region": region,
                        "family": "service_admin",
                        "selected_count": 1,
                    })
                    writer.writerow({
                        "feed_date": "2026-08-22",
                        "region": region,
                        "family": "support_worker",
                        "selected_count": 2,
                    })

            with mock.patch.object(coverage, "CATALOG_PATH", catalog), mock.patch.object(
                coverage, "OUTPUT_PATH", report
            ):
                feed_date, admin, support, sales = coverage._load_coverage_csv()

            self.assertEqual(feed_date, "2026-08-22")
            self.assertEqual(len(admin), 33)
            self.assertEqual(len(support), 33)
            self.assertEqual(sales, {})


if __name__ == "__main__":
    unittest.main()

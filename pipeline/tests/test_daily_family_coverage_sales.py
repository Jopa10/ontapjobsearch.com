from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import assess_daily_family_coverage as coverage


class DailyFamilyCoverageSalesTests(unittest.TestCase):
    def test_apply_existing_populates_nonlive_sales_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            register = root / "region_category_slice_register.csv"
            overview = root / "daily-region-overview.md"

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

            admin = {"Cumbria - North": 3, "London": 100, "Yorkshire - North": 4}
            support = {"Cumbria - North": 6, "London": 10, "Yorkshire - North": 5}
            sales = {"Cumbria - North": 2, "London": 20, "Yorkshire - North": 8}

            with mock.patch.object(coverage, "REGISTER_PATH", register), mock.patch.object(
                coverage, "OVERVIEW_PATH", overview
            ):
                coverage._apply_to_overview("2026-08-22", admin, support, sales)

            text = overview.read_text(encoding="utf-8")
            self.assertIn("| Cumbria - North | 3 | 6 | 2 |", text)
            self.assertIn("| Yorkshire - North | 4 | 5 | 8 |", text)
            self.assertIn("| London | 100 | 10 |  |", text)
            self.assertIn("Sales diagnostic counts are evidence only", text)
            self.assertNotIn("NOT LIVE Sales Advisor remains `—`", text)


if __name__ == "__main__":
    unittest.main()

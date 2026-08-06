from __future__ import annotations

import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGION = "West Midlands - Coventry & Warwickshire"
ROUTE = "coventry-warwickshire/service-administrator-jobs"


class CoventryWarwickshireSliceTests(unittest.TestCase):
    def test_slice_is_live_in_register(self) -> None:
        register = ROOT / "pipeline" / "registers" / "region_category_slice_register.csv"
        with register.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

        self.assertIn(
            {"region": REGION, "category": "admin_service", "status": "LIVE"},
            rows,
        )

    def test_pipeline_and_publish_wrappers_include_slice(self) -> None:
        pipeline_wrapper = (
            ROOT / "pipeline" / "scripts" / "service_admin_pipeline_coventry.py"
        ).read_text(encoding="utf-8")
        publish_wrapper = (
            ROOT / "pipeline" / "scripts" / "publish_verified_pages_coventry.py"
        ).read_text(encoding="utf-8")

        self.assertIn(REGION, pipeline_wrapper)
        self.assertIn("coventry-warwickshire-admin-service.json", pipeline_wrapper)
        self.assertIn(REGION, publish_wrapper)
        self.assertIn("app/coventry-warwickshire/service-administrator-jobs.json", publish_wrapper)

    def test_live_page_is_discoverable(self) -> None:
        page = ROOT / "app" / ROUTE / "page.tsx"
        self.assertTrue(page.is_file())
        self.assertTrue(
            (ROOT / "app" / "coventry-warwickshire" / "service-administrator-jobs.json").is_file()
        )
        self.assertTrue(
            (
                ROOT
                / "pipeline"
                / "output-admin-service"
                / "coventry-warwickshire-admin-service.json"
            ).is_file()
        )

        for surface in (
            ROOT / "app" / "browse-jobs" / "page.tsx",
            ROOT / "app" / "sitemap.ts",
        ):
            self.assertIn(ROUTE, surface.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

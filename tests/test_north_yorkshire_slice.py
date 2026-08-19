from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "pipeline" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from pipeline.scripts import service_admin_pipeline_north_yorkshire as north_yorkshire


class NorthYorkshireSliceTests(unittest.TestCase):
    def test_pipeline_configuration(self) -> None:
        core = north_yorkshire.live.live.core
        self.assertEqual(
            "north-yorkshire-admin-service.json",
            core.OUTPUT_FILES["Yorkshire - North"],
        )
        self.assertEqual(6, core.PUBLISH_THRESHOLDS["Yorkshire - North"])
        self.assertEqual(
            "Yorkshire - North",
            core.REGION_MAP["north yorkshire"],
        )

    def test_anchor_town(self) -> None:
        workbook = ROOT / "pipeline" / "geo" / "geo_lookup.xlsx"
        anchors = north_yorkshire.load_anchor_towns(workbook, "admin_service")
        self.assertEqual("York", anchors["Yorkshire - North"])

    def test_live_register_and_discovery(self) -> None:
        register = (
            ROOT / "pipeline" / "registers" / "region_category_slice_register.csv"
        ).read_text(encoding="utf-8")
        self.assertIn("Yorkshire - North,admin_service,LIVE", register)

        route = "north-yorkshire/service-administrator-jobs"
        for surface in (
            ROOT / "app" / "browse-jobs" / "page.tsx",
            ROOT / "app" / "sitemap.ts",
        ):
            with self.subTest(surface=surface):
                self.assertIn(route, surface.read_text(encoding="utf-8"))

        page = ROOT / "app" / route / "page.tsx"
        page_source = page.read_text(encoding="utf-8")
        self.assertIn('anchorTown="York"', page_source)
        self.assertNotIn("robots: { index: false, follow: false }", page_source)

    def test_workflow_entrypoints(self) -> None:
        daily = (
            ROOT / ".github" / "workflows" / "run-full-jobg8-daily-process.yml"
        ).read_text(encoding="utf-8")
        publish = (
            ROOT / ".github" / "workflows" / "publish-verified-pages.yml"
        ).read_text(encoding="utf-8")

        self.assertIn("service_admin_pipeline_north_yorkshire", daily)
        self.assertIn("support_worker_pipeline_live_config", daily)
        self.assertIn("publish_verified_pages_north_yorkshire", publish)
        self.assertIn("app/north-yorkshire/service-administrator-jobs.json", publish)


if __name__ == "__main__":
    unittest.main()

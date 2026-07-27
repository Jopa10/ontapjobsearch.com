from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "pipeline" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import service_admin_pipeline as admin  # noqa: E402
import support_worker_pipeline as support  # noqa: E402


class CandidateSliceScaffoldTests(unittest.TestCase):
    def test_compilers_emit_all_three_candidate_outputs(self) -> None:
        self.assertEqual("hampshire-support-worker.json", support.OUTPUT_FILES["Hampshire"])
        self.assertEqual("surrey-admin-service.json", admin.OUTPUT_FILES["Surrey"])
        self.assertEqual("kent-admin-service.json", admin.OUTPUT_FILES["Kent"])

    def test_authoritative_anchor_towns_cover_new_candidates(self) -> None:
        workbook = ROOT / "pipeline" / "geo" / "geo_lookup.xlsx"
        admin_anchors = admin.load_anchor_towns(workbook, "admin_service")
        support_anchors = support.load_anchor_towns(workbook, "support_worker")

        self.assertEqual("Southampton", support_anchors["Hampshire"])
        self.assertEqual("Guildford", admin_anchors["Surrey"])
        self.assertEqual("Maidstone", admin_anchors["Kent"])

    def test_candidate_pages_are_hidden_from_live_discovery(self) -> None:
        candidate_routes = (
            "hampshire/support-worker",
            "surrey/service-administrator-jobs",
            "kent/service-administrator-jobs",
        )
        live_surfaces = (
            ROOT / "app" / "page.tsx",
            ROOT / "app" / "browse-jobs" / "page.tsx",
            ROOT / "app" / "sitemap.ts",
        )

        for surface in live_surfaces:
            content = surface.read_text(encoding="utf-8")
            for route in candidate_routes:
                with self.subTest(surface=surface, route=route):
                    self.assertNotIn(route, content)

        for route in candidate_routes:
            page = ROOT / "app" / route / "page.tsx"
            content = page.read_text(encoding="utf-8")
            with self.subTest(page=page):
                self.assertIn("robots: { index: false, follow: false }", content)


if __name__ == "__main__":
    unittest.main()

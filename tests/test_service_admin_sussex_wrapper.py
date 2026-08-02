import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

PIPELINE_DIR = Path(__file__).resolve().parents[1] / "pipeline"
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

from scripts import service_admin_pipeline_sussex as sussex


class SussexServiceAdminWrapperTests(unittest.TestCase):
    def test_sussex_output_configuration_is_enabled(self):
        self.assertEqual(sussex.core.REGION_MAP["sussex"], "Sussex")
        self.assertEqual(
            sussex.core.OUTPUT_FILES["Sussex"],
            "sussex-admin-service.json",
        )
        self.assertEqual(sussex.core.PUBLISH_THRESHOLDS["Sussex"], 6)

    def test_sussex_anchor_is_added_without_weakening_existing_validation(self):
        with mock.patch.object(
            sussex,
            "_ORIGINAL_LOAD_ANCHOR_TOWNS",
            return_value={"Hampshire": "Southampton"},
        ):
            anchors = sussex.load_anchor_towns(Path("unused.xlsx"), "admin_service")

        self.assertEqual(anchors["Sussex"], "Brighton")
        self.assertEqual(anchors["Hampshire"], "Southampton")
        self.assertEqual(
            sussex.core.OUTPUT_FILES["Sussex"],
            "sussex-admin-service.json",
        )

    def test_sussex_review_sections_are_generated(self):
        rows = [
            {
                "region": "Sussex",
                "selection_status": "SELECTED",
                "job_id": "sussex-1",
                "town": "Brighton",
                "salary_text": "£25,000",
                "title": "Administrator",
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "review.md"
            sussex.core.CURRENT_FEED_DATE = "2026-08-02"
            sussex.write_manual_review_markdown(path, rows)
            content = path.read_text(encoding="utf-8")

        self.assertIn("## SUSSEX — SELECTED", content)
        self.assertIn("sussex-1", content)


if __name__ == "__main__":
    unittest.main()

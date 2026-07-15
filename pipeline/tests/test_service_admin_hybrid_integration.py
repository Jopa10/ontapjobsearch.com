from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.scripts import service_admin_pipeline as core  # noqa: E402
from pipeline.scripts import service_admin_pipeline_education as integrated  # noqa: E402

SCRIPTS_DIR = REPO_ROOT / "pipeline" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from publish_verified_pages import Mapping, publish_one  # noqa: E402


class ServiceAdminHybridIntegrationTests(unittest.TestCase):
    def make_frame(self, description: str) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    core.COL["job_id"]: "hybrid-test-1",
                    core.COL["title"]: "Administrative Assistant",
                    core.COL["advertiser_name"]: "Example Employer",
                    core.COL["advertiser_type"]: "Direct Employer",
                    core.COL["employment_type"]: "Permanent",
                    core.COL["area"]: "Leeds",
                    core.COL["location"]: "Leeds",
                    core.COL["apply_url"]: "https://example.test/apply",
                    core.COL["description"]: description,
                    core.COL["salary_min"]: "25000",
                    core.COL["salary_max"]: "28000",
                    core.COL["salary_period"]: "Year",
                    core.COL["salary_additional"]: "£25,000 to £28,000 per year",
                }
            ]
        )

    def run_process(self, description: str):
        return integrated.process(
            self.make_frame(description),
            {"leeds": "Yorkshire - West"},
            {},
            {},
            set(),
            {},
        )

    def test_eligible_json_record_contains_hybrid_fields(self) -> None:
        outputs, report_rows = self.run_process(
            "Hybrid working with three days in the office and two days from home."
        )
        item = outputs["Yorkshire - West"][0]
        cleaned = core.clean_for_json(item)

        self.assertEqual("hybrid", cleaned["working_arrangement"])
        self.assertEqual(
            "2 days from home / 3 days in office",
            cleaned["working_arrangement_text"],
        )
        self.assertIn("hybrid", cleaned["working_arrangement_evidence"].casefold())
        self.assertEqual(cleaned, json.loads(json.dumps(cleaned)))

        included = next(row for row in report_rows if row["decision"] == "INCLUDED")
        self.assertEqual("hybrid", included["working_arrangement"])
        self.assertIn("working_arrangement", integrated.decision_report_fieldnames())
        self.assertIn("working_arrangement_evidence", core.MANUAL_REVIEW_FIELDNAMES)

    def test_non_hybrid_eligible_record_keeps_explicit_non_badge_value(self) -> None:
        outputs, report_rows = self.run_process(
            "This office-based administration role supports a remote team."
        )
        item = outputs["Yorkshire - West"][0]
        self.assertEqual("onsite_or_not_stated", item["working_arrangement"])
        self.assertEqual("", item["working_arrangement_text"])
        self.assertEqual("", item["working_arrangement_evidence"])

        included = next(row for row in report_rows if row["decision"] == "INCLUDED")
        self.assertEqual("onsite_or_not_stated", included["working_arrangement"])

    def test_verified_publish_preserves_working_arrangement_fields(self) -> None:
        source_row = {
            "job_id": "publish-hybrid-1",
            "title": "Administrative Assistant",
            "apply_url": "https://example.test/apply",
            "working_arrangement": "hybrid",
            "working_arrangement_text": "2 days from home",
            "working_arrangement_evidence": "Hybrid working with two days from home.",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "pipeline" / "output-admin-service" / "test.json"
            destination = root / "app" / "test" / "jobs.json"
            source.parent.mkdir(parents=True)
            destination.parent.mkdir(parents=True)
            source.write_text(json.dumps([source_row]), encoding="utf-8")
            destination.write_text("[]", encoding="utf-8")

            mapping = Mapping(
                "Test admin jobs",
                "Test Region",
                "admin_service",
                Path("pipeline/output-admin-service/test.json"),
                Path("app/test/jobs.json"),
            )
            result = publish_one(
                mapping,
                write=True,
                active_slices={("Test Region", "admin_service")},
                root=root,
            )

            self.assertEqual("published", result["status"])
            published = json.loads(destination.read_text(encoding="utf-8"))[0]
            self.assertEqual("hybrid", published["working_arrangement"])
            self.assertEqual("2 days from home", published["working_arrangement_text"])
            self.assertIn("two days", published["working_arrangement_evidence"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

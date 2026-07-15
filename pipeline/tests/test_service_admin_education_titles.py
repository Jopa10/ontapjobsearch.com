from __future__ import annotations

import csv
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.scripts.service_admin_pipeline_education import (  # noqa: E402
    classify_title,
)
from pipeline.scripts.service_admin_pipeline import (  # noqa: E402
    normalise_title_for_register,
)

REGISTER_PATH = REPO_ROOT / "pipeline" / "registers" / "admin_service_title_classification_register.csv"


def load_register() -> dict[str, dict[str, str]]:
    with REGISTER_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = csv.DictReader(handle)
        return {
            normalise_title_for_register(row["title"]): {
                "classification": row["classification"],
                "review_status": row["review_status"],
                "reason": row["reason"],
            }
            for row in rows
            if row.get("title")
        }


class ServiceAdminEducationTitleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.title_register = load_register()

    def classification_for(self, title: str) -> str:
        classification, _reason, _priority, _review_status = classify_title(
            title,
            self.title_register,
        )
        return classification

    def test_school_office_admin_titles_are_eligible(self) -> None:
        eligible_titles = (
            "School Administrator",
            "Primary School Administrator",
            "School Reception Administrator",
            "School Receptionist Administrator",
            "School Office Manager",
        )
        for title in eligible_titles:
            with self.subTest(title=title):
                self.assertEqual("HIGH_CONFIDENCE", self.classification_for(title))

    def test_non_admin_education_titles_remain_excluded(self) -> None:
        excluded_titles = (
            "Teaching Assistant",
            "Learning Support Assistant",
            "Cover Supervisor",
        )
        for title in excluded_titles:
            with self.subTest(title=title):
                self.assertEqual("HARD_PASS", self.classification_for(title))

    def test_specialist_education_support_beats_admin_word(self) -> None:
        self.assertEqual(
            "HARD_PASS",
            self.classification_for("School Behaviour Support Administrator"),
        )

    def test_plain_office_manager_keeps_existing_register_rule(self) -> None:
        self.assertEqual("OUT_OF_SCOPE", self.classification_for("Office Manager"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

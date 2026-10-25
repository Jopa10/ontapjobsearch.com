from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

from scripts.derive_city_pages import (  # noqa: E402
    CityConfig,
    Rule,
    derive_rows,
)
from scripts.enforce_jobg8_accountant_exclusion import (  # noqa: E402
    enforce_exclusion,
)
from scripts.jobg8_title_policy import is_jobg8_accountant_title  # noqa: E402


def city_config() -> CityConfig:
    return CityConfig(
        city_key="test-city",
        display_name="Test City",
        category_label="admin jobs",
        parent_page=Path("app/test/service-administrator-jobs.json"),
        review_csv=Path("pipeline/reviews/city-pages/test.csv"),
        summary_md=Path("pipeline/reviews/city-pages/test.md"),
        output_json=Path("app/_city-pages/test/service-administrator-jobs.json"),
        route="/test/service-administrator-jobs",
        minimum_live_jobs=1,
        mode="review_only",
        include_rules=(Rule("test city", "Test City workplace"),),
        review_rules=(),
        exclude_rules=(),
        fallback_decision="review",
        fallback_reason="No rule matched",
        exact_localities=(),
        include_office_family_supplements=False,
    )


def job(job_id: str, title: str, source: str = "JobG8") -> dict[str, str]:
    return {
        "job_id": job_id,
        "title": title,
        "company": "Employer",
        "location": "Test City",
        "summary": "",
        "description": "",
        "apply_url": f"https://example.test/{job_id}",
        "source": source,
    }


class JobG8AccountantCityGuardTests(unittest.TestCase):
    def test_accountant_title_patterns_are_source_scoped(self) -> None:
        for title in (
            "Assistant Accountant",
            "Financial Accountant",
            "Management Accountant",
            "Accountant / Accounts Bookkeeper",
            "Accounts Senior",
            "Accounts Semi-Senior",
        ):
            self.assertTrue(
                is_jobg8_accountant_title(
                    {"source": "JobG8", "title": title}
                ),
                title,
            )

        self.assertFalse(
            is_jobg8_accountant_title(
                {"source": "NHS Jobs", "title": "Assistant Accountant"}
            )
        )
        self.assertFalse(
            is_jobg8_accountant_title(
                {"source": "JobG8", "title": "Accounts Assistant"}
            )
        )

    def test_city_page_hard_fail_cannot_be_overridden_by_manual_select(self) -> None:
        row = job("2164756", "Assistant Accountant")
        rows = derive_rows(
            [row], city_config(), prior_actions={"jobg8-2164756": "include"}
        )

        self.assertEqual(rows[0]["automatic_decision"], "exclude")
        self.assertEqual(rows[0]["decision"], "exclude")
        self.assertEqual(rows[0]["effective_decision"], "exclude")
        self.assertEqual(rows[0]["action"], "")
        self.assertEqual(rows[0]["matched_rule"], "jobg8_accountant_title")

    def test_publication_sweep_removes_only_jobg8_accountant_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            app_dir = Path(directory) / "app"
            app_dir.mkdir()
            page = app_dir / "jobs.json"
            page.write_text(
                json.dumps(
                    [
                        {"job_id": "1", "title": "Assistant Accountant", "source": "JobG8"},
                        {"job_id": "2", "title": "Assistant Accountant", "source": "NHS Jobs"},
                        {"job_id": "3", "title": "Accounts Assistant", "source": "JobG8"},
                    ]
                ),
                encoding="utf-8",
            )

            removed = enforce_exclusion(app_dir)

            self.assertEqual(removed, {str(page): 1})
            remaining = json.loads(page.read_text(encoding="utf-8"))
            self.assertEqual([row["job_id"] for row in remaining], ["2", "3"])
            self.assertEqual(enforce_exclusion(app_dir), {})


if __name__ == "__main__":
    unittest.main()

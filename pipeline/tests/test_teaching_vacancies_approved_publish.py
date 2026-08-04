from datetime import date, datetime
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

from external_sources import teaching_vacancies_etl as etl  # noqa: E402
from external_sources import teaching_vacancies_poc as poc  # noqa: E402
from external_sources.compose_west_yorkshire_admin import compose_rows  # noqa: E402
from external_sources.teaching_vacancies_approved import (  # noqa: E402
    approval_errors,
    approved_output_rows,
    vacancy_to_published_job,
)


def vacancy(
    source_job_id: str,
    *,
    closing_date: str = "2099-08-31T23:59:00+01:00",
    classification: str = "HC",
) -> poc.Vacancy:
    return poc.Vacancy(
        source_job_id=source_job_id,
        title="School Office Administrator",
        employer="Example School",
        location="Leeds, Yorkshire and the Humber, LS1 1AA",
        salary_text="£24,000 - £26,000 Annually (Actual)",
        posted_date="2026-08-01",
        closing_date=closing_date,
        employment_type="FULL_TIME",
        description_excerpt="Office-based school administration.",
        source_url=(
            "https://teaching-vacancies.service.gov.uk/jobs/"
            + source_job_id
        ),
        geography_status="IN_SCOPE",
        geography_reason="West Yorkshire place marker",
        classification=classification,
        classification_reason="Clear admin/service title",
        jobg8_check="NO_MATCH",
    )


def decisions(
    *reviewed_ids: str,
    selections: set[str] | None = None,
    exclusions: set[str] | None = None,
) -> poc.ManualDecisionState:
    return poc.ManualDecisionState(
        selections=selections or set(),
        exclusions=exclusions or set(),
        reviewed_ids=set(reviewed_ids),
        review_date="2026-08-04",
    )


class TeachingVacanciesApprovedPublishTests(unittest.TestCase):
    def test_approval_requires_exact_review_set_and_allows_blank_poss(self):
        rows = [vacancy("hc"), vacancy("poss", classification="POSS")]
        state = decisions("hc", "poss")
        state.review_fingerprint = poc.review_fingerprint(rows)

        self.assertEqual(
            [],
            approval_errors(
                rows,
                state,
                review_date="2026-08-04",
                failures=[],
            ),
        )

        incomplete = decisions("hc")
        incomplete.review_fingerprint = poc.review_fingerprint(rows)
        errors = approval_errors(
            rows,
            incomplete,
            review_date="2026-08-04",
            failures=["poss failed"],
        )
        self.assertTrue(any("new IDs: poss" in error for error in errors))
        self.assertTrue(any("detail page(s) failed" in error for error in errors))

    def test_blank_poss_is_not_published(self):
        rows = approved_output_rows(
            [vacancy("hc"), vacancy("poss", classification="POSS")],
            decisions("hc", "poss"),
            now=datetime.fromisoformat("2026-08-04T12:00:00+01:00"),
        )
        self.assertEqual(
            ["teaching-vacancies-hc"],
            [row["job_id"] for row in rows],
        )

    def test_expired_selected_vacancy_is_not_published(self):
        state = decisions("open", "closed", selections={"open", "closed"})
        rows = approved_output_rows(
            [
                vacancy("open", closing_date="2026-08-04T23:59:00+01:00"),
                vacancy("closed", closing_date="2026-08-04T09:00:00+01:00"),
            ],
            state,
            now=datetime.fromisoformat("2026-08-04T12:00:00+01:00"),
        )
        self.assertEqual(
            ["teaching-vacancies-open"],
            [row["job_id"] for row in rows],
        )

    def test_published_record_has_source_tracking_and_stable_id(self):
        row = vacancy_to_published_job(vacancy("school-office"))
        query = parse_qs(urlsplit(row["apply_url"]).query)

        self.assertEqual("teaching-vacancies-school-office", row["job_id"])
        self.assertEqual("Teaching Vacancies", row["source"])
        self.assertEqual("Yorkshire - West", row["region"])
        self.assertEqual("Leeds", row["location"])
        self.assertEqual("2026-08-01", row["posted_date"])
        self.assertEqual("2099-08-31", row["closing_date"])
        self.assertIn("complete duties, person specification", row["description"])
        self.assertEqual(["ontap"], query["utm_source"])
        self.assertEqual(["referral"], query["utm_medium"])
        self.assertEqual(
            ["teaching_vacancies_external"],
            query["utm_campaign"],
        )

    def test_composer_replaces_old_snapshot_and_preserves_jobg8(self):
        jobg8 = {
            "job_id": "jobg8-1",
            "title": "Office Administrator",
            "company": "Private Employer",
            "location": "Leeds",
            "source": "JobG8",
        }
        old = {
            **vacancy_to_published_job(vacancy("old")),
            "job_id": "teaching-vacancies-old",
        }
        new = vacancy_to_published_job(vacancy("new"))
        expired = vacancy_to_published_job(
            vacancy("expired", closing_date="2026-08-03")
        )

        composed, counts = compose_rows(
            [old, jobg8],
            [new, expired],
            today=date(2026, 8, 4),
        )

        self.assertEqual(
            ["teaching-vacancies-new", "jobg8-1"],
            [row["job_id"] for row in composed],
        )
        self.assertEqual(1, counts["teaching_vacancies"])
        self.assertEqual(1, counts["expired_teaching_vacancies_skipped"])

    def test_composer_gives_jobg8_priority_for_factual_duplicate(self):
        jobg8 = {
            "job_id": "jobg8-1",
            "title": "School Office Administrator",
            "company": "Example School",
            "location": "Leeds",
            "source": "JobG8",
        }
        external = vacancy_to_published_job(vacancy("duplicate"))

        composed, counts = compose_rows(
            [jobg8],
            [external],
            today=date(2026, 8, 4),
        )

        self.assertEqual([jobg8], composed)
        self.assertEqual(1, counts["duplicate_teaching_vacancies_skipped"])

    def test_composer_uses_exact_current_day_closing_time(self):
        external = vacancy_to_published_job(
            vacancy("early", closing_date="2026-08-04T09:00:00+01:00")
        )

        composed, counts = compose_rows(
            [],
            [external],
            today=date(2026, 8, 4),
            now=datetime.fromisoformat("2026-08-04T12:00:00+01:00"),
        )

        self.assertEqual([], composed)
        self.assertEqual(1, counts["expired_teaching_vacancies_skipped"])

    def test_discovery_requires_two_matching_sweeps(self):
        with patch.object(
            etl,
            "_BASE_LIVE_URLS",
            side_effect=[
                ["https://example/jobs/a"],
                ["https://example/jobs/a"],
            ],
        ):
            self.assertEqual(
                ["https://example/jobs/a"],
                etl.stable_live_urls(2),
            )

        with patch.object(
            etl,
            "_BASE_LIVE_URLS",
            side_effect=[
                ["https://example/jobs/a"],
                ["https://example/jobs/b"],
            ],
        ):
            with self.assertRaisesRegex(ValueError, "discovery was not stable"):
                etl.stable_live_urls(2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

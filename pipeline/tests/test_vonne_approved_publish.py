from datetime import date, datetime
from pathlib import Path
import sys
import unittest
from urllib.parse import parse_qs, urlsplit


PIPELINE_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

from external_sources.compose_northeast_admin import compose_rows  # noqa: E402
from external_sources.northeast_jobs_poc import ManualDecisionState  # noqa: E402
from external_sources.vonne_approved import (  # noqa: E402
    approval_errors,
    approved_output_rows,
    parse_vonne_deadline,
    vacancy_to_published_job,
)
from external_sources.vonne_poc import VonneVacancy, review_fingerprint  # noqa: E402


def vacancy(
    source_job_id: str,
    *,
    title: str = "Accreditation and Outreach Officer",
    employer: str = "Example Charity",
    location: str = "Tyne and Wear",
    based: str = "Newcastle",
    closing_date: str = "Friday, August 21, 2026 - 17:00",
    classification: str = "POSS",
) -> VonneVacancy:
    return VonneVacancy(
        source="VONNE",
        source_job_id=source_job_id,
        title=title,
        employer=employer,
        location=location,
        ontap_geography="North East - Tyneside, Wearside & Northumberland",
        contract_type="Fixed term",
        working_pattern="Part time",
        salary_text="£29,000 Per Annum",
        posted_date="",
        closing_date=closing_date,
        source_url=f"https://www.vonne.org.uk/vonne-jobs-details?cid={source_job_id}",
        screening_basis="borderline transferable title",
        detail_status="snapshot",
        classification=classification,
        classification_reason="manual review",
        duplicate_status="UNIQUE",
        role_type="Employment",
        based=based,
        hours="Part time",
        role_description="Officer",
        geography_status="CONFIRMED",
        geography_reason="based: exact area",
        nejobs_duplicate_status="UNIQUE",
    )


def decisions(
    rows: list[VonneVacancy],
    *,
    selections: set[str],
    exclusions: set[str] | None = None,
) -> ManualDecisionState:
    reviewable = {
        row.source_job_id
        for row in rows
        if row.classification != "HARD_PASS"
    }
    return ManualDecisionState(
        selections=set(selections),
        exclusions=set(exclusions or set()),
        reviewed_ids=reviewable,
        review_date="2026-08-03",
        review_fingerprint=review_fingerprint(rows),
        rerun_mode=True,
    )


def published(
    job_id: str,
    *,
    source: str,
    title: str,
    company: str,
    location: str,
    closing_date: str = "2026-08-31",
) -> dict[str, str]:
    return {
        "job_id": job_id,
        "title": title,
        "company": company,
        "location": location,
        "region": "North East",
        "description": "A sufficiently factual original description.",
        "apply_url": "https://example.com/apply",
        "source": source,
        "closing_date": closing_date,
    }


class VonneApprovedPublishTests(unittest.TestCase):
    def test_vonne_deadline_formats_are_parsed_without_guessing(self):
        exact = parse_vonne_deadline("Friday, August 21, 2026 - 17:00")
        date_only = parse_vonne_deadline("16 August 2026")

        self.assertEqual("2026-08-21T17:00:00+01:00", exact.isoformat())
        self.assertEqual("2026-08-16T23:59:59+01:00", date_only.isoformat())
        self.assertIsNone(parse_vonne_deadline("Closing soon"))

    def test_approval_requires_exact_fingerprint_and_explicit_decisions(self):
        rows = [vacancy("173252"), vacancy("173262")]
        complete = decisions(
            rows,
            selections={"173252"},
            exclusions={"173262"},
        )
        self.assertEqual(
            [],
            approval_errors(
                rows,
                complete,
                review_date="2026-08-03",
                failures=[],
            ),
        )

        incomplete = decisions(rows, selections={"173252"})
        incomplete.exclusions.clear()
        errors = approval_errors(
            rows,
            incomplete,
            review_date="2026-08-03",
            failures=["173262 failed"],
        )
        self.assertTrue(any("explicitly selected or excluded" in error for error in errors))
        self.assertTrue(any("detail page(s) failed" in error for error in errors))

        changed = [vacancy("173252", title="Changed title"), vacancy("173262")]
        errors = approval_errors(
            changed,
            complete,
            review_date="2026-08-03",
            failures=[],
        )
        self.assertTrue(any("fingerprint" in error for error in errors))

    def test_published_record_uses_facts_stable_id_and_referral_tracking(self):
        row = vacancy_to_published_job(vacancy("173252"))
        query = parse_qs(urlsplit(row["apply_url"]).query)

        self.assertEqual("vonne-173252", row["job_id"])
        self.assertEqual("VONNE", row["source"])
        self.assertEqual("Newcastle", row["location"])
        self.assertEqual("", row["posted_date"])
        self.assertEqual("2026-08-21", row["closing_date"])
        self.assertEqual("2026-08-21T17:00:00+01:00", row["closing_datetime"])
        self.assertIn("Use the original VONNE advert", row["description"])
        self.assertNotIn("full source description", row["description"].casefold())
        self.assertEqual(["ontap"], query["utm_source"])
        self.assertEqual(["referral"], query["utm_medium"])
        self.assertEqual(["vonne_external"], query["utm_campaign"])

    def test_approved_output_uses_explicit_selections_and_omits_closed_jobs(self):
        rows = [
            vacancy("selected"),
            vacancy("excluded"),
            vacancy("closed", closing_date="01 August 2026"),
        ]
        state = decisions(
            rows,
            selections={"selected", "closed"},
            exclusions={"excluded"},
        )
        output = approved_output_rows(
            rows,
            state,
            now=datetime.fromisoformat("2026-08-03T12:00:00+01:00"),
        )

        self.assertEqual(["vonne-selected"], [row["job_id"] for row in output])

    def test_composer_reattaches_both_sources_and_preserves_jobg8(self):
        jobg8 = published(
            "jobg8-1",
            source="JobG8",
            title="Office Administrator",
            company="Private Employer",
            location="Newcastle",
        )
        old_nejobs = published(
            "nejobs-old",
            source="NEJobs",
            title="Old Administrator",
            company="Old Council",
            location="Durham",
        )
        old_vonne = published(
            "vonne-old",
            source="VONNE",
            title="Old Coordinator",
            company="Old Charity",
            location="Newcastle",
        )
        new_nejobs = published(
            "nejobs-new",
            source="NEJobs",
            title="Administration Assistant",
            company="Council",
            location="Durham",
        )
        new_vonne = published(
            "vonne-new",
            source="VONNE",
            title="Outreach Officer",
            company="Charity",
            location="Newcastle",
        )

        composed, counts = compose_rows(
            [old_nejobs, old_vonne, jobg8],
            [new_nejobs],
            [new_vonne],
            today=date(2026, 8, 3),
        )

        self.assertEqual(
            ["nejobs-new", "vonne-new", "jobg8-1"],
            [row["job_id"] for row in composed],
        )
        self.assertEqual(1, counts["nejobs"])
        self.assertEqual(1, counts["vonne"])
        self.assertEqual(1, counts["jobg8_or_other"])

    def test_composer_prefers_jobg8_then_nejobs_over_vonne_duplicates(self):
        jobg8 = published(
            "jobg8-1",
            source="JobG8",
            title="Outreach Officer",
            company="Charity",
            location="Newcastle",
        )
        vonne_duplicate = published(
            "vonne-1",
            source="VONNE",
            title="Outreach Officer",
            company="Charity",
            location="Newcastle",
        )
        composed, counts = compose_rows(
            [jobg8],
            [],
            [vonne_duplicate],
            today=date(2026, 8, 3),
        )
        self.assertEqual([jobg8], composed)
        self.assertEqual(1, counts["duplicate_vonne_skipped"])

        nejobs = published(
            "nejobs-1",
            source="NEJobs",
            title="Family Coordinator",
            company="Children North East",
            location="Tyne and Wear",
        )
        vonne_same = published(
            "vonne-2",
            source="VONNE",
            title="Family Coordinator",
            company="Children North East",
            location="Tyne and Wear",
        )
        composed, counts = compose_rows(
            [],
            [nejobs],
            [vonne_same],
            today=date(2026, 8, 3),
        )
        self.assertEqual(["nejobs-1"], [row["job_id"] for row in composed])
        self.assertEqual(1, counts["duplicate_vonne_skipped"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

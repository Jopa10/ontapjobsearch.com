import csv
from pathlib import Path

import pytest

from external_sources.teaching_vacancies_etl import (
    parse_jobposting,
    validate_core_fields,
    visible_label_value,
)
from external_sources.teaching_vacancies_poc import (
    Vacancy,
    classify,
    discover_job_urls,
    empty_manual_decisions,
    final_decision_for,
    geography,
    load_manual_decisions_from_markdown,
    process,
    review_fingerprint,
    write_csv,
    write_summary,
)


def test_discover_job_urls_deduplicates_and_ignores_search_page():
    document = """
    <a href="/jobs">Jobs</a>
    <a href="/jobs/administrative-assistant-example">One</a>
    <a href="https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-example">Again</a>
    <a href="/jobs/exams-officer-example">Two</a>
    """
    assert discover_job_urls(document) == [
        "https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-example",
        "https://teaching-vacancies.service.gov.uk/jobs/exams-officer-example",
    ]


def test_parse_jobposting_json_ld():
    document = """<script type="application/ld+json">{
      "@context":"https://schema.org","@type":"JobPosting",
      "identifier":{"value":"TV-123"},"title":"Administrative Assistant",
      "hiringOrganization":{"name":"Example Academy"},
      "jobLocation":{"address":{"addressLocality":"Leeds","addressRegion":"West Yorkshire","postalCode":"LS1 1AA"}},
      "baseSalary":{"value":{"minValue":24000,"maxValue":26000,"unitText":"YEAR"}},
      "datePosted":"2026-08-01","validThrough":"2026-08-12",
      "employmentType":"FULL_TIME","description":"Provide administrative support and reception duties."
    }</script>"""
    vacancy = parse_jobposting(
        document,
        "https://teaching-vacancies.service.gov.uk/jobs/example",
    )
    assert vacancy.source_job_id == "TV-123"
    assert vacancy.title == "Administrative Assistant"
    assert vacancy.employer == "Example Academy"
    assert "Leeds" in vacancy.location
    assert vacancy.salary_text == "£24000–£26000 YEAR"
    assert vacancy.closing_date == "2026-08-12"


def test_visible_salary_fallback_when_json_ld_omits_base_salary():
    document = """
    <script type="application/ld+json">{
      "@context":"https://schema.org","@type":"JobPosting",
      "identifier":{"value":"TV-456"},"title":"Exams Officer",
      "hiringOrganization":{"name":"Newsome Academy"},
      "jobLocation":{"address":{"addressLocality":"Huddersfield","addressRegion":"West Yorkshire","postalCode":"HD4 6JN"}},
      "datePosted":"2026-07-14","validThrough":"2026-08-10T09:00:00+01:00",
      "employmentType":"FULL_TIME","description":"Administer examinations."
    }</script>
    <h3>Full time equivalent salary</h3>
    <div>£28,262.00 - £30,199.00 Annually (Actual) Scale 6, SCP 18-22 (FTE £31,537 - £33,699)</div>
    """
    vacancy = parse_jobposting(
        document,
        "https://teaching-vacancies.service.gov.uk/jobs/exams-officer-example",
    )
    assert vacancy.salary_text == (
        "£28,262.00 - £30,199.00 Annually (Actual) Scale 6, SCP 18-22 "
        "(FTE £31,537 - £33,699)"
    )


def test_visible_label_value_ignores_json_ld_and_scripts():
    document = """
    <script>Full time equivalent salary fake</script>
    <h3>Full time equivalent salary</h3>
    <p>£25,000 - £27,000</p>
    """
    assert visible_label_value(document, "Full time equivalent salary") == (
        "£25,000 - £27,000"
    )


def test_field_audit_blocks_in_scope_blank_salary():
    vacancy = Vacancy(
        source_job_id="missing-salary",
        title="Administrator",
        location="Leeds, West Yorkshire, LS1 1AA",
        geography_status="IN_SCOPE",
    )
    with pytest.raises(ValueError, match="field audit failed"):
        validate_core_fields([vacancy])


def test_geography_and_classification():
    vacancy = Vacancy(
        title="Administrative Assistant",
        employer="Example Academy",
        location="Leeds, West Yorkshire, LS1 1AA",
        description_excerpt="Reception and administrative support.",
    )
    vacancy.geography_status, vacancy.geography_reason = geography(vacancy)
    assert vacancy.geography_status == "IN_SCOPE"
    assert classify(vacancy)[0] == "HC"


def test_teacher_is_hard_pass():
    vacancy = Vacancy(
        title="Teacher of English",
        location="Bradford, West Yorkshire",
    )
    vacancy.geography_status, vacancy.geography_reason = geography(vacancy)
    assert classify(vacancy)[0] == "HARD_PASS"


def test_confirmed_jobg8_duplicate_is_hard_pass():
    vacancy = Vacancy(
        source_job_id="1",
        title="School Receptionist",
        employer="Example Academy",
        location="Wakefield, West Yorkshire, WF1 1AA",
        closing_date="2026-08-15",
        source_url="https://example.test/jobs/1",
    )
    jobg8 = [
        {
            "title": "School Receptionist",
            "advertiser_name": "Example Academy",
        }
    ]
    reviewed = process([vacancy], jobg8)
    assert reviewed[0].classification == "HARD_PASS"
    assert reviewed[0].classification_reason == "Confirmed JobG8 duplicate"


def test_review_csv_and_markdown_match_existing_external_source_format(
    tmp_path: Path,
):
    vacancies = process(
        [
            Vacancy(
                source_job_id="hc-1",
                title="Administrative Assistant",
                employer="A Academy",
                location="Leeds, West Yorkshire, LS1 1AA",
                salary_text="£25,000",
                closing_date="2026-08-20",
                source_url="https://example.test/hc-1",
            ),
            Vacancy(
                source_job_id="poss-1",
                title="Office Manager",
                employer="B Academy",
                location="Bradford, West Yorkshire, BD1 1AA",
                salary_text="£30,000",
                closing_date="2026-08-21",
                source_url="https://example.test/poss-1",
            ),
            Vacancy(
                source_job_id="hard-1",
                title="Teacher of English",
                employer="C Academy",
                location="Leeds, West Yorkshire, LS2 2AA",
                closing_date="2026-08-22",
                source_url="https://example.test/hard-1",
            ),
        ],
        [],
    )
    csv_path = tmp_path / "west-yorkshire-teaching-vacancies-review.csv"
    md_path = tmp_path / "west-yorkshire-teaching-vacancies-summary.md"
    decisions = empty_manual_decisions()

    write_csv(csv_path, vacancies, decisions)
    write_summary(
        md_path,
        vacancies,
        discovered=3,
        decisions=decisions,
        review_date="2026-08-04",
    )

    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        assert reader.fieldnames[0] == "final_decision"
    assert [row["final_decision"] for row in rows] == [
        "SELECTED",
        "POSS",
        "HARD_PASS",
    ]

    markdown = md_path.read_text(encoding="utf-8")
    assert markdown.startswith(
        "# Teaching Vacancies ETL proof-of-concept review\n\n"
        "review_date: 2026-08-04\n"
        "review_fingerprint: "
    )
    assert "Edit only the `action:` line in each editable block:" in markdown
    assert "## SELECTED" in markdown
    assert "action:\nSELECTED | West Yorkshire |" in markdown
    assert "## POSS — choose SELECT or EXCLUDE" in markdown
    assert "action:\nPOSS | West Yorkshire |" in markdown
    assert "## EXCLUDED BY REVIEW" in markdown
    assert "## HARD_PASS" in markdown
    assert "source_job_id: hc-1" in markdown


def test_same_day_action_edits_are_loaded_and_applied(tmp_path: Path):
    vacancies = process(
        [
            Vacancy(
                source_job_id="hc-1",
                title="Administrative Assistant",
                employer="A Academy",
                location="Leeds, West Yorkshire, LS1 1AA",
                source_url="https://example.test/hc-1",
            ),
            Vacancy(
                source_job_id="poss-1",
                title="Office Manager",
                employer="B Academy",
                location="Bradford, West Yorkshire, BD1 1AA",
                source_url="https://example.test/poss-1",
            ),
        ],
        [],
    )
    fingerprint = review_fingerprint(vacancies)
    summary = tmp_path / "summary.md"
    summary.write_text(
        f"""# Teaching Vacancies ETL proof-of-concept review

review_date: 2026-08-04
review_fingerprint: {fingerprint}

---
action: exclude
SELECTED | West Yorkshire | Leeds | £25,000 | Administrative Assistant
source_job_id: hc-1
---

---
action: select
POSS | West Yorkshire | Bradford | £30,000 | Office Manager
source_job_id: poss-1
---
""",
        encoding="utf-8",
    )
    decisions = load_manual_decisions_from_markdown(
        summary,
        "2026-08-04",
    )
    assert decisions.exclusions == {"hc-1"}
    assert decisions.selections == {"poss-1"}
    assert final_decision_for(vacancies[0], decisions) == "EXCLUDED"
    assert final_decision_for(vacancies[1], decisions) == "SELECTED"


def test_old_actions_are_ignored(tmp_path: Path):
    summary = tmp_path / "summary.md"
    summary.write_text(
        """review_date: 2026-08-03

---
action: select
source_job_id: poss-1
---
""",
        encoding="utf-8",
    )
    decisions = load_manual_decisions_from_markdown(
        summary,
        "2026-08-04",
    )
    assert not decisions.selections
    assert "old actions ignored" in decisions.load_warning

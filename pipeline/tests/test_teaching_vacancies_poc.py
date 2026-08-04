from pathlib import Path

from external_sources.teaching_vacancies_poc import (
    Vacancy,
    classify,
    discover_job_urls,
    geography,
    parse_jobposting,
    process,
    write_csv,
    write_summary,
)


def test_discover_job_urls_deduplicates_and_ignores_search_page():
    html = '''
    <a href="/jobs">Jobs</a>
    <a href="/jobs/administrative-assistant-example">One</a>
    <a href="https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-example">Again</a>
    <a href="/jobs/exams-officer-example">Two</a>
    '''
    urls = discover_job_urls(html)
    assert urls == [
        "https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-example",
        "https://teaching-vacancies.service.gov.uk/jobs/exams-officer-example",
    ]


def test_parse_jobposting_json_ld():
    document = '''<script type="application/ld+json">{
      "@context":"https://schema.org","@type":"JobPosting",
      "identifier":{"value":"TV-123"},"title":"Administrative Assistant",
      "hiringOrganization":{"name":"Example Academy"},
      "jobLocation":{"address":{"addressLocality":"Leeds","addressRegion":"West Yorkshire","postalCode":"LS1 1AA"}},
      "baseSalary":{"value":{"minValue":24000,"maxValue":26000,"unitText":"YEAR"}},
      "datePosted":"2026-08-01","validThrough":"2026-08-12",
      "employmentType":"FULL_TIME","description":"Provide administrative support and reception duties."
    }</script>'''
    vacancy = parse_jobposting(document, "https://teaching-vacancies.service.gov.uk/jobs/example")
    assert vacancy.source_job_id == "TV-123"
    assert vacancy.title == "Administrative Assistant"
    assert vacancy.employer == "Example Academy"
    assert "Leeds" in vacancy.location
    assert vacancy.closing_date == "2026-08-12"


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
    vacancy = Vacancy(title="Teacher of English", location="Bradford, West Yorkshire")
    vacancy.geography_status, vacancy.geography_reason = geography(vacancy)
    assert classify(vacancy)[0] == "HARD_PASS"


def test_process_flags_probable_duplicate_and_writes_review_outputs(tmp_path: Path):
    vacancy = Vacancy(
        source_job_id="1",
        title="School Receptionist",
        employer="Example Academy",
        location="Wakefield, West Yorkshire, WF1 1AA",
        closing_date="2026-08-15",
        source_url="https://example.test/jobs/1",
    )
    jobg8 = [{"title": "School Receptionist", "advertiser_name": "Example Academy"}]
    reviewed = process([vacancy], jobg8)
    assert reviewed[0].classification == "HC"
    assert reviewed[0].jobg8_check == "DUPLICATE"
    csv_path = tmp_path / "review.csv"
    md_path = tmp_path / "summary.md"
    write_csv(csv_path, reviewed)
    write_summary(md_path, reviewed, 1)
    assert csv_path.stat().st_size > 0
    assert "Review output only" in md_path.read_text(encoding="utf-8")

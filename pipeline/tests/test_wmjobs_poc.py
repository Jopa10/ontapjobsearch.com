from external_sources.wmjobs_poc import (
    WmjobsVacancy,
    build_parser,
    build_vacancies,
    classify,
    parse_rss,
)


def sample_rss() -> str:
    return """<?xml version="1.0" encoding="utf-8"?>
    <rss version="2.0"><channel>
      <item>
        <title>Smith's Wood Primary Academy: Administration Assistant</title>
        <link>https://www.wmjobs.co.uk/job/273822/administration-assistant/</link>
        <description><![CDATA[£26,824 - £29,540 pro rata per annum: Smith's Wood Primary Academy: We are seeking a proactive Administration Assistant in Smith's Wood, Birmingham.]]></description>
        <pubDate>Mon, 03 Aug 2026 23:00:00 +0000</pubDate>
      </item>
      <item>
        <title>Solihull Metropolitan Borough Council: Apprentice Admin Systems Support Officer</title>
        <link>https://www.wmjobs.co.uk/job/273815/apprentice-admin-systems-support-officer/</link>
        <description><![CDATA[National Living Wage: Solihull Metropolitan Borough Council: Join the Income and Awards team. Location flexible and hybrid.]]></description>
        <pubDate>Mon, 03 Aug 2026 23:00:00 +0000</pubDate>
      </item>
      <item>
        <title>Staffordshire County Council: Registration Officer</title>
        <link>https://www.wmjobs.co.uk/job/273816/registration-officer/</link>
        <description><![CDATA[£30,024 - £33,699: Staffordshire County Council: Public registration role at Newcastle Registration Office.]]></description>
        <pubDate>Mon, 03 Aug 2026 23:00:00 +0000</pubDate>
      </item>
    </channel></rss>"""


def test_parse_rss_extracts_factual_fields() -> None:
    items = parse_rss(sample_rss())
    assert len(items) == 3
    assert items[0].source_job_id == "273822"
    assert items[0].employer == "Smith's Wood Primary Academy"
    assert items[0].title == "Administration Assistant"
    assert items[0].salary_text.startswith("£26,824")
    assert items[0].location == "Birmingham"
    assert items[0].source_url.endswith("/administration-assistant/")


def test_build_vacancies_is_bounded_to_target_or_diagnostic_admin_rows() -> None:
    vacancies = build_vacancies(parse_rss(sample_rss()))
    by_title = {vacancy.title: vacancy for vacancy in vacancies}
    assert by_title["Administration Assistant"].classification == "HC"
    assert by_title["Apprentice Admin Systems Support Officer"].geography_status == "IN_SCOPE"
    assert by_title["Registration Officer"].classification == "HARD_PASS"
    assert "outside Birmingham" in by_title["Registration Officer"].classification_reason


def test_specialist_admin_can_be_reviewed() -> None:
    vacancy = WmjobsVacancy(
        source="WMJobs",
        source_job_id="1",
        title="Finance Administrator",
        employer="Example",
        location="Birmingham",
        ontap_geography="Birmingham & Solihull",
        contract_type="",
        working_pattern="",
        salary_text="£28,000",
        posted_date="",
        closing_date="",
        source_url="https://www.wmjobs.co.uk/job/1/example/",
        screening_basis="rss",
        detail_status="rss-only",
        description_excerpt="Specialist finance and payroll administration.",
        apply_url="https://www.wmjobs.co.uk/job/1/example/",
        geography_status="IN_SCOPE",
        geography_reason="Explicit Birmingham wording in RSS",
    )
    assert classify(vacancy)[0] == "POSS"


def test_cli_has_no_publish_or_approval_options() -> None:
    parser = build_parser()
    options = {
        option
        for action in parser._actions
        for option in action.option_strings
    }
    assert "--publish" not in options
    assert "--approved-json" not in options
    assert "--approval-confirmation" not in options

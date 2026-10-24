from argparse import Namespace
from pathlib import Path

from external_sources.bvsc_poc import (
    BvscVacancy,
    build_parser,
    classify,
    geography,
    parse_detail,
    parse_listing,
)


def test_listing_parser_extracts_article_summary() -> None:
    html = """
    <h2><a href="/vacancy-admin-assistant">Admin Assistant</a></h2>
    <p>Example Charity. Closing Date: Friday 28th August, 5pm. Read more</p>
    <p>Published: 1st August, 2026</p>
    <p>Location: Solihull, B91 1AA</p>
    """
    items = parse_listing(html)
    assert len(items) == 1
    assert items[0].title == "Admin Assistant"
    assert items[0].employer == "Example Charity"
    assert items[0].location == "Solihull, B91 1AA"
    assert "28th August" in items[0].closing_date


def test_detail_parser_extracts_fields_and_apply_link() -> None:
    item = parse_listing(
        '<h2><a href="/vacancy-project-assistant">Project Assistant</a></h2>'
        '<p>Example Charity. Closing Date: 31 August. Read more</p>'
        '<p>Location: Birmingham</p>'
    )[0]
    detail = parse_detail(
        """
        <h1>Project Assistant</h1>
        <p>Job Title: Project Assistant</p>
        <p>Salary: £25,000 per annum</p>
        <p>Location: Birmingham, B1 1AA</p>
        <p>Closing Date: 31 August 2026</p>
        <p>Provide administrative support, answer enquiries and maintain records.</p>
        <a href="https://example.org/apply">Apply now</a>
        """,
        item,
    )
    assert detail["salary_text"] == "£25,000 per annum"
    assert detail["location"] == "Birmingham, B1 1AA"
    assert detail["apply_url"] == "https://example.org/apply"
    assert "administrative support" in detail["description_excerpt"]


def test_geography_is_tightly_bounded() -> None:
    assert geography("Birmingham, B1 2AJ", "")[0] == "IN_SCOPE"
    assert geography("The Core, Solihull", "")[0] == "IN_SCOPE"
    assert geography("Gloucester", "")[0] == "HARD_PASS"
    assert geography("Hybrid, West Midlands", "")[0] == "POSS"


def make_vacancy(title: str, description: str = "") -> BvscVacancy:
    return BvscVacancy(
        source="BVSC",
        source_job_id="1",
        title=title,
        employer="Example Charity",
        location="Birmingham",
        ontap_geography="Birmingham & Solihull",
        contract_type="",
        working_pattern="",
        salary_text="£24,000",
        posted_date="",
        closing_date="31/08/2026",
        source_url="https://www.bvsc.org/vacancy-example",
        screening_basis="title+detail",
        detail_status="snapshot",
        description_excerpt=description,
        geography_status="IN_SCOPE",
        geography_reason="Explicit Birmingham location",
    )


def test_classification_reuses_admin_service_rules() -> None:
    assert classify(make_vacancy("Administrator"))[0] == "HC"
    assert classify(make_vacancy("Project Assistant"))[0] == "POSS"
    assert classify(make_vacancy("Chef / Cook"))[0] == "HARD_PASS"


def test_cli_has_no_publish_or_approval_option() -> None:
    parser = build_parser()
    option_strings = {
        option
        for action in parser._actions
        for option in action.option_strings
    }
    assert "--publish" not in option_strings
    assert "--approved-json" not in option_strings
    assert "--approval-confirmation" not in option_strings

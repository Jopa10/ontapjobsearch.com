from pathlib import Path
import sys


PIPELINE_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

from external_sources.northeast_jobs_poc import (  # noqa: E402
    FeedItem,
    REPORT_FIELDS,
    Vacancy,
    annual_salary_upper,
    classify,
    compact_review_text,
    deduplicate,
    deduplicate_within_source,
    employer_from_page_title,
    extract_job_id,
    infer_location_from_detail,
    parse_detail,
    parse_args,
    parse_rss_xml,
    review_closing_date,
    review_posted_date,
    review_row,
    screen_item,
    cluster_for_location,
)


def test_parse_rss_xml_extracts_factual_fields():
    xml = """<?xml version="1.0"?>
    <rss><channel><item>
      <title>Business Support Officer</title>
      <link>http://www.northeastjobs.org.uk/Default.aspx?page=jobdetail&amp;jid=300058</link>
      <description><![CDATA[
        General office support
        Contract Type: Permanent|Working Pattern: Full time|
        Salary: £25,000 - £27,000|Advert End Date: 17/08/2026 12:00|
      ]]></description>
      <pubDate>Tue, 28 Jul 2026 00:00:00 GMT</pubDate>
    </item></channel></rss>"""

    items = parse_rss_xml(xml)

    assert len(items) == 1
    assert items[0].source_job_id == "300058"
    assert items[0].contract_type == "Permanent"
    assert items[0].working_pattern == "Full time"
    assert items[0].salary_text == "£25,000 - £27,000"
    assert items[0].closing_date == "17/08/2026 12:00"


def test_screen_keeps_clear_office_role_and_rejects_clear_occupation():
    clear = FeedItem("1", "Receptionist & Administrator", "https://example/1")
    hard = FeedItem("2", "Teaching Assistant", "https://example/2")

    assert screen_item(clear)[0] == "HC_SCREEN"
    assert screen_item(hard)[0] == "HARD_PASS_SCREEN"


def test_rendered_detail_parser_keeps_only_factual_fields():
    item = FeedItem(
        "299953",
        "Receptionist & Administrator (HR / School)",
        "https://example/299953",
    )
    rendered = """Title: Receptionist & Administrator (HR / School) - Talbot House Children's Charity

Markdown Content:
##### Job Summary

Contract Type:

Permanent

Working Pattern:

Full time - term time

Advert Start Date:

21/07/2026

Advert End Date:

09/08/2026 23:59

Salary:

£21,547.50 per annum

Vacancy ID:

299953

Employment Location:

Newcastle upon Tyne

##### Further Information

This full description must not be retained in the standardised record.
"""

    detail = parse_detail(rendered, item)

    assert detail["employer"] == "Talbot House Children's Charity"
    assert detail["location"] == "Newcastle upon Tyne"
    assert detail["vacancy_id"] == "299953"
    assert "description" not in detail


def test_title_and_job_id_helpers():
    assert (
        employer_from_page_title(
            "Business Coordinator - Blue Sky Trust",
            "Business Coordinator",
        )
        == "Blue Sky Trust"
    )
    assert extract_job_id("https://example.test/job/Test/300001") == "300001"


def test_possible_duplicate_stays_in_manual_review():
    vacancy = Vacancy(
        source="North East Jobs",
        source_job_id="300001",
        title="Business Support Officer",
        employer="Example Council",
        location="Durham",
        ontap_geography="North East - County Durham & Darlington/Hartlepool",
        contract_type="Permanent",
        working_pattern="Full time",
        salary_text="£25,000",
        posted_date="",
        closing_date="",
        source_url="https://example.test/300001",
        screening_basis="clear title",
        detail_status="snapshot",
        duplicate_status="POSSIBLE_DUPLICATE",
    )

    classify(vacancy, 30_000)

    assert vacancy.classification == "POSS"
    assert "possible JobG8 duplicate" in vacancy.classification_reason


def test_salary_parser_reads_range_with_one_currency_symbol():
    assert annual_salary_upper("Grade 5 £28598 -31022") == 31022


def test_receptionist_with_secondary_hr_wording_remains_clear():
    vacancy = Vacancy(
        source="North East Jobs",
        source_job_id="299953",
        title="Receptionist & Administrator (HR / School)",
        employer="Talbot House Children's Charity",
        location="Newcastle upon Tyne",
        ontap_geography="North East - Tyneside, Wearside & Northumberland",
        contract_type="Permanent",
        working_pattern="Full time - term time",
        salary_text="£21,547.50 per annum",
        posted_date="",
        closing_date="",
        source_url="https://example.test/299953",
        screening_basis="clear title",
        detail_status="snapshot",
        duplicate_status="UNIQUE",
    )

    classify(vacancy, 30_000)

    assert vacancy.classification == "HC"


def test_employer_can_supply_geo_when_detail_page_omits_location():
    area_map = {
        "south tyneside": "North East - Tyneside, Wearside & Northumberland"
    }
    cluster, reason = cluster_for_location(
        "South Tyneside Council",
        area_map,
        {},
    )

    assert cluster == "North East - Tyneside, Wearside & Northumberland"
    assert "area found in address" in reason


def test_identical_source_rows_are_flagged_not_silently_removed():
    shared = dict(
        source="North East Jobs",
        title="PMO Support Officer",
        employer="Gateshead Council",
        location="Gateshead",
        ontap_geography="North East - Tyneside, Wearside & Northumberland",
        contract_type="Permanent",
        working_pattern="Full time",
        salary_text="£39,152 - £41,771",
        posted_date="17/07/2026",
        closing_date="02/08/2026",
        screening_basis="provisional review",
        detail_status="snapshot",
        duplicate_status="UNIQUE",
    )
    vacancies = [
        Vacancy(source_job_id="299841", source_url="https://example/299841", **shared),
        Vacancy(source_job_id="299843", source_url="https://example/299843", **shared),
    ]

    deduplicate_within_source(vacancies)
    classify(vacancies[0], 30_000)

    assert vacancies[0].source_duplicate_status == "POSSIBLE_SOURCE_DUPLICATE"
    assert vacancies[0].classification == "POSS"


def test_detail_text_fallback_uses_specific_area_phrase():
    area_map = {
        "north tyneside": "North East - Tyneside, Wearside & Northumberland",
        "south tyneside": "North East - Tyneside, Wearside & Northumberland",
    }
    text = (
        "We have roles in various school settings within the North Tyneside area. "
        "Our network also covers South Tyneside."
    )

    location, cluster, reason = infer_location_from_detail(text, area_map, {})

    assert location == "North Tyneside"
    assert cluster == "North East - Tyneside, Wearside & Northumberland"
    assert "specific detail-page phrase" in reason


def test_detail_text_fallback_refuses_multiple_clusters():
    area_map = {
        "alnwick": "North East - Tyneside, Wearside & Northumberland",
        "harrogate": "Yorkshire - North Yorkshire",
    }

    location, cluster, reason = infer_location_from_detail(
        "Links: school-alnwick.example and regional-harrogate.example",
        area_map,
        {},
    )

    assert location == ""
    assert cluster == ""
    assert "multiple Ontap geographies" in reason


def test_dedupe_does_not_confuse_school_and_sales_administrators():
    vacancy = Vacancy(
        source="North East Jobs",
        source_job_id="256127",
        title="School Administrator",
        employer="First Class Supply & Training",
        location="County Durham",
        ontap_geography="North East - County Durham & Darlington/Hartlepool",
        contract_type="Temporary",
        working_pattern="Full time",
        salary_text="£15.20 per hour",
        posted_date="",
        closing_date="",
        source_url="https://example.test/256127",
        screening_basis="clear title",
        detail_status="snapshot",
    )
    jobg8 = [{
        "job_id": "jobg8-1",
        "title": "Sales Administrator",
        "employer": "Example Recruitment",
        "area": "County Durham",
        "location": "Durham",
        "description": "A sales support role for a private employer.",
        "cluster": "North East - County Durham & Darlington/Hartlepool",
    }]

    deduplicate(vacancy, jobg8)

    assert vacancy.duplicate_status == "UNIQUE"


def test_review_sheet_starts_with_requested_nejobs_fields():
    assert REPORT_FIELDS[:6] == [
        "title",
        "salary_text",
        "employer",
        "location",
        "posted_date",
        "closing_date",
    ]


def test_review_sheet_hides_implausible_jobg8_candidate():
    vacancy = Vacancy(
        source="North East Jobs",
        source_job_id="299480",
        title="Administration Assistant",
        employer="Durham County Council",
        location="Meadowfield",
        ontap_geography="North East - County Durham & Darlington/Hartlepool",
        contract_type="Permanent",
        working_pattern="Full time",
        salary_text="£25,583",
        posted_date="10/07/2026",
        closing_date="09/08/2026 23:59",
        source_url="https://example.test/299480",
        screening_basis="clear title",
        detail_status="snapshot",
        classification="HC",
        duplicate_status="UNIQUE",
        jobg8_candidate_title="Optical Assistant",
        jobg8_candidate_advertiser="ASDA Opticians",
        jobg8_match_score="0.490",
    )

    row = review_row(vacancy)

    assert row["closing_date"] == "09/08/2026"
    assert row["jobg8_check"] == "No plausible JobG8 match"
    assert row["jobg8_candidate_title"] == ""
    assert row["jobg8_candidate_employer"] == ""
    assert row["jobg8_match_score"] == ""


def test_review_sheet_keeps_plausible_jobg8_candidate():
    vacancy = Vacancy(
        source="North East Jobs",
        source_job_id="300001",
        title="Business Support Officer",
        employer="Example Council",
        location="Durham",
        ontap_geography="North East - County Durham & Darlington/Hartlepool",
        contract_type="Permanent",
        working_pattern="Full time",
        salary_text="£25,000",
        posted_date="",
        closing_date="02/08/2026 12:00",
        source_url="https://example.test/300001",
        screening_basis="clear title",
        detail_status="snapshot",
        classification="POSS",
        duplicate_status="POSSIBLE_DUPLICATE",
        jobg8_candidate_title="Business Support Officer",
        jobg8_candidate_advertiser="Example Recruitment",
        jobg8_match_score="0.810",
    )

    row = review_row(vacancy)

    assert row["closing_date"] == "02/08/2026 12:00"
    assert row["jobg8_check"] == "POSSIBLE_DUPLICATE"
    assert row["jobg8_candidate_title"] == "Business Support Officer"
    assert row["jobg8_candidate_employer"] == "Example Recruitment"


def test_only_default_end_of_day_closing_time_is_removed():
    assert review_closing_date("09/08/2026 23:59") == "09/08/2026"
    assert review_closing_date("09/08/2026 09:00") == "09/08/2026 09:00"


def test_rss_posted_date_is_standardised_for_review():
    assert review_posted_date("Wed, 15 Jul 2026 00:00:00 GMT") == "15/07/2026"
    assert review_posted_date("10/07/2026") == "10/07/2026"


def test_long_review_text_is_capped_without_changing_short_text():
    assert compact_review_text("Administration Assistant", 38) == (
        "Administration Assistant"
    )
    compacted = compact_review_text(
        "Finance & Office Administrator (Maternity Cover) – Office based",
        38,
    )
    assert compacted == "Finance & Office Administrator (Mater…"
    assert len(compacted) == 38


def test_default_review_outputs_are_separated_from_jobg8_reviews():
    args = parse_args([])

    assert args.report_csv == Path("reviews/external/northeast-jobs-review.csv")
    assert args.summary_md == Path("reviews/external/northeast-jobs-summary.md")

from pathlib import Path
import ssl
import sys
import urllib.error
from unittest.mock import patch


PIPELINE_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

from external_sources.northeast_jobs_poc import (  # noqa: E402
    FeedItem,
    ManualDecisionState,
    REPORT_FIELDS,
    Vacancy,
    annual_salary_upper,
    classify,
    compact_review_text,
    deduplicate,
    deduplicate_within_source,
    employer_from_page_title,
    extract_job_id,
    _fetch_renderer_text,
    fetch_text,
    infer_location_from_detail,
    parse_detail,
    parse_args,
    parse_rss_xml,
    final_decision_for,
    load_manual_decisions_from_markdown,
    review_closing_date,
    review_posted_date,
    review_row,
    screen_item,
    selected_vacancies,
    cluster_for_location,
    write_summary,
)


class FakeHeaders:
    @staticmethod
    def get_content_charset():
        return "utf-8"


class FakeResponse:
    headers = FakeHeaders()

    def __init__(self, text):
        self.text = text

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.text.encode("utf-8")


def test_fetch_uses_verified_renderer_only_for_nejobs_certificate_error():
    certificate_error = ssl.SSLCertVerificationError(
        1,
        "certificate verify failed: unable to get local issuer certificate",
    )
    url = "https://www.northeastjobs.org.uk/RSSJobs.aspx?orgid=62"

    with (
        patch(
            "external_sources.northeast_jobs_poc.urllib.request.urlopen",
            side_effect=[
                urllib.error.URLError(certificate_error),
                FakeResponse("rendered feed"),
            ],
        ) as urlopen,
        patch(
            "external_sources.northeast_jobs_poc._wait_for_renderer_slot"
        ),
    ):
        assert fetch_text(url) == "rendered feed"

    assert urlopen.call_count == 2
    assert urlopen.call_args_list[0].args[0].full_url == url
    assert urlopen.call_args_list[1].args[0].full_url == (
        "https://r.jina.ai/" + url
    )
    for call in urlopen.call_args_list:
        context = call.kwargs["context"]
        assert context.verify_mode == ssl.CERT_REQUIRED
        assert context.check_hostname is True


def test_fetch_does_not_hide_non_certificate_network_errors():
    with patch(
        "external_sources.northeast_jobs_poc.urllib.request.urlopen",
        side_effect=urllib.error.URLError("temporary DNS failure"),
    ) as urlopen:
        try:
            fetch_text("https://www.northeastjobs.org.uk/test")
        except urllib.error.URLError as exc:
            assert "temporary DNS failure" in str(exc)
        else:
            raise AssertionError("expected the original network failure")

    assert urlopen.call_count == 1


def test_renderer_retries_rate_limit_using_retry_after():
    url = "https://r.jina.ai/https://www.northeastjobs.org.uk/test"
    rate_limit_error = urllib.error.HTTPError(
        url,
        429,
        "Too Many Requests",
        {"Retry-After": "4"},
        None,
    )

    with (
        patch(
            "external_sources.northeast_jobs_poc.urllib.request.urlopen",
            side_effect=[rate_limit_error, FakeResponse("rendered detail")],
        ) as urlopen,
        patch(
            "external_sources.northeast_jobs_poc._wait_for_renderer_slot"
        ) as wait_for_slot,
        patch("external_sources.northeast_jobs_poc.time.sleep") as sleep,
    ):
        assert _fetch_renderer_text(url, 30) == "rendered detail"

    assert urlopen.call_count == 2
    assert wait_for_slot.call_count == 2
    sleep.assert_called_once_with(4.0)


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


def review_vacancy(
    source_job_id: str,
    classification: str,
    title: str = "Example Administrator",
) -> Vacancy:
    return Vacancy(
        source="North East Jobs",
        source_job_id=source_job_id,
        title=title,
        employer="Example Council",
        location="Durham",
        ontap_geography="North East - County Durham & Darlington/Hartlepool",
        contract_type="Permanent",
        working_pattern="Full time",
        salary_text="£25,000",
        posted_date="29/07/2026",
        closing_date="09/08/2026 23:59",
        source_url=f"https://example.test/{source_job_id}",
        screening_basis="test",
        detail_status="snapshot",
        classification=classification,
        classification_reason="test classification",
        duplicate_status="UNIQUE",
    )


def test_manual_review_actions_are_same_day_and_source_id_scoped(tmp_path):
    path = tmp_path / "review.md"
    path.write_text(
        "\n".join(
            [
                "# Review",
                "",
                "review_date: 2026-07-29",
                "",
                "---",
                "action: select",
                "POSS | Durham | Example role",
                "source_job_id: 300001",
                "---",
                "",
                "---",
                "action: exclude",
                "SELECTED | Newcastle | Another role",
                "source_job_id: 300002",
                "---",
            ]
        ),
        encoding="utf-8",
    )

    decisions = load_manual_decisions_from_markdown(path, "2026-07-29")
    old_decisions = load_manual_decisions_from_markdown(path, "2026-07-30")

    assert decisions.selections == {"300001"}
    assert decisions.exclusions == {"300002"}
    assert decisions.rerun_mode
    assert old_decisions.selections == set()
    assert old_decisions.exclusions == set()
    assert "old actions ignored" in old_decisions.load_warning


def test_manual_actions_change_the_final_selection():
    clear = review_vacancy("hc-1", "HC", "Administration Assistant")
    possible_selected = review_vacancy("poss-1", "POSS", "Attendance Officer")
    possible_excluded = review_vacancy("poss-2", "POSS", "Facilities Coordinator")
    decisions = ManualDecisionState(
        selections={"poss-1"},
        exclusions={"hc-1", "poss-2"},
        review_date="2026-07-29",
        rerun_mode=True,
    )

    assert final_decision_for(clear, decisions) == "EXCLUDED"
    assert final_decision_for(possible_selected, decisions) == "SELECTED"
    assert final_decision_for(possible_excluded, decisions) == "EXCLUDED"
    assert selected_vacancies(
        [clear, possible_selected, possible_excluded],
        decisions,
    ) == [possible_selected]


def test_summary_generates_jobg8_style_editable_action_blocks(tmp_path):
    path = tmp_path / "summary.md"
    clear = review_vacancy("hc-1", "HC", "Administration Assistant")
    possible = review_vacancy("poss-1", "POSS", "Attendance Officer")
    decisions = ManualDecisionState(
        selections=set(),
        exclusions=set(),
        review_date="2026-07-29",
    )
    counts = {
        "feed_total": 2,
        "hard_pass_before_detail": 0,
        "detail_candidates": 2,
        "detail_failures": 0,
        "outside_target_geography": 0,
        "tees_valley_excluded": 0,
        "target_geography_candidates": 2,
    }

    write_summary(
        path,
        counts=counts,
        vacancies=[clear, possible],
        decisions=decisions,
        review_date="2026-07-29",
        jobg8_count=10,
        rss_source="fixture.xml",
        failures=[],
    )
    text = path.read_text(encoding="utf-8")

    assert "Edit only the `action:` line" in text
    assert "## POSS — choose SELECT or EXCLUDE" in text
    assert "action:\nPOSS |" in text
    assert "source_job_id: poss-1" in text
    assert "Final selected after manual actions: 1" in text

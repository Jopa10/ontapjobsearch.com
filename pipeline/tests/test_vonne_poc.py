from pathlib import Path
import json
import sys


PIPELINE_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

from external_sources.vonne_poc import (  # noqa: E402
    COMBINED_TARGET_REGION,
    TARGET_CLUSTERS,
    TEES_VALLEY_CLUSTER,
    ListingItem,
    VonneVacancy,
    classify,
    deduplicate_nejobs,
    geography_for_item,
    parse_args,
    parse_detail,
    parse_listing_html,
    parse_listing_markdown,
    review_row,
)


def sample_vacancy(**overrides):
    values = {
        "source": "VONNE",
        "source_job_id": "173001",
        "title": "Business Support Officer",
        "employer": "Example Trust",
        "location": "Newcastle",
        "ontap_geography": (
            "North East - Tyneside, Wearside & Northumberland"
        ),
        "contract_type": "Permanent",
        "working_pattern": "Full time",
        "salary_text": "£25,000",
        "posted_date": "",
        "closing_date": "23 August 2026",
        "source_url": (
            "https://www.vonne.org.uk/"
            "vonne-jobs-details?cid=173001"
        ),
        "screening_basis": "clear title",
        "detail_status": "snapshot",
        "role_type": "Employment",
        "based": "Newcastle",
        "hours": "Full time",
        "role_description": "Officer",
        "geography_status": "CONFIRMED",
        "geography_reason": "location",
    }
    values.update(overrides)
    return VonneVacancy(**values)


def test_parse_listing_html_extracts_card_facts():
    text = """
    <html>
      <h3><a href="/vonne-jobs-details?cid=173001">
        Business Support Officer
      </a></h3>
      <a href="/vonne-jobs-details?cid=173001">Find out more</a>
      <div>Example Trust</div>
      <ul>
        <li>Salary: £25,000 Per Annum</li>
        <li>Location: Newcastle</li>
        <li>Closing Date: 23 August 2026</li>
      </ul>
    </html>
    """

    items = parse_listing_html(text)

    assert len(items) == 1
    assert items[0].title == "Business Support Officer"
    assert items[0].employer == "Example Trust"
    assert items[0].location == "Newcastle"
    assert items[0].source_job_id == "173001"


def test_parse_listing_markdown_extracts_card_facts():
    text = """### [Administrator](https://www.vonne.org.uk/vonne-jobs-details?cid=173002)

[Find out more](https://www.vonne.org.uk/vonne-jobs-details?cid=173002)

Example Charity

* Salary: £24,000 Per Annum
* Location: Durham
* Closing Date: 24 August 2026
"""

    item = parse_listing_markdown(text)[0]

    assert item.employer == "Example Charity"
    assert item.location == "Durham"


def test_parse_detail_retains_only_factual_fields():
    item = ListingItem(
        "173001",
        "Business Support Officer",
        "Example Trust",
        "Newcastle",
        "£25,000",
        "23 August 2026",
        "https://example.test/job",
    )
    text = """
    <html>
      <title>Job: Business Support Officer at Example Trust | VONNE</title>
      <h1>Business Support Officer at Example Trust</h1>
      <div>Contract Type:</div><div>Permanent</div>
      <div>Role Type:</div><div>Employment</div>
      <div>Hours:</div><div>Full time</div>
      <div>Application deadline:</div>
      <div>Sunday, August 23, 2026 - 00:00</div>
      <div>Based:</div><div>Hybrid</div>
      <div>Salary:</div><div>£25,000 Per Annum</div>
      <div>Location:</div><div>Newcastle</div>
      <div>Role description:</div><div>Officer</div>
      <p>This full description must never be retained.</p>
    </html>
    """

    detail = parse_detail(text, item)

    assert detail["employer"] == "Example Trust"
    assert detail["contract_type"] == "Permanent"
    assert "description" not in detail
    assert "This full description" not in json.dumps(detail)


def test_geography_confirms_target_and_excludes_tees_valley():
    cluster, status, _ = geography_for_item(
        title="Administrator",
        employer="Charity",
        location="Newcastle",
        based="",
        area_map={},
        fallback_map={},
    )
    assert cluster in TARGET_CLUSTERS
    assert status == "CONFIRMED"

    cluster, status, _ = geography_for_item(
        title="Administrator - Tees Valley",
        employer="Charity",
        location="Hybrid",
        based="",
        area_map={},
        fallback_map={},
    )
    assert cluster == TEES_VALLEY_CLUSTER
    assert status == "EXCLUDED"


def test_generic_hybrid_location_is_forced_to_review():
    cluster, status, _ = geography_for_item(
        title="Administrator",
        employer="Example Charity",
        location="Hybrid",
        based="Home-based",
        area_map={},
        fallback_map={},
    )

    assert cluster == COMBINED_TARGET_REGION
    assert status == "GENERIC_REVIEW"


def test_strong_approved_nejobs_duplicate_is_hard_pass():
    vacancy = sample_vacancy()
    candidates = [
        {
            "job_id": "nejobs-1",
            "title": "Business Support Officer",
            "employer": "Example Trust",
            "location": "Newcastle",
            "salary_text": "£25,000",
        }
    ]

    deduplicate_nejobs(vacancy, candidates)
    classify(vacancy, 30_000)

    assert vacancy.nejobs_duplicate_status == "DUPLICATE"
    assert vacancy.classification == "HARD_PASS"


def test_possible_jobg8_duplicate_stays_in_manual_review():
    vacancy = sample_vacancy(
        duplicate_status="POSSIBLE_DUPLICATE"
    )

    classify(vacancy, 30_000)

    assert vacancy.classification == "POSS"


def test_non_employment_role_is_hard_pass():
    vacancy = sample_vacancy(
        role_type="Trustee",
        title="Administrator",
    )

    classify(vacancy, 30_000)

    assert vacancy.classification == "HARD_PASS"


def test_review_row_keeps_vonne_source_identity():
    vacancy = sample_vacancy(classification="HC")

    row = review_row(vacancy)

    assert row["source"] == "VONNE"
    assert row["tracking_key"] == "vonne-173001"
    assert row["source_url"].endswith("cid=173001")



def test_hard_title_is_not_softened_by_derived_geography():
    vacancy = sample_vacancy(
        title="Chair of Trustees",
        location="Not stated",
        geography_status="DERIVED_REVIEW",
        geography_reason="employer-derived geography",
    )

    classify(vacancy, 30_000)

    assert vacancy.classification == "HARD_PASS"

def test_cli_has_no_publishing_option():
    try:
        parse_args(["--write-approved-json"])
    except SystemExit:
        pass
    else:
        raise AssertionError(
            "review-only parser accepted a publishing option"
        )

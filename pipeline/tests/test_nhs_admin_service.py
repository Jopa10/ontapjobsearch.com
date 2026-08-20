from __future__ import annotations

from datetime import date

from external_sources import nhs_admin_inventory as inventory
from external_sources import nhs_admin_service as nhs

TODAY = date(2026, 8, 20)


def test_title_classification_is_conservative() -> None:
    assert nhs.classify_title("Administrator")[0:2] == ("HC", "OPEN_SWITCH")
    assert nhs.classify_title("Medical Secretary")[0:2] == ("POSS", "BRIDGEABLE")
    assert nhs.classify_title("Service Manager")[0] == "HARD_PASS"


def test_compose_replaces_only_nhs_and_caps_share() -> None:
    base = [
        {"job_id": f"jobg8-{i}", "source": "JobG8", "region": "Yorkshire - West"}
        for i in range(8)
    ]
    current = [*base, {"job_id": "nhs-old", "source": "NHS Jobs", "region": "Yorkshire - West"}]
    candidates = [
        {"job_id": f"nhs-{i}", "source": "NHS Jobs", "region": "Yorkshire - West"}
        for i in range(5)
    ]
    composed, deferred = nhs.compose_region(current, candidates, region="Yorkshire - West")
    assert all(row["job_id"] != "nhs-old" for row in composed)
    assert len([row for row in composed if row["source"] == "JobG8"]) == 8
    assert len([row for row in composed if row["source"] == "NHS Jobs"]) == 2
    assert len(deferred) == 3
    assert all(row["deferred_reason"] == "NHS_SOURCE_SHARE_CAP" for row in deferred)


def test_selected_rows_require_same_day_live_and_open() -> None:
    rows = [
        {
            "review_date": TODAY.isoformat(),
            "source_job_id": "1",
            "title": "Administrator",
            "employer": "Example Trust",
            "location": "Leeds",
            "region": "Yorkshire - West",
            "apply_url": "https://example.test/1",
            "source_url": "https://example.test/1",
            "closing_date": "2026-08-31",
            "final_decision": "SELECTED",
            "publish_eligible": "YES",
            "switchability": "OPEN_SWITCH",
        },
        {
            "review_date": TODAY.isoformat(),
            "source_job_id": "2",
            "title": "Administrator",
            "employer": "Example Trust",
            "location": "Leeds",
            "region": "Yorkshire - West",
            "apply_url": "https://example.test/2",
            "closing_date": "2026-08-19",
            "final_decision": "SELECTED",
            "publish_eligible": "YES",
        },
    ]
    selected = nhs.selected_rows_for_composition(rows, today=TODAY)
    assert [row["job_id"] for row in selected] == ["nhs-1"]


def test_fingerprint_changes_when_material_facts_change() -> None:
    row = {
        "source": "NHS Jobs",
        "source_job_id": "x",
        "title": "Administrator",
        "employer": "Trust",
        "location": "Leeds",
        "region": "Yorkshire - West",
        "closing_date": "2026-08-31",
    }
    first = nhs.factual_fingerprint(row)
    second = nhs.factual_fingerprint({**row, "title": "Senior Administrator"})
    assert first != second


def test_public_advert_description_extracts_summary_and_duties_only() -> None:
    html = """
    <html><body>
      <h2>Job summary</h2>
      <p>Help the service with day-to-day administration.</p>
      <h3>Main duties of the job</h3>
      <p>Manage bookings and answer patient queries.</p>
      <ul><li>Maintain accurate records.</li></ul>
      <h2>About us</h2>
      <p>This employer boilerplate should not be copied.</p>
      <h2>Person Specification</h2>
      <p>This should not be copied either.</p>
    </body></html>
    """
    description = inventory.extract_advert_description(html)
    assert "day-to-day administration" in description
    assert "Manage bookings" in description
    assert "Maintain accurate records" in description
    assert "employer boilerplate" not in description
    assert "Person Specification" not in description

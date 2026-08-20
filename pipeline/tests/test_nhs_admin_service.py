from __future__ import annotations

from datetime import date

from external_sources import nhs_admin_inventory as inventory
from external_sources import nhs_admin_service as nhs

TODAY = date(2026, 8, 20)


def test_title_classification_uses_registry_and_is_conservative() -> None:
    assert nhs.classify_title("Administrator")[0:2] == ("HC", "OPEN_SWITCH")
    assert nhs.classify_title("Administrator")[3] == "A"
    assert nhs.classify_title("Medical Receptionist")[0] == "HC"
    assert nhs.classify_title("Medical Receptionist")[3] == "B"
    assert nhs.classify_title("Medical Secretary")[0:2] == ("POSS", "BRIDGEABLE")
    assert nhs.classify_title("Technician Support Officer")[0:2] == ("POSS", "BRIDGEABLE")
    assert nhs.classify_title("Network Administrator")[0:2] == ("POSS", "BRIDGEABLE")
    assert nhs.classify_title("SQL Database Administrator")[0:2] == ("POSS", "BRIDGEABLE")
    assert nhs.classify_title("Business Support Manager")[0:2] == ("POSS", "BRIDGEABLE")
    assert nhs.classify_title("Administrator and Health Care Support Worker")[0:2] == ("POSS", "BRIDGEABLE")
    assert nhs.classify_title("Medical Receptionist Team Lead")[0:2] == ("POSS", "BRIDGEABLE")
    assert nhs.classify_title("Service Manager")[0] == "HARD_PASS"
    assert nhs.classify_title("A completely unseen NHS admin title")[0] == "POSS"


def test_compose_replaces_only_nhs_caps_share_and_prioritises_tier_a() -> None:
    base = [
        {"job_id": f"jobg8-{i}", "source": "JobG8", "region": "Yorkshire - West"}
        for i in range(8)
    ]
    current = [
        *base,
        {"job_id": "nhs-old", "source": "NHS Jobs", "region": "Yorkshire - West"},
    ]
    candidates = [
        {
            "job_id": "nhs-b",
            "source": "NHS Jobs",
            "region": "Yorkshire - West",
            "hc_tier": "B",
            "switchability": "OPEN_SWITCH",
        },
        {
            "job_id": "nhs-a1",
            "source": "NHS Jobs",
            "region": "Yorkshire - West",
            "hc_tier": "A",
            "switchability": "OPEN_SWITCH",
        },
        {
            "job_id": "nhs-a2",
            "source": "NHS Jobs",
            "region": "Yorkshire - West",
            "hc_tier": "A",
            "switchability": "OPEN_SWITCH",
        },
        {
            "job_id": "nhs-b2",
            "source": "NHS Jobs",
            "region": "Yorkshire - West",
            "hc_tier": "B",
            "switchability": "OPEN_SWITCH",
        },
        {
            "job_id": "nhs-b3",
            "source": "NHS Jobs",
            "region": "Yorkshire - West",
            "hc_tier": "B",
            "switchability": "OPEN_SWITCH",
        },
    ]
    composed, deferred = nhs.compose_region(
        current, candidates, region="Yorkshire - West"
    )
    assert all(row["job_id"] != "nhs-old" for row in composed)
    assert len([row for row in composed if row["source"] == "JobG8"]) == 8
    accepted_nhs = [row for row in composed if row["source"] == "NHS Jobs"]
    assert [row["job_id"] for row in accepted_nhs] == ["nhs-a1", "nhs-a2"]
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
            "hc_tier": "A",
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
            "hc_tier": "A",
        },
    ]
    selected = nhs.selected_rows_for_composition(rows, today=TODAY)
    assert [row["job_id"] for row in selected] == ["nhs-1"]
    assert selected[0]["hc_tier"] == "A"


def test_fingerprint_changes_when_material_facts_change() -> None:
    row = {
        "source": "NHS Jobs",
        "source_job_id": "x",
        "title": "Administrator",
        "employer": "Trust",
        "location": "Leeds",
        "region": "Yorkshire - West",
        "closing_date": "2026-08-31",
        "hc_tier": "A",
    }
    first = nhs.factual_fingerprint(row)
    second = nhs.factual_fingerprint({**row, "title": "Senior Administrator"})
    assert first != second
    third = nhs.factual_fingerprint({**row, "hc_tier": "B"})
    assert first == third  # Tier tuning must not invalidate remembered decisions.


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

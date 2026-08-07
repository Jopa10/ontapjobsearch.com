from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from external_sources import teaching_vacancies_regional_review as review

LONDON = ZoneInfo("Europe/London")


def routed_row(
    source_job_id: str,
    *,
    region: str = "Yorkshire - West",
    status: str = "LIVE",
    title: str = "Administrator",
    employer: str = "Example School",
    location: str = "Leeds, Yorkshire and the Humber, LS1 1AA",
    salary: str = "£25,000",
    closing: str = "2026-08-30T23:59:00+01:00",
    fingerprint: str = "a" * 64,
) -> dict[str, str]:
    row = {field: "" for field in review.routing.ROUTING_FIELDS}
    row.update(
        {
            "run_date": "2026-08-06",
            "source": "Teaching Vacancies",
            "source_job_id": source_job_id,
            "canonical_url": (
                "https://teaching-vacancies.service.gov.uk/jobs/" + source_job_id
            ),
            "title": title,
            "employer": employer,
            "location": location,
            "postcode": "LS1 1AA",
            "salary_text": salary,
            "posted_date": "2026-08-01",
            "closing_date": closing,
            "employment_type": "FULL_TIME",
            "description_excerpt": "Provide administrative support.",
            "discovery_routes": "[]",
            "detail_fetch_status": "OK",
            "factual_fingerprint": fingerprint,
            "geo_cluster": region,
            "ontap_region": region,
            "geography_status": "ROUTED",
            "geography_reason": "Exact locality match in geo_lookup.xlsx",
            "geography_lookup_key": "leeds",
            "slice_category": "admin_service",
            "slice_status": status,
            "publish_eligible": "YES" if status == "LIVE" else "NO",
        }
    )
    return row


def classify(rows: list[dict[str, str]], jobg8: dict[str, list[dict]] | None = None):
    return review.classify_routed_rows(
        rows,
        jobg8_by_region=jobg8 or {},
        now=datetime(2026, 8, 6, 14, 0, tzinfo=LONDON),
    )


def test_region_slugs_follow_existing_yorkshire_names_and_support_any_region() -> None:
    assert review.region_slug("Yorkshire - West") == "west-yorkshire"
    assert review.region_slug("Yorkshire - East") == "east-yorkshire"
    assert review.region_slug("North East") == "north-east"
    assert review.region_slug("Lancashire - Central") == "lancashire-central"


def test_live_and_candidate_regions_both_generate_reviewable_records() -> None:
    records = classify(
        [
            routed_row("west", status="LIVE"),
            routed_row(
                "east",
                region="Yorkshire - East",
                status="CANDIDATE",
                location="Hull, East Riding of Yorkshire, HU1 1AA",
            ),
        ]
    )
    by_id = {row.vacancy.source_job_id: row for row in records}

    assert review.decision_for(by_id["west"]) == "SELECTED"
    assert by_id["west"].publish_eligible == "YES"
    assert review.decision_for(by_id["east"]) == "SELECTED"
    assert by_id["east"].publish_eligible == "NO"
    assert by_id["east"].slice_status == "CANDIDATE"


def test_confirmed_jobg8_duplicate_hard_passes_external_copy() -> None:
    row = routed_row("duplicate", title="Administrator", employer="Example School")
    records = classify(
        [row],
        {
            "Yorkshire - West": [
                {
                    "title": "Administrator",
                    "advertiser_name": "Example School",
                    "source": "JobG8",
                }
            ]
        },
    )

    assert records[0].vacancy.jobg8_check == "DUPLICATE"
    assert review.decision_for(records[0]) == "HARD_PASS"
    assert records[0].vacancy.classification_reason == "Confirmed JobG8 duplicate"


def test_expired_vacancy_drops_to_hard_pass() -> None:
    records = classify(
        [routed_row("expired", closing="2026-08-05T23:59:00+01:00")]
    )

    assert review.decision_for(records[0]) == "HARD_PASS"
    assert records[0].vacancy.classification_reason == "Expired, closed or invalid deadline"


def test_reviewable_missing_salary_hard_passes_only_that_vacancy() -> None:
    records = classify(
        [
            routed_row("missing-pay", salary=""),
            routed_row("normal-pay", salary="£25,000"),
        ]
    )
    by_id = {row.vacancy.source_job_id: row for row in records}

    assert len(records) == 2
    assert review.decision_for(by_id["missing-pay"]) == "HARD_PASS"
    assert (
        by_id["missing-pay"].vacancy.classification_reason
        == "Missing salary or pay scale"
    )
    assert review.decision_for(by_id["normal-pay"]) == "SELECTED"


def legacy_summary_block(
    *,
    source_job_id: str,
    action: str,
    title: str = "Administrator",
    employer: str = "Example School",
    location: str = "Leeds, Yorkshire and the Humber, LS1 1AA",
    salary: str = "£25,000",
    closing: str = "2026-08-30T23:59:00+01:00",
    reason: str = "Clear admin/service title: administrator",
) -> str:
    return f"""# Legacy review

---
action: {action}
SELECTED | Yorkshire - West | {location} | {salary} | {title}
employer: {employer}
closing_date: {closing}
reason: {reason}
source: Teaching Vacancies
source_job_id: {source_job_id}
source_url: https://teaching-vacancies.service.gov.uk/jobs/{source_job_id}
---
"""


def write_approved(path: Path, ids: list[str]) -> None:
    path.write_text(
        json.dumps(
            [
                {
                    "job_id": "teaching-vacancies-" + source_job_id,
                    "source": "Teaching Vacancies",
                }
                for source_job_id in ids
            ]
        ),
        encoding="utf-8",
    )


def test_legacy_selection_migrates_only_when_full_facts_and_approval_match(
    tmp_path: Path,
) -> None:
    records = classify([routed_row("old-selected")])
    summary = tmp_path / "legacy.md"
    summary.write_text(
        legacy_summary_block(source_job_id="old-selected", action="select"),
        encoding="utf-8",
    )
    approved_path = tmp_path / "approved.json"
    write_approved(approved_path, ["old-selected"])

    report = review.migrate_legacy_west_yorkshire(
        records,
        legacy_summary_path=summary,
        legacy_approved_path=approved_path,
    )

    assert records[0].manual_action == "select"
    assert records[0].migration_status == "MIGRATED_UNCHANGED"
    assert report[0]["migration_status"] == "MIGRATED_UNCHANGED"


def test_changed_legacy_record_requires_review_and_does_not_migrate(
    tmp_path: Path,
) -> None:
    records = classify([routed_row("changed", salary="£26,000")])
    summary = tmp_path / "legacy.md"
    summary.write_text(
        legacy_summary_block(
            source_job_id="changed",
            action="select",
            salary="£25,000",
        ),
        encoding="utf-8",
    )
    approved_path = tmp_path / "approved.json"
    write_approved(approved_path, ["changed"])

    report = review.migrate_legacy_west_yorkshire(
        records,
        legacy_summary_path=summary,
        legacy_approved_path=approved_path,
    )

    assert records[0].manual_action == ""
    assert records[0].migration_status == "REVIEW_REQUIRED"
    assert "salary" in report[0]["detail"]


def test_blank_legacy_poss_remains_blank(tmp_path: Path) -> None:
    records = classify(
        [
            routed_row(
                "borderline",
                title="Office Manager",
            )
        ]
    )
    summary = tmp_path / "legacy.md"
    summary.write_text(
        legacy_summary_block(
            source_job_id="borderline",
            action="",
            title="Office Manager",
            reason="Borderline school administration title: office manager",
        ).replace("SELECTED |", "POSS |"),
        encoding="utf-8",
    )
    approved_path = tmp_path / "approved.json"
    write_approved(approved_path, [])

    review.migrate_legacy_west_yorkshire(
        records,
        legacy_summary_path=summary,
        legacy_approved_path=approved_path,
    )

    assert records[0].manual_action == ""
    assert records[0].migration_status == "BLANK_POSS_PRESERVED"
    assert review.decision_for(records[0]) == "POSS"


def test_same_day_action_requires_matching_factual_fingerprint(tmp_path: Path) -> None:
    records = classify([routed_row("same-day", fingerprint="f" * 64)])
    summary_path = tmp_path / "summary.md"
    summary_path.write_text(
        """review_date: 2026-08-06
---
action: exclude
factual_fingerprint: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
source_job_id: same-day
---
""",
        encoding="utf-8",
    )

    review.apply_existing_actions(
        records,
        summary_path=summary_path,
        review_date="2026-08-06",
    )

    assert records[0].manual_action == "exclude"
    assert review.decision_for(records[0]) == "EXCLUDED"


def test_verified_routing_hash_blocks_review_on_tampering(tmp_path: Path) -> None:
    path = tmp_path / "routed.csv"
    path.write_text("bad", encoding="utf-8")
    summary = tmp_path / "summary.json"
    summary.write_text(
        json.dumps(
            {
                "source": "Teaching Vacancies",
                "records": 1,
                "routed_csv_sha256": hashlib.sha256(b"different").hexdigest(),
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="SHA256"):
        review.load_verified_routing(path, summary)

def test_possible_jobg8_duplicate_requires_fresh_review_before_select_carries(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        review.poc,
        "compare_jobg8",
        lambda vacancy, rows: (
            "POSSIBLE_DUPLICATE",
            "Admin Assistant",
            "Example Employer",
            "0.695",
        ),
    )
    records = classify([routed_row("possible-duplicate")])
    record = records[0]

    assert record.vacancy.classification == "POSS"
    assert record.vacancy.jobg8_check == "POSSIBLE_DUPLICATE"
    assert review.decision_for(record) == "POSS"

    summary_path = tmp_path / "summary.md"
    summary_path.write_text(
        "review_date: 2026-08-06\n"
        "---\n"
        "action: select\n"
        "factual_fingerprint: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"
        "source_job_id: possible-duplicate\n"
        "---\n",
        encoding="utf-8",
    )

    review.apply_existing_actions(
        records,
        summary_path=summary_path,
        review_date="2026-08-06",
    )

    assert record.manual_action == ""
    assert record.migration_status == "REVIEW_REQUIRED_DUPLICATE"
    assert review.decision_for(record) == "POSS"


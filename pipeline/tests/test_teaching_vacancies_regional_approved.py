from __future__ import annotations

import csv
import hashlib
import io
import json
from datetime import datetime
from pathlib import Path

import pytest

from external_sources import teaching_vacancies_approved as legacy_approved
from external_sources import teaching_vacancies_poc as poc
from external_sources import teaching_vacancies_regional_approved as approval
from external_sources import teaching_vacancies_regional_review as review

NOW = datetime(2026, 8, 6, 12, 0, tzinfo=legacy_approved.LONDON)


def make_record(
    source_job_id: str,
    *,
    region: str = "Yorkshire - West",
    slice_status: str = "LIVE",
    classification: str = "HC",
    title: str = "Administrative Assistant",
    manual_action: str = "",
    migration_status: str = "",
    closing_date: str = "2026-08-31T17:00:00+01:00",
) -> review.ReviewRecord:
    reasons = {
        "HC": "Clear admin/service title: administrative assistant",
        "POSS": "Borderline school administration title: office manager",
        "HARD_PASS": "Out-of-scope occupation: teacher",
    }
    vacancy = poc.Vacancy(
        source_job_id=source_job_id,
        title=title,
        employer="Example Academy",
        location="Leeds, Yorkshire and the Humber, LS1 1AA",
        salary_text="£25,000",
        posted_date="2026-08-01",
        closing_date=closing_date,
        employment_type="FULL_TIME",
        source_url=(
            "https://teaching-vacancies.service.gov.uk/jobs/" + source_job_id
        ),
        geography_status="IN_SCOPE",
        geography_reason="Exact location fallback match",
        classification=classification,
        classification_reason=reasons[classification],
        jobg8_check="NO_MATCH",
        jobg8_match_score="0.000",
    )
    return review.ReviewRecord(
        vacancy=vacancy,
        ontap_region=region,
        geo_cluster=region,
        geography_reason="Exact location fallback match",
        geography_lookup_key="leeds",
        slice_status=slice_status,
        publish_eligible="YES" if slice_status == "LIVE" else "NO",
        factual_fingerprint=hashlib.sha256(source_job_id.encode()).hexdigest(),
        discovery_routes="[]",
        manual_action=manual_action,
        migration_status=migration_status,
    )


def write_review(
    tmp_path: Path,
    records: list[review.ReviewRecord],
    *,
    review_date: str = "2026-08-06",
) -> tuple[Path, Path]:
    region = records[0].ontap_region
    review_csv = tmp_path / "review.csv"
    summary_md = tmp_path / "summary.md"
    review_csv.write_bytes(review.review_csv_bytes(records))
    summary_md.write_text(
        review.markdown_summary(
            region,
            records,
            review_date=review_date,
            routing_manifest_sha256="a" * 64,
        ),
        encoding="utf-8",
    )
    return review_csv, summary_md


def rewrite_csv(path: Path, mutate) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [dict(row) for row in reader]
    mutate(rows)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def test_live_snapshot_includes_selected_and_excludes_blank_poss(
    tmp_path: Path,
) -> None:
    records = [
        make_record("auto-selected"),
        make_record(
            "blank-poss",
            classification="POSS",
            title="Office Manager",
        ),
        make_record(
            "selected-poss",
            classification="POSS",
            title="Office Manager",
            manual_action="select",
        ),
        make_record("excluded-hc", manual_action="exclude"),
    ]
    review_csv, summary_md = write_review(tmp_path, records)

    metadata, loaded, review_content, summary_content = (
        approval.validate_review_for_approval(
            review_csv,
            summary_md,
            now=NOW,
        )
    )
    rows = approval.approved_output_rows(loaded, region=metadata.region)

    assert metadata.slice_status == "LIVE"
    assert {row["job_id"] for row in rows} == {
        "teaching-vacancies-auto-selected",
        "teaching-vacancies-selected-poss",
    }
    assert all(row["region"] == "Yorkshire - West" for row in rows)
    assert review_content == review_csv.read_bytes()
    assert summary_content == summary_md.read_bytes()


def test_candidate_slice_cannot_write_approved_snapshot(tmp_path: Path) -> None:
    records = [
        make_record(
            "east-job",
            region="Yorkshire - East",
            slice_status="CANDIDATE",
        )
    ]
    review_csv, summary_md = write_review(tmp_path, records)

    with pytest.raises(ValueError, match="not LIVE"):
        approval.validate_review_for_approval(
            review_csv,
            summary_md,
            now=NOW,
        )


def test_inconsistent_final_decision_is_blocked(tmp_path: Path) -> None:
    records = [make_record("blank-poss", classification="POSS", title="Office Manager")]
    review_csv, summary_md = write_review(tmp_path, records)
    rewrite_csv(
        review_csv,
        lambda rows: rows[0].update({"final_decision": "SELECTED"}),
    )

    with pytest.raises(ValueError, match="inconsistent final decision"):
        approval.validate_review_for_approval(
            review_csv,
            summary_md,
            now=NOW,
        )


def test_summary_fingerprint_mismatch_is_blocked(tmp_path: Path) -> None:
    records = [make_record("admin")]
    review_csv, summary_md = write_review(tmp_path, records)
    text = summary_md.read_text(encoding="utf-8")
    summary_md.write_text(
        text.replace(
            f"review_fingerprint: {review.review_fingerprint(records)}",
            "review_fingerprint: " + "b" * 64,
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="fingerprint differs"):
        approval.validate_review_for_approval(
            review_csv,
            summary_md,
            now=NOW,
        )


def test_changed_migrated_job_requires_explicit_action(tmp_path: Path) -> None:
    records = [make_record("changed", migration_status="REVIEW_REQUIRED")]
    review_csv, summary_md = write_review(tmp_path, records)

    with pytest.raises(ValueError, match="requires an explicit"):
        approval.validate_review_for_approval(
            review_csv,
            summary_md,
            now=NOW,
        )

    records[0].manual_action = "select"
    review_csv, summary_md = write_review(tmp_path, records)
    metadata, loaded, _, _ = approval.validate_review_for_approval(
        review_csv,
        summary_md,
        now=NOW,
    )
    assert approval.approved_output_rows(loaded, region=metadata.region)


def test_expired_selected_job_is_blocked(tmp_path: Path) -> None:
    records = [make_record("expired", closing_date="2026-08-05T17:00:00+01:00")]
    review_csv, summary_md = write_review(tmp_path, records)

    with pytest.raises(ValueError, match="expired or closed"):
        approval.validate_review_for_approval(
            review_csv,
            summary_md,
            now=NOW,
        )


def test_region_specific_paths_do_not_replace_legacy_snapshot() -> None:
    approved_path, evidence_path = approval.default_output_paths(
        "Yorkshire - West"
    )

    assert approved_path == Path(
        "output-external/teaching-vacancies-regional/"
        "west-yorkshire-admin-service.json"
    )
    assert approved_path != legacy_approved.DEFAULT_APPROVED_JSON
    assert evidence_path.name == "west-yorkshire-admin-service-evidence.json"


def test_evidence_binds_review_summary_and_snapshot(tmp_path: Path) -> None:
    records = [make_record("admin")]
    review_csv, summary_md = write_review(tmp_path, records)
    metadata, loaded, review_content, summary_content = (
        approval.validate_review_for_approval(
            review_csv,
            summary_md,
            now=NOW,
        )
    )
    rows = approval.approved_output_rows(loaded, region=metadata.region)
    snapshot = approval.snapshot_bytes(rows)
    evidence = json.loads(
        approval.evidence_bytes(
            metadata=metadata,
            rows=rows,
            review_content=review_content,
            summary_content=summary_content,
            snapshot_content=snapshot,
            generated_at=NOW,
        )
    )

    assert evidence["approved_rows"] == 1
    assert evidence["approved_job_ids"] == ["teaching-vacancies-admin"]
    assert evidence["review_csv_sha256"] == hashlib.sha256(
        review_content
    ).hexdigest()
    assert evidence["summary_md_sha256"] == hashlib.sha256(
        summary_content
    ).hexdigest()
    assert evidence["approved_snapshot_sha256"] == hashlib.sha256(
        snapshot
    ).hexdigest()


def test_review_from_yesterday_is_still_approvable(tmp_path: Path) -> None:
    records = [make_record("admin")]
    review_csv, summary_md = write_review(
        tmp_path,
        records,
        review_date="2026-08-05",
    )

    metadata, loaded, _, _ = approval.validate_review_for_approval(
        review_csv,
        summary_md,
        now=NOW,
    )
    assert metadata.review_date == "2026-08-05"
    assert approval.approved_output_rows(loaded, region=metadata.region)


def test_review_older_than_two_days_is_blocked(tmp_path: Path) -> None:
    records = [make_record("admin")]
    review_csv, summary_md = write_review(
        tmp_path,
        records,
        review_date="2026-08-03",
    )

    with pytest.raises(ValueError, match="older than 2 days"):
        approval.validate_review_for_approval(
            review_csv,
            summary_md,
            now=NOW,
        )

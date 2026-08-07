"""Build separate approved Teaching Vacancies snapshots from regional reviews.

This stage consumes one completed regional review at a time. It verifies the
review CSV against its Markdown summary, requires an explicit LIVE slice, and
writes a region-specific approved snapshot plus audit evidence. CANDIDATE,
UNREGISTERED, blank POSS, unresolved and stale reviews cannot publish.

The existing West Yorkshire approved snapshot is not replaced by this module;
new snapshots are written under ``output-external/teaching-vacancies-regional``
so old/new compatibility can be proved before daily composition changes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

from external_sources import teaching_vacancies_approved as legacy_approved
from external_sources import teaching_vacancies_discovery as discovery
from external_sources import teaching_vacancies_poc as poc
from external_sources import teaching_vacancies_regional_review as regional_review
from external_sources.regional_contracts import clean

APPROVAL_CONTRACT_VERSION = "teaching-vacancies-regional-approved-v1"
APPROVAL_CONFIRMATION = legacy_approved.APPROVAL_CONFIRMATION
CATEGORY = "admin_service"
LIVE_STATUS = "LIVE"
SOURCE_CODE = discovery.SOURCE_CODE
DEFAULT_OUTPUT_DIR = Path("output-external/teaching-vacancies-regional")
DEFAULT_EVIDENCE_DIR = Path("manifests/external/teaching-vacancies/approved")
MAX_REVIEW_AGE_DAYS = 2


@dataclass(frozen=True)
class ReviewMetadata:
    review_date: str
    review_fingerprint: str
    routing_manifest_sha256: str
    region: str
    category: str
    slice_status: str


@dataclass
class LoadedReviewRow:
    record: regional_review.ReviewRecord
    declared_decision: str


def _line_value(text: str, key: str) -> str:
    match = re.search(
        rf"(?mi)^{re.escape(key)}:[ \t]*(.*?)[ \t]*$",
        text,
    )
    return clean(match.group(1)) if match else ""


def parse_review_metadata(path: Path) -> tuple[ReviewMetadata, str]:
    if not path.is_file():
        raise ValueError(f"regional review summary not found: {path}")
    text = path.read_text(encoding="utf-8-sig")
    metadata = ReviewMetadata(
        review_date=_line_value(text, "review_date"),
        review_fingerprint=_line_value(text, "review_fingerprint"),
        routing_manifest_sha256=_line_value(text, "routing_manifest_sha256"),
        region=_line_value(text, "ontap_region"),
        category=_line_value(text, "slice_category"),
        slice_status=_line_value(text, "slice_status").upper(),
    )
    missing = [
        field
        for field, value in (
            ("review_date", metadata.review_date),
            ("review_fingerprint", metadata.review_fingerprint),
            ("routing_manifest_sha256", metadata.routing_manifest_sha256),
            ("ontap_region", metadata.region),
            ("slice_category", metadata.category),
            ("slice_status", metadata.slice_status),
        )
        if not value
    ]
    if missing:
        raise ValueError(
            "regional review summary is missing metadata: " + ", ".join(missing)
        )
    return metadata, text


def parse_summary_actions(text: str) -> dict[str, tuple[str, str]]:
    actions: dict[str, tuple[str, str]] = {}
    for block in re.findall(r"(?ms)^---\s*$\n(.*?)^---\s*$", text):
        source_job_id = _line_value(block, "source_job_id")
        if not source_job_id:
            continue
        if source_job_id in actions:
            raise ValueError(
                f"duplicate source_job_id in regional review summary: {source_job_id}"
            )
        action = _line_value(block, "action").casefold()
        fingerprint = _line_value(block, "factual_fingerprint")
        if action not in {"", "select", "exclude"}:
            raise ValueError(
                f"invalid regional review action for {source_job_id}: {action}"
            )
        if not fingerprint:
            raise ValueError(
                f"regional review summary block has no factual fingerprint: "
                f"{source_job_id}"
            )
        actions[source_job_id] = (action, fingerprint)
    return actions


def _review_record_from_csv(row: dict[str, str]) -> regional_review.ReviewRecord:
    jobg8_check = clean(row.get("jobg8_check"))
    if jobg8_check == "No plausible JobG8 match":
        jobg8_check = "NO_MATCH"
    vacancy = poc.Vacancy(
        source=discovery.SOURCE,
        source_job_id=clean(row.get("source_job_id")),
        title=clean(row.get("title")),
        employer=clean(row.get("employer")),
        location=clean(row.get("location")),
        salary_text=clean(row.get("salary_text")),
        posted_date=clean(row.get("posted_date")),
        closing_date=clean(row.get("closing_date")),
        employment_type=clean(row.get("employment_type")),
        source_url=clean(row.get("source_url")),
        geography_status="IN_SCOPE",
        geography_reason=clean(row.get("geography_reason")),
        classification=clean(row.get("classification")),
        classification_reason=clean(row.get("classification_reason")),
        jobg8_check=jobg8_check,
        jobg8_candidate_title=clean(row.get("jobg8_candidate_title")),
        jobg8_candidate_employer=clean(row.get("jobg8_candidate_employer")),
        jobg8_match_score=clean(row.get("jobg8_match_score")),
    )
    return regional_review.ReviewRecord(
        vacancy=vacancy,
        ontap_region=clean(row.get("ontap_region")),
        geo_cluster=clean(row.get("geo_cluster")),
        geography_reason=clean(row.get("geography_reason")),
        geography_lookup_key=clean(row.get("geography_lookup_key")),
        slice_status=clean(row.get("slice_status")).upper(),
        publish_eligible=clean(row.get("publish_eligible")).upper(),
        factual_fingerprint=clean(row.get("factual_fingerprint")),
        discovery_routes=clean(row.get("discovery_routes")),
        manual_action=clean(row.get("manual_action")).casefold(),
        migration_status=clean(row.get("migration_status")),
    )


def load_review_csv(path: Path) -> tuple[list[LoadedReviewRow], bytes]:
    if not path.is_file():
        raise ValueError(f"regional review CSV not found: {path}")
    content = path.read_bytes()
    with io.StringIO(content.decode("utf-8-sig"), newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != regional_review.REVIEW_FIELDS:
            raise ValueError("regional review CSV columns do not match the contract")
        source_rows = [dict(row) for row in reader]
    if not source_rows:
        raise ValueError("regional review CSV contains no rows")

    output: list[LoadedReviewRow] = []
    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    for line_number, row in enumerate(source_rows, start=2):
        if clean(row.get("source")) != SOURCE_CODE:
            raise ValueError(f"regional review row {line_number} has wrong source")
        if clean(row.get("geography_status")) != "ROUTED":
            raise ValueError(
                f"regional review row {line_number} is not factually routed"
            )
        source_job_id = clean(row.get("source_job_id"))
        source_url = clean(row.get("source_url")).rstrip("/")
        if not source_job_id or not source_url:
            raise ValueError(
                f"regional review row {line_number} has no stable ID or source URL"
            )
        if source_job_id.casefold() in seen_ids:
            raise ValueError(f"duplicate regional review ID: {source_job_id}")
        if source_url.casefold() in seen_urls:
            raise ValueError(f"duplicate regional review URL: {source_url}")
        seen_ids.add(source_job_id.casefold())
        seen_urls.add(source_url.casefold())

        record = _review_record_from_csv(row)
        if record.manual_action not in {"", "select", "exclude"}:
            raise ValueError(
                f"invalid manual action for regional review ID {source_job_id}"
            )
        if not record.factual_fingerprint:
            raise ValueError(
                f"regional review ID {source_job_id} has no factual fingerprint"
            )
        output.append(
            LoadedReviewRow(
                record=record,
                declared_decision=clean(row.get("final_decision")).upper(),
            )
        )
    return output, content


def _review_age_days(value: str, now: datetime | None) -> int | None:
    current = now or datetime.now(legacy_approved.LONDON)
    if current.tzinfo is None:
        current = current.replace(tzinfo=legacy_approved.LONDON)
    try:
        reviewed = date.fromisoformat(value)
    except ValueError:
        return None
    today = current.astimezone(legacy_approved.LONDON).date()
    return (today - reviewed).days


def validate_review_for_approval(
    review_csv: Path,
    summary_md: Path,
    *,
    now: datetime | None = None,
) -> tuple[ReviewMetadata, list[LoadedReviewRow], bytes, bytes]:
    metadata, summary_text = parse_review_metadata(summary_md)
    loaded, review_content = load_review_csv(review_csv)
    summary_content = summary_md.read_bytes()
    errors: list[str] = []

    review_age = _review_age_days(metadata.review_date, now)
    if review_age is None:
        errors.append("the regional review date is invalid")
    elif review_age < 0:
        errors.append("the regional review date is in the future")
    elif review_age > MAX_REVIEW_AGE_DAYS:
        errors.append(
            f"the regional review is older than {MAX_REVIEW_AGE_DAYS} days"
        )
    if metadata.category != CATEGORY:
        errors.append("the regional review category is not admin_service")
    if metadata.slice_status != LIVE_STATUS:
        errors.append(
            f"slice {metadata.region} is {metadata.slice_status}, not LIVE"
        )

    records = [item.record for item in loaded]
    regions = {row.ontap_region for row in records}
    statuses = {row.slice_status for row in records}
    publish_flags = {row.publish_eligible for row in records}
    if regions != {metadata.region}:
        errors.append("the review CSV contains a different or mixed Ontap region")
    if statuses != {metadata.slice_status}:
        errors.append("the review CSV slice status differs from the summary")
    if publish_flags != {"YES"}:
        errors.append("one or more regional review rows are not publish eligible")

    actual_fingerprint = regional_review.review_fingerprint(records)
    if metadata.review_fingerprint != actual_fingerprint:
        errors.append("the review CSV fingerprint differs from the summary")

    summary_actions = parse_summary_actions(summary_text)
    reviewable_ids = {
        row.vacancy.source_job_id
        for row in records
        if row.vacancy.classification != "HARD_PASS"
    }
    if set(summary_actions) != reviewable_ids:
        added = sorted(reviewable_ids - set(summary_actions))
        removed = sorted(set(summary_actions) - reviewable_ids)
        detail: list[str] = []
        if added:
            detail.append("missing summary IDs: " + ", ".join(added))
        if removed:
            detail.append("unexpected summary IDs: " + ", ".join(removed))
        errors.append(
            "the Markdown reviewable set differs from the CSV"
            + (f" ({'; '.join(detail)})" if detail else "")
        )

    for loaded_row in loaded:
        record = loaded_row.record
        vacancy = record.vacancy
        source_job_id = vacancy.source_job_id
        expected_decision = regional_review.decision_for(record)
        if loaded_row.declared_decision != expected_decision:
            errors.append(
                f"regional review ID {source_job_id} has an inconsistent final decision"
            )
        if vacancy.classification == "HARD_PASS":
            if record.manual_action:
                errors.append(
                    f"hard-pass regional review ID {source_job_id} has a manual action"
                )
            continue

        summary_action = summary_actions.get(source_job_id)
        if summary_action:
            action, fingerprint = summary_action
            if action != record.manual_action:
                errors.append(
                    f"regional review action differs between CSV and Markdown: "
                    f"{source_job_id}"
                )
            if fingerprint != record.factual_fingerprint:
                errors.append(
                    f"regional review factual fingerprint differs in Markdown: "
                    f"{source_job_id}"
                )

        if (
            record.migration_status == "REVIEW_REQUIRED"
            and record.manual_action not in {"select", "exclude"}
        ):
            errors.append(
                f"migrated regional review ID {source_job_id} requires an "
                "explicit select or exclude action"
            )

        if expected_decision != "SELECTED":
            continue
        missing = [
            label
            for label, value in (
                ("title", vacancy.title),
                ("employer", vacancy.employer),
                ("location", vacancy.location),
                ("salary or pay scale", vacancy.salary_text),
                ("closing date", vacancy.closing_date),
                ("source URL", vacancy.source_url),
            )
            if not clean(value)
        ]
        if missing:
            errors.append(
                f"selected regional review ID {source_job_id} is missing facts: "
                + ", ".join(missing)
            )
        if vacancy.jobg8_check == "DUPLICATE":
            errors.append(
                f"selected regional review ID {source_job_id} is a JobG8 duplicate"
            )

    if errors:
        raise ValueError(
            "Teaching Vacancies regional approval is blocked:\n- "
            + "\n- ".join(errors)
        )
    return metadata, loaded, review_content, summary_content


def approved_output_rows(
    loaded: Iterable[LoadedReviewRow],
    *,
    region: str,
    now: datetime | None = None,
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for item in loaded:
        if item.declared_decision != "SELECTED":
            continue
        if not legacy_approved.vacancy_is_open(item.record.vacancy, now=now):
            continue
        row = legacy_approved.vacancy_to_published_job(item.record.vacancy)
        row["region"] = clean(region)
        output.append(row)
    job_ids = [row["job_id"] for row in output]
    if len(job_ids) != len(set(job_ids)):
        raise ValueError("approved regional snapshot would contain duplicate job IDs")
    return sorted(
        output,
        key=lambda row: (
            row["closing_date"],
            row["title"].casefold(),
            row["job_id"],
        ),
    )


def default_output_paths(region: str) -> tuple[Path, Path]:
    slug = regional_review.region_slug(region)
    return (
        DEFAULT_OUTPUT_DIR / f"{slug}-admin-service.json",
        DEFAULT_EVIDENCE_DIR / f"{slug}-admin-service-evidence.json",
    )


def snapshot_bytes(rows: list[dict[str, str]]) -> bytes:
    return (json.dumps(rows, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def evidence_bytes(
    *,
    metadata: ReviewMetadata,
    rows: list[dict[str, str]],
    review_content: bytes,
    summary_content: bytes,
    snapshot_content: bytes,
    generated_at: datetime | None = None,
) -> bytes:
    now = generated_at or datetime.now(legacy_approved.LONDON)
    if now.tzinfo is None:
        now = now.replace(tzinfo=legacy_approved.LONDON)
    evidence = {
        "contract_version": APPROVAL_CONTRACT_VERSION,
        "generated_at": now.astimezone(legacy_approved.LONDON).isoformat(
            timespec="seconds"
        ),
        "source": SOURCE_CODE,
        "region": metadata.region,
        "category": metadata.category,
        "slice_status": metadata.slice_status,
        "review_date": metadata.review_date,
        "review_fingerprint": metadata.review_fingerprint,
        "routing_manifest_sha256": metadata.routing_manifest_sha256,
        "review_csv_sha256": hashlib.sha256(review_content).hexdigest(),
        "summary_md_sha256": hashlib.sha256(summary_content).hexdigest(),
        "approved_snapshot_sha256": hashlib.sha256(snapshot_content).hexdigest(),
        "approved_rows": len(rows),
        "approved_job_ids": [row["job_id"] for row in rows],
    }
    return (json.dumps(evidence, ensure_ascii=False, indent=2) + "\n").encode(
        "utf-8"
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-csv", type=Path, required=True)
    parser.add_argument("--summary-md", type=Path, required=True)
    parser.add_argument("--approved-json", type=Path)
    parser.add_argument("--evidence-json", type=Path)
    parser.add_argument("--write-approved-json", action="store_true")
    parser.add_argument("--confirm-approved", default="")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.write_approved_json:
        raise SystemExit(
            "STOP: add --write-approved-json only after reviewing the exact "
            "regional Teaching Vacancies summary."
        )
    if args.confirm_approved != APPROVAL_CONFIRMATION:
        raise SystemExit("STOP: approval confirmation must be exactly PUBLISH.")

    try:
        metadata, loaded, review_content, summary_content = (
            validate_review_for_approval(args.review_csv, args.summary_md)
        )
        rows = approved_output_rows(loaded, region=metadata.region)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    approved_path, evidence_path = default_output_paths(metadata.region)
    if args.approved_json:
        approved_path = args.approved_json
    if args.evidence_json:
        evidence_path = args.evidence_json

    snapshot_content = snapshot_bytes(rows)
    evidence_content = evidence_bytes(
        metadata=metadata,
        rows=rows,
        review_content=review_content,
        summary_content=summary_content,
        snapshot_content=snapshot_content,
    )
    discovery.write_bytes_atomic(approved_path, snapshot_content)
    discovery.write_bytes_atomic(evidence_path, evidence_content)
    print(
        f"Approved Teaching Vacancies regional snapshot wrote {len(rows)} open "
        f"selected jobs for {metadata.region} to {approved_path}; evidence: "
        f"{evidence_path}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

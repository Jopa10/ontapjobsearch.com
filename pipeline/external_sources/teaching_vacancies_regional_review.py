"""Generate region-aware Teaching Vacancies admin/service reviews.

This stage consumes verified routing evidence, classifies routed vacancies,
checks current regional JobG8 outputs, and writes separate CSV/Markdown reviews
for every encountered Ontap region. LIVE and CANDIDATE regions are both
reviewable; neither reviews nor migration reports publish jobs.

The completed West Yorkshire review can be migrated once. An old action is
carried forward only when its stable source ID and full material review facts
still match. Selected actions must also exist in the approved West Yorkshire
snapshot. Changed, new, expired or missing records are not silently approved.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

from external_sources import teaching_vacancies_approved as approved
from external_sources import teaching_vacancies_discovery as discovery
from external_sources import teaching_vacancies_poc as poc
from external_sources import teaching_vacancies_routing as routing
from external_sources.regional_contracts import clean, normalise

LONDON = ZoneInfo("Europe/London")
REVIEW_CONTRACT_VERSION = "teaching-vacancies-regional-review-v1"
SOURCE_CODE = "Teaching Vacancies"

REVIEW_FIELDS = (
    "final_decision",
    "title",
    "salary_text",
    "employer",
    "location",
    "posted_date",
    "closing_date",
    "classification",
    "classification_reason",
    "jobg8_check",
    "jobg8_candidate_title",
    "jobg8_candidate_employer",
    "jobg8_match_score",
    "employment_type",
    "ontap_region",
    "geo_cluster",
    "geography_status",
    "geography_reason",
    "geography_lookup_key",
    "slice_status",
    "publish_eligible",
    "source_job_id",
    "source_url",
    "manual_action",
    "migration_status",
    "factual_fingerprint",
    "discovery_routes",
    "source",
)

MIGRATION_FIELDS = (
    "source_job_id",
    "old_action",
    "migration_status",
    "detail",
)


@dataclass(frozen=True)
class LegacyDecision:
    source_job_id: str
    action: str
    decision: str
    region: str
    location: str
    salary_text: str
    title: str
    employer: str
    closing_date: str
    reason: str
    source_url: str


@dataclass
class ReviewRecord:
    vacancy: poc.Vacancy
    ontap_region: str
    geo_cluster: str
    geography_reason: str
    geography_lookup_key: str
    slice_status: str
    publish_eligible: str
    factual_fingerprint: str
    discovery_routes: str
    manual_action: str = ""
    migration_status: str = ""


def region_slug(region: str) -> str:
    """Follow existing Yorkshire naming while supporting arbitrary regions."""
    value = clean(region)
    match = re.fullmatch(r"Yorkshire\s*-\s*(West|South|North|East)", value, re.I)
    if match:
        return f"{match.group(1).casefold()}-yorkshire"
    if normalise(value) == "north east":
        return "north-east"
    if normalise(value) == "west midlands coventry warwickshire":
        return "coventry-warwickshire"
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    if not slug:
        raise ValueError("cannot create a regional output slug from a blank region")
    return slug


def review_paths(root: Path, region: str) -> tuple[Path, Path]:
    stem = f"{region_slug(region)}-admin-service"
    return root / f"{stem}-review.csv", root / f"{stem}-summary.md"


def load_verified_routing(
    routed_path: Path,
    summary_path: Path,
) -> tuple[list[dict[str, str]], dict[str, object]]:
    if not summary_path.is_file():
        raise ValueError(f"routing summary not found: {summary_path}")
    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("routing summary is not valid JSON") from exc
    if not isinstance(summary, dict):
        raise ValueError("routing summary must be a JSON object")
    if clean(summary.get("source")) != discovery.SOURCE_CODE:
        raise ValueError("routing summary has an unexpected source")
    content = routed_path.read_bytes()
    actual_sha = hashlib.sha256(content).hexdigest()
    if actual_sha != clean(summary.get("routed_csv_sha256")):
        raise ValueError("routed CSV SHA256 does not match its routing summary")
    with io.StringIO(content.decode("utf-8-sig"), newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != routing.ROUTING_FIELDS:
            raise ValueError("routed CSV columns do not match the routing contract")
        rows = [dict(row) for row in reader]
    if int(summary.get("records") or 0) != len(rows):
        raise ValueError("routed CSV count does not match its routing summary")
    return rows, summary


def load_jobg8_by_region(output_dir: Path) -> dict[str, list[dict]]:
    """Index current JobG8 rows without treating retained externals as JobG8."""
    output: dict[str, list[dict]] = defaultdict(list)
    if not output_dir.is_dir():
        return {}
    for path in sorted(output_dir.glob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"invalid admin/service output JSON: {path}") from exc
        if not isinstance(value, list):
            raise ValueError(f"admin/service output is not a list: {path}")
        for row in value:
            if not isinstance(row, dict):
                continue
            source = clean(row.get("source")).casefold()
            if source not in {"", "jobg8"}:
                continue
            region = clean(row.get("region"))
            if region:
                output[region].append(row)
    return dict(output)


def routed_row_to_vacancy(row: dict[str, str]) -> poc.Vacancy:
    return poc.Vacancy(
        source=discovery.SOURCE,
        source_job_id=clean(row.get("source_job_id")),
        title=clean(row.get("title")),
        employer=clean(row.get("employer")),
        location=clean(row.get("location")),
        salary_text=clean(row.get("salary_text")),
        posted_date=clean(row.get("posted_date")),
        closing_date=clean(row.get("closing_date")),
        employment_type=clean(row.get("employment_type")),
        description_excerpt=clean(row.get("description_excerpt")),
        source_url=clean(row.get("canonical_url")),
        geography_status="IN_SCOPE",
        geography_reason=clean(row.get("geography_reason")),
    )


def classify_routed_rows(
    rows: Iterable[dict[str, str]],
    *,
    jobg8_by_region: dict[str, list[dict]],
    now: datetime | None = None,
) -> list[ReviewRecord]:
    current = now or datetime.now(LONDON)
    output: list[ReviewRecord] = []
    for row in rows:
        if clean(row.get("geography_status")) != "ROUTED":
            continue
        region = clean(row.get("ontap_region"))
        if not region:
            raise ValueError("routed Teaching Vacancies row has no Ontap region")
        vacancy = routed_row_to_vacancy(row)
        vacancy.classification, vacancy.classification_reason = poc.classify(vacancy)
        (
            vacancy.jobg8_check,
            vacancy.jobg8_candidate_title,
            vacancy.jobg8_candidate_employer,
            vacancy.jobg8_match_score,
        ) = poc.compare_jobg8(vacancy, jobg8_by_region.get(region, []))
        if vacancy.jobg8_check == "DUPLICATE":
            vacancy.classification = "HARD_PASS"
            vacancy.classification_reason = "Confirmed JobG8 duplicate"
        elif (
            vacancy.jobg8_check == "POSSIBLE_DUPLICATE"
            and vacancy.classification != "HARD_PASS"
        ):
            vacancy.classification = "POSS"
            vacancy.classification_reason = (
                "Possible JobG8 duplicate requires review"
            )
        if not approved.vacancy_is_open(vacancy, now=current):
            vacancy.classification = "HARD_PASS"
            vacancy.classification_reason = "Expired, closed or invalid deadline"
        if vacancy.classification != "HARD_PASS" and not clean(vacancy.salary_text):
            vacancy.classification = "HARD_PASS"
            vacancy.classification_reason = "Missing salary or pay scale"
        output.append(
            ReviewRecord(
                vacancy=vacancy,
                ontap_region=region,
                geo_cluster=clean(row.get("geo_cluster")),
                geography_reason=clean(row.get("geography_reason")),
                geography_lookup_key=clean(row.get("geography_lookup_key")),
                slice_status=clean(row.get("slice_status")),
                publish_eligible=clean(row.get("publish_eligible")),
                factual_fingerprint=clean(row.get("factual_fingerprint")),
                discovery_routes=clean(row.get("discovery_routes")),
            )
        )
    return output


def decision_for(record: ReviewRecord) -> str:
    if record.vacancy.classification == "HARD_PASS":
        return "HARD_PASS"
    if record.manual_action == "exclude":
        return "EXCLUDED"
    if record.manual_action == "select":
        return "SELECTED"
    if record.vacancy.classification == "HC":
        return "SELECTED"
    return "POSS"


def review_fingerprint(records: Iterable[ReviewRecord]) -> str:
    payload = [
        {
            "source_job_id": row.vacancy.source_job_id,
            "factual_fingerprint": row.factual_fingerprint,
            "classification": row.vacancy.classification,
            "classification_reason": row.vacancy.classification_reason,
            "jobg8_check": row.vacancy.jobg8_check,
            "ontap_region": row.ontap_region,
            "slice_status": row.slice_status,
        }
        for row in records
        if row.vacancy.classification != "HARD_PASS"
    ]
    payload.sort(key=lambda row: row["source_job_id"])
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _block_value(block: str, key: str) -> str:
    # Horizontal whitespace only: a blank value must never absorb the next line.
    match = re.search(rf"(?mi)^{re.escape(key)}:[ \t]*(.*?)[ \t]*$", block)
    return clean(match.group(1)) if match else ""


def load_existing_actions(
    path: Path,
    *,
    review_date: str,
    current_by_id: dict[str, ReviewRecord],
) -> dict[str, str]:
    """Reuse same-day regional actions only for the same row fingerprint."""
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8-sig")
    date_match = re.search(r"(?mi)^review_date:\s*(\d{4}-\d{2}-\d{2})\s*$", text)
    if not date_match or date_match.group(1) != review_date:
        return {}
    actions: dict[str, str] = {}
    for block in re.findall(r"(?ms)^---\s*$\n(.*?)^---\s*$", text):
        source_job_id = _block_value(block, "source_job_id")
        action = _block_value(block, "action").casefold()
        fingerprint = _block_value(block, "factual_fingerprint")
        current = current_by_id.get(source_job_id)
        if (
            current
            and action in {"select", "exclude"}
            and fingerprint
            and fingerprint == current.factual_fingerprint
        ):
            actions[source_job_id] = action
    return actions


def parse_legacy_summary(path: Path) -> dict[str, LegacyDecision]:
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8-sig")
    output: dict[str, LegacyDecision] = {}
    for block in re.findall(r"(?ms)^---\s*$\n(.*?)^---\s*$", text):
        source_job_id = _block_value(block, "source_job_id")
        if not source_job_id:
            continue
        action = _block_value(block, "action").casefold()
        line_match = re.search(
            r"(?m)^(SELECTED|POSS|EXCLUDED|HARD_PASS)\s*\|\s*(.*?)$",
            block,
        )
        if not line_match:
            continue
        decision = line_match.group(1)
        parts = [clean(value) for value in line_match.group(2).split("|", 3)]
        if len(parts) != 4:
            continue
        region, location, salary_text, title = parts
        output[source_job_id] = LegacyDecision(
            source_job_id=source_job_id,
            action=action,
            decision=decision,
            region=region,
            location=location,
            salary_text=salary_text,
            title=title,
            employer=_block_value(block, "employer"),
            closing_date=_block_value(block, "closing_date"),
            reason=_block_value(block, "reason"),
            source_url=_block_value(block, "source_url").rstrip("/"),
        )
    return output


def load_approved_source_ids(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"legacy approved snapshot is invalid JSON: {path}") from exc
    if not isinstance(value, list):
        raise ValueError("legacy approved snapshot must be a JSON list")
    prefix = "teaching-vacancies-"
    return {
        clean(row.get("job_id"))[len(prefix) :]
        for row in value
        if isinstance(row, dict) and clean(row.get("job_id")).startswith(prefix)
    }


def legacy_match(record: ReviewRecord, legacy: LegacyDecision) -> tuple[bool, str]:
    vacancy = record.vacancy
    comparisons = (
        ("region", record.ontap_region, legacy.region),
        ("title", vacancy.title, legacy.title),
        ("employer", vacancy.employer, legacy.employer),
        ("location", vacancy.location, legacy.location),
        ("salary", vacancy.salary_text, legacy.salary_text),
        ("closing date", vacancy.closing_date, legacy.closing_date),
        ("classification reason", vacancy.classification_reason, legacy.reason),
        ("source URL", vacancy.source_url.rstrip("/"), legacy.source_url),
    )
    changed = [
        label
        for label, current, old in comparisons
        if normalise(current) != normalise(old)
    ]
    return (not changed, ", ".join(changed))


def migrate_legacy_west_yorkshire(
    records: list[ReviewRecord],
    *,
    legacy_summary_path: Path,
    legacy_approved_path: Path,
) -> list[dict[str, str]]:
    legacy = parse_legacy_summary(legacy_summary_path)
    approved_ids = load_approved_source_ids(legacy_approved_path)
    current_by_id = {row.vacancy.source_job_id: row for row in records}
    report: list[dict[str, str]] = []

    for source_job_id, old in sorted(legacy.items()):
        current = current_by_id.get(source_job_id)
        if not current:
            report.append(
                {
                    "source_job_id": source_job_id,
                    "old_action": old.action,
                    "migration_status": "NOT_CURRENT",
                    "detail": "Expired, closed, no longer discovered or routed elsewhere",
                }
            )
            continue
        if not old.action:
            report.append(
                {
                    "source_job_id": source_job_id,
                    "old_action": "",
                    "migration_status": "BLANK_POSS_PRESERVED",
                    "detail": "No decision migrated",
                }
            )
            current.migration_status = "BLANK_POSS_PRESERVED"
            continue
        matches, changed = legacy_match(current, old)
        if not matches:
            report.append(
                {
                    "source_job_id": source_job_id,
                    "old_action": old.action,
                    "migration_status": "REVIEW_REQUIRED",
                    "detail": "Material fields changed: " + changed,
                }
            )
            current.migration_status = "REVIEW_REQUIRED"
            continue
        if old.action == "select" and source_job_id not in approved_ids:
            report.append(
                {
                    "source_job_id": source_job_id,
                    "old_action": old.action,
                    "migration_status": "REVIEW_REQUIRED",
                    "detail": "Old selection is absent from the approved snapshot",
                }
            )
            current.migration_status = "REVIEW_REQUIRED"
            continue
        current.manual_action = old.action
        current.migration_status = "MIGRATED_UNCHANGED"
        report.append(
            {
                "source_job_id": source_job_id,
                "old_action": old.action,
                "migration_status": "MIGRATED_UNCHANGED",
                "detail": "Stable ID and full material review facts match",
            }
        )

    for source_job_id, current in sorted(current_by_id.items()):
        if source_job_id in legacy:
            continue
        current.migration_status = "NEW_REVIEW"
        report.append(
            {
                "source_job_id": source_job_id,
                "old_action": "",
                "migration_status": "NEW_REVIEW",
                "detail": "New regional vacancy or newly reviewable record",
            }
        )
    return report


def apply_existing_actions(
    records: list[ReviewRecord],
    *,
    summary_path: Path,
    review_date: str,
) -> None:
    current_by_id = {row.vacancy.source_job_id: row for row in records}
    actions = load_existing_actions(
        summary_path,
        review_date=review_date,
        current_by_id=current_by_id,
    )
    for source_job_id, action in actions.items():
        record = current_by_id[source_job_id]
        if (
            action == "select"
            and record.vacancy.jobg8_check == "POSSIBLE_DUPLICATE"
        ):
            if not record.migration_status:
                record.migration_status = "REVIEW_REQUIRED_DUPLICATE"
            continue
        record.manual_action = action
        if not record.migration_status:
            record.migration_status = "SAME_DAY_ACTION"


def review_row(record: ReviewRecord) -> dict[str, str]:
    vacancy = record.vacancy
    plausible = vacancy.jobg8_check in {"DUPLICATE", "POSSIBLE_DUPLICATE"}
    return {
        "final_decision": decision_for(record),
        "title": vacancy.title,
        "salary_text": vacancy.salary_text,
        "employer": vacancy.employer,
        "location": vacancy.location,
        "posted_date": vacancy.posted_date,
        "closing_date": vacancy.closing_date,
        "classification": vacancy.classification,
        "classification_reason": vacancy.classification_reason,
        "jobg8_check": vacancy.jobg8_check if plausible else "No plausible JobG8 match",
        "jobg8_candidate_title": vacancy.jobg8_candidate_title if plausible else "",
        "jobg8_candidate_employer": vacancy.jobg8_candidate_employer if plausible else "",
        "jobg8_match_score": vacancy.jobg8_match_score if plausible else "",
        "employment_type": vacancy.employment_type,
        "ontap_region": record.ontap_region,
        "geo_cluster": record.geo_cluster,
        "geography_status": "ROUTED",
        "geography_reason": record.geography_reason,
        "geography_lookup_key": record.geography_lookup_key,
        "slice_status": record.slice_status,
        "publish_eligible": record.publish_eligible,
        "source_job_id": vacancy.source_job_id,
        "source_url": vacancy.source_url,
        "manual_action": record.manual_action,
        "migration_status": record.migration_status,
        "factual_fingerprint": record.factual_fingerprint,
        "discovery_routes": record.discovery_routes,
        "source": SOURCE_CODE,
    }


def review_csv_bytes(records: Iterable[ReviewRecord]) -> bytes:
    rows = sorted(
        (review_row(row) for row in records),
        key=lambda row: (
            {"SELECTED": 0, "POSS": 1, "EXCLUDED": 2, "HARD_PASS": 3}.get(
                row["final_decision"], 9
            ),
            row["title"].casefold(),
            row["source_job_id"],
        ),
    )
    handle = io.StringIO(newline="")
    writer = csv.DictWriter(handle, fieldnames=REVIEW_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue().encode("utf-8")


def migration_csv_bytes(rows: Iterable[dict[str, str]]) -> bytes:
    handle = io.StringIO(newline="")
    writer = csv.DictWriter(handle, fieldnames=MIGRATION_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue().encode("utf-8")


def markdown_summary(
    region: str,
    records: list[ReviewRecord],
    *,
    review_date: str,
    routing_manifest_sha256: str,
) -> str:
    status = records[0].slice_status if records else "UNREGISTERED"
    counts = Counter(decision_for(row) for row in records)
    lines = [
        f"# Teaching Vacancies regional review — {region}",
        "",
        f"review_date: {review_date}",
        f"review_fingerprint: {review_fingerprint(records)}",
        f"routing_manifest_sha256: {routing_manifest_sha256}",
        f"ontap_region: {region}",
        "slice_category: admin_service",
        f"slice_status: {status}",
        "",
        "Edit only the `action:` line in each editable block.",
        "Blank POSS decisions remain unpublished.",
        "CANDIDATE and UNREGISTERED slices remain unpublished regardless of actions.",
        "",
        "## Counts",
        "",
        f"- Records: {len(records)}",
        f"- Selected: {counts['SELECTED']}",
        f"- POSS awaiting decision: {counts['POSS']}",
        f"- Excluded: {counts['EXCLUDED']}",
        f"- Hard pass: {counts['HARD_PASS']}",
        "",
    ]
    sections = (
        ("SELECTED", "SELECTED"),
        ("POSS — choose SELECT or EXCLUDE", "POSS"),
        ("EXCLUDED BY REVIEW", "EXCLUDED"),
    )
    for heading, decision in sections:
        lines.extend([f"## {heading}", ""])
        selected = [row for row in records if decision_for(row) == decision]
        if not selected:
            lines.extend(["- None.", ""])
            continue
        for row in sorted(selected, key=lambda item: item.vacancy.title.casefold()):
            vacancy = row.vacancy
            lines.extend(
                [
                    "---",
                    f"action: {row.manual_action}",
                    (
                        f"{decision} | {region} | {vacancy.location} | "
                        f"{vacancy.salary_text} | {vacancy.title}"
                    ),
                    f"employer: {vacancy.employer}",
                    f"closing_date: {vacancy.closing_date}",
                    f"reason: {vacancy.classification_reason}",
                    f"jobg8_check: {vacancy.jobg8_check}",
                    f"slice_status: {row.slice_status}",
                    f"migration_status: {row.migration_status}",
                    f"factual_fingerprint: {row.factual_fingerprint}",
                    f"source: {SOURCE_CODE}",
                    f"source_job_id: {vacancy.source_job_id}",
                    f"source_url: {vacancy.source_url}",
                    "---",
                    "",
                ]
            )
    lines.extend(["## HARD_PASS", ""])
    hard = [row for row in records if decision_for(row) == "HARD_PASS"]
    if not hard:
        lines.append("- None.")
    else:
        lines.extend(
            f"- [{row.vacancy.title}]({row.vacancy.source_url}) — "
            f"{row.vacancy.classification_reason}."
            for row in sorted(hard, key=lambda item: item.vacancy.title.casefold())
        )
    lines.extend(
        [
            "",
            "## Safety boundary",
            "",
            "- This file is a review artifact only.",
            "- It does not write approved snapshots, combined outputs or app JSON.",
            "- LIVE/CANDIDATE status comes only from the existing slice register.",
            "- Geography comes only from the existing geographic lookup contract.",
            "",
        ]
    )
    return "\n".join(lines)


def group_by_region(records: Iterable[ReviewRecord]) -> dict[str, list[ReviewRecord]]:
    output: dict[str, list[ReviewRecord]] = defaultdict(list)
    for row in records:
        output[row.ontap_region].append(row)
    return dict(sorted(output.items()))


def prune_stale_review_outputs(
    review_dir: Path,
    *,
    active_regions: Iterable[str],
) -> list[Path]:
    """Remove generated regional pairs that are absent from the current routing."""
    expected: set[Path] = set()
    for region in active_regions:
        expected.update(review_paths(review_dir, region))

    removed: list[Path] = []
    for pattern in (
        "*-admin-service-review.csv",
        "*-admin-service-summary.md",
    ):
        for path in sorted(review_dir.glob(pattern)):
            if path.name.startswith("england-wide-admin-service-"):
                continue
            if path in expected:
                continue
            path.unlink()
            removed.append(path)
    return removed


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--routed-csv", type=Path, required=True)
    parser.add_argument("--routing-summary-json", type=Path, required=True)
    parser.add_argument(
        "--jobg8-output-dir",
        type=Path,
        default=Path("output-admin-service"),
    )
    parser.add_argument(
        "--review-dir",
        type=Path,
        default=Path("reviews/external/teaching-vacancies"),
    )
    parser.add_argument(
        "--legacy-west-summary",
        type=Path,
        default=Path("reviews/external/west-yorkshire-teaching-vacancies-summary.md"),
    )
    parser.add_argument(
        "--legacy-west-approved",
        type=Path,
        default=Path("output-external/west-yorkshire-teaching-vacancies-admin-service.json"),
    )
    parser.add_argument(
        "--migration-report",
        type=Path,
        default=Path("reviews/external/teaching-vacancies/west-yorkshire-migration.csv"),
    )
    parser.add_argument("--write-reviews", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.write_reviews:
        raise SystemExit("STOP: add --write-reviews to create review-only outputs.")
    routed_rows, routing_summary = load_verified_routing(
        args.routed_csv,
        args.routing_summary_json,
    )
    records = classify_routed_rows(
        routed_rows,
        jobg8_by_region=load_jobg8_by_region(args.jobg8_output_dir),
    )
    grouped = group_by_region(records)
    stale_outputs = prune_stale_review_outputs(
        args.review_dir,
        active_regions=grouped,
    )
    review_date = clean(routing_summary.get("run_date"))
    migration_rows: list[dict[str, str]] = []

    for region, region_records in grouped.items():
        csv_path, summary_path = review_paths(args.review_dir, region)
        if region == "Yorkshire - West":
            migration_rows = migrate_legacy_west_yorkshire(
                region_records,
                legacy_summary_path=args.legacy_west_summary,
                legacy_approved_path=args.legacy_west_approved,
            )
        apply_existing_actions(
            region_records,
            summary_path=summary_path,
            review_date=review_date,
        )
        discovery.write_bytes_atomic(csv_path, review_csv_bytes(region_records))
        discovery.write_bytes_atomic(
            summary_path,
            markdown_summary(
                region,
                region_records,
                review_date=review_date,
                routing_manifest_sha256=clean(
                    routing_summary.get("routed_csv_sha256")
                ),
            ).encode("utf-8"),
        )

    if migration_rows:
        discovery.write_bytes_atomic(
            args.migration_report,
            migration_csv_bytes(migration_rows),
        )
    print(
        f"Teaching Vacancies regional review wrote {len(grouped)} regional "
        f"review sets for {len(records)} routed records; removed "
        f"{len(stale_outputs)} stale regional output file(s); no jobs were published."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

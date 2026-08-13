"""Compose approved regional Teaching Vacancies snapshots with current outputs.

The composer is region-neutral. It discovers current admin/service output files
from their row-level region, verifies separately approved Teaching Vacancies
snapshots and evidence, and replaces only the Teaching Vacancies subset.

Safety rules:
* the existing slice register must say LIVE;
* approved snapshot evidence and hashes must reconcile;
* a current output must contain at least one non-Teaching-Vacancies base row;
* missing snapshots leave current outputs unchanged;
* empty or external-only overwrites are blocked;
* legacy West Yorkshire and North East compositors remain available for rollback.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

from external_sources.compose_northeast_admin import (
    closing_date_is_live,
    factual_fingerprint,
    load_rows,
    normalise,
    text,
    write_json_atomic,
)
from external_sources.regional_contracts import (
    CATEGORY_ADMIN_SERVICE,
    load_slice_authorities,
    publishable_region,
)
from external_sources.teaching_vacancies_regional_approved import (
    APPROVAL_CONTRACT_VERSION,
    DEFAULT_EVIDENCE_DIR,
    DEFAULT_OUTPUT_DIR,
)

SOURCE = "Teaching Vacancies"
JOB_ID_PREFIX = "teaching-vacancies-"
DEFAULT_CURRENT_OUTPUT_DIR = Path("output-admin-service")
DEFAULT_SLICE_REGISTER = Path("registers/region_category_slice_register.csv")
ADMIN_SERVICE_OUTPUT_GLOB = "*-admin-service.json"
_GENERIC_EMPLOYER_TOKENS = {
    "academy",
    "college",
    "company",
    "council",
    "limited",
    "ltd",
    "school",
    "the",
    "trust",
    "university",
}


@dataclass(frozen=True)
class ApprovedSnapshot:
    region: str
    rows: tuple[dict[str, Any], ...]
    snapshot_path: Path
    evidence_path: Path


@dataclass
class CompositionResult:
    path: Path
    region: str
    status: str
    reason: str
    base_rows: int = 0
    teaching_rows: int = 0
    expired_skipped: int = 0
    duplicate_skipped: int = 0
    total: int = 0


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def validate_teaching_row(row: dict[str, Any], *, region: str) -> None:
    required = (
        "job_id",
        "title",
        "company",
        "location",
        "region",
        "description",
        "apply_url",
        "source",
        "closing_date",
    )
    missing = [field for field in required if not text(row.get(field))]
    if missing:
        raise ValueError(
            f"Teaching Vacancies row {text(row.get('job_id')) or '<unknown>'} "
            f"is missing: {', '.join(missing)}"
        )
    if text(row.get("source")) != SOURCE:
        raise ValueError("approved snapshot contains a non-Teaching-Vacancies row")
    if text(row.get("region")) != region:
        raise ValueError(
            f"approved Teaching Vacancies row region differs from {region}: "
            f"{row.get('region')!r}"
        )
    if not text(row.get("job_id")).startswith(JOB_ID_PREFIX):
        raise ValueError(
            f"Teaching Vacancies row has invalid job_id: {row.get('job_id')!r}"
        )


def evidence_path_for(snapshot_path: Path, evidence_dir: Path) -> Path:
    return evidence_dir / f"{snapshot_path.stem}-evidence.json"


def load_approved_snapshot(
    snapshot_path: Path,
    *,
    evidence_dir: Path,
) -> ApprovedSnapshot:
    rows = load_rows(snapshot_path, required=True)
    evidence_path = evidence_path_for(snapshot_path, evidence_dir)
    if not evidence_path.is_file():
        raise ValueError(f"approved snapshot evidence does not exist: {evidence_path}")
    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"approved snapshot evidence is invalid JSON: {evidence_path}") from exc
    if not isinstance(evidence, dict):
        raise ValueError("approved snapshot evidence must be a JSON object")
    if text(evidence.get("contract_version")) != APPROVAL_CONTRACT_VERSION:
        raise ValueError("approved snapshot evidence has an unexpected contract version")
    if text(evidence.get("source")) != SOURCE:
        raise ValueError("approved snapshot evidence has an unexpected source")
    if text(evidence.get("category")) != CATEGORY_ADMIN_SERVICE:
        raise ValueError("approved snapshot evidence has an unexpected category")
    if text(evidence.get("slice_status")) != "LIVE":
        raise ValueError("approved snapshot evidence is not for a LIVE slice")

    snapshot_content = snapshot_path.read_bytes()
    actual_sha = hashlib.sha256(snapshot_content).hexdigest()
    if actual_sha != text(evidence.get("approved_snapshot_sha256")):
        raise ValueError("approved snapshot SHA256 differs from its evidence")
    if int(evidence.get("approved_rows") or 0) != len(rows):
        raise ValueError("approved snapshot count differs from its evidence")

    region = text(evidence.get("region"))
    if not region:
        raise ValueError("approved snapshot evidence has no region")
    job_ids = [text(row.get("job_id")) for row in rows]
    evidence_ids = [text(value) for value in evidence.get("approved_job_ids", [])]
    if job_ids != evidence_ids:
        raise ValueError("approved snapshot job IDs differ from its evidence")
    if len(job_ids) != len(set(job_ids)):
        raise ValueError("approved snapshot contains duplicate job IDs")
    for row in rows:
        validate_teaching_row(row, region=region)
    return ApprovedSnapshot(
        region=region,
        rows=tuple(dict(row) for row in rows),
        snapshot_path=snapshot_path,
        evidence_path=evidence_path,
    )


def load_approved_snapshots(
    snapshot_dir: Path,
    *,
    evidence_dir: Path,
) -> dict[str, ApprovedSnapshot]:
    output: dict[str, ApprovedSnapshot] = {}
    if not snapshot_dir.is_dir():
        return output
    for path in sorted(snapshot_dir.glob("*.json")):
        snapshot = load_approved_snapshot(path, evidence_dir=evidence_dir)
        if snapshot.region in output:
            raise ValueError(
                f"more than one approved Teaching Vacancies snapshot for "
                f"{snapshot.region}"
            )
        output[snapshot.region] = snapshot
    return output


def current_base_contract(
    current_rows: list[dict[str, Any]],
) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    teaching = [
        dict(row)
        for row in current_rows
        if text(row.get("source")).casefold() == SOURCE.casefold()
    ]
    base = [
        dict(row)
        for row in current_rows
        if text(row.get("source")).casefold() != SOURCE.casefold()
    ]
    if not base:
        return "", base, teaching
    regions = {text(row.get("region")) for row in base if text(row.get("region"))}
    if len(regions) != 1:
        raise ValueError(
            "current admin/service output has blank or mixed base-row regions"
        )
    if any(not text(row.get("job_id")) for row in base):
        raise ValueError("current admin/service base row has no job_id")
    return next(iter(regions)), base, teaching


def _distinctive_employer(value: object) -> str:
    """Return a company label only when it is specific enough for dedupe."""
    normalised = normalise(value)
    tokens = [
        token
        for token in normalised.split()
        if len(token) > 2 and token not in _GENERIC_EMPLOYER_TOKENS
    ]
    return normalised if len(tokens) >= 3 else ""


def likely_same_cross_source_vacancy(
    left: dict[str, Any],
    right: dict[str, Any],
) -> bool:
    """Conservatively catch provider naming differences for the same vacancy.

    This intentionally requires the same title and closing day plus a distinctive
    employer from one source appearing explicitly in the other source's company
    or location text. It handles school-vs-academy-trust attribution without
    broadly fuzzy-matching ordinary same-title jobs in the same town.
    """
    if normalise(left.get("title")) != normalise(right.get("title")):
        return False
    left_close = text(left.get("closing_date"))
    right_close = text(right.get("closing_date"))
    if not left_close or left_close != right_close:
        return False

    left_company = _distinctive_employer(left.get("company"))
    right_company = _distinctive_employer(right.get("company"))
    left_context = normalise(
        f"{text(left.get('company'))} {text(left.get('location'))}"
    )
    right_context = normalise(
        f"{text(right.get('company'))} {text(right.get('location'))}"
    )
    return bool(
        (left_company and left_company in right_context)
        or (right_company and right_company in left_context)
    )


def compose_rows(
    current_output: list[dict[str, Any]],
    approved_teaching: list[dict[str, Any]],
    *,
    region: str,
    today: date,
    now: datetime | None = None,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    actual_region, base_rows, _old_teaching = current_base_contract(current_output)
    if not base_rows:
        raise ValueError(
            "external-only overwrite blocked: current output has no JobG8/other base rows"
        )
    if actual_region != region:
        raise ValueError(
            f"current output region {actual_region!r} differs from snapshot {region!r}"
        )

    occupied_ids = {text(row.get("job_id")) for row in base_rows}
    occupied_fingerprints = {factual_fingerprint(row) for row in base_rows}
    accepted: list[dict[str, Any]] = []
    seen_source_ids: set[str] = set()
    expired = 0
    duplicates = 0

    for source_row in approved_teaching:
        row = dict(source_row)
        validate_teaching_row(row, region=region)
        job_id = text(row.get("job_id"))
        if job_id in seen_source_ids:
            raise ValueError(f"duplicate approved Teaching Vacancies job_id: {job_id}")
        seen_source_ids.add(job_id)
        if not closing_date_is_live(row, today=today, now=now):
            expired += 1
            continue
        fingerprint = factual_fingerprint(row)
        if (
            job_id in occupied_ids
            or fingerprint in occupied_fingerprints
            or any(
                likely_same_cross_source_vacancy(row, base_row)
                for base_row in base_rows
            )
        ):
            duplicates += 1
            continue
        accepted.append(row)
        occupied_ids.add(job_id)
        occupied_fingerprints.add(fingerprint)

    accepted.sort(
        key=lambda row: (
            text(row.get("closing_date")),
            text(row.get("title")).casefold(),
            text(row.get("job_id")),
        )
    )
    result = accepted + base_rows
    result_ids = [text(row.get("job_id")) for row in result]
    if not result:
        raise ValueError("empty output overwrite blocked")
    if len(result) == len(accepted):
        raise ValueError("external-only output overwrite blocked")
    if any(not value for value in result_ids):
        raise ValueError("composed output contains a row without job_id")
    if len(result_ids) != len(set(result_ids)):
        raise ValueError("composed output contains duplicate job IDs")
    return result, {
        "base_rows": len(base_rows),
        "teaching_vacancies": len(accepted),
        "expired_teaching_vacancies_skipped": expired,
        "duplicate_teaching_vacancies_skipped": duplicates,
        "total": len(result),
    }


def canonical_rows(rows: list[dict[str, Any]]) -> bytes:
    return json.dumps(
        rows,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def compose_directory(
    *,
    current_output_dir: Path,
    snapshot_dir: Path,
    evidence_dir: Path,
    slice_register: Path,
    today: date,
    now: datetime | None = None,
    write: bool = False,
    regions: set[str] | None = None,
) -> list[CompositionResult]:
    authorities = load_slice_authorities(slice_register)
    snapshots = load_approved_snapshots(
        snapshot_dir,
        evidence_dir=evidence_dir,
    )
    results: list[CompositionResult] = []
    matched_regions: set[str] = set()

    if not current_output_dir.is_dir():
        raise ValueError(f"current output directory does not exist: {current_output_dir}")
    for path in sorted(current_output_dir.glob(ADMIN_SERVICE_OUTPUT_GLOB)):
        current = load_rows(path, required=True)
        if not current:
            results.append(
                CompositionResult(
                    path=path,
                    region="",
                    status="SKIPPED",
                    reason="current output is empty; empty overwrite blocked",
                )
            )
            continue
        region, base_rows, old_teaching = current_base_contract(current)
        if regions is not None and region not in regions:
            results.append(
                CompositionResult(
                    path=path,
                    region=region,
                    status="SKIPPED",
                    reason="region was not requested for this composition run",
                    base_rows=len(base_rows),
                    teaching_rows=len(old_teaching),
                    total=len(current),
                )
            )
            continue
        if not base_rows:
            results.append(
                CompositionResult(
                    path=path,
                    region=text(old_teaching[0].get("region")) if old_teaching else "",
                    status="SKIPPED",
                    reason="no JobG8/other base rows; external-only overwrite blocked",
                    teaching_rows=len(old_teaching),
                    total=len(current),
                )
            )
            continue
        if not publishable_region(
            authorities,
            region=region,
            category=CATEGORY_ADMIN_SERVICE,
        ):
            results.append(
                CompositionResult(
                    path=path,
                    region=region,
                    status="SKIPPED",
                    reason="slice is not LIVE in region_category_slice_register.csv",
                    base_rows=len(base_rows),
                    teaching_rows=len(old_teaching),
                    total=len(current),
                )
            )
            continue
        snapshot = snapshots.get(region)
        if snapshot is None:
            results.append(
                CompositionResult(
                    path=path,
                    region=region,
                    status="SKIPPED",
                    reason="no approved regional Teaching Vacancies snapshot; current output retained",
                    base_rows=len(base_rows),
                    teaching_rows=len(old_teaching),
                    total=len(current),
                )
            )
            continue
        matched_regions.add(region)
        composed, counts = compose_rows(
            current,
            list(snapshot.rows),
            region=region,
            today=today,
            now=now,
        )
        changed = canonical_rows(current) != canonical_rows(composed)
        if write and changed:
            write_json_atomic(path, composed)
        results.append(
            CompositionResult(
                path=path,
                region=region,
                status="WRITTEN" if write and changed else "WOULD_WRITE" if changed else "UNCHANGED",
                reason="approved snapshot composed with preserved JobG8/other base rows",
                base_rows=counts["base_rows"],
                teaching_rows=counts["teaching_vacancies"],
                expired_skipped=counts[
                    "expired_teaching_vacancies_skipped"
                ],
                duplicate_skipped=counts[
                    "duplicate_teaching_vacancies_skipped"
                ],
                total=counts["total"],
            )
        )

    for region, snapshot in sorted(snapshots.items()):
        if regions is not None and region not in regions:
            continue
        if region in matched_regions:
            continue
        results.append(
            CompositionResult(
                path=snapshot.snapshot_path,
                region=region,
                status="SKIPPED",
                reason="approved snapshot has no non-empty current regional base output",
                teaching_rows=len(snapshot.rows),
                total=len(snapshot.rows),
            )
        )
    return results


def format_report(results: list[CompositionResult]) -> str:
    lines = [
        "# Teaching Vacancies regional composition",
        "",
        "| Region | File | Status | Base | Teaching | Expired | Duplicate | Total | Reason |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in results:
        lines.append(
            f"| {row.region or '-'} | `{row.path}` | {row.status} | "
            f"{row.base_rows} | {row.teaching_rows} | {row.expired_skipped} | "
            f"{row.duplicate_skipped} | {row.total} | {row.reason} |"
        )
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--current-output-dir",
        type=Path,
        default=DEFAULT_CURRENT_OUTPUT_DIR,
    )
    parser.add_argument("--snapshot-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--evidence-dir", type=Path, default=DEFAULT_EVIDENCE_DIR)
    parser.add_argument(
        "--slice-register",
        type=Path,
        default=DEFAULT_SLICE_REGISTER,
    )
    parser.add_argument(
        "--region",
        action="append",
        default=[],
        help="Compose only this exact Ontap region; may be repeated.",
    )
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    parser.add_argument("--write", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        results = compose_directory(
            current_output_dir=args.current_output_dir,
            snapshot_dir=args.snapshot_dir,
            evidence_dir=args.evidence_dir,
            slice_register=args.slice_register,
            today=args.today,
            write=args.write,
            regions=set(args.region) if args.region else None,
        )
    except ValueError as exc:
        raise SystemExit(f"STOP: {exc}") from exc
    print(format_report(results), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
"""Compose approved Teaching Vacancies with West Yorkshire JobG8 output."""

from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
from typing import Any

from external_sources.compose_northeast_admin import (
    closing_date_is_live,
    factual_fingerprint,
    load_rows,
    text,
    write_json_atomic,
)

DEFAULT_JOBG8_OUTPUT = Path(
    "output-admin-service/west-yorkshire-admin-service.json"
)
DEFAULT_TEACHING_OUTPUT = Path(
    "output-external/west-yorkshire-teaching-vacancies-admin-service.json"
)
SOURCE = "Teaching Vacancies"
JOB_ID_PREFIX = "teaching-vacancies-"
REGION = "Yorkshire - West"


def validate_teaching_row(row: dict[str, Any]) -> None:
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
    if row["source"] != SOURCE:
        raise ValueError(
            f"Teaching Vacancies row has unexpected source: {row['source']!r}"
        )
    if row["region"] != REGION:
        raise ValueError(
            f"Teaching Vacancies row has unexpected region: {row['region']!r}"
        )
    if not text(row["job_id"]).startswith(JOB_ID_PREFIX):
        raise ValueError(
            f"Teaching Vacancies row has invalid job_id: {row['job_id']!r}"
        )


def compose_rows(
    current_output: list[dict[str, Any]],
    approved_teaching: list[dict[str, Any]],
    *,
    today: date,
    now: datetime | None = None,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Replace the previous snapshot while preserving current non-source jobs."""
    base_rows = [
        dict(row)
        for row in current_output
        if text(row.get("source")).casefold() != SOURCE.casefold()
    ]
    occupied_ids = {text(row.get("job_id")) for row in base_rows}
    occupied_fingerprints = {factual_fingerprint(row) for row in base_rows}

    accepted: list[dict[str, Any]] = []
    seen_source_ids: set[str] = set()
    expired = 0
    duplicates = 0

    for source_row in approved_teaching:
        row = dict(source_row)
        validate_teaching_row(row)
        job_id = text(row["job_id"])
        if job_id in seen_source_ids:
            raise ValueError(
                f"duplicate approved Teaching Vacancies job_id: {job_id}"
            )
        seen_source_ids.add(job_id)

        if not closing_date_is_live(row, today=today, now=now):
            expired += 1
            continue
        fingerprint = factual_fingerprint(row)
        if job_id in occupied_ids or fingerprint in occupied_fingerprints:
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
    if any(not job_id for job_id in result_ids):
        raise ValueError("composed output contains a row without job_id")
    if len(result_ids) != len(set(result_ids)):
        raise ValueError("composed output contains duplicate job_id values")

    return result, {
        "jobg8_or_other": len(base_rows),
        "teaching_vacancies": len(accepted),
        "expired_teaching_vacancies_skipped": expired,
        "duplicate_teaching_vacancies_skipped": duplicates,
        "total": len(result),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--jobg8-output",
        type=Path,
        default=DEFAULT_JOBG8_OUTPUT,
    )
    parser.add_argument(
        "--teaching-output",
        type=Path,
        default=DEFAULT_TEACHING_OUTPUT,
    )
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    current = load_rows(args.jobg8_output, required=True)
    approved = load_rows(args.teaching_output, required=False)
    composed, counts = compose_rows(
        current,
        approved,
        today=args.today,
    )

    action = "would write"
    if args.write:
        write_json_atomic(args.jobg8_output, composed)
        action = "wrote"
    print(
        f"West Yorkshire admin composition {action} {counts['total']} jobs: "
        f"{counts['jobg8_or_other']} JobG8/other + "
        f"{counts['teaching_vacancies']} Teaching Vacancies; "
        f"{counts['expired_teaching_vacancies_skipped']} expired and "
        f"{counts['duplicate_teaching_vacancies_skipped']} duplicate "
        "Teaching Vacancies skipped."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

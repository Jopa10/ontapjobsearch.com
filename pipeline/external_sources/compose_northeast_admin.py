"""Compose approved NEJobs vacancies with the current JobG8 North East output."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from datetime import date, datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


DEFAULT_JOBG8_OUTPUT = Path(
    "output-admin-service/north-east-admin-service.json"
)
DEFAULT_NEJOBS_OUTPUT = Path(
    "output-external/northeast-jobs-admin-service.json"
)
NEJOBS_SOURCE = "NEJobs"


def text(value: object) -> str:
    return str(value or "").strip()


def normalise(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text(value).casefold()).strip()


def load_rows(path: Path, *, required: bool) -> list[dict[str, Any]]:
    if not path.exists():
        if required:
            raise ValueError(f"required JSON does not exist: {path}")
        return []
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        raise ValueError(f"JSON must be an array of objects: {path}")
    return data


def closing_date_is_live(
    row: dict[str, Any],
    *,
    today: date,
    now: datetime | None = None,
) -> bool:
    deadline_text = text(row.get("closing_datetime"))
    if deadline_text:
        try:
            deadline = datetime.fromisoformat(deadline_text)
        except ValueError:
            return False
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=ZoneInfo("Europe/London"))
        london_deadline = deadline.astimezone(ZoneInfo("Europe/London"))
        if london_deadline.date() < today:
            return False
        if london_deadline.date() > today:
            return True
        if now is not None or today == date.today():
            current = now or datetime.now(ZoneInfo("Europe/London"))
            if current.tzinfo is None:
                current = current.replace(tzinfo=ZoneInfo("Europe/London"))
            return london_deadline >= current.astimezone(
                ZoneInfo("Europe/London")
            )
        return True

    raw = text(row.get("closing_date"))
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
        return False
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date() >= today
    except ValueError:
        return False


def factual_fingerprint(row: dict[str, Any]) -> tuple[str, str, str]:
    return (
        normalise(row.get("title")),
        normalise(row.get("company")),
        normalise(row.get("location")),
    )


def validate_nejobs_row(row: dict[str, Any]) -> None:
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
            f"NEJobs row {text(row.get('job_id')) or '<unknown>'} "
            f"is missing: {', '.join(missing)}"
        )
    if row["source"] != NEJOBS_SOURCE:
        raise ValueError(f"external row has unexpected source: {row['source']!r}")
    if row["region"] != "North East":
        raise ValueError(f"external row has unexpected region: {row['region']!r}")
    if not text(row["job_id"]).startswith("nejobs-"):
        raise ValueError(f"external row has invalid job_id: {row['job_id']!r}")


def compose_rows(
    current_output: list[dict[str, Any]],
    approved_nejobs: list[dict[str, Any]],
    *,
    today: date,
    now: datetime | None = None,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Replace the previous NEJobs subset while preserving other suppliers."""
    base_rows = [
        dict(row)
        for row in current_output
        if text(row.get("source")).casefold() != NEJOBS_SOURCE.casefold()
    ]
    base_ids = {text(row.get("job_id")) for row in base_rows}
    base_fingerprints = {factual_fingerprint(row) for row in base_rows}

    external_rows: list[dict[str, Any]] = []
    seen_external_ids: set[str] = set()
    skipped_expired = 0
    skipped_duplicate = 0
    for source_row in approved_nejobs:
        row = dict(source_row)
        validate_nejobs_row(row)
        job_id = text(row["job_id"])
        if job_id in seen_external_ids:
            raise ValueError(f"duplicate approved NEJobs job_id: {job_id}")
        seen_external_ids.add(job_id)

        if not closing_date_is_live(row, today=today, now=now):
            skipped_expired += 1
            continue
        if job_id in base_ids or factual_fingerprint(row) in base_fingerprints:
            skipped_duplicate += 1
            continue
        external_rows.append(row)

    external_rows.sort(
        key=lambda row: (
            text(row.get("closing_date")),
            text(row.get("title")).casefold(),
            text(row.get("job_id")),
        )
    )
    result = external_rows + base_rows

    result_ids = [text(row.get("job_id")) for row in result]
    if any(not job_id for job_id in result_ids):
        raise ValueError("composed output contains a row without job_id")
    if len(result_ids) != len(set(result_ids)):
        raise ValueError("composed output contains duplicate job_id values")

    return result, {
        "jobg8_or_other": len(base_rows),
        "nejobs": len(external_rows),
        "expired_nejobs_skipped": skipped_expired,
        "duplicate_nejobs_skipped": skipped_duplicate,
        "total": len(result),
    }


def write_json_atomic(path: Path, rows: list[dict[str, Any]]) -> None:
    content = json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    handle, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as temp:
            temp.write(content)
            temp.flush()
            os.fsync(temp.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobg8-output", type=Path, default=DEFAULT_JOBG8_OUTPUT)
    parser.add_argument("--nejobs-output", type=Path, default=DEFAULT_NEJOBS_OUTPUT)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    current = load_rows(args.jobg8_output, required=True)
    approved = load_rows(args.nejobs_output, required=False)
    composed, counts = compose_rows(current, approved, today=args.today)

    action = "would write"
    if args.write:
        write_json_atomic(args.jobg8_output, composed)
        action = "wrote"
    print(
        f"North East admin composition {action} {counts['total']} jobs: "
        f"{counts['jobg8_or_other']} JobG8/other + {counts['nejobs']} NEJobs; "
        f"{counts['expired_nejobs_skipped']} expired and "
        f"{counts['duplicate_nejobs_skipped']} duplicate NEJobs skipped."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

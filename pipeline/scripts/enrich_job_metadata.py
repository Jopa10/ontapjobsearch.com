"""Attach factual JobG8 metadata to final pipeline JSON before publication.

The selection pipelines deliberately remain focused on eligibility and ranking.
This bounded post-processing step preserves source fields that are already in
the daily JobG8 feed but were previously discarded from the published JSON.
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = REPO_ROOT / "pipeline" / "input"
OUTPUT_DIRECTORIES = {
    "admin-service": REPO_ROOT / "pipeline" / "output-admin-service",
    "support-worker": REPO_ROOT / "pipeline" / "output-support-worker",
}

COL = {
    "job_id": "/Job/DisplayReference",
    "advertiser_name": "/Job/AdvertiserName",
    "advertiser_type": "/Job/AdvertiserType",
    "work_pattern": "/Job/WorkHours",
    "salary_period": "/Job/SalaryPeriod",
}
OPTIONAL_POSTED_DATE_COLUMNS = ("/Job/PostedDate", "/Job/Posted", "/Job/DatePosted")
REQUIRED_COLUMNS = {COL["job_id"], COL["advertiser_name"], COL["advertiser_type"]}
MAX_CONFLICTING_JOB_IDS = 15


def text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def find_jobg8_input(input_dir: Path = INPUT_DIR) -> Path:
    candidates = [
        path
        for path in input_dir.iterdir()
        if path.is_file()
        and path.suffix.lower() in {".xlsx", ".xls", ".csv"}
        and not path.name.startswith("~$")
    ]
    named = [path for path in candidates if "jobg8" in path.name.lower()]
    selected = named if named else candidates
    if len(selected) != 1:
        names = ", ".join(path.name for path in selected) or "none"
        raise RuntimeError(f"Expected one current JobG8 input file; found {names}")
    return selected[0]


def read_feed(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        frame = pd.read_csv(path, dtype=str).fillna("")
    else:
        frame = pd.read_excel(path, dtype=str).fillna("")
    missing = sorted(REQUIRED_COLUMNS - set(frame.columns))
    if missing:
        raise RuntimeError("JobG8 input is missing required columns: " + ", ".join(missing))
    return frame


def metadata_by_job_id(
    frame: pd.DataFrame,
    *,
    conflicted_job_ids: set[str] | None = None,
) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    conflicts = conflicted_job_ids if conflicted_job_ids is not None else set()
    posted_date_column = next(
        (column for column in OPTIONAL_POSTED_DATE_COLUMNS if column in frame.columns),
        "",
    )
    for _, row in frame.iterrows():
        job_id = text(row.get(COL["job_id"]))
        if not job_id:
            continue
        if job_id in conflicts:
            continue
        metadata = {
            "advertiser_name": text(row.get(COL["advertiser_name"])),
            "advertiser_type": text(row.get(COL["advertiser_type"])),
            "work_pattern": text(row.get(COL["work_pattern"])),
            "salary_period": text(row.get(COL["salary_period"])),
            "posted_date_basis": (
                "source" if posted_date_column and text(row.get(posted_date_column)) else ""
            ),
        }
        existing = result.get(job_id)
        if existing is not None and existing != metadata:
            conflicts.add(job_id)
            result.pop(job_id, None)
            continue
        result[job_id] = metadata
    return result


def validate_conflicting_job_ids(
    conflicted_job_ids: set[str],
    *,
    max_conflicts: int = MAX_CONFLICTING_JOB_IDS,
) -> None:
    if len(conflicted_job_ids) > max_conflicts:
        raise RuntimeError(
            "Too many conflicting duplicate JobG8 job IDs for safe job-level "
            f"quarantine: {len(conflicted_job_ids)} > {max_conflicts}"
        )
    if conflicted_job_ids:
        print(
            "Warning: quarantining JobG8 rows with conflicting duplicate metadata: "
            + ", ".join(sorted(conflicted_job_ids))
        )


def atomic_write_json(path: Path, rows: list[dict[str, Any]]) -> None:
    content = json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    handle, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
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


def enrich_rows(
    rows: list[dict[str, Any]],
    metadata: dict[str, dict[str, str]],
) -> tuple[list[dict[str, Any]], int, list[str]]:
    enriched: list[dict[str, Any]] = []
    changed = 0
    unmatched: list[str] = []

    for original in rows:
        row = dict(original)
        source = text(row.get("source")) or "JobG8"
        job_id = text(row.get("job_id"))

        if source.lower() == "jobg8":
            source_metadata = metadata.get(job_id)
            if source_metadata is None:
                unmatched.append(job_id or "<missing job_id>")
            else:
                for field, value in source_metadata.items():
                    if row.get(field) != value:
                        row[field] = value
        else:
            defaults = {
                "advertiser_name": text(row.get("advertiser_name"))
                or text(row.get("company")),
                "advertiser_type": text(row.get("advertiser_type")),
                "work_pattern": text(row.get("work_pattern")),
                "salary_period": text(row.get("salary_period")),
                "posted_date_basis": (
                    text(row.get("posted_date_basis"))
                    or ("source" if text(row.get("posted_date")) else "")
                ),
            }
            for field, value in defaults.items():
                if row.get(field) != value:
                    row[field] = value

        if row != original:
            changed += 1
        enriched.append(row)

    return enriched, changed, unmatched


def enrich_directory(
    directory: Path,
    metadata: dict[str, dict[str, str]],
    *,
    write: bool,
    quarantined_job_ids: set[str] | None = None,
) -> dict[str, int]:
    totals = {
        "files": 0,
        "rows": 0,
        "changed_rows": 0,
        "unmatched_rows": 0,
        "quarantined_rows": 0,
    }
    unmatched: list[str] = []
    quarantined: list[str] = []
    quarantine_ids = quarantined_job_ids or set()

    for path in sorted(directory.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise RuntimeError(f"{path} must contain a JSON array")
        safe_rows: list[dict[str, Any]] = []
        for row in data:
            source = text(row.get("source")) or "JobG8"
            job_id = text(row.get("job_id"))
            if source.lower() == "jobg8" and job_id in quarantine_ids:
                quarantined.append(f"{path.name}:{job_id}")
                continue
            safe_rows.append(row)

        rows, changed, missing = enrich_rows(safe_rows, metadata)
        totals["files"] += 1
        totals["rows"] += len(rows)
        totals["changed_rows"] += changed
        unmatched.extend(f"{path.name}:{job_id}" for job_id in missing)
        totals["unmatched_rows"] += len(missing)
        if write and rows != data:
            atomic_write_json(path, rows)

    if unmatched:
        sample = ", ".join(unmatched[:10])
        extra = f" (+{len(unmatched) - 10} more)" if len(unmatched) > 10 else ""
        print(
            "Warning: retained metadata unchanged for JobG8 rows not present in "
            f"the current feed: {sample}{extra}"
        )
    totals["quarantined_rows"] = len(quarantined)
    if quarantined:
        sample = ", ".join(quarantined[:10])
        extra = f" (+{len(quarantined) - 10} more)" if len(quarantined) > 10 else ""
        print(
            "Warning: withheld JobG8 output rows with conflicting duplicate "
            f"metadata: {sample}{extra}"
        )
    return totals


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--category",
        choices=sorted(OUTPUT_DIRECTORIES),
        required=True,
        help="Pipeline output family to enrich",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    feed_path = find_jobg8_input()
    conflicted_job_ids: set[str] = set()
    metadata = metadata_by_job_id(
        read_feed(feed_path), conflicted_job_ids=conflicted_job_ids
    )
    validate_conflicting_job_ids(conflicted_job_ids)
    totals = enrich_directory(
        OUTPUT_DIRECTORIES[args.category],
        metadata,
        write=not args.dry_run,
        quarantined_job_ids=conflicted_job_ids,
    )
    mode = "would enrich" if args.dry_run else "enriched"
    print(
        f"{args.category}: {mode} {totals['changed_rows']} of {totals['rows']} rows "
        f"across {totals['files']} JSON files from {feed_path.name}; "
        f"{totals['unmatched_rows']} retained rows were not in the current feed; "
        f"{totals['quarantined_rows']} conflicting duplicate rows were withheld"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

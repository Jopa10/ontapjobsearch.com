"""Attach validated Quick View duty attributes to final pipeline JSON.

The extraction is deterministic and evidence-based. Jobs without at least two
supported attributes retain no public quick-duty field.
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .at_a_glance_review_core import review_job

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIRECTORIES = {
    "admin-service": REPO_ROOT / "pipeline" / "output-admin-service",
    "support-worker": REPO_ROOT / "pipeline" / "output-support-worker",
}
FIELD = "at_a_glance_attributes"


def attributes_for_job(row: dict[str, Any]) -> list[str]:
    review = review_job(row, [])
    if review.get("status") != "generated":
        return []
    return [
        value.strip()
        for value in str(review.get("attributes", "")).split("|")
        if value.strip()
    ]


def attach_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int, int]:
    result: list[dict[str, Any]] = []
    changed = 0
    generated = 0

    for original in rows:
        row = dict(original)
        attributes = attributes_for_job(row)
        if len(attributes) >= 2:
            generated += 1
            row[FIELD] = attributes
        else:
            row.pop(FIELD, None)

        if row != original:
            changed += 1
        result.append(row)

    return result, changed, generated


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


def attach_directory(directory: Path, *, write: bool) -> dict[str, int]:
    totals = {"files": 0, "rows": 0, "changed_rows": 0, "generated_rows": 0}
    for path in sorted(directory.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise RuntimeError(f"{path} must contain a JSON array")
        rows, changed, generated = attach_rows(data)
        totals["files"] += 1
        totals["rows"] += len(rows)
        totals["changed_rows"] += changed
        totals["generated_rows"] += generated
        if write and rows != data:
            atomic_write_json(path, rows)
    return totals


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--category",
        choices=sorted(OUTPUT_DIRECTORIES),
        required=True,
        help="Pipeline output family to process",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    totals = attach_directory(
        OUTPUT_DIRECTORIES[args.category], write=not args.dry_run
    )
    mode = "would update" if args.dry_run else "updated"
    print(
        f"{args.category}: {mode} {totals['changed_rows']} of {totals['rows']} rows "
        f"across {totals['files']} JSON files; "
        f"{totals['generated_rows']} rows have validated Quick View duties"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Publish the six verified pipeline JSON pages to their live page JSON files."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Mapping:
    label: str
    source: Path
    destination: Path


MAPPINGS: tuple[Mapping, ...] = (
    Mapping("North East service administrator jobs", Path("pipeline/output-admin-service/north-east-admin-service.json"), Path("app/north-east/service-administrator-jobs.json")),
    Mapping("South Yorkshire service administrator jobs", Path("pipeline/output-admin-service/south-yorkshire-admin-service.json"), Path("app/south-yorkshire/service-administrator-jobs.json")),
    Mapping("West Yorkshire service administrator jobs", Path("pipeline/output-admin-service/west-yorkshire-admin-service.json"), Path("app/west-yorkshire/service-administrator-jobs.json")),
    Mapping("North East support worker jobs", Path("pipeline/output-support-worker/north-east-support-worker.json"), Path("app/north-east/support-worker-jobs.json")),
    Mapping("South Yorkshire support worker jobs", Path("pipeline/output-support-worker/south-yorkshire-support-worker.json"), Path("app/south-yorkshire/support-worker.json")),
    Mapping("West Yorkshire support worker jobs", Path("pipeline/output-support-worker/west-yorkshire-support-worker.json"), Path("app/west-yorkshire/support-worker.json")),
)

STATUSES = ("published", "unchanged", "skipped", "failed")


def canonical_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def display_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def usable_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_source(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError("source file does not exist")
    data = load_json(path)
    if not isinstance(data, list):
        raise ValueError("source JSON must be an array")

    seen: set[str] = set()
    for index, row in enumerate(data):
        if not isinstance(row, dict):
            raise ValueError(f"row {index} is not an object")
        for field in ("job_id", "title", "apply_url"):
            if not usable_text(row.get(field)):
                raise ValueError(f"row {index} has no usable {field}")
        job_id = row["job_id"].strip()
        if job_id in seen:
            raise ValueError(f"duplicate job_id {job_id!r}")
        seen.add(job_id)
    return data


def validate_destination_path(path: Path) -> None:
    if not path.parent.is_dir():
        raise ValueError("destination parent directory does not exist")
    if not path.is_file():
        raise ValueError("destination file does not exist")


def atomic_write(path: Path, content: str) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def publish_one(mapping: Mapping, *, write: bool, root: Path = REPO_ROOT) -> dict[str, Any]:
    source = root / mapping.source
    destination = root / mapping.destination
    result = {
        "page_label": mapping.label,
        "source": str(mapping.source),
        "destination": str(mapping.destination),
        "selected_count": 0,
        "status": "failed",
        "reason": "",
    }

    try:
        source_data = validate_source(source)
        result["selected_count"] = len(source_data)
        validate_destination_path(destination)
        destination_before_text = destination.read_text(encoding="utf-8")
        destination_data = json.loads(destination_before_text)
        if not isinstance(destination_data, list):
            raise ValueError("destination JSON must be an array")

        if not source_data:
            result.update(status="skipped", reason="source selected zero jobs; live destination left unchanged")
            return result

        source_canonical = canonical_json(source_data)
        if canonical_json(destination_data) == source_canonical:
            result.update(status="unchanged", reason="source and destination canonical content already match")
            return result

        if not write:
            result.update(status="published", reason="dry-run: destination would be updated")
            return result

        previous_text = destination_before_text
        atomic_write(destination, display_json(source_data))
        reopened_data = load_json(destination)
        if len(reopened_data) != len(source_data):
            raise RuntimeError("post-write destination count does not equal validated source count")
        if canonical_json(reopened_data) != source_canonical:
            raise RuntimeError("post-write canonical destination content does not equal validated source content")
        result.update(status="published", reason="destination updated and post-write verification passed")
        return result
    except Exception as exc:  # keep processing remaining mappings
        if write and destination.exists() and "previous_text" in locals():
            try:
                atomic_write(destination, previous_text)
                result["reason"] = f"{exc}; restored previous destination"
            except Exception as restore_exc:
                result["reason"] = f"{exc}; restore failed: {restore_exc}"
        else:
            result["reason"] = str(exc)
        result["status"] = "failed"
        return result


def format_report(results: Iterable[dict[str, Any]]) -> str:
    rows = list(results)
    lines = ["# Publish verified pages report", "", "| Page | Source | Destination | Selected | Status | Reason |", "| --- | --- | --- | ---: | --- | --- |"]
    for row in rows:
        lines.append(f"| {row['page_label']} | `{row['source']}` | `{row['destination']}` | {row['selected_count']} | {row['status']} | {row['reason']} |")
    lines.extend(["", "## Totals"])
    for status in STATUSES:
        lines.append(f"- {status}: {sum(1 for row in rows if row['status'] == status)}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="validate and report without writing")
    mode.add_argument("--write", action="store_true", help="publish changed verified pages")
    args = parser.parse_args()

    results = [publish_one(mapping, write=args.write) for mapping in MAPPINGS]
    print(format_report(results), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

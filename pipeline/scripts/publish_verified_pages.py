#!/usr/bin/env python3
"""Publish verified pipeline JSON pages for slices marked LIVE in the register."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

from slice_registry import live_slices

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Mapping:
    label: str
    region: str
    category: str
    source: Path
    destination: Path


MAPPINGS: tuple[Mapping, ...] = (
    Mapping("Hampshire service administrator jobs", "Hampshire", "admin_service", Path("pipeline/output-admin-service/hampshire-admin-service.json"), Path("app/hampshire/service-administrator-jobs.json")),
    Mapping("Kent service administrator jobs", "Kent", "admin_service", Path("pipeline/output-admin-service/kent-admin-service.json"), Path("app/kent/service-administrator-jobs.json")),
    Mapping("London service administrator jobs", "London", "admin_service", Path("pipeline/output-admin-service/london-admin-service.json"), Path("app/london/service-administrator-jobs.json")),
    Mapping("North East service administrator jobs", "North East", "admin_service", Path("pipeline/output-admin-service/north-east-admin-service.json"), Path("app/north-east/service-administrator-jobs.json")),
    Mapping("South Yorkshire service administrator jobs", "Yorkshire - South", "admin_service", Path("pipeline/output-admin-service/south-yorkshire-admin-service.json"), Path("app/south-yorkshire/service-administrator-jobs.json")),
    Mapping("Surrey service administrator jobs", "Surrey", "admin_service", Path("pipeline/output-admin-service/surrey-admin-service.json"), Path("app/surrey/service-administrator-jobs.json")),
    Mapping("West Yorkshire service administrator jobs", "Yorkshire - West", "admin_service", Path("pipeline/output-admin-service/west-yorkshire-admin-service.json"), Path("app/west-yorkshire/service-administrator-jobs.json")),
    Mapping("Cumbria South support worker jobs", "Cumbria - South", "support_worker", Path("pipeline/output-support-worker/cumbria-south-support-worker.json"), Path("app/cumbria-south/support-worker.json")),
    Mapping("Hampshire support worker jobs", "Hampshire", "support_worker", Path("pipeline/output-support-worker/hampshire-support-worker.json"), Path("app/hampshire/support-worker.json")),
    Mapping("North East support worker jobs", "North East", "support_worker", Path("pipeline/output-support-worker/north-east-support-worker.json"), Path("app/north-east/support-worker-jobs.json")),
    Mapping("South Yorkshire support worker jobs", "Yorkshire - South", "support_worker", Path("pipeline/output-support-worker/south-yorkshire-support-worker.json"), Path("app/south-yorkshire/support-worker.json")),
    Mapping("Sussex support worker jobs", "Sussex", "support_worker", Path("pipeline/output-support-worker/sussex-support-worker.json"), Path("app/sussex/support-worker.json")),
    Mapping("West Yorkshire support worker jobs", "Yorkshire - West", "support_worker", Path("pipeline/output-support-worker/west-yorkshire-support-worker.json"), Path("app/west-yorkshire/support-worker.json")),
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


def normalise_posted_date(value: str) -> str:
    normalised = value.strip()
    for date_format in ("%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(normalised, date_format).date().isoformat()
        except ValueError:
            pass
    return normalised


def add_stable_posted_dates(
    source_data: list[dict[str, Any]],
    destination_data: list[dict[str, Any]],
    *,
    publication_date: str,
) -> list[dict[str, Any]]:
    """Keep genuine source dates distinct from Ontap's first publication date."""
    previous_dates = {
        row["job_id"].strip(): (
            row["posted_date"].strip(),
            row.get("posted_date_basis", "").strip()
            if isinstance(row.get("posted_date_basis"), str)
            else "",
        )
        for row in destination_data
        if isinstance(row, dict)
        and usable_text(row.get("job_id"))
        and usable_text(row.get("posted_date"))
    }

    result: list[dict[str, Any]] = []
    for source_row in source_data:
        row = dict(source_row)
        source_code = row.get("source", "JobG8")
        source_code = source_code.strip() if isinstance(source_code, str) else "JobG8"
        basis = row.get("posted_date_basis", "")
        basis = basis.strip() if isinstance(basis, str) else ""

        if usable_text(row.get("posted_date")):
            row["posted_date"] = normalise_posted_date(row["posted_date"])
            if basis:
                row["posted_date_basis"] = basis
            elif source_code.lower() != "jobg8":
                # Approved external-source dates are extracted directly from the
                # provider record and are therefore safe to identify as source dates.
                row["posted_date_basis"] = "source"
            else:
                # Legacy JobG8 output may contain either a provider date or an
                # Ontap fallback. Do not guess which one it is.
                row.pop("posted_date_basis", None)
        else:
            job_id = row["job_id"].strip()
            previous_date, previous_basis = previous_dates.get(job_id, ("", ""))
            if previous_date:
                row["posted_date"] = previous_date
                if previous_basis:
                    row["posted_date_basis"] = previous_basis
                else:
                    row.pop("posted_date_basis", None)
            else:
                row["posted_date"] = publication_date
                row["posted_date_basis"] = "ontap_first_published"
        result.append(row)
    return result


def atomic_write(path: Path, content: str) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(fd)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def publish_one(
    mapping: Mapping,
    *,
    write: bool,
    active_slices: set[tuple[str, str]],
    root: Path = REPO_ROOT,
    publication_date: str | None = None,
) -> dict[str, Any]:
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

    if (mapping.region, mapping.category) not in active_slices:
        result.update(status="skipped", reason="slice is not LIVE in region_category_slice_register.csv")
        return result

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

        source_data = add_stable_posted_dates(
            source_data,
            destination_data,
            publication_date=publication_date or date.today().isoformat(),
        )

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
    except Exception as exc:
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

    active_slices = live_slices()
    results = [
        publish_one(mapping, write=args.write, active_slices=active_slices)
        for mapping in MAPPINGS
    ]
    print(format_report(results), end="")
    return 1 if any(row["status"] == "failed" for row in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())

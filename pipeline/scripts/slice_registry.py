from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTER_PATH = REPO_ROOT / "pipeline" / "registers" / "region_category_slice_register.csv"
ALLOWED_STATUSES = {"LIVE", "CANDIDATE", "RETIRED"}
ALLOWED_CATEGORIES = {"admin_service", "support_worker"}


@dataclass(frozen=True)
class SliceRecord:
    region: str
    category: str
    status: str


def load_slice_register(path: Path = DEFAULT_REGISTER_PATH) -> list[SliceRecord]:
    if not path.is_file():
        raise SystemExit(f"STOP: slice register not found: {path}")

    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["region", "category", "status"]:
            raise SystemExit(
                "STOP: slice register columns must be exactly: region,category,status"
            )

        records: list[SliceRecord] = []
        seen: set[tuple[str, str]] = set()
        for line_number, row in enumerate(reader, start=2):
            region = (row.get("region") or "").strip()
            category = (row.get("category") or "").strip()
            status = (row.get("status") or "").strip().upper()
            if not region or not category or not status:
                raise SystemExit(f"STOP: incomplete slice-register row at line {line_number}")
            if category not in ALLOWED_CATEGORIES:
                raise SystemExit(
                    f"STOP: unsupported category {category!r} at line {line_number}"
                )
            if status not in ALLOWED_STATUSES:
                raise SystemExit(
                    f"STOP: unsupported status {status!r} at line {line_number}"
                )
            key = (region, category)
            if key in seen:
                raise SystemExit(
                    f"STOP: duplicate slice-register row for {region!r} / {category!r}"
                )
            seen.add(key)
            records.append(SliceRecord(region, category, status))

    if not records:
        raise SystemExit("STOP: slice register contains no rows")
    return records


def live_slices(path: Path = DEFAULT_REGISTER_PATH) -> set[tuple[str, str]]:
    return {
        (record.region, record.category)
        for record in load_slice_register(path)
        if record.status == "LIVE"
    }


def is_live(region: str, category: str, path: Path = DEFAULT_REGISTER_PATH) -> bool:
    return (region, category) in live_slices(path)

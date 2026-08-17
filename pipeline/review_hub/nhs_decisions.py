from __future__ import annotations

import csv
from pathlib import Path

FIELDS = (
    "category",
    "source_job_id",
    "hub_fingerprint",
    "action",
    "title",
)


def load_decisions(path: Path) -> dict[tuple[str, str, str], str]:
    if not path.is_file():
        return {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = csv.DictReader(handle)
        return {
            (
                str(row.get("category") or "").strip(),
                str(row.get("source_job_id") or "").strip(),
                str(row.get("hub_fingerprint") or "").strip(),
            ): str(row.get("action") or "").strip().casefold()
            for row in rows
            if str(row.get("action") or "").strip().casefold() in {"select", "exclude"}
        }


def write_decision(
    path: Path,
    *,
    category: str,
    source_job_id: str,
    hub_fingerprint: str,
    action: str,
    title: str = "",
) -> None:
    action = action.strip().casefold()
    if action not in {"select", "exclude"}:
        raise ValueError(f"invalid NHS decision action: {action!r}")
    category = category.strip()
    source_job_id = source_job_id.strip()
    hub_fingerprint = hub_fingerprint.strip()
    if not category or not source_job_id or not hub_fingerprint:
        raise ValueError("NHS decision requires category, source_job_id and fingerprint")

    existing: list[dict[str, str]] = []
    if path.is_file():
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            existing = [dict(row) for row in csv.DictReader(handle)]

    # A changed fingerprint is deliberately a new decision. Remove older
    # decisions for the same source/category so the register stays compact.
    existing = [
        row
        for row in existing
        if not (
            str(row.get("category") or "").strip() == category
            and str(row.get("source_job_id") or "").strip() == source_job_id
        )
    ]
    existing.append(
        {
            "category": category,
            "source_job_id": source_job_id,
            "hub_fingerprint": hub_fingerprint,
            "action": action,
            "title": title.strip(),
        }
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(existing)

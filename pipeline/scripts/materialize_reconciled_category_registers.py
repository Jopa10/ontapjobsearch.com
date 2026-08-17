#!/usr/bin/env python3
"""Materialize temporary category registers with agreed refinement overrides applied.

This keeps the historical profiler registers immutable while giving Compiler Module 2
an authoritative classification view. Existing titles are overridden by exact
(category, title) refinement rules; agreed refinement titles missing from a source
register are appended so they can participate in the category analysis.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

REGISTER_FILES = {
    "admin_service": "admin_service_title_classification_register.csv",
    "support_worker": "support_worker_title_classification_register.csv",
    "finance_accounts": "finance_accounts_title_classification_register.csv",
    "customer_service_contact_centre": "customer_service_contact_centre_title_classification_register.csv",
    "hr_recruitment": "hr_recruitment_title_classification_register.csv",
    "warehouse_logistics": "warehouse_logistics_title_classification_register.csv",
}


def norm(value: object) -> str:
    return " ".join(str(value or "").strip().casefold().split())


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"{path} has no header")
        return list(reader.fieldnames), [dict(row) for row in reader]


def load_refinements(path: Path) -> dict[str, dict[str, dict[str, str]]]:
    _, rows = read_csv(path)
    result: dict[str, dict[str, dict[str, str]]] = {}
    for row in rows:
        category = str(row.get("category", "")).strip()
        title_key = norm(row.get("title", ""))
        classification = str(row.get("classification", "")).strip().upper()
        if not category or not title_key or not classification:
            continue
        result.setdefault(category, {})[title_key] = row
    return result


def reconcile_register(
    category: str,
    source_path: Path,
    output_path: Path,
    refinements: dict[str, dict[str, dict[str, str]]],
) -> tuple[int, int]:
    fieldnames, rows = read_csv(source_path)
    required = {"title", "classification"}
    missing = required.difference(fieldnames)
    if missing:
        raise ValueError(f"{source_path} missing required columns: {sorted(missing)}")

    rules = refinements.get(category, {})
    existing: dict[str, dict[str, str]] = {
        norm(row.get("title", "")): row for row in rows if norm(row.get("title", ""))
    }

    overrides = 0
    additions = 0
    for title_key, rule in rules.items():
        classification = str(rule.get("classification", "")).strip().upper()
        if title_key in existing:
            row = existing[title_key]
            if str(row.get("classification", "")).strip().upper() != classification:
                row["classification"] = classification
                overrides += 1
            if "review_status" in fieldnames:
                row["review_status"] = str(rule.get("review_status", "")).strip() or "REFINEMENT_OVERRIDE"
            if "reason" in fieldnames and str(rule.get("reason", "")).strip():
                row["reason"] = str(rule.get("reason", "")).strip()
            continue

        new_row = {field: "" for field in fieldnames}
        new_row["title"] = str(rule.get("title", "")).strip()
        new_row["classification"] = classification
        if "review_status" in fieldnames:
            new_row["review_status"] = str(rule.get("review_status", "")).strip() or "REFINEMENT_OVERRIDE"
        if "reason" in fieldnames:
            new_row["reason"] = str(rule.get("reason", "")).strip()
        rows.append(new_row)
        existing[title_key] = new_row
        additions += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return overrides, additions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registers-dir", required=True, type=Path)
    parser.add_argument("--refinements", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    refinements = load_refinements(args.refinements)
    total_overrides = 0
    total_additions = 0

    for category, filename in REGISTER_FILES.items():
        source = args.registers_dir / filename
        if not source.is_file():
            raise SystemExit(f"Missing source register: {source}")
        overrides, additions = reconcile_register(
            category,
            source,
            args.output_dir / filename,
            refinements,
        )
        total_overrides += overrides
        total_additions += additions
        print(f"{category}: {overrides} overrides, {additions} agreed-title additions")

    print(f"Total: {total_overrides} overrides, {total_additions} agreed-title additions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

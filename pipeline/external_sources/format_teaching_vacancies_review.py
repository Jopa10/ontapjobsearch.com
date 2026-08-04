"""Format the West Yorkshire Teaching Vacancies review output.

Keeps review rows in the same practical order as Ontap's other external-source
reviews: selected (HC) first, manual review (POSS) second, and hard passes last.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

CLASSIFICATION_ORDER = {
    "HC": 0,
    "POSS": 1,
    "DUPLICATE": 2,
    "HARD_PASS": 3,
}


def sort_key(row: dict[str, str]) -> tuple[int, str, str, str]:
    classification = (row.get("classification") or "").strip().upper()
    return (
        CLASSIFICATION_ORDER.get(classification, 99),
        (row.get("title") or "").casefold(),
        (row.get("employer") or "").casefold(),
        (row.get("location") or "").casefold(),
    )


def sort_review_csv(path: Path) -> None:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    if not fieldnames:
        raise ValueError(f"Review CSV has no header: {path}")
    rows.sort(key=sort_key)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    sort_review_csv(args.csv_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

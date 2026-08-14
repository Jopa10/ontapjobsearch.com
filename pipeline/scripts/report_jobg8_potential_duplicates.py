#!/usr/bin/env python3
"""Report likely duplicate JobG8 adverts without suppressing any jobs.

The detector is deliberately conservative. It only compares rows that share a
normalised title, location and advertiser name, then requires strong content
similarity plus compatible salary data. The output is diagnostic only: no
selection, review or publish data is modified.
"""
from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import pandas as pd

COL = {
    "job_id": "/Job/DisplayReference",
    "title": "/Job/Position",
    "advertiser": "/Job/AdvertiserName",
    "area": "/Job/Area",
    "location": "/Job/Location",
    "description": "/Job/Description",
    "salary_min": "/Job/SalaryMinimum",
    "salary_max": "/Job/SalaryMaximum",
    "salary_period": "/Job/SalaryPeriod",
}

REQUIRED_COLUMNS = [
    COL["job_id"],
    COL["title"],
    COL["advertiser"],
    COL["area"],
    COL["location"],
    COL["description"],
]

REPORT_FIELDS = [
    "confidence",
    "duplicate_basis",
    "job_id_1",
    "job_id_2",
    "title",
    "location",
    "advertiser_1",
    "advertiser_2",
    "salary_1",
    "salary_2",
    "description_similarity",
]

COMPANY_SUFFIXES = {
    "limited",
    "ltd",
    "plc",
    "llp",
    "inc",
    "incorporated",
    "company",
    "co",
    "uk",
}


@dataclass(frozen=True)
class Vacancy:
    job_id: str
    title: str
    advertiser: str
    area: str
    location: str
    description: str
    salary_min: str
    salary_max: str
    salary_period: str


def _text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def _normalise_words(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def _normalise_advertiser(value: str) -> str:
    words = _normalise_words(value).split()
    while words and words[-1] in COMPANY_SUFFIXES:
        words.pop()
    return " ".join(words)


def _normalise_location(location: str, area: str) -> str:
    return _normalise_words(location or area)


def _normalise_description(value: str) -> str:
    return _normalise_words(value)


def _normalise_number(value: str) -> str:
    if not value:
        return ""
    try:
        number = float(value.replace(",", ""))
    except ValueError:
        return _normalise_words(value)
    return f"{number:.2f}"


def _salary_key(vacancy: Vacancy) -> tuple[str, str, str]:
    return (
        _normalise_number(vacancy.salary_min),
        _normalise_number(vacancy.salary_max),
        _normalise_words(vacancy.salary_period),
    )


def _salary_display(vacancy: Vacancy) -> str:
    bits = [vacancy.salary_min, vacancy.salary_max, vacancy.salary_period]
    return " | ".join(bit for bit in bits if bit)


def _description_similarity(left: Vacancy, right: Vacancy) -> float:
    a = _normalise_description(left.description)
    b = _normalise_description(right.description)
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b, autojunk=False).ratio()


def _load_vacancies(path: Path) -> list[Vacancy]:
    frame = pd.read_excel(path, dtype=str, keep_default_na=False)
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required JobG8 columns: {', '.join(missing)}")

    for optional in (COL["salary_min"], COL["salary_max"], COL["salary_period"]):
        if optional not in frame.columns:
            frame[optional] = ""

    vacancies: list[Vacancy] = []
    for _, row in frame.iterrows():
        job_id = _text(row.get(COL["job_id"]))
        title = _text(row.get(COL["title"]))
        advertiser = _text(row.get(COL["advertiser"]))
        if not job_id or not title or not advertiser:
            continue
        vacancies.append(
            Vacancy(
                job_id=job_id,
                title=title,
                advertiser=advertiser,
                area=_text(row.get(COL["area"])),
                location=_text(row.get(COL["location"])),
                description=_text(row.get(COL["description"])),
                salary_min=_text(row.get(COL["salary_min"])),
                salary_max=_text(row.get(COL["salary_max"])),
                salary_period=_text(row.get(COL["salary_period"])),
            )
        )
    return vacancies


def find_likely_duplicates(vacancies: list[Vacancy]) -> list[dict[str, str]]:
    """Return conservative likely-duplicate pairs; never mutate input rows."""
    blocks: dict[tuple[str, str, str], list[Vacancy]] = defaultdict(list)
    for vacancy in vacancies:
        key = (
            _normalise_words(vacancy.title),
            _normalise_location(vacancy.location, vacancy.area),
            _normalise_advertiser(vacancy.advertiser),
        )
        if all(key):
            blocks[key].append(vacancy)

    matches: list[dict[str, str]] = []
    seen_pairs: set[tuple[str, str]] = set()
    for block in blocks.values():
        if len(block) < 2:
            continue
        for index, left in enumerate(block):
            for right in block[index + 1 :]:
                if left.job_id == right.job_id:
                    continue
                pair = tuple(sorted((left.job_id, right.job_id)))
                if pair in seen_pairs:
                    continue

                similarity = _description_similarity(left, right)
                left_salary = _salary_key(left)
                right_salary = _salary_key(right)
                salaries_match = left_salary == right_salary and any(left_salary)
                salaries_missing = not any(left_salary) and not any(right_salary)

                # Exact title/location/advertiser blocks are already strong.
                # Require near-identical advert copy, with a slightly lower bar
                # when the structured salary also agrees.
                if salaries_match and similarity >= 0.80:
                    basis = "same title/location/advertiser + salary + very similar description"
                elif (salaries_match or salaries_missing) and similarity >= 0.92:
                    basis = "same title/location/advertiser + near-identical description"
                else:
                    continue

                seen_pairs.add(pair)
                matches.append(
                    {
                        "confidence": "LIKELY_DUPLICATE",
                        "duplicate_basis": basis,
                        "job_id_1": left.job_id,
                        "job_id_2": right.job_id,
                        "title": left.title,
                        "location": left.location or left.area,
                        "advertiser_1": left.advertiser,
                        "advertiser_2": right.advertiser,
                        "salary_1": _salary_display(left),
                        "salary_2": _salary_display(right),
                        "description_similarity": f"{similarity:.3f}",
                    }
                )

    return sorted(
        matches,
        key=lambda row: (
            row["title"].casefold(),
            row["location"].casefold(),
            row["job_id_1"],
            row["job_id_2"],
        ),
    )


def write_report(path: Path, matches: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REPORT_FIELDS)
        writer.writeheader()
        writer.writerows(matches)


def main() -> int:
    parser = argparse.ArgumentParser(description="Report likely duplicate JobG8 adverts.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("pipeline/reports-daily/potential-jobg8-duplicates.csv"),
    )
    args = parser.parse_args()

    vacancies = _load_vacancies(args.input)
    matches = find_likely_duplicates(vacancies)
    write_report(args.output, matches)

    print(f"JobG8 rows inspected for duplicate candidates: {len(vacancies)}")
    print(f"Likely duplicate pairs: {len(matches)}")
    print(f"Report: {args.output.as_posix()}")
    for row in matches[:20]:
        print(
            f"- {row['title']} | {row['location']} | "
            f"{row['advertiser_1']} <> {row['advertiser_2']} | "
            f"{row['job_id_1']} <> {row['job_id_2']} | "
            f"similarity={row['description_similarity']}"
        )
    if len(matches) > 20:
        print(f"- ... {len(matches) - 20} more pair(s) in CSV")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Create and validate the repository review for West Yorkshire Teaching Vacancies."""
from __future__ import annotations

import argparse
import csv
import hashlib
from dataclasses import asdict
from datetime import date
from pathlib import Path

from external_sources.teaching_vacancies_poc import Vacancy

REVIEWABLE = {"HC", "POSS"}
DECISION_ORDER = {"HC": 0, "POSS": 1, "DUPLICATE": 2, "HARD_PASS": 3}
FINGERPRINT_FIELDS = (
    "source_job_id", "title", "employer", "location", "salary_text",
    "closing_date", "source_url", "classification", "jobg8_check",
)


def ordered(vacancies: list[Vacancy]) -> list[Vacancy]:
    return sorted(vacancies, key=lambda v: (
        DECISION_ORDER.get(v.final_decision or v.classification, 99),
        v.title.casefold(), v.employer.casefold(), v.source_job_id,
    ))


def reviewable(vacancies: list[Vacancy]) -> list[Vacancy]:
    return [v for v in ordered(vacancies)
            if v.classification in REVIEWABLE and v.jobg8_check != "DUPLICATE"]


def review_fingerprint(vacancies: list[Vacancy]) -> str:
    rows = []
    for vacancy in reviewable(vacancies):
        values = asdict(vacancy)
        rows.append("|".join(str(values.get(field, "")) for field in FINGERPRINT_FIELDS))
    return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()


def write_review_markdown(path: Path, vacancies: list[Vacancy], review_date: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = reviewable(vacancies)
    lines = [
        "# West Yorkshire — Teaching Vacancies review",
        "",
        f"Review date: {review_date or date.today().isoformat()}",
        f"Vacancy-set fingerprint: `{review_fingerprint(vacancies)}`",
        "",
        "For every vacancy below, replace exactly one box with `[x]`.",
        "",
    ]
    for vacancy in rows:
        lines += [
            f"## {vacancy.classification} — {vacancy.title}",
            f"Source ID: `{vacancy.source_job_id}`",
            f"Employer: {vacancy.employer}",
            f"Location: {vacancy.location}",
            f"Salary: {vacancy.salary_text or 'Not stated'}",
            f"Closes: {vacancy.closing_date or 'Not stated'}",
            f"Source: {vacancy.source_url}",
            "- [ ] SELECT",
            "- [ ] EXCLUDE",
            "",
        ]
    lines += [
        "## Hard passes",
        "",
        "Hard-pass rows remain visible in the companion CSV but require no decision.",
        "",
        "No approved output may be generated unless every reviewable vacancy has exactly one decision and the live fingerprint still matches.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_csv(path: Path) -> list[Vacancy]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [Vacancy(**{key: row.get(key, "") for key in Vacancy.__dataclass_fields__})
                for row in csv.DictReader(handle)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("review_csv", type=Path)
    parser.add_argument("review_markdown", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    write_review_markdown(args.review_markdown, load_csv(args.review_csv))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

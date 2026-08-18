"""Review-only NHS Support Worker discovery and classification.

This module deliberately keeps transport separate from selection. It accepts a
normalised list of NHS vacancies (for example rows parsed from the NHS XML review
feed), identifies Support Worker candidates, applies Ontap's NHS switchability
rules, and writes the shared NHS review CSV/summary consumed by the unified daily
Review Hub.

No live page or approved-output publishing is performed here.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date
import json
from pathlib import Path
from typing import Iterable, Mapping

from external_sources.nhs_switchability import classify_support_worker, is_support_worker_title


REVIEW_FIELDS = (
    "source_job_id", "title", "employer", "locations", "salary_text",
    "closing_date", "source_url", "final_decision", "manual_action",
    "ontap_category", "switchability", "classification_reason", "source",
)


@dataclass(frozen=True)
class DiscoveryRow:
    source_job_id: str
    title: str
    employer: str = ""
    locations: str = ""
    salary_text: str = ""
    closing_date: str = ""
    source_url: str = ""
    final_decision: str = ""
    manual_action: str = ""
    ontap_category: str = "support_worker"
    switchability: str = ""
    classification_reason: str = ""
    source: str = "NHS Jobs"


def clean(value: object) -> str:
    return " ".join(str(value or "").split())


def _criteria(row: Mapping[str, object]) -> str:
    """Use whichever review/discovery text fields are available without inventing facts."""
    parts = [
        row.get("criteria_text"),
        row.get("description"),
        row.get("person_specification"),
        row.get("essential_criteria"),
    ]
    return "\n".join(clean(value) for value in parts if clean(value))


def classify_rows(rows: Iterable[Mapping[str, object]]) -> list[DiscoveryRow]:
    output: list[DiscoveryRow] = []
    seen: set[str] = set()
    for row in rows:
        source_job_id = clean(row.get("source_job_id") or row.get("id") or row.get("job_id"))
        title = clean(row.get("title"))
        if not source_job_id or not title or not is_support_worker_title(title):
            continue
        if source_job_id in seen:
            continue
        seen.add(source_job_id)

        classification = classify_support_worker(title, _criteria(row))
        output.append(
            DiscoveryRow(
                source_job_id=source_job_id,
                title=title,
                employer=clean(row.get("employer") or row.get("company")),
                locations=clean(row.get("locations") or row.get("location")),
                salary_text=clean(row.get("salary_text") or row.get("salary")),
                closing_date=clean(row.get("closing_date")),
                source_url=clean(row.get("source_url") or row.get("url")),
                final_decision=classification.final_decision,
                ontap_category=classification.category,
                switchability=classification.switchability,
                classification_reason=classification.reason,
            )
        )
    return output


def merge_review_rows(existing: Iterable[Mapping[str, object]], support: Iterable[DiscoveryRow]) -> list[dict[str, str]]:
    """Merge Support Worker rows into the shared NHS review file by category + stable ID.

    Existing manual_action is retained only when the material classification facts
    are unchanged. Changed rows deliberately return with blank manual_action so the
    unified Review Hub can ask for a fresh judgement.
    """
    existing_rows = [dict(row) for row in existing]
    existing_index = {
        (clean(row.get("ontap_category")), clean(row.get("source_job_id"))): row
        for row in existing_rows
    }
    support_rows = [asdict(row) for row in support]

    # Preserve non-support NHS categories exactly as they are.
    merged = [row for row in existing_rows if clean(row.get("ontap_category")) != "support_worker"]

    material = (
        "title", "employer", "locations", "salary_text", "closing_date",
        "final_decision", "switchability", "classification_reason", "source_url",
    )
    for row in support_rows:
        previous = existing_index.get(("support_worker", clean(row.get("source_job_id"))))
        if previous and all(clean(previous.get(field)) == clean(row.get(field)) for field in material):
            row["manual_action"] = clean(previous.get("manual_action"))
        merged.append({field: clean(row.get(field)) for field in REVIEW_FIELDS})
    return merged


def counts(rows: Iterable[DiscoveryRow]) -> dict[str, int]:
    values = Counter(row.switchability for row in rows)
    return {
        label: values.get(label, 0)
        for label in ("OPEN_SWITCH", "BRIDGEABLE", "HEALTHCARE_EXPERIENCED", "NHS_EXPERIENCED", "HARD_PASS")
    }


def write_outputs(
    rows: list[DiscoveryRow],
    *,
    review_csv: Path,
    summary_md: Path,
    today: date | None = None,
) -> dict[str, object]:
    today = today or date.today()
    existing: list[dict[str, str]] = []
    if review_csv.is_file():
        with review_csv.open("r", encoding="utf-8-sig", newline="") as handle:
            existing = [dict(row) for row in csv.DictReader(handle)]
    merged = merge_review_rows(existing, rows)
    review_csv.parent.mkdir(parents=True, exist_ok=True)
    with review_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_FIELDS)
        writer.writeheader()
        writer.writerows(merged)

    bucket_counts = counts(rows)
    summary_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NHS Jobs review summary",
        "",
        f"review_date: {today.isoformat()}",
        "",
        "## Support Worker discovery",
        "",
        f"- Support Worker candidates: {len(rows)}",
        *[f"- {label}: {bucket_counts[label]}" for label in bucket_counts],
        "",
        "Review-only: this output feeds the unified Ontap daily review and does not publish jobs.",
    ]
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"review_date": today.isoformat(), "support_worker_candidates": len(rows), **bucket_counts}


def _read_json(path: Path) -> list[dict[str, object]]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, list):
        raise ValueError("input JSON must contain a list of vacancy objects")
    return [row for row in value if isinstance(row, dict)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path, help="Normalised NHS vacancy rows for dry-run classification")
    parser.add_argument("--review-csv", type=Path, default=Path("reviews/external/nhs-jobs-review.csv"))
    parser.add_argument("--summary-md", type=Path, default=Path("reviews/external/nhs-jobs-summary.md"))
    args = parser.parse_args(argv)
    report = write_outputs(
        classify_rows(_read_json(args.input_json)),
        review_csv=args.review_csv,
        summary_md=args.summary_md,
    )
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Build one England-wide human review CSV from regional review CSVs.

Regional review files remain the authoritative regional evidence and approval
boundaries. This file is a convenience view only and does not publish jobs.
"""
from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path

from external_sources import teaching_vacancies_discovery as discovery

MASTER_FIELDS = (
    "final_decision",
    "title",
    "salary_text",
    "regional_slice",
    "classification_reason",
    "employer",
    "location",
    "posted_date",
    "closing_date",
    "classification",
    "jobg8_check",
    "jobg8_candidate_title",
    "jobg8_candidate_employer",
    "jobg8_match_score",
    "employment_type",
    "ontap_region",
    "geo_cluster",
    "geography_status",
    "geography_reason",
    "geography_lookup_key",
    "slice_status",
    "publish_eligible",
    "source_job_id",
    "source_url",
    "manual_action",
    "migration_status",
    "factual_fingerprint",
    "discovery_routes",
    "source",
)


def build_master_rows(review_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(review_dir.glob("*-admin-service-review.csv")):
        if path.name == "england-wide-admin-service-review.csv":
            continue
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for source_row in csv.DictReader(handle):
                row = dict(source_row)
                row["regional_slice"] = (
                    f"{row.get('ontap_region', '').strip()} / admin_service"
                )
                rows.append({field: row.get(field, "") for field in MASTER_FIELDS})
    return sorted(
        rows,
        key=lambda row: (
            {"SELECTED": 0, "POSS": 1, "EXCLUDED": 2, "HARD_PASS": 3}.get(
                row["final_decision"], 9
            ),
            row["regional_slice"].casefold(),
            row["title"].casefold(),
            row["source_job_id"],
        ),
    )


def master_csv_bytes(rows: list[dict[str, str]]) -> bytes:
    handle = io.StringIO(newline="")
    writer = csv.DictWriter(handle, fieldnames=MASTER_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue().encode("utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--review-dir",
        type=Path,
        default=Path("reviews/external/teaching-vacancies"),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path(
            "reviews/external/teaching-vacancies/"
            "england-wide-admin-service-review.csv"
        ),
    )
    parser.add_argument("--write-master-review", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.write_master_review:
        raise SystemExit(
            "STOP: add --write-master-review to create the review-only master CSV."
        )
    rows = build_master_rows(args.review_dir)
    if not rows:
        raise SystemExit("STOP: no regional review rows found for the master CSV.")
    discovery.write_bytes_atomic(args.output_csv, master_csv_bytes(rows))
    print(
        f"Teaching Vacancies master review wrote {len(rows)} rows; "
        "regional controls remain unchanged and no jobs were published."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

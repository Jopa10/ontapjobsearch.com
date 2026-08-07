"""Build England-wide Teaching Vacancies review outputs from regional CSVs.

Regional review files remain the authoritative regional evidence and approval
boundaries. The master CSV and Markdown summary are convenience views only and
do not publish jobs.
"""
from __future__ import annotations

import argparse
import csv
import io
from collections import Counter, defaultdict
from pathlib import Path

from external_sources import teaching_vacancies_discovery as discovery

REVIEW_NOW = "REVIEW NOW"
DEFERRED = "DEFERRED - REGION NOT LIVE"

MASTER_FIELDS = (
    "final_decision",
    "title",
    "salary_text",
    "regional_slice",
    "classification_reason",
    "review_scope",
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


def _review_scope(slice_status: str) -> str:
    return REVIEW_NOW if slice_status.strip().upper() == "LIVE" else DEFERRED


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
                row["review_scope"] = _review_scope(row.get("slice_status", ""))
                rows.append({field: row.get(field, "") for field in MASTER_FIELDS})
    return sorted(
        rows,
        key=lambda row: (
            0 if row["review_scope"] == REVIEW_NOW else 1,
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


def _md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def _review_block(row: dict[str, str]) -> list[str]:
    action = row.get("manual_action", "").strip().casefold()
    headline = " | ".join(
        [
            _md(row["final_decision"]),
            _md(row["ontap_region"]),
            _md(row["location"]),
            _md(row["salary_text"]),
            _md(row["title"]),
        ]
    )
    return [
        "---",
        f"action: {action}" if action else "action:",
        headline,
        f"employer: {_md(row['employer'])}",
        f"closing_date: {_md(row['closing_date'])}",
        f"reason: {_md(row['classification_reason'])}",
        f"source_job_id: {_md(row['source_job_id'])}",
        f"source_url: {_md(row['source_url'])}",
        "---",
        "",
    ]


def master_summary_text(rows: list[dict[str, str]]) -> str:
    live_rows = [row for row in rows if row["review_scope"] == REVIEW_NOW]
    deferred_rows = [row for row in rows if row["review_scope"] == DEFERRED]
    live_decisions = Counter(row["final_decision"] or "BLANK" for row in live_rows)
    deferred_by_region: dict[str, Counter[str]] = defaultdict(Counter)
    for row in deferred_rows:
        deferred_by_region[row["regional_slice"]][
            row["final_decision"] or "BLANK"
        ] += 1

    lines = [
        "# England-wide Teaching Vacancies admin/service manual review",
        "",
        "Edit only the `action:` line in each block:",
        "",
        "- For a selected job, use `action: exclude` to remove it.",
        "- For a possible job, use `action: select` to add it.",
        "- Leave `action:` blank for no change.",
        "- Manual edits are matched by `source_job_id`.",
        "- Only LIVE Ontap regions appear as individual review blocks.",
        "- This England-wide file is the review surface; regional files remain the approval boundaries.",
        "",
        "## TOTALS",
        "",
        f"- All routed roles: **{len(rows)}**",
        f"- REVIEW NOW (LIVE regions): **{len(live_rows)}**",
        f"- DEFERRED - REGION NOT LIVE: **{len(deferred_rows)}**",
        f"- SELECTED: **{live_decisions['SELECTED']}**",
        f"- POSS: **{live_decisions['POSS']}**",
        f"- HARD PASS / EXCLUDED: **{live_decisions['HARD_PASS'] + live_decisions['EXCLUDED']}**",
        "",
    ]

    regions = sorted(
        {row["ontap_region"] for row in live_rows if row["ontap_region"]},
        key=str.casefold,
    )
    for region in regions:
        region_rows = [row for row in live_rows if row["ontap_region"] == region]
        for decision, heading in (("SELECTED", "SELECTED"), ("POSS", "POSSIBLES")):
            grouped = [row for row in region_rows if row["final_decision"] == decision]
            lines.extend([f"## {region.upper()} — {heading}", ""])
            if not grouped:
                lines.extend(["_No jobs in this group._", ""])
                continue
            for row in grouped:
                lines.extend(_review_block(row))

    lines.extend(
        [
            "## DEFERRED REGIONS — NOT FOR MANUAL REVIEW",
            "",
            "These roles remain visible in the CSV but are not individually marked until the corresponding Ontap regional slice goes LIVE.",
            "",
            "| Region | Total | Selected | POSS | Hard pass / excluded |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for region in sorted(deferred_by_region, key=str.casefold):
        counts = deferred_by_region[region]
        lines.append(
            f"| {_md(region)} | {sum(counts.values())} | {counts['SELECTED']} | "
            f"{counts['POSS']} | {counts['HARD_PASS'] + counts['EXCLUDED']} |"
        )
    lines.append("")
    return "\n".join(lines)


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
    parser.add_argument(
        "--output-summary",
        type=Path,
        default=Path(
            "reviews/external/teaching-vacancies/"
            "england-wide-admin-service-summary.md"
        ),
    )
    parser.add_argument("--write-master-review", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.write_master_review:
        raise SystemExit(
            "STOP: add --write-master-review to create the review-only master outputs."
        )
    rows = build_master_rows(args.review_dir)
    if not rows:
        raise SystemExit("STOP: no regional review rows found for the master outputs.")
    discovery.write_bytes_atomic(args.output_csv, master_csv_bytes(rows))
    discovery.write_bytes_atomic(
        args.output_summary, master_summary_text(rows).encode("utf-8")
    )
    print(
        f"Teaching Vacancies master review wrote {len(rows)} rows plus the "
        "England-wide summary; regional controls remain unchanged and no jobs "
        "were published."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

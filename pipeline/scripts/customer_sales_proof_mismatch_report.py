"""Reconcile national Customer Sales candidates against proof-slice outputs.

Diagnostic only. Runs after targeted pipeline + expansion + refinement.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

REPORT_DIR = Path("reports-daily")
DETAIL_PATH = REPORT_DIR / "customer-sales-national-detail.csv"
OUT_PATH = REPORT_DIR / "customer-sales-proof-slice-mismatches.md"
OUTPUT_DIR = Path("output-customer-sales-test")

PROOF = {
    "Hampshire": "hampshire.json",
    "Greater Manchester - Manchester & Salford": "manchester-salford.json",
    "Yorkshire - West": "west-yorkshire.json",
}


def as_bool(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.lower().isin({"true", "1", "yes"})


def main() -> None:
    detail = pd.read_csv(DETAIL_PATH, dtype=str).fillna("")
    detail["in_scope_bool"] = as_bool(detail["in_scope"])
    detail["campaign_rep_bool"] = as_bool(detail["campaign_representative"])

    lines = [
        "# Customer Sales proof-slice reconciliation",
        "",
        "Compares national in-scope campaign representatives with the final targeted proof-slice JSON after expansion + QA refinement.",
        "",
    ]

    mismatch_total = 0
    for region, filename in PROOF.items():
        national = detail[
            (detail["region"] == region)
            & detail["in_scope_bool"]
            & detail["campaign_rep_bool"]
        ].copy()
        national_ids = set(national["job_id"].astype(str))

        path = OUTPUT_DIR / filename
        jobs = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
        target_by_id = {str(job.get("job_id", "")): job for job in jobs if str(job.get("job_id", ""))}
        target_ids = set(target_by_id)

        national_only = sorted(national_ids - target_ids)
        target_only = sorted(target_ids - national_ids)
        mismatch_total += len(national_only) + len(target_only)

        lines += [
            f"## {region}",
            "",
            f"National deduped: **{len(national_ids)}** | Final proof output: **{len(target_ids)}**",
            "",
        ]

        if not national_only and not target_only:
            lines += ["**MATCH — no discrepancy.**", ""]
            continue

        if national_only:
            lines += ["### National-only", "", "| Job | Employer | Location | National reason |", "|---|---|---|---|"]
            subset = national[national["job_id"].astype(str).isin(national_only)]
            for _, row in subset.iterrows():
                lines.append(
                    f"| {row['title']} | {row['employer']} | {row['area'] or row['location']} | {row['decision_reason']} |"
                )
            lines.append("")

        if target_only:
            lines += ["### Proof-output-only", "", "| Job | Employer | Location | Classification |", "|---|---|---|---|"]
            for job_id in target_only:
                job = target_by_id[job_id]
                lines.append(
                    f"| {job.get('title','')} | {job.get('advertiser_name','')} | {job.get('location','')} | {job.get('customer_sales_classification','')} |"
                )
            lines.append("")

    lines += ["## Result", "", f"Total mismatched rows across proof slices: **{mismatch_total}**", ""]
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Proof-slice mismatch rows: {mismatch_total}")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()

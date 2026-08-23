"""Branch-only Legal Assistant / Paralegal proof-region selector.

Uses the governed reusable family-discovery output as the occupational selector, then
joins accepted content-unique JobG8 rows back to the current feed to produce inspectable
proof slices. This is test evidence only: it does not touch the LIVE slice register,
production output or public pages.

The workflow deliberately rebuilds discovery from current main inputs before this
selector runs, so proof output never depends on a stale branch-side feed snapshot.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from scripts.service_admin_pipeline_core import (
    COL,
    build_company,
    build_salary_details,
    clean_description,
    clean_record_strings,
    format_number,
    get_posted_date,
    norm,
)

INPUT_PATH = Path("input/jobg8.xlsx")
DISCOVERY_PATH = Path("reports-discovery-audit/jobg8-legal-assistant-paralegal-discovery-current.csv")
OUTPUT_DIR = Path("output-legal-assistant-test")

TARGETS = {
    "London": "london.json",
    "Norfolk": "norfolk.json",
    "Bristol & Bath": "bristol-bath.json",
}

DISPLAY_REF_COL = "/Job/DisplayReference"
REQUIRED_COLUMNS = [
    COL["job_id"], COL["title"], COL["advertiser_name"], COL["advertiser_type"],
    COL["employment_type"], COL["area"], COL["location"], COL["apply_url"], COL["description"],
]


def falseish(value: object) -> bool:
    return str(value).strip().casefold() in {"", "false", "0", "no"}


def main() -> None:
    if not INPUT_PATH.exists():
        raise SystemExit(f"STOP: missing {INPUT_PATH}")
    if not DISCOVERY_PATH.exists():
        raise SystemExit(f"STOP: missing {DISCOVERY_PATH}; run family discovery first")

    discovery = pd.read_csv(DISCOVERY_PATH, dtype=str).fillna("")
    required_discovery = {"display_reference", "assessable_market", "provisional_decision"}
    missing_discovery = sorted(required_discovery - set(discovery.columns))
    if missing_discovery:
        raise SystemExit("STOP: discovery output missing columns: " + ", ".join(missing_discovery))

    accepted = discovery.loc[
        discovery["provisional_decision"].eq("LIKELY_IN")
        & discovery["assessable_market"].isin(TARGETS)
    ].copy()
    if "is_duplicate" in accepted.columns:
        accepted = accepted.loc[accepted["is_duplicate"].map(falseish)]
    if "is_content_duplicate" in accepted.columns:
        accepted = accepted.loc[accepted["is_content_duplicate"].map(falseish)]

    accepted_by_ref = {
        norm(row["display_reference"]): {
            "region": norm(row["assessable_market"]),
            "decision": norm(row["provisional_decision"]),
            "reason": norm(row.get("provisional_reason", "")),
        }
        for _, row in accepted.iterrows()
        if norm(row["display_reference"])
    }

    raw = pd.read_excel(INPUT_PATH, dtype=str).fillna("")
    missing = [column for column in REQUIRED_COLUMNS if column not in raw.columns]
    if DISPLAY_REF_COL not in raw.columns:
        missing.append(DISPLAY_REF_COL)
    if missing:
        raise SystemExit("STOP: missing JobG8 columns: " + ", ".join(sorted(set(missing))))

    outputs: dict[str, list[dict[str, Any]]] = {region: [] for region in TARGETS}
    df_columns = list(raw.columns)
    seen_refs: set[str] = set()

    for _, row in raw.iterrows():
        ref = norm(row.get(DISPLAY_REF_COL, ""))
        match = accepted_by_ref.get(ref)
        if not match or ref in seen_refs:
            continue

        title = norm(row.get(COL["title"]))
        apply_url = norm(row.get(COL["apply_url"]))
        raw_description = norm(row.get(COL["description"]))
        job_id = norm(row.get(COL["job_id"]))
        if not job_id or not title or not raw_description or not apply_url.lower().startswith("http"):
            continue

        region = match["region"]
        description = clean_description(raw_description)
        salary_text, _salary_source = build_salary_details(row)
        item = clean_record_strings({
            "job_id": job_id,
            "display_reference": ref,
            "title": title,
            "company": build_company(row),
            "advertiser_name": norm(row.get(COL["advertiser_name"])),
            "advertiser_type": norm(row.get(COL["advertiser_type"])),
            "location": norm(row.get(COL["location"])) or norm(row.get(COL["area"])),
            "region": region,
            "country": "UK",
            "category": "Legal Assistant / Paralegal",
            "employment_type": norm(row.get(COL["employment_type"])),
            "salary_min": format_number(row.get(COL["salary_min"])),
            "salary_max": format_number(row.get(COL["salary_max"])),
            "salary_text": salary_text,
            "posted_date": get_posted_date(row, df_columns),
            "description": description,
            "apply_url": apply_url,
            "source": "JobG8",
            "legal_discovery_decision": match["decision"],
            "legal_discovery_reason": match["reason"],
            "proof_stage_only": True,
        })
        outputs[region].append(item)
        seen_refs.add(ref)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for region, filename in TARGETS.items():
        jobs = sorted(outputs[region], key=lambda job: (
            str(job.get("title", "")).casefold(),
            str(job.get("location", "")).casefold(),
            str(job.get("company", "")).casefold(),
        ))
        (OUTPUT_DIR / filename).write_text(
            json.dumps(jobs, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        employers = {
            str(job.get("advertiser_name", "")).strip().casefold()
            for job in jobs if str(job.get("advertiser_name", "")).strip()
        }
        print(f"{region}: {len(jobs)} jobs / {len(employers)} advertisers")


if __name__ == "__main__":
    main()

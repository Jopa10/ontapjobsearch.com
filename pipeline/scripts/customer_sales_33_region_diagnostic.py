"""Run the governed Customer Sales family boundary across Ontap's current 33 regions.

Diagnostic only. This script does not publish Customer Sales pages or change LIVE
slice state. It intentionally reuses the proof selector, guarded account-role pass
and QA refinement functions so national validation cannot silently drift away from
the three-region proof rules.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

from scripts.customer_sales_test_expand import (
    CONDITIONAL_TITLES,
    EXCLUDES as ACCOUNT_EXCLUDES,
    OFFICE_EVIDENCE,
    SALES_EVIDENCE as ACCOUNT_SALES_EVIDENCE,
    has_any,
)
from scripts.customer_sales_test_pipeline import classify as classify_proof_core
from scripts.customer_sales_test_refine import keep_job, load_title_location_lookup
from scripts.service_admin_pipeline_core import COL, norm, norm_key

INPUT_PATH = Path("input/jobg8.xlsx")
GEO_PATH = Path("geo/geo_lookup.xlsx")
REPORT_DIR = Path("reports-daily")
REGION_CSV_PATH = REPORT_DIR / "customer-sales-33-region-diagnostic.csv"
DETAIL_CSV_PATH = REPORT_DIR / "customer-sales-33-region-detail.csv"
MD_PATH = REPORT_DIR / "customer-sales-33-region-diagnostic.md"
REPO_ROOT = Path(__file__).resolve().parents[2]
AREA_UNUSABLE = {"", "not specified", "unknown"}


def git_show_text(path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"origin/main:{path}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else ""


def git_show_json(path: str) -> Any:
    text = git_show_text(path)
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def load_current_region_catalog() -> dict[str, str]:
    catalog = git_show_json("pipeline/config/job_slice_catalog.json")
    if not isinstance(catalog, dict):
        raise SystemExit("STOP: could not read current main job_slice_catalog.json")
    regions = catalog.get("regions")
    if not isinstance(regions, dict):
        raise SystemExit("STOP: current main job slice catalog has no regions object")

    result: dict[str, str] = {}
    for region, meta in regions.items():
        if not isinstance(meta, dict):
            continue
        slug = str(meta.get("slug", "")).strip()
        if region and slug:
            result[str(region).strip()] = slug
    if len(result) != 33:
        raise SystemExit(f"STOP: expected 33 Ontap regions from main catalog; found {len(result)}")
    return result


def canonical_region(value: Any) -> str:
    region = norm(value)
    if region.startswith("North East - "):
        return "North East"
    return region


def load_geo() -> tuple[dict[str, str], dict[str, str]]:
    geo = pd.read_excel(GEO_PATH, dtype=str).fillna("")
    if not {"Area", "Cluster"}.issubset(geo.columns):
        raise SystemExit("STOP: geo lookup requires Area and Cluster columns")

    area_lookup: dict[str, str] = {}
    for _, row in geo.iterrows():
        area = norm_key(row.get("Area"))
        region = canonical_region(row.get("Cluster"))
        if area and region:
            area_lookup[area] = region

    fallback_lookup: dict[str, str] = {}
    try:
        fallback = pd.read_excel(GEO_PATH, sheet_name="LocationFallback", dtype=str).fillna("")
    except ValueError:
        fallback = pd.DataFrame()
    if {"Status", "Location", "Cluster"}.issubset(fallback.columns):
        for _, row in fallback.iterrows():
            if norm_key(row.get("Status")) != "auto":
                continue
            location = norm_key(row.get("Location"))
            region = canonical_region(row.get("Cluster"))
            if location and location not in AREA_UNUSABLE and region:
                fallback_lookup[location] = region

    return area_lookup, fallback_lookup


def resolve_region(
    area: Any,
    location: Any,
    area_lookup: dict[str, str],
    fallback_lookup: dict[str, str],
) -> str:
    area_key = norm_key(area)
    if area_key not in AREA_UNUSABLE:
        return area_lookup.get(area_key, "")
    location_key = norm_key(location)
    if location_key in AREA_UNUSABLE:
        return ""
    return fallback_lookup.get(location_key, "")


def classify_candidate(title: str, description: str) -> tuple[str, str] | None:
    core = classify_proof_core(title, description)
    if core:
        return core

    title_key = norm_key(title)
    if not has_any(title_key, CONDITIONAL_TITLES):
        return None

    combined = f"{title_key} {norm_key(description)}"
    if has_any(combined, ACCOUNT_EXCLUDES):
        return None
    if not has_any(combined, ACCOUNT_SALES_EVIDENCE):
        return None
    if not has_any(combined, OFFICE_EVIDENCE):
        return None
    return (
        "CONDITIONAL_ACCOUNT_SALES",
        "account-based title with sales and office/digital evidence",
    )


def normalise_campaign_text(value: Any) -> str:
    text = norm_key(value)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\b\d{4,}\b", "#", text)
    text = re.sub(r"[^a-z0-9£%+#]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def campaign_key(region: str, employer: str, description: str, title: str) -> str:
    desc = normalise_campaign_text(description)
    if len(desc) >= 120:
        basis = f"{norm_key(region)}|{norm_key(employer)}|{desc}"
    else:
        basis = f"{norm_key(region)}|{norm_key(employer)}|{norm_key(title)}|{desc}"
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


def load_main_service_admin_ids(region_slugs: dict[str, str]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for region, slug in region_slugs.items():
        data = git_show_json(f"app/{slug}/service-administrator-jobs.json")
        ids: set[str] = set()
        if isinstance(data, list):
            for job in data:
                if isinstance(job, dict):
                    job_id = str(job.get("job_id", "")).strip()
                    if job_id:
                        ids.add(job_id)
        result[region] = ids
    return result


def volume_band(count: int) -> str:
    if count >= 6:
        return "6_PLUS"
    if count >= 3:
        return "3_TO_5"
    if count >= 1:
        return "1_TO_2"
    return "ZERO"


def main() -> None:
    if not INPUT_PATH.exists():
        raise SystemExit(f"STOP: missing {INPUT_PATH}")
    if not GEO_PATH.exists():
        raise SystemExit(f"STOP: missing {GEO_PATH}")

    region_slugs = load_current_region_catalog()
    region_names = set(region_slugs)
    service_admin_ids = load_main_service_admin_ids(region_slugs)
    area_lookup, fallback_lookup = load_geo()
    title_location_lookup = load_title_location_lookup()

    feed = pd.read_excel(INPUT_PATH, dtype=str).fillna("")
    required = [
        COL["job_id"],
        COL["title"],
        COL["advertiser_name"],
        COL["area"],
        COL["location"],
        COL["apply_url"],
        COL["description"],
    ]
    missing = [column for column in required if column not in feed.columns]
    if missing:
        raise SystemExit("STOP: missing JobG8 columns: " + ", ".join(missing))

    selected_rows: list[dict[str, Any]] = []
    seen_job_region: set[tuple[str, str]] = set()

    for _, row in feed.iterrows():
        title = norm(row.get(COL["title"]))
        description = norm(row.get(COL["description"]))
        job_id = norm(row.get(COL["job_id"]))
        apply_url = norm(row.get(COL["apply_url"]))
        if not title or not description or not job_id or not apply_url.lower().startswith("http"):
            continue

        region = resolve_region(
            row.get(COL["area"]),
            row.get(COL["location"]),
            area_lookup,
            fallback_lookup,
        )
        if region not in region_names:
            continue
        if (region, job_id) in seen_job_region:
            continue

        decision = classify_candidate(title, description)
        if not decision:
            continue
        classification, reason = decision

        qa_job = {
            "job_id": job_id,
            "title": title,
            "description": description,
            "region": region,
            "customer_sales_classification": classification,
        }
        keep, qa_reason = keep_job(qa_job, title_location_lookup)
        if not keep:
            continue

        employer = norm(row.get(COL["advertiser_name"])) or "Unknown company"
        location = norm(row.get(COL["area"])) or norm(row.get(COL["location"]))
        selected_rows.append(
            {
                "job_id": job_id,
                "title": title,
                "employer": employer,
                "location": location,
                "region": region,
                "classification": classification,
                "selection_reason": reason,
                "boundary_review": classification == "CONDITIONAL_ACCOUNT_SALES",
                "service_admin_overlap": job_id in service_admin_ids.get(region, set()),
                "campaign_key": campaign_key(region, employer, description, title),
            }
        )
        seen_job_region.add((region, job_id))

    detail = pd.DataFrame(selected_rows)
    if detail.empty:
        raise SystemExit("STOP: governed Customer Sales boundary selected zero jobs")

    detail["campaign_representative"] = False
    representatives = detail.groupby(["region", "campaign_key"], sort=False).head(1).index
    detail.loc[representatives, "campaign_representative"] = True

    region_rows: list[dict[str, Any]] = []
    for region in region_slugs:
        group = detail[detail["region"] == region]
        deduped = group[group["campaign_representative"]]
        employer_counts = Counter(deduped["employer"].astype(str))
        top_employer = ""
        top_count = 0
        if employer_counts:
            top_employer, top_count = employer_counts.most_common(1)[0]
        jobs = len(deduped)
        top_share = round((top_count / jobs) * 100, 1) if jobs else 0.0
        classification_counts = Counter(deduped["classification"].astype(str))
        overlap = int(deduped["service_admin_overlap"].sum()) if jobs else 0
        employers_3_plus = sum(1 for count in employer_counts.values() if count >= 3)

        region_rows.append(
            {
                "region": region,
                "selected_rows_before_campaign_dedupe": len(group),
                "campaign_deduped_jobs": jobs,
                "duplicate_campaign_rows_removed": len(group) - jobs,
                "unique_employers": len(employer_counts),
                "top_employer": top_employer,
                "top_employer_jobs": top_count,
                "top_employer_share_pct": top_share,
                "employers_with_3_plus_jobs": employers_3_plus,
                "direct_sales": classification_counts.get("DIRECT_SALES", 0),
                "customer_sales_crossover": classification_counts.get("CUSTOMER_SALES", 0),
                "conditional_account_sales": classification_counts.get("CONDITIONAL_ACCOUNT_SALES", 0),
                "also_in_current_main_service_admin": overlap,
                "incremental_vs_current_main_service_admin": jobs - overlap,
                "volume_band": volume_band(jobs),
                "concentration_flag": jobs >= 3 and top_share >= 40.0,
            }
        )

    region_df = pd.DataFrame(region_rows)
    region_df = region_df.sort_values(
        ["campaign_deduped_jobs", "unique_employers", "region"],
        ascending=[False, False, True],
    ).reset_index(drop=True)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    detail.sort_values(["region", "classification", "employer", "title"]).to_csv(
        DETAIL_CSV_PATH, index=False
    )
    region_df.to_csv(REGION_CSV_PATH, index=False)

    total_jobs = int(region_df["campaign_deduped_jobs"].sum())
    total_overlap = int(region_df["also_in_current_main_service_admin"].sum())
    regions_6_plus = int((region_df["campaign_deduped_jobs"] >= 6).sum())
    account_jobs = int(region_df["conditional_account_sales"].sum())
    concentration_regions = int(region_df["concentration_flag"].sum())

    lines = [
        "# Customer Sales — governed 33-region diagnostic",
        "",
        "Diagnostic only. No Customer Sales slice is LIVE and no production selector is changed.",
        "",
        f"- Current JobG8 rows analysed: {len(feed)}",
        f"- Campaign-deduped Customer Sales jobs across the 33 regions: {total_jobs}",
        f"- Exact overlap with current main Service Admin pages: {total_overlap}",
        f"- Incremental versus current main Service Admin pages: {total_jobs - total_overlap}",
        f"- Regions with 6+ jobs: {regions_6_plus}",
        f"- Conditional account-role jobs requiring boundary attention: {account_jobs}",
        f"- Regions with >=40% top-employer concentration (where 3+ jobs): {concentration_regions}",
        "",
        "| Region | Jobs | Employers | Direct | Customer crossover | Account review | Service Admin overlap | Top employer share | 3+ employer groups | Band |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for _, row in region_df.iterrows():
        lines.append(
            "| {region} | {jobs} | {employers} | {direct} | {customer} | {account} | {overlap} | {share:.1f}% | {campaigns} | {band} |".format(
                region=row["region"],
                jobs=int(row["campaign_deduped_jobs"]),
                employers=int(row["unique_employers"]),
                direct=int(row["direct_sales"]),
                customer=int(row["customer_sales_crossover"]),
                account=int(row["conditional_account_sales"]),
                overlap=int(row["also_in_current_main_service_admin"]),
                share=float(row["top_employer_share_pct"]),
                campaigns=int(row["employers_with_3_plus_jobs"]),
                band=row["volume_band"],
            )
        )

    lines.extend(
        [
            "",
            "## Interpretation guardrails",
            "",
            "`6_PLUS` is a diagnostic volume band, not LIVE approval.",
            "Conditional Account Manager / Account Executive jobs remain visible for review rather than silently becoming automatic title approvals.",
            "Sales + Service Admin overlap is allowed; the overlap column is informational, not an exclusion rule.",
            "Employer concentration and campaign dedupe must be reviewed before any region is proposed for LIVE status.",
            "",
        ]
    )
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")

    print(f"Customer Sales governed 33-region diagnostic: {total_jobs} campaign-deduped jobs")
    print(f"Service Admin exact-ID overlap: {total_overlap}; incremental: {total_jobs - total_overlap}")
    print(f"Regions with 6+ jobs: {regions_6_plus}")
    print(f"Conditional account-role jobs: {account_jobs}")
    print(f"Wrote {REGION_CSV_PATH}")
    print(f"Wrote {DETAIL_CSV_PATH}")
    print(f"Wrote {MD_PATH}")


if __name__ == "__main__":
    main()

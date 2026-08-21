"""Second-pass QA filter for the branch-only Customer Sales test family.

Keeps genuine office/contact-centre/customer-led sales while removing obvious
non-sales customer service, field/event campaign sales, specialist/senior sales,
automotive dealership sales, and title/location conflicts. Overlap with Service
Admin is deliberately allowed.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

OUTPUT_DIR = Path("output-customer-sales-test")
GEO_PATH = Path("geo/geo_lookup.xlsx")
REPORT_PATH = OUTPUT_DIR / "refinement-report.json"

STRONG_CUSTOMER_SALES_EVIDENCE = [
    "commission", "uncapped commission", "sales target", "sales targets",
    "sales opportunity", "sales opportunities", "upsell", "up-sell",
    "cross-sell", "cross sell", "convert enquiries", "convert inquiries",
    "convert leads", "convert prospects", "convert interest", "conversion target",
    "conversion targets", "warm leads", "warm enquiries", "warm inquiries",
    "inbound sales", "outbound sales", "telesales", "telephone sales",
    "cold calling", "new business", "lead generation", "sales pipeline",
    "close sales", "closing sales", "close deals", "closing deals",
    "booked and paid", "retention target", "renewal target", "renewals",
    "retain customers", "increase membership", "sales experience", "sales role",
]

CUSTOMER_TITLE_EXCLUDES = [
    "strategic customer success manager", "enterprise customer success manager",
    "senior customer success manager",
]

DIRECT_DESCRIPTION_EXCLUDES = [
    "door to door", "door-to-door", "event-based campaigns",
    "face-to-face sales environments", "travel to different campaign locations",
    "subcontracted basis", "self-employed", "self employed",
    "commission-only", "commission only",
]

# Direct titles such as "Sales Executive" are too generic to identify showroom/car
# sales from title alone, so catch unmistakable dealership context in the advert body.
AUTOMOTIVE_DESCRIPTION_EXCLUDES = [
    "car dealership", "vehicle dealership", "motor dealership",
    "buying their car", "buying a new car", "buying a used car",
    "new & used vehicles", "new and used vehicles", "used car sales",
    "new car sales", "vehicle presentations", "test drives",
]

DIRECT_TITLE_EXCLUDES = [
    "product sales executive", "senior sales executive", "senior sales consultant",
]


def norm(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def contains_any(text: str, terms: list[str]) -> list[str]:
    return [term for term in terms if term in text]


def load_title_location_lookup() -> list[tuple[str, str]]:
    if not GEO_PATH.exists():
        return []

    pairs: dict[str, str] = {}
    try:
        geo = pd.read_excel(GEO_PATH, dtype=str).fillna("")
        if {"Area", "Cluster"}.issubset(geo.columns):
            for _, row in geo.iterrows():
                place = norm(row.get("Area"))
                cluster = str(row.get("Cluster", "")).strip()
                if len(place) >= 4 and cluster:
                    pairs.setdefault(place, cluster)
    except Exception:
        pass

    try:
        fallback = pd.read_excel(GEO_PATH, sheet_name="LocationFallback", dtype=str).fillna("")
        if {"Location", "Cluster"}.issubset(fallback.columns):
            for _, row in fallback.iterrows():
                status = norm(row.get("Status"))
                if status and status != "auto":
                    continue
                place = norm(row.get("Location"))
                cluster = str(row.get("Cluster", "")).strip()
                if len(place) >= 4 and place not in {"not specified", "unknown"} and cluster:
                    pairs.setdefault(place, cluster)
    except Exception:
        pass

    return sorted(pairs.items(), key=lambda item: len(item[0]), reverse=True)


def title_location_conflict(title: str, region: str, lookup: list[tuple[str, str]]) -> str | None:
    t = norm(title)
    region_norm = norm(region)
    for place, cluster in lookup:
        if re.search(rf"(?<![a-z0-9]){re.escape(place)}(?![a-z0-9])", t):
            if norm(cluster) != region_norm:
                return f"title location '{place}' maps to {cluster}, not {region}"
            return None
    return None


def keep_job(job: dict, lookup: list[tuple[str, str]]) -> tuple[bool, str]:
    title = norm(job.get("title"))
    description = norm(job.get("description"))
    combined = f"{title} {description}"
    classification = str(job.get("customer_sales_classification", ""))
    region = str(job.get("region", ""))

    conflict = title_location_conflict(title, region, lookup)
    if conflict:
        return False, conflict

    if classification == "CUSTOMER_SALES":
        title_excludes = contains_any(title, CUSTOMER_TITLE_EXCLUDES)
        if title_excludes:
            return False, "senior/specialist customer-success title: " + ", ".join(title_excludes)
        evidence = contains_any(combined, STRONG_CUSTOMER_SALES_EVIDENCE)
        if not evidence:
            return False, "customer/service role has no strong sales/conversion evidence"

    if classification == "DIRECT_SALES":
        title_excludes = contains_any(title, DIRECT_TITLE_EXCLUDES)
        if title_excludes:
            return False, "specialist/senior direct-sales title: " + ", ".join(title_excludes)
        automotive_excludes = contains_any(description, AUTOMOTIVE_DESCRIPTION_EXCLUDES)
        if automotive_excludes:
            return False, "automotive dealership/showroom sales signal: " + ", ".join(automotive_excludes[:3])
        description_excludes = contains_any(description, DIRECT_DESCRIPTION_EXCLUDES)
        if description_excludes:
            return False, "field/event/self-employed sales signal: " + ", ".join(description_excludes[:3])

    return True, ""


def main() -> None:
    lookup = load_title_location_lookup()
    report: dict[str, dict] = {}

    for path in sorted(OUTPUT_DIR.glob("*.json")):
        if path.name == REPORT_PATH.name:
            continue
        try:
            jobs = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(jobs, list):
            continue

        kept: list[dict] = []
        removed: list[dict] = []
        for job in jobs:
            if not isinstance(job, dict):
                continue
            keep, reason = keep_job(job, lookup)
            if keep:
                kept.append(job)
            else:
                removed.append({
                    "job_id": job.get("job_id", ""),
                    "title": job.get("title", ""),
                    "location": job.get("location", ""),
                    "region": job.get("region", ""),
                    "reason": reason,
                })

        path.write_text(json.dumps(kept, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report[path.name] = {
            "before": len(jobs),
            "after": len(kept),
            "removed": removed,
        }
        print(f"{path.name}: {len(jobs)} -> {len(kept)} jobs ({len(removed)} removed)")

    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

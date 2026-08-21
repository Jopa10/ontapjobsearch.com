"""Final QA pass for LIVE Customer Sales outputs.

This is the production equivalent of the proof-region refinement stage. It keeps
legitimate office/contact-centre/home/hybrid sales (including Service Admin
crossover) while fail-closing weak customer-service evidence, obvious geography
conflicts, field/in-home campaigns, dealership/retail/property sales and senior or
specialist customer-service/account contamination.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

from .slice_catalog import category_meta, output_filename
from .slice_registry import live_slices

CATEGORY = "customer_sales"
GEO_PATH = Path("geo/geo_lookup.xlsx")

STRONG_CUSTOMER_SALES_EVIDENCE = [
    "commission", "uncapped commission", "sales target", "sales targets",
    "sales opportunity", "sales opportunities", "upsell", "up-sell",
    "cross-sell", "cross sell", "convert enquiries", "convert inquiries",
    "convert leads", "convert prospects", "convert interest", "conversion target",
    "conversion targets", "warm leads", "warm enquiries", "warm inquiries",
    "inbound sales", "outbound sales", "telesales", "telephone sales",
    "cold calling", "new business", "lead generation", "sales pipeline",
    "close sales", "closing sales", "close deals", "closing deals",
    "booked and paid", "retention target", "renewal target",
    "retain customers", "increase membership", "sales experience", "sales role",
]

CUSTOMER_TITLE_EXCLUDES = [
    "strategic customer success manager", "enterprise customer success manager",
    "senior customer success manager", "client services manager", "client service manager",
]

# These signals are outside the agreed office/contact-centre/home/hybrid seam for
# every Customer Sales classification, not only roles with a direct sales title.
OUT_OF_BOUND_DESCRIPTION_EXCLUDES = [
    "door to door", "door-to-door", "event-based campaigns",
    "face-to-face sales environments", "face-to-face customer engagement",
    "face to face customer engagement", "high-footfall venues", "high footfall venues",
    "retail spaces and events", "travel to different campaign locations",
    "subcontracted basis", "self-employed", "self employed",
    "commission-only", "commission only", "in-home consultation",
    "in home consultation", "visit customers in their homes",
    "visit customers at home", "travel time from your home postcode",
    "transforming kitchens", "kitchen transformation journey", "kitchen makeovers",
    "kitchen makeover", "kitchen transformation", "home improvement campaign",
]

AUTOMOTIVE_CONTEXT_EXCLUDES = [
    "car dealership", "vehicle dealership", "motor dealership", "motor group",
    "car dealer", "vehicle dealer", "main dealership", "franchised dealership",
    "buying their car", "buying a new car", "buying a used car",
    "new & used vehicles", "new and used vehicles", "used car sales",
    "new car sales", "vehicle presentations", "test drives",
]

RETAIL_PROPERTY_DESCRIPTION_EXCLUDES = [
    "luxury retail", "premium retail", "retail environment", "shop floor",
    "luxury jewellery", "fine timepieces", "estate agency", "house builder",
    "new homes development",
]

SPECIALIST_ACCOUNT_CONTEXT_EXCLUDES = [
    "rare cask assets", "premium whisky casks", "whisky cask",
    "new investment opportunities", "investment opportunity", "investment opportunities",
    "supply-constrained asset class", "asset class", "private client investment",
]

DIRECT_TITLE_EXCLUDES = [
    "product sales executive", "senior sales executive", "senior sales consultant",
    "conservatory sales", "new homes sales", "luxury sales consultant",
]

LOCATION_IGNORE = {
    "city", "town", "county", "remote", "home", "home based", "home-based",
    "england", "uk", "united kingdom", "nationwide",
}


def norm(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def canonical_region(value: object) -> str:
    region = str(value or "").strip()
    if region.startswith("North East - "):
        return "North East"
    return region


def contains_any(text: str, terms: list[str]) -> list[str]:
    return [term for term in terms if term in text]


def load_location_lookup() -> list[tuple[str, str]]:
    if not GEO_PATH.exists():
        return []

    pairs: dict[str, str] = {}
    geo = pd.read_excel(GEO_PATH, dtype=str).fillna("")
    if {"Area", "Cluster"}.issubset(geo.columns):
        for _, row in geo.iterrows():
            place = norm(row.get("Area"))
            region = canonical_region(row.get("Cluster"))
            if len(place) >= 4 and place not in LOCATION_IGNORE and region:
                pairs.setdefault(place, region)

    try:
        fallback = pd.read_excel(GEO_PATH, sheet_name="LocationFallback", dtype=str).fillna("")
    except ValueError:
        fallback = pd.DataFrame()
    if {"Location", "Cluster"}.issubset(fallback.columns):
        for _, row in fallback.iterrows():
            status = norm(row.get("Status"))
            if status and status != "auto":
                continue
            place = norm(row.get("Location"))
            region = canonical_region(row.get("Cluster"))
            if len(place) >= 4 and place not in LOCATION_IGNORE and region:
                pairs.setdefault(place, region)

    return sorted(pairs.items(), key=lambda item: len(item[0]), reverse=True)


def _places_in(text: str, lookup: list[tuple[str, str]]) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for place, region in lookup:
        if re.search(rf"(?<![a-z0-9]){re.escape(place)}(?![a-z0-9])", text):
            found.append((place, region))
    return found


def location_conflict(title: str, description: str, region: str, lookup: list[tuple[str, str]]) -> str | None:
    target = norm(canonical_region(region))

    title_places = _places_in(norm(title), lookup)
    if title_places:
        if any(norm(mapped) == target for _, mapped in title_places):
            return None
        place, mapped = title_places[0]
        return f"title location '{place}' maps to {mapped}, not {region}"

    # Many JobG8 rows have generic Area/Location values while the true place is
    # stated at the very start of the advert. Limit this guard to the opening copy
    # so later references to customers/territories do not create false conflicts.
    opening = norm(description)[:240]
    opening_places = _places_in(opening, lookup)
    if opening_places and not any(norm(mapped) == target for _, mapped in opening_places):
        place, mapped = opening_places[0]
        return f"advert opening location '{place}' maps to {mapped}, not {region}"
    return None


def keep_job(job: dict, lookup: list[tuple[str, str]]) -> tuple[bool, str]:
    title = norm(job.get("title"))
    description = norm(job.get("description"))
    employer = norm(job.get("advertiser_name")) or norm(job.get("company"))
    combined = f"{title} {description}"
    context = f"{title} {description} {employer}"
    classification = str(job.get("customer_sales_classification", ""))
    region = str(job.get("region", ""))

    conflict = location_conflict(title, description, region, lookup)
    if conflict:
        return False, conflict

    out_of_bound = contains_any(description, OUT_OF_BOUND_DESCRIPTION_EXCLUDES)
    if out_of_bound:
        return False, "field/event/self-employed sales signal: " + ", ".join(out_of_bound[:3])

    if classification == "CUSTOMER_SALES":
        title_excludes = contains_any(title, CUSTOMER_TITLE_EXCLUDES)
        if title_excludes:
            return False, "senior/specialist customer-success title: " + ", ".join(title_excludes)
        evidence = contains_any(combined, STRONG_CUSTOMER_SALES_EVIDENCE)
        if not evidence:
            return False, "customer/service role has no strong sales/conversion evidence"

    if classification == "CONDITIONAL_ACCOUNT_SALES":
        specialist_excludes = contains_any(context, SPECIALIST_ACCOUNT_CONTEXT_EXCLUDES)
        if specialist_excludes:
            return False, "specialist investment/account-sales signal: " + ", ".join(specialist_excludes[:3])

    if classification == "DIRECT_SALES":
        title_excludes = contains_any(title, DIRECT_TITLE_EXCLUDES)
        if title_excludes:
            return False, "out-of-bound direct-sales title: " + ", ".join(title_excludes)
        automotive_excludes = contains_any(context, AUTOMOTIVE_CONTEXT_EXCLUDES)
        if automotive_excludes:
            return False, "automotive dealership/showroom sales signal: " + ", ".join(automotive_excludes[:3])
        retail_property_excludes = contains_any(description, RETAIL_PROPERTY_DESCRIPTION_EXCLUDES)
        if retail_property_excludes:
            return False, "retail/property sales signal: " + ", ".join(retail_property_excludes[:3])

    return True, ""


def main() -> int:
    lookup = load_location_lookup()
    output_dir = Path(category_meta(CATEGORY)["output_dir"])
    active_regions = sorted(region for region, category in live_slices() if category == CATEGORY)

    for region in active_regions:
        path = output_dir / output_filename(region, CATEGORY)
        if not path.exists():
            raise SystemExit(f"STOP: missing LIVE Customer Sales output before QA: {path}")
        jobs = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(jobs, list):
            raise SystemExit(f"STOP: Customer Sales output is not an array: {path}")

        kept: list[dict] = []
        removed: list[dict] = []
        for job in jobs:
            if not isinstance(job, dict):
                continue
            keep, reason = keep_job(job, lookup)
            if keep:
                kept.append(job)
            else:
                removed.append({"job_id": job.get("job_id", ""), "title": job.get("title", ""), "reason": reason})

        path.write_text(json.dumps(kept, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{region}: Customer Sales QA {len(jobs)} -> {len(kept)} ({len(removed)} removed)")
        for row in removed:
            print(f"  REMOVE {row['job_id']} | {row['title']} | {row['reason']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

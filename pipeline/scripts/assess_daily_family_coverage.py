from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd

from . import customer_sales_pipeline as sales
from . import customer_sales_production_refine as sales_refine
from . import daily_family_coverage_history as coverage_history
from . import finance_accounts_pipeline as finance
from . import legal_assistant_pipeline as legal
from . import marketing_pipeline as marketing
from . import hr_recruitment_pipeline as hr
from . import registered_category_pipeline as customer_service
from . import persistent_jobg8_review as persistence
from . import service_admin_pipeline_live_config as admin_config
from . import support_worker_pipeline_live_config as support_config
from .pipeline_refinement import resolve_feed_date


# Import through the config-driven production wrappers, not the bare family
# modules. This preserves the same established wrapper mutations used by the
# live daily pipelines before diagnostic expansion happens in-memory.
admin = admin_config.core
support = support_config.core

DEFAULT_ASSESSABLE_REGIONS_PATH = Path("config/uk_assessable_regions.json")
CATALOG_PATH = DEFAULT_ASSESSABLE_REGIONS_PATH
REGISTER_PATH = Path("registers/region_category_slice_register.csv")
OUTPUT_PATH = Path("reports-daily/daily-family-coverage.csv")
OVERVIEW_PATH = Path("reports-daily/daily-region-overview.md")
EXPECTED_REGION_COUNT = 78
LEGACY_REGION_COUNTS = {33, 55, 73}
FAMILY_KEYS = (
    "service_admin",
    "support_worker",
    "customer_sales",
    "legal_assistant_paralegal",
    "marketing",
    "finance_accounts",
    "hr_recruitment",
    "customer_service_contact_centre",
)


def _load_region_config() -> tuple[dict[str, dict[str, str]], dict[str, str]]:
    raw = json.loads(CATALOG_PATH.read_text(encoding="utf-8-sig"))
    regions = raw.get("regions", {})
    rollups = raw.get("detail_rollups", {})
    if not isinstance(regions, dict) or not all(isinstance(v, dict) for v in regions.values()):
        raise RuntimeError(f"Invalid assessable-region catalogue: {CATALOG_PATH}")
    if not isinstance(rollups, dict):
        raise RuntimeError(f"Invalid detail_rollups in {CATALOG_PATH}")

    declared_count = raw.get("region_count")
    if declared_count is not None and int(declared_count) != len(regions):
        raise RuntimeError(
            f"Assessable-region catalogue declares {declared_count} regions but contains {len(regions)}"
        )
    if CATALOG_PATH == DEFAULT_ASSESSABLE_REGIONS_PATH and len(regions) != EXPECTED_REGION_COUNT:
        raise RuntimeError(
            f"Expected {EXPECTED_REGION_COUNT} assessable UK markets, found {len(regions)}"
        )
    return regions, {str(k): str(v) for k, v in rollups.items()}


def _load_regions() -> dict[str, dict[str, str]]:
    return _load_region_config()[0]


def _load_statuses() -> dict[tuple[str, str], str]:
    statuses: dict[tuple[str, str], str] = {}
    with REGISTER_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["region", "category", "status"]:
            raise RuntimeError(f"Unexpected slice register header: {reader.fieldnames}")
        for row in reader:
            region = (row.get("region") or "").strip()
            category = (row.get("category") or "").strip()
            status = (row.get("status") or "").strip().upper()
            if region and category:
                statuses[(region, category)] = status
    return statuses


def _prepare_family_module(module: Any, regions: dict[str, dict[str, str]]) -> None:
    """Expand one production selector in-memory for diagnostic coverage only."""
    module.OUTPUT_FILES = {
        region: f"diagnostic-{facts['slug']}.json"
        for region, facts in regions.items()
    }
    module.PUBLISH_THRESHOLDS = {region: 6 for region in regions}
    module.ANCHOR_TOWNS = {
        region: str(facts.get("anchor_town") or region)
        for region, facts in regions.items()
    }

    # Identity-map every assessable market that is not normally LIVE.
    for region in regions:
        module.REGION_MAP[module.norm_key(region)] = region

    # Apply explicit detail -> assessable-market rollups only inside the diagnostic process.
    _regions, rollups = _load_region_config()
    if hasattr(module, "COMBINED_OUTPUT_REGION_MAP"):
        module.COMBINED_OUTPUT_REGION_MAP.update(rollups)
    if hasattr(module, "PUBLISH_REGION_BY_DETAIL_REGION"):
        module.PUBLISH_REGION_BY_DETAIL_REGION.update({region: region for region in regions})
        module.PUBLISH_REGION_BY_DETAIL_REGION.update(rollups)


def _persistent_actions(category: str) -> tuple[dict[str, str], set[str]]:
    """Read the same durable human decisions used by production, without mutating reviews."""
    decisions = persistence._load_category_store(category)
    overrides: dict[str, str] = {}
    selections: set[str] = set()
    for job_id, record in decisions.items():
        action = str(record.get("action") or "").strip().lower()
        if action == "exclude":
            overrides[job_id] = "FORCE_EXCLUDE"
        elif action == "select":
            selections.add(job_id)
    return overrides, selections


def _assess_family(
    module: Any,
    family_key: str,
    persistence_category: str,
    regions: dict[str, dict[str, str]],
) -> tuple[str, dict[str, int]]:
    """Run the production family selector against the already-materialized current feed."""
    _prepare_family_module(module, regions)

    job_file = module.find_input_file(module.JOB_FILE_KEYWORDS)
    lookup_file = module.find_lookup_file(job_file)
    feed_date = resolve_feed_date(job_file)

    job_df = module.read_table(job_file)
    module.validate_job_columns(job_df)
    lookup_df = module.read_xlsx_sheet(lookup_file)
    fallback_df = module.read_xlsx_sheet(lookup_file, sheet_name="LocationFallback")
    lookup = module.build_lookup(lookup_df)
    fallback = module.build_location_fallback_lookup(fallback_df)

    overrides, selections = _persistent_actions(persistence_category)
    title_register = module.load_title_register()
    outputs, report_rows = module.process(
        job_df,
        lookup,
        fallback,
        overrides,
        selections,
        title_register,
    )
    selected, _status = module.anchor_sort_and_select(
        outputs,
        report_rows,
        manual_rerun_mode=bool(overrides or selections),
        previously_selected_ids=set(),
    )

    missing = sorted(set(regions) - set(selected))
    if missing:
        raise RuntimeError(
            f"{family_key} selector failed to assess region(s): " + ", ".join(missing)
        )
    return feed_date, {region: len(selected[region]) for region in regions}


def _assess_customer_sales(
    regions: dict[str, dict[str, str]],
) -> tuple[str, dict[str, int]]:
    """Assess every UK market with the governed Customer Sales production rules."""
    if not sales.INPUT_PATH.is_file():
        raise RuntimeError(f"Missing current JobG8 input: {sales.INPUT_PATH}")
    if not sales.GEO_PATH.is_file():
        raise RuntimeError(f"Missing Customer Sales geo lookup: {sales.GEO_PATH}")

    feed_date = resolve_feed_date(sales.INPUT_PATH)
    feed = pd.read_excel(sales.INPUT_PATH, dtype=str).fillna("")
    required = [
        sales.COL["job_id"],
        sales.COL["title"],
        sales.COL["advertiser_name"],
        sales.COL["area"],
        sales.COL["location"],
        sales.COL["apply_url"],
        sales.COL["description"],
    ]
    missing = [column for column in required if column not in feed.columns]
    if missing:
        raise RuntimeError("Current JobG8 input missing Customer Sales columns: " + ", ".join(missing))

    area_lookup, fallback_lookup = sales.load_geo()
    qa_lookup = sales_refine.load_location_lookup()
    target_regions = set(regions)
    _regions, rollups = _load_region_config()
    candidates: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_ids: dict[str, set[str]] = defaultdict(set)

    for _, row in feed.iterrows():
        region = sales.resolve_region(
            row.get(sales.COL["area"]),
            row.get(sales.COL["location"]),
            area_lookup,
            fallback_lookup,
        )
        region = rollups.get(region, region)
        if region not in target_regions:
            continue

        job_id = sales.norm(row.get(sales.COL["job_id"]))
        title = sales.norm(row.get(sales.COL["title"]))
        apply_url = sales.norm(row.get(sales.COL["apply_url"]))
        raw_description = sales.norm(row.get(sales.COL["description"]))
        employer = sales.norm(row.get(sales.COL["advertiser_name"]))
        if (
            not job_id
            or job_id in seen_ids[region]
            or not title
            or not raw_description
            or not apply_url.lower().startswith("http")
        ):
            continue

        decision = sales.classify(title, raw_description, employer)
        if not decision:
            continue
        classification, reason = decision
        description = sales.clean_description(raw_description)
        if not description:
            continue

        item: dict[str, Any] = {
            "job_id": job_id,
            "title": title,
            "company": employer,
            "advertiser_name": employer,
            "location": sales.norm(row.get(sales.COL["area"])) or sales.norm(row.get(sales.COL["location"])),
            "region": region,
            "description": description,
            "customer_sales_classification": classification,
            "customer_sales_reason": reason,
        }
        item["_campaign_key"] = sales.campaign_key(region, employer, raw_description, title)
        candidates[region].append(item)
        seen_ids[region].add(job_id)

    counts: dict[str, int] = {}
    for region in regions:
        kept = 0
        seen_campaigns: set[str] = set()
        for job in sorted(
            candidates.get(region, []),
            key=lambda item: (
                0 if item.get("customer_sales_classification") == "DIRECT_SALES" else 1,
                str(item.get("title", "")).lower(),
                str(item.get("location", "")).lower(),
            ),
        ):
            key = str(job.pop("_campaign_key", ""))
            if key and key in seen_campaigns:
                continue
            if key:
                seen_campaigns.add(key)
            keep, _reason = sales_refine.keep_job(job, qa_lookup)
            if keep:
                kept += 1
        counts[region] = kept

    return feed_date, counts


def _assess_new_family(
    module: Any,
    family_key: str,
    regions: dict[str, dict[str, str]],
) -> tuple[str, dict[str, int]]:
    """Assess Legal, Marketing or Finance across all 78 markets with production rules.

    Both production modules expose their frozen advert classifier and reuse the
    same content fingerprint and canonical geography helpers. This diagnostic
    path counts only; it never writes a slice or changes the LIVE register.
    """
    if not module.INPUT_PATH.is_file():
        raise RuntimeError(f"Missing current JobG8 input: {module.INPUT_PATH}")
    if not module.GEO_PATH.is_file():
        raise RuntimeError(f"Missing {family_key} geo lookup: {module.GEO_PATH}")

    feed_date = resolve_feed_date(module.INPUT_PATH)
    feed = pd.read_excel(module.INPUT_PATH, dtype=str).fillna("")
    required = [
        module.COL["job_id"],
        module.TITLE_COL,
        module.AREA_COL,
        module.LOCATION_COL,
        module.COL["apply_url"],
        module.DESCRIPTION_COL,
        module.SALARY_MIN_COL,
        module.SALARY_MAX_COL,
        module.SALARY_PERIOD_COL,
    ]
    missing = [column for column in required if column not in feed.columns]
    if missing:
        raise RuntimeError(
            f"Current JobG8 input missing {family_key} columns: " + ", ".join(missing)
        )

    cfg = module._load_config()
    area_lookup, fallback_lookup = module.load_geo_lookups(module.GEO_PATH)
    _regions, rollups = _load_region_config()
    target_regions = set(regions)
    counts = {region: 0 for region in regions}
    seen_content: set[str] = set()
    location_lookup = (
        module.load_location_lookup(module.GEO_PATH)
        if family_key in {"marketing", "finance_accounts"}
        else []
    )

    for _, row in feed.iterrows():
        title = module.norm(row.get(module.TITLE_COL, ""))
        description = module.norm(row.get(module.DESCRIPTION_COL, ""))
        if not title or not description:
            continue

        period = module.norm(row.get(module.SALARY_PERIOD_COL, ""))
        if family_key in {"marketing", "finance_accounts"}:
            keep, _reason = module.classify(
                title,
                description,
                period,
                row.get(module.SALARY_MIN_COL, ""),
                row.get(module.SALARY_MAX_COL, ""),
                cfg,
            )
        else:
            keep, _reason = legal._include(
                title,
                description,
                period,
                row.get(module.SALARY_MIN_COL, ""),
                row.get(module.SALARY_MAX_COL, ""),
                cfg,
            )
        if not keep:
            continue

        area = module.norm(row.get(module.AREA_COL, ""))
        location = module.norm(row.get(module.LOCATION_COL, ""))
        region = module.ontap_region(area, location, area_lookup, fallback_lookup)
        region = rollups.get(region, region)
        if region not in target_regions:
            continue

        if family_key in {"marketing", "finance_accounts"}:
            conflict = module.location_conflict(
                title,
                description,
                region,
                location_lookup,
            )
            conflict = conflict or module._based_in_conflict(
                description,
                region,
                location_lookup,
            )
            if conflict:
                continue

        fingerprint = module.content_dedupe_key(title, location, description)
        if fingerprint in seen_content:
            continue
        seen_content.add(fingerprint)

        job_id = module.norm(row.get(module.COL["job_id"], ""))
        apply_url = module.norm(row.get(module.COL["apply_url"], ""))
        if (
            not job_id
            or not apply_url.lower().startswith("http")
            or not module.clean_description(description)
        ):
            continue
        counts[region] += 1

    return feed_date, counts


def _assess_hr_recruitment(
    regions: dict[str, dict[str, str]],
) -> tuple[str, dict[str, int]]:
    """Assess all UK markets with the frozen HR production boundary."""
    if not hr.INPUT_PATH.is_file():
        raise RuntimeError(f"Missing current JobG8 input: {hr.INPUT_PATH}")
    if not hr.GEO_PATH.is_file():
        raise RuntimeError(f"Missing HR / Recruitment geo lookup: {hr.GEO_PATH}")

    feed_date = resolve_feed_date(hr.INPUT_PATH)
    feed = pd.read_excel(hr.INPUT_PATH, dtype=str).fillna("")
    required = [
        hr.COL["job_id"], hr.TITLE_COL, hr.AREA_COL, hr.LOCATION_COL,
        hr.COL["apply_url"], hr.DESCRIPTION_COL, hr.SALARY_MIN_COL,
        hr.SALARY_MAX_COL, hr.SALARY_PERIOD_COL,
    ]
    missing = [column for column in required if column not in feed.columns]
    if missing:
        raise RuntimeError(
            "Current JobG8 input missing HR / Recruitment columns: " + ", ".join(missing)
        )

    cfg = hr._load_config()
    area_lookup, fallback_lookup = hr.load_geo_lookups(hr.GEO_PATH)
    location_lookup = hr.load_location_lookup(hr.GEO_PATH)
    _regions, rollups = _load_region_config()
    target_regions = set(regions)
    counts = {region: 0 for region in regions}
    seen_content: set[str] = set()
    seen_near: list[tuple[str, str, str, str]] = []

    for _, row in feed.iterrows():
        title = hr.norm(row.get(hr.TITLE_COL, ""))
        description = hr.norm(row.get(hr.DESCRIPTION_COL, ""))
        if not title or not description:
            continue
        keep, _reason = hr.classify(
            title,
            description,
            hr.norm(row.get(hr.SALARY_PERIOD_COL, "")),
            row.get(hr.SALARY_MIN_COL, ""),
            row.get(hr.SALARY_MAX_COL, ""),
            cfg,
        )
        if not keep:
            continue

        area = hr.norm(row.get(hr.AREA_COL, ""))
        location = hr.norm(row.get(hr.LOCATION_COL, ""))
        region = hr.ontap_region(area, location, area_lookup, fallback_lookup)
        region = rollups.get(region, region)
        if region not in target_regions:
            continue

        conflict = hr.location_conflict(title, description, region, location_lookup)
        conflict = conflict or hr._based_in_conflict(description, region, location_lookup)
        if hr._approved_proof_market_exception(region, description, conflict):
            conflict = None
        if conflict:
            continue

        fingerprint = hr.content_dedupe_key(title, location, description)
        if fingerprint in seen_content:
            continue
        if hr.is_near_duplicate(title, region, area or location, description, seen_near):
            continue
        seen_content.add(fingerprint)

        job_id = hr.norm(row.get(hr.COL["job_id"], ""))
        apply_url = hr.norm(row.get(hr.COL["apply_url"], ""))
        if not job_id or not apply_url.lower().startswith("http") or not hr.clean_description(description):
            continue
        counts[region] += 1

    return feed_date, counts


def _assess_customer_service(
    regions: dict[str, dict[str, str]],
) -> tuple[str, dict[str, int]]:
    """Assess every UK market with the production exact-title CS boundary."""
    category = "customer_service_contact_centre"
    feed_path = customer_service.find_current_feed()
    feed_date = resolve_feed_date(feed_path)
    feed = customer_service.read_feed(feed_path)
    columns = set(feed.columns)
    required = {
        customer_service.admin.COL["job_id"],
        customer_service.admin.COL["title"],
        customer_service.admin.COL["area"],
        customer_service.admin.COL["location"],
        customer_service.admin.COL["apply_url"],
        customer_service.admin.COL["description"],
    }
    missing = sorted(required - columns)
    if missing:
        raise RuntimeError(
            "Current JobG8 input missing Customer Service columns: " + ", ".join(missing)
        )

    titles = customer_service.load_titles(category)
    area_map, fallback = customer_service.load_geo()
    _regions, rollups = _load_region_config()
    target_regions = set(regions)
    counts = {region: 0 for region in regions}
    seen_ids: dict[str, set[str]] = defaultdict(set)
    seen_campaigns: dict[str, set[str]] = defaultdict(set)
    location_lookup = sales_refine.load_location_lookup()

    for _, row in feed.iterrows():
        title = customer_service.norm(row.get(customer_service.admin.COL["title"]))
        if customer_service.key(title) not in titles:
            continue

        area = customer_service.norm(row.get(customer_service.admin.COL["area"]))
        location = customer_service.norm(row.get(customer_service.admin.COL["location"]))
        if customer_service.admin.area_is_unusable(area):
            raw_region = fallback.get(customer_service.key(location), "")
        else:
            raw_region = area_map.get(customer_service.key(area), "")
        candidate_regions = {
            rollups.get(region, region)
            for region in customer_service.candidate_regions(raw_region)
        }

        job_id = customer_service.norm(row.get(customer_service.admin.COL["job_id"]))
        apply_url = customer_service.norm(row.get(customer_service.admin.COL["apply_url"]))
        description = customer_service.norm(row.get(customer_service.admin.COL["description"]))
        if (
            not job_id
            or not apply_url.lower().startswith("http")
            or not customer_service.admin.clean_description(description)
        ):
            continue

        salary_text, _salary_source = customer_service.admin.build_salary_details(row)
        salary_period = customer_service.admin.normalise_salary_period(row)
        for region in candidate_regions:
            if region not in target_regions or job_id in seen_ids[region]:
                continue
            if sales_refine.location_conflict(title, description, region, location_lookup):
                continue
            employer = customer_service.norm(
                row.get(customer_service.admin.COL["advertiser_name"])
            )
            campaign = sales.campaign_key(region, employer, description, title)
            if campaign in seen_campaigns[region]:
                continue
            salary = customer_service.assess_salary(
                salary_min=row.get(customer_service.admin.COL["salary_min"]),
                salary_max=row.get(customer_service.admin.COL["salary_max"]),
                salary_period=salary_period,
                salary_text=salary_text,
                region=region,
                thresholds=customer_service.SALARY_THRESHOLDS,
            )
            if salary.corrupt or salary.review_required:
                continue
            seen_ids[region].add(job_id)
            seen_campaigns[region].add(campaign)
            counts[region] += 1

    return feed_date, counts


def _write_coverage_csv(
    feed_date: str,
    regions: dict[str, dict[str, str]],
    admin_counts: dict[str, int],
    support_counts: dict[str, int],
    sales_counts: dict[str, int],
    legal_counts: dict[str, int],
    marketing_counts: dict[str, int],
    finance_counts: dict[str, int],
    hr_counts: dict[str, int],
    customer_service_counts: dict[str, int],
) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["feed_date", "region", "family", "selected_count"],
            lineterminator="\n",
        )
        writer.writeheader()
        for region in sorted(regions, key=str.casefold):
            writer.writerow({"feed_date": feed_date, "region": region, "family": "service_admin", "selected_count": admin_counts[region]})
            writer.writerow({"feed_date": feed_date, "region": region, "family": "support_worker", "selected_count": support_counts[region]})
            writer.writerow({"feed_date": feed_date, "region": region, "family": "customer_sales", "selected_count": sales_counts[region]})
            writer.writerow({"feed_date": feed_date, "region": region, "family": "legal_assistant_paralegal", "selected_count": legal_counts[region]})
            writer.writerow({"feed_date": feed_date, "region": region, "family": "marketing", "selected_count": marketing_counts[region]})
            writer.writerow({"feed_date": feed_date, "region": region, "family": "finance_accounts", "selected_count": finance_counts[region]})
            writer.writerow({"feed_date": feed_date, "region": region, "family": "hr_recruitment", "selected_count": hr_counts[region]})
            writer.writerow({"feed_date": feed_date, "region": region, "family": "customer_service_contact_centre", "selected_count": customer_service_counts[region]})


def _load_coverage_csv() -> tuple[str, dict[str, dict[str, int]]]:
    if not OUTPUT_PATH.is_file():
        raise RuntimeError(f"Missing daily family coverage: {OUTPUT_PATH}")
    dates: set[str] = set()
    counts: dict[str, dict[str, int]] = {family: {} for family in FAMILY_KEYS}
    with OUTPUT_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"feed_date", "region", "family", "selected_count"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise RuntimeError(f"Unexpected daily family coverage header: {reader.fieldnames}")
        for row in reader:
            feed_date = (row.get("feed_date") or "").strip()
            region = (row.get("region") or "").strip()
            family = (row.get("family") or "").strip()
            if feed_date:
                dates.add(feed_date)
            if family not in counts or not region:
                continue
            counts[family][region] = int((row.get("selected_count") or "0").strip())
    if len(dates) != 1:
        raise RuntimeError(f"Daily family coverage must contain one feed date, found {sorted(dates)}")

    regions = _load_regions()
    assessable = set(regions)
    for family in ("service_admin", "support_worker"):
        present = set(counts[family])
        if not present.issubset(assessable):
            unexpected = sorted(present - assessable)
            raise RuntimeError(f"Coverage contains unknown {family} region(s): " + ", ".join(unexpected))
        if present != assessable and len(present) not in LEGACY_REGION_COUNTS:
            missing = sorted(assessable - present)
            raise RuntimeError(f"Coverage missing {family} region(s): " + ", ".join(missing))

    for family in (
        "customer_sales",
        "legal_assistant_paralegal",
        "marketing",
        "finance_accounts",
        "hr_recruitment",
        "customer_service_contact_centre",
    ):
        if not counts[family]:
            continue
        present = set(counts[family])
        if not present.issubset(assessable):
            unexpected = sorted(present - assessable)
            raise RuntimeError(f"Coverage contains unknown {family} region(s): " + ", ".join(unexpected))
        if present != assessable and len(present) not in LEGACY_REGION_COUNTS:
            missing = sorted(assessable - present)
            raise RuntimeError(f"Coverage missing {family} region(s): " + ", ".join(missing))

    return next(iter(dates)), counts


def _apply_to_overview(
    feed_date: str,
    counts: dict[str, dict[str, int]],
) -> None:
    """Render current and rolling diagnostics in NOT LIVE cells only."""
    if not OVERVIEW_PATH.is_file():
        raise RuntimeError(f"Daily overview must be built before coverage is applied: {OVERVIEW_PATH}")

    statuses = _load_statuses()
    history = coverage_history.load_history()
    lines = OVERVIEW_PATH.read_text(encoding="utf-8").splitlines()
    in_not_live = False
    seen_regions: set[str] = set()
    patched: list[str] = []
    admin_counts = counts["service_admin"]
    support_counts = counts["support_worker"]
    sales_counts = counts["customer_sales"]
    legal_counts = counts["legal_assistant_paralegal"]
    marketing_counts = counts["marketing"]
    finance_counts = counts["finance_accounts"]
    hr_counts = counts["hr_recruitment"]
    customer_service_counts = counts.get("customer_service_contact_centre", {})
    sales_ready = bool(sales_counts)
    assessed_count = len(admin_counts)

    for line in lines:
        if line.startswith("> LIVE Service Admin") or line.startswith("> LIVE counts "):
            live_prefix = line.split(". NOT LIVE", 1)[0].rstrip(".")
            if sales_ready:
                sales_note = (
                    f" NOT LIVE Sales Advisor was assessed from that same feed across {len(sales_counts)} UK markets using the governed Customer Sales classifier, canonical geo, campaign dedupe and final production QA. Sales diagnostic counts are evidence only and never activate a slice automatically; LIVE Sales Advisor counts continue to come from the current published Customer Sales configured-slice JSON."
                )
            else:
                sales_note = (
                    " NOT LIVE Sales Advisor remains `—` for this transitional snapshot because the persisted coverage file predates the three-family rollout. LIVE Sales Advisor counts continue to come from the current published Customer Sales configured-slice JSON."
                )
            patched.append(
                live_prefix
                + f". NOT LIVE Service Admin and Support Worker were assessed from the same JobG8 daily feed ({feed_date}) used by the production family run, across {assessed_count} UK markets with the config-driven production wrappers, persistent review decisions and canonical geo."
                + sales_note
                + (
                    f" NOT LIVE Paralegal, Marketing, Finance / Accounts and HR / Recruitment were assessed from that same feed across {len(legal_counts)}, {len(marketing_counts)}, {len(finance_counts)} and {len(hr_counts)} UK markets respectively, using their governed production boundaries and canonical geo."
                    if legal_counts and marketing_counts and finance_counts and hr_counts
                    else " NOT LIVE Paralegal, Marketing, Finance / Accounts and HR / Recruitment remain `—` until their first persisted coverage run."
                )
                + (
                    f" NOT LIVE Customer Service / Contact Centre was assessed from that same feed across {len(customer_service_counts)} UK markets using its governed exact-title, salary and geography rules."
                    if customer_service_counts
                    else " NOT LIVE Customer Service / Contact Centre temporarily retains the overview builder's latest Module 2 profile fallback until the first eight-family coverage run."
                )
                + " All diagnostic counts are evidence only and never activate a slice automatically. Rolling family history stores one snapshot per feed date, replaces same-date reruns, retains the latest 14 feed dates and is used only as decision evidence for NOT LIVE slices."
            )
            continue

        if line == "## NOT LIVE":
            in_not_live = True
            patched.append(line)
            patched.append("")
            patched.append("> Cells show `today / 14d avg / 6+ days` over observed feed dates (maximum 14). The 6+ measure is a watch signal only, not an automatic activation threshold.")
            continue
        if line == "## HEADLINE":
            in_not_live = False
            patched.append(line)
            continue

        if in_not_live and line.startswith("| ") and not line.startswith("| Region ") and not line.startswith("|---"):
            cells = [cell.strip() for cell in line.split("|")]
            if len(cells) >= 11:
                region = cells[1]
                if region in admin_counts and region in support_counts:
                    cells[2] = "" if statuses.get((region, "admin_service"), "") == "LIVE" else coverage_history.format_metric(history, region, "service_admin", admin_counts[region], as_of_date=feed_date)
                    cells[3] = "" if statuses.get((region, "support_worker"), "") == "LIVE" else coverage_history.format_metric(history, region, "support_worker", support_counts[region], as_of_date=feed_date)
                    if region in sales_counts:
                        cells[4] = "" if statuses.get((region, "customer_sales"), "") == "LIVE" else coverage_history.format_metric(history, region, "customer_sales", sales_counts[region], as_of_date=feed_date)
                    if region in legal_counts:
                        cells[5] = "" if statuses.get((region, "legal_assistant_paralegal"), "") == "LIVE" else coverage_history.format_metric(history, region, "legal_assistant_paralegal", legal_counts[region], as_of_date=feed_date)
                    if region in marketing_counts:
                        cells[6] = "" if statuses.get((region, "marketing"), "") == "LIVE" else coverage_history.format_metric(history, region, "marketing", marketing_counts[region], as_of_date=feed_date)
                    if region in finance_counts:
                        cells[7] = "" if statuses.get((region, "finance_accounts"), "") == "LIVE" else coverage_history.format_metric(history, region, "finance_accounts", finance_counts[region], as_of_date=feed_date)
                    if region in hr_counts:
                        cells[8] = "" if statuses.get((region, "hr_recruitment"), "") == "LIVE" else coverage_history.format_metric(history, region, "hr_recruitment", hr_counts[region], as_of_date=feed_date)
                    if region in customer_service_counts:
                        cells[9] = "" if statuses.get((region, "customer_service_contact_centre"), "") == "LIVE" else coverage_history.format_metric(history, region, "customer_service_contact_centre", customer_service_counts[region], as_of_date=feed_date)
                    line = "| " + " | ".join(cells[1:-1]) + " |"
                    seen_regions.add(region)
        patched.append(line)

    missing = sorted(set(admin_counts) - seen_regions)
    if missing:
        raise RuntimeError("Overview NOT LIVE table missing assessed region(s): " + ", ".join(missing))

    OVERVIEW_PATH.write_text("\n".join(patched) + "\n", encoding="utf-8")


def build_coverage() -> tuple[str, dict[str, dict[str, int]]]:
    regions = _load_regions()
    admin_date, admin_counts = _assess_family(admin, "service_admin", "service_admin", regions)
    support_date, support_counts = _assess_family(support, "support_worker", "support_worker", regions)
    sales_date, sales_counts = _assess_customer_sales(regions)
    legal_date, legal_counts = _assess_new_family(legal, "legal_assistant_paralegal", regions)
    marketing_date, marketing_counts = _assess_new_family(marketing, "marketing", regions)
    finance_date, finance_counts = _assess_new_family(finance, "finance_accounts", regions)
    hr_date, hr_counts = _assess_hr_recruitment(regions)
    customer_service_date, customer_service_counts = _assess_customer_service(regions)
    dates = {
        admin_date,
        support_date,
        sales_date,
        legal_date,
        marketing_date,
        finance_date,
        hr_date,
        customer_service_date,
    }
    if len(dates) != 1:
        raise RuntimeError(
            "Family assessment feed-date mismatch: "
            f"admin={admin_date}, support={support_date}, sales={sales_date}, "
            f"legal={legal_date}, marketing={marketing_date}, finance={finance_date}, "
            f"hr={hr_date}, customer_service={customer_service_date}"
        )
    _write_coverage_csv(
        admin_date,
        regions,
        admin_counts,
        support_counts,
        sales_counts,
        legal_counts,
        marketing_counts,
        finance_counts,
        hr_counts,
        customer_service_counts,
    )
    coverage_history.record_snapshot(
        admin_date,
        regions,
        admin_counts,
        support_counts,
        sales_counts,
        legal_counts,
        marketing_counts,
        finance_counts,
        hr_counts,
        customer_service_counts,
    )
    return admin_date, {
        "service_admin": admin_counts,
        "support_worker": support_counts,
        "customer_sales": sales_counts,
        "legal_assistant_paralegal": legal_counts,
        "marketing": marketing_counts,
        "finance_accounts": finance_counts,
        "hr_recruitment": hr_counts,
        "customer_service_contact_centre": customer_service_counts,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply-existing",
        action="store_true",
        help="Apply the already-generated daily-family-coverage.csv to the overview without re-reading JobG8.",
    )
    args = parser.parse_args()

    if args.apply_existing:
        feed_date, counts = _load_coverage_csv()
        _apply_to_overview(feed_date, counts)
        print(f"Applied {OUTPUT_PATH} to {OVERVIEW_PATH}")
        return 0

    feed_date, _counts = build_coverage()
    print(
        f"Wrote {OUTPUT_PATH}: {EXPECTED_REGION_COUNT} UK markets x 8 families for feed {feed_date}; "
        f"updated {coverage_history.HISTORY_PATH}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

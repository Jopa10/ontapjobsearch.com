"""Three-region Sales Advisor volume proof.

Diagnostic only. This script does not publish slices.

Purpose:
- measure whether the proposed Sales Advisor family has enough plausible volume
  to support regional slices;
- deliberately allow legitimate overlap with Service Admin;
- show how much of the candidate volume would be genuinely new surfacing versus
  jobs already surfaced by Service Admin;
- keep obvious salary, senior/specialist and field-sales rejects out of the
  slice-supporting count without pretending this is the final governed selector.

Proof regions:
- Hampshire
- Greater Manchester - Manchester & Salford
- Yorkshire - West
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

from scripts.service_admin_pipeline import build_complete_geo_lookups, resolve_job_geography
from scripts.service_admin_pipeline_core import COL, norm, norm_key

INPUT_PATH = Path("input/jobg8.xlsx")
REPORT_DIR = Path("reports-daily")
SUMMARY_PATH = REPORT_DIR / "sales-advisor-volume-proof-summary.csv"
DETAIL_PATH = REPORT_DIR / "sales-advisor-volume-proof-detail.csv"
MD_PATH = REPORT_DIR / "sales-advisor-volume-proof.md"

TARGETS = {
    "Hampshire": Path("output-admin-service/hampshire-admin-service.json"),
    "Greater Manchester - Manchester & Salford": Path(
        "output-admin-service/manchester-salford-admin-service.json"
    ),
    "Yorkshire - West": Path("output-admin-service/west-yorkshire-admin-service.json"),
}

# These three proof regions are outside the London/SE exception case. £40k is a
# hard ceiling for this diagnostic: a known structured salary above it is OUT.
# Missing salary is retained for discovery rather than silently treated as low.
HARD_MAX_ANNUAL = 40_000.0

# Direct Sales Advisor-family titles. These are deliberately broader than the
# old branch test because the goal is volume discovery before final governance.
DIRECT_TITLE_TERMS = [
    "sales advisor",
    "sales adviser",
    "sales executive",
    "sales consultant",
    "sales representative",
    "sales agent",
    "sales associate",
    "sales development representative",
    "internal sales",
    "inside sales",
    "inbound sales",
    "outbound sales",
    "telephone sales",
    "telesales",
    "tele sales",
    "telemarketing",
    "business development executive",
    "new business executive",
    "new business advisor",
    "new business adviser",
    "customer sales",
    "membership sales",
    "membership advisor",
    "membership adviser",
    "retention advisor",
    "retention adviser",
    "retention executive",
    "renewals advisor",
    "renewals adviser",
    "renewals executive",
    "lead generator",
    "appointment setter",
]

# IMPORTANT: these were wrongly excluded by the superseded test. They are now
# explicit candidates because legitimate Service Admin <-> Sales Advisor overlap
# is allowed and commercially important to measure.
OVERLAP_TITLE_TERMS = [
    "sales administrator",
    "sales administration",
    "sales admin",
    "sales support",
    "sales coordinator",
    "sales co-ordinator",
    "sales office",
    "order sales",
]

CUSTOMER_TITLE_TERMS = [
    "customer service",
    "customer advisor",
    "customer adviser",
    "customer support",
    "customer care",
    "customer representative",
    "customer success",
    "client service",
    "client services",
    "client advisor",
    "client adviser",
    "call centre",
    "call center",
    "contact centre",
    "contact center",
    "move manager",
]

ACCOUNT_TITLE_TERMS = ["account manager", "account executive", "client manager"]

# Evidence needed to bring a generic customer/service title into this family.
# Avoid generic occurrences of the word "sales" so sales-ledger/order admin does
# not become a false positive merely because the description mentions sales data.
CUSTOMER_SALES_EVIDENCE = [
    "commission",
    "sales target",
    "sales targets",
    "sales opportunity",
    "sales opportunities",
    "upsell",
    "up-sell",
    "cross-sell",
    "cross sell",
    "convert enquiries",
    "convert inquiries",
    "convert leads",
    "convert prospects",
    "convert interest",
    "conversion target",
    "conversion targets",
    "warm leads",
    "warm enquiries",
    "warm inquiries",
    "inbound sales",
    "outbound sales",
    "telesales",
    "telephone sales",
    "cold calling",
    "new business",
    "lead generation",
    "sales pipeline",
    "close sales",
    "closing sales",
    "close deals",
    "closing deals",
    "booked and paid",
    "increase membership",
    "sales experience",
    "sales role",
    "sales kpi",
    "sales kpis",
]

ACCOUNT_SALES_EVIDENCE = CUSTOMER_SALES_EVIDENCE + [
    "revenue growth",
    "grow revenue",
    "account growth",
    "grow accounts",
    "renewals",
    "retention",
    "selling",
]

OFFICE_DIGITAL_EVIDENCE = [
    "office",
    "office-based",
    "office based",
    "hybrid",
    "remote",
    "home-based",
    "home based",
    "phone",
    "telephone",
    "crm",
    "inbound",
    "outbound",
    "email",
]

# These are obvious OUTs even in a broad volume-discovery pass.
TITLE_HARD_EXCLUDES = [
    "field sales",
    "door to door",
    "door-to-door",
    "territory sales",
    "area sales",
    "regional sales",
    "sales manager",
    "business development manager",
    "head of sales",
    "sales director",
    "technical sales",
    "sales engineer",
    "sales engineering",
    "product sales engineer",
    "product sales executive",
    "car sales",
    "vehicle sales",
    "showroom sales",
    "estate agent",
    "lettings negotiator",
    "sales negotiator",
    "recruitment consultant",
    "senior sales executive",
    "senior sales consultant",
    "national account manager",
    "key account manager",
    "strategic account manager",
    "enterprise account manager",
    "senior account manager",
    "technical account manager",
    "field account manager",
    "area account manager",
    "regional account manager",
    "netsuite account manager",
    "it account manager",
    "insurance account manager",
    "insurance client manager",
]

DESCRIPTION_HARD_EXCLUDES = [
    "door to door",
    "door-to-door",
    "event-based campaigns",
    "face-to-face sales environments",
    "travel to different campaign locations",
    "subcontracted basis",
    "self-employed",
    "self employed",
    "commission-only",
    "commission only",
]

ACCOUNT_SPECIALIST_SIGNALS = [
    "commercial insurance",
    "insurance broker",
    "insurance brokerage",
    "underwriting",
    "pensions",
    "wealth management",
    "financial adviser",
    "financial advisor",
    "erp",
    "saas",
    "netsuite",
    "managed services",
    "network security",
    "telecoms solutions",
    "medical device",
    "pharmaceutical",
]

BROAD_TITLE_TERMS = sorted(
    set(
        DIRECT_TITLE_TERMS
        + OVERLAP_TITLE_TERMS
        + CUSTOMER_TITLE_TERMS
        + ACCOUNT_TITLE_TERMS
        + ["sales", "business development", "retention", "renewal"]
    )
)


def contains_any(text: str, terms: list[str]) -> list[str]:
    return [term for term in terms if term in text]


def number(value: Any) -> float | None:
    text = norm(value).replace(",", "").replace("£", "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        match = re.search(r"-?\d+(?:\.\d+)?", text)
        return float(match.group(0)) if match else None


def annualised_upper(row: Any) -> float | None:
    high = number(row.get(COL["salary_max"]))
    low = number(row.get(COL["salary_min"]))
    value = high if high is not None and high > 0 else low
    if value is None or value <= 0:
        return None

    period = norm_key(row.get(COL["salary_period"]))
    if "hour" in period:
        return value * 37.5 * 52
    if "day" in period:
        return value * 260
    if "week" in period:
        return value * 52
    if "month" in period:
        return value * 12
    # JobG8 annual periods vary in wording; annual is also the safest default
    # for values already in normal salary-scale territory.
    return value


def salary_text(row: Any) -> str:
    low = norm(row.get(COL["salary_min"]))
    high = norm(row.get(COL["salary_max"]))
    period = norm(row.get(COL["salary_period"]))
    additional = norm(row.get(COL["salary_additional"]))
    structured = " - ".join(v for v in [low, high] if v)
    if structured and period:
        structured = f"{structured} {period}"
    return additional or structured


def load_service_admin_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    try:
        items = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return set()
    return {norm(item.get("job_id")) for item in items if norm(item.get("job_id"))}


def classify(title: str, description: str, annual_upper: float | None) -> tuple[str, str, bool]:
    """Return classification, reason, and whether it supports the core volume count."""
    t = norm_key(title)
    d = norm_key(description)
    combined = f"{t} {d}"

    if annual_upper is not None and annual_upper > HARD_MAX_ANNUAL:
        return "OUT_SALARY", f"known annualised upper salary £{annual_upper:,.0f} > £40,000", False

    hard_title = contains_any(t, TITLE_HARD_EXCLUDES)
    if hard_title:
        return "OUT_TITLE", "obvious field/senior/specialist title: " + ", ".join(hard_title[:3]), False

    hard_desc = contains_any(d, DESCRIPTION_HARD_EXCLUDES)
    if hard_desc:
        return "OUT_FIELD_CAMPAIGN", "field/event/self-employed signal: " + ", ".join(hard_desc[:3]), False

    overlap = contains_any(t, OVERLAP_TITLE_TERMS)
    if overlap:
        return "CORE_SALES_SUPPORT", "sales admin/support overlap title: " + ", ".join(overlap[:3]), True

    direct = contains_any(t, DIRECT_TITLE_TERMS)
    if direct:
        return "CORE_DIRECT_SALES", "direct Sales Advisor-family title: " + ", ".join(direct[:3]), True

    customer = contains_any(t, CUSTOMER_TITLE_TERMS)
    if customer:
        evidence = contains_any(combined, CUSTOMER_SALES_EVIDENCE)
        if evidence:
            return "CORE_CUSTOMER_SALES", "customer/service title with commercial evidence: " + ", ".join(evidence[:3]), True
        return "OUT_PURE_SERVICE", "customer/service title without strong sales/conversion evidence", False

    account = contains_any(t, ACCOUNT_TITLE_TERMS)
    if account:
        specialist = contains_any(combined, ACCOUNT_SPECIALIST_SIGNALS)
        if specialist:
            return "OUT_ACCOUNT_SPECIALIST", "specialist account role: " + ", ".join(specialist[:3]), False
        sales = contains_any(combined, ACCOUNT_SALES_EVIDENCE)
        office = contains_any(combined, OFFICE_DIGITAL_EVIDENCE)
        if sales and office:
            return "EDGE_ACCOUNT_SALES", "non-specialist account role with sales + office/digital evidence", False
        return "OUT_ACCOUNT_AMBIGUOUS", "generic account role without enough evidence", False

    # Broad Sales/BD leftovers are kept visible as REVIEW rather than silently
    # disappearing, because this stage is about discovering possible volume.
    if contains_any(t, BROAD_TITLE_TERMS):
        return "REVIEW_BROAD_SALES", "broad sales-related title outside current core rules", False

    return "OUT_NOT_FAMILY", "not a Sales Advisor-family candidate", False


def main() -> None:
    if not INPUT_PATH.exists():
        raise SystemExit(f"STOP: missing {INPUT_PATH}")

    df = pd.read_excel(INPUT_PATH, dtype=str).fillna("")
    required = [
        COL["job_id"], COL["title"], COL["advertiser_name"], COL["area"],
        COL["location"], COL["description"], COL["salary_min"], COL["salary_max"],
        COL["salary_period"],
    ]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise SystemExit("STOP: missing JobG8 columns: " + ", ".join(missing))

    area_lookup, location_lookup = build_complete_geo_lookups()
    admin_ids = {region: load_service_admin_ids(path) for region, path in TARGETS.items()}

    detail_rows: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for _, row in df.iterrows():
        job_id = norm(row.get(COL["job_id"]))
        title = norm(row.get(COL["title"]))
        if not job_id or not title or job_id in seen_ids:
            continue

        title_key = norm_key(title)
        if not contains_any(title_key, BROAD_TITLE_TERMS):
            continue

        resolution = resolve_job_geography(row, area_lookup, location_lookup)
        region = norm(resolution.region)
        if region not in TARGETS:
            continue
        seen_ids.add(job_id)

        description = norm(row.get(COL["description"]))
        annual_upper = annualised_upper(row)
        classification, reason, core = classify(title, description, annual_upper)
        is_edge = classification in {"EDGE_ACCOUNT_SALES", "REVIEW_BROAD_SALES"}
        plausible_with_edge = core or classification == "EDGE_ACCOUNT_SALES"
        overlap = job_id in admin_ids[region]
        surfacing = (
            "OVERLAP_ALREADY_SERVICE_ADMIN" if plausible_with_edge and overlap
            else "NEW_SURFACING" if plausible_with_edge
            else "NOT_COUNTED"
        )

        detail_rows.append({
            "region": region,
            "job_id": job_id,
            "title": title,
            "employer": norm(row.get(COL["advertiser_name"])),
            "area": norm(row.get(COL["area"])),
            "location": norm(resolution.town) or norm(row.get(COL["location"])),
            "salary_text": salary_text(row),
            "annualised_upper_salary": round(annual_upper, 2) if annual_upper is not None else "",
            "classification": classification,
            "core_slice_candidate": core,
            "edge_review_candidate": is_edge,
            "plausible_including_edge": plausible_with_edge,
            "already_in_service_admin": overlap,
            "surfacing_effect": surfacing,
            "reason": reason,
            "description_excerpt": re.sub(r"\s+", " ", description)[:500],
        })

    detail = pd.DataFrame(detail_rows)
    if detail.empty:
        raise SystemExit("STOP: zero three-region Sales Advisor candidates found")

    region_rows: list[dict[str, Any]] = []
    for region in TARGETS:
        g = detail[detail["region"] == region]
        core = g[g["core_slice_candidate"] == True]  # noqa: E712
        edge = g[g["classification"] == "EDGE_ACCOUNT_SALES"]
        plausible = g[g["plausible_including_edge"] == True]  # noqa: E712
        overlap_core = core[core["already_in_service_admin"] == True]  # noqa: E712
        new_core = core[core["already_in_service_admin"] == False]  # noqa: E712
        overlap_plausible = plausible[plausible["already_in_service_admin"] == True]  # noqa: E712
        new_plausible = plausible[plausible["already_in_service_admin"] == False]  # noqa: E712
        region_rows.append({
            "region": region,
            "broad_candidates_reviewed": len(g),
            "core_slice_candidates": len(core),
            "edge_account_review_candidates": len(edge),
            "potential_slice_jobs_including_edge": len(plausible),
            "core_already_service_admin": len(overlap_core),
            "core_genuinely_new": len(new_core),
            "including_edge_already_service_admin": len(overlap_plausible),
            "including_edge_genuinely_new": len(new_plausible),
            "obvious_out_or_not_counted": len(g) - len(plausible),
        })

    summary = pd.DataFrame(region_rows)
    total = {
        "region": "TOTAL",
        "broad_candidates_reviewed": int(summary["broad_candidates_reviewed"].sum()),
        "core_slice_candidates": int(summary["core_slice_candidates"].sum()),
        "edge_account_review_candidates": int(summary["edge_account_review_candidates"].sum()),
        "potential_slice_jobs_including_edge": int(summary["potential_slice_jobs_including_edge"].sum()),
        "core_already_service_admin": int(summary["core_already_service_admin"].sum()),
        "core_genuinely_new": int(summary["core_genuinely_new"].sum()),
        "including_edge_already_service_admin": int(summary["including_edge_already_service_admin"].sum()),
        "including_edge_genuinely_new": int(summary["including_edge_genuinely_new"].sum()),
        "obvious_out_or_not_counted": int(summary["obvious_out_or_not_counted"].sum()),
    }
    summary = pd.concat([summary, pd.DataFrame([total])], ignore_index=True)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    summary.to_csv(SUMMARY_PATH, index=False)
    detail = detail.sort_values(
        ["region", "plausible_including_edge", "already_in_service_admin", "classification", "title"],
        ascending=[True, False, False, True, True],
    )
    detail.to_csv(DETAIL_PATH, index=False)

    lines: list[str] = []
    lines.append("# Sales Advisor three-region volume proof")
    lines.append("")
    lines.append("**Diagnostic only. Nothing here is LIVE or published.**")
    lines.append("")
    lines.append(
        "Purpose: test whether the proposed Sales Advisor family has enough regional volume to support slices, "
        "not to pretend the final governed selector is already settled."
    )
    lines.append("")
    lines.append("Current proof rules:")
    lines.append("- legitimate Service Admin overlap is explicitly allowed;")
    lines.append("- Sales Administrator / Sales Support / Sales Coordinator-type titles are candidates, not automatic exclusions;")
    lines.append("- known annualised salary above £40,000 is OUT in these three proof regions;")
    lines.append("- obvious field, senior-manager and specialist sales titles are OUT;")
    lines.append("- generic account roles are shown separately as EDGE review and do not inflate the core count;")
    lines.append("- NEW vs OVERLAP uses exact JobG8 job_id against the current Service Admin regional outputs.")
    lines.append("")
    lines.append(f"Feed rows read: **{len(df):,}**")
    lines.append("")
    lines.append("## Volume")
    lines.append("")
    lines.append(
        "| Region | Broad reviewed | Core slice candidates | Edge account review | Potential incl. edge | "
        "Core overlap with Service Admin | **Core genuinely new** |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for _, row in summary.iterrows():
        lines.append(
            f"| {row['region']} | {int(row['broad_candidates_reviewed'])} | "
            f"{int(row['core_slice_candidates'])} | {int(row['edge_account_review_candidates'])} | "
            f"{int(row['potential_slice_jobs_including_edge'])} | "
            f"{int(row['core_already_service_admin'])} | **{int(row['core_genuinely_new'])}** |"
        )

    for region in TARGETS:
        lines.append("")
        lines.append(f"## {region}")
        lines.append("")
        g = detail[(detail["region"] == region) & (detail["core_slice_candidate"] == True)]  # noqa: E712
        if g.empty:
            lines.append("No core candidates.")
            continue
        for label, flag in [("Already surfaced via Service Admin", True), ("Genuinely new surfacing", False)]:
            subset = g[g["already_in_service_admin"] == flag]
            lines.append(f"**{label}: {len(subset)}**")
            if subset.empty:
                lines.append("")
                continue
            for _, item in subset.iterrows():
                salary = f"; {item['salary_text']}" if item["salary_text"] else ""
                lines.append(
                    f"- {item['title']} — {item['location']} — {item['classification']}{salary}"
                )
            lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "Use **core slice candidates** as the main volume signal. Edge account roles are headroom for review, not assumed inventory. "
        "Use **core genuinely new** to measure how much the family expands Ontap inventory surfacing rather than merely presenting "
        "existing Service Admin jobs under another search term."
    )
    lines.append("")

    MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(summary.to_string(index=False))
    print(f"Wrote {SUMMARY_PATH}")
    print(f"Wrote {DETAIL_PATH}")
    print(f"Wrote {MD_PATH}")


if __name__ == "__main__":
    main()

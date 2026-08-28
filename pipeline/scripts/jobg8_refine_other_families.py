from __future__ import annotations

import argparse
import math
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path = [entry for entry in sys.path if Path(entry or ".").resolve() != SCRIPT_DIR]

import pandas as pd

TITLE_COL = "/Job/Position"
DESCRIPTION_COL = "/Job/Description"
AREA_COL = "/Job/Area"
LOCATION_COL = "/Job/Location"
SALARY_MIN_COL = "/Job/SalaryMinimum"
SALARY_MAX_COL = "/Job/SalaryMaximum"
SALARY_PERIOD_COL = "/Job/SalaryPeriod"
AREA_UNUSABLE_VALUES = {"", "not specified", "unknown"}
SALARY_BANDS = ["Below £20k / unknown", "£20k–<£35k", "£35k–£45k", "Over £45k"]

CATEGORY_FAMILY = {
    "support_worker": "Care / Support Work",
    "finance_accounts": "Professional Finance / Accountancy",
    "hr_recruitment": "HR / Recruitment",
    "warehouse_logistics": "Driving / Warehouse / Logistics",
    "customer_service_contact_centre": "Admin / Customer Service",
    "admin_service": "Admin / Customer Service",
}
CATEGORY_PRECEDENCE = [
    "support_worker", "finance_accounts", "hr_recruitment",
    "warehouse_logistics", "customer_service_contact_centre", "admin_service",
]

OTHER_RULES = [
    ("Legal / Conveyancing", r"\b(conveyancer|conveyancing|employment counsel|court adviser|court advisor)\b"),
    ("Professional Finance / Accountancy", r"\b(bookkeeper|bookkeeping|fp&a|fp and a|financial planning and analysis|financial planning analyst)\b"),
    ("Healthcare / Clinical", r"\b(optometrist|optician|optical assistant|dispensing optician|pharmacist|pharmacy|psychologist|podiatrist|audiologist|audiology|physiotherapy|physiotherapist|functional assessor|psychiatrist)\b"),
    ("Care / Support Work", r"\b(autism practitioner|family court adviser|family court advisor|senior practitioner)\b"),
    ("IT / Data / Software", r"\b(ai consultant|artificial intelligence consultant|ethical hacker|penetration tester|pen tester|servicenow architect|technical architect|data consultant|product owner)\b"),
    ("Market Research / Field Interviewing", r"\b(market research|field interviewer|research interviewer|survey interviewer|field researcher)\b"),
    ("Insurance / Claims", r"\b(insurance|claims?|underwriter|underwriting|loss adjuster|adjuster|broker|actuarial|actuary|reinsurance|commercial account handler)\b"),
    ("Compliance / Risk / Quality", r"\b(compliance manager|compliance officer|risk assessor|risk manager|quality manager|quality assurance manager|regulatory manager|ai governance consultant|governance consultant)\b"),
    ("Property / Housing / Planning", r"\b(town planner|planning officer|resident liaison officer|housing solutions officer|income officer|scheme manager|housing manager|rental agent|asset manager|director of planning|rtpi|housing support officer)\b"),
    ("Retail / Store", r"\b(customer team member|service colleague|store leader|online manager)\b"),
    ("Employment Support / Careers", r"\b(employment specialist|ips employment specialist|employment adviser|employment advisor|job coach|youth employment coach)\b"),
    ("Manufacturing / Production", r"\b(production|manufacturing|machine operator|machine operative|assembler|assembly|factory|plant operator|process operator|production operative|production operator|print finisher)\b"),
    ("Cleaning / Domestic / Facilities", r"\b(cleaner|cleaning|domestic assistant|domestic cleaner|caretaker|janitor|facilities assistant|facilities operative|hygiene operative)\b"),
    ("Management / Team Leadership", r"\b(registered manager|deputy manager|assistant manager|service manager|team leader|client manager|centre manager|unit manager|department manager|supervisor|practice manager|business manager|home manager|duty manager|lodge manager)\b"),
    ("Admin / Customer Service", r"\b(executive assistant|executive pa|ea\b|office support|business administrator|administrative assistant|document controller|service controller|hire controller|parts advisor|customer success manager|order processor|data entry assistant|registration support officer|project co-ordinator)\b"),
    ("Marketing / Digital / Creative", r"\b(paid media specialist|paid media executive|bid writer)\b"),
    ("Charity / Fundraising / Community", r"\b(fundraiser|fundraising|charity|community worker|community officer|engagement officer|outreach worker|outreach officer|trustee|grants officer)\b"),
    ("Security / Emergency Services", r"\b(security|door supervisor|prison officer|custody|police|firefighter|fire fighter|probation officer)\b"),
    ("Agriculture / Environment", r"\b(agriculture|agricultural|farm worker|farm operative|farmer|horticulture|horticultural|gardener|grounds maintenance|landscape|landscaping|environmental officer|ecologist)\b"),
]
COMPILED = [(name, re.compile(pattern, re.IGNORECASE)) for name, pattern in OTHER_RULES]

DESCRIPTION_RULES = {
    "Retail / Store": ["shop floor", "retail store", "store team", "stock shelves", "replenish stock", "checkout", "till", "supermarket", "convenience store"],
    "Care / Support Work": ["personal care", "care home", "residential care", "learning disabilities", "autism", "support people", "supporting people", "children's home", "children’s home", "social work"],
    "Legal / Conveyancing": ["conveyancing", "solicitor", "law firm", "legal advice", "court proceedings", "legal counsel"],
    "Professional Finance / Accountancy": ["bookkeeping", "management accounts", "purchase ledger", "sales ledger", "vat returns", "payroll", "financial planning and analysis", "insolvency"],
    "IT / Data / Software": ["software", "servicenow", "cyber", "penetration testing", "artificial intelligence", "machine learning", "data platform", "product owner", "cloud platform"],
    "Engineering / Technical": ["engineering", "technical design", "mechanical", "electrical", "water design", "maintenance engineering"],
    "Construction / Trades / Property": ["construction site", "principal designer", "cdm", "building project", "contractor management", "quantity surveying"],
    "Property / Housing / Planning": ["housing association", "social housing", "town planning", "planning application", "resident liaison", "tenancy", "rent account", "property lettings"],
    "HR / Recruitment": ["recruitment", "talent acquisition", "employee relations", "human resources"],
    "Employment Support / Careers": ["employability", "employment support", "job coach", "ips employment", "support people into work", "return to work"],
    "Marketing / Digital / Creative": ["paid media", "ppc", "seo", "digital marketing", "social media campaign", "media buying", "bid writing", "tender response"],
    "Insurance / Claims": ["insurance policy", "claims handling", "claims handler", "insurer", "underwriting", "policyholder", "commercial insurance"],
    "Admin / Customer Service": ["customer enquiries", "customer queries", "administrative support", "office administration", "booking appointments", "update records", "data entry", "telephone and email"],
    "Compliance / Risk / Quality": ["regulatory compliance", "risk management", "quality assurance", "governance framework", "compliance monitoring"],
    "Healthcare / Clinical": ["clinical care", "mental health", "psychiatry", "psychology", "patient assessment", "nhs trust"],
}


def norm(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip()).casefold()


def text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def annualised_salary(value: object, period: object) -> float | None:
    raw = text(value).replace(",", "")
    match = re.search(r"\d+(?:\.\d+)?", raw)
    if not match:
        return None
    amount = float(match.group())
    if amount <= 0:
        return None
    # Some JobG8 rows label an already-annual salary as Weekly. A five-figure
    # value is therefore treated as annual before applying period multipliers.
    if amount >= 10000:
        return amount
    salary_period = norm(period)
    if any(term in salary_period for term in ("annual", "annum", "year")):
        return amount
    if "month" in salary_period:
        return amount * 12
    if "week" in salary_period:
        return amount * 52
    if "day" in salary_period:
        return amount * 260
    if "hour" in salary_period:
        return amount * 1950
    return None


def salary_band(minimum: object, maximum: object, period: object) -> str:
    values = [
        value
        for value in (
            annualised_salary(minimum, period),
            annualised_salary(maximum, period),
        )
        if value is not None
    ]
    if not values:
        return "Below £20k / unknown"
    midpoint = sum(values) / len(values)
    if midpoint < 20000:
        return "Below £20k / unknown"
    if midpoint < 35000:
        return "£20k–<£35k"
    if midpoint <= 45000:
        return "£35k–£45k"
    return "Over £45k"


def latest_feed(input_dir: Path) -> Path:
    files = sorted(p for p in input_dir.iterdir() if p.suffix.lower() in {".xlsx", ".xls", ".xlsm"})
    if not files:
        raise SystemExit(f"No Excel feeds found in {input_dir}")
    dated = [(p, re.search(r"(20\d{2}-\d{2}-\d{2})", p.stem)) for p in files]
    dated = [(p, m.group(1)) for p, m in dated if m]
    return max(dated, key=lambda x: x[1])[0] if dated else files[-1]


def split_categories(value: object) -> list[str]:
    return [part.strip() for part in str(value or "").split(";") if part.strip()]


def conflict_categories(value: object) -> set[str]:
    out: set[str] = set()
    for part in split_categories(value):
        if "->HARD_PASS" in part or "->OUT_OF_SCOPE" in part:
            out.add(part.split(":", 1)[0].strip())
    return out


def existing_register_family(row: pd.Series) -> tuple[str | None, str | None]:
    selected = set(split_categories(row.get("selected_categories", "")))
    selected -= conflict_categories(row.get("refinement_conflicts", ""))
    for category in CATEGORY_PRECEDENCE:
        if category in selected:
            return CATEGORY_FAMILY[category], category
    return None, None


def title_refine(title: str, original: str, row: pd.Series) -> tuple[str, str]:
    register_family, register_category = existing_register_family(row)
    if register_family:
        return register_family, f"existing_register:{register_category}"
    if original != "Other / Unclassified":
        return original, "title_rule_pass1"
    for family, rx in COMPILED:
        if rx.search(title):
            return family, "title_rule_pass2"
    return original, "still_unclassified"


def description_family(value: str) -> str | None:
    padded = norm(value)
    if not padded:
        return None
    scores: dict[str, int] = {}
    for family, terms in DESCRIPTION_RULES.items():
        score = sum(1 for term in terms if term in padded)
        if score:
            scores[family] = score
    if not scores:
        return None
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    if ranked[0][1] < 2 or (len(ranked) > 1 and ranked[0][1] == ranked[1][1]):
        return None
    return ranked[0][0]


def raw_feed(input_dir: Path) -> pd.DataFrame:
    return pd.read_excel(latest_feed(input_dir), dtype=str).fillna("")


def description_votes(raw: pd.DataFrame) -> dict[str, Counter[str]]:
    if TITLE_COL not in raw.columns or DESCRIPTION_COL not in raw.columns:
        return {}
    votes: defaultdict[str, Counter[str]] = defaultdict(Counter)
    for _, row in raw.iterrows():
        key = norm(row.get(TITLE_COL, ""))
        if not key:
            continue
        family = description_family(str(row.get(DESCRIPTION_COL, "")))
        if family:
            votes[key][family] += 1
    return dict(votes)


def load_geo_lookups(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    area_df = pd.read_excel(path, dtype=str).fillna("")
    if not {"Area", "Cluster"}.issubset(area_df.columns):
        raise SystemExit("Geo lookup missing Area/Cluster columns")
    area_lookup = {
        norm(row["Area"]): text(row["Cluster"])
        for _, row in area_df.iterrows()
        if norm(row["Area"]) and text(row["Cluster"])
    }
    fallback_df = pd.read_excel(path, sheet_name="LocationFallback", dtype=str).fillna("")
    if not {"Status", "Location", "Cluster"}.issubset(fallback_df.columns):
        raise SystemExit("LocationFallback missing required columns")
    fallback = {
        norm(row["Location"]): text(row["Cluster"])
        for _, row in fallback_df.iterrows()
        if norm(row["Status"]) == "auto" and norm(row["Location"]) and text(row["Cluster"])
    }
    return area_lookup, fallback


def ontap_region(row: pd.Series, area_lookup: dict[str, str], fallback: dict[str, str]) -> str:
    area = norm(row.get(AREA_COL, ""))
    location = norm(row.get(LOCATION_COL, ""))
    if area in AREA_UNUSABLE_VALUES:
        return fallback.get(location, "Other / Unknown")
    return area_lookup.get(area, "Other / Unknown")


def family_geo_metrics(raw: pd.DataFrame, title_family: dict[str, str], geo_lookup_path: Path) -> dict[str, dict[str, object]]:
    area_lookup, fallback = load_geo_lookups(geo_lookup_path)
    counts: defaultdict[str, Counter[str]] = defaultdict(Counter)
    for _, row in raw.iterrows():
        family = title_family.get(norm(row.get(TITLE_COL, "")))
        if not family:
            continue
        counts[family][ontap_region(row, area_lookup, fallback)] += 1
    out: dict[str, dict[str, object]] = {}
    for family, by_region in counts.items():
        known = Counter({r: n for r, n in by_region.items() if r != "Other / Unknown"})
        vals = list(known.values())
        out[family] = {
            "regions": len(known),
            "median": statistics.median(vals) if vals else 0,
            "regions_ge_5": sum(1 for n in vals if n >= 5),
            "regions_ge_10": sum(1 for n in vals if n >= 10),
            "unknown": by_region.get("Other / Unknown", 0),
            "top": "; ".join(f"{r} ({n})" for r, n in known.most_common(5)),
        }
    return out


def family_salary_metrics(raw: pd.DataFrame, title_family: dict[str, str]) -> dict[str, Counter[str]]:
    counts: defaultdict[str, Counter[str]] = defaultdict(Counter)
    for _, row in raw.iterrows():
        family = title_family.get(norm(row.get(TITLE_COL, "")))
        if not family:
            continue
        band = salary_band(
            row.get(SALARY_MIN_COL, ""),
            row.get(SALARY_MAX_COL, ""),
            row.get(SALARY_PERIOD_COL, ""),
        )
        counts[family][band] += 1
    return dict(counts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-csv", required=True, type=Path)
    ap.add_argument("--input-dir", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    ap.add_argument("--geo-lookup", type=Path, default=Path("pipeline/geo/geo_lookup.xlsx"))
    args = ap.parse_args()

    df = pd.read_csv(args.input_csv, dtype=str, encoding="utf-8-sig").fillna("")
    count_col = "count_in_latest_feed"
    required = {count_col, "primary_broad_family", "title", "selected_categories", "refinement_conflicts"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Expected discovery audit CSV columns are missing: {sorted(missing)}")
    df[count_col] = pd.to_numeric(df[count_col], errors="coerce").fillna(0).astype(int)

    refined = [title_refine(str(row["title"]), str(row["primary_broad_family"]), row) for _, row in df.iterrows()]
    df["refined_broad_family"] = [family for family, _ in refined]
    df["reconciliation_basis"] = [basis for _, basis in refined]

    raw = raw_feed(args.input_dir)
    votes = description_votes(raw)
    for idx, row in df.loc[df["reconciliation_basis"] == "still_unclassified"].iterrows():
        key = norm(row["title"])
        title_votes = votes.get(key, Counter())
        if not title_votes:
            continue
        family, vote_count = title_votes.most_common(1)[0]
        occurrences = int(row[count_col])
        required_votes = 1 if occurrences == 1 else max(2, math.ceil(occurrences * 0.6))
        second = title_votes.most_common(2)
        tied = len(second) > 1 and second[1][1] == vote_count
        if vote_count >= required_votes and not tied:
            df.at[idx, "refined_broad_family"] = family
            df.at[idx, "reconciliation_basis"] = "description_majority"

    family_counts: Counter[str] = Counter()
    family_titles: defaultdict[str, Counter[str]] = defaultdict(Counter)
    basis_counts: Counter[str] = Counter()
    family_existing: Counter[str] = Counter()
    for _, row in df.iterrows():
        n = int(row[count_col])
        family = str(row["refined_broad_family"])
        basis = str(row["reconciliation_basis"])
        family_counts[family] += n
        family_titles[family][str(row["title"])] += n
        basis_counts[basis] += n
        if basis.startswith("existing_register:"):
            family_existing[family] += n

    total = int(df[count_col].sum())
    if sum(family_counts.values()) != total:
        raise SystemExit("Refined family reconciliation failed")

    title_family = {norm(row["title"]): str(row["refined_broad_family"]) for _, row in df.iterrows()}
    geo = family_geo_metrics(raw, title_family, args.geo_lookup)
    salaries = family_salary_metrics(raw, title_family)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output_dir / "jobg8-broad-family-reconciliation-current.csv", index=False, encoding="utf-8-sig")
    report_path = args.output_dir / "jobg8-broad-family-reconciliation-current.md"

    original_other = int(df.loc[df["primary_broad_family"] == "Other / Unclassified", count_col].sum())
    remaining_other = family_counts.get("Other / Unclassified", 0)
    existing_register_jobs = sum(family_existing.values())

    lines = [
        "# JobG8 register-first broad-family reconciliation", "",
        f"Jobs reconciled: **{total:,}**",
        f"Jobs assigned first from an existing selected Ontap register: **{existing_register_jobs:,}**",
        f"Original title-rule Other / Unclassified: **{original_other:,}**",
        f"Jobs resolved by description-majority pass: **{basis_counts.get('description_majority', 0):,}**",
        f"Remaining Other / Unclassified after register-first + title + description passes: **{remaining_other:,}**", "",
        "Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.", "",
        "## Refined family totals", "", "| Broad family | Jobs | Share |", "|---|---:|---:|",
    ]
    for family, count in family_counts.most_common():
        lines.append(f"| {family} | {count:,} | {(count / total * 100):.1f}% |")

    lines += [f"| **TOTAL** | **{total:,}** | **100.0%** |", "", "## Refined family totals by salary band", "",
              "Salary uses the midpoint of the available structured minimum/maximum after annualising hourly, daily, weekly or monthly amounts. Five-figure values are treated as annual even when the source period is inconsistent. The first column combines genuinely sub-£20k jobs with missing or unusable salary so every family reconciles exactly to its total.", "",
              "| Broad family | Below £20k / unknown | £20k–<£35k | £35k–£45k | Over £45k | Total |",
              "|---|---:|---:|---:|---:|---:|"]
    salary_totals: Counter[str] = Counter()
    for family, count in family_counts.most_common():
        band_counts = salaries.get(family, Counter())
        if sum(band_counts.values()) != count:
            raise SystemExit(f"Salary-band reconciliation failed for {family}")
        for band in SALARY_BANDS:
            salary_totals[band] += band_counts.get(band, 0)
        lines.append(
            f"| {family} | {band_counts.get(SALARY_BANDS[0], 0):,} | {band_counts.get(SALARY_BANDS[1], 0):,} | "
            f"{band_counts.get(SALARY_BANDS[2], 0):,} | {band_counts.get(SALARY_BANDS[3], 0):,} | {count:,} |"
        )
    if sum(salary_totals.values()) != total:
        raise SystemExit("Overall salary-band reconciliation failed")
    lines.append(
        f"| **TOTAL** | **{salary_totals[SALARY_BANDS[0]]:,}** | **{salary_totals[SALARY_BANDS[1]]:,}** | "
        f"**{salary_totals[SALARY_BANDS[2]]:,}** | **{salary_totals[SALARY_BANDS[3]]:,}** | **{total:,}** |"
    )

    lines += ["", "## Opportunity and Ontap-region density", "",
              "Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.", "",
              "| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |",
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for family, count in family_counts.most_common():
        if family == "Other / Unclassified":
            continue
        existing = family_existing.get(family, 0)
        gm = geo.get(family, {})
        median = gm.get("median", 0)
        median_text = f"{median:.1f}" if isinstance(median, float) else str(median)
        top = str(gm.get("top", "")).replace("|", "\\|")
        lines.append(
            f"| {family} | {count:,} | {existing:,} | {count-existing:,} | {gm.get('regions', 0)} | {median_text} | "
            f"{gm.get('regions_ge_5', 0)} | {gm.get('regions_ge_10', 0)} | {gm.get('unknown', 0)} | {top} |"
        )

    lines += ["", "## Reconciliation basis", "", "| Basis | Jobs |", "|---|---:|"]
    for basis, count in basis_counts.most_common():
        lines.append(f"| {basis} | {count:,} |")
    lines += ["", "## Largest titles still genuinely unclassified", "", "| Count | Title |", "|---:|---|"]
    for title, count in family_titles["Other / Unclassified"].most_common(75):
        safe_title = title.replace("|", "\\|")
        lines.append(f"| {count} | {safe_title} |")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:75]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

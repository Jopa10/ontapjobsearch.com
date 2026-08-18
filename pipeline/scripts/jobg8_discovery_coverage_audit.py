from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path = [entry for entry in sys.path if Path(entry or ".").resolve() != SCRIPT_DIR]

import pandas as pd

TITLE_COL = "/Job/Position"
AREA_COL = "/Job/Area"
LOCATION_COL = "/Job/Location"

REGISTER_FILES = {
    "admin_service": "admin_service_title_classification_register.csv",
    "support_worker": "support_worker_title_classification_register.csv",
    "finance_accounts": "finance_accounts_title_classification_register.csv",
    "customer_service_contact_centre": "customer_service_contact_centre_title_classification_register.csv",
    "hr_recruitment": "hr_recruitment_title_classification_register.csv",
    "warehouse_logistics": "warehouse_logistics_title_classification_register.csv",
}

SELECTED = {"HIGH_CONFIDENCE", "ELASTIC_FIT"}

CLUES = {
    "admin_service": ["admin", "administrator", "administration", "reception", "secretary", "office", "business support", "clerical", "scheduler", "coordinator"],
    "support_worker": ["support worker", "care assistant", "care worker", "healthcare assistant", "residential support", "personal assistant"],
    "finance_accounts": ["accounts", "accounting", "finance", "payroll", "ledger", "credit control", "bookkeeper", "billing", "invoice"],
    "customer_service_contact_centre": ["customer service", "customer support", "contact centre", "call centre", "call handler", "service advisor", "complaints"],
    "hr_recruitment": ["hr ", "human resources", "recruitment", "recruiter", "talent", "people administrator", "people assistant"],
    "warehouse_logistics": ["warehouse", "logistics", "stock", "picker", "packer", "forklift", "goods in", "goods out", "dispatch"],
}

# Diagnostic broad-family rules. Every titled job is assigned to the FIRST matching
# family, once and only once. These are deliberately broad occupational buckets,
# not Ontap publishing decisions.
FAMILY_RULES = [
    ("Education / Teaching", r"\b(teacher|teaching|lecturer|tutor|school|education|headteacher|head teacher|teaching assistant|learning support|cover supervisor|sen|curriculum|academic)\b"),
    ("Healthcare / Clinical", r"\b(nurse|nursing|doctor|medical|clinical|pharmac|physio|therapist|radiograph|sonograph|paramedic|dentist|dental|optomet|veterinary|vet nurse|midwi|health visitor|occupational therapist|psycholog|healthcare)\b"),
    ("Care / Support Work", r"\b(support worker|care assistant|care worker|carer|residential support|home care|domiciliary|support practitioner|care coordinator|care manager|social worker|youth worker)\b"),
    ("Legal / Conveyancing", r"\b(solicitor|lawyer|legal|conveyanc|paralegal|litigation|barrister|probate|fee earner|legal secretary|legal assistant)\b"),
    ("Financial Advice / Mortgages", r"\b(mortgage|financial adviser|financial advisor|ifa\b|wealth manager|wealth adviser|wealth advisor|pensions adviser|pensions advisor|paraplanner|financial planner)\b"),
    ("Professional Finance / Accountancy", r"\b(accountant|accountancy|accounts|finance|financial controller|finance manager|finance director|finance analyst|bookkeep|payroll|purchase ledger|sales ledger|credit control|auditor|audit |tax |taxation|treasury|management accountant)\b"),
    ("IT / Data / Software", r"\b(software|developer|programmer|devops|cloud|cyber|security engineer|data analyst|data engineer|data scientist|database|network engineer|systems engineer|it support|technical support|service desk|helpdesk|infrastructure|solution architect|solutions architect|business analyst|product manager|scrum|qa engineer|test engineer)\b"),
    ("Engineering / Technical", r"\b(engineer|engineering|technician|mechanic|maintenance|electrician|electrical|mechanical|cnc|welder|fabricator|fitter|machinist|cad |draught|quality engineer|process engineer|manufacturing engineer|field service|service engineer)\b"),
    ("Construction / Trades / Property", r"\b(construction|site manager|site supervisor|quantity surveyor|surveyor|estimator|bricklayer|plumber|carpenter|joiner|roofer|painter|decorator|labourer|groundworker|plasterer|property manager|estate agent|lettings|housing officer|facilities manager|building manager)\b"),
    ("Driving / Warehouse / Logistics", r"\b(driver|driving|hgv|lgv|van driver|delivery driver|courier|warehouse|picker|packer|forklift|flt|logistics|transport planner|transport manager|dispatch|despatch|goods in|goods out|stock controller|distribution)\b"),
    ("Sales / Business Development", r"\b(sales|business development|account executive|account manager|commercial manager|telesales|tele sales|sales advisor|sales adviser|sales consultant|sales representative|sales rep|bdm\b|new business|inside sales|field sales)\b"),
    ("Retail / Store", r"\b(retail|store manager|store assistant|shop assistant|shop manager|sales assistant|merchandiser|visual merchandiser|checkout|cashier)\b"),
    ("Marketing / Digital / Creative", r"\b(marketing|digital|seo\b|ppc\b|social media|content|copywriter|graphic designer|designer|creative|communications|pr manager|public relations|brand manager|campaign manager|ecommerce|e-commerce)\b"),
    ("HR / Recruitment", r"\b(hr\b|human resources|recruitment|recruiter|talent acquisition|talent partner|people partner|people advisor|people adviser|employee relations|resourcing)\b"),
    ("Procurement / Buying / Supply Chain", r"\b(procurement|buyer|buying|purchasing|supply chain|category manager|category buyer|materials planner|demand planner|supply planner)\b"),
    ("Hospitality / Catering", r"\b(chef|cook|catering|restaurant|barista|bartender|bar staff|waiter|waitress|kitchen|hotel|housekeeper|housekeeping|front of house|food and beverage)\b"),
    ("Operations / General Management", r"\b(operations manager|general manager|branch manager|regional manager|area manager|programme manager|program manager|project manager|project lead|head of operations|operations director|managing director|chief executive|ceo\b|coo\b)\b"),
    ("Admin / Customer Service", r"\b(admin|administrator|administration|reception|receptionist|secretary|pa\b|personal assistant|office manager|office assistant|coordinator|scheduler|customer service|customer support|contact centre|call centre|call handler|service advisor|service adviser|complaints|business support|clerical)\b"),
    ("Science / Laboratory", r"\b(scientist|laboratory|laboratory technician|lab technician|chemist|microbiolog|biolog|research scientist|research assistant)\b"),
    ("Security / Emergency Services", r"\b(security officer|security guard|police|firefighter|fire fighter|prison officer|custody officer|probation officer)\b"),
]

COMPILED_FAMILY_RULES = [(name, re.compile(pattern, re.IGNORECASE)) for name, pattern in FAMILY_RULES]


def norm(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip()).casefold()


def read_utf8_csv(path: Path) -> pd.DataFrame:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return pd.read_csv(handle, dtype=str).fillna("")


def load_register(path: Path) -> dict[str, str]:
    df = read_utf8_csv(path)
    return {norm(row["title"]): str(row["classification"]).strip().upper() for _, row in df.iterrows() if norm(row["title"])}


def load_refinements(path: Path) -> dict[tuple[str, str], str]:
    if not path.is_file():
        return {}
    df = read_utf8_csv(path)
    out: dict[tuple[str, str], str] = {}
    for _, row in df.iterrows():
        category = str(row.get("category", "")).strip()
        title = norm(row.get("title", ""))
        classification = str(row.get("classification", "")).strip().upper()
        if category and title and classification:
            out[(category, title)] = classification
    return out


def latest_feed(input_dir: Path) -> Path:
    files = sorted(p for p in input_dir.iterdir() if p.suffix.lower() in {".xlsx", ".xls", ".xlsm"})
    if not files:
        raise SystemExit(f"No Excel feeds found in {input_dir}")
    dated = [(p, re.search(r"(20\d{2}-\d{2}-\d{2})", p.stem)) for p in files]
    dated = [(p, m.group(1)) for p, m in dated if m]
    return max(dated, key=lambda x: x[1])[0] if dated else files[-1]


def clue_categories(title_key: str) -> list[str]:
    found = []
    padded = f" {title_key} "
    for category, terms in CLUES.items():
        if any(term in padded for term in terms):
            found.append(category)
    return found


def primary_family(title: str) -> str:
    for family, rx in COMPILED_FAMILY_RULES:
        if rx.search(title):
            return family
    return "Other / Unclassified"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True, type=Path)
    ap.add_argument("--registers-dir", required=True, type=Path)
    ap.add_argument("--refinements", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    args = ap.parse_args()

    feed = latest_feed(args.input_dir)
    df = pd.read_excel(feed, dtype=str).fillna("")
    if TITLE_COL not in df.columns:
        raise SystemExit(f"Missing {TITLE_COL} in {feed}")

    registers = {
        category: load_register(args.registers_dir / filename)
        for category, filename in REGISTER_FILES.items()
    }
    refinements = load_refinements(args.refinements)

    title_counts: Counter[str] = Counter()
    examples: dict[str, str] = {}
    geos: defaultdict[str, Counter[str]] = defaultdict(Counter)
    family_counts: Counter[str] = Counter()
    family_geos: defaultdict[str, Counter[str]] = defaultdict(Counter)
    family_titles: defaultdict[str, Counter[str]] = defaultdict(Counter)

    for _, row in df.iterrows():
        raw_title = str(row.get(TITLE_COL, "")).strip()
        key = norm(raw_title)
        if not key:
            continue
        geo = str(row.get(AREA_COL, "")).strip() or str(row.get(LOCATION_COL, "")).strip() or "Unknown"
        title_counts[key] += 1
        examples.setdefault(key, raw_title)
        geos[key][geo] += 1

        family = primary_family(key)
        family_counts[family] += 1
        family_geos[family][geo] += 1
        family_titles[family][raw_title] += 1

    rows = []
    unknown_relevant_jobs = 0
    conflict_jobs = 0
    for key, count in title_counts.most_common():
        matches = []
        selected_matches = []
        conflicts = []
        for category, register in registers.items():
            cls = register.get(key)
            if cls:
                matches.append(f"{category}:{cls}")
                if cls in SELECTED:
                    selected_matches.append(category)
                    refined = refinements.get((category, key), "")
                    if refined in {"HARD_PASS", "OUT_OF_SCOPE"}:
                        conflicts.append(f"{category}:{cls}->{refined}")
        clues = clue_categories(key)
        status = "KNOWN" if matches else "UNKNOWN"
        if status == "UNKNOWN" and clues:
            unknown_relevant_jobs += count
        if conflicts:
            conflict_jobs += count
        rows.append({
            "title": examples[key],
            "count_in_latest_feed": count,
            "primary_broad_family": primary_family(key),
            "status": status,
            "register_matches": "; ".join(matches),
            "selected_categories": "; ".join(selected_matches),
            "likely_category_clues": "; ".join(clues),
            "refinement_conflicts": "; ".join(conflicts),
            "top_geographies": "; ".join(f"{g} ({n})" for g, n in geos[key].most_common(5)),
        })

    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "jobg8-discovery-coverage-current.csv"
    md_path = args.output_dir / "jobg8-discovery-coverage-current.md"
    pd.DataFrame(rows).to_csv(csv_path, index=False, encoding="utf-8-sig")

    total_jobs = sum(title_counts.values())
    reconciled_total = sum(family_counts.values())
    if reconciled_total != total_jobs:
        raise SystemExit(f"Family reconciliation failed: {reconciled_total} != {total_jobs}")

    known_jobs = sum(r["count_in_latest_feed"] for r in rows if r["status"] == "KNOWN")
    unknown_jobs = total_jobs - known_jobs
    unknown_titles = [r for r in rows if r["status"] == "UNKNOWN"]
    likely_unknown = [r for r in unknown_titles if r["likely_category_clues"]]
    conflicts = [r for r in rows if r["refinement_conflicts"]]

    lines = [
        "# JobG8 discovery coverage audit",
        "",
        f"Feed: `{feed.name}`",
        f"Jobs with titles: **{total_jobs:,}**",
        f"Known to at least one register: **{known_jobs:,}**",
        f"Unknown to every register: **{unknown_jobs:,}**",
        f"Unknown jobs with an existing-category clue: **{unknown_relevant_jobs:,}**",
        f"Jobs in register/refinement conflicts: **{conflict_jobs:,}**",
        "",
        "## Exact broad-family reconciliation",
        "",
        "Every titled job below is counted once and only once using first-match broad occupational rules. This is a diagnostic inventory map, not a publish recommendation.",
        "",
        "| Broad family | Jobs | Share | Top geographies |",
        "|---|---:|---:|---|",
    ]

    for family, count in family_counts.most_common():
        share = (count / total_jobs * 100) if total_jobs else 0
        top_geo = "; ".join(f"{g} ({n})" for g, n in family_geos[family].most_common(5)).replace("|", "\\|")
        lines.append(f"| {family} | {count:,} | {share:.1f}% | {top_geo} |")

    lines += [
        f"| **TOTAL** | **{reconciled_total:,}** | **100.0%** | |",
        "",
        "## Top titles inside each broad family",
        "",
    ]
    for family, count in family_counts.most_common():
        lines.append(f"### {family} — {count:,}")
        lines.append("")
        lines.append("| Count | Title |")
        lines.append("|---:|---|")
        for title, n in family_titles[family].most_common(12):
            lines.append(f"| {n} | {title.replace('|', '\\|')} |")
        lines.append("")

    lines += [
        "## Highest-frequency unknown titles with existing-category clues",
        "",
        "| Count | Title | Likely category clue | Top geographies |",
        "|---:|---|---|---|",
    ]
    for r in likely_unknown[:60]:
        title = str(r["title"]).replace("|", "\\|")
        clues = str(r["likely_category_clues"]).replace("|", "\\|")
        geo = str(r["top_geographies"]).replace("|", "\\|")
        lines.append(f"| {r['count_in_latest_feed']} | {title} | {clues} | {geo} |")

    lines += [
        "",
        "## Register selections contradicted by later refinement rules",
        "",
        "| Count | Title | Conflict |",
        "|---:|---|---|",
    ]
    if conflicts:
        for r in conflicts[:80]:
            title = str(r["title"]).replace("|", "\\|")
            conflict = str(r["refinement_conflicts"]).replace("|", "\\|")
            lines.append(f"| {r['count_in_latest_feed']} | {title} | {conflict} |")
    else:
        lines.append("| 0 | None | None |")

    lines += [
        "",
        "## Interpretation",
        "",
        "This report is diagnostic only. It does not change registers, slice status, reviews, or live job pages.",
        "The broad-family reconciliation is intentionally exhaustive: the family total must equal the feed total.",
        "Broad-family keyword assignment is for opportunity discovery; individual titles still need inspection before any new Ontap family is approved.",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:32]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

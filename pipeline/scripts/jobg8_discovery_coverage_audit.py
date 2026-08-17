from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

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
    for _, row in df.iterrows():
        raw_title = str(row.get(TITLE_COL, "")).strip()
        key = norm(raw_title)
        if not key:
            continue
        title_counts[key] += 1
        examples.setdefault(key, raw_title)
        geo = str(row.get(AREA_COL, "")).strip() or str(row.get(LOCATION_COL, "")).strip() or "Unknown"
        geos[key][geo] += 1

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
        "## Highest-frequency unknown titles with category clues",
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
        "Unknown-title clues are deliberately broad prompts for human audit, not automatic classifications.",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:14]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

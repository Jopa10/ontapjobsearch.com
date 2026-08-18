from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# This repo contains pipeline/scripts/pandas.py as a compatibility shim. Remove
# the script directory while importing so this audit gets the installed pandas
# package rather than the local shim.
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path = [entry for entry in sys.path if Path(entry or ".").resolve() != SCRIPT_DIR]

import pandas as pd

# Existing Ontap selected registers take priority over broad title heuristics.
# This prevents jobs already covered by Ontap (e.g. Bookkeeper in finance,
# Sales Administrator in admin) from being presented as a new-category gap.
CATEGORY_FAMILY = {
    "support_worker": "Care / Support Work",
    "finance_accounts": "Professional Finance / Accountancy",
    "hr_recruitment": "HR / Recruitment",
    "warehouse_logistics": "Driving / Warehouse / Logistics",
    "customer_service_contact_centre": "Admin / Customer Service",
    "admin_service": "Admin / Customer Service",
}
CATEGORY_PRECEDENCE = [
    "support_worker",
    "finance_accounts",
    "hr_recruitment",
    "warehouse_logistics",
    "customer_service_contact_centre",
    "admin_service",
]

# Second-pass rules only apply where there is no effective selected Ontap
# register and the first broad-family pass left the title unclassified.
OTHER_RULES = [
    ("Legal / Conveyancing", r"\b(conveyancer|conveyancing)\b"),
    ("Professional Finance / Accountancy", r"\b(bookkeeper|bookkeeping|fp&a|fp and a|financial planning and analysis)\b"),
    ("Healthcare / Clinical", r"\b(optometrist|optician|optical assistant|dispensing optician|pharmacist|pharmacy|psychologist|podiatrist|audiologist|audiology|physiotherapy|physiotherapist|functional assessor)\b"),
    ("IT / Data / Software", r"\b(ai consultant|artificial intelligence consultant|ethical hacker|penetration tester|pen tester)\b"),
    ("Market Research / Field Interviewing", r"\b(market research|field interviewer|research interviewer|survey interviewer|field researcher)\b"),
    ("Insurance / Claims", r"\b(insurance|claims?|underwriter|underwriting|loss adjuster|adjuster|broker|actuarial|actuary|reinsurance)\b"),
    ("Compliance / Risk / Quality", r"\b(compliance manager|compliance officer|risk assessor|risk manager|quality manager|quality assurance manager|regulatory manager)\b"),
    ("Property / Housing / Planning", r"\b(town planner|planning officer|resident liaison officer|housing solutions officer|income officer|scheme manager|housing manager)\b"),
    ("Manufacturing / Production", r"\b(production|manufacturing|machine operator|machine operative|assembler|assembly|factory|plant operator|process operator|production operative|production operator)\b"),
    ("Cleaning / Domestic / Facilities", r"\b(cleaner|cleaning|domestic assistant|domestic cleaner|caretaker|janitor|facilities assistant|facilities operative|hygiene operative)\b"),
    ("Management / Team Leadership", r"\b(registered manager|deputy manager|assistant manager|service manager|team leader|client manager|centre manager|unit manager|department manager|supervisor|practice manager|business manager|home manager)\b"),
    ("Admin / Customer Service", r"\b(executive assistant|executive pa|ea\b|credit controller|credit control|office support|business administrator|administrative assistant|document controller|service controller|hire controller|parts advisor)\b"),
    ("Charity / Fundraising / Community", r"\b(fundraiser|fundraising|charity|community worker|community officer|engagement officer|outreach worker|outreach officer)\b"),
    ("Security / Emergency Services", r"\b(security|door supervisor|prison officer|custody|police|firefighter|fire fighter|probation officer)\b"),
    ("Agriculture / Environment", r"\b(agriculture|agricultural|farm worker|farm operative|farmer|horticulture|horticultural|gardener|grounds maintenance|landscape|landscaping|environmental officer|ecologist)\b"),
]
COMPILED = [(name, re.compile(pattern, re.IGNORECASE)) for name, pattern in OTHER_RULES]


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


def refine(title: str, original: str, row: pd.Series) -> tuple[str, str]:
    register_family, register_category = existing_register_family(row)
    if register_family:
        return register_family, f"existing_register:{register_category}"
    if original != "Other / Unclassified":
        return original, "title_rule_pass1"
    for family, rx in COMPILED:
        if rx.search(title):
            return family, "title_rule_pass2"
    return original, "still_unclassified"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-csv", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    args = ap.parse_args()

    df = pd.read_csv(args.input_csv, dtype=str, encoding="utf-8-sig").fillna("")
    count_col = "count_in_latest_feed"
    required = {count_col, "primary_broad_family", "title", "selected_categories", "refinement_conflicts"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Expected discovery audit CSV columns are missing: {sorted(missing)}")

    df[count_col] = pd.to_numeric(df[count_col], errors="coerce").fillna(0).astype(int)
    refined = [
        refine(str(row["title"]), str(row["primary_broad_family"]), row)
        for _, row in df.iterrows()
    ]
    df["refined_broad_family"] = [family for family, _ in refined]
    df["reconciliation_basis"] = [basis for _, basis in refined]

    total = int(df[count_col].sum())
    family_counts: Counter[str] = Counter()
    family_titles: defaultdict[str, Counter[str]] = defaultdict(Counter)
    basis_counts: Counter[str] = Counter()

    for _, row in df.iterrows():
        n = int(row[count_col])
        family = str(row["refined_broad_family"])
        basis = str(row["reconciliation_basis"])
        family_counts[family] += n
        family_titles[family][str(row["title"])] += n
        basis_counts[basis] += n

    if sum(family_counts.values()) != total:
        raise SystemExit("Refined family reconciliation failed")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = args.output_dir / "jobg8-broad-family-reconciliation-current.csv"
    report_path = args.output_dir / "jobg8-broad-family-reconciliation-current.md"
    df.to_csv(detail_path, index=False, encoding="utf-8-sig")

    original_other = int(df.loc[df["primary_broad_family"] == "Other / Unclassified", count_col].sum())
    remaining_other = family_counts.get("Other / Unclassified", 0)
    existing_register_jobs = sum(count for basis, count in basis_counts.items() if basis.startswith("existing_register:"))

    lines = [
        "# JobG8 register-first broad-family reconciliation",
        "",
        f"Jobs reconciled: **{total:,}**",
        f"Jobs assigned first from an existing selected Ontap register: **{existing_register_jobs:,}**",
        f"Original title-rule Other / Unclassified: **{original_other:,}**",
        f"Remaining Other / Unclassified after register-first + second pass: **{remaining_other:,}**",
        "",
        "Every job is counted once and only once. Existing selected Ontap registers take priority; only then are broad title rules used. This is diagnostic only and does not change publishing logic.",
        "",
        "## Refined family totals",
        "",
        "| Broad family | Jobs | Share |",
        "|---|---:|---:|",
    ]
    for family, count in family_counts.most_common():
        share = count / total * 100 if total else 0
        lines.append(f"| {family} | {count:,} | {share:.1f}% |")
    lines += [
        f"| **TOTAL** | **{total:,}** | **100.0%** |",
        "",
        "## Reconciliation basis",
        "",
        "| Basis | Jobs |",
        "|---|---:|",
    ]
    for basis, count in basis_counts.most_common():
        lines.append(f"| {basis} | {count:,} |")

    lines += ["", "## Largest titles still genuinely unclassified", "", "| Count | Title |", "|---:|---|"]
    for title, count in family_titles["Other / Unclassified"].most_common(50):
        safe_title = title.replace("|", "\\|")
        lines.append(f"| {count} | {safe_title} |")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:45]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

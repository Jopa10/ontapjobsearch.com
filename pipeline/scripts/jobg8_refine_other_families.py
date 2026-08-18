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

# Second-pass rules only apply to rows left as Other / Unclassified by the
# exhaustive first-pass audit. First match wins. These are diagnostic broad
# occupational families, not publishing decisions.
OTHER_RULES = [
    ("Market Research / Field Interviewing", r"\b(market research|field interviewer|research interviewer|survey interviewer|field researcher)\b"),
    ("Insurance / Claims", r"\b(insurance|claims?|underwriter|underwriting|loss adjuster|adjuster|broker|actuar|actuary|reinsurance)\b"),
    ("Manufacturing / Production", r"\b(production|manufacturing|machine operator|machine operative|assembler|assembly|factory|plant operator|process operator|production operative|production operator)\b"),
    ("Cleaning / Domestic / Facilities", r"\b(cleaner|cleaning|domestic assistant|domestic cleaner|caretaker|janitor|facilities assistant|facilities operative)\b"),
    ("Management / Team Leadership", r"\b(registered manager|deputy manager|assistant manager|service manager|team leader|client manager|centre manager|unit manager|department manager|supervisor)\b"),
    ("Admin / Customer Service", r"\b(executive assistant|executive pa|ea\b|credit controller|credit control|office support|business administrator|administrative assistant)\b"),
    ("Healthcare / Clinical", r"\b(optometrist|optician|optical assistant|dispensing optician|pharmacist|pharmacy|psychologist|podiatrist|audiologist|audiology)\b"),
    ("Charity / Fundraising / Community", r"\b(fundraiser|fundraising|charity|community worker|community officer|engagement officer|outreach worker|outreach officer)\b"),
    ("Security / Emergency Services", r"\b(security|door supervisor|prison officer|custody|police|firefighter|fire fighter|probation officer)\b"),
    ("Agriculture / Environment", r"\b(agricultur|farm worker|farm operative|farmer|horticultur|gardener|grounds maintenance|landscap|environmental officer|ecologist)\b"),
]
COMPILED = [(name, re.compile(pattern, re.IGNORECASE)) for name, pattern in OTHER_RULES]


def refine(title: str, original: str) -> str:
    if original != "Other / Unclassified":
        return original
    for family, rx in COMPILED:
        if rx.search(title):
            return family
    return original


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-csv", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    args = ap.parse_args()

    df = pd.read_csv(args.input_csv, dtype=str, encoding="utf-8-sig").fillna("")
    count_col = "count_in_latest_feed"
    if count_col not in df.columns or "primary_broad_family" not in df.columns or "title" not in df.columns:
        raise SystemExit("Expected discovery audit CSV columns are missing")

    df[count_col] = pd.to_numeric(df[count_col], errors="coerce").fillna(0).astype(int)
    df["refined_broad_family"] = [
        refine(str(title), str(family))
        for title, family in zip(df["title"], df["primary_broad_family"])
    ]

    total = int(df[count_col].sum())
    family_counts: Counter[str] = Counter()
    family_titles: defaultdict[str, Counter[str]] = defaultdict(Counter)
    moved_counts: Counter[str] = Counter()

    for _, row in df.iterrows():
        n = int(row[count_col])
        family = str(row["refined_broad_family"])
        family_counts[family] += n
        family_titles[family][str(row["title"])] += n
        if str(row["primary_broad_family"]) == "Other / Unclassified" and family != "Other / Unclassified":
            moved_counts[family] += n

    if sum(family_counts.values()) != total:
        raise SystemExit("Refined family reconciliation failed")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    detail_path = args.output_dir / "jobg8-broad-family-reconciliation-current.csv"
    report_path = args.output_dir / "jobg8-broad-family-reconciliation-current.md"
    df.to_csv(detail_path, index=False, encoding="utf-8-sig")

    original_other = int(df.loc[df["primary_broad_family"] == "Other / Unclassified", count_col].sum())
    remaining_other = family_counts.get("Other / Unclassified", 0)
    moved = original_other - remaining_other

    lines = [
        "# JobG8 refined broad-family reconciliation",
        "",
        f"Jobs reconciled: **{total:,}**",
        f"Original Other / Unclassified: **{original_other:,}**",
        f"Moved into added families on second pass: **{moved:,}**",
        f"Remaining Other / Unclassified: **{remaining_other:,}**",
        "",
        "Every job is still counted once and only once. This is a diagnostic inventory map, not a publishing recommendation.",
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
        "## Added categories from the old Other bucket",
        "",
        "| Added family | Jobs moved |",
        "|---|---:|",
    ]
    for family, count in moved_counts.most_common():
        lines.append(f"| {family} | {count:,} |")

    lines += ["", "## Largest titles still unclassified", "", "| Count | Title |", "|---:|---|"]
    for title, count in family_titles["Other / Unclassified"].most_common(50):
        safe_title = title.replace("|", "\\|")
        lines.append(f"| {count} | {safe_title} |")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:35]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

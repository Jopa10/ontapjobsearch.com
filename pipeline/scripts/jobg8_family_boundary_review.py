from __future__ import annotations

import argparse
import html
import re
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path = [entry for entry in sys.path if Path(entry or ".").resolve() != SCRIPT_DIR]

import pandas as pd

TITLE_COL = "/Job/Position"
DESCRIPTION_COL = "/Job/Description"
DISPLAY_REF_COL = "/Job/DisplayReference"


def norm(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def clean_description(value: object) -> str:
    text = html.unescape(norm(value))
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def latest_feed(input_dir: Path) -> Path:
    files = sorted(p for p in input_dir.iterdir() if p.suffix.lower() in {".xlsx", ".xls", ".xlsm"})
    if not files:
        raise SystemExit(f"No Excel feeds found in {input_dir}")
    dated = [(p, re.search(r"(20\d{2}-\d{2}-\d{2})", p.stem)) for p in files]
    dated = [(p, m.group(1)) for p, m in dated if m]
    return max(dated, key=lambda x: x[1])[0] if dated else files[-1]


def evidence_snippet(description: str, keywords: list[str], width: int = 1200) -> str:
    if not description:
        return ""
    folded = description.casefold()
    hits = [folded.find(k.casefold()) for k in keywords if k and folded.find(k.casefold()) >= 0]
    if not hits:
        return description[:width]
    hit = min(hits)
    start = max(0, hit - width // 3)
    end = min(len(description), start + width)
    if start > 0:
        start = description.rfind(" ", 0, start)
        start = max(0, start)
    return ("…" if start > 0 else "") + description[start:end] + ("…" if end < len(description) else "")


def numeric(value: object) -> float | None:
    try:
        n = float(value)
    except (TypeError, ValueError):
        return None
    return n if pd.notna(n) else None


def first_existing(columns: set[str], *names: str) -> str | None:
    for name in names:
        if name in columns:
            return name
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a compact one-advert-per-row family boundary review file.")
    ap.add_argument("--input-dir", required=True, type=Path)
    ap.add_argument("--diagnostic-csv", required=True, type=Path)
    ap.add_argument("--output-csv", required=True, type=Path)
    ap.add_argument("--summary-md", type=Path)
    ap.add_argument("--family-name", default="Family")
    ap.add_argument("--keywords", default="")
    ap.add_argument("--exclude-decision", action="append", default=[])
    ap.add_argument("--hard-salary-max", type=float, default=50000)
    args = ap.parse_args()

    diagnostic = pd.read_csv(args.diagnostic_csv, dtype=str).fillna("")
    columns = set(diagnostic.columns)
    if "display_reference" not in columns:
        raise SystemExit("Diagnostic CSV must contain display_reference")

    decision_col = first_existing(columns, "discovery_decision", "provisional_decision")
    reason_col = first_existing(columns, "discovery_reason", "provisional_reason")
    region_col = first_existing(columns, "ontap_region", "assessable_market", "ontap_geo_cluster")
    if not decision_col:
        raise SystemExit("Diagnostic CSV must contain discovery_decision or provisional_decision")

    if args.exclude_decision:
        diagnostic = diagnostic.loc[~diagnostic[decision_col].isin(args.exclude_decision)].copy()

    feed = latest_feed(args.input_dir)
    raw = pd.read_excel(feed, dtype=str).fillna("")
    if DISPLAY_REF_COL not in raw.columns or DESCRIPTION_COL not in raw.columns:
        raise SystemExit("Latest feed is missing display reference or description")

    raw_lookup = {}
    for _, row in raw.iterrows():
        ref = norm(row.get(DISPLAY_REF_COL, ""))
        if ref and ref not in raw_lookup:
            raw_lookup[ref] = {
                "raw_title": norm(row.get(TITLE_COL, "")),
                "description": clean_description(row.get(DESCRIPTION_COL, "")),
            }

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    rows: list[dict[str, object]] = []
    for _, row in diagnostic.iterrows():
        ref = norm(row.get("display_reference", ""))
        source = raw_lookup.get(ref, {})
        description = source.get("description", "")
        annual_max = numeric(row.get("annualised_maximum_estimate", ""))
        hard_salary_out = bool(annual_max is not None and annual_max > args.hard_salary_max)
        rows.append({
            "display_reference": ref,
            "title": norm(row.get("title", "")) or source.get("raw_title", ""),
            "current_decision": norm(row.get(decision_col, "")),
            "current_reason": norm(row.get(reason_col, "")) if reason_col else "",
            "jobg8_classification": norm(row.get("jobg8_classification", "")),
            "ontap_region": norm(row.get(region_col, "")) if region_col else "",
            "salary_minimum_raw": norm(row.get("salary_minimum_raw", "")),
            "salary_maximum_raw": norm(row.get("salary_maximum_raw", "")),
            "salary_period": norm(row.get("salary_period", "")),
            "annualised_maximum_estimate": row.get("annualised_maximum_estimate", ""),
            "hard_salary_out_over_50k": "YES" if hard_salary_out else "NO",
            "description_evidence": evidence_snippet(description, keywords),
            "manual_boundary_decision": "",
            "manual_boundary_note": "",
        })

    out = pd.DataFrame(rows)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output_csv, index=False, encoding="utf-8-sig")

    print(f"Boundary review rows: {len(out):,}")
    print(f"Hard salary outs (> £{args.hard_salary_max:,.0f} max): {(out['hard_salary_out_over_50k'] == 'YES').sum():,}")
    print(f"Output: {args.output_csv}")

    if args.summary_md:
        decision_counts = Counter(out["current_decision"])
        title_counts = out["title"].value_counts().head(40)
        class_counts = out["jobg8_classification"].replace("", "(blank)").value_counts().head(20)
        lines = [
            f"# {args.family_name} boundary-review evidence",
            "",
            f"Feed: **{feed.name}**",
            f"Advert rows for boundary review: **{len(out):,}**.",
            f"Hard salary outs above £{args.hard_salary_max:,.0f}: **{(out['hard_salary_out_over_50k'] == 'YES').sum():,}**.",
            "",
            "This is boundary-review evidence only. The current discovery decision is provisional; `manual_boundary_decision` remains blank until the family boundary is frozen.",
            "",
            "## Current provisional decisions",
            "",
            "| Decision | Jobs |",
            "|---|---:|",
        ]
        for decision, count in decision_counts.most_common():
            lines.append(f"| {decision or '(blank)'} | {count:,} |")
        lines += ["", "## Most common exact titles", "", "| Title | Jobs |", "|---|---:|"]
        for title, count in title_counts.items():
            lines.append(f"| {str(title).replace('|', '/')} | {count:,} |")
        lines += ["", "## JobG8 classification spread", "", "| Classification | Jobs |", "|---|---:|"]
        for classification, count in class_counts.items():
            lines.append(f"| {str(classification).replace('|', '/')} | {count:,} |")
        args.summary_md.parent.mkdir(parents=True, exist_ok=True)
        args.summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Summary: {args.summary_md}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

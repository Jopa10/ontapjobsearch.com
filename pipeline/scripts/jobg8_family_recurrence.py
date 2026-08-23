from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def as_bool_false(value: object) -> bool:
    return str(value).strip().casefold() in {"false", "0", "no", ""}


def main() -> int:
    ap = argparse.ArgumentParser(description="Summarise one governed family discovery across the canonical UK assessment markets.")
    ap.add_argument("--discovery-csv", required=True, type=Path)
    ap.add_argument("--config", required=True, type=Path)
    ap.add_argument("--assessable-regions", type=Path, default=Path("pipeline/config/uk_assessable_regions.json"))
    ap.add_argument("--output-dir", required=True, type=Path)
    args = ap.parse_args()

    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    family_key = str(cfg["family_key"])
    display_name = str(cfg["display_name"])

    geo = json.loads(args.assessable_regions.read_text(encoding="utf-8"))
    markets = list(geo.get("regions", {}).keys())
    expected = int(geo.get("region_count", len(markets)))
    if expected != len(markets):
        raise SystemExit(f"Canonical geography says {expected} markets but contains {len(markets)}")

    df = pd.read_csv(args.discovery_csv, dtype=str).fillna("")
    required = {"assessable_market", "in_uk_market_universe", "provisional_decision"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Discovery CSV missing columns: {sorted(missing)}")

    if "is_duplicate" in df.columns:
        df = df.loc[df["is_duplicate"].map(as_bool_false)].copy()
    df = df.loc[df["in_uk_market_universe"].str.upper().eq("YES")].copy()

    rows = []
    for market in markets:
        part = df.loc[df["assessable_market"].eq(market)]
        likely = int(part["provisional_decision"].eq("LIKELY_IN").sum())
        borderline = int(part["provisional_decision"].eq("BORDERLINE").sum())
        out_salary = int(part["provisional_decision"].eq("OUT_SALARY").sum())
        out_specialist = int(part["provisional_decision"].eq("OUT_SPECIALIST").sum())
        rows.append({
            "market": market,
            "likely_in": likely,
            "borderline": borderline,
            "plausible_including_borderline": likely + borderline,
            "out_salary": out_salary,
            "out_specialist": out_specialist,
        })

    out = pd.DataFrame(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stem = family_key.replace("_", "-")
    csv_path = args.output_dir / f"jobg8-{stem}-recurrence-current.csv"
    md_path = args.output_dir / f"jobg8-{stem}-recurrence-current.md"
    out.to_csv(csv_path, index=False, encoding="utf-8-sig")

    likely_total = int(out["likely_in"].sum())
    borderline_total = int(out["borderline"].sum())
    active_markets = int((out["likely_in"] > 0).sum())
    likely_3 = int((out["likely_in"] >= 3).sum())
    likely_6 = int((out["likely_in"] >= 6).sum())
    likely_9 = int((out["likely_in"] >= 9).sum())
    ranked = out.sort_values(["likely_in", "borderline", "market"], ascending=[False, False, True]).head(30)

    lines = [
        f"# JobG8 {display_name} regional recurrence — current feed", "",
        f"Canonical UK assessment universe: **{len(markets)} markets**.",
        f"LIKELY_IN jobs mapped into the universe: **{likely_total}**.",
        f"BORDERLINE jobs mapped into the universe: **{borderline_total}**.",
        f"Markets with at least one LIKELY_IN job: **{active_markets} / {len(markets)}**.", "",
        "Descriptive current-feed spread only — these thresholds do not activate a slice:",
        f"- markets with 3+ LIKELY_IN: **{likely_3}**",
        f"- markets with 6+ LIKELY_IN: **{likely_6}**",
        f"- markets with 9+ LIKELY_IN: **{likely_9}**", "",
        "## Strongest current markets", "",
        "| Market | LIKELY_IN | BORDERLINE | Plausible incl. borderline |",
        "|---|---:|---:|---:|",
    ]
    for _, row in ranked.iterrows():
        lines.append(
            f"| {str(row['market']).replace('|', '/')} | {int(row['likely_in'])} | {int(row['borderline'])} | {int(row['plausible_including_borderline'])} |"
        )
    lines += [
        "", "This report is diagnostic evidence only. New-family LIVE activation remains an explicit owner decision after the governed family boundary and national validation are complete.",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(md_path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

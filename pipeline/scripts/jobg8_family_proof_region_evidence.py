from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import pandas as pd


def falseish(value: object) -> bool:
    return str(value).strip().casefold() in {"", "false", "0", "no"}


def main() -> int:
    ap = argparse.ArgumentParser(description="Build proof-region evidence from a governed family discovery output.")
    ap.add_argument("--discovery-csv", required=True, type=Path)
    ap.add_argument("--config", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    ap.add_argument("--markets", type=int, default=5)
    args = ap.parse_args()

    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    family_key = str(cfg["family_key"])
    display_name = str(cfg["display_name"])
    viability_floor = int(cfg.get("viability_floor", 100))
    df = pd.read_csv(args.discovery_csv, dtype=str).fillna("")

    required = {"title", "assessable_market", "in_uk_market_universe", "provisional_decision"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Discovery CSV missing columns: {sorted(missing)}")
    if "is_duplicate" in df.columns:
        df = df.loc[df["is_duplicate"].map(falseish)].copy()
    if "is_content_duplicate" in df.columns:
        df = df.loc[df["is_content_duplicate"].map(falseish)].copy()

    plausible_national = int(df["provisional_decision"].isin(["LIKELY_IN", "BORDERLINE"]).sum())
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stem = family_key.replace("_", "-")
    md_path = args.output_dir / f"jobg8-{stem}-proof-region-evidence-current.md"
    csv_path = args.output_dir / f"jobg8-{stem}-proof-region-evidence-current.csv"

    if plausible_national < viability_floor:
        lines = [
            f"# JobG8 {display_name} proof-region evidence candidates", "",
            f"Status: **SKIPPED / BELOW NATIONAL VIABILITY FLOOR**.", "",
            f"Content-unique LIKELY_IN + BORDERLINE national inventory: **{plausible_national}**.",
            f"Viability floor: **{viability_floor}**.", "",
            "No proof-region advert expansion is generated for a family that is below the national scale gate.",
        ]
        md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        pd.DataFrame(columns=["market", "display_reference", "title", "decision", "reason", "salary_bucket", "jobg8_classification", "description_excerpt"]).to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(md_path.read_text(encoding="utf-8"))
        return 0

    df = df.loc[df["in_uk_market_universe"].str.upper().eq("YES")].copy()
    score = (
        df.assign(
            likely=df["provisional_decision"].eq("LIKELY_IN").astype(int),
            borderline=df["provisional_decision"].eq("BORDERLINE").astype(int),
        )
        .groupby("assessable_market", as_index=False)[["likely", "borderline"]]
        .sum()
    )
    score["plausible"] = score["likely"] + score["borderline"]
    score = score.sort_values(["likely", "borderline", "assessable_market"], ascending=[False, False, True])
    chosen = score.head(max(1, args.markets))["assessable_market"].tolist()

    lines = [
        f"# JobG8 {display_name} proof-region evidence candidates", "",
        f"Content-unique national LIKELY_IN + BORDERLINE inventory: **{plausible_national}** against viability floor **{viability_floor}**.",
        "This report does not approve proof regions or any LIVE slice. It surfaces the strongest current markets for human boundary inspection after national discovery.", "",
    ]
    evidence_rows: list[dict[str, object]] = []
    for market in chosen:
        part = df.loc[df["assessable_market"].eq(market)].copy()
        likely = part.loc[part["provisional_decision"].eq("LIKELY_IN")]
        borderline = part.loc[part["provisional_decision"].eq("BORDERLINE")]
        outs = part.loc[part["provisional_decision"].isin(["OUT_SALARY", "OUT_SPECIALIST"])]
        title_counts = Counter(likely["title"])
        lines += [
            f"## {market}", "",
            f"- LIKELY_IN: **{len(likely)}**",
            f"- BORDERLINE: **{len(borderline)}**",
            f"- Provisional OUT: **{len(outs)}**", "",
            "Most common LIKELY_IN titles:", "",
        ]
        if title_counts:
            for title, count in title_counts.most_common(12):
                lines.append(f"- {title}: {count}")
        else:
            lines.append("- none")
        if len(borderline):
            lines += ["", "Borderline titles:", ""]
            for title, count in Counter(borderline["title"]).most_common():
                lines.append(f"- {title}: {count}")
        lines.append("")
        for _, row in part.iterrows():
            evidence_rows.append({
                "market": market,
                "display_reference": row.get("display_reference", ""),
                "title": row.get("title", ""),
                "decision": row.get("provisional_decision", ""),
                "reason": row.get("provisional_reason", ""),
                "salary_bucket": row.get("salary_bucket", ""),
                "jobg8_classification": row.get("jobg8_classification", ""),
                "description_excerpt": row.get("description_excerpt", ""),
            })

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    pd.DataFrame(evidence_rows).to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(md_path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
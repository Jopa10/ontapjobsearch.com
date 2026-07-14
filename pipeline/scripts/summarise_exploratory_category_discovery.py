#!/usr/bin/env python3
"""Create a review shortlist and readable summary from exploratory Module 2 output."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def run(validation_path: Path, shortlist_path: Path, summary_path: Path) -> None:
    df = pd.read_csv(validation_path, dtype=str).fillna("")
    numeric = [
        "average_daily_count", "days_seen", "feed_days", "first_five_day_average",
        "last_five_day_average", "unique_title_count", "unique_company_count",
        "unique_location_count", "top_1_company_share_pct", "top_2_company_share_pct",
    ]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df = df[
        df["region_scope"].isin(["lookup_region", "published_aggregate"])
        & df["region"].ne("Other / Unknown")
    ].copy()
    df["credible_slice"] = (
        df["recommendation"].eq("BUILD")
        & df["last_five_day_average"].ge(3)
        & df["concentration_risk"].ne("HIGH")
    )
    df["manual_review_pilot"] = (
        df["recommendation"].eq("BUILD")
        & df["last_five_day_average"].ge(3)
        & df["unique_company_count"].ge(3)
        & df["unique_location_count"].ge(3)
    )
    shortlist = df[df["recommendation"].isin(["BUILD", "WATCH"])].sort_values(
        ["credible_slice", "manual_review_pilot", "recommendation", "average_daily_count", "last_five_day_average"],
        ascending=[False, False, True, False, False],
    )
    shortlist.to_csv(shortlist_path, index=False, encoding="utf-8-sig")

    category_rows = []
    for category, group in df.groupby("category"):
        builds = group[group["recommendation"] == "BUILD"]
        watches = group[group["recommendation"] == "WATCH"]
        credible = group[group["credible_slice"]]
        top = group.sort_values("average_daily_count", ascending=False).head(1)
        top_region = top.iloc[0]["region"] if not top.empty else ""
        top_avg = float(top.iloc[0]["average_daily_count"]) if not top.empty else 0.0
        if len(credible) >= 2:
            decision = "STRONG"
        elif len(builds) >= 1 or len(watches) >= 3:
            decision = "PILOT_OR_WATCH"
        else:
            decision = "REJECT_FOR_NOW"
        category_rows.append((category, len(builds), len(watches), len(credible), top_region, top_avg, decision))

    credible_df = df[df["credible_slice"]].sort_values(
        ["average_daily_count", "last_five_day_average"], ascending=False
    )
    pilot_df = df[df["manual_review_pilot"]].sort_values(
        ["average_daily_count", "last_five_day_average"], ascending=False
    )
    lines = [
        "# July 2026 exploratory category discovery",
        "",
        f"Credible new region × category slices: **{len(credible_df)}**",
        f"At least six credible slices exist: **{'YES' if len(credible_df) >= 6 else 'NO'}**",
        f"Slices stable enough for a manual-review pilot: **{len(pilot_df)}**",
        "",
        "## Candidate-family assessment",
        "",
        "| Category | BUILD | WATCH | Credible | Strongest region | Top avg/day | Decision |",
        "|---|---:|---:|---:|---|---:|---|",
    ]
    for row in sorted(category_rows, key=lambda x: (-x[3], -x[1], -x[5], x[0])):
        lines.append(
            f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | "
            f"{row[4]} | {row[5]:.2f} | {row[6]} |"
        )

    lines += ["", "## Strongest credible slices", ""]
    if credible_df.empty:
        lines.append("None met the credible-slice safeguard.")
    else:
        lines.append(
            "| Region | Category | Avg/day | Days present | First 5 | Last 5 | Companies | Locations | Concentration | Reason |"
        )
        lines.append("|---|---|---:|---:|---:|---:|---:|---:|---|---|")
        for _, row in credible_df.head(30).iterrows():
            reason = str(row["recommendation_reason"]).replace("|", "/")
            lines.append(
                f"| {row['region']} | {row['category']} | {row['average_daily_count']:.2f} | "
                f"{int(row['days_seen'])}/{int(row['feed_days'])} | {row['first_five_day_average']:.2f} | "
                f"{row['last_five_day_average']:.2f} | {int(row['unique_company_count'])} | "
                f"{int(row['unique_location_count'])} | {row['concentration_risk']} | {reason} |"
            )

    lines += ["", "## Manual-review pilot candidates", ""]
    if pilot_df.empty:
        lines.append("None met the pilot safeguard.")
    else:
        for _, row in pilot_df.head(20).iterrows():
            lines.append(
                f"- {row['region']} × {row['category']} — {row['average_daily_count']:.2f}/day; "
                f"last five days {row['last_five_day_average']:.2f}; "
                f"{int(row['unique_company_count'])} advertisers."
            )

    rejected = [row[0] for row in category_rows if row[-1] == "REJECT_FOR_NOW"]
    lines += [
        "",
        "## Candidate families rejected for now",
        "",
        ", ".join(rejected) if rejected else "None.",
    ]
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation", required=True)
    parser.add_argument("--shortlist", required=True)
    parser.add_argument("--summary", required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(Path(args.validation), Path(args.shortlist), Path(args.summary))

#!/usr/bin/env python3
"""Create a review shortlist and readable summary from exploratory Module 2 output."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

EXPECTED_CATEGORIES = [
    "care_assistant_healthcare_assistant",
    "teaching_sen_learning_support",
    "broader_customer_service",
    "broader_office_administration",
    "residential_childcare_children_support",
    "warehouse_logistics_operative",
]


def run(validation_path: Path, shortlist_path: Path, summary_path: Path) -> None:
    df = pd.read_csv(validation_path, dtype=str).fillna("")
    numeric = [
        "average_daily_count", "days_seen", "feed_days", "seen_ratio_pct",
        "first_five_day_average", "last_five_day_average",
        "unique_title_count", "unique_company_count", "unique_location_count",
        "top_1_company_share_pct", "top_2_company_share_pct",
    ]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    valid_region = ~df["region"].str.strip().str.lower().isin(
        {"unknown", "other / unknown"}
    )
    df = df[
        df["region_scope"].isin(["lookup_region", "published_aggregate"])
        & valid_region
    ].copy()

    build_ready = (
        df["recommendation"].eq("BUILD")
        & df["last_five_day_average"].ge(3.0)
        & df["unique_company_count"].ge(3)
        & df["unique_location_count"].ge(3)
        & df["concentration_risk"].ne("HIGH")
    )
    stable_watch = (
        df["recommendation"].eq("WATCH")
        & df["average_daily_count"].ge(4.5)
        & df["seen_ratio_pct"].ge(80.0)
        & df["last_five_day_average"].ge(4.0)
        & df["unique_title_count"].ge(5)
        & df["unique_company_count"].ge(3)
        & df["unique_location_count"].ge(3)
        & df["concentration_risk"].ne("HIGH")
    )
    exploratory_pilot_watch = (
        df["recommendation"].eq("WATCH")
        & df["average_daily_count"].ge(3.0)
        & df["seen_ratio_pct"].ge(80.0)
        & df["last_five_day_average"].ge(2.5)
        & df["unique_company_count"].ge(3)
        & df["unique_location_count"].ge(3)
        & df["concentration_risk"].ne("HIGH")
    )

    df["credible_slice"] = build_ready | stable_watch
    df["manual_review_pilot"] = build_ready | stable_watch | exploratory_pilot_watch
    df["pilot_basis"] = ""
    df.loc[build_ready, "pilot_basis"] = "Module 2 BUILD with recent volume and acceptable breadth/concentration"
    df.loc[stable_watch, "pilot_basis"] = "Strong persistent WATCH just below the BUILD volume threshold"
    df.loc[exploratory_pilot_watch & ~stable_watch, "pilot_basis"] = "Exploratory WATCH with enough persistence and recent supply for manual review"

    shortlist = df[df["recommendation"].isin(["BUILD", "WATCH"])].sort_values(
        ["credible_slice", "manual_review_pilot", "recommendation", "average_daily_count", "last_five_day_average"],
        ascending=[False, False, True, False, False],
    )
    shortlist.to_csv(shortlist_path, index=False, encoding="utf-8-sig")

    category_rows = []
    for category in EXPECTED_CATEGORIES:
        group = df[df["category"] == category]
        builds = group[group["recommendation"] == "BUILD"]
        watches = group[group["recommendation"] == "WATCH"]
        credible = group[group["credible_slice"]]
        pilots = group[group["manual_review_pilot"]]
        top = group.sort_values("average_daily_count", ascending=False).head(1)
        top_region = top.iloc[0]["region"] if not top.empty else "—"
        top_avg = float(top.iloc[0]["average_daily_count"]) if not top.empty else 0.0

        if not builds.empty and not credible.empty:
            decision = "BUILD_CANDIDATE"
            decision_reason = "At least one Module 2 BUILD remains credible after recent-volume and concentration safeguards."
        elif not credible.empty:
            decision = "PILOT_CANDIDATE"
            decision_reason = "A persistent WATCH is close enough to BUILD for a manual-review pilot."
        elif not pilots.empty:
            decision = "PILOT_CANDIDATE"
            decision_reason = "No BUILD, but one WATCH has enough recent supply and breadth for a limited manual-review pilot."
        else:
            decision = "REJECT_FOR_NOW"
            if group.empty:
                decision_reason = "No selected July titles produced any region-level evidence."
            elif group["concentration_risk"].eq("HIGH").all():
                decision_reason = "Available supply is too concentrated to support a credible slice."
            elif top_avg < 3.0:
                decision_reason = "No region reaches the 3 jobs/day WATCH floor."
            else:
                decision_reason = "No region combines persistence, recent supply, breadth and acceptable concentration."

        category_rows.append({
            "category": category,
            "builds": len(builds),
            "watches": len(watches),
            "credible": len(credible),
            "pilots": len(pilots),
            "top_region": top_region,
            "top_avg": top_avg,
            "decision": decision,
            "decision_reason": decision_reason,
        })

    credible_df = df[df["credible_slice"]].sort_values(
        ["average_daily_count", "last_five_day_average"], ascending=False
    )
    pilot_df = df[df["manual_review_pilot"]].sort_values(
        ["credible_slice", "average_daily_count", "last_five_day_average"],
        ascending=[False, False, False],
    )

    lines = [
        "# July 2026 exploratory category discovery",
        "",
        f"Credible new region × category slices: **{len(credible_df)}**",
        f"At least six credible slices exist: **{'YES' if len(credible_df) >= 6 else 'NO'}**",
        f"Slices suitable for a limited manual-review pilot: **{len(pilot_df)}**",
        "",
        "## Candidate-family assessment",
        "",
        "| Category | BUILD | WATCH | Credible | Pilot | Strongest region | Top avg/day | Decision | Why |",
        "|---|---:|---:|---:|---:|---|---:|---|---|",
    ]
    for row in sorted(
        category_rows,
        key=lambda item: (-item["credible"], -item["pilots"], -item["builds"], -item["top_avg"], item["category"]),
    ):
        lines.append(
            f"| {row['category']} | {row['builds']} | {row['watches']} | {row['credible']} | "
            f"{row['pilots']} | {row['top_region']} | {row['top_avg']:.2f} | "
            f"{row['decision']} | {row['decision_reason']} |"
        )

    lines += ["", "## Strongest credible slices", ""]
    if credible_df.empty:
        lines.append("None met the credible-slice safeguard.")
    else:
        lines.append(
            "| Region | Category | Status | Avg/day | Days present | First 5 | Last 5 | Companies | Locations | Concentration | Why |"
        )
        lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|---|---|")
        for _, row in credible_df.head(30).iterrows():
            reason = str(row["pilot_basis"]).replace("|", "/")
            lines.append(
                f"| {row['region']} | {row['category']} | {row['recommendation']} | "
                f"{row['average_daily_count']:.2f} | {int(row['days_seen'])}/{int(row['feed_days'])} | "
                f"{row['first_five_day_average']:.2f} | {row['last_five_day_average']:.2f} | "
                f"{int(row['unique_company_count'])} | {int(row['unique_location_count'])} | "
                f"{row['concentration_risk']} | {reason} |"
            )

    lines += ["", "## Manual-review pilot candidates", ""]
    if pilot_df.empty:
        lines.append("None met the pilot safeguard.")
    else:
        for _, row in pilot_df.head(20).iterrows():
            lines.append(
                f"- {row['region']} × {row['category']} — {row['recommendation']}; "
                f"{row['average_daily_count']:.2f}/day; last five days {row['last_five_day_average']:.2f}; "
                f"{int(row['unique_company_count'])} advertisers; {row['pilot_basis']}."
            )

    rejected = [
        row["category"] for row in category_rows if row["decision"] == "REJECT_FOR_NOW"
    ]
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

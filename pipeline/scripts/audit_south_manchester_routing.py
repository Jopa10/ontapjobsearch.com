#!/usr/bin/env python3
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[2]
ARCHIVE_DIR = BASE / "pipeline" / "input-jobg8-archive" / "2026-08"
GEO_PATH = BASE / "pipeline" / "geo" / "geo_lookup.xlsx"
REGISTER_PATH = BASE / "pipeline" / "registers" / "admin_service_title_classification_register.csv"
OUT_DIR = BASE / "pipeline" / "reports-audit"
OUT_CSV = OUT_DIR / "south-manchester-routing-audit.csv"
OUT_MD = OUT_DIR / "south-manchester-routing-audit.md"

COL_JOB_ID = "/Job/DisplayReference"
COL_TITLE = "/Job/Position"
COL_COMPANY = "/Job/AdvertiserName"
COL_AREA = "/Job/Area"
COL_LOCATION = "/Job/Location"
COL_DESCRIPTION = "/Job/Description"

TARGET = "Greater Manchester - South"
CURRENT_BUCKET = "Greater Manchester - Manchester & Salford"
SELECTED = {"HIGH_CONFIDENCE", "ELASTIC_FIT"}
AREA_UNUSABLE = {"", "not specified", "unknown", "city"}


def norm(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def key(value: object) -> str:
    return norm(value).lower()


def load_geo() -> tuple[dict[str, str], dict[str, str], list[str]]:
    area_df = pd.read_excel(GEO_PATH, dtype=str).fillna("")
    area_lookup = {
        key(row["Area"]): norm(row["Cluster"])
        for _, row in area_df.iterrows()
        if key(row.get("Area")) and norm(row.get("Cluster"))
    }

    fallback_df = pd.read_excel(GEO_PATH, sheet_name="LocationFallback", dtype=str).fillna("")
    fallback_lookup = {
        key(row["Location"]): norm(row["Cluster"])
        for _, row in fallback_df.iterrows()
        if key(row.get("Status")) == "auto" and key(row.get("Location")) and norm(row.get("Cluster"))
    }

    south_names = sorted(
        {
            key(row["Area"])
            for _, row in area_df.iterrows()
            if norm(row.get("Cluster")) == TARGET and len(key(row.get("Area"))) >= 5
        }
        | {
            key(row["Location"])
            for _, row in fallback_df.iterrows()
            if key(row.get("Status")) == "auto"
            and norm(row.get("Cluster")) == TARGET
            and len(key(row.get("Location"))) >= 5
        },
        key=len,
        reverse=True,
    )
    return area_lookup, fallback_lookup, south_names


def load_register() -> dict[str, str]:
    df = pd.read_csv(REGISTER_PATH, dtype=str).fillna("")
    return {key(row["title"]): norm(row["classification"]).upper() for _, row in df.iterrows()}


def current_region(row: pd.Series, area_lookup: dict[str, str], fallback_lookup: dict[str, str]) -> str:
    area = key(row.get(COL_AREA))
    location = key(row.get(COL_LOCATION))
    if area in AREA_UNUSABLE:
        return fallback_lookup.get(location, "Other / Unknown")
    return area_lookup.get(area, "Other / Unknown")


def evidence_for_south(row: pd.Series, south_names: list[str]) -> str:
    location = key(row.get(COL_LOCATION))
    description = key(row.get(COL_DESCRIPTION))[:900]

    if "south manchester" in location:
        return "location says South Manchester"
    if re.search(r"\b(?:location\s*[:\-]?\s*|based\s+(?:in|at)\s+|office\s+(?:in|at)\s+)south manchester\b", description):
        return "description says South Manchester"

    for place in south_names:
        escaped = re.escape(place)
        if location == place:
            return f"structured location says {place}"
        patterns = [
            rf"\blocation\s*[:\-]?\s*{escaped}\b",
            rf"\bbased\s+(?:in|at|near)\s+{escaped}\b",
            rf"\boffice\s+(?:in|at|near)\s+{escaped}\b",
            rf"\b{escaped}[\s-]+based\b",
            rf"\b{escaped}\s+office\b",
            rf"\b{escaped}\s+area\b",
        ]
        if any(re.search(pattern, description) for pattern in patterns):
            return f"description strongly locates role in {place}"
    return ""


def main() -> None:
    area_lookup, fallback_lookup, south_names = load_geo()
    register = load_register()
    files = sorted(ARCHIVE_DIR.glob("2026-08-*.xlsx"))
    if not files:
        raise SystemExit(f"No archive files found in {ARCHIVE_DIR}")

    rows: list[dict[str, object]] = []
    daily: list[dict[str, object]] = []

    for path in files:
        date = path.stem
        df = pd.read_excel(path, dtype=str).fillna("")
        selected = df[df[COL_TITLE].map(lambda value: register.get(key(value), "") in SELECTED)].copy()
        selected["current_region"] = selected.apply(
            lambda row: current_region(row, area_lookup, fallback_lookup), axis=1
        )

        south = selected[selected["current_region"] == TARGET]
        manchester = selected[selected["current_region"] == CURRENT_BUCKET].copy()
        manchester["south_evidence"] = manchester.apply(
            lambda row: evidence_for_south(row, south_names), axis=1
        )
        moved = manchester[manchester["south_evidence"] != ""]

        daily.append(
            {
                "date": date,
                "south_current": len(south),
                "south_misrouted_from_manchester_salford": len(moved),
                "south_adjusted": len(south) + len(moved),
                "manchester_salford_current": len(manchester),
                "manchester_salford_adjusted": len(manchester) - len(moved),
            }
        )

        for _, row in moved.iterrows():
            rows.append(
                {
                    "date": date,
                    "job_id": norm(row.get(COL_JOB_ID)),
                    "title": norm(row.get(COL_TITLE)),
                    "company": norm(row.get(COL_COMPANY)),
                    "raw_area": norm(row.get(COL_AREA)),
                    "raw_location": norm(row.get(COL_LOCATION)),
                    "evidence": norm(row.get("south_evidence")),
                    "description_head": norm(row.get(COL_DESCRIPTION))[:320],
                }
            )

    daily_df = pd.DataFrame(daily)
    moved_df = pd.DataFrame(rows)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    moved_df.to_csv(OUT_CSV, index=False)

    current_avg = daily_df["south_current"].mean()
    adjusted_avg = daily_df["south_adjusted"].mean()
    current_6 = int((daily_df["south_current"] >= 6).sum())
    adjusted_6 = int((daily_df["south_adjusted"] >= 6).sum())
    unique_jobs = moved_df.drop_duplicates("job_id") if not moved_df.empty else moved_df

    title_counts = Counter(unique_jobs["title"]) if not unique_jobs.empty else Counter()
    company_counts = Counter(unique_jobs["company"]) if not unique_jobs.empty else Counter()

    lines = [
        "# South Manchester routing audit",
        "",
        f"Archive days assessed: **{len(daily_df)}**",
        f"Current South Manchester average: **{current_avg:.2f} jobs/day**",
        f"Adjusted South Manchester average after strong-evidence reroutes: **{adjusted_avg:.2f} jobs/day**",
        f"Days at 6+ jobs: **{current_6} current -> {adjusted_6} adjusted**",
        f"Unique misrouted admin/service jobs found: **{len(unique_jobs)}**",
        "",
        "## Daily counts",
        "",
        "| Date | South current | Strong-evidence reroutes | South adjusted | Manchester/Salford current | Manchester/Salford adjusted |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for _, row in daily_df.iterrows():
        lines.append(
            f"| {row['date']} | {int(row['south_current'])} | {int(row['south_misrouted_from_manchester_salford'])} | "
            f"{int(row['south_adjusted'])} | {int(row['manchester_salford_current'])} | {int(row['manchester_salford_adjusted'])} |"
        )

    lines += ["", "## Unique strong-evidence misroutes", ""]
    if unique_jobs.empty:
        lines.append("None found.")
    else:
        lines += [
            "| Job ID | Title | Company | Raw area | Raw location | Evidence |",
            "|---|---|---|---|---|---|",
        ]
        for _, row in unique_jobs.sort_values(["title", "company"]).iterrows():
            safe = {k: str(v).replace("|", "/") for k, v in row.items()}
            lines.append(
                f"| {safe['job_id']} | {safe['title']} | {safe['company']} | {safe['raw_area']} | "
                f"{safe['raw_location']} | {safe['evidence']} |"
            )

    lines += ["", "## Concentration check", ""]
    lines.append("Top rerouted titles: " + ("; ".join(f"{k} ({v})" for k, v in title_counts.most_common(10)) or "—"))
    lines.append("Top rerouted companies: " + ("; ".join(f"{k} ({v})" for k, v in company_counts.most_common(10)) or "—"))
    lines += [
        "",
        "## Method",
        "",
        "Only jobs already classified HIGH_CONFIDENCE or ELASTIC_FIT in the current admin/service register are assessed. "
        "A Manchester & Salford job is proposed for South Manchester only when its structured location, or a strong early-description location phrase, points to an area that the authoritative geo lookup already maps to Greater Manchester - South. This is intentionally conservative and does not infer from recruiter branch addresses or generic mentions.",
    ]

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(OUT_MD.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()

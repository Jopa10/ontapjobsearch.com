from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

from . import service_admin_pipeline as service_admin

INPUT_PATH = Path("input/jobg8.xlsx")
OUT_DIR = Path("reports-audit")
OUT_CSV = OUT_DIR / "live-service-admin-structured-geo-branch.csv"
OUT_MD = OUT_DIR / "live-service-admin-structured-geo-branch.md"

TARGET_TITLE_CLASSES = {"HIGH_CONFIDENCE", "ELASTIC_FIT"}
MANCHESTER_SALFORD = "Greater Manchester - Manchester & Salford"
MANCHESTER_SOUTH = "Greater Manchester - South"


def norm(value: Any) -> str:
    return service_admin.norm(value)


def key(value: Any) -> str:
    return service_admin.norm_key(value)


def old_region(
    row: pd.Series,
    area_lookup: dict[str, str],
    location_lookup: dict[str, str],
) -> tuple[str, str]:
    """Mirror the pre-fix Area-first routing for comparison."""
    area = norm(row.get(service_admin.COL["area"]))
    location = norm(row.get(service_admin.COL["location"]))
    if service_admin.area_is_unusable(area):
        return location_lookup.get(key(location), ""), "location_fallback"
    return area_lookup.get(key(area), ""), "area"


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    if not rows:
        return ["_None._"]
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join(["---"] * len(headers)) + "|",
    ]
    for row in rows:
        safe = [str(value).replace("|", "/").replace("\n", " ") for value in row]
        lines.append("| " + " | ".join(safe) + " |")
    return lines


def main() -> int:
    if not INPUT_PATH.exists():
        raise SystemExit(f"STOP: missing current JobG8 input: {INPUT_PATH}")

    df = service_admin.read_table(INPUT_PATH).fillna("")
    service_admin.validate_job_columns(df)
    postal_col = service_admin.POSTAL_CODE_COLUMN
    if postal_col not in df.columns:
        raise SystemExit(
            f"STOP: current JobG8 feed does not contain required structured postcode column {postal_col}"
        )

    lookup_path = service_admin.find_lookup_file(INPUT_PATH)
    area_lookup, location_lookup = service_admin.build_complete_geo_lookups(lookup_path)
    postcode_overrides = service_admin._geo.load_postcode_overrides()
    title_register = service_admin.load_title_register()

    records: list[dict[str, Any]] = []
    source_counts: Counter[str] = Counter()
    move_counts: Counter[tuple[str, str]] = Counter()
    old_ms_postcodes: Counter[str] = Counter()
    unmapped_ms_postcodes: Counter[str] = Counter()

    for _, row in df.iterrows():
        title = norm(row.get(service_admin.COL["title"]))
        classification, _, _, _ = service_admin.classify_title(title, title_register)
        if classification not in TARGET_TITLE_CLASSES:
            continue

        previous_region, previous_source = old_region(row, area_lookup, location_lookup)
        resolution = service_admin.resolve_job_geography(
            row,
            area_lookup,
            location_lookup,
            postcode_overrides,
        )
        source_counts[resolution.source] += 1
        if previous_region and resolution.region and previous_region != resolution.region:
            move_counts[(previous_region, resolution.region)] += 1

        raw_postcode = norm(row.get(postal_col))
        district = service_admin.normalize_postcode_district(raw_postcode)
        if previous_region == MANCHESTER_SALFORD and district:
            old_ms_postcodes[district] += 1
            if district not in postcode_overrides:
                unmapped_ms_postcodes[district] += 1

        records.append(
            {
                "job_id": norm(row.get(service_admin.COL["job_id"])),
                "title": title,
                "title_classification": classification,
                "raw_area": norm(row.get(service_admin.COL["area"])),
                "raw_location": norm(row.get(service_admin.COL["location"])),
                "raw_postcode": raw_postcode,
                "postcode_district": district,
                "old_region": previous_region,
                "old_geo_source": previous_source,
                "new_region": resolution.region,
                "new_town": resolution.town,
                "new_geo_source": resolution.source,
                "new_geo_evidence": resolution.evidence,
                "description_head": service_admin.make_description_preview(
                    row.get(service_admin.COL["description"]), max_chars=240
                ),
            }
        )

    result_df = pd.DataFrame(records)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(OUT_CSV, index=False)

    selected_title_rows = len(result_df)
    nonblank_postcodes = int((result_df["raw_postcode"].astype(str).str.strip() != "").sum()) if not result_df.empty else 0
    mapped_postcodes = int((result_df["new_geo_source"] == "structured_postcode").sum()) if not result_df.empty else 0
    changed = result_df[
        (result_df["old_region"] != "")
        & (result_df["new_region"] != "")
        & (result_df["old_region"] != result_df["new_region"])
    ] if not result_df.empty else result_df
    ms_to_south = changed[
        (changed["old_region"] == MANCHESTER_SALFORD)
        & (changed["new_region"] == MANCHESTER_SOUTH)
    ] if not changed.empty else changed

    lines = [
        "# Live Service Admin structured geography branch audit",
        "",
        f"Feed rows: **{len(df)}**",
        f"Admin/Service title-candidate rows assessed: **{selected_title_rows}**",
        f"Rows with structured /Job/PostalCode: **{nonblank_postcodes}**",
        f"Rows currently resolved by mapped structured postcode: **{mapped_postcodes}**",
        f"Rows whose regional allocation changes versus old Area-first logic: **{len(changed)}**",
        f"Manchester & Salford -> Greater Manchester - South changes: **{len(ms_to_south)}**",
        "",
        "## New resolver source counts",
        "",
    ]
    lines += markdown_table(
        ["Source", "Count"],
        [[source, count] for source, count in source_counts.most_common()],
    )

    lines += ["", "## Region moves", ""]
    lines += markdown_table(
        ["Old region", "New region", "Count"],
        [[old, new, count] for (old, new), count in move_counts.most_common()],
    )

    lines += ["", "## Manchester & Salford -> South Manchester detail", ""]
    detail_rows: list[list[Any]] = []
    if not ms_to_south.empty:
        for _, row in ms_to_south.sort_values(["new_geo_source", "title"]).iterrows():
            detail_rows.append(
                [
                    row["job_id"],
                    row["title"],
                    row["raw_area"],
                    row["raw_location"],
                    row["raw_postcode"],
                    row["new_town"],
                    row["new_geo_source"],
                ]
            )
    lines += markdown_table(
        ["Job ID", "Title", "Area", "Location", "PostalCode", "Resolved town", "Source"],
        detail_rows,
    )

    lines += ["", "## Postcode districts in jobs old logic sends to Manchester & Salford", ""]
    lines += markdown_table(
        ["District", "Rows", "Mapped by branch?"],
        [
            [district, count, "yes" if district in postcode_overrides else "no"]
            for district, count in old_ms_postcodes.most_common()
        ],
    )

    lines += ["", "## Unmapped postcode districts in old Manchester & Salford candidate rows", ""]
    lines += markdown_table(
        ["District", "Rows"],
        [[district, count] for district, count in unmapped_ms_postcodes.most_common()],
    )

    lines += [
        "",
        "## Safety notes",
        "",
        "- This audit does not publish anything.",
        "- Postcode routing only occurs for postcode districts explicitly present in the curated postcode-region register.",
        "- Location can override Area only when Area is absent/invalid or an explicitly broad umbrella value; a county Location cannot casually overrule a specific city Area.",
        "- A resolved non-LIVE region is deliberately not pushed into a neighbouring LIVE output.",
    ]

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(OUT_MD.read_text(encoding="utf-8"))
    print(f"CSV: {OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

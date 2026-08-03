from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"Expected exactly one {label}; found {text.count(old)}")
    return text.replace(old, new, 1)


module = Path("pipeline/scripts/jobg8_module_2_monthly_category_profiler.py")
text = module.read_text(encoding="utf-8")

text = replace_once(
    text,
    "- geo_lookup.xlsx with columns: Area, Cluster.\n",
    "- geo_lookup.xlsx with Area/Cluster plus the controlled LocationFallback sheet.\n",
    "Module 2 geo input description",
)
text = replace_once(
    text,
    'COL_LOCATION = "/Job/Location"\n',
    'COL_LOCATION = "/Job/Location"\nAREA_UNUSABLE_VALUES = {"", "not specified", "unknown"}\n',
    "Module 2 location constant",
)

old_geo = '''def load_geo_lookup(path: Path) -> Dict[str, str]:
    df = pd.read_excel(path, dtype=str).fillna("")
    required = {"Area", "Cluster"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Geo lookup missing columns: {sorted(missing)}")

    lookup: Dict[str, str] = {}
    for _, row in df.iterrows():
        area = norm_key(row["Area"])
        cluster = norm_text(row["Cluster"])
        if area and cluster:
            lookup[area] = cluster

    if not lookup:
        raise ValueError("Geo lookup contains no usable Area → Cluster mappings.")
    return lookup
'''
new_geo = '''def load_geo_lookups(path: Path) -> tuple[Dict[str, str], Dict[str, str]]:
    area_df = pd.read_excel(path, dtype=str).fillna("")
    required = {"Area", "Cluster"}
    missing = required.difference(area_df.columns)
    if missing:
        raise ValueError(f"Geo lookup missing columns: {sorted(missing)}")

    area_lookup: Dict[str, str] = {}
    for _, row in area_df.iterrows():
        area = norm_key(row["Area"])
        cluster = norm_text(row["Cluster"])
        if area and cluster:
            area_lookup[area] = cluster

    if not area_lookup:
        raise ValueError("Geo lookup contains no usable Area → Cluster mappings.")

    try:
        fallback_df = pd.read_excel(
            path,
            sheet_name="LocationFallback",
            dtype=str,
        ).fillna("")
    except ValueError as exc:
        raise ValueError(
            "Geo lookup is missing the required LocationFallback sheet."
        ) from exc

    fallback_required = {"Status", "Location", "Cluster"}
    fallback_missing = fallback_required.difference(fallback_df.columns)
    if fallback_missing:
        raise ValueError(
            "LocationFallback missing columns: " + str(sorted(fallback_missing))
        )

    location_fallback_lookup: Dict[str, str] = {}
    for _, row in fallback_df.iterrows():
        if norm_key(row["Status"]) != "auto":
            continue
        location = norm_key(row["Location"])
        cluster = norm_text(row["Cluster"])
        if location and cluster:
            location_fallback_lookup[location] = cluster

    return area_lookup, location_fallback_lookup


def area_is_unusable(area: object) -> bool:
    return norm_key(area) in AREA_UNUSABLE_VALUES
'''
text = replace_once(text, old_geo, new_geo, "Module 2 geo loader")

text = replace_once(
    text,
    '''def load_daily_feeds(
    input_dir: Path,
    geo_lookup: Dict[str, str],
    registers: Dict[str, Dict[str, str]],
) -> tuple[pd.DataFrame, List[str], List[str]]:
''',
    '''def load_daily_feeds(
    input_dir: Path,
    geo_lookup: Dict[str, str],
    location_fallback_lookup: Dict[str, str],
    registers: Dict[str, Dict[str, str]],
) -> tuple[pd.DataFrame, List[str], List[str]]:
''',
    "Module 2 feed-loader signature",
)
text = replace_once(
    text,
    "    required_cols = {COL_TITLE, COL_COMPANY, COL_AREA}\n",
    "    required_cols = {COL_TITLE, COL_COMPANY, COL_AREA, COL_LOCATION}\n",
    "Module 2 required feed columns",
)

old_mapping = '''            area_key = norm_key(area)
            region = geo_lookup.get(area_key, "Other / Unknown")
            if region == "Other / Unknown":
                unknown_reason = (
                    "blank_or_missing_area"
                    if not area_key
                    else "area_not_found_in_geo_lookup"
                )
            else:
                unknown_reason = ""
'''
new_mapping = '''            area_key = norm_key(area)
            location_key = norm_key(raw_location)
            if area_is_unusable(area):
                region = location_fallback_lookup.get(
                    location_key,
                    "Other / Unknown",
                )
                report_location = raw_location
                geo_source = (
                    "location_fallback"
                    if region != "Other / Unknown"
                    else "unknown"
                )
                if region == "Other / Unknown":
                    unknown_reason = (
                        "area_unusable_and_blank_location"
                        if not location_key
                        else "area_unusable_and_location_not_auto_fallback"
                    )
                else:
                    unknown_reason = ""
            else:
                region = geo_lookup.get(area_key, "Other / Unknown")
                report_location = area
                geo_source = "area" if region != "Other / Unknown" else "unknown"
                unknown_reason = (
                    "area_not_found_in_geo_lookup"
                    if region == "Other / Unknown"
                    else ""
                )
'''
text = replace_once(text, old_mapping, new_mapping, "Module 2 area-only mapping")

text = replace_once(
    text,
    '''                    "location": area,
                    "raw_location": raw_location,
                    "lookup_region": region,
                    "unknown_reason": unknown_reason,
''',
    '''                    "location": report_location,
                    "raw_area": area,
                    "raw_location": raw_location,
                    "lookup_region": region,
                    "geo_source": geo_source,
                    "unknown_reason": unknown_reason,
''',
    "Module 2 expanded geo fields",
)
text = replace_once(
    text,
    "    geo_lookup = load_geo_lookup(geo_lookup_path)\n",
    "    geo_lookup, location_fallback_lookup = load_geo_lookups(geo_lookup_path)\n",
    "Module 2 run geo loader",
)
text = replace_once(
    text,
    '''        input_dir=input_dir,
        geo_lookup=geo_lookup,
        registers=registers,
''',
    '''        input_dir=input_dir,
        geo_lookup=geo_lookup,
        location_fallback_lookup=location_fallback_lookup,
        registers=registers,
''',
    "Module 2 run feed-loader call",
)

old_unknown = '''            "location",
            "raw_location",
            "category",
            "source_file",
            "unknown_reason",
        ],
    ].copy()
    unknown_detail = unknown_detail.rename(columns={"location": "raw_area"})
'''
new_unknown = '''            "raw_area",
            "raw_location",
            "geo_source",
            "category",
            "source_file",
            "unknown_reason",
        ],
    ].copy()
'''
text = replace_once(text, old_unknown, new_unknown, "Module 2 unknown-detail columns")
text = replace_once(
    text,
    '        f"Geo areas loaded: {len(geo_lookup)}",\n',
    '        f"Geo areas loaded: {len(geo_lookup)}",\n'
    '        f"AUTO location fallbacks loaded: {len(location_fallback_lookup)}",\n'
    '        f"Rows assigned by location fallback: "\n'
    '        f"{int(expanded[\'geo_source\'].eq(\'location_fallback\').sum())}",\n',
    "Module 2 geo log lines",
)
module.write_text(text, encoding="utf-8")

workflow = Path(".github/workflows/run-compiler-module-2.yml")
wf = workflow.read_text(encoding="utf-8")
old_validation = '''          geo_df = pd.read_excel(geo_lookup_path)
          missing_geo_columns = sorted(required_geo_columns - set(geo_df.columns))
          if missing_geo_columns:
              raise SystemExit(
                  f"::error::{geo_lookup_path} is missing required column(s): "
                  + ", ".join(missing_geo_columns)
              )

          usable_geo_rows = geo_df[["Area", "Cluster"]].dropna(how="any")
'''
new_validation = '''          geo_df = pd.read_excel(geo_lookup_path)
          missing_geo_columns = sorted(required_geo_columns - set(geo_df.columns))
          if missing_geo_columns:
              raise SystemExit(
                  f"::error::{geo_lookup_path} is missing required column(s): "
                  + ", ".join(missing_geo_columns)
              )

          try:
              fallback_df = pd.read_excel(
                  geo_lookup_path,
                  sheet_name="LocationFallback",
                  dtype=str,
              ).fillna("")
          except ValueError as exc:
              raise SystemExit(
                  f"::error::{geo_lookup_path} is missing the LocationFallback sheet"
              ) from exc
          required_fallback_columns = {"Status", "Location", "Cluster"}
          missing_fallback_columns = sorted(
              required_fallback_columns - set(fallback_df.columns)
          )
          if missing_fallback_columns:
              raise SystemExit(
                  f"::error::{geo_lookup_path} LocationFallback is missing required column(s): "
                  + ", ".join(missing_fallback_columns)
              )

          usable_geo_rows = geo_df[["Area", "Cluster"]].dropna(how="any")
'''
wf = replace_once(wf, old_validation, new_validation, "Module 2 workflow geo validation")
workflow.write_text(wf, encoding="utf-8")

Path("tests/test_module2_location_fallback.py").write_text(
    '''from pathlib import Path

import pandas as pd

from pipeline.scripts.jobg8_module_2_monthly_category_profiler import (
    load_daily_feeds,
    load_geo_lookups,
)


def test_location_fallback_is_auto_only(tmp_path: Path) -> None:
    geo_path = tmp_path / "geo.xlsx"
    with pd.ExcelWriter(geo_path) as writer:
        pd.DataFrame([{"Area": "Solihull", "Cluster": "Birmingham"}]).to_excel(
            writer, index=False
        )
        pd.DataFrame([
            {"Status": "AUTO", "Location": "Birmingham", "Cluster": "Birmingham"},
            {"Status": "REVIEW", "Location": "Coventry", "Cluster": "Coventry"},
        ]).to_excel(writer, sheet_name="LocationFallback", index=False)

    area_lookup, fallback_lookup = load_geo_lookups(geo_path)
    assert area_lookup == {"solihull": "Birmingham"}
    assert fallback_lookup == {"birmingham": "Birmingham"}


def test_daily_feed_uses_area_then_controlled_location_fallback(tmp_path: Path) -> None:
    input_dir = tmp_path / "feeds"
    input_dir.mkdir()
    pd.DataFrame([
        {
            "/Job/DisplayReference": "1",
            "/Job/Position": "Administrator",
            "/Job/AdvertiserName": "A",
            "/Job/Area": "Solihull",
            "/Job/Location": "Wrong fallback",
        },
        {
            "/Job/DisplayReference": "2",
            "/Job/Position": "Administrator",
            "/Job/AdvertiserName": "B",
            "/Job/Area": "Not Specified",
            "/Job/Location": "Birmingham",
        },
        {
            "/Job/DisplayReference": "3",
            "/Job/Position": "Administrator",
            "/Job/AdvertiserName": "C",
            "/Job/Area": "Not Specified",
            "/Job/Location": "Coventry",
        },
    ]).to_excel(input_dir / "jobg8-2026-07-01.xlsx", index=False)

    expanded, dates, errors = load_daily_feeds(
        input_dir=input_dir,
        geo_lookup={"solihull": "Birmingham cluster"},
        location_fallback_lookup={"birmingham": "Birmingham cluster"},
        registers={"admin_service": {"administrator": "HIGH_CONFIDENCE"}},
    )

    assert dates == ["2026-07-01"]
    assert errors == []
    rows = expanded.set_index("job_id")
    assert rows.loc["1", "lookup_region"] == "Birmingham cluster"
    assert rows.loc["1", "geo_source"] == "area"
    assert rows.loc["1", "location"] == "Solihull"
    assert rows.loc["2", "lookup_region"] == "Birmingham cluster"
    assert rows.loc["2", "geo_source"] == "location_fallback"
    assert rows.loc["2", "location"] == "Birmingham"
    assert rows.loc["3", "lookup_region"] == "Other / Unknown"
    assert rows.loc["3", "unknown_reason"] == "area_unusable_and_location_not_auto_fallback"
''',
    encoding="utf-8",
)

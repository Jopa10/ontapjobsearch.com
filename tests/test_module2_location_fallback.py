from pathlib import Path

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

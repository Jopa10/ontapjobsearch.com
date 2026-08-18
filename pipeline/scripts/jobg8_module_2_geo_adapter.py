from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

try:
    from . import jobg8_geo_resolver as _geo
except ImportError:  # direct script/test loading
    import jobg8_geo_resolver as _geo


COL_DESCRIPTION = "/Job/Description"
COL_POSTAL_CODE = _geo.POSTAL_CODE_COLUMN


def install(compiler: Any) -> None:
    """Replace Module 2's Area-first loader with the shared JobG8 geo resolver.

    Category classification remains untouched. Only geography changes so Module 2
    and the live selector use the same precision order: mapped structured postcode,
    precise structured Location, specific Area, advert postcode/place, broad fallback.
    """

    def module2_area_is_unusable(area: object) -> bool:
        return compiler.area_is_unusable(area) or compiler.norm_key(area) == "city"

    def load_daily_feeds(
        input_dir: Path,
        geo_lookup: dict[str, str],
        location_fallback_lookup: dict[str, str],
        registers: dict[str, dict[str, str]],
    ) -> tuple[pd.DataFrame, list[str], list[str]]:
        files = sorted(
            p for p in input_dir.iterdir()
            if p.suffix.lower() in {".xlsx", ".xls", ".xlsm"}
            and not p.name.startswith("~$")
        )
        if not files:
            raise FileNotFoundError(f"No JobG8 Excel files found in {input_dir}")

        rows: list[dict[str, Any]] = []
        errors: list[str] = []
        valid_dates: list[str] = []
        required_cols = {
            compiler.COL_TITLE,
            compiler.COL_COMPANY,
            compiler.COL_AREA,
            compiler.COL_LOCATION,
        }
        postcode_overrides = _geo.load_postcode_overrides()
        description_place_rules = _geo.description_place_rules_for_lookup(geo_lookup)

        for path in files:
            date = compiler.extract_date(path)
            if not date:
                errors.append(f"{path.name}: date not recognised from filename")
                continue

            try:
                df = pd.read_excel(path, dtype=str).fillna("")
            except Exception as exc:
                errors.append(f"{path.name}: failed to read: {exc}")
                continue

            missing = required_cols.difference(df.columns)
            if missing:
                errors.append(f"{path.name}: missing columns {sorted(missing)}")
                continue

            valid_dates.append(date)

            for index, row in df.iterrows():
                title = compiler.norm_text(row.get(compiler.COL_TITLE))
                title_key = compiler.norm_key(title)
                area = compiler.norm_text(row.get(compiler.COL_AREA))
                raw_location = compiler.norm_text(row.get(compiler.COL_LOCATION))
                raw_postal_code = compiler.norm_text(row.get(COL_POSTAL_CODE))

                resolution = _geo.resolve_job_geography(
                    row,
                    area_column=compiler.COL_AREA,
                    location_column=compiler.COL_LOCATION,
                    description_column=COL_DESCRIPTION,
                    area_lookup=geo_lookup,
                    location_lookup=location_fallback_lookup,
                    postcode_overrides=postcode_overrides,
                    area_is_unusable=module2_area_is_unusable,
                    postal_code_column=COL_POSTAL_CODE,
                    description_place_rules=description_place_rules,
                )
                region = resolution.region or "Other / Unknown"
                report_location = (
                    compiler.norm_text(resolution.town)
                    or raw_location
                    or area
                )
                geo_source = resolution.source if resolution.region else "unknown"
                unknown_reason = "" if resolution.region else (
                    resolution.evidence or "shared_geo_resolver_unresolved"
                )

                company = compiler.norm_text(row.get(compiler.COL_COMPANY)) or "Unknown company"
                job_id = (
                    compiler.norm_text(row.get(compiler.COL_JOB_ID))
                    if compiler.COL_JOB_ID in df.columns
                    else ""
                )
                if not job_id:
                    job_id = f"{path.name}:{index + 2}"

                matched_categories = [
                    category
                    for category, register in registers.items()
                    if register.get(title_key) in compiler.SELECTED_CLASSIFICATIONS
                ]

                for category in matched_categories:
                    rows.append({
                        "date": date,
                        "job_id": job_id,
                        "title": title,
                        "title_key": title_key,
                        "company": company,
                        "location": report_location,
                        "raw_area": area,
                        "raw_location": raw_location,
                        "raw_postal_code": raw_postal_code,
                        "lookup_region": region,
                        "geo_source": geo_source,
                        "geo_evidence": resolution.evidence,
                        "postcode_district": resolution.postcode_district,
                        "unknown_reason": unknown_reason,
                        "category": category,
                        "source_file": path.name,
                    })

        if not rows:
            raise RuntimeError(
                "No jobs matched HIGH_CONFIDENCE or ELASTIC_FIT in the six registers."
            )

        expanded = pd.DataFrame(rows).drop_duplicates(
            subset=["date", "job_id", "category", "lookup_region"]
        )
        return expanded, sorted(set(valid_dates)), errors

    compiler.load_daily_feeds = load_daily_feeds

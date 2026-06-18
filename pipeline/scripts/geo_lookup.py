"""Shared authoritative geography lookup loader for JobG8 publishing pipelines."""
from __future__ import annotations

import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import pandas as pd

GEO_LOOKUP_PATH = Path(__file__).resolve().parents[1] / "geo" / "geo_lookup.xlsx"
GEO_LOOKUP_DISPLAY_PATH = "pipeline/geo/geo_lookup.xlsx"
GEO_LOOKUP_SHEET = "Sheet1"
REQUIRED_COLUMNS = ("Area", "Cluster")


def _norm_key(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip().lower())


def _display(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def _namespace(tag: str) -> str:
    match = re.match(r"\{([^}]+)\}", tag)
    return match.group(1) if match else ""


def _sheet_names(path: Path) -> list[str]:
    try:
        with zipfile.ZipFile(path) as archive:
            workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    except FileNotFoundError:
        raise
    except Exception as exc:  # pragma: no cover - defensive workbook corruption message
        raise SystemExit(f"STOP: could not inspect {GEO_LOOKUP_DISPLAY_PATH}: {exc}") from exc
    ns = _namespace(workbook.tag)
    return [str(sheet.attrib.get("name", "")) for sheet in workbook.findall(f"{{{ns}}}sheets/{{{ns}}}sheet")]


@dataclass(frozen=True)
class GeoLookup:
    area_to_cluster: dict[str, str]
    valid_clusters: frozenset[str]


def load_geo_lookup() -> GeoLookup:
    """Load and validate Sheet1 from the authoritative geography workbook."""
    path = GEO_LOOKUP_PATH
    if not path.exists():
        raise SystemExit(f"STOP: missing authoritative geography workbook: {GEO_LOOKUP_DISPLAY_PATH}")

    names = _sheet_names(path)
    if GEO_LOOKUP_SHEET not in names:
        available = ", ".join(names) if names else "none"
        raise SystemExit(
            f"STOP: {GEO_LOOKUP_DISPLAY_PATH} must contain worksheet {GEO_LOOKUP_SHEET!r}; available worksheets: {available}"
        )

    try:
        df = pd.read_excel(path, sheet_name=GEO_LOOKUP_SHEET, dtype=str).fillna("")
    except TypeError:
        # Local lightweight pandas shim only reads the first worksheet; Sheet1 was verified above.
        df = pd.read_excel(path, dtype=str).fillna("")
    except Exception as exc:
        raise SystemExit(f"STOP: failed to read {GEO_LOOKUP_DISPLAY_PATH} worksheet {GEO_LOOKUP_SHEET!r}: {exc}") from exc

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise SystemExit(
            "STOP: geography lookup worksheet Sheet1 must contain columns named exactly: Area, Cluster; "
            f"missing: {', '.join(missing)}"
        )

    area_to_cluster: dict[str, str] = {}
    display_area: dict[str, str] = {}
    valid_clusters: set[str] = set()
    for idx, row in df.iterrows():
        excel_row = int(idx) + 2
        area = _display(row.get("Area"))
        cluster = _display(row.get("Cluster"))
        if not area:
            raise SystemExit(f"STOP: {GEO_LOOKUP_DISPLAY_PATH} Sheet1 row {excel_row} has a blank Area value")
        if not cluster:
            raise SystemExit(f"STOP: {GEO_LOOKUP_DISPLAY_PATH} Sheet1 row {excel_row} has a blank Cluster value")
        area_key = _norm_key(area)
        previous = area_to_cluster.get(area_key)
        if previous is not None and previous != cluster:
            raise SystemExit(
                "STOP: geography lookup has conflicting Cluster values for Area "
                f"{display_area[area_key]!r}: {previous!r} and {cluster!r}"
            )
        area_to_cluster[area_key] = cluster
        display_area[area_key] = area
        valid_clusters.add(cluster)

    if not area_to_cluster:
        raise SystemExit(f"STOP: {GEO_LOOKUP_DISPLAY_PATH} Sheet1 contains no Area -> Cluster mappings")
    return GeoLookup(area_to_cluster=area_to_cluster, valid_clusters=frozenset(valid_clusters))


def validate_publishing_clusters(configured: dict[str, set[str] | frozenset[str]], valid_clusters: set[str] | frozenset[str]) -> None:
    """Fail if publishing configuration references clusters not present exactly in the workbook."""
    for output_name, clusters in configured.items():
        if not clusters:
            raise SystemExit(f"STOP: publishing output {output_name!r} has no configured workbook clusters")
        missing = sorted(cluster for cluster in clusters if cluster not in valid_clusters)
        if missing:
            valid = "; ".join(sorted(valid_clusters))
            raise SystemExit(
                f"STOP: publishing output {output_name!r} uses unknown or obsolete Cluster value(s): "
                f"{', '.join(missing)}. Configure exact Cluster values from {GEO_LOOKUP_DISPLAY_PATH} Sheet1. "
                f"Valid clusters: {valid}"
            )

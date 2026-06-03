#!/usr/bin/env python3
"""
jobg8_feed_profiler_V2_4.py

Purpose:
    Reads daily JobG8 Excel uploads for a month and produces small CSV summaries
    to help decide which Ontap job slices stay deep enough across the month.

Default expected structure:
    Ontap Pipeline/
      input-jobg8-archive/
        2026-05/
          2026-05-01-jobg8.xlsx
          2026-05-02-jobg8.xlsx
          ...
      output-feed-profiler/

Run from the Ontap Pipeline folder:
    python3 jobg8_feed_profiler_V2_4.py --month 2026-05

Or specify folders directly:
    python3 jobg8_feed_profiler_V2_4.py \
      --input-dir input-jobg8-archive/2026-05 \
      --output-dir output-feed-profiler \
      --month 2026-05

Outputs:
    output-feed-profiler/daily/2026-05-daily-summary.csv
    output-feed-profiler/monthly/2026-05-family-trends.csv
    output-feed-profiler/monthly/2026-05-slice-viability.csv
    output-feed-profiler/title-analysis/2026-05-top-titles.csv
    output-feed-profiler/title-analysis/2026-05-unclassified-titles.csv
    output-feed-profiler/title-analysis/2026-05-title-breadth.csv
    output-feed-profiler/regional/2026-05-family-region-breakdown.csv
    output-feed-profiler/regional/2026-05-regional-location-audit.csv

Optional geography:
    By default, the profiler reads pipeline/geo/lookup.xlsx from the repository
    and uses it to map raw JobG8 locations into Ontap regions. The built-in town
    keyword rules are used only if that lookup file is missing or unreadable.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import pandas as pd


# -----------------------------
# Region configuration
# -----------------------------

REGION_KEYWORDS: Dict[str, List[str]] = {
    "West Yorkshire": [
        "leeds", "bradford", "wakefield", "huddersfield", "halifax",
        "keighley", "pontefract", "castleford", "dewsbury", "batley",
        "morley", "shipley", "otley", "guiseley", "hebden bridge"
    ],
    "South Yorkshire": [
        "sheffield", "rotherham", "doncaster", "barnsley",
        "mexborough", "wath", "penistone", "stocksbridge"
    ],
    "Lancashire": [
        "preston", "blackpool", "burnley", "blackburn", "lancaster",
        "chorley", "accrington", "fleetwood", "leyland", "nelson",
        "morecambe", "skelmersdale"
    ],
    "Greater Manchester": [
        "manchester", "salford", "bolton", "bury", "oldham", "rochdale",
        "stockport", "tameside", "trafford", "wigan", "altrincham",
        "sale", "stretford", "leigh"
    ],
    "Cumbria": [
        "carlisle", "kendal", "barrow", "barrow-in-furness", "workington",
        "whitehaven", "penrith", "ulverston", "keswick", "windermere"
    ],
    "North East": [
        "newcastle", "gateshead", "sunderland", "durham", "darlington",
        "middlesbrough", "stockton", "hartlepool", "northumberland",
        "south shields", "north shields", "tyne", "wear", "tees",
        "washington", "peterlee", "bishop auckland", "ashington", "blyth"
    ],
}

REGION_ORDER = list(REGION_KEYWORDS.keys())

SUPPORT_WORKER_FAMILIES = ["support_worker"]
ADMIN_SERVICE_FAMILIES = ["service_administrator", "administrator_general"]
COMPILER_SUMMARY_COLUMNS = [
    "report_month",
    "run_date",
    "total_jobs_month_to_date",
    "total_support_worker_jobs",
    "total_admin_service_jobs",
    "region",
    "support_worker_count",
    "admin_service_count",
    "strongest_title_families",
    "top_locations",
    "top_companies",
    "slice_status",
    "recommendation",
    "red_flags",
]


# -----------------------------
# Optional geo lookup support
# -----------------------------

CLUSTER_TO_ONTAP_REGION = {
    "yorkshire (west)": "West Yorkshire",
    "west yorkshire": "West Yorkshire",
    "yorkshire west": "West Yorkshire",
    "yorkshire (south)": "South Yorkshire",
    "yorkshire south": "South Yorkshire",
    "south yorkshire": "South Yorkshire",
    "lancashire": "Lancashire",
    "greater manchester": "Greater Manchester",
    "cumbria": "Cumbria",
    "north east": "North East",
    "north east (tyne & wear)": "North East",
    "tyne and wear": "North East",
    "tyne & wear": "North East",
    "northumberland": "North East",
    "county durham": "North East",
    "durham": "North East",
    "tees valley": "North East",
    "tees": "North East",
    "darlington": "North East",
    "hartlepool": "North East",
}


def ontap_region_from_cluster(cluster: object, anchor: object = "") -> Optional[str]:
    cluster_text = normalise_text(cluster)
    anchor_text = normalise_text(anchor)
    combined = f"{cluster_text} {anchor_text}".strip()

    if not combined:
        return None

    if cluster_text in CLUSTER_TO_ONTAP_REGION:
        return CLUSTER_TO_ONTAP_REGION[cluster_text]

    # Broader contains checks for lookup sheets with slightly different labels.
    # Support the user's older geo sheet shorthand, e.g.
    # "4. W Yorkshire", "6. South Yorks", "5 Great Manchester".
    if ("yorkshire" in combined or "yorks" in combined) and ("west" in combined or " w " in f" {combined} " or "w york" in combined):
        return "West Yorkshire"
    if ("yorkshire" in combined or "yorks" in combined) and ("south" in combined or " s " in f" {combined} " or "south york" in combined):
        return "South Yorkshire"
    if anchor_text in ["leeds", "bradford", "wakefield", "huddersfield", "halifax"]:
        return "West Yorkshire"
    if anchor_text in ["sheffield", "rotherham", "doncaster", "barnsley"]:
        return "South Yorkshire"
    if "lancashire" in combined or anchor_text in ["preston", "blackpool", "blackburn", "burnley", "lancaster"]:
        return "Lancashire"
    if "greater manchester" in combined or "great manchester" in combined or combined == "manchester" or anchor_text == "manchester":
        return "Greater Manchester"
    if "cumbria" in combined or anchor_text in ["carlisle", "kendal", "barrow", "workington", "whitehaven"]:
        return "Cumbria"
    if (
        "north east" in combined
        or "tyne" in combined
        or "wear" in combined
        or "northumberland" in combined
        or "durham" in combined
        or "tees" in combined
        or "darlington" in combined
        or "hartlepool" in combined
        or "newcastle" in combined
        or "sunderland" in combined
        or "middlesbrough" in combined
        or "gateshead" in combined
    ):
        return "North East"

    return None


def normalise_lookup_place(value: object) -> str:
    text = normalise_text(value)
    # Keep hyphens because locations such as Barrow-in-Furness and Bradford-on-Avon
    # are meaningful, but collapse spacing around punctuation.
    text = re.sub(r"\s*-\s*", "-", text)
    return text.strip()


def is_broad_ambiguous_location(value: object) -> bool:
    """True when JobG8 location is too broad to assign safely by itself.

    These values should not be forced into a specific Ontap region. Instead, V2_4
    can scan title/description for a stronger town-level clue such as Sheffield or Leeds.
    """
    loc = normalise_lookup_place(value)
    if not loc:
        return True

    broad_exact = {
        "yorkshire", "yorkshire and the humber", "yorkshire humber",
        "north of england", "northern england", "england", "united kingdom",
        "uk", "remote", "home based", "field based", "nationwide",
        "various", "multiple locations", "multiple sites",
    }
    if loc in broad_exact:
        return True

    broad_contains = [
        "yorkshire and humber", "yorkshire & humber", "north of england",
        "northern england", "home based", "field based", "multiple locations",
    ]
    return any(term in loc for term in broad_contains)


class GeoMapper:
    """Maps raw JobG8 location text to Ontap regions using an optional lookup sheet.

    The lookup is deliberately used for region assignment only. Reports still count
    unique original JobG8 location strings separately, so repeated campaigns remain visible.
    """

    def __init__(self, lookup_path: Optional[Path] = None):
        self.place_to_region: Dict[str, str] = {}
        self.lookup_path = lookup_path
        self.lookup_loaded = False
        self.lookup_rows_loaded = 0
        self.lookup_error = ""
        self.fallback_keywords_enabled = True

        if lookup_path:
            if lookup_path.exists():
                self.load_lookup(lookup_path)
            else:
                self.lookup_error = f"lookup file missing: {lookup_path}"

        # The shared workbook is the primary geography source. Built-in keyword
        # rules are only a backup for runs where the workbook could not be read.
        self.fallback_keywords_enabled = not self.lookup_loaded

    def add_place(self, place: object, region: Optional[str]) -> bool:
        place_text = normalise_lookup_place(place)
        if not place_text or not region:
            return False
        if len(place_text) < 3:
            return False
        # Keep the first mapping encountered so the shared lookup workbook remains
        # the single source of truth when duplicate places appear across sheets.
        if place_text in self.place_to_region:
            return False
        self.place_to_region[place_text] = region
        return True

    def load_lookup(self, lookup_path: Path) -> None:
        loaded_rows = 0

        try:
            workbook = pd.ExcelFile(lookup_path) if hasattr(pd, "ExcelFile") else None
            sheet_names = workbook.sheet_names if workbook else [None]
        except Exception as exc:
            self.lookup_error = f"failed opening lookup workbook: {exc}"
            return

        for sheet_name in sheet_names:
            try:
                if sheet_name is None:
                    df = pd.read_excel(lookup_path)
                else:
                    df = pd.read_excel(lookup_path, sheet_name=sheet_name)
            except TypeError:
                # The local lightweight pandas shim only reads the first sheet and
                # does not accept a sheet_name argument. That is enough for the
                # shared lookup workbook's main Area -> Cluster table.
                try:
                    df = pd.read_excel(lookup_path)
                except Exception as exc:
                    self.lookup_error = f"failed reading lookup sheet: {exc}"
                    continue
            except Exception as exc:
                self.lookup_error = f"failed reading lookup sheet: {exc}"
                continue

            # General all-UK lookup block: Area -> Cluster.
            if "Area" in df.columns and "Cluster" in df.columns:
                for _, row in df.iterrows():
                    region = ontap_region_from_cluster(row.get("Cluster"))
                    if self.add_place(row.get("Area"), region):
                        loaded_rows += 1

            # Older/support-worker helper block in the uploaded sheet:
            # Geo = town/place, Unnamed: 1 = subcluster, Unnamed: 2 = anchor city.
            if "Geo" in df.columns:
                cluster_col = "Unnamed: 1" if "Unnamed: 1" in df.columns else None
                anchor_col = "Unnamed: 2" if "Unnamed: 2" in df.columns else None
                for _, row in df.iterrows():
                    cluster = row.get(cluster_col) if cluster_col else ""
                    anchor = row.get(anchor_col) if anchor_col else ""
                    region = ontap_region_from_cluster(cluster, anchor)
                    if self.add_place(row.get("Geo"), region):
                        loaded_rows += 1

        self.lookup_rows_loaded = loaded_rows
        self.lookup_loaded = loaded_rows > 0
        if self.lookup_loaded:
            self.lookup_error = ""
        elif not self.lookup_error:
            self.lookup_error = "no matching geo rows were found in lookup workbook"

    def lookup_match(self, text: object) -> Tuple[Optional[str], str]:
        lookup_text = normalise_lookup_place(text)
        if not lookup_text:
            return None, ""

        # Prefer longest lookup terms first so "south shields" wins before "shields".
        for place, region in sorted(self.place_to_region.items(), key=lambda item: len(item[0]), reverse=True):
            pattern = r"(?<![a-z0-9])" + re.escape(place) + r"(?![a-z0-9])"
            if re.search(pattern, lookup_text):
                return region, place

        return None, ""

    def classify_with_context(self, location: object, title: object = "", description: object = "") -> Tuple[str, str, str]:
        """Classify region, using title/description only for broad ambiguous locations.

        Returns: (region, match_source, match_place)
        """
        loc = normalise_lookup_place(location)

        region, place = self.lookup_match(loc)
        if region:
            return region, "location_lookup", place

        if self.fallback_keywords_enabled:
            keyword_region = classify_region_keywords(loc)
            if keyword_region != "Other / Unknown":
                return keyword_region, "location_keyword", ""

        # Only scan title/description when the original location is broad/ambiguous.
        # This avoids mapping normal out-of-area jobs such as London into Ontap regions
        # just because a company address or national advert mentions Leeds/Sheffield.
        if is_broad_ambiguous_location(loc):
            context = f"{normalise_text(title)} {normalise_text(description)[:1500]}"
            region, place = self.lookup_match(context)
            if region:
                return region, "title_description_lookup", place

            if self.fallback_keywords_enabled:
                context_keyword_region = classify_region_keywords(context)
                if context_keyword_region != "Other / Unknown":
                    return context_keyword_region, "title_description_keyword", ""

        return "Other / Unknown", "unmapped", ""

    def classify(self, location: object) -> str:
        return self.classify_with_context(location)[0]


def find_default_geo_lookup(base_dir: Path) -> Path:
    script_path = Path(__file__).resolve()
    pipeline_dir = script_path.parents[1]
    candidates = [
        pipeline_dir / "geo" / "lookup.xlsx",
        base_dir / "Geo lookup sheet.xlsx",
        base_dir / "geo_lookup.xlsx",
        base_dir / "geo-lookup.xlsx",
        base_dir / "lookup.xlsx",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()

    # Return the intended repository default even when it is missing so the run
    # log can show the exact path checked before falling back to keyword rules.
    return candidates[0].resolve()


def resolve_geo_lookup_arg(geo_lookup: Optional[Path]) -> Path:
    if geo_lookup is None:
        return find_default_geo_lookup(Path.cwd())

    if geo_lookup.is_absolute():
        return geo_lookup.resolve()

    # First honour paths relative to the current working directory. The GitHub
    # Actions job runs from pipeline/, so --geo-lookup geo/lookup.xlsx resolves
    # here.
    cwd_relative = (Path.cwd() / geo_lookup).resolve()
    if cwd_relative.exists():
        return cwd_relative

    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[2]
    repo_relative = (repo_root / geo_lookup).resolve()
    if repo_relative.exists():
        return repo_relative

    pipeline_dir = script_path.parents[1]
    pipeline_relative = (pipeline_dir / geo_lookup).resolve()
    if pipeline_relative.exists():
        return pipeline_relative

    # Return the cwd-relative path for transparent diagnostics if none of the
    # supported locations exists.
    return cwd_relative


# -----------------------------
# Job family rules
# Order matters: more specific before broader.
# -----------------------------

JOB_FAMILY_RULES: List[Tuple[str, List[str], List[str]]] = [
    (
        "support_worker",
        [
            r"\bsupport worker\b", r"\bsenior support worker\b",
            r"\bresidential support worker\b", r"\bfamily support worker\b",
            r"\blearning disabilities support\b", r"\bmental health support worker\b",
            r"\bsupported living\b", r"\bcare support worker\b",
        ],
        [
            r"\bit support\b", r"\btechnical support\b", r"\bsales support\b",
            r"\bcustomer support\b", r"\bbusiness support\b", r"\bdesktop support\b",
        ],
    ),
    (
        "healthcare_assistant",
        [
            r"\bhealthcare assistant\b", r"\bhealth care assistant\b", r"\bhca\b",
            r"\bclinical support worker\b", r"\bnursing assistant\b",
        ],
        [],
    ),
    (
        "care_assistant",
        [
            r"\bcare assistant\b", r"\bcare worker\b", r"\bhome care\b",
            r"\bdomiciliary care\b", r"\bcaregiver\b", r"\bcarer\b",
        ],
        [
            r"\bcustomer care\b", r"\bcare coordinator\b", r"\bcare co-ordinator\b",
        ],
    ),
    (
        "care_coordinator",
        [
            r"\bcare coordinator\b", r"\bcare co-ordinator\b",
            r"\bcare scheduler\b", r"\bcare planner\b",
        ],
        [],
    ),
    (
        "service_administrator",
        [
            r"\bservice administrator\b", r"\bservice admin\b",
            r"\bcustomer service administrator\b", r"\bcustomer service admin\b",
            r"\bservice coordinator\b", r"\bservice co-ordinator\b",
            r"\bservice advisor\b", r"\bservice adviser\b",
            r"\bhelpdesk administrator\b", r"\bhelpdesk admin\b",
        ],
        [
            r"\bautomotive service advisor\b", r"\bvehicle service advisor\b",
        ],
    ),
    (
        "customer_service",
        [
            r"\bcustomer service\b", r"\bcustomer advisor\b",
            r"\bcustomer adviser\b", r"\bcustomer support\b",
            r"\bcontact centre\b", r"\bcall centre\b", r"\bcall center\b",
            r"\bclient support\b", r"\bcustomer care\b",
        ],
        [],
    ),
    (
        "scheduler_planner",
        [
            r"\bscheduler\b", r"\bplanner\b", r"\bplanning administrator\b",
            r"\bplanning admin\b", r"\bworks planner\b", r"\brepairs planner\b",
            r"\bresource planner\b", r"\bwork scheduler\b",
        ],
        [
            r"\btown planner\b", r"\btransport planner\b", r"\bfinancial planner\b",
        ],
    ),
    (
        "administrator_general",
        [
            r"\badministrator\b", r"\badmin assistant\b", r"\boffice administrator\b",
            r"\boffice admin\b", r"\bbusiness administrator\b",
            r"\boperations administrator\b", r"\bdata administrator\b",
        ],
        [
            r"\bsystems administrator\b", r"\bit administrator\b",
            r"\bdatabase administrator\b", r"\bnetwork administrator\b",
        ],
    ),
    (
        "warehouse_logistics",
        [
            r"\bwarehouse\b", r"\bpicker\b", r"\bpacker\b",
            r"\bforklift\b", r"\bflt\b", r"\blogistics\b",
            r"\bparcel sorter\b", r"\bdespatch\b", r"\bdispatch\b",
        ],
        [],
    ),
    (
        "sales",
        [
            r"\bsales\b", r"\bbusiness development\b", r"\baccount executive\b",
            r"\btelemarketing\b", r"\btelesales\b",
        ],
        [
            r"\bsales support\b", r"\bsales administrator\b",
        ],
    ),
    (
        "teaching_assistant",
        [
            r"\bteaching assistant\b", r"\bta\b", r"\blearning support assistant\b",
            r"\bclassroom assistant\b", r"\bsen\b",
        ],
        [],
    ),
    (
        "finance_admin",
        [
            r"\baccounts assistant\b", r"\bfinance assistant\b",
            r"\bpayroll administrator\b", r"\bpurchase ledger\b",
            r"\bsales ledger\b", r"\bcredit controller\b",
        ],
        [],
    ),
]

JOB_FAMILIES = [family for family, _, _ in JOB_FAMILY_RULES]


# -----------------------------
# Column detection
# -----------------------------

COLUMN_ALIASES = {
    "title": [
        "title", "job title", "/job/title", "job_title", "position", "role",
    ],
    "location": [
        "location", "job location", "/job/location", "city", "town", "region",
    ],
    "description": [
        "description", "job description", "/job/description", "body", "job_description",
    ],
    "company": [
        "company", "employer", "recruiter", "advertiser", "/job/company",
        "/job/recruiter", "company name", "recruiter name",
    ],
    "salary": [
        "salary", "salary text", "salary_text", "/job/salary", "pay", "rate",
        "salary description",
    ],
}


def clean_col_name(value: object) -> str:
    return str(value).strip().lower().replace("\\", "/").replace("  ", " ")


def find_column(df: pd.DataFrame, logical_name: str) -> Optional[str]:
    aliases = [clean_col_name(a) for a in COLUMN_ALIASES[logical_name]]
    normalised = {clean_col_name(c): c for c in df.columns}

    # Location needs special handling. Some JobG8 exports contain region-ish
    # columns as well as the true location field. The profiler must map from
    # the original town/location text, not a broad/blank region column.
    if logical_name == "location":
        scored = []
        for norm_col, original_col in normalised.items():
            score = 0
            if norm_col in ["/job/location", "job location", "location"]:
                score = 100
            elif "job/location" in norm_col or "/location" in norm_col:
                score = 95
            elif "location" in norm_col:
                score = 90
            elif norm_col in ["city", "town"] or norm_col.endswith("/city") or norm_col.endswith("/town"):
                score = 80
            elif norm_col == "region" or norm_col.endswith("/region") or "region" in norm_col:
                score = 10

            if score:
                scored.append((score, original_col))

        if scored:
            scored.sort(key=lambda item: item[0], reverse=True)
            return scored[0][1]

        return None

    for alias in aliases:
        if alias in normalised:
            return normalised[alias]

    # fallback: contains match, useful for feeds with verbose paths
    for norm_col, original_col in normalised.items():
        for alias in aliases:
            if alias in norm_col:
                return original_col

    return None


def require_column(df: pd.DataFrame, logical_name: str) -> str:
    col = find_column(df, logical_name)
    if not col:
        raise ValueError(
            f"Could not find a {logical_name!r} column. "
            f"Available columns: {list(df.columns)}"
        )
    return col


# -----------------------------
# Cleaning and classification
# -----------------------------

def normalise_text(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).lower()
    text = re.sub(r"[^a-z0-9£€$.,/\-\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalise_title(value: object) -> str:
    text = normalise_text(value)
    text = re.sub(r"\b(full time|part time|permanent|temporary|temp|contract|hybrid|remote)\b", " ", text)
    text = re.sub(r"\b(days|nights|night shift|day shift|immediate start)\b", " ", text)
    text = re.sub(r"\b\(?[mf]/[fd]\)?\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" -")
    return text or "unknown_title"


def classify_region_keywords(location: object) -> str:
    loc = normalise_text(location)
    if not loc:
        return "Other / Unknown"

    for region, keywords in REGION_KEYWORDS.items():
        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword.lower()) + r"\b"
            if re.search(pattern, loc):
                return region

    return "Other / Unknown"


def classify_region(location: object, geo_mapper: Optional[GeoMapper] = None) -> str:
    if geo_mapper:
        return geo_mapper.classify(location)
    return classify_region_keywords(location)


def pattern_hit(patterns: Iterable[str], text: str) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def classify_family(title: object, description: object = "") -> str:
    title_text = normalise_text(title)
    desc_text = normalise_text(description)
    combined = f"{title_text} {desc_text[:500]}"

    for family, include_patterns, exclude_patterns in JOB_FAMILY_RULES:
        # Use title first. Description acts only as a weak backup.
        title_included = pattern_hit(include_patterns, title_text)
        combined_included = pattern_hit(include_patterns, combined)
        excluded = pattern_hit(exclude_patterns, combined)

        if (title_included or combined_included) and not excluded:
            return family

    return "unclassified"


def extract_date_from_filename(path: Path) -> Optional[str]:
    text = path.stem
    patterns = [
        r"(20\d{2})[-_\.](\d{2})[-_\.](\d{2})",
        r"(\d{2})[-_\.](\d{2})[-_\.](20\d{2})",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if not match:
            continue

        parts = match.groups()
        if len(parts[0]) == 4:
            year, month, day = parts
        else:
            day, month, year = parts

        return f"{year}-{month}-{day}"

    return None


def parse_salary_band(value: object) -> str:
    text = normalise_text(value)
    if not text:
        return "unknown_salary"

    # crude but useful V1 extraction
    nums = []
    for raw in re.findall(r"\b\d{2,6}(?:[,.]\d{3})*(?:\.\d+)?\b", text):
        cleaned = raw.replace(",", "")
        try:
            nums.append(float(cleaned))
        except ValueError:
            pass

    if not nums:
        return "unknown_salary"

    # If hourly rate likely, convert rough annual equivalent using 37.5 hours x 52 weeks.
    if any(token in text for token in ["hour", "hr", "ph", "per hour", "/h"]):
        annuals = [n * 37.5 * 52 for n in nums if n < 100]
    else:
        annuals = []
        for n in nums:
            if n < 100:
                annuals.append(n * 37.5 * 52)
            elif n < 1000:
                continue
            elif n < 100:
                annuals.append(n * 1000)
            else:
                annuals.append(n)

    if not annuals:
        return "unknown_salary"

    annual = max(annuals)

    if annual < 22000:
        return "under_22k"
    if annual < 25000:
        return "22k_25k"
    if annual < 30000:
        return "25k_30k"
    return "30k_plus"


# -----------------------------
# File loading
# -----------------------------

def read_jobg8_file(path: Path, geo_mapper: Optional[GeoMapper] = None) -> pd.DataFrame:
    try:
        df = pd.read_excel(path, engine="openpyxl")
    except TypeError:
        # The repository includes a tiny pandas shim for constrained local runs;
        # it does not accept engine= but can still read the bundled xlsx files.
        try:
            df = pd.read_excel(path)
        except Exception as exc:
            raise RuntimeError(f"Failed reading {path.name}: {exc}") from exc
    except Exception as exc:
        raise RuntimeError(f"Failed reading {path.name}: {exc}") from exc

    if df.empty:
        return df

    title_col = require_column(df, "title")
    location_col = find_column(df, "location")
    description_col = find_column(df, "description")
    company_col = find_column(df, "company")
    salary_col = find_column(df, "salary")

    # Preserve the source row index before assigning scalar columns.
    # Without an index here, scalar assignments such as date/source_file stay empty,
    # then become NaN when title/location columns are added later.
    # That made top-title days_seen show as 0.
    out = pd.DataFrame(index=df.index)
    out["source_file"] = path.name
    out["date"] = extract_date_from_filename(path) or "unknown_date"
    out["title"] = df[title_col].fillna("").astype(str)
    out["normalised_title"] = out["title"].apply(normalise_title)

    out["location"] = df[location_col].fillna("").astype(str) if location_col else ""
    out["description"] = df[description_col].fillna("").astype(str) if description_col else ""
    out["company"] = df[company_col].fillna("").astype(str) if company_col else ""
    out["salary_text"] = df[salary_col].fillna("").astype(str) if salary_col else ""

    region_results = [
        geo_mapper.classify_with_context(location, title, desc) if geo_mapper else (classify_region_keywords(location), "location_keyword", "")
        for location, title, desc in zip(out["location"], out["title"], out["description"])
    ]
    out["region"] = [result[0] for result in region_results]
    out["region_match_source"] = [result[1] for result in region_results]
    out["region_match_place"] = [result[2] for result in region_results]

    out["job_family"] = [
        classify_family(title, desc)
        for title, desc in zip(out["title"], out["description"])
    ]
    out["salary_band"] = out["salary_text"].apply(parse_salary_band)

    return out


# -----------------------------
# Reports
# -----------------------------

def build_daily_summary(all_jobs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for date, group in all_jobs.groupby("date", dropna=False):
        row = {"date": date, "total_jobs": len(group)}
        for region in REGION_ORDER:
            row[f"total_{slug(region)}"] = int((group["region"] == region).sum())
        row["total_other_unknown"] = int((group["region"] == "Other / Unknown").sum())
        rows.append(row)

    return pd.DataFrame(rows).sort_values("date")


def build_family_trends(all_jobs: pd.DataFrame, month: str) -> pd.DataFrame:
    """Monthly family-level summary.

    V2 keeps this compact: one row per job family for the month, with breadth
    guardrails that show whether volume is spread across titles, companies,
    locations and regions, or concentrated in repeated campaigns.
    """
    rows = []
    valid_dates = [d for d in all_jobs["date"].dropna().unique() if d != "unknown_date"]
    total_days = len(set(valid_dates))

    for family in sorted(all_jobs["job_family"].dropna().unique()):
        fam_group = all_jobs[all_jobs["job_family"] == family]
        if fam_group.empty:
            continue

        row = {
            "month": month,
            "job_family": family,
            "total_jobs": len(fam_group),
            "days_seen": fam_group["date"].nunique(),
            "unique_titles": unique_nonblank_count(fam_group["normalised_title"]),
            "unique_companies": unique_nonblank_count(fam_group["company"]),
            "unique_locations": unique_nonblank_count(fam_group["location"]),
            "top_regions": top_values(fam_group["region"], limit=5),
            "slice_viability_flag": family_viability_flag(all_jobs, family, total_days),
        }
        for region in REGION_ORDER:
            row[slug(region)] = int((fam_group["region"] == region).sum())
        row["other_unknown"] = int((fam_group["region"] == "Other / Unknown").sum())
        rows.append(row)

    if not rows:
        return pd.DataFrame(columns=[
            "month", "job_family", "total_jobs", "days_seen", "unique_titles",
            "unique_companies", "unique_locations", "top_regions",
            "slice_viability_flag", *[slug(r) for r in REGION_ORDER], "other_unknown"
        ])

    return pd.DataFrame(rows).sort_values(["total_jobs", "job_family"], ascending=[False, True])


def build_slice_viability(all_jobs: pd.DataFrame, month: str) -> pd.DataFrame:
    rows = []
    columns = [
        "month",
        "region",
        "job_family",
        "days_seen",
        "average_daily_count",
        "lowest_daily_count",
        "highest_daily_count",
        "month_start_avg",
        "month_end_avg",
        "month_end_drop_pct",
        "days_above_6",
        "days_above_12",
        "viability",
    ]

    valid_dates = sorted([d for d in all_jobs["date"].unique() if d != "unknown_date"])

    # If the month has readable files but no date can be extracted from filenames,
    # still write an empty slice-viability CSV with the correct headers instead of crashing.
    if not valid_dates:
        return pd.DataFrame(columns=columns)

    first_window = set(valid_dates[:5])
    last_window = set(valid_dates[-5:])

    for region in REGION_ORDER:
        for family in sorted(all_jobs["job_family"].unique()):
            if family == "unclassified":
                continue

            daily_counts = []
            for date in valid_dates:
                count = len(
                    all_jobs[
                        (all_jobs["date"] == date)
                        & (all_jobs["region"] == region)
                        & (all_jobs["job_family"] == family)
                    ]
                )
                daily_counts.append((date, count))

            counts = [count for _, count in daily_counts]
            if not counts or max(counts) == 0:
                continue

            start_counts = [count for date, count in daily_counts if date in first_window]
            end_counts = [count for date, count in daily_counts if date in last_window]

            start_avg = sum(start_counts) / len(start_counts) if start_counts else 0
            end_avg = sum(end_counts) / len(end_counts) if end_counts else 0
            avg = sum(counts) / len(counts)
            lowest = min(counts)
            highest = max(counts)
            days_seen = sum(1 for c in counts if c > 0)
            days_above_6 = sum(1 for c in counts if c >= 6)
            days_above_12 = sum(1 for c in counts if c >= 12)
            drop_pct = ((start_avg - end_avg) / start_avg * 100) if start_avg else 0

            if days_above_12 == len(counts) and lowest >= 12:
                viability = "strong"
            elif days_above_6 == len(counts) and avg >= 12:
                viability = "usable_watch"
            elif days_above_6 >= max(1, int(len(counts) * 0.7)):
                viability = "thin_but_possible"
            else:
                viability = "weak"

            if start_avg > 0 and drop_pct >= 50:
                viability = f"{viability}_month_end_drop"

            rows.append({
                "month": month,
                "region": region,
                "job_family": family,
                "days_seen": days_seen,
                "average_daily_count": round(avg, 1),
                "lowest_daily_count": lowest,
                "highest_daily_count": highest,
                "month_start_avg": round(start_avg, 1),
                "month_end_avg": round(end_avg, 1),
                "month_end_drop_pct": round(drop_pct, 1),
                "days_above_6": days_above_6,
                "days_above_12": days_above_12,
                "viability": viability,
            })

    # If there are jobs in the feed but none match the profiled Ontap families/regions,
    # write the CSV headers and continue rather than raising KeyError: 'viability'.
    if not rows:
        return pd.DataFrame(columns=columns)

    return pd.DataFrame(rows, columns=columns).sort_values(
        ["viability", "region", "average_daily_count"],
        ascending=[True, True, False],
    )


def build_top_titles(all_jobs: pd.DataFrame, month: str, limit: int = 200) -> pd.DataFrame:
    rows = []

    grouped = all_jobs.groupby("normalised_title", dropna=False)
    for title, group in grouped:
        examples = "; ".join(
            list(dict.fromkeys(group["title"].dropna().astype(str).head(5).tolist()))
        )
        likely_family = most_common_value(group["job_family"])
        rows.append({
            "month": month,
            "normalised_title": title,
            "total_count": len(group),
            "days_seen": group["date"].nunique(),
            "example_titles": examples,
            "likely_family": likely_family,
        })

    return (
        pd.DataFrame(rows)
        .sort_values(["total_count", "days_seen"], ascending=[False, False])
        .head(limit)
    )


def build_unclassified_titles(all_jobs: pd.DataFrame, month: str, limit: int = 200) -> pd.DataFrame:
    unclassified = all_jobs[all_jobs["job_family"] == "unclassified"].copy()
    rows = []

    for title, group in unclassified.groupby("normalised_title", dropna=False):
        rows.append({
            "month": month,
            "title": title,
            "total_count": len(group),
            "days_seen": group["date"].nunique(),
            "example_region": most_common_value(group["region"]),
            "example_company": most_common_value(group["company"]),
        })

    if not rows:
        return pd.DataFrame(columns=[
            "month", "title", "total_count", "days_seen",
            "example_region", "example_company"
        ])

    return (
        pd.DataFrame(rows)
        .sort_values(["total_count", "days_seen"], ascending=[False, False])
        .head(limit)
    )



def build_title_breadth(all_jobs: pd.DataFrame, month: str, limit: int = 500) -> pd.DataFrame:
    rows = []

    for title, group in all_jobs.groupby("normalised_title", dropna=False):
        examples = "; ".join(
            list(dict.fromkeys(group["title"].dropna().astype(str).head(5).tolist()))
        )
        rows.append({
            "month": month,
            "normalised_title": title,
            "likely_family": most_common_value(group["job_family"]),
            "total_count": len(group),
            "days_seen": group["date"].nunique(),
            "unique_companies": unique_nonblank_count(group["company"]),
            "unique_locations": unique_nonblank_count(group["location"]),
            "top_companies": top_values(group["company"], limit=5),
            "top_locations": top_values(group["location"], limit=5),
            "top_regions": top_values(group["region"], limit=5),
            "example_titles": examples,
        })

    if not rows:
        return pd.DataFrame(columns=[
            "month", "normalised_title", "likely_family", "total_count", "days_seen",
            "unique_companies", "unique_locations", "top_companies", "top_locations",
            "top_regions", "example_titles"
        ])

    return (
        pd.DataFrame(rows)
        .sort_values(["total_count", "days_seen"], ascending=[False, False])
        .head(limit)
    )


def build_family_region_breakdown(all_jobs: pd.DataFrame, month: str) -> pd.DataFrame:
    rows = []

    grouped = all_jobs.groupby(["region", "job_family"], dropna=False)
    for (region, family), group in grouped:
        rows.append({
            "month": month,
            "region": region,
            "likely_family": family,
            "total_count": len(group),
            "unique_companies": unique_nonblank_count(group["company"]),
            "unique_locations": unique_nonblank_count(group["location"]),
            "top_titles": top_values(group["normalised_title"], limit=10),
        })

    if not rows:
        return pd.DataFrame(columns=[
            "month", "region", "likely_family", "total_count",
            "unique_companies", "unique_locations", "top_titles"
        ])

    return pd.DataFrame(rows).sort_values(
        ["region", "total_count", "likely_family"], ascending=[True, False, True]
    )




def read_profiler_csv(path: Path, warnings: List[str]) -> pd.DataFrame:
    """Read an already-written profiler CSV without making the daily run brittle."""
    if not path.exists():
        warnings.append(f"missing source report: {path}")
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except AttributeError:
        try:
            return pd.read_csv(str(path))
        except Exception as exc:
            warnings.append(f"could not read source report {path}: {exc}")
            return pd.DataFrame()
    except Exception as exc:
        warnings.append(f"could not read source report {path}: {exc}")
        return pd.DataFrame()


def compiler_top_from_report(
    report: pd.DataFrame,
    value_column: str,
    count_column: str = "total_count",
    limit: int = 5,
) -> str:
    if report.empty or value_column not in report.columns or count_column not in report.columns:
        return ""

    rows = []
    for _, row in report.head(limit).iterrows():
        value = str(row.get(value_column, "")).strip()
        if not value or value.lower() == "nan":
            continue
        try:
            count = int(float(row.get(count_column, 0)))
        except (TypeError, ValueError):
            count = 0
        rows.append(f"{value} ({count})" if count else value)
    return "; ".join(rows)


def compiler_red_flag_text(flags: List[str]) -> str:
    return "; ".join(dict.fromkeys(flag for flag in flags if flag)) or "none"


def compiler_slice_status(
    support_count: int,
    admin_count: int,
    total_region_jobs: int,
    red_flags: List[str],
) -> str:
    serious_flags = [flag for flag in red_flags if "missing source report" not in flag and "could not read source report" not in flag]
    if any("sharp feed total drop" in flag or "generic Yorkshire" in flag for flag in serious_flags):
        return "INVESTIGATE"
    if support_count == 0 and admin_count == 0:
        return "INVESTIGATE" if total_region_jobs >= 20 else "THIN"
    if support_count >= 12 and admin_count >= 12 and not serious_flags:
        return "STRONG"
    if support_count >= 6 and admin_count >= 6:
        return "OK" if not serious_flags else "INVESTIGATE"
    if support_count >= 3 or admin_count >= 3:
        return "THIN" if not serious_flags else "INVESTIGATE"
    return "THIN"


def compiler_recommendation(status: str, red_flags: List[str]) -> str:
    flag_text = " | ".join(red_flags).lower()
    if status == "STRONG":
        return "Publish candidate"
    if "location mapping" in flag_text or "generic yorkshire" in flag_text or "unmapped" in flag_text:
        return "Investigate location mapping"
    if "dominates" in flag_text:
        return "Hold unless manually topped up"
    if status == "OK":
        return "Publish candidate"
    if status == "THIN":
        return "Not enough depth yet"
    return "Hold unless manually topped up"


def build_compiler_summary_from_outputs(
    all_jobs: pd.DataFrame,
    month: str,
    output_dir: Path,
) -> Tuple[pd.DataFrame, List[str]]:
    """Build a first-stop operational CSV from the existing profiler outputs.

    The summary intentionally reuses the CSVs written by the profiler earlier in
    the same run. Missing source CSVs are treated as red flags so the GitHub
    Action still produces a compiler summary for operators to inspect.
    """
    warnings: List[str] = []

    daily = read_profiler_csv(output_dir / "daily" / f"{month}-daily-summary.csv", warnings)
    family_trends = read_profiler_csv(output_dir / "monthly" / f"{month}-family-trends.csv", warnings)
    slice_viability = read_profiler_csv(output_dir / "monthly" / f"{month}-slice-viability.csv", warnings)
    title_breadth = read_profiler_csv(output_dir / "title-analysis" / f"{month}-title-breadth.csv", warnings)
    regional_breakdown = read_profiler_csv(output_dir / "regional" / f"{month}-family-region-breakdown.csv", warnings)
    location_audit = read_profiler_csv(output_dir / "regional" / f"{month}-regional-location-audit.csv", warnings)

    valid_dates = sorted(str(d) for d in all_jobs["date"].dropna().unique() if str(d) != "unknown_date")
    run_date = valid_dates[-1] if valid_dates else date.today().isoformat()
    total_jobs = int(len(all_jobs))
    total_support = int(all_jobs["job_family"].isin(SUPPORT_WORKER_FAMILIES).sum())
    total_admin = int(all_jobs["job_family"].isin(ADMIN_SERVICE_FAMILIES).sum())

    shared_flags = list(warnings)

    if not daily.empty and {"date", "total_jobs"}.issubset(daily.columns):
        known_daily = daily[daily["date"].astype(str) != "unknown_date"].copy()
        if len(known_daily) >= 2:
            known_daily["total_jobs_numeric"] = pd.to_numeric(known_daily["total_jobs"], errors="coerce").fillna(0)
            latest = known_daily.sort_values("date").iloc[-1]
            earlier = known_daily.sort_values("date").iloc[:-1]
            earlier_max = float(earlier["total_jobs_numeric"].max()) if not earlier.empty else 0
            latest_total = float(latest["total_jobs_numeric"])
            if earlier_max > 0 and latest_total <= earlier_max * 0.6:
                shared_flags.append(
                    f"sharp feed total drop versus earlier days: latest {int(latest_total)} vs earlier high {int(earlier_max)}"
                )

    if not location_audit.empty and {"mapped_region", "raw_location", "total_count"}.issubset(location_audit.columns):
        audit = location_audit.copy()
        audit["total_count_numeric"] = pd.to_numeric(audit["total_count"], errors="coerce").fillna(0)
        unmapped_count = int(audit.loc[audit["mapped_region"].astype(str) == "Other / Unknown", "total_count_numeric"].sum())
        if total_jobs and unmapped_count / total_jobs >= 0.5:
            shared_flags.append(f"many jobs unmapped: {unmapped_count} of {total_jobs}")
        yorkshire_count = int(audit.loc[audit["raw_location"].astype(str).str.lower() == "yorkshire", "total_count_numeric"].sum())
        if total_jobs and yorkshire_count / total_jobs >= 0.03:
            shared_flags.append(f"many jobs in generic Yorkshire: {yorkshire_count} of {total_jobs}")

    dominant_company = ""
    dominant_title = ""
    if not title_breadth.empty:
        if {"normalised_title", "total_count"}.issubset(title_breadth.columns):
            top_title = title_breadth.copy()
            top_title["total_count_numeric"] = pd.to_numeric(top_title["total_count"], errors="coerce").fillna(0)
            top_title = top_title.sort_values("total_count_numeric", ascending=False).head(1)
            if not top_title.empty:
                title_count = int(top_title.iloc[0]["total_count_numeric"])
                title_name = str(top_title.iloc[0].get("normalised_title", "")).strip()
                if total_jobs and title_count / total_jobs >= 0.08:
                    dominant_title = f"one title dominates: {title_name} ({title_count})"
        if "top_companies" in title_breadth.columns:
            company_counter: Counter[str] = Counter()
            for value in title_breadth["top_companies"].dropna().astype(str):
                for company, count in re.findall(r"([^;()]+)\s+\((\d+)\)", value):
                    company_counter[company.strip()] += int(count)
            if company_counter:
                company, count = company_counter.most_common(1)[0]
                if total_jobs and count / total_jobs >= 0.15:
                    dominant_company = f"one company dominates: {company} ({count})"
    if dominant_title:
        shared_flags.append(dominant_title)
    if dominant_company:
        shared_flags.append(dominant_company)

    rows = []
    for region in REGION_ORDER:
        region_jobs = all_jobs[all_jobs["region"] == region]
        support_count = int(region_jobs["job_family"].isin(SUPPORT_WORKER_FAMILIES).sum())
        admin_count = int(region_jobs["job_family"].isin(ADMIN_SERVICE_FAMILIES).sum())
        total_region_jobs = int(len(region_jobs))

        region_flags = list(shared_flags)
        if support_count < 3:
            region_flags.append(f"region has unexpectedly low support count: {support_count}")
        if admin_count < 3:
            region_flags.append(f"region has unexpectedly low admin/service count: {admin_count}")

        if not slice_viability.empty and {"region", "job_family", "viability"}.issubset(slice_viability.columns):
            region_viability = slice_viability[
                (slice_viability["region"].astype(str) == region)
                & (slice_viability["job_family"].astype(str).isin(SUPPORT_WORKER_FAMILIES + ADMIN_SERVICE_FAMILIES))
            ]
            drop_rows = region_viability[region_viability["viability"].astype(str).str.contains("month_end_drop", na=False)]
            if not drop_rows.empty:
                region_flags.append("sharp feed total drop compared with earlier days for key slices")

        region_breakdown = regional_breakdown[regional_breakdown["region"].astype(str) == region] if not regional_breakdown.empty and "region" in regional_breakdown.columns else pd.DataFrame()
        region_locations = location_audit[location_audit["mapped_region"].astype(str) == region] if not location_audit.empty and "mapped_region" in location_audit.columns else pd.DataFrame()

        status = compiler_slice_status(support_count, admin_count, total_region_jobs, region_flags)
        rows.append({
            "report_month": month,
            "run_date": run_date,
            "total_jobs_month_to_date": total_jobs,
            "total_support_worker_jobs": total_support,
            "total_admin_service_jobs": total_admin,
            "region": region,
            "support_worker_count": support_count,
            "admin_service_count": admin_count,
            "strongest_title_families": compiler_top_from_report(region_breakdown, "likely_family", limit=5),
            "top_locations": compiler_top_from_report(region_locations, "raw_location", limit=5),
            "top_companies": top_values(region_jobs["company"], limit=5),
            "slice_status": status,
            "recommendation": compiler_recommendation(status, region_flags),
            "red_flags": compiler_red_flag_text(region_flags),
        })

    if not rows:
        rows.append({
            "report_month": month,
            "run_date": run_date,
            "total_jobs_month_to_date": total_jobs,
            "total_support_worker_jobs": total_support,
            "total_admin_service_jobs": total_admin,
            "region": "All regions",
            "support_worker_count": total_support,
            "admin_service_count": total_admin,
            "strongest_title_families": compiler_top_from_report(family_trends, "job_family", "total_jobs", limit=5),
            "top_locations": "",
            "top_companies": top_values(all_jobs["company"], limit=5),
            "slice_status": "INVESTIGATE" if shared_flags else "THIN",
            "recommendation": "Investigate location mapping" if shared_flags else "Not enough depth yet",
            "red_flags": compiler_red_flag_text(shared_flags),
        })

    return pd.DataFrame(rows, columns=COMPILER_SUMMARY_COLUMNS), warnings

def build_regional_location_audit(all_jobs: pd.DataFrame, month: str) -> pd.DataFrame:
    """Shows which raw JobG8 locations are being mapped into each Ontap region."""
    rows = []

    group_cols = ["region", "location", "region_match_source", "region_match_place"]
    grouped = all_jobs.groupby(group_cols, dropna=False)
    for (region, location, match_source, match_place), group in grouped:
        loc = str(location).strip() if str(location).strip() else "blank_location"
        rows.append({
            "month": month,
            "mapped_region": region,
            "raw_location": loc,
            "match_source": match_source,
            "match_place": match_place,
            "total_count": len(group),
            "unique_companies": unique_nonblank_count(group["company"]),
            "top_titles": top_values(group["normalised_title"], limit=6),
            "top_families": top_values(group["job_family"], limit=6),
        })

    if not rows:
        return pd.DataFrame(columns=[
            "month", "mapped_region", "raw_location", "match_source", "match_place",
            "total_count", "unique_companies", "top_titles", "top_families"
        ])

    return pd.DataFrame(rows).sort_values(
        ["mapped_region", "total_count", "raw_location"], ascending=[True, False, True]
    )

def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")



def cleaned_values(series: pd.Series) -> List[str]:
    return [str(v).strip() for v in series.dropna() if str(v).strip()]


def unique_nonblank_count(series: pd.Series) -> int:
    return len(set(cleaned_values(series)))


def top_values(series: pd.Series, limit: int = 5) -> str:
    values = cleaned_values(series)
    if not values:
        return ""
    return "; ".join(f"{value} ({count})" for value, count in Counter(values).most_common(limit))


def family_viability_flag(all_jobs: pd.DataFrame, family: str, total_days: int) -> str:
    valid_dates = sorted([d for d in all_jobs["date"].dropna().unique() if d != "unknown_date"])
    if not valid_dates:
        return "unknown_no_valid_dates"

    counts = []
    for date in valid_dates:
        counts.append(len(all_jobs[(all_jobs["date"] == date) & (all_jobs["job_family"] == family)]))

    if not counts or max(counts) == 0:
        return "not_seen"

    days_seen = sum(1 for c in counts if c > 0)
    days_above_6 = sum(1 for c in counts if c >= 6)
    days_above_12 = sum(1 for c in counts if c >= 12)
    avg = sum(counts) / len(counts)
    lowest = min(counts)

    if days_above_12 == len(counts) and lowest >= 12:
        flag = "strong"
    elif days_above_6 == len(counts) and avg >= 12:
        flag = "usable_watch"
    elif days_above_6 >= max(1, int(len(counts) * 0.7)):
        flag = "thin_but_possible"
    elif days_seen >= max(1, int(total_days * 0.5)):
        flag = "visible_but_weak"
    else:
        flag = "weak"

    return flag

def most_common_value(series: pd.Series) -> str:
    values = [str(v).strip() for v in series.dropna() if str(v).strip()]
    if not values:
        return ""
    return Counter(values).most_common(1)[0][0]


# -----------------------------
# Main
# -----------------------------

def run(input_dir: Path, output_dir: Path, month: str, geo_lookup: Optional[Path] = None) -> None:
    files = sorted(
        list(input_dir.glob("*.xlsx"))
        + list(input_dir.glob("*.xls"))
        + list(input_dir.glob("*.xlsm"))
    )

    files = [f for f in files if not f.name.startswith("~$")]

    if not files:
        raise FileNotFoundError(f"No Excel files found in: {input_dir}")

    frames = []
    errors = []

    geo_lookup = resolve_geo_lookup_arg(geo_lookup)
    geo_lookup_exists = geo_lookup.exists()

    geo_mapper = GeoMapper(geo_lookup)
    geo_lookup_status = "loaded" if geo_mapper.lookup_loaded else "not loaded"
    fallback_status = "yes" if geo_mapper.fallback_keywords_enabled else "no"

    for path in files:
        try:
            frame = read_jobg8_file(path, geo_mapper=geo_mapper)
            if not frame.empty:
                frames.append(frame)
        except Exception as exc:
            errors.append(f"{path.name}: {exc}")

    if not frames:
        raise RuntimeError("No readable job rows found in the supplied files.")

    all_jobs = pd.concat(frames, ignore_index=True)

    daily_dir = output_dir / "daily"
    monthly_dir = output_dir / "monthly"
    title_dir = output_dir / "title-analysis"
    regional_dir = output_dir / "regional"
    compiler_dir = output_dir / "compiler-summary"

    for folder in [daily_dir, monthly_dir, title_dir, regional_dir, compiler_dir]:
        folder.mkdir(parents=True, exist_ok=True)

    build_daily_summary(all_jobs).to_csv(
        daily_dir / f"{month}-daily-summary.csv", index=False
    )
    build_family_trends(all_jobs, month).to_csv(
        monthly_dir / f"{month}-family-trends.csv", index=False
    )
    build_slice_viability(all_jobs, month).to_csv(
        monthly_dir / f"{month}-slice-viability.csv", index=False
    )
    build_top_titles(all_jobs, month).to_csv(
        title_dir / f"{month}-top-titles.csv", index=False
    )
    build_unclassified_titles(all_jobs, month).to_csv(
        title_dir / f"{month}-unclassified-titles.csv", index=False
    )
    build_title_breadth(all_jobs, month).to_csv(
        title_dir / f"{month}-title-breadth.csv", index=False
    )
    build_family_region_breakdown(all_jobs, month).to_csv(
        regional_dir / f"{month}-family-region-breakdown.csv", index=False
    )
    build_regional_location_audit(all_jobs, month).to_csv(
        regional_dir / f"{month}-regional-location-audit.csv", index=False
    )
    compiler_summary_path = compiler_dir / f"{month}-compiler-summary.csv"
    compiler_summary, compiler_warnings = build_compiler_summary_from_outputs(
        all_jobs=all_jobs,
        month=month,
        output_dir=output_dir,
    )
    compiler_summary.to_csv(compiler_summary_path, index=False)

    # Also save a small run log.
    log_lines = [
        f"Month: {month}",
        f"Input folder: {input_dir}",
        f"Files found: {len(files)}",
        f"Files read successfully: {len(frames)}",
        f"Total rows profiled: {len(all_jobs)}",
        f"Current working directory: {Path.cwd().resolve()}",
        f"Resolved geo lookup path: {geo_lookup}",
        f"Geo lookup file exists: {'yes' if geo_lookup_exists else 'no'}",
        f"Geo lookup status: {geo_lookup_status}",
        f"Geo lookup rows loaded: {geo_mapper.lookup_rows_loaded}",
        f"Fallback keyword rules used: {fallback_status}",
        "",
        "Output files:",
        f"- {daily_dir / f'{month}-daily-summary.csv'}",
        f"- {monthly_dir / f'{month}-family-trends.csv'}",
        f"- {monthly_dir / f'{month}-slice-viability.csv'}",
        f"- {title_dir / f'{month}-top-titles.csv'}",
        f"- {title_dir / f'{month}-unclassified-titles.csv'}",
        f"- {title_dir / f'{month}-title-breadth.csv'}",
        f"- {regional_dir / f'{month}-family-region-breakdown.csv'}",
        f"- {regional_dir / f'{month}-regional-location-audit.csv'}",
        f"- {compiler_summary_path}",
        "",
        f"Compiler summary generated: {compiler_summary_path}",
    ]

    if errors:
        log_lines.extend(["", "Files with errors:"])
        log_lines.extend(f"- {e}" for e in errors)

    if compiler_warnings:
        log_lines.extend(["", "Compiler summary warnings:"])
        log_lines.extend(f"- {warning}" for warning in compiler_warnings)

    if geo_mapper.lookup_error:
        log_lines.extend(["", f"Geo lookup note: {geo_mapper.lookup_error}"])

    (output_dir / f"{month}-feed-profiler-run-log.txt").write_text(
        "\n".join(log_lines),
        encoding="utf-8",
    )

    print("\n".join(log_lines))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Profile daily JobG8 uploads and produce monthly slice-depth reports."
    )
    parser.add_argument(
        "--month",
        required=True,
        help="Month in YYYY-MM format, e.g. 2026-05",
    )
    parser.add_argument(
        "--input-dir",
        default=None,
        help="Folder containing daily JobG8 Excel files. Default: input-jobg8-archive/<month>",
    )
    parser.add_argument(
        "--output-dir",
        default="output-feed-profiler",
        help="Output folder. Default: output-feed-profiler",
    )
    parser.add_argument(
        "--geo-lookup",
        "--geo-path",
        dest="geo_lookup",
        default=None,
        help="Optional geo lookup Excel file. Default: pipeline/geo/lookup.xlsx in this repository.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir) if args.input_dir else Path("input-jobg8-archive") / args.month
    output_dir = Path(args.output_dir)
    geo_lookup = Path(args.geo_lookup) if args.geo_lookup else None

    run(input_dir=input_dir, output_dir=output_dir, month=args.month, geo_lookup=geo_lookup)


if __name__ == "__main__":
    main()

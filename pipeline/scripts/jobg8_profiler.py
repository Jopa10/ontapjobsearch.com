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
    output-feed-profiler/regional/2026-05-geo-unmapped-review.csv
    output-feed-profiler/regional/2026-05-geo-lookup-qa-summary.csv

Optional geography:
    By default, the profiler reads pipeline/geo/lookup.xlsx from the repository
    and uses it to map raw JobG8 locations into Ontap regions. /input is not
    searched for geo files; pass --geo-lookup deliberately to override.
"""

from __future__ import annotations

import argparse
import json
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
    "section",
    "report_month",
    "run_date",
    "total_jobs_month_to_date",
    "total_support_worker_jobs",
    "total_admin_service_jobs",
    "overall_status",
    "headline_recommendation",
    "main_red_flags",
    "region",
    "slice_family",
    "selected_count",
    "selected_count_source_file",
    "profiler_count",
    "profiler_count_source_file",
    "status",
    "recommendation",
    "reconciliation_note",
    "month_to_date_count",
    "today_count",
    "red_flags",
    "warning_type",
    "severity",
    "finding",
    "source_file",
    "source_column",
    "source_filter_used",
    "validation_note",
]

TRACKED_ONTAP_REGIONS = ["West Yorkshire", "South Yorkshire"]
ACTIVE_ONTAP_SLICE_REGIONS = list(REGION_ORDER)
GEO_REVIEW_ACTIONS = [
    "ADD_TO_LOOKUP_ACTIVE_REGION",
    "ADD_TO_LOOKUP_OUTSIDE_ACTIVE_SLICE",
    "AMBIGUOUS_REVIEW",
    "FIX_EXISTING_LOOKUP",
    "IGNORE_BAD_OR_NON_UK",
]
UNMAPPED_LOCATION_WARNING_THRESHOLD = 0.20
UNMAPPED_LOCATION_HIGH_THRESHOLD = 0.50
DEFAULT_GEO_LOOKUP_PATH = Path(__file__).resolve().parents[1] / "geo" / "lookup.xlsx"
DEFAULT_GEO_LOOKUP_DISPLAY_PATH = Path("pipeline/geo/lookup.xlsx")


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
    "london": "London",
    "greater london": "London",
}


def display_region_from_cluster(cluster: object) -> Optional[str]:
    """Return the exact UK geography label represented by lookup.xlsx Cluster.

    Geography classification should preserve the workbook's most specific
    recognised cluster. Active Ontap slice membership is calculated separately
    from the cluster label, so broad reporting aliases such as London are not
    allowed to overwrite finer lookup clusters such as Croydon / South London.
    """
    cluster_text = str(cluster or "").strip()
    if not normalise_lookup_place(cluster_text):
        return None
    return cluster_text


def is_broad_london_cluster(cluster: object) -> bool:
    return normalise_lookup_place(cluster) in {"london", "greater london"}


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
        "not specified", "unspecified", "n/a", "na",
        "various", "multiple locations", "multiple sites",
        "scotland", "wales", "northern ireland", "great britain",
    }
    if loc in broad_exact:
        return True

    broad_contains = [
        "yorkshire and humber", "yorkshire & humber", "north of england",
        "northern england", "home based", "field based", "multiple locations",
    ]
    return any(term in loc for term in broad_contains)


UK_GEO_SUGGESTIONS: Dict[str, Tuple[str, str]] = {
    # Major cities and countries/counties commonly present in JobG8 feeds.
    "london": ("London", "city/county-level UK place"),
    "bristol": ("South West England", "UK city"),
    "birmingham": ("West Midlands", "UK city"),
    "edinburgh": ("Scotland", "UK city"),
    "liverpool": ("North West England / Merseyside", "UK city"),
    "cardiff": ("Wales", "UK city"),
    "glasgow": ("Scotland", "UK city"),
    "cambridge": ("East of England / Cambridgeshire", "UK city"),
    "leicester": ("East Midlands / Leicestershire", "UK city"),
    "nottingham": ("East Midlands / Nottinghamshire", "UK city"),
    "derby": ("East Midlands / Derbyshire", "UK city"),
    "coventry": ("West Midlands", "UK city"),
    "wolverhampton": ("West Midlands", "UK city"),
    "stoke-on-trent": ("West Midlands / Staffordshire", "UK city"),
    "norwich": ("East of England / Norfolk", "UK city"),
    "ipswich": ("East of England / Suffolk", "UK town"),
    "oxford": ("South East England / Oxfordshire", "UK city"),
    "reading": ("South East England / Berkshire", "UK town"),
    "southampton": ("South East England / Hampshire", "UK city"),
    "portsmouth": ("South East England / Hampshire", "UK city"),
    "brighton": ("South East England / East Sussex", "UK city"),
    "plymouth": ("South West England / Devon", "UK city"),
    "exeter": ("South West England / Devon", "UK city"),
    "swindon": ("South West England / Wiltshire", "UK town"),
    "bath": ("South West England / Somerset", "UK city"),
    "swansea": ("Wales", "UK city"),
    "newport": ("Wales", "UK city; ambiguous without county if not clearly Wales"),
    "aberdeen": ("Scotland", "UK city"),
    "dundee": ("Scotland", "UK city"),
    "inverness": ("Scotland", "UK city"),
    "belfast": ("Northern Ireland", "UK city"),
    # Counties and broader ceremonial/county labels used as useful clusters,
    # but many county-only rows should remain human-reviewed before addition.
    "kent": ("South East England / Kent", "UK county"),
    "surrey": ("South East England / Surrey", "UK county"),
    "essex": ("East of England / Essex", "UK county"),
    "hertfordshire": ("East of England / Hertfordshire", "UK county"),
    "bedfordshire": ("East of England / Bedfordshire", "UK county"),
    "buckinghamshire": ("South East England / Buckinghamshire", "UK county"),
    "berkshire": ("South East England / Berkshire", "UK county"),
    "oxfordshire": ("South East England / Oxfordshire", "UK county"),
    "cambridgeshire": ("East of England / Cambridgeshire", "UK county"),
    "suffolk": ("East of England / Suffolk", "UK county"),
    "norfolk": ("East of England / Norfolk", "UK county"),
    "hampshire": ("South East England / Hampshire", "UK county"),
    "dorset": ("South West England / Dorset", "UK county"),
    "devon": ("South West England / Devon", "UK county"),
    "cornwall": ("South West England / Cornwall", "UK county"),
    "somerset": ("South West England / Somerset", "UK county"),
    "wiltshire": ("South West England / Wiltshire", "UK county"),
    "gloucestershire": ("South West England / Gloucestershire", "UK county"),
    "warwickshire": ("West Midlands / Warwickshire", "UK county"),
    "staffordshire": ("West Midlands / Staffordshire", "UK county"),
    "shropshire": ("West Midlands / Shropshire", "UK county"),
    "worcestershire": ("West Midlands / Worcestershire", "UK county"),
    "leicestershire": ("East Midlands / Leicestershire", "UK county"),
    "nottinghamshire": ("East Midlands / Nottinghamshire", "UK county"),
    "derbyshire": ("East Midlands / Derbyshire", "UK county"),
    "lincolnshire": ("East Midlands / Lincolnshire", "UK county"),
    "northamptonshire": ("East Midlands / Northamptonshire", "UK county"),
    "merseyside": ("North West England / Merseyside", "UK county"),
    "cheshire": ("North West England / Cheshire", "UK county"),
}

NON_UK_OR_BAD_LOCATION_TERMS = {
    "blank_location", "unknown", "unknown location", "not applicable", "tbc",
    "republic of ireland", "ireland", "dublin", "cork", "galway",
}

COUNTY_ONLY_REVIEW_TERMS = {
    place for place, (_, reason) in UK_GEO_SUGGESTIONS.items() if "UK county" in reason
}

RISKY_AMBIGUOUS_PLACE_TERMS = {
    "bury st. edmunds", "bury st edmunds", "bury saint edmunds",
}


def _lookup_exact_suggestion(value: object) -> Tuple[str, str]:
    loc = normalise_lookup_place(value)
    if not loc:
        return "", ""
    if loc in UK_GEO_SUGGESTIONS:
        return UK_GEO_SUGGESTIONS[loc]
    return "", ""


def _uk_geo_suggestion_from_group(raw_location: object, group: pd.DataFrame) -> Tuple[str, str]:
    """Suggest a UK-wide lookup cluster for proposal/reporting rows only.

    The profiler still maps live regions only from pipeline/geo/lookup.xlsx; these
    suggestions help humans decide whether an unmapped UK place should be added
    to the shared workbook or held for review.
    """
    cluster, reason = _lookup_exact_suggestion(raw_location)
    if cluster:
        return cluster, reason

    for column in ["jobg8_area", "jobg8_location"]:
        if column not in group.columns:
            continue
        values = cleaned_values(group[column])
        for value, _ in Counter(values).most_common(5):
            cluster, reason = _lookup_exact_suggestion(value)
            if cluster:
                return cluster, f"{reason} from {column}"

    return "", ""


def _looks_non_uk_or_bad(raw_location: object, group: pd.DataFrame) -> Tuple[bool, str]:
    loc = normalise_lookup_place(raw_location)
    if not loc or loc in NON_UK_OR_BAD_LOCATION_TERMS:
        return True, "blank, bad, or explicitly non-UK location"

    context = " ".join(
        str(value)
        for column in ["jobg8_area", "jobg8_location", "normalised_title"]
        if column in group.columns
        for value in cleaned_values(group[column])[:5]
    ).lower()
    if "€" in context or any(term in context for term in ["republic of ireland", " dublin ", " cork ", " galway "]):
        return True, "non-UK signal in JobG8 area/location/title"

    return False, ""


class GeoMapper:
    """Maps raw JobG8 location text to Ontap regions using an optional lookup sheet.

    The lookup is deliberately used for region assignment only. Reports still count
    unique original JobG8 location strings separately, so repeated campaigns remain visible.
    """

    def __init__(self, lookup_path: Optional[Path] = None):
        self.place_to_region: Dict[str, str] = {}
        self.place_to_active_ontap_region: Dict[str, str] = {}
        self._lookup_items_by_length: List[Tuple[str, str]] = []
        self._lookup_patterns_by_length: List[Tuple[re.Pattern[str], str, str]] = []
        self.lookup_path = lookup_path
        self.lookup_loaded = False
        self.lookup_rows_loaded = 0
        self.lookup_mapped_row_count = 0
        self.lookup_source_rows = 0
        self.lookup_error = ""
        self.fallback_keywords_enabled = True

        if lookup_path:
            if lookup_path.exists():
                self.load_lookup(lookup_path)
            else:
                self.lookup_error = f"lookup file missing: {lookup_path}"

        # pipeline/geo/lookup.xlsx is the geography source of truth. Do not use
        # per-script keyword lists as an automatic mapping fallback.
        self.fallback_keywords_enabled = False

    def add_place(self, place: object, region: Optional[str], active_ontap_region: Optional[str] = None) -> bool:
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
        if active_ontap_region:
            self.place_to_active_ontap_region[place_text] = active_ontap_region
        self._lookup_items_by_length = []
        self._lookup_patterns_by_length = []
        return True

    def load_lookup(self, lookup_path: Path) -> None:
        loaded_rows = 0
        mapped_rows = 0
        source_rows = 0

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

            # Shared Ontap geo source of truth: Area -> Cluster.
            if "Area" not in df.columns or "Cluster" not in df.columns:
                continue

            for _, row in df.iterrows():
                if normalise_lookup_place(row.get("Area")):
                    source_rows += 1
                region = display_region_from_cluster(row.get("Cluster"))
                active_ontap_region = ontap_region_from_cluster(row.get("Cluster"), row.get("Area"))
                if normalise_lookup_place(row.get("Area")) and region:
                    mapped_rows += 1
                if self.add_place(row.get("Area"), region, active_ontap_region):
                    loaded_rows += 1

        self.lookup_source_rows = source_rows
        self.lookup_mapped_row_count = mapped_rows
        self.lookup_rows_loaded = loaded_rows
        self.lookup_loaded = loaded_rows > 0
        if self.lookup_loaded:
            self.lookup_error = ""
        elif not self.lookup_error:
            self.lookup_error = "lookup workbook must contain columns named exactly: Area, Cluster"

    def lookup_match(self, text: object) -> Tuple[Optional[str], str]:
        lookup_text = normalise_lookup_place(text)
        if not lookup_text:
            return None, ""

        # Prefer the most specific recognised lookup area, not the broadest exact
        # token. This makes values such as "Croydon, London" resolve through
        # Croydon when that cluster exists, with broad London used only when no
        # finer lookup key matches the same raw location.
        candidates: List[Tuple[int, int, str, str]] = []
        exact_region = self.place_to_region.get(lookup_text)
        if exact_region:
            candidates.append((len(lookup_text), 1, lookup_text, exact_region))

        # Prefer longest lookup terms first so "south shields" wins before "shields".
        if not self._lookup_patterns_by_length:
            self._lookup_items_by_length = sorted(self.place_to_region.items(), key=lambda item: len(item[0]), reverse=True)
            self._lookup_patterns_by_length = [
                (re.compile(r"(?<![a-z0-9])" + re.escape(place) + r"(?![a-z0-9])"), place, region)
                for place, region in self._lookup_items_by_length
            ]
        for pattern, place, region in self._lookup_patterns_by_length:
            if pattern.search(lookup_text):
                candidates.append((len(place), 0, place, region))

        if not candidates:
            return None, ""

        specific_candidates = [candidate for candidate in candidates if not is_broad_london_cluster(candidate[3])]
        best_length, _exact_priority, best_place, best_region = max(
            specific_candidates or candidates,
            key=lambda candidate: (candidate[0], candidate[1]),
        )
        del best_length
        return best_region, best_place

    def active_ontap_region_for_match(self, place: object, cluster: object) -> str:
        place_text = normalise_lookup_place(place)
        active_region = self.place_to_active_ontap_region.get(place_text)
        if active_region:
            return active_region
        return ontap_region_from_cluster(cluster, place) or ""

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
    """Return the shared Ontap geo lookup workbook path.

    base_dir is accepted for backwards-compatible callers, but the daily input
    folder and current working directory are intentionally not searched.
    """
    del base_dir
    return DEFAULT_GEO_LOOKUP_PATH.resolve()




def display_geo_lookup_path(path: Optional[Path]) -> str:
    if path is None:
        return ""
    try:
        if path.resolve() == DEFAULT_GEO_LOOKUP_PATH.resolve():
            return str(DEFAULT_GEO_LOOKUP_DISPLAY_PATH)
    except Exception:
        pass
    return str(path)


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
    "area": [
        "/job/area", "job area", "area", "town", "city",
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


def is_missing_location_value(value: object) -> bool:
    text = normalise_lookup_place(value)
    if not text:
        return True
    return text in {
        "not specified",
        "not set",
        "unknown",
        "n/a",
        "na",
        "none",
        "null",
        "city",
        "town",
    }


def choose_region_mapping_location(area: object, location: object) -> str:
    """Choose the most specific JobG8 geography field for region mapping.

    JobG8 exports often put the specific town/city in /Job/Area and a broader
    county/feed geography in /Job/Location. Ontap region mapping should therefore
    prefer /Job/Area when it contains a real place, falling back to /Job/Location
    for rows where /Job/Area is blank/generic (for example "Not Specified").
    """
    area_text = str(area or "").strip()
    if not is_missing_location_value(area_text):
        return area_text
    return str(location or "").strip()


def find_region_mapping_columns(df: pd.DataFrame) -> Tuple[Optional[str], Optional[str]]:
    """Return the source columns used to build the mappable JobG8 location.

    The first value is the town/area column and the second is the broader
    location fallback. These names are logged so region mapping can be audited.
    """
    return find_column(df, "area"), find_column(df, "location")


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
    area_col, location_col = find_region_mapping_columns(df)
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

    out["jobg8_area"] = df[area_col].fillna("").astype(str) if area_col else ""
    out["jobg8_location"] = df[location_col].fillna("").astype(str) if location_col else ""
    out["location"] = [
        choose_region_mapping_location(area, location)
        for area, location in zip(out["jobg8_area"], out["jobg8_location"])
    ]
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
    out["active_ontap_slice_region"] = [
        geo_mapper.active_ontap_region_for_match(match_place, region) if geo_mapper and match_source.endswith("lookup") else (region if region in ACTIVE_ONTAP_SLICE_REGIONS else "")
        for region, match_source, match_place in zip(out["region"], out["region_match_source"], out["region_match_place"])
    ]
    out["is_active_ontap_slice_region"] = [
        "yes" if region in ACTIVE_ONTAP_SLICE_REGIONS else "no"
        for region in out["active_ontap_slice_region"]
    ]

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
            row[f"total_{slug(region)}"] = int((group["active_ontap_slice_region"] == region).sum())
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
            row[slug(region)] = int((fam_group["active_ontap_slice_region"] == region).sum())
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
                        & (all_jobs["active_ontap_slice_region"] == region)
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
            "is_active_ontap_slice_region": "yes" if region in ACTIVE_ONTAP_SLICE_REGIONS else "no",
            "likely_family": family,
            "total_count": len(group),
            "unique_companies": unique_nonblank_count(group["company"]),
            "unique_locations": unique_nonblank_count(group["location"]),
            "top_titles": top_values(group["normalised_title"], limit=10),
        })

    if not rows:
        return pd.DataFrame(columns=[
            "month", "region", "is_active_ontap_slice_region", "likely_family", "total_count",
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


def compiler_source_path(path: Path, output_dir: Path) -> str:
    """Return a stable source report path for compiler trace columns."""
    try:
        return str(path.relative_to(output_dir.parent))
    except ValueError:
        return str(path)


def compiler_selector_file_slug(value: str) -> str:
    """Return the hyphenated slug used by final selector JSON filenames."""
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def compiler_selector_output_path(output_dir: Path, region: str, slice_family: str) -> Path:
    """Return the final selector JSON path used for a live Ontap slice."""
    base_dir = output_dir.parent
    region_slug = compiler_selector_file_slug(region)
    if slice_family == "support-worker":
        return base_dir / "output-support-worker" / f"{region_slug}-support-worker.json"
    return base_dir / "output-admin-service" / f"{region_slug}-admin-service.json"


def compiler_count_from_selector_json(
    path: Path,
    output_dir: Path,
    warnings: List[str],
) -> Tuple[int, str, str, bool]:
    """Read selected/published count from the final selector JSON output.

    The compiler summary treats this JSON as the operational source of truth
    because these files are the same outputs copied into the live pages.
    """
    source = compiler_source_path(path, output_dir)
    if not path.exists():
        warning = f"selector output missing: {path}"
        warnings.append(warning)
        return 0, source, warning, True

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        warning = f"could not read selector output for selected_count {path}: {exc}"
        warnings.append(warning)
        return 0, source, warning, True

    if isinstance(data, list):
        return len(data), source, "selected_count read from final selector JSON", False
    if isinstance(data, dict):
        for key in ("jobs", "selected_jobs", "selected", "published_jobs"):
            value = data.get(key)
            if isinstance(value, list):
                return len(value), source, f"selected_count read from final selector JSON field '{key}'", False
        warning = f"selector output for selected_count is an object without a recognised jobs list: {path}"
        warnings.append(warning)
        return 0, source, warning, True

    warning = f"selector output for selected_count has unsupported JSON shape: {path}"
    warnings.append(warning)
    return 0, source, warning, True


def compiler_reconciliation_note(
    selected_count: int,
    profiler_count: int,
    selector_note: str,
    profiler_issue: bool,
    selector_source_issue: bool,
) -> str:
    base_note = "selected_count from selector/publish output; profiler_count from broad feed profiler for QA only"
    if selector_source_issue:
        return compiler_join_notes([
            base_note,
            selector_note,
            "status set to INVESTIGATE because selector output could not be read",
        ])
    if selected_count == profiler_count and not profiler_issue:
        return f"{base_note}; counts match"

    notes = [base_note]
    if selected_count != profiler_count:
        notes.append(
            f"selected_count ({selected_count}) differs from profiler_count ({profiler_count}); profiler difference is diagnostic only and does not drive status"
        )
    if profiler_issue:
        notes.append("profiler source/mapping/classification cross-check needs review")
    return compiler_join_notes(notes)


def compiler_number_from_family_trends(
    family_trends: pd.DataFrame,
    family: str,
    region_column: Optional[str] = None,
) -> Tuple[int, str]:
    """Read a family total or family/region count from monthly family trends."""
    if family_trends.empty or "job_family" not in family_trends.columns:
        return 0, "family-trends source missing or lacks job_family"

    rows = family_trends[family_trends["job_family"].astype(str) == family]
    if rows.empty:
        return 0, f"family '{family}' not found in family-trends"

    column = region_column or "total_jobs"
    if column not in rows.columns:
        return 0, f"family-trends source lacks column '{column}'"

    value = int(pd.to_numeric(rows[column], errors="coerce").fillna(0).sum())
    return value, "matched family-trends row"


def compiler_number_from_regional_breakdown(
    family_region_breakdown: pd.DataFrame,
    region: str,
    families: List[str],
) -> Tuple[int, str]:
    """Read a regional family count from the family-region profiler report."""
    required = {"region", "likely_family", "total_count"}
    if family_region_breakdown.empty or not required.issubset(family_region_breakdown.columns):
        return 0, "family-region-breakdown source missing or lacks required columns"

    rows = family_region_breakdown[
        (family_region_breakdown["region"].astype(str) == region)
        & (family_region_breakdown["likely_family"].astype(str).isin(families))
    ]
    if rows.empty:
        return 0, "no matching family-region rows found"

    value = int(pd.to_numeric(rows["total_count"], errors="coerce").fillna(0).sum())
    return value, "matched family-region-breakdown row(s)"


def compiler_total_for_families_from_trends(
    family_trends: pd.DataFrame,
    families: List[str],
) -> Tuple[int, List[str]]:
    total = 0
    notes = []
    for family in families:
        count, note = compiler_number_from_family_trends(family_trends, family)
        total += count
        notes.append(f"{family}: {note}")
    return total, notes


def compiler_region_column(region: str) -> str:
    return slug(region)


def compiler_join_notes(notes: List[str]) -> str:
    return "; ".join(dict.fromkeys(note for note in notes if note)) or "validated"


def compiler_add_reconciliation_row(
    rows: List[dict],
    month: str,
    run_date: str,
    slice_family: str,
    metric: str,
    count: int,
    source_file: str,
    source_column: str,
    source_filter_used: str,
    validation_note: str,
) -> None:
    rows.append({
        "section": "RECONCILIATION",
        "report_month": month,
        "run_date": run_date,
        "region": metric,
        "slice_family": slice_family,
        "month_to_date_count": count,
        "source_file": source_file,
        "source_column": source_column,
        "source_filter_used": source_filter_used,
        "validation_note": validation_note,
    })


def compiler_top_from_report(
    report: pd.DataFrame,
    value_column: str,
    count_column: str = "total_count",
    limit: int = 5,
    suppress_values: Optional[List[str]] = None,
) -> str:
    if report.empty or value_column not in report.columns or count_column not in report.columns:
        return ""

    suppress = {value.lower() for value in (suppress_values or [])}
    rows = []
    for _, row in report.iterrows():
        value = str(row.get(value_column, "")).strip()
        if not value or value.lower() == "nan" or value.lower() in suppress:
            continue
        try:
            count = int(float(row.get(count_column, 0)))
        except (TypeError, ValueError):
            count = 0
        rows.append(f"{value} ({count})" if count else value)
        if len(rows) >= limit:
            break
    return "; ".join(rows)


def compiler_red_flag_text(flags: List[str]) -> str:
    return "; ".join(dict.fromkeys(flag for flag in flags if flag)) or "none"


def compiler_today_count(all_jobs: pd.DataFrame, run_date: str, has_valid_dates: bool, region: str, families: List[str]) -> str:
    if not has_valid_dates:
        return ""
    today_jobs = all_jobs[(all_jobs["date"].astype(str) == run_date) & (all_jobs["region"] == region)]
    return str(int(today_jobs["job_family"].isin(families).sum()))


def compiler_slice_status(selected_count: int) -> str:
    if selected_count >= 12:
        return "PUBLISHABLE"
    if selected_count >= 6:
        return "OK"
    if selected_count >= 1:
        return "THIN"
    return "HOLD"


def compiler_slice_recommendation(status: str, slice_family: str) -> str:
    family_label = "support-worker" if slice_family == "support-worker" else "service-admin"
    if status == "PUBLISHABLE":
        return f"Use as a live {family_label} slice."
    if status == "OK":
        return f"Usable {family_label} slice; keep an eye on depth."
    if status == "THIN":
        return f"Thin {family_label} slice; consider manual top-up before pushing hard."
    if status == "HOLD":
        return f"Hold {family_label} slice unless manually topped up."
    return f"Check data quality before using this {family_label} slice."


def compiler_slice_red_flags(status: str, selected_count: int, data_quality_flags: List[str]) -> str:
    if data_quality_flags:
        return compiler_red_flag_text(data_quality_flags)
    if status == "HOLD":
        return f"no selected jobs in selector output: {selected_count}"
    if status == "THIN":
        return f"low selected slice depth: {selected_count}"
    return "none"


def compiler_add_warning(
    rows: List[dict],
    month: str,
    run_date: str,
    warning_type: str,
    severity: str,
    finding: str,
    recommendation: str,
) -> None:
    rows.append({
        "section": "FEED_QA_WARNINGS",
        "report_month": month,
        "run_date": run_date,
        "warning_type": warning_type,
        "severity": severity,
        "finding": finding,
        "recommendation": recommendation,
    })


def compiler_headline(slice_rows: List[dict], qa_rows: List[dict]) -> str:
    status_by_slice = {
        (row.get("region"), row.get("slice_family")): row.get("status")
        for row in slice_rows
    }
    support_statuses = [
        status_by_slice.get(("West Yorkshire", "support-worker"), "HOLD"),
        status_by_slice.get(("South Yorkshire", "support-worker"), "HOLD"),
    ]
    admin_statuses = [
        status_by_slice.get(("West Yorkshire", "service-admin"), "HOLD"),
        status_by_slice.get(("South Yorkshire", "service-admin"), "HOLD"),
    ]
    admin_usable = any(status in {"PUBLISHABLE", "OK"} for status in admin_statuses)
    support_usable = any(status in {"PUBLISHABLE", "OK"} for status in support_statuses)

    if admin_usable and not support_usable:
        return "Admin-service slices look usable; support-worker remains thin"
    if support_usable and not admin_usable:
        return "Support-worker slices look usable; admin-service remains thin"
    if admin_usable and support_usable:
        medium_or_high = [row for row in qa_rows if row.get("severity") in {"HIGH", "MEDIUM"}]
        if medium_or_high:
            first = medium_or_high[0].get("warning_type", "feed QA").replace("_", " ").lower()
            return f"Live slices look usable; check {first}"
        return "Feed looks healthy for live Ontap slices"
    return "Live Ontap slices remain thin; hold or manually top up"


def compiler_overall_status(slice_rows: List[dict], qa_rows: List[dict]) -> str:
    if any(row.get("severity") == "HIGH" for row in qa_rows):
        return "INVESTIGATE"
    statuses = [row.get("status") for row in slice_rows]
    if any(status == "INVESTIGATE" for status in statuses):
        return "INVESTIGATE"
    if statuses and all(status == "HOLD" for status in statuses):
        return "HOLD"
    if any(status in {"HOLD", "THIN"} for status in statuses):
        return "THIN"
    if any(row.get("severity") == "MEDIUM" for row in qa_rows):
        return "OK"
    return "PUBLISHABLE"


def build_compiler_summary_from_outputs(
    all_jobs: pd.DataFrame,
    month: str,
    output_dir: Path,
) -> Tuple[pd.DataFrame, List[str], Dict[str, List[str]]]:
    """Build a traceable daily operating report from selector and profiler outputs.

    The detailed profiler CSVs remain unchanged. Live SLICE_DECISIONS use the
    final selector JSON files as their selected_count source of truth, while
    profiler counts remain as separated QA diagnostics for reconciliation.
    """
    warnings: List[str] = []
    trace: Dict[str, List[str]] = {
        "selected_count_sources": [],
        "profiler_count_sources": [],
        "reconciliation_warnings": [],
    }

    daily_path = output_dir / "daily" / f"{month}-daily-summary.csv"
    family_trends_path = output_dir / "monthly" / f"{month}-family-trends.csv"
    slice_viability_path = output_dir / "monthly" / f"{month}-slice-viability.csv"
    title_breadth_path = output_dir / "title-analysis" / f"{month}-title-breadth.csv"
    family_region_path = output_dir / "regional" / f"{month}-family-region-breakdown.csv"
    location_audit_path = output_dir / "regional" / f"{month}-regional-location-audit.csv"

    daily = read_profiler_csv(daily_path, warnings)
    family_trends = read_profiler_csv(family_trends_path, warnings)
    slice_viability = read_profiler_csv(slice_viability_path, warnings)
    title_breadth = read_profiler_csv(title_breadth_path, warnings)
    family_region_breakdown = read_profiler_csv(family_region_path, warnings)
    location_audit = read_profiler_csv(location_audit_path, warnings)

    daily_source = compiler_source_path(daily_path, output_dir)
    family_trends_source = compiler_source_path(family_trends_path, output_dir)
    slice_viability_source = compiler_source_path(slice_viability_path, output_dir)
    title_breadth_source = compiler_source_path(title_breadth_path, output_dir)
    family_region_source = compiler_source_path(family_region_path, output_dir)
    location_audit_source = compiler_source_path(location_audit_path, output_dir)
    trace["profiler_count_sources"].extend([
        family_region_source,
        family_trends_source,
        slice_viability_source,
    ])

    valid_dates = sorted(str(d) for d in all_jobs["date"].dropna().unique() if str(d) != "unknown_date")
    has_valid_dates = bool(valid_dates)
    run_date = valid_dates[-1] if has_valid_dates else date.today().isoformat()

    source_notes: List[str] = []
    if not daily.empty and "date" in daily.columns:
        known_daily = daily[daily["date"].astype(str) != "unknown_date"].copy()
        if not known_daily.empty:
            run_date = str(known_daily.sort_values("date").iloc[-1]["date"])
        elif "unknown_date" in set(daily["date"].astype(str)):
            source_notes.append("daily-summary contains unknown_date only; run_date uses current run date")

    raw_total_jobs = int(len(all_jobs))
    if not daily.empty and "total_jobs" in daily.columns:
        total_jobs = int(pd.to_numeric(daily["total_jobs"], errors="coerce").fillna(0).sum())
        if total_jobs != raw_total_jobs:
            source_notes.append(f"daily total {total_jobs} differs from profiler input rows {raw_total_jobs}")
    else:
        total_jobs = raw_total_jobs
        source_notes.append("daily-summary total unavailable; fell back to profiler input row count")

    total_support, support_total_notes = compiler_total_for_families_from_trends(
        family_trends, SUPPORT_WORKER_FAMILIES
    )
    total_admin, admin_total_notes = compiler_total_for_families_from_trends(
        family_trends, ADMIN_SERVICE_FAMILIES
    )

    raw_total_support = int(all_jobs["job_family"].isin(SUPPORT_WORKER_FAMILIES).sum())
    raw_total_admin = int(all_jobs["job_family"].isin(ADMIN_SERVICE_FAMILIES).sum())
    if total_support != raw_total_support:
        source_notes.append(f"support-worker family-trends total {total_support} differs from profiler input rows {raw_total_support}")
    if total_admin != raw_total_admin:
        source_notes.append(f"service-admin family-trends total {total_admin} differs from profiler input rows {raw_total_admin}")

    qa_rows: List[dict] = []
    for warning in warnings:
        warning_type = "missing_source_report" if "missing source report" in warning else "source_report_read_error"
        compiler_add_warning(
            qa_rows,
            month,
            run_date,
            warning_type,
            "HIGH",
            warning,
            "Profiler still generated this compiler CSV; check why the source report was unavailable.",
        )
        qa_rows[-1].update({
            "source_file": "compiler source-loader",
            "source_column": "n/a",
            "source_filter_used": "required compiler input report",
            "validation_note": "source/reconciliation issue",
        })

    if not daily.empty and {"date", "total_jobs"}.issubset(daily.columns):
        known_daily = daily[daily["date"].astype(str) != "unknown_date"].copy()
        if len(known_daily) >= 2:
            known_daily["total_jobs_numeric"] = pd.to_numeric(known_daily["total_jobs"], errors="coerce").fillna(0)
            latest = known_daily.sort_values("date").iloc[-1]
            earlier = known_daily.sort_values("date").iloc[:-1]
            earlier_max = float(earlier["total_jobs_numeric"].max()) if not earlier.empty else 0
            latest_total = float(latest["total_jobs_numeric"])
            if earlier_max > 0 and latest_total <= earlier_max * 0.6:
                compiler_add_warning(
                    qa_rows,
                    month,
                    run_date,
                    "sharp_feed_drop",
                    "HIGH",
                    f"Latest daily feed total is {int(latest_total)} versus earlier high {int(earlier_max)}.",
                    "Check whether the newest JobG8 export is incomplete before making publishing decisions.",
                )
                qa_rows[-1].update({
                    "source_file": daily_source,
                    "source_column": "date,total_jobs",
                    "source_filter_used": "date != unknown_date; latest daily row versus earlier max",
                    "validation_note": "daily total trend warning",
                })

    if not location_audit.empty and {"mapped_region", "raw_location", "total_count"}.issubset(location_audit.columns):
        audit = location_audit.copy()
        audit["total_count_numeric"] = pd.to_numeric(audit["total_count"], errors="coerce").fillna(0)
        unmapped_count = int(audit.loc[audit["mapped_region"].astype(str) == "Other / Unknown", "total_count_numeric"].sum())
        if total_jobs and unmapped_count / total_jobs >= UNMAPPED_LOCATION_WARNING_THRESHOLD:
            severity = "HIGH" if unmapped_count / total_jobs >= UNMAPPED_LOCATION_HIGH_THRESHOLD else "MEDIUM"
            compiler_add_warning(
                qa_rows,
                month,
                run_date,
                "high_unmapped_location_count",
                severity,
                f"{unmapped_count} of {total_jobs} jobs map to Other / Unknown.",
                "Review the geo lookup and add recurring unmapped places before relying on regional depth.",
            )
            qa_rows[-1].update({
                "source_file": location_audit_source,
                "source_column": "total_count",
                "source_filter_used": "mapped_region == Other / Unknown",
                "validation_note": "summed regional-location-audit unmapped rows",
            })
        yorkshire_count = int(audit.loc[audit["raw_location"].astype(str).str.lower() == "yorkshire", "total_count_numeric"].sum())
        if total_jobs and yorkshire_count / total_jobs >= 0.03:
            compiler_add_warning(
                qa_rows,
                month,
                run_date,
                "generic_yorkshire_location_count",
                "MEDIUM",
                f"{yorkshire_count} of {total_jobs} jobs use generic Yorkshire as the raw location.",
                "Check whether generic Yorkshire jobs can be mapped to West or South Yorkshire from title/company context.",
            )
            qa_rows[-1].update({
                "source_file": location_audit_source,
                "source_column": "total_count",
                "source_filter_used": "raw_location lower-case == yorkshire",
                "validation_note": "summed regional-location-audit generic Yorkshire rows",
            })

    if not title_breadth.empty:
        if {"normalised_title", "likely_family", "total_count"}.issubset(title_breadth.columns):
            title_candidates = title_breadth.copy()
            title_candidates["total_count_numeric"] = pd.to_numeric(title_candidates["total_count"], errors="coerce").fillna(0)
            title_candidates = title_candidates[
                title_candidates["likely_family"].astype(str).str.lower() != "unclassified"
            ]
            title_candidates = title_candidates.sort_values("total_count_numeric", ascending=False).head(1)
            if not title_candidates.empty:
                title_count = int(title_candidates.iloc[0]["total_count_numeric"])
                title_name = str(title_candidates.iloc[0].get("normalised_title", "")).strip()
                if total_jobs and title_count / total_jobs >= 0.08:
                    compiler_add_warning(
                        qa_rows,
                        month,
                        run_date,
                        "dominant_title_concentration",
                        "MEDIUM",
                        f"Non-unclassified title '{title_name}' accounts for {title_count} of {total_jobs} jobs.",
                        "Check whether a single title family is distorting the operating picture.",
                    )
                    qa_rows[-1].update({
                        "source_file": title_breadth_source,
                        "source_column": "normalised_title,likely_family,total_count",
                        "source_filter_used": "likely_family != unclassified; highest total_count",
                        "validation_note": "dominant title warning derived from title-breadth",
                    })
        if "top_companies" in title_breadth.columns:
            company_counter: Counter[str] = Counter()
            for value in title_breadth["top_companies"].dropna().astype(str):
                for company, count in re.findall(r"([^;()]+)\s+\((\d+)\)", value):
                    company_counter[company.strip()] += int(count)
            if company_counter:
                company, count = company_counter.most_common(1)[0]
                if total_jobs and count / total_jobs >= 0.15:
                    compiler_add_warning(
                        qa_rows,
                        month,
                        run_date,
                        "dominant_company_concentration",
                        "MEDIUM",
                        f"{company} accounts for {count} title/company appearances across {total_jobs} jobs.",
                        "Review whether one employer campaign is making the feed look deeper than it is.",
                    )
                    qa_rows[-1].update({
                        "source_file": title_breadth_source,
                        "source_column": "top_companies",
                        "source_filter_used": "parsed company counts from all title-breadth rows",
                        "validation_note": "dominant company warning derived from title-breadth",
                    })

    slice_specs = [
        ("West Yorkshire", "support-worker", SUPPORT_WORKER_FAMILIES),
        ("South Yorkshire", "support-worker", SUPPORT_WORKER_FAMILIES),
        ("West Yorkshire", "service-admin", ADMIN_SERVICE_FAMILIES),
        ("South Yorkshire", "service-admin", ADMIN_SERVICE_FAMILIES),
    ]
    slice_rows: List[dict] = []
    slice_counts: Dict[Tuple[str, str], int] = {}
    for region, slice_family, families in slice_specs:
        profiler_count, regional_note = compiler_number_from_regional_breakdown(
            family_region_breakdown, region, families
        )
        raw_region_jobs = all_jobs[all_jobs["region"] == region]
        raw_profiler_count = int(raw_region_jobs["job_family"].isin(families).sum())
        region_column = compiler_region_column(region)
        family_trend_region_count = 0
        family_trend_notes = []
        for family in families:
            value, note = compiler_number_from_family_trends(family_trends, family, region_column)
            family_trend_region_count += value
            family_trend_notes.append(f"{family}: {note}")

        validation_notes = [regional_note]
        if (
            regional_note == "no matching family-region rows found"
            and profiler_count == 0
            and raw_profiler_count == 0
            and family_trend_region_count == 0
        ):
            validation_notes = ["no matching family-region rows because the profiler slice count is zero"]

        profiler_source_issue = False
        if profiler_count == raw_profiler_count == family_trend_region_count:
            validation_notes.append("profiler_count validated against profiler input rows and monthly family-trends region column")
        else:
            profiler_source_issue = True
            validation_notes.append(
                f"profiler join/filter mismatch detected: family-region={profiler_count}, family-trends {region_column}={family_trend_region_count}, profiler input rows={raw_profiler_count}"
            )

        selector_path = compiler_selector_output_path(output_dir, region, slice_family)
        selected_count, count_source, selector_note, selector_source_issue = compiler_count_from_selector_json(
            selector_path, output_dir, warnings
        )
        trace["selected_count_sources"].append(f"{region} {slice_family}: {count_source}")

        today_count = compiler_today_count(all_jobs, run_date, has_valid_dates, region, families)
        if today_count == "":
            validation_notes.append("today_count unavailable because source export dates are unknown_date")
        else:
            validation_notes.append("today_count filtered from profiler input rows by date, region and family for QA context only")

        data_quality_flags: List[str] = []
        if selector_source_issue:
            data_quality_flags.append("selector output source issue")
        if profiler_source_issue:
            data_quality_flags.append("profiler source/mapping/classification issue")

        if not slice_viability.empty and {"region", "job_family", "viability"}.issubset(slice_viability.columns):
            region_viability = slice_viability[
                (slice_viability["region"].astype(str) == region)
                & (slice_viability["job_family"].astype(str).isin(families))
            ]
            drop_rows = region_viability[region_viability["viability"].astype(str).str.contains("month_end_drop", na=False)]
            if not drop_rows.empty:
                data_quality_flags.append("sharp feed drop for this slice")
        elif slice_viability.empty:
            validation_notes.append("slice-viability report has no dated slice rows for this month")

        reconciliation_note = compiler_reconciliation_note(
            selected_count, profiler_count, selector_note, profiler_source_issue, selector_source_issue
        )
        if selected_count != profiler_count or profiler_source_issue or selector_source_issue:
            trace["reconciliation_warnings"].append(
                f"{region} {slice_family}: selected_count={selected_count} ({count_source}); profiler_count={profiler_count} ({family_region_source}); {reconciliation_note}"
            )

        status = "INVESTIGATE" if selector_source_issue else compiler_slice_status(selected_count)
        row = {
            "section": "SLICE_DECISIONS",
            "report_month": month,
            "run_date": run_date,
            "region": region,
            "slice_family": slice_family,
            "month_to_date_count": selected_count,
            "today_count": today_count,
            "selected_count": selected_count,
            "selected_count_source_file": count_source,
            "profiler_count": profiler_count,
            "profiler_count_source_file": family_region_source,
            "reconciliation_note": reconciliation_note,
            "status": status,
            "recommendation": compiler_slice_recommendation(status, slice_family),
            "red_flags": compiler_slice_red_flags(status, selected_count, data_quality_flags),
            "source_file": f"selected_count={count_source}; profiler_count={family_region_source}; profiler QA cross-checks={family_trends_source}; {slice_viability_source}",
            "source_column": f"selector JSON list length for selected_count; family-region-breakdown.total_count for profiler_count QA; family-trends.{region_column}; slice-viability.viability; profiler input date/region/job_family for today_count",
            "source_filter_used": f"selected_count from final {slice_family} selector JSON for {region}; profiler QA region == {region}; likely_family/job_family in {', '.join(families)}",
            "validation_note": compiler_join_notes([selector_note] + validation_notes + family_trend_notes),
        }
        slice_rows.append(row)
        slice_counts[(region, slice_family)] = profiler_count

    reconciliation_rows: List[dict] = []
    reconciliation_specs = [
        ("support-worker", SUPPORT_WORKER_FAMILIES, total_support, support_total_notes),
        ("service-admin", ADMIN_SERVICE_FAMILIES, total_admin, admin_total_notes),
    ]
    for slice_family, families, total_count, total_notes in reconciliation_specs:
        tracked_count = sum(slice_counts.get((region, slice_family), 0) for region in TRACKED_ONTAP_REGIONS)
        other_region_columns = [compiler_region_column(region) for region in REGION_ORDER if region not in TRACKED_ONTAP_REGIONS]
        other_unknown_count = 0
        if not family_trends.empty:
            for family in families:
                rows = family_trends[family_trends["job_family"].astype(str) == family] if "job_family" in family_trends.columns else pd.DataFrame()
                if not rows.empty and "other_unknown" in rows.columns:
                    other_unknown_count += int(pd.to_numeric(rows["other_unknown"], errors="coerce").fillna(0).sum())
        outside_tracked = max(total_count - tracked_count, 0)
        generic_yorkshire_count = 0
        if not location_audit.empty and {"raw_location", "top_families", "total_count"}.issubset(location_audit.columns):
            audit_rows = location_audit[location_audit["raw_location"].astype(str).str.lower() == "yorkshire"]
            # The location audit provides family counts inside top_families, so use
            # those parsed counts where available instead of treating every generic
            # Yorkshire job as belonging to the family.
            for _, audit_row in audit_rows.iterrows():
                top_families = str(audit_row.get("top_families", ""))
                for family in families:
                    match = re.search(rf"{re.escape(family)}\s+\((\d+)\)", top_families)
                    if match:
                        generic_yorkshire_count += int(match.group(1))

        family_columns = ",".join(["total_jobs"] + [compiler_region_column(region) for region in TRACKED_ONTAP_REGIONS] + other_region_columns + ["other_unknown"])
        if tracked_count + outside_tracked != total_count:
            compiler_add_warning(
                qa_rows,
                month,
                run_date,
                f"{slice_family}_regional_reconciliation_mismatch".replace("-", "_"),
                "HIGH",
                f"{slice_family} total {total_count} does not reconcile with tracked {tracked_count} plus outside tracked {outside_tracked}.",
                "Inspect compiler source trace columns for a source/reconciliation issue before using this slice decision.",
            )
            qa_rows[-1].update({
                "source_file": f"{family_trends_source}; {family_region_source}",
                "source_column": "family-trends.total_jobs; family-region-breakdown.total_count",
                "source_filter_used": f"families in {', '.join(families)}; tracked regions {', '.join(TRACKED_ONTAP_REGIONS)}",
                "validation_note": "source/reconciliation issue",
            })

        explanation = (
            f"{slice_family} jobs exist but not in tracked West/South Yorkshire"
            if total_count > 0 and tracked_count == 0
            else "tracked regional count reconciled to month-to-date total"
        )
        compiler_add_reconciliation_row(
            reconciliation_rows, month, run_date, slice_family,
            f"total {slice_family} jobs month-to-date", total_count,
            family_trends_source, "total_jobs",
            f"job_family in {', '.join(families)}",
            compiler_join_notes(total_notes + ["validated against profiler input family counts"]),
        )
        compiler_add_reconciliation_row(
            reconciliation_rows, month, run_date, slice_family,
            f"{slice_family} jobs in tracked Ontap regions", tracked_count,
            f"{family_region_source}; {family_trends_source}",
            "family-region-breakdown.total_count; family-trends west_yorkshire,south_yorkshire",
            f"regions in {', '.join(TRACKED_ONTAP_REGIONS)}; families in {', '.join(families)}",
            explanation,
        )
        compiler_add_reconciliation_row(
            reconciliation_rows, month, run_date, slice_family,
            f"{slice_family} jobs outside tracked Ontap regions", outside_tracked,
            family_trends_source, family_columns,
            f"total_jobs minus tracked Ontap regions for families in {', '.join(families)}",
            f"outside tracked includes other Ontap regions and Other / Unknown; family-trends other_unknown contributes {other_unknown_count}",
        )
        compiler_add_reconciliation_row(
            reconciliation_rows, month, run_date, slice_family,
            f"unmapped/generic Yorkshire {slice_family} jobs", generic_yorkshire_count,
            location_audit_source, "raw_location,top_families,total_count",
            f"raw_location lower-case == yorkshire; parsed top_families for {', '.join(families)}",
            "available from regional-location-audit top_families; 0 means no matching family listed for generic Yorkshire",
        )

    overall_status = compiler_overall_status(slice_rows, qa_rows)
    headline = compiler_headline(slice_rows, qa_rows)
    main_red_flags = compiler_red_flag_text([
        row.get("finding", "") for row in qa_rows if row.get("severity") in {"HIGH", "MEDIUM"}
    ])

    executive_validation_notes = source_notes + support_total_notes + admin_total_notes
    executive_row = {
        "section": "EXECUTIVE_SUMMARY",
        "report_month": month,
        "run_date": run_date,
        "total_jobs_month_to_date": total_jobs,
        "total_support_worker_jobs": total_support,
        "total_admin_service_jobs": total_admin,
        "overall_status": overall_status,
        "headline_recommendation": headline,
        "main_red_flags": main_red_flags,
        "source_file": f"{daily_source}; {family_trends_source}; {family_region_source}; {location_audit_source}; {title_breadth_source}",
        "source_column": "daily-summary.total_jobs; family-trends.total_jobs; family-trends regional columns; family-region-breakdown.total_count; regional-location-audit total_count/top_families; title-breadth top_companies,total_count",
        "source_filter_used": f"month == {month}; support-worker families: {', '.join(SUPPORT_WORKER_FAMILIES)}; service-admin families: {', '.join(ADMIN_SERVICE_FAMILIES)}",
        "validation_note": compiler_join_notes(executive_validation_notes + ["executive totals read from existing profiler reports and cross-checked against profiler input rows"]),
    }

    rows = [executive_row] + slice_rows + reconciliation_rows + qa_rows
    return pd.DataFrame(rows, columns=COMPILER_SUMMARY_COLUMNS), warnings, trace

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
            "is_active_ontap_slice_region": "yes" if region in ACTIVE_ONTAP_SLICE_REGIONS else "no",
            "raw_location": loc,
            "raw_jobg8_area": top_values(group["jobg8_area"], limit=3) if "jobg8_area" in group.columns else "",
            "raw_jobg8_location": top_values(group["jobg8_location"], limit=3) if "jobg8_location" in group.columns else "",
            "match_source": match_source,
            "match_place": match_place,
            "total_count": len(group),
            "unique_companies": unique_nonblank_count(group["company"]),
            "top_titles": top_values(group["normalised_title"], limit=6),
            "top_families": top_values(group["job_family"], limit=6),
        })

    if not rows:
        return pd.DataFrame(columns=[
            "month", "mapped_region", "is_active_ontap_slice_region", "raw_location", "raw_jobg8_area", "raw_jobg8_location",
            "match_source", "match_place", "total_count", "unique_companies", "top_titles", "top_families"
        ])

    return pd.DataFrame(rows).sort_values(
        ["mapped_region", "total_count", "raw_location"], ascending=[True, False, True]
    )



def _suspected_region_from_known_terms(text: object) -> Tuple[str, str]:
    lookup_text = normalise_lookup_place(text)
    if not lookup_text:
        return "", ""

    for region in REGION_ORDER:
        for place in sorted(REGION_KEYWORDS.get(region, []), key=len, reverse=True):
            place_text = normalise_lookup_place(place)
            pattern = r"(?<![a-z0-9])" + re.escape(place_text) + r"(?![a-z0-9])"
            if re.search(pattern, lookup_text):
                return region, f"target-region town term '{place}' appears in raw location"
    return "", ""


def _suspected_region_from_context(group: pd.DataFrame) -> Tuple[str, str]:
    context = " ".join(
        (
            group.get(column, pd.Series(dtype=str)).fillna("").astype(str).str.cat(sep=" ")
            if column in group.columns else ""
        )
        for column in ["title", "description"]
    )
    return _suspected_region_from_known_terms(context[:5000])


def build_geo_unmapped_review(all_jobs: pd.DataFrame, month: str) -> pd.DataFrame:
    """Material geo QA rows for lookup workbook review, not an auto-write stage.

    Valid UK towns/cities/counties are proposed for the UK-wide shared lookup,
    even when Ontap does not currently publish an active slice there. The selector
    and compiler decide later whether a mapped place belongs to an active slice.
    """
    columns = [
        "month",
        "raw_location",
        "raw_jobg8_area",
        "raw_jobg8_location",
        "suspected_region",
        "suspected_reason",
        "job_family_counts",
        "total_count",
        "unique_companies",
        "top_titles",
        "recommended_action",
        "suggested_lookup_area",
        "suggested_lookup_cluster",
        "confidence",
    ]
    rows = []
    target_families = set(SUPPORT_WORKER_FAMILIES + ADMIN_SERVICE_FAMILIES)

    group_cols = ["region", "location", "region_match_source", "region_match_place"]
    for (region, location, match_source, match_place), group in all_jobs.groupby(group_cols, dropna=False):
        raw_location = str(location).strip() if str(location).strip() else "blank_location"
        loc_norm = normalise_lookup_place(raw_location)
        family_counts = Counter(str(value) for value in group["job_family"].fillna(""))
        target_family_count = sum(family_counts.get(family, 0) for family in target_families)
        total_count = len(group)
        is_unmapped = region == "Other / Unknown" or match_source == "unmapped"
        is_broad = is_broad_ambiguous_location(raw_location)
        suspected_region, suspected_reason = _suspected_region_from_known_terms(raw_location)
        uk_cluster, uk_reason = _uk_geo_suggestion_from_group(raw_location, group)
        is_bad_or_non_uk, bad_or_non_uk_reason = _looks_non_uk_or_bad(raw_location, group)
        recommended_action = ""
        confidence = ""

        if not suspected_region and is_broad:
            suspected_region, suspected_reason = _suspected_region_from_context(group)
            if suspected_region:
                suspected_reason = f"broad/ambiguous location; {suspected_reason} in title/description"

        suspicious_mapping = False
        match_norm = normalise_lookup_place(match_place)
        if region != "Other / Unknown" and match_norm and loc_norm and loc_norm != match_norm:
            match_tokens = match_norm.split()
            if len(match_tokens) == 1 and re.search(r"(?<![a-z0-9])" + re.escape(match_norm) + r"\s+(st\.?|saint)\b", loc_norm):
                suspicious_mapping = True
                suspected_reason = f"short lookup match '{match_place}' may be a different longer place in raw location"
                suspected_region = ""

        if suspicious_mapping:
            recommended_action = "FIX_EXISTING_LOOKUP"
            confidence = "medium"
        elif is_bad_or_non_uk:
            recommended_action = "IGNORE_BAD_OR_NON_UK"
            confidence = "medium"
            suspected_reason = suspected_reason or bad_or_non_uk_reason
        elif is_unmapped and is_broad:
            recommended_action = "AMBIGUOUS_REVIEW"
            confidence = "medium"
            suspected_reason = suspected_reason or "broad/ambiguous location; do not add blindly"
        elif is_unmapped and suspected_region:
            recommended_action = (
                "ADD_TO_LOOKUP_ACTIVE_REGION"
                if suspected_region in TRACKED_ONTAP_REGIONS
                else "ADD_TO_LOOKUP_OUTSIDE_ACTIVE_SLICE"
            )
            confidence = "high"
        elif is_unmapped and uk_cluster:
            # Valid UK places outside currently active Ontap slices should still be
            # proposed for the UK-wide lookup rather than ignored, unless the raw
            # value is county-only or a known risky place that needs human QA.
            suspected_region = uk_cluster
            suspected_reason = uk_reason
            needs_human_geo_review = loc_norm in COUNTY_ONLY_REVIEW_TERMS or loc_norm in RISKY_AMBIGUOUS_PLACE_TERMS
            recommended_action = "AMBIGUOUS_REVIEW" if needs_human_geo_review else "ADD_TO_LOOKUP_OUTSIDE_ACTIVE_SLICE"
            confidence = "medium" if needs_human_geo_review else "high"
        elif is_unmapped and target_family_count:
            recommended_action = "AMBIGUOUS_REVIEW"
            confidence = "low"
            suspected_reason = suspected_reason or "unmapped UK possibility connected to support-worker/admin-service families; needs human geo review"
        elif is_broad and suspected_region:
            recommended_action = "AMBIGUOUS_REVIEW"
            confidence = "medium"

        if not recommended_action:
            continue

        if not (target_family_count or suspected_region or suspicious_mapping or is_broad or is_bad_or_non_uk or total_count >= 2):
            continue

        suggested_lookup_area = "" if recommended_action in {"FIX_EXISTING_LOOKUP", "AMBIGUOUS_REVIEW", "IGNORE_BAD_OR_NON_UK"} else raw_location
        suggested_lookup_cluster = suspected_region if recommended_action in {"ADD_TO_LOOKUP_ACTIVE_REGION", "ADD_TO_LOOKUP_OUTSIDE_ACTIVE_SLICE"} else ""

        rows.append({
            "month": month,
            "raw_location": raw_location,
            "raw_jobg8_area": top_values(group["jobg8_area"], limit=3) if "jobg8_area" in group.columns else "",
            "raw_jobg8_location": top_values(group["jobg8_location"], limit=3) if "jobg8_location" in group.columns else "",
            "suspected_region": suspected_region,
            "suspected_reason": suspected_reason,
            "job_family_counts": "; ".join(f"{family}: {count}" for family, count in family_counts.most_common() if family),
            "total_count": total_count,
            "unique_companies": unique_nonblank_count(group["company"]),
            "top_titles": top_values(group["normalised_title"], limit=8),
            "recommended_action": recommended_action,
            "suggested_lookup_area": suggested_lookup_area,
            "suggested_lookup_cluster": suggested_lookup_cluster,
            "confidence": confidence,
        })

    if not rows:
        return pd.DataFrame(columns=columns)

    action_order = {
        "FIX_EXISTING_LOOKUP": 0,
        "ADD_TO_LOOKUP_ACTIVE_REGION": 1,
        "ADD_TO_LOOKUP_OUTSIDE_ACTIVE_SLICE": 2,
        "AMBIGUOUS_REVIEW": 3,
        "IGNORE_BAD_OR_NON_UK": 4,
    }
    return (
        pd.DataFrame(rows, columns=columns)
        .assign(_action_sort=lambda df: df["recommended_action"].map(action_order).fillna(9))
        .sort_values(["_action_sort", "total_count", "raw_location"], ascending=[True, False, True])
        .drop(columns=["_action_sort"])
    )


def build_geo_lookup_qa_summary(geo_mapper: GeoMapper, geo_unmapped_review: pd.DataFrame, all_jobs: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Summarise lookup coverage and proposal actions for the latest geo QA review."""
    action_counts = Counter()
    if not geo_unmapped_review.empty and "recommended_action" in geo_unmapped_review.columns:
        if hasattr(geo_unmapped_review, "_rows"):
            action_counts = Counter(str(row.get("recommended_action") or "") for row in geo_unmapped_review._rows)
        else:
            action_counts = Counter(str(action) for action in geo_unmapped_review["recommended_action"].fillna(""))

    total_rows = len(all_jobs) if all_jobs is not None else 0
    if all_jobs is not None and not all_jobs.empty:
        active_mapped_count = int((all_jobs["is_active_ontap_slice_region"] == "yes").sum())
        known_inactive_mapped_count = int(((all_jobs["region"] != "Other / Unknown") & (all_jobs["is_active_ontap_slice_region"] != "yes")).sum())
        genuinely_unmapped_ambiguous_count = int((all_jobs["region"] == "Other / Unknown").sum())
    else:
        active_mapped_count = 0
        known_inactive_mapped_count = 0
        genuinely_unmapped_ambiguous_count = 0

    columns = [
        "lookup_file_path",
        "mapped_lookup_row_count",
        "unique_lookup_key_count",
        "total_rows_profiled",
        "active_ontap_region_mapped_count",
        "known_uk_inactive_region_mapped_count",
        "genuinely_unmapped_ambiguous_count",
        "geo_unmapped_review_row_count",
        "ADD_TO_LOOKUP_ACTIVE_REGION_count",
        "ADD_TO_LOOKUP_OUTSIDE_ACTIVE_SLICE_count",
        "AMBIGUOUS_REVIEW_count",
        "FIX_EXISTING_LOOKUP_count",
        "IGNORE_BAD_OR_NON_UK_count",
    ]
    row = {
        "lookup_file_path": display_geo_lookup_path(geo_mapper.lookup_path),
        "mapped_lookup_row_count": geo_mapper.lookup_mapped_row_count,
        "unique_lookup_key_count": len(geo_mapper.place_to_region),
        "total_rows_profiled": total_rows,
        "active_ontap_region_mapped_count": active_mapped_count,
        "known_uk_inactive_region_mapped_count": known_inactive_mapped_count,
        "genuinely_unmapped_ambiguous_count": genuinely_unmapped_ambiguous_count,
        "geo_unmapped_review_row_count": len(geo_unmapped_review),
    }
    row.update({f"{action}_count": action_counts.get(action, 0) for action in GEO_REVIEW_ACTIONS})
    return pd.DataFrame([row], columns=columns)



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

    area_columns = []
    location_columns = []
    for path in files:
        try:
            header_df = pd.read_excel(path, engine="openpyxl", nrows=0)
        except TypeError:
            header_df = pd.read_excel(path, nrows=0)
        except Exception:
            continue
        area_col, location_col = find_region_mapping_columns(header_df)
        if area_col and area_col not in area_columns:
            area_columns.append(area_col)
        if location_col and location_col not in location_columns:
            location_columns.append(location_col)

    region_match_source_counts = top_values(all_jobs["region_match_source"], limit=10)
    other_unknown_count = int((all_jobs["region"] == "Other / Unknown").sum())
    other_unknown_ratio = (other_unknown_count / len(all_jobs)) if len(all_jobs) else 0
    expected_lookup_checks = [
        "Leeds", "Bradford", "Wakefield", "Huddersfield", "Halifax",
        "Sheffield", "Rotherham", "Doncaster", "Barnsley",
    ]
    lookup_check_results = []
    for place in expected_lookup_checks:
        region, matched_place = geo_mapper.lookup_match(place)
        lookup_check_results.append(f"{place}->{region or 'unmapped'} via {matched_place or 'no lookup match'}")

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
    geo_unmapped_review_path = regional_dir / f"{month}-geo-unmapped-review.csv"
    geo_unmapped_review = build_geo_unmapped_review(all_jobs, month)
    geo_unmapped_review.to_csv(
        geo_unmapped_review_path, index=False
    )
    geo_lookup_qa_summary_path = regional_dir / f"{month}-geo-lookup-qa-summary.csv"
    geo_lookup_qa_summary = build_geo_lookup_qa_summary(geo_mapper, geo_unmapped_review, all_jobs)
    geo_lookup_qa_summary.to_csv(geo_lookup_qa_summary_path, index=False)
    compiler_summary_path = compiler_dir / f"{month}-compiler-summary.csv"
    compiler_summary, compiler_warnings, compiler_trace = build_compiler_summary_from_outputs(
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
        f"Default geo lookup path: {DEFAULT_GEO_LOOKUP_DISPLAY_PATH}",
        f"Resolved geo lookup path: {geo_lookup}",
        f"Geo lookup file exists: {'yes' if geo_lookup_exists else 'no'}",
        f"Geo lookup status: {geo_lookup_status}",
        f"Geo lookup rows in workbook: {geo_mapper.lookup_source_rows}",
        f"Geo lookup unique mapped keys loaded: {len(geo_mapper.place_to_region)}",
        f"Fallback keyword rules used: {fallback_status}",
        f"Region mapping town/area source columns: {', '.join(area_columns) if area_columns else 'none found'}",
        f"Region mapping fallback location columns: {', '.join(location_columns) if location_columns else 'none found'}",
        f"Region match source counts: {region_match_source_counts}",
        f"Other / Unknown region count: {other_unknown_count} of {len(all_jobs)} ({other_unknown_ratio:.1%})",
        f"Other / Unknown warning threshold: {UNMAPPED_LOCATION_WARNING_THRESHOLD:.0%}",
        "Lookup verification checks: " + "; ".join(lookup_check_results),
        "",
        "Geo lookup QA summary:",
        *[f"- {column}: {geo_lookup_qa_summary.iloc[0][column]}" for column in geo_lookup_qa_summary.columns],
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
        f"- {geo_unmapped_review_path}",
        f"- {geo_lookup_qa_summary_path}",
        f"- {compiler_summary_path}",
        "",
        f"Traceable compiler summary generated with reconciliation/source tracing: {compiler_summary_path}",
        "",
        "Compiler selected_count source files by live slice:",
        *[f"- {source}" for source in dict.fromkeys(compiler_trace.get("selected_count_sources", []))],
        "",
        "Compiler profiler_count diagnostic files:",
        *[f"- {source}" for source in dict.fromkeys(compiler_trace.get("profiler_count_sources", []))],
    ]

    if compiler_trace.get("reconciliation_warnings"):
        log_lines.extend(["", "Compiler reconciliation warnings:"])
        log_lines.extend(f"- {warning}" for warning in compiler_trace["reconciliation_warnings"])

    if errors:
        log_lines.extend(["", "Files with errors:"])
        log_lines.extend(f"- {e}" for e in errors)

    if compiler_warnings:
        log_lines.extend(["", "Compiler summary warnings:"])
        log_lines.extend(f"- {warning}" for warning in compiler_warnings)

    if other_unknown_ratio >= UNMAPPED_LOCATION_WARNING_THRESHOLD:
        log_lines.extend([
            "",
            "Region mapping QA warning:",
            f"- {other_unknown_count} of {len(all_jobs)} jobs ({other_unknown_ratio:.1%}) still map to Other / Unknown after lookup mapping.",
        ])

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


"""
Ontap Phase-1: JobG8 CSV/XLSX -> support-worker JSON pipeline

V_12 rollback:
- simple support-worker selector process only
- writes to output-support-worker/
- produces named support-worker reports and West/South Yorkshire JSON only
- no below-6 comparator, no archive-runs, no comparison-output, no live-json update

V11_5 additions:
- secondary salary fallback: if structured JobG8 salary fields are blank, extract only explicit £ salary phrases from /Job/Description; never infer or fabricate salary

V12_6 fix:
- lookup file selection now mirrors the working admin/service script: use /input/lookup.xlsx only
- Geo lookup sheet beside the script is ignored for this support-worker run
- report ordering remains report-only; no selection count-fill

V12_3 additions:
- separate selection-summary-report.csv for quick per-region QA

V11 additions:
- expanded North-of-England regional selection: West Yorkshire, South Yorkshire, Lancashire, Greater Manchester, Cumbria, North East

V10 additions:
- daily selection scenario reporting for West/South Yorkshire
- manual_select = 1 for Scenario 3 candidate fill
- anchor-town selection logic before cap

V9 additions:
- title classification layer for Support Worker slices
- HIGH_CONFIDENCE / ELASTIC_FIT / REVIEW_CONTEXT_DEPENDENT / HARD_PASS
- optional support_worker_title_classification_register.csv exact-title lookup
- hard-pass titles remain hard-pass even with FORCE_INCLUDE
- elastic titles can fill thin slices after high-confidence titles

Input folder:
  input/   put ONE JobG8 export and ONE region lookup file here

Output folder:
  output-support-worker/decision-report-support-worker.csv
  output-support-worker/validation-report-support-worker.csv
  output-support-worker/selection-summary-report-support-worker.csv
  output-support-worker/west-yorkshire-support-worker.json
  output-support-worker/south-yorkshire-support-worker.json


Run:
  python3 jobg8_to_ontap_json_V_12.py

"""
from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import pandas as pd

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output-support-worker")
DECISION_REPORT_PATH = OUTPUT_DIR / "decision-report-support-worker.csv"
MANUAL_DIR = Path("manual")
MANUAL_REVIEW_CSV_PATH = MANUAL_DIR / "support-worker-review.csv"
MANUAL_REVIEW_MD_PATH = MANUAL_DIR / "support-worker-review.md"
# Backwards-compatible alias for older helper code.
MANUAL_REVIEW_PATH = MANUAL_REVIEW_CSV_PATH
MANUAL_REVIEW_FIELDNAMES = [
    "decision",
    "region",
    "title",
    "town",
    "salary_text",
    "manual_override",
    "manual_select",
    "job_id",
]

JOB_FILE_KEYWORDS = ["jobg8", "jobs"]
LOOKUP_FILE_KEYWORDS = ["lookup", "region", "town"]
TITLE_REGISTER_FILE_KEYWORDS = ["support_worker_title_classification_register", "title_classification_register"]

# Locked source columns from the real JobG8 export checked on 30-04
COL = {
    "job_id": "/Job/DisplayReference",
    "title": "/Job/Position",
    "advertiser_name": "/Job/AdvertiserName",
    "advertiser_type": "/Job/AdvertiserType",
    "employment_type": "/Job/EmploymentType",
    "area": "/Job/Area",
    "apply_url": "/Job/ApplicationURL",
    "description": "/Job/Description",
    "salary_min": "/Job/SalaryMinimum",
    "salary_max": "/Job/SalaryMaximum",
    "salary_period": "/Job/SalaryPeriod",
    "salary_additional": "/Job/SalaryAdditional",
}

# There was no /Job/PostedDate column in the sample export. Keep blank unless JobG8 adds it later.
OPTIONAL_POSTED_DATE_COLUMNS = ["/Job/PostedDate", "/Job/Posted", "/Job/DatePosted"]

REQUIRED_COLUMNS = [
    COL["job_id"],
    COL["title"],
    COL["advertiser_name"],
    COL["advertiser_type"],
    COL["employment_type"],
    COL["area"],
    COL["apply_url"],
    COL["description"],
]

INCLUDE_TERMS = [
    "support worker",
    "care assistant",
    "healthcare assistant",
]

EXCLUDE_TERMS = [
    "senior",
    "manager",
    "nurse",
    "driver",
    "teacher",
    "semh",
    "housing",
]

REGION_MAP = {
    # Existing V10_3 regions
    "yorkshire (west)": "West Yorkshire",
    "yorkshire west": "West Yorkshire",
    "west yorkshire": "West Yorkshire",
    "yorkshire (south)": "South Yorkshire",
    "yorkshire south": "South Yorkshire",
    "south yorkshire": "South Yorkshire",

    # V11 North expansion regions. These map lookup.xlsx Cluster values to clean internal region names.
    "lancashire": "Lancashire",
    "greater manchester": "Greater Manchester",
    "manchester": "Greater Manchester",
    "cumbria": "Cumbria",

    # V11_4: split the old combined North East region into three publishable sub-regions.
    "north east - tyneside, wearside & northumberland": "North East - Tyneside, Wearside & Northumberland",
    "tyneside, wearside & northumberland": "North East - Tyneside, Wearside & Northumberland",
    "tyneside wearside northumberland": "North East - Tyneside, Wearside & Northumberland",
    "north east - county durham & darlington/hartlepool": "North East - County Durham & Darlington/Hartlepool",
    "county durham & darlington/hartlepool": "North East - County Durham & Darlington/Hartlepool",
    "county durham darlington hartlepool": "North East - County Durham & Darlington/Hartlepool",
    "north east - tees valley": "North East - Tees Valley",
    "tees valley": "North East - Tees Valley",
}

OUTPUT_FILES = {
    "West Yorkshire": "west-yorkshire-support-worker.json",
    "South Yorkshire": "south-yorkshire-support-worker.json",
}

REGION_CAPS = {
    "West Yorkshire": 12,
    "South Yorkshire": 12,
}

ANCHOR_TOWNS = {
    "West Yorkshire": "Leeds",
    "South Yorkshire": "Sheffield",
}

PUBLISH_THRESHOLDS = {
    "West Yorkshire": 6,
    "South Yorkshire": 6,
}

POSSIBLE_SELECTION_REVIEW_COUNT = 6


CLASSIFICATION_PRIORITY = {
    "HIGH_CONFIDENCE": 1,
    "ELASTIC_FIT": 2,
    "REVIEW_CONTEXT_DEPENDENT": 50,
    "HARD_PASS": 99,
    "OUT_OF_SCOPE": 99,
}

# Stable hard-pass title patterns from the support-worker title register.
# These are excluded even if the slice is thin.
HARD_PASS_PATTERNS = [
    "senior", "lead", "team leader", "deputy", "manager", "coordinator", "officer",
    "housing", "homeless", "homelessness", "tenancy", "night concierge",
    "driver", "drivers", "transport", "minibus",
    "school", "sen ", "send", "semh", "teacher", "teaching", "aln", "lsa", "ta ", "teaching assistant",
    "nurse", "therapist", "social worker", "counsellor", "counselor", "psychologist",
    "admin", "administrator", "administration", "business support", "sales support", "it support", "project support",
]

# Stable high-confidence title patterns from the support-worker title register.
HIGH_CONFIDENCE_PATTERNS = [
    "support worker", "support workers",
    "care assistant", "care worker", "healthcare assistant", "health care assistant",
    "healthcare support worker", "health care support worker", "homecare assistant", "home care assistant",
    "personal assistant", "community care assistant", "community care worker",
]

# Elastic-fit patterns: not core enough to outrank high-confidence titles,
# but plausible enough to fill a thin slice when there are not enough HC roles.
ELASTIC_FIT_PATTERNS = [
    "residential support worker", "mental health support worker", "learning disability support worker",
    "waking night support worker", "bank support worker", "relief support worker",
    "recovery support worker", "outreach support worker", "female support worker", "male support worker",
]

# Exact review titles from the register. These stay manual/context-dependent until settled.
REVIEW_CONTEXT_DEPENDENT_TITLES = {
    "autism support assistant",
    "bank residential care worker",
    "behavior support assistant - slough",
    "behavior support assistant - wantage",
    "behaviour support assistant",
    "behaviour support assistant - oxford",
    "behaviour support assistant (challenging behaviour)",
    "casual family support worker",
    "challenging behaviour support assistant",
    "child & youth support worker",
    "childlren and young people support worker",
    "children and young people support worker",
    "children and young people support worker - family supervision",
    "children and young people support worker - mental health",
    "children and young peoples learning support worker (autism)",
    "children and young persons support worker",
    "childrens residential care worker",
    "crisis recovery worker",
    "family assessment support worker",
    "family support worker",
    "family support worker, trafford council",
    "family support worker, wakefield council",
    "learning support worker",
    "peebles - relief support practitioners",
    "recovery worker",
    "residential care worker",
    "residential care worker children - assessment home",
    "residential care worker children's",
    "support practitioner",
    "therapeutic residential childcare worker",
    "therapy support assistant",
    "waking night childcare worker",
    "waking night recovery worker",
    "young people support worker",
    "young person support worker",
    "young person support worker wiltshire leaving care",
    "youth support worker",
    "youth support worker - oxford",
    "youth support worker - reading",
}


def fix_encoding(value: Any) -> Any:
    """
    Repair common mojibake from UTF-8 text misread as Windows/Latin-1.

    Examples fixed:
      Â£ -> £
      â€“ -> –
      â€™ -> '
      CafÃ© -> Café
    """
    if not isinstance(value, str):
        return value

    text = value

    def marker_score(s: str) -> int:
        markers = ["Â", "â", "Ã", "�", "¢", "€"]
        return sum(s.count(m) for m in markers)

    # Try latin1/cp1252 -> utf-8 repair twice to catch double-encoded text.
    for _ in range(2):
        for enc in ("latin1", "cp1252"):
            try:
                repaired = text.encode(enc, errors="strict").decode("utf-8", errors="strict")
                if marker_score(repaired) < marker_score(text):
                    text = repaired
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass

    replacements = {
        "Â£": "£",
        "Â": "",
        "â€“": "–",
        "â€”": "—",
        "â€˜": "'",
        "â€™": "'",
        "â€œ": '"',
        "â€�": '"',
        "â€": '"',
        "â€¢": "•",
        "â€¦": "...",
        "Ã©": "é",
        "Ã¨": "è",
        "Ã¡": "á",
        "Ã ": "à",
        "Ã¶": "ö",
        "Ã¼": "ü",
        "Ã±": "ñ",
        "&nbsp;": " ",
    }

    for bad, good in replacements.items():
        text = text.replace(bad, good)

    return text
    """
    Repair common mojibake from UTF-8 text misread as Windows/Latin-1/CP1252.

    Keeps already-correct Unicode such as Café unchanged, while repairing cases like:
      CafÃ© -> Café
      Â£    -> £
      â€“   -> –
      â€¢   -> •
    """
    if not isinstance(value, str):
        return value

    text = value

    def mojibake_score(s: str) -> int:
        markers = [
            "Â", "Ã", "â€", "â€“", "â€”", "â€¢", "â€¦", "â?", "�",
            "Ã¢", "â€˜", "â€™", "â€œ", "â€�",
        ]
        return sum(s.count(marker) for marker in markers)

    # Try the common repair routes, but only accept a candidate if it reduces
    # mojibake markers. This avoids damaging already-correct accented text.
    candidates = [text]
    for source_encoding in ("latin1", "cp1252"):
        try:
            candidates.append(text.encode(source_encoding).decode("utf-8"))
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass

    text = min(candidates, key=mojibake_score)

    # Safety-net replacements for common JobG8/export artefacts that may not
    # round-trip cleanly through encode/decode repair.
    replacements = {
        "Â£": "£",
        "Â ": " ",
        "Â": "",
        "â€“": "–",
        "â€”": "—",
        "â€˜": "'",
        "â€™": "'",
        "â€œ": '"',
        "â€�": '"',
        "â€": '"',
        "â€¢": "•",
        "â€¦": "...",
        "Ã©": "é",
        "Ã¨": "è",
        "Ã¡": "á",
        "Ãà": "à",
        "Ã ": "à",
        "Ã¶": "ö",
        "Ã¼": "ü",
        "Ã±": "ñ",
        "Ã¢": "â",
        "&nbsp;": " ",
        "\u00a0": " ",
    }

    for bad, good in replacements.items():
        text = text.replace(bad, good)

    return text

def clean_string(value: Any) -> str:
    return fix_encoding(norm(value))


def clean_record_strings(item: dict[str, Any]) -> dict[str, Any]:
    """Apply encoding cleanup to every string field in a JSON object."""
    cleaned: dict[str, Any] = {}
    for key, value in item.items():
        cleaned[key] = fix_encoding(value) if isinstance(value, str) else value
    return cleaned


def norm(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return fix_encoding(str(value).strip())


def norm_key(value: Any) -> str:
    return re.sub(r"\s+", " ", norm(value).lower())


class DescriptionCleaner(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0
        self.in_li = False

    def _append_break(self) -> None:
        if self.parts and not self.parts[-1].endswith("\n"):
            self.parts.append("\n")

    def _append_block_break(self) -> None:
        if not self.parts:
            return
        joined = "".join(self.parts)
        if joined.endswith("\n\n"):
            return
        if joined.endswith("\n"):
            self.parts.append("\n")
        else:
            self.parts.append("\n\n")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()

        if tag in {"script", "style", "noscript"}:
            self.skip_depth += 1
            return

        if self.skip_depth:
            return

        # Drop tracking pixels / invisible image tags entirely.
        if tag == "img":
            return

        if tag == "li":
            self._append_break()
            self.parts.append("- ")
            self.in_li = True
            return

        if tag == "br":
            self._append_break()
            return

        # Avoid creating paragraph gaps inside list items such as <li><p>Text</p></li>.
        if self.in_li and tag in {"p", "div"}:
            return

        if tag in {"p", "div", "section", "article", "h1", "h2", "h3", "h4"}:
            self._append_block_break()

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        if tag in {"script", "style", "noscript"} and self.skip_depth:
            self.skip_depth -= 1
            return

        if self.skip_depth:
            return

        if tag == "li":
            self.in_li = False
            self._append_break()
            return

        if self.in_li and tag in {"p", "div"}:
            return

        if tag in {"p", "div", "section", "article", "h1", "h2", "h3", "h4", "ul", "ol"}:
            self._append_block_break()

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return

        text = fix_encoding(unescape(data))
        text = text.replace("\u00a0", " ")

        # Inline bullet separators from pasted HTML/email markup.
        # Keep compact list breaks rather than rendering literal corrupted bullets.
        text = re.sub(r"\s*(?:[•·▪■◦]|â€¢|“¢|\"¢)+\s*", "\n- ", text)

        self.parts.append(text)

    def get_text(self) -> str:
        text = "".join(self.parts)
        text = fix_encoding(text)

        text = re.sub(r"\r\n|\r", "\n", text)

        # Repair common missing-space joins from stripped HTML.
        text = re.sub(r"([a-z])(\d)", r"\1 \2", text)
        text = re.sub(r"(\d)([A-Z])", r"\1 \2", text)
        text = re.sub(r"([a-z])\(([A-Z])", r"\1 (\2", text)
        text = re.sub(r"\b(at|for|with|in|on|to)([A-Z][a-z])", r"\1 \2", text)

        # Normalise whitespace without destroying intended paragraph/list breaks.
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n[ \t]+", "\n", text)
        text = re.sub(r"[ \t]+\n", "\n", text)

        # Remove empty/orphan bullets or separator-only lines.
        text = re.sub(r"(?m)^[ \t]*[-–—•·▪■◦][ \t]*$", "", text)
        text = re.sub(r"(?m)^[ \t]*[|][ \t]*$", "", text)

        # Compact heading -> bullet spacing and list spacing.
        text = re.sub(r"([^\n])\n{2,}(- )", r"\1\n\2", text)
        text = re.sub(r"(?m)^- (.+)\n{2,}(?=- )", r"- \1\n", text)

        # Prevent giant paragraph gaps.
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

def clean_description(html: str) -> str:
    parser = DescriptionCleaner()
    parser.feed(norm(html))
    parser.close()

    text = parser.get_text()

    # Remove stray standalone/question-mark artifacts at paragraph starts.
    text = re.sub(r"(?m)^[ \t]*\?[ \t]+(?=[A-Z])", "", text)
    text = re.sub(r"(?m)^[ \t]*\?[ \t]*$", "", text)

    # Remove dangling separators left behind by malformed HTML.
    text = re.sub(r"(?m)^[ \t]*[|•·▪■◦][ \t]*$", "", text)
    text = re.sub(r"(?m)^[ \t]*[-–—][ \t]*$", "", text)

    # Final compacting pass for heading/list output.
    text = re.sub(r"([^\n])\n{2,}(- )", r"\1\n\2", text)
    text = re.sub(r"(?m)^- (.+)\n{2,}(?=- )", r"- \1\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()



def make_description_preview(raw_description: Any, max_chars: int = 350) -> str:
    """Short cleaned description preview for decision-report.csv only."""
    text = clean_description(norm(raw_description))
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "..."

def read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path, dtype=str)
    if suffix == ".csv":
        return pd.read_csv(path, dtype=str)
    raise ValueError(f"Unsupported file type: {path.name}")


def _table_has_columns(path: Path, required: set[str]) -> bool:
    """Cheap header check used to identify lookup/register files safely."""
    try:
        if path.suffix.lower() in {".xlsx", ".xls"}:
            cols = set(pd.read_excel(path, dtype=str, nrows=0).columns)
        elif path.suffix.lower() == ".csv":
            cols = set(pd.read_csv(path, dtype=str, nrows=0).columns)
        else:
            return False
    except Exception:
        return False
    return required.issubset(cols)


def _candidate_tables(search_dirs: list[Path]) -> list[Path]:
    """Return unique spreadsheet/CSV candidates from the supplied folders."""
    seen: set[Path] = set()
    candidates: list[Path] = []
    for directory in search_dirs:
        if not directory.exists() or not directory.is_dir():
            continue
        for p in directory.iterdir():
            if p.suffix.lower() not in {".xlsx", ".xls", ".csv"}:
                continue
            if p.name.startswith("~$"):
                continue
            resolved = p.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            candidates.append(p)
    return candidates


def find_input_file(keywords: list[str], exclude: Path | None = None) -> Path:
    """Find the JobG8 input file inside /input. Avoid treating the title register as a lookup fallback."""
    files = _candidate_tables([INPUT_DIR])
    if exclude:
        files = [p for p in files if p.resolve() != exclude.resolve()]

    # Do not let the optional title classification register be mistaken for the JobG8 or geo lookup file.
    files = [p for p in files if not any(k in p.name.lower() for k in TITLE_REGISTER_FILE_KEYWORDS)]

    matches = [p for p in files if any(k in p.name.lower() for k in keywords)]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise SystemExit(
            "STOP: multiple matching input files found: " + ", ".join(p.name for p in matches)
        )
    if len(files) == 1:
        return files[0]
    raise SystemExit(
        "STOP: could not identify the JobG8 input file clearly. Put ONE JobG8 export in /input, "
        "with a name including 'jobg8'."
    )


def _unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        unique.append(path)
    return unique


def find_lookup_file(job_file: Path) -> Path:
    """
    Find the geo lookup safely, using the same practical behaviour as the working admin/service script.

    V_12_5 fix:
    - prefer the lookup file in /input first
    - only search beside the script if /input has no valid geo lookup
    - do not fail just because another geo/lookup workbook also exists in the pipeline folder
    - never treat the title classification register as the geo lookup
    - final check requires actual Area + Cluster columns
    """

    def valid_lookup_candidates(search_dirs: list[Path]) -> list[Path]:
        candidates = _candidate_tables(search_dirs)
        candidates = [p for p in candidates if p.resolve() != job_file.resolve()]
        candidates = [p for p in candidates if not any(k in p.name.lower() for k in TITLE_REGISTER_FILE_KEYWORDS)]

        named = [p for p in candidates if any(k in p.name.lower() for k in LOOKUP_FILE_KEYWORDS)]
        valid_named = [p for p in named if _table_has_columns(p, {"Area", "Cluster"})]
        if valid_named:
            return _unique_paths(valid_named)

        valid_by_columns = [p for p in candidates if _table_has_columns(p, {"Area", "Cluster"})]
        return _unique_paths(valid_by_columns)

    # Match the proven admin/service workflow: if /input has a single valid lookup, use it.
    input_matches = valid_lookup_candidates([INPUT_DIR])
    if len(input_matches) == 1:
        return input_matches[0]
    if len(input_matches) > 1:
        raise SystemExit(
            "STOP: multiple valid geo lookup files found in /input: "
            + ", ".join(p.name for p in input_matches)
            + ". Keep only one lookup workbook in /input."
        )

    # Fallback only: support the geo lookup sitting beside the script/pipeline folder.
    script_dir = Path(__file__).resolve().parent
    fallback_dirs = [Path("geo"), Path.cwd(), script_dir]
    fallback_matches = valid_lookup_candidates(fallback_dirs)
    if len(fallback_matches) == 1:
        return fallback_matches[0]
    if len(fallback_matches) > 1:
        raise SystemExit(
            "STOP: multiple valid geo lookup files found beside the script/pipeline folder: "
            + ", ".join(p.name for p in fallback_matches)
            + ". Move the one you want into /input or remove the duplicate."
        )

    raise SystemExit(
        "STOP: could not find the geo lookup file. Put one lookup/geo spreadsheet with columns Area and Cluster "
        "in /input."
    )

def validate_job_columns(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise SystemExit("STOP: missing required JobG8 column(s): " + ", ".join(missing))


def build_lookup(lookup_df: pd.DataFrame) -> dict[str, str]:
    if "Area" not in lookup_df.columns or "Cluster" not in lookup_df.columns:
        raise SystemExit("STOP: lookup file must contain columns named exactly: Area, Cluster")

    lookup: dict[str, str] = {}
    for _, row in lookup_df.iterrows():
        area = norm_key(row.get("Area"))
        cluster = norm_key(row.get("Cluster"))
        if not area:
            continue
        region = REGION_MAP.get(cluster)
        if region:
            lookup[area] = region
    if not lookup:
        raise SystemExit("STOP: lookup file contains no supported V11 region areas after mapping Cluster values.")
    return lookup


def included_by_title(title: str) -> tuple[bool, str]:
    t = norm_key(title)
    include_hits = [term for term in INCLUDE_TERMS if term in t]
    exclude_hits = [term for term in EXCLUDE_TERMS if term in t]
    if not include_hits:
        return False, "failed filter: no include term"
    if exclude_hits:
        return False, "failed filter: excluded keyword " + ", ".join(exclude_hits)
    return True, "role_match: " + ", ".join(include_hits)


def format_number(value: Any) -> str:
    raw = norm(value)
    if raw == "":
        return ""
    try:
        number = float(raw)
    except ValueError:
        return raw
    if number.is_integer():
        return str(int(number))
    return str(number).rstrip("0").rstrip(".")


def salary_numbers_for_period_check(*values: Any) -> list[float]:
    """Return numeric salary values only, used for salary-period sanity checks."""
    nums: list[float] = []
    for value in values:
        raw = norm(value)
        if not raw:
            continue
        try:
            nums.append(float(raw))
        except ValueError:
            continue
    return nums


def normalise_salary_period(row: pd.Series) -> str:
    """
    Normalise JobG8 salary period with a guard for bad period labels.

    JobG8 exports can label small hourly-looking rates such as 14-15 as annual.
    That produces impossible display text like '£14 - £15 per year'.
    V7 treats annual values below £1,000 as hourly, because a UK annual salary
    below £1,000 is not a credible job salary but £14-£15 is a credible hourly rate.
    """
    period = norm(row.get(COL["salary_period"])).lower()
    nums = salary_numbers_for_period_check(row.get(COL["salary_min"]), row.get(COL["salary_max"]))
    max_num = max(nums) if nums else None

    if period in {"annual", "year", "yearly", "annum"} and max_num is not None and max_num < 1000:
        return "hourly"

    return period


def clean_salary_additional(value: Any) -> str:
    """Clean /Job/SalaryAdditional before adding it to salary_text."""
    raw = norm(value)
    if not raw:
        return ""

    had_mojibake = any(marker in raw for marker in ["Â", "Ã", "â", "�", "?", "¢"])
    text = fix_encoding(unescape(raw))
    text = text.replace("\u00a0", " ")

    # Normalise specific corrupted currency/bullet fragments seen in JobG8 exports.
    text = re.sub(r"(?:Ã¢|â)\s*[\"'“”]?\s*\??", "", text)
    text = text.replace("�", "")
    text = text.replace("¢", "")
    text = re.sub(r"\s+", " ", text).strip()

    # If a corrupted salary amount appears before a useful parenthetical addition,
    # drop the duplicate/bad amount and keep the useful note.
    # Example: â?32.920 (Inc. sleep-ins) -> Inc. sleep-ins
    if had_mojibake:
        text = re.sub(r"^[^A-Za-z(]*\d[\d,\.\s]*(?=\()", "", text).strip()
        m = re.fullmatch(r"\(([^)]{2,})\)", text)
        if m:
            text = m.group(1).strip()

    text = text.strip(" -–—,;")
    if not text or text.lower() == "not provided":
        return ""

    # Do not pass through fragments that still visibly contain mojibake markers.
    if any(marker in text for marker in ["Â", "Ã", "â", "�", "¢"]):
        return ""

    return text


def extract_salary_from_description(raw_description: Any) -> str:
    """
    Secondary salary fallback for JobG8 rows where structured salary columns are blank.

    Safety rule:
    - extract only explicit £ amounts with a nearby pay period from /Job/Description
    - never infer from similar roles, title, employer, or location
    - return blank if no clear explicit salary phrase is present
    """
    raw = norm(raw_description)
    if not raw:
        return ""

    text = clean_description(raw)
    text = re.sub(r"\s+", " ", text).strip()
    if not text or "£" not in text:
        return ""

    amount = r"£\s*\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?"
    range_amount = rf"{amount}(?:\s*(?:-|–|—|to)\s*{amount})?"
    period = (
        r"(?:"
        r"per\s+(?:hour|hr|annum|year|sleep[- ]?in|shift|week|month|day)"
        r"|an\s+hour|a\s+year"
        r"|p/?h|ph|hourly|annually|annual"
        r")"
    )
    salary_phrase = rf"{range_amount}\s*(?:{period})"
    chained_salary_phrase = rf"{salary_phrase}(?:\s*(?:\+|and|plus)\s*{salary_phrase})*"

    match = re.search(chained_salary_phrase, text, flags=re.IGNORECASE)
    if not match:
        return ""

    extracted = match.group(0).strip(" .;,:")
    extracted = re.sub(r"\s+", " ", extracted)
    extracted = re.sub(r"£\s+", "£", extracted)
    extracted = re.sub(r"\bph\b", "per hour", extracted, flags=re.IGNORECASE)
    extracted = re.sub(r"\bp/h\b", "per hour", extracted, flags=re.IGNORECASE)
    extracted = re.sub(r"\bannually\b", "per year", extracted, flags=re.IGNORECASE)
    extracted = re.sub(r"\bannual\b", "per year", extracted, flags=re.IGNORECASE)
    extracted = re.sub(r"\ban hour\b", "per hour", extracted, flags=re.IGNORECASE)
    extracted = re.sub(r"\ba year\b", "per year", extracted, flags=re.IGNORECASE)
    extracted = re.sub(r"sleep[ -]in", "sleep-in", extracted, flags=re.IGNORECASE)

    # Final safety check: require a currency symbol and a pay-period word in the final result.
    if "£" not in extracted:
        return ""
    if not re.search(r"\b(per hour|per hr|per annum|per year|per sleep-in|per shift|per week|per month|per day|hourly)\b", extracted, flags=re.IGNORECASE):
        return ""

    return fix_encoding(extracted)

def build_salary_details(row: pd.Series) -> tuple[str, str]:
    """Return deterministic salary_text plus source marker for decision-report QA."""
    mn = format_number(row.get(COL["salary_min"]))
    mx = format_number(row.get(COL["salary_max"]))
    period = normalise_salary_period(row)
    additional = clean_salary_additional(row.get(COL["salary_additional"]))

    if not mn and not mx:
        if additional:
            return fix_encoding(additional), "structured"
        fallback = extract_salary_from_description(row.get(COL["description"]))
        if fallback:
            return fallback, "description_fallback"
        return "", "missing"

    period_text = ""
    if period in {"annual", "year", "yearly", "annum"}:
        period_text = " per year"
    elif period in {"hourly", "hour", "hr"}:
        period_text = " per hour"
    elif period:
        period_text = f" per {period}"

    if mn and mx and mn != mx:
        base = f"£{mn} - £{mx}{period_text}"
    else:
        base = f"£{mn or mx}{period_text}"

    if additional:
        return fix_encoding(f"{base} ({additional})"), "structured"
    return fix_encoding(base), "structured"


def build_salary_text(row: pd.Series) -> str:
    """Compatibility wrapper: return salary text only."""
    salary_text, _salary_source = build_salary_details(row)
    return salary_text


def build_company(row: pd.Series) -> str:
    parts = [
        norm(row.get(COL["advertiser_name"])),
        norm(row.get(COL["advertiser_type"])),
        norm(row.get(COL["employment_type"])),
    ]
    return fix_encoding(" - ".join([p for p in parts if p]))


def get_posted_date(row: pd.Series, df_columns: list[str]) -> str:
    for col in OPTIONAL_POSTED_DATE_COLUMNS:
        if col in df_columns:
            return norm(row.get(col))
    return ""


@dataclass
class ManualDecisionState:
    """Editorial decisions loaded from the human review markdown or legacy CSV."""

    report_loaded: bool
    rerun_mode: bool
    overrides: dict[str, str]
    selections: set[str]
    previously_selected: set[str]
    load_warning: str = ""
    source: str = "none"
    markdown_excludes_loaded: int = 0
    markdown_selections_loaded: int = 0


MANUAL_OVERRIDE_ALIASES = {
    "FORCE_INCLUDE": "FORCE_INCLUDE",
    "FORCE_EXCLUDE": "FORCE_EXCLUDE",
    "EXCLUDE": "FORCE_EXCLUDE",
}


def _truthy_manual_marker(value: Any) -> bool:
    return norm(value).strip().lower() in {"1", "yes", "y", "true"}


def normalise_manual_override(value: Any) -> str:
    """Return the internal manual_override token for a human-entered value."""
    return MANUAL_OVERRIDE_ALIASES.get(norm(value).strip().upper(), "")


def _parse_markdown_review_blocks(text: str) -> list[dict[str, str]]:
    """Parse --- delimited key/value blocks from support-worker-review.md.

    The compact review format keeps the editable ``action:`` field on one
    line and puts the immutable job summary on the next line. Older expanded
    key/value blocks are also accepted so existing action edits can be
    preserved if the review file is regenerated.
    """
    blocks: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    last_key: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "---":
            if current is not None and current:
                blocks.append(current)
                current = None
            else:
                current = {}
            last_key = None
            continue

        if current is None or not line or line.startswith("#"):
            continue

        key_match = re.match(r"^([A-Za-z_][A-Za-z0-9_ -]*):(.*)$", line)
        if key_match:
            key, value = key_match.groups()
            last_key = key.strip().lower()
            current[last_key] = value.strip()
            continue

        if last_key == "action":
            current["summary"] = line

    if current is not None and current:
        blocks.append(current)

    return blocks


def _markdown_review_action_by_job_id(text: str) -> dict[str, str]:
    """Return explicit Markdown review actions keyed by job_id."""
    actions: dict[str, str] = {}
    for block in _parse_markdown_review_blocks(text):
        job_id = norm(block.get("job_id"))
        action = norm(block.get("action")).strip().lower()
        if job_id and action in {"exclude", "select"}:
            actions[job_id] = action
    return actions


def load_manual_decisions_from_markdown() -> ManualDecisionState:
    """Read manual rerun decisions from manual/support-worker-review.md."""
    try:
        text = MANUAL_REVIEW_MD_PATH.read_text(encoding="utf-8-sig")
    except Exception as exc:
        return ManualDecisionState(
            report_loaded=False,
            rerun_mode=False,
            overrides={},
            selections=set(),
            previously_selected=set(),
            load_warning=f"support-worker review Markdown exists but could not be read: {exc}",
            source="none",
        )

    overrides: dict[str, str] = {}
    selections: set[str] = set()
    previously_selected: set[str] = set()

    for block in _parse_markdown_review_blocks(text):
        job_id = norm(block.get("job_id"))
        if not job_id:
            continue

        action = norm(block.get("action")).strip().lower()
        if action == "exclude":
            overrides[job_id] = "FORCE_EXCLUDE"
        elif action == "select":
            selections.add(job_id)

        decision = norm(block.get("decision")).upper()
        summary_decision = norm(block.get("summary")).split("|", 1)[0].strip().upper()
        if decision == "SELECTED" or summary_decision == "SELECTED":
            previously_selected.add(job_id)

    markdown_excludes = sum(1 for value in overrides.values() if value == "FORCE_EXCLUDE")
    return ManualDecisionState(
        report_loaded=True,
        rerun_mode=True,
        overrides=overrides,
        selections=selections,
        previously_selected=previously_selected,
        source="markdown",
        markdown_excludes_loaded=markdown_excludes,
        markdown_selections_loaded=len(selections),
    )


def load_manual_decisions_from_csv() -> ManualDecisionState:
    """Read manual rerun decisions from manual/support-worker-review.csv."""
    try:
        df = pd.read_csv(MANUAL_REVIEW_CSV_PATH, dtype=str).fillna("")
    except Exception as exc:
        return ManualDecisionState(
            report_loaded=False,
            rerun_mode=False,
            overrides={},
            selections=set(),
            previously_selected=set(),
            load_warning=f"support-worker review CSV exists but could not be read: {exc}",
            source="none",
        )

    overrides: dict[str, str] = {}
    selections: set[str] = set()
    previously_selected: set[str] = set()

    has_manual_override = "manual_override" in df.columns
    has_manual_select = "manual_select" in df.columns
    has_selection_status = "selection_status" in df.columns
    has_decision = "decision" in df.columns

    for _, row in df.iterrows():
        job_id = norm(row.get("job_id"))
        if not job_id:
            continue

        if has_manual_override:
            override = normalise_manual_override(row.get("manual_override"))
            if override:
                overrides[job_id] = override

        if has_manual_select and _truthy_manual_marker(row.get("manual_select")):
            selections.add(job_id)

        selection_status = norm(row.get("selection_status")).upper() if has_selection_status else ""
        decision = norm(row.get("decision")).upper() if has_decision else ""
        if selection_status == "SELECTED" or decision == "SELECTED":
            previously_selected.add(job_id)

    return ManualDecisionState(
        report_loaded=True,
        rerun_mode=True,
        overrides=overrides,
        selections=selections,
        previously_selected=previously_selected,
        source="csv",
    )


def load_manual_decisions() -> ManualDecisionState:
    """Prefer GitHub-editable Markdown, falling back to the preview CSV."""
    empty_state = ManualDecisionState(
        report_loaded=False,
        rerun_mode=False,
        overrides={},
        selections=set(),
        previously_selected=set(),
        source="none",
    )

    if MANUAL_REVIEW_MD_PATH.exists():
        return load_manual_decisions_from_markdown()

    if MANUAL_REVIEW_CSV_PATH.exists():
        return load_manual_decisions_from_csv()

    return empty_state


def load_manual_overrides() -> dict[str, str]:
    """Read supported manual_override values from the human review source."""
    return load_manual_decisions().overrides


def load_manual_selects() -> set[str]:
    """Read manual_select = 1/yes/y/true from the human review source."""
    return load_manual_decisions().selections


def find_optional_input_file(keywords: list[str]) -> Path | None:
    """Return an optional input/register file if one clearly matches; otherwise None."""
    files = _candidate_tables([INPUT_DIR, Path("registers")])
    for keyword in keywords:
        matches = [path for path in files if keyword in path.name.lower()]
        if len(matches) == 1:
            return matches[0]
    return None


def normalise_title_for_register(title: Any) -> str:
    return re.sub(r"\s+", " ", norm(title).lower()).strip()


def load_title_register() -> dict[str, dict[str, str]]:
    """
    Optional exact-title classification register.

    Recommended source file:
      input/support_worker_title_classification_register.csv

    Required columns if supplied:
      title, classification, review_status, reason

    If no register is supplied, V9 falls back to the embedded rule seeds.
    """
    register_path = find_optional_input_file(TITLE_REGISTER_FILE_KEYWORDS)
    if not register_path:
        return {}

    try:
        df = read_table(register_path).fillna("")
    except Exception:
        return {}

    required = {"title", "classification", "review_status", "reason"}
    if not required.issubset(set(df.columns)):
        return {}

    register: dict[str, dict[str, str]] = {}
    for _, row in df.iterrows():
        title_key = normalise_title_for_register(row.get("title"))
        if not title_key:
            continue
        classification = norm(row.get("classification")).upper() or "REVIEW_CONTEXT_DEPENDENT"
        review_status = norm(row.get("review_status")).upper()
        if review_status == "REVIEW" and classification != "ELASTIC_FIT":
             classification = "REVIEW_CONTEXT_DEPENDENT"
        register[title_key] = {
            "classification": classification,
            "reason": norm(row.get("reason")) or "exact title register match",
            "review_status": review_status or "STABLE",
        }
    return register


def contains_pattern(title_key: str, pattern: str) -> bool:
    """Simple guarded substring matcher for title classification patterns."""
    padded_title = f" {title_key} "
    padded_pattern = f" {pattern.strip()} "
    if pattern.endswith(" "):
        return padded_pattern in padded_title
    return pattern in title_key


def classify_title(title: str, title_register: dict[str, dict[str, str]] | None = None) -> tuple[str, str, int, str]:
    """
    Classify support-worker slice title intent.

    Returns:
      classification, reason, priority, review_status

    Rules:
    - exact register REVIEW stays REVIEW_CONTEXT_DEPENDENT
    - hard-pass patterns override everything
    - exact stable register match is used where present
    - high-confidence and elastic-fit patterns are fallback rules
    """
    title_key = normalise_title_for_register(title)
    title_register = title_register or {}

    hard_hits = [p.strip() for p in HARD_PASS_PATTERNS if contains_pattern(title_key, p)]
    if hard_hits:
        classification = "HARD_PASS"
        return classification, "hard pass title pattern: " + ", ".join(hard_hits), CLASSIFICATION_PRIORITY[classification], "STABLE"

    exact = title_register.get(title_key)
    if exact:
        classification = exact.get("classification", "REVIEW_CONTEXT_DEPENDENT")
        review_status = exact.get("review_status", "STABLE")
        reason = exact.get("reason", "exact title register match")
        if classification not in CLASSIFICATION_PRIORITY:
            classification = "REVIEW_CONTEXT_DEPENDENT"
        return classification, "title register: " + reason, CLASSIFICATION_PRIORITY[classification], review_status

    if title_key in REVIEW_CONTEXT_DEPENDENT_TITLES:
        classification = "REVIEW_CONTEXT_DEPENDENT"
        return classification, "context-dependent title from review queue", CLASSIFICATION_PRIORITY[classification], "REVIEW"

    hc_hits = [p for p in HIGH_CONFIDENCE_PATTERNS if contains_pattern(title_key, p)]
    if hc_hits:
        classification = "HIGH_CONFIDENCE"
        return classification, "high-confidence title pattern: " + ", ".join(hc_hits), CLASSIFICATION_PRIORITY[classification], "STABLE"

    elastic_hits = [p for p in ELASTIC_FIT_PATTERNS if contains_pattern(title_key, p)]
    if elastic_hits:
        classification = "ELASTIC_FIT"
        return classification, "elastic-fit title pattern: " + ", ".join(elastic_hits), CLASSIFICATION_PRIORITY[classification], "STABLE"

    classification = "OUT_OF_SCOPE"
    return classification, "no support-worker title classification match", CLASSIFICATION_PRIORITY[classification], "STABLE"

def title_filter_details(title: str) -> tuple[list[str], list[str]]:
    """Return include/exclude title hits separately so hard exclusions can stay hard."""
    t = norm_key(title)
    include_hits = [term for term in INCLUDE_TERMS if term in t]
    exclude_hits = [term for term in EXCLUDE_TERMS if term in t]
    return include_hits, exclude_hits


def process(
    job_df: pd.DataFrame,
    lookup: dict[str, str],
    overrides: dict[str, str],
    manual_selects: set[str],
    title_register: dict[str, dict[str, str]],
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    outputs = {region: [] for region in OUTPUT_FILES}
    report_rows: list[dict[str, Any]] = []
    df_columns = list(job_df.columns)

    for idx, row in job_df.iterrows():
        excel_row = idx + 2
        job_id = norm(row.get(COL["job_id"]))
        title = norm(row.get(COL["title"]))
        area = norm(row.get(COL["area"]))
        apply_url = norm(row.get(COL["apply_url"]))
        raw_description = norm(row.get(COL["description"]))
        description_preview = make_description_preview(raw_description) if raw_description else ""
        employment_type = norm(row.get(COL["employment_type"]))
        salary_text_preview, salary_source = build_salary_details(row)
        manual_override = overrides.get(job_id, "")
        manual_select = "1" if job_id in manual_selects else ""
        title_classification, title_classification_reason, title_priority, review_status = classify_title(title, title_register)

        def add_report(decision: str, reason: str, region: str = "") -> None:
            report_rows.append({
                "decision": decision,
                "manual_override": manual_override,
                "manual_select": manual_select,
                "selection_status": "",
                "selection_scenario": "",
                "region_selection_message": "",
                "remaining_slots": "",
                "possible_selection_rank": "",
                "excel_row": excel_row,
                "job_id": job_id,
                "title": title,
                "town": area,
                "region": region,
                "employment_type": employment_type,
                "salary_text": salary_text_preview,
                "salary_source": salary_source,
                "description_preview": description_preview,
                "title_classification": title_classification,
                "title_priority": title_priority,
                "review_status": review_status,
                "classification_reason": title_classification_reason,
                "reason": reason,
                "apply_url_present": "yes" if apply_url else "no",
                "description_present": "yes" if raw_description else "no",
            })

        def drop(reason: str, region: str = "") -> None:
            add_report("DROPPED", reason, region)

        if not job_id:
            drop("missing job_id")
            continue
        if not title:
            drop("missing title")
            continue
        if not area:
            drop("invalid location: blank /Job/Area")
            continue
        region = lookup.get(norm_key(area))
        if not region:
            drop("invalid location: town not in lookup")
            continue
        if region not in OUTPUT_FILES:
            drop("outside support-worker V_12 target regions", region)
            continue
        if not apply_url or not apply_url.lower().startswith("http"):
            drop("missing apply_url")
            continue
        if not raw_description:
            drop("missing description")
            continue
        if not salary_text_preview or str(salary_text_preview).strip() == "":
            drop("missing_salary", region)
            continue
        if manual_override == "FORCE_EXCLUDE":
            drop("manual override: FORCE_EXCLUDE", region)
            continue

        if title_classification in {"HARD_PASS", "OUT_OF_SCOPE"}:
            drop("title classification: " + title_classification + " - " + title_classification_reason, region)
            continue

        if title_classification == "REVIEW_CONTEXT_DEPENDENT" and manual_override != "FORCE_INCLUDE":
            drop("manual review required: " + title_classification_reason, region)
            continue

        if manual_override == "FORCE_INCLUDE":
            reason = "manual override: FORCE_INCLUDE; title classification: " + title_classification
        else:
            reason = "title classification: " + title_classification + " - " + title_classification_reason

        description = clean_description(raw_description)
        if not description:
            drop("missing description")
            continue

        item = {
            "_excel_row": excel_row,
            "_manual_override": manual_override,
            "_manual_select": manual_select,
            "_title_priority": title_priority,
            "_title_classification": title_classification,
            "job_id": job_id,
            "title": title,
            "company": build_company(row),
            "location": area,
            "region": region,
            "country": "UK",
            "category": "Support Worker – Wide",
            "employment_type": employment_type,
            "salary_min": format_number(row.get(COL["salary_min"])),
            "salary_max": format_number(row.get(COL["salary_max"])),
            "salary_text": salary_text_preview,
            "posted_date": get_posted_date(row, df_columns),
            "description": description,
            "apply_url": apply_url,
            "source": "JobG8",
        }
        outputs[region].append(clean_record_strings(item))
        add_report("INCLUDED", reason, region)

    return outputs, report_rows


def anchor_sort_and_cap(
    outputs: dict[str, list[dict[str, Any]]],
    report_rows: list[dict[str, Any]],
    manual_rerun_mode: bool = False,
    previously_selected_ids: set[str] | None = None,
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    """
    Support-worker V12_7 selection/report logic copied from working admin/service V2 pattern.

    Core behaviour:
    - Cap remains 12 per region.
    - FORCE_EXCLUDE removes bad rows earlier in process().
    - In manual rerun mode, previously SELECTED rows and manual_select = 1 rows are
      the editorial selection set; routine cap-filling/backfill is disabled.
    - Outside manual rerun mode, manual_select = 1 promotes a credible row into the
      selected set before routine ranking.
    - POSS rows are shown as the next credible swap/review candidates even when the slice is full.
    """
    final_outputs: dict[str, list[dict[str, Any]]] = {}
    selected_ids: set[str] = set()
    previously_selected_ids = previously_selected_ids or set()
    possible_selection_ids: dict[str, int] = {}
    region_status: dict[str, dict[str, Any]] = {}

    def feed_town_order(items: list[dict[str, Any]]) -> dict[str, int]:
        order: dict[str, int] = {}
        next_index = 0
        for item in items:
            town = norm_key(item.get("location"))
            if town not in order:
                order[town] = next_index
                next_index += 1
        return order

    for region, items in outputs.items():
        cap = REGION_CAPS[region]
        threshold = PUBLISH_THRESHOLDS.get(region, 6)
        anchor = ANCHOR_TOWNS[region]
        anchor_key = norm_key(anchor)
        town_order = feed_town_order(items)

        def routine_sort_key(item: dict[str, Any]) -> tuple[int, int, int, int]:
            return (
                int(item.get("_title_priority", 99)),
                0 if norm_key(item.get("location")) == anchor_key else 1,
                town_order.get(norm_key(item.get("location")), 9999),
                int(item.get("_excel_row", 999999)),
            )

        def anchor_sort_key(item: dict[str, Any]) -> tuple[int, int, int]:
            return (
                0 if norm_key(item.get("location")) == anchor_key else 1,
                town_order.get(norm_key(item.get("location")), 9999),
                int(item.get("_excel_row", 999999)),
            )

        forced = sorted(
            [item for item in items if item.get("_manual_override") == "FORCE_INCLUDE"],
            key=anchor_sort_key,
        )
        routine = [item for item in items if item.get("_manual_override") != "FORCE_INCLUDE"]
        hc = sorted(
            [item for item in routine if item.get("_title_classification") == "HIGH_CONFIDENCE"],
            key=anchor_sort_key,
        )
        anchor_elastic = sorted(
            [
                item for item in routine
                if item.get("_title_classification") == "ELASTIC_FIT"
                and norm_key(item.get("location")) == anchor_key
            ],
            key=anchor_sort_key,
        )
        other_elastic = sorted(
            [
                item for item in routine
                if item.get("_title_classification") == "ELASTIC_FIT"
                and norm_key(item.get("location")) != anchor_key
            ],
            key=anchor_sort_key,
        )
        manually_selected = sorted(
            [item for item in routine if str(item.get("_manual_select", "")).strip() == "1"],
            key=routine_sort_key,
        )
        previously_selected = sorted(
            [item for item in routine if str(item.get("job_id", "")) in previously_selected_ids],
            key=routine_sort_key,
        )

        selected: list[dict[str, Any]] = []
        seen: set[str] = set()

        def add_candidates(candidates: list[dict[str, Any]], limit: int | None = None) -> None:
            for item in candidates:
                if limit is not None and len(selected) >= limit:
                    return
                job_id = str(item.get("job_id", ""))
                if job_id and job_id not in seen:
                    selected.append(item)
                    seen.add(job_id)

        credible_total = len(forced + hc + anchor_elastic + other_elastic)
        base_without_manual = len(forced) + len(hc) + len(anchor_elastic)

        if manual_rerun_mode:
            # Editorial reruns preserve the reviewed selected set and only add explicit
            # manual_select rows. Do not refill to the cap from routine HC/elastic pools.
            add_candidates(forced, cap)
            add_candidates(previously_selected, cap)
            add_candidates(manually_selected, cap)
            scenario = "SCENARIO_MANUAL_RERUN"
            message = (
                f"{region} manual rerun: {len(previously_selected)} previously SELECTED row(s) retained "
                f"and {len(manually_selected)} manual_select row(s) applied; "
                f"{min(len(selected), cap)}/{cap} selected. Cap treated as a maximum; auto backfill disabled."
            )
        else:
            # V2: manual_select rows are deliberate editorial choices, so add them before routine fill.
            add_candidates(forced, cap)
            add_candidates(manually_selected, cap)
            add_candidates(hc, cap)
            add_candidates(anchor_elastic, cap)
            add_candidates(other_elastic, cap)

            if credible_total < threshold:
                scenario = "SCENARIO_4_BELOW_PUBLISH_THRESHOLD"
                message = (
                    f"{region} selection below publish threshold: {credible_total}/{threshold} credible roles. "
                    "Do not publish/refresh this slice from this run."
                )
            elif manually_selected:
                scenario = "SCENARIO_3_MANUAL_SELECTION_APPLIED"
                message = (
                    f"{region} manual_select applied: {len(manually_selected)} row(s) prioritised; "
                    f"{min(len(selected), cap)}/{cap} selected."
                )
            elif len(forced) + len(hc) >= cap:
                scenario = "SCENARIO_1_COMPLETE_HC_ONLY"
                message = (
                    f"{region} selection complete: HIGH_CONFIDENCE roles meet/exceed cap; "
                    f"{anchor} HC roles protected before cap."
                )
            elif base_without_manual >= cap:
                scenario = "SCENARIO_2_COMPLETE_HC_PLUS_ANCHOR_ELASTIC"
                message = f"{region} selection complete: HIGH_CONFIDENCE plus {anchor} ELASTIC_FIT fills cap."
            else:
                needed = max(cap - base_without_manual, 0)
                scenario = "SCENARIO_3_ACTION_REQUIRED"
                message = (
                    f"{region} selection incomplete: {base_without_manual}/{cap} selected after HIGH_CONFIDENCE + "
                    f"{anchor} ELASTIC_FIT. {needed} slots remain. Review POSS candidates; "
                    "put 1 in manual_select for chosen rows and rerun."
                )

        capped_selected = selected[:cap]
        selected_for_region = {str(item.get("job_id", "")) for item in capped_selected}

        # V2: show the next credible non-selected candidates as POSS for review/swap,
        # even if the region is already full. This keeps manual decisions visible near the top.
        review_pool = sorted(
            [item for item in items if str(item.get("job_id", "")) not in selected_for_region],
            key=routine_sort_key,
        )
        for rank, item in enumerate(review_pool[:POSSIBLE_SELECTION_REVIEW_COUNT], start=1):
            possible_selection_ids[str(item.get("job_id"))] = rank

        # Display-order only: render anchor-town jobs first in JSON.
        original_selected_order = {str(item.get("job_id", "")): idx for idx, item in enumerate(capped_selected)}
        final_outputs[region] = sorted(
            capped_selected,
            key=lambda item: (
                0 if norm_key(item.get("location")) == anchor_key else 1,
                original_selected_order.get(str(item.get("job_id", "")), 9999),
            ),
        )
        selected_ids.update(str(item["job_id"]) for item in final_outputs[region])
        region_status[region] = {
            "scenario": scenario,
            "message": message,
            "selected_count": len(final_outputs[region]),
            "cap": cap,
            "credible_total": credible_total,
            "high_confidence_count": len(forced) + len(hc),
            "anchor_elastic_count": len(anchor_elastic),
            "other_elastic_count": len(other_elastic),
        }

    # Keep decision report truthful and actionable.
    for row in report_rows:
        region = str(row.get("region", ""))
        job_id = str(row.get("job_id", ""))
        status = region_status.get(region)
        if status:
            row["selection_scenario"] = status["scenario"]
            row["region_selection_message"] = status["message"]
            row["remaining_slots"] = max(int(status["cap"]) - int(status["selected_count"]), 0)

        if row.get("decision") == "INCLUDED" and job_id in selected_ids:
            row["selection_status"] = "SELECTED"
            row["decision"] = "SELECTED"
        elif job_id in possible_selection_ids:
            row["selection_status"] = "POSSIBLE_SELECTION"
            row["possible_selection_rank"] = possible_selection_ids[job_id]
            region_label = region.upper() if region else "UNKNOWN REGION"
            row["decision"] = f"POSS - {region_label}"
            row["reason"] = "possible manual_select candidate for review/swap"
        elif row.get("decision") == "INCLUDED" and job_id not in selected_ids:
            row["selection_status"] = "NOT_SELECTED"
            row["decision"] = "DROPPED"
            row["reason"] = "over_cap/not selected by V12_7 regional selection logic"

    return final_outputs, region_status

def clean_for_json(item: dict[str, Any]) -> dict[str, Any]:
    cleaned = {k: v for k, v in item.items() if not k.startswith("_")}
    return clean_record_strings(cleaned)



def write_selection_summary_report(
    report_rows: list[dict[str, Any]],
    region_status: dict[str, dict[str, Any]],
) -> None:
    """Write a compact per-region dashboard for daily selection QA."""
    summary_path = OUTPUT_DIR / "selection-summary-report-support-worker.csv"
    fieldnames = [
        "region",
        "cap",
        "selected_total",
        "selected_high_confidence",
        "selected_anchor_elastic",
        "selected_other_elastic",
        "possible_candidates",
        "remaining_slots",
        "credible_total",
        "anchor_town",
        "scenario",
        "message",
    ]

    rows: list[dict[str, Any]] = []
    for region in OUTPUT_FILES:
        status = region_status.get(region, {})
        anchor = ANCHOR_TOWNS.get(region, "")
        anchor_key = norm_key(anchor)
        region_rows = [r for r in report_rows if str(r.get("region", "")) == region]
        selected_rows = [r for r in region_rows if str(r.get("selection_status", "")) == "SELECTED"]
        possible_rows = [r for r in region_rows if str(r.get("selection_status", "")) == "POSSIBLE_SELECTION"]

        selected_hc = sum(
            1 for r in selected_rows
            if str(r.get("title_classification", "")) == "HIGH_CONFIDENCE"
        )
        selected_anchor_elastic = sum(
            1 for r in selected_rows
            if str(r.get("title_classification", "")) == "ELASTIC_FIT"
            and norm_key(r.get("town", "")) == anchor_key
        )
        selected_other_elastic = sum(
            1 for r in selected_rows
            if str(r.get("title_classification", "")) == "ELASTIC_FIT"
            and norm_key(r.get("town", "")) != anchor_key
        )

        rows.append({
            "region": region,
            "cap": status.get("cap", REGION_CAPS.get(region, "")),
            "selected_total": len(selected_rows),
            "selected_high_confidence": selected_hc,
            "selected_anchor_elastic": selected_anchor_elastic,
            "selected_other_elastic": selected_other_elastic,
            "possible_candidates": len(possible_rows),
            "remaining_slots": max(int(status.get("cap", REGION_CAPS.get(region, 0))) - len(selected_rows), 0),
            "credible_total": status.get("credible_total", ""),
            "anchor_town": anchor,
            "scenario": status.get("scenario", ""),
            "message": status.get("message", ""),
        })

    with summary_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def decision_report_fieldnames() -> list[str]:
    return [
        # Daily QA / review columns first.
        "decision",
        "region",
        "title",
        "manual_override",
        "manual_select",
        "remaining_slots",
        "selection_status",
        "possible_selection_rank",
        "town",
        "title_classification",
        "selection_scenario",
        "employment_type",
        "salary_text",
        "salary_source",
        "description_preview",

        # Audit/detail columns pushed right.
        "title_priority",
        "review_status",
        "classification_reason",
        "reason",
        "apply_url_present",
        "job_id",
        "description_present",
        "excel_row",
        "region_selection_message",
    ]


def decision_report_sort_key(r: dict[str, Any]) -> tuple[int, int, int, int, str, str]:
    # V2 daily QA order:
    # West SELECTED -> West POSS -> South SELECTED -> South POSS -> all remaining dropped/audit rows.
    region_order = {region: idx for idx, region in enumerate(OUTPUT_FILES.keys())}
    selection_status = str(r.get("selection_status", ""))
    region_rank = region_order.get(str(r.get("region", "")), 9999)
    if selection_status == "SELECTED":
        top_group = region_rank * 2
    elif selection_status == "POSSIBLE_SELECTION":
        top_group = region_rank * 2 + 1
    else:
        top_group = 9999
    return (
        top_group,
        int(r.get("possible_selection_rank") or 9999),
        int(r.get("excel_row") or 999999),
        region_rank,
        str(r.get("town", "")),
        str(r.get("title", "")),
    )


def write_decision_report(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=decision_report_fieldnames())
        writer.writeheader()
        writer.writerows(rows)


def write_manual_review_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write the compact GitHub-editable support-worker review CSV."""
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=MANUAL_REVIEW_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in MANUAL_REVIEW_FIELDNAMES})


def _markdown_review_rows(rows: list[dict[str, Any]], region: str, selection_status: str) -> list[dict[str, Any]]:
    return [
        row for row in rows
        if str(row.get("region", "")) == region
        and str(row.get("selection_status", "")) == selection_status
    ]


def _markdown_value(value: Any) -> str:
    """Keep generated Markdown block values single-line and easy to edit."""
    return re.sub(r"\s+", " ", norm(value)).strip()


def write_manual_review_markdown(
    path: Path,
    rows: list[dict[str, Any]],
    preserved_actions: dict[str, str] | None = None,
) -> None:
    """Write the compact GitHub-editable support-worker review Markdown file."""
    preserved_actions = preserved_actions or {}
    lines = [
        "# Support-worker manual review",
        "",
        "Edit only the `action:` line in each block:",
        "",
        "- For a selected job, use `action: exclude` to remove it.",
        "- For a possible job, use `action: select` to add it on a manual rerun if it remains credible and is not excluded.",
        "- Leave `action:` blank for no change.",
        "- Manual edits are matched by `job_id`.",
        "",
    ]

    groups = [
        ("WEST YORKSHIRE — SELECTED", "West Yorkshire", "SELECTED", "SELECTED"),
        ("WEST YORKSHIRE — POSSIBLES", "West Yorkshire", "POSSIBLE_SELECTION", "POSS"),
        ("SOUTH YORKSHIRE — SELECTED", "South Yorkshire", "SELECTED", "SELECTED"),
        ("SOUTH YORKSHIRE — POSSIBLES", "South Yorkshire", "POSSIBLE_SELECTION", "POSS"),
    ]

    for heading, region, status, decision_label in groups:
        lines.extend([f"## {heading}", ""])
        group_rows = _markdown_review_rows(rows, region, status)
        if not group_rows:
            lines.extend(["_No jobs in this group._", ""])
            continue

        for row in group_rows:
            job_id = _markdown_value(row.get("job_id"))
            action = preserved_actions.get(job_id, "")
            review_label = decision_label
            if decision_label == "POSS":
                review_label = f"POSS - {region.upper()}"
            summary = " | ".join([
                review_label,
                _markdown_value(row.get("region")),
                _markdown_value(row.get("town")),
                _markdown_value(row.get("salary_text")),
                _markdown_value(row.get("title")),
            ])
            lines.extend([
                "---",
                f"action: {action}" if action else "action:",
                summary,
                f"job_id: {job_id}",
                "---",
                "",
            ])

    path.write_text("\n".join(lines), encoding="utf-8")


def write_outputs(
    outputs: dict[str, list[dict[str, Any]]],
    report_rows: list[dict[str, Any]],
    total_input: int,
    manual_decisions: ManualDecisionState | None = None,
) -> tuple[bool, bool]:
    OUTPUT_DIR.mkdir(exist_ok=True)

    manual_decisions = manual_decisions or ManualDecisionState(False, False, {}, set(), set())

    # IMPORTANT: cap first, then write JSON and validation counts from the capped output.
    outputs, region_status = anchor_sort_and_cap(
        outputs,
        report_rows,
        manual_rerun_mode=manual_decisions.rerun_mode,
        previously_selected_ids=manual_decisions.previously_selected,
    )

    for region, filename in OUTPUT_FILES.items():
        path = OUTPUT_DIR / filename
        payload = [clean_for_json(item) for item in outputs[region]]

        # HARD STOP: do not write user-facing JSON if encoding garbage remains.
        payload_text = json.dumps(payload, ensure_ascii=False)
        bad_markers = ["Â£", "Â", "â€“", "â€”", "â€", "Ã", "â?", "�", "“¢", "\"¢"]
        remaining = [marker for marker in bad_markers if marker in payload_text]
        if remaining:
            raise SystemExit(
                "STOP: encoding garbage still present in JSON payload for "
                f"{region}: {', '.join(remaining)}"
            )

        with path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    # Clean report rows after over-cap adjustment.
    report_rows = [clean_record_strings(row) for row in report_rows]

    # Compact daily selection dashboard.
    write_selection_summary_report(report_rows, region_status)

    # Short summary report
    report_path = OUTPUT_DIR / "validation-report-support-worker.csv"
    dropped_count = sum(1 for r in report_rows if r["decision"] == "DROPPED")
    included_count = sum(1 for r in report_rows if r["decision"] == "SELECTED")

    with report_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["metric", "value"])
        writer.writeheader()
        writer.writerow({"metric": "total rows input", "value": total_input})
        writer.writerow({"metric": "total rows included", "value": included_count})
        writer.writerow({"metric": "total rows dropped", "value": dropped_count})
        for classification in ["HIGH_CONFIDENCE", "ELASTIC_FIT", "REVIEW_CONTEXT_DEPENDENT", "HARD_PASS", "OUT_OF_SCOPE"]:
            writer.writerow({
                "metric": f"title classification count - {classification}",
                "value": sum(1 for r in report_rows if r.get("title_classification") == classification),
            })
        for region in OUTPUT_FILES:
            status = region_status.get(region, {})
            writer.writerow({"metric": f"selection scenario - {region}", "value": status.get("scenario", "")})
            writer.writerow({"metric": f"selection message - {region}", "value": status.get("message", "")})
            writer.writerow({"metric": f"credible total - {region}", "value": status.get("credible_total", "")})
            writer.writerow({"metric": f"high confidence count - {region}", "value": status.get("high_confidence_count", "")})
            writer.writerow({"metric": f"anchor elastic count - {region}", "value": status.get("anchor_elastic_count", "")})
            writer.writerow({"metric": f"other elastic count - {region}", "value": status.get("other_elastic_count", "")})
            writer.writerow({"metric": f"total rows output - {region}", "value": len(outputs[region])})
            ids = "; ".join(item["job_id"] for item in outputs[region])
            writer.writerow({"metric": f"job_id included - {region}", "value": ids})

    # Full audit report: this is the one to review daily.
    sorted_decision_rows = sorted(report_rows, key=decision_report_sort_key)
    write_decision_report(DECISION_REPORT_PATH, sorted_decision_rows)

    # Review sources for humans. The Markdown file is the GitHub-editable manual
    # source. It is regenerated in compact form while preserving explicit
    # action edits by job_id. The CSV remains a short preview/table overview for
    # backwards compatibility. The full decision report stays in
    # output-support-worker as the audit/detail artifact.
    markdown_review_created = False
    csv_review_created = False
    MANUAL_DIR.mkdir(exist_ok=True)
    preserved_markdown_actions: dict[str, str] = {}
    markdown_review_existed = MANUAL_REVIEW_MD_PATH.exists()
    markdown_review_can_write = True
    if markdown_review_existed:
        try:
            preserved_markdown_actions = _markdown_review_action_by_job_id(
                MANUAL_REVIEW_MD_PATH.read_text(encoding="utf-8-sig")
            )
        except Exception:
            markdown_review_can_write = False
    if markdown_review_can_write:
        write_manual_review_markdown(
            MANUAL_REVIEW_MD_PATH,
            sorted_decision_rows,
            preserved_actions=preserved_markdown_actions,
        )
    markdown_review_created = not markdown_review_existed and markdown_review_can_write
    if not MANUAL_REVIEW_CSV_PATH.exists():
        write_manual_review_csv(MANUAL_REVIEW_CSV_PATH, sorted_decision_rows)
        csv_review_created = True

    return markdown_review_created, csv_review_created

def main() -> int:
    if not INPUT_DIR.exists():
        INPUT_DIR.mkdir()
        raise SystemExit("Created /input folder. Put the JobG8 export and lookup file in it, then run again.")

    job_file = find_input_file(JOB_FILE_KEYWORDS)
    lookup_file = find_lookup_file(job_file)

    print(f"Reading JobG8 export: {job_file}")
    job_df = read_table(job_file)
    validate_job_columns(job_df)

    print(f"Reading lookup file: {lookup_file}")
    lookup_df = read_table(lookup_file)
    lookup = build_lookup(lookup_df)

    support_worker_csv_review_exists = MANUAL_REVIEW_CSV_PATH.exists()
    support_worker_markdown_review_exists = MANUAL_REVIEW_MD_PATH.exists()
    manual_decisions = load_manual_decisions()
    print(f"Support-worker CSV review file exists: {'yes' if support_worker_csv_review_exists else 'no'}")
    print(f"Support-worker Markdown review file exists: {'yes' if support_worker_markdown_review_exists else 'no'}")
    if manual_decisions.load_warning:
        print(f"WARNING: {manual_decisions.load_warning}")
    print(f"Manual source used: {manual_decisions.source}")
    print(f"Markdown excludes loaded: {manual_decisions.markdown_excludes_loaded}")
    print(f"Markdown selections loaded: {manual_decisions.markdown_selections_loaded}")
    print(f"Manual rerun mode: {'yes' if manual_decisions.rerun_mode else 'no'}")
    print(f"Manual overrides loaded: {len(manual_decisions.overrides)}")
    print(f"Manual selections loaded: {len(manual_decisions.selections)}")
    if manual_decisions.rerun_mode:
        print("Auto backfill disabled because manual rerun mode is active")

    overrides = manual_decisions.overrides
    manual_selects = manual_decisions.selections

    title_register = load_title_register()
    if title_register:
        print(f"Title classification register loaded: {len(title_register)} titles")
    else:
        print("Title classification register loaded: 0; using embedded V9 rule seeds")

    outputs, report_rows = process(job_df, lookup, overrides, manual_selects, title_register)
    markdown_review_created, csv_review_created = write_outputs(outputs, report_rows, len(job_df), manual_decisions)
    print(f"Support-worker CSV review file created: {'yes' if csv_review_created else 'no'}")
    print("Support-worker CSV review file committed: no")
    print(f"Support-worker Markdown review file created: {'yes' if markdown_review_created else 'no'}")
    print("Support-worker Markdown review file committed: no")
    existing_markdown_regenerated = support_worker_markdown_review_exists and not markdown_review_created
    existing_csv_preserved = support_worker_csv_review_exists and not csv_review_created
    print(f"Existing support-worker Markdown review file regenerated compactly: {'yes' if existing_markdown_regenerated else 'no'}")
    print(f"Existing support-worker CSV review file preserved: {'yes' if existing_csv_preserved else 'no'}")
    if existing_markdown_regenerated:
        print("Existing support-worker Markdown review action edits preserved by job_id where present.")
    if existing_csv_preserved:
        print("Existing support-worker CSV review file protected; not overwritten.")

    print("Done. V_12 simple support-worker selector workflow complete.")
    print(f"Input rows: {len(job_df)}")
    print(f"West Yorkshire output: {REGION_CAPS['West Yorkshire']} max; check validation-report-support-worker.csv for actual count")
    print(f"South Yorkshire output: {REGION_CAPS['South Yorkshire']} max; check validation-report-support-worker.csv for actual count")
    for region in OUTPUT_FILES:
        if region not in {"West Yorkshire", "South Yorkshire"}:
            print(f"{region} output: {REGION_CAPS[region]} max; check validation-report-support-worker.csv for actual count")
    print(f"Dropped rows: {sum(1 for r in report_rows if r['decision'] == 'DROPPED')}")
    print("Files written to /output-support-worker")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except pd.errors.ParserError as exc:
        raise SystemExit(f"STOP: row parsing error: {exc}") from exc
    except Exception as exc:
        raise SystemExit(f"STOP: unexpected error: {exc}") from exc

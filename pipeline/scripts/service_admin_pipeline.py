
"""
Ontap Phase-1: JobG8 CSV/XLSX -> admin/service JSON pipeline

V2_5 fix:
- missing salary no longer drops otherwise credible admin/service rows; salary_source remains missing for QA

V2 additions:
- manual_select = 1 can promote a credible POSS/NOT_SELECTED row as a swap candidate
- selected rows display as SELECTED in the first decision column
- decision report sorts West SELECTED -> West POSS -> South SELECTED -> South POSS -> rest below

V11_6 additions:
- adds salary_source to decision-report.csv: structured / description_fallback / missing

V11_5 additions:
- secondary salary fallback: if structured JobG8 salary fields are blank, extract only explicit £ salary phrases from /Job/Description; never infer or fabricate salary

V12_3 additions:
- separate selection-summary-report.csv for quick per-region QA

V11 additions:
- expanded North-of-England regional selection: West Yorkshire, South Yorkshire, Lancashire, Greater Manchester, Cumbria, North East

V10 additions:
- daily selection scenario reporting for West/South Yorkshire
- manual_select = 1 for Scenario 3 candidate fill
- anchor-town selection logic before cap

V9 additions:
- title classification layer for Admin/Service slices
- HIGH_CONFIDENCE / ELASTIC_FIT / REVIEW_CONTEXT_DEPENDENT / HARD_PASS
- optional admin_service_title_classification_register.csv exact-title lookup
- hard-pass titles remain hard-pass even with FORCE_INCLUDE
- elastic titles can fill thin slices after high-confidence titles

Input folder:
  input/   put ONE JobG8 export and ONE region lookup file here

Output folder:
  output/west-yorkshire-admin/service.json
  output/south-yorkshire-admin/service.json
  output/lancashire-admin/service.json
  output/greater-manchester-admin/service.json
  output/cumbria-admin/service.json
  output/north-east-admin/service.json
  output/validation-report.csv
  output/selection-summary-report.csv
  output/decision-report.csv  add manual_override values or manual_select = 1 where flagged, then rerun

Run:
  python3 jobg8_to_ontap_json_admin_service_V2.py

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
OUTPUT_DIR = Path("output-admin-service")
DECISION_REPORT_PATH = OUTPUT_DIR / "decision-report-admin-service.csv"

JOB_FILE_KEYWORDS = ["jobg8", "jobs"]
LOOKUP_FILE_KEYWORDS = ["lookup", "region", "town"]
TITLE_REGISTER_FILE_KEYWORDS = ["admin_service_title_classification_register", "title_classification_register"]

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
    "admin",
    "administrator",
    "administration",
    "administrative",
    "customer service",
    "receptionist",
    "office",
    "service advisor",
    "service administrator",
    "service coordinator",
    "business support",
    "data entry",
    "call handler",
    "contact centre",
    "scheduler",
    "planner",
    "booking",
    "bookings",
]

EXCLUDE_TERMS = [
    "support worker",
    "care assistant",
    "healthcare assistant",
    "health care assistant",
    "nurse",
    "teacher",
    "driver",
    "engineer",
    "warehouse",
    "operative",
    "labourer",
    "labourer",
    "manager",
    "senior manager",
    "sales executive",
    "field sales",
    "business development",
    "account manager",
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
    "West Yorkshire": "west-yorkshire-admin-service.json",
    "South Yorkshire": "south-yorkshire-admin-service.json",
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

# Stable hard-pass title patterns for admin/service-office slice.
# These are excluded even if the slice is thin.
HARD_PASS_PATTERNS = [
    # Care/admin/service pollution from the first slice family.
    "support worker", "care assistant", "care worker", "healthcare assistant", "health care assistant",
    "homecare", "home care", "personal assistant", "residential support", "waking night",
    "nurse", "therapist", "social worker", "counsellor", "counselor", "psychologist",
    "teacher", "teaching", "school", "semh", "send", "sen ", "learning support", "teaching assistant",

    # Manual/technical/field roles.
    "driver", "drivers", "transport", "warehouse", "operative", "labourer", "laborer",
    "engineer", "technician", "mechanic", "electrician", "plumber", "fitter", "installer",
    "chef", "cook", "cleaner", "cleaning", "security guard", "production", "manufacturing",

    # Senior/management and sales-heavy roles.
    "senior manager", "general manager", "operations manager", "sales executive", "field sales",
    "business development", "account manager", "sales consultant", "telesales", "estate agent",
]

# Clear office/admin/service-support roles.
HIGH_CONFIDENCE_PATTERNS = [
    "administrator", "admin assistant", "administration assistant", "administrative assistant",
    "office administrator", "office assistant", "office support", "clerical", "data entry",
    "receptionist", "front of house", "secretary", "personal secretary", "pa to",
    "customer service advisor", "customer service adviser", "customer service assistant",
    "customer service administrator", "customer support advisor", "client service advisor",
    "call handler", "contact centre", "call centre", "service advisor", "service adviser",
    "service administrator", "service coordinator", "service co-ordinator", "business support officer",
    "business support administrator", "bookings administrator", "booking coordinator", "scheduler",
]

# Adjacent credible admin/service roles; useful for filling a thin slice but should not outrank HC.
ELASTIC_FIT_PATTERNS = [
    "coordinator", "co-ordinator", "planner", "scheduler", "recruitment administrator",
    "hr assistant", "hr administrator", "payroll administrator", "accounts assistant", "finance assistant",
    "procurement assistant", "purchasing assistant", "sales administrator", "sales support",
    "service desk", "helpdesk", "help desk", "complaints handler", "claims handler",
    "case administrator", "document controller", "compliance administrator",
]

# Exact review titles can be added here after manual QA. Keep empty in V1.
REVIEW_CONTEXT_DEPENDENT_TITLES: set[str] = set()



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


def find_input_file(keywords: list[str], exclude: Path | None = None) -> Path:
    files = [
        p
        for p in INPUT_DIR.iterdir()
        if p.suffix.lower() in {".xlsx", ".xls", ".csv"}
        and not p.name.startswith("~$")
    ]
    if exclude:
        files = [p for p in files if p.resolve() != exclude.resolve()]
    matches = [p for p in files if any(k in p.name.lower() for k in keywords)]
    if len(matches) == 1:
        return matches[0]
    if len(files) == 1:
        return files[0]
    raise SystemExit(
        "STOP: could not identify input files clearly. Put ONE JobG8 export and ONE lookup file in /input, "
        "with names including 'jobg8' and 'lookup'."
    )


def _table_has_columns(path: Path, required: set[str]) -> bool:
    """Cheap header check used to identify geo lookup files safely."""
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
        for candidate in directory.iterdir():
            if candidate.suffix.lower() not in {".xlsx", ".xls", ".csv"}:
                continue
            if candidate.name.startswith("~$"):
                continue
            resolved = candidate.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            candidates.append(candidate)
    return candidates


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
    """Find the geo lookup in /input first, then fall back to pipeline/geo."""

    def valid_lookup_candidates(search_dirs: list[Path]) -> list[Path]:
        candidates = _candidate_tables(search_dirs)
        candidates = [path for path in candidates if path.resolve() != job_file.resolve()]
        candidates = [
            path
            for path in candidates
            if not any(keyword in path.name.lower() for keyword in TITLE_REGISTER_FILE_KEYWORDS)
        ]
        named = [path for path in candidates if any(keyword in path.name.lower() for keyword in LOOKUP_FILE_KEYWORDS)]
        valid_named = [path for path in named if _table_has_columns(path, {"Area", "Cluster"})]
        if valid_named:
            return _unique_paths(valid_named)
        return _unique_paths([path for path in candidates if _table_has_columns(path, {"Area", "Cluster"})])

    input_matches = valid_lookup_candidates([INPUT_DIR])
    if len(input_matches) == 1:
        return input_matches[0]
    if len(input_matches) > 1:
        raise SystemExit(
            "STOP: multiple valid geo lookup files found in /input: "
            + ", ".join(path.name for path in input_matches)
            + ". Keep only one lookup workbook in /input."
        )

    fallback_matches = valid_lookup_candidates([Path("geo"), Path.cwd(), Path(__file__).resolve().parent])
    if len(fallback_matches) == 1:
        return fallback_matches[0]
    if len(fallback_matches) > 1:
        raise SystemExit(
            "STOP: multiple valid geo lookup files found beside the script/pipeline folder: "
            + ", ".join(path.name for path in fallback_matches)
            + ". Move the one you want into /input or remove the duplicate."
        )

    raise SystemExit(
        "STOP: could not find the geo lookup file. Put one lookup/geo spreadsheet with columns Area and Cluster "
        "in /input or pipeline/geo."
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


def load_manual_overrides() -> dict[str, str]:
    """
    Read manual overrides from output/decision-report.csv if it already exists.

    Supported manual_override values:
      FORCE_INCLUDE
      FORCE_EXCLUDE

    Notes:
    - First run normally has no manual_override values.
    - After reviewing decision-report.csv, add values in the manual_override column and rerun.
    - FORCE_INCLUDE bypasses missing include-term filtering but does NOT bypass hard exclusions
      such as driver, senior, manager, nurse, teacher, semh, or housing.
    """
    overrides: dict[str, str] = {}

    if not DECISION_REPORT_PATH.exists():
        return overrides

    try:
        df = pd.read_csv(DECISION_REPORT_PATH, dtype=str).fillna("")
    except Exception:
        return overrides

    if "manual_override" not in df.columns:
        return overrides

    for _, row in df.iterrows():
        job_id = norm(row.get("job_id"))
        override = norm(row.get("manual_override")).upper()

        if not job_id:
            continue

        if override in {"FORCE_INCLUDE", "FORCE_EXCLUDE"}:
            overrides[job_id] = override

    return overrides


def load_manual_selects() -> set[str]:
    """
    Read manual_select = 1 from output/decision-report.csv if it already exists.

    V10 use:
    - Only use this for Scenario 3 rows marked POSSIBLE_SELECTION.
    - Keep manual_override for true FORCE_INCLUDE / FORCE_EXCLUDE exceptions.
    """
    selected: set[str] = set()

    if not DECISION_REPORT_PATH.exists():
        return selected

    try:
        df = pd.read_csv(DECISION_REPORT_PATH, dtype=str).fillna("")
    except Exception:
        return selected

    if "manual_select" not in df.columns:
        return selected

    for _, row in df.iterrows():
        job_id = norm(row.get("job_id"))
        marker = norm(row.get("manual_select")).strip().lower()

        if job_id and marker in {"1", "yes", "y", "true"}:
            selected.add(job_id)

    return selected



def find_optional_input_file(keywords: list[str]) -> Path | None:
    """Return an optional input/register file if one clearly matches; otherwise None."""
    files = _candidate_tables([INPUT_DIR, Path("registers"), Path(".")])
    for keyword in keywords:
        matches = _unique_paths([path for path in files if keyword in path.name.lower()])
        if len(matches) == 1:
            return matches[0]
    return None

def normalise_title_for_register(title: Any) -> str:
    return re.sub(r"\s+", " ", norm(title).lower()).strip()


def load_title_register() -> dict[str, dict[str, str]]:
    """
    Optional exact-title classification register.

    Recommended source file:
      admin_service_title_classification_register.csv beside this script
      or input/admin_service_title_classification_register.csv

    Required columns if supplied:
      title, classification, review_status, reason

    If no register is supplied, V1 falls back to the embedded admin/service rule seeds.
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
    Classify admin/service-office slice title intent.

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
    return classification, "no admin/service title classification match", CLASSIFICATION_PRIORITY[classification], "STABLE"

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
            drop("outside admin/service V1 target regions", region)
            continue
        if not apply_url or not apply_url.lower().startswith("http"):
            drop("missing apply_url")
            continue
        if not raw_description:
            drop("missing description")
            continue
        # V2_5 fix: missing salary must not remove otherwise credible admin/service roles.
        # JobG8 often supplies clear regional admin roles with blank structured salary
        # and no explicit salary in the description. Keep salary_source=missing for QA,
        # but allow the selector to count/select the role.
        if not salary_text_preview or str(salary_text_preview).strip() == "":
            salary_text_preview = ""
            salary_source = "missing"
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
            "category": "Admin/Service – Office Support",
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
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    """
    Admin/service V2 selection logic.

    Core behaviour:
    - Cap remains 12 per region.
    - FORCE_EXCLUDE removes bad rows earlier in process().
    - manual_select = 1 promotes a credible row into the selected set before routine ranking,
      making swaps practical after FORCE_EXCLUDE has removed an unwanted selected row.
    - POSS rows are shown as the next credible swap/review candidates even when the slice is full.
    """
    final_outputs: dict[str, list[dict[str, Any]]] = {}
    selected_ids: set[str] = set()
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
            row["reason"] = "over_cap/not selected by V2 regional selection logic"

    return final_outputs, region_status

def clean_for_json(item: dict[str, Any]) -> dict[str, Any]:
    cleaned = {k: v for k, v in item.items() if not k.startswith("_")}
    return clean_record_strings(cleaned)



def write_selection_summary_report(
    report_rows: list[dict[str, Any]],
    region_status: dict[str, dict[str, Any]],
) -> None:
    """Write a compact per-region dashboard for daily selection QA."""
    summary_path = OUTPUT_DIR / "selection-summary-report-admin-service.csv"
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

def write_outputs(outputs: dict[str, list[dict[str, Any]]], report_rows: list[dict[str, Any]], total_input: int) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    # IMPORTANT: cap first, then write JSON and validation counts from the capped output.
    outputs, region_status = anchor_sort_and_cap(outputs, report_rows)

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
    report_path = OUTPUT_DIR / "validation-report-admin-service.csv"
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

    # Full audit report: this is the one to review daily
    decision_path = OUTPUT_DIR / "decision-report-admin-service.csv"
    fieldnames = [
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
    with decision_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # V2 daily QA order:
        # West SELECTED -> West POSS -> South SELECTED -> South POSS -> all remaining dropped/audit rows.
        region_order = {region: idx for idx, region in enumerate(OUTPUT_FILES.keys())}

        def decision_report_sort_key(r: dict[str, Any]) -> tuple[int, int, int, int, str, str]:
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

        writer.writerows(sorted(report_rows, key=decision_report_sort_key))


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

    overrides = load_manual_overrides()
    if overrides:
        print(f"Manual overrides loaded: {len(overrides)}")
    else:
        print("Manual overrides loaded: 0")

    manual_selects = load_manual_selects()
    if manual_selects:
        print(f"Manual selections loaded: {len(manual_selects)}")
    else:
        print("Manual selections loaded: 0")

    title_register = load_title_register()
    if title_register:
        print(f"Title classification register loaded: {len(title_register)} titles")
    else:
        print("Title classification register loaded: 0; using embedded V9 rule seeds")

    outputs, report_rows = process(job_df, lookup, overrides, manual_selects, title_register)
    write_outputs(outputs, report_rows, len(job_df))

    print("Done. Admin/service V2 selector workflow complete.")
    print(f"Input rows: {len(job_df)}")
    print(f"West Yorkshire admin/service output: {REGION_CAPS['West Yorkshire']} max; check validation-report-admin-service.csv for actual count")
    print(f"South Yorkshire admin/service output: {REGION_CAPS['South Yorkshire']} max; check validation-report-admin-service.csv for actual count")
    for region in OUTPUT_FILES:
        if region not in {"West Yorkshire", "South Yorkshire"}:
            print(f"{region} output: {REGION_CAPS[region]} max; check validation-report.csv for actual count")
    print(f"Dropped rows: {sum(1 for r in report_rows if r['decision'] == 'DROPPED')}")
    print("Files written to /output-admin-service")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except pd.errors.ParserError as exc:
        raise SystemExit(f"STOP: row parsing error: {exc}") from exc
    except Exception as exc:
        raise SystemExit(f"STOP: unexpected error: {exc}") from exc

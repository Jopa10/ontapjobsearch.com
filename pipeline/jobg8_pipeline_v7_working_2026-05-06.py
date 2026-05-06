#!/usr/bin/env python3
"""
Ontap Phase-1: JobG8 CSV/XLSX -> JSON pipeline

V7 fix: salary-period sanity guard prevents small hourly rates being labelled as annual/yearly.

Input folder:
  input/   put ONE JobG8 export and ONE region lookup file here

Output folder:
  output/west-yorkshire-support-worker.json
  output/south-yorkshire-support-worker.json
  output/validation-report.csv
  output/decision-report.csv

Run:
  python3 jobg8_to_ontap_json_v7.py
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
OUTPUT_DIR = Path("output")

JOB_FILE_KEYWORDS = ["jobg8", "jobs"]
LOOKUP_FILE_KEYWORDS = ["lookup", "region", "town"]

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
    "teacher",
    "semh",
    "housing",
]

REGION_MAP = {
    "yorkshire (west)": "West Yorkshire",
    "yorkshire west": "West Yorkshire",
    "west yorkshire": "West Yorkshire",
    "yorkshire (south)": "South Yorkshire",
    "yorkshire south": "South Yorkshire",
    "south yorkshire": "South Yorkshire",
}

OUTPUT_FILES = {
    "West Yorkshire": "west-yorkshire-support-worker.json",
    "South Yorkshire": "south-yorkshire-support-worker.json",
}

REGION_CAPS = {
    "West Yorkshire": 12,
    "South Yorkshire": 6,
}

ANCHOR_TOWNS = {
    "West Yorkshire": "Leeds",
    "South Yorkshire": "Sheffield",
}


def fix_encoding(value: Any) -> Any:
    """
    Repair common mojibake from UTF-8 text misread as Windows/Latin-1.

    Examples fixed:
      Â£  -> £
      â€“ -> –
      â€™ -> '
      â€œ -> "
      â€� -> "
    """
    if not isinstance(value, str):
        return value

    text = value

    # First try proper mojibake reversal.
    # This fixes cases like "Â£" and "â€“" at source level.
    try:
        repaired = text.encode("latin1").decode("utf-8")
        # Only accept if it improves typical mojibake markers.
        bad_markers = ["Â", "â€", "â€“", "â€”", "Ã"]
        if sum(marker in repaired for marker in bad_markers) <= sum(marker in text for marker in bad_markers):
            text = repaired
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass

    # Safety-net replacements.
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
        "Ãè": "è",
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

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript"}:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in {"p", "div", "br", "section", "article", "h1", "h2", "h3", "h4"}:
            self.parts.append("\n\n")
        elif tag == "li":
            self.in_li = True
            self.parts.append("\n- ")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript"} and self.skip_depth:
            self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag == "li":
            self.in_li = False
        elif tag in {"p", "div", "ul", "ol", "section", "article"}:
            self.parts.append("\n\n")

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = fix_encoding(unescape(data))
        self.parts.append(text)

    def get_text(self) -> str:
        text = "".join(self.parts)
        text = fix_encoding(text)
        text = re.sub(r"\r\n|\r", "\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n[ \t]+", "\n", text)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def clean_description(html: str) -> str:
    parser = DescriptionCleaner()
    parser.feed(norm(html))
    parser.close()
    return parser.get_text()


def read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path, dtype=str)
    if suffix == ".csv":
        return pd.read_csv(path, dtype=str)
    raise ValueError(f"Unsupported file type: {path.name}")


def find_input_file(keywords: list[str], exclude: Path | None = None) -> Path:
    files = [p for p in INPUT_DIR.iterdir() if p.suffix.lower() in {".xlsx", ".xls", ".csv"}]
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
        raise SystemExit("STOP: lookup file contains no West/South Yorkshire areas after mapping Cluster values.")
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


def build_salary_text(row: pd.Series) -> str:
    """Deterministic transform from JobG8 salary fields with salary-period sanity guard."""
    mn = format_number(row.get(COL["salary_min"]))
    mx = format_number(row.get(COL["salary_max"]))
    period = normalise_salary_period(row)
    additional = norm(row.get(COL["salary_additional"]))

    if not mn and not mx:
        return fix_encoding(additional) if additional and additional.lower() != "not provided" else ""

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

    if additional and additional.lower() != "not provided":
        return fix_encoding(f"{base} ({additional})")
    return fix_encoding(base)


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


def process(job_df: pd.DataFrame, lookup: dict[str, str]) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    outputs = {"West Yorkshire": [], "South Yorkshire": []}
    report_rows: list[dict[str, Any]] = []
    df_columns = list(job_df.columns)

    for idx, row in job_df.iterrows():
        excel_row = idx + 2
        job_id = norm(row.get(COL["job_id"]))
        title = norm(row.get(COL["title"]))
        area = norm(row.get(COL["area"]))
        apply_url = norm(row.get(COL["apply_url"]))
        raw_description = norm(row.get(COL["description"]))
        employment_type = norm(row.get(COL["employment_type"]))
        salary_text_preview = build_salary_text(row)

        def add_report(decision: str, reason: str, region: str = "") -> None:
            report_rows.append({
                "decision": decision,
                "excel_row": excel_row,
                "job_id": job_id,
                "title": title,
                "town": area,
                "region": region,
                "employment_type": employment_type,
                "salary_text": salary_text_preview,
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
            drop("invalid location: town not in West/South lookup")
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
        ok, reason = included_by_title(title)
        if not ok:
            drop(reason, region)
            continue

        description = clean_description(raw_description)
        if not description:
            drop("missing description")
            continue

        item = {
            "_excel_row": excel_row,
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
) -> dict[str, list[dict[str, Any]]]:
    """Leeds/Sheffield first, then original JobG8 order, then enforce region caps."""
    final_outputs: dict[str, list[dict[str, Any]]] = {}
    selected_ids: set[str] = set()

    for region, items in outputs.items():
        anchor = ANCHOR_TOWNS[region].lower()
        ordered = sorted(
            items,
            key=lambda item: (
                0 if norm_key(item.get("location")) == anchor else 1,
                int(item.get("_excel_row", 999999)),
            ),
        )
        capped = ordered[:REGION_CAPS[region]]
        final_outputs[region] = capped
        selected_ids.update(item["job_id"] for item in capped)

    # Keep decision report truthful: rows matched by role but cut by cap are shown as dropped.
    for row in report_rows:
        if row.get("decision") == "INCLUDED" and row.get("job_id") not in selected_ids:
            row["decision"] = "DROPPED"
            row["reason"] = f"over_cap: not in first {REGION_CAPS.get(row.get('region'), '')} for region"

    return final_outputs


def clean_for_json(item: dict[str, Any]) -> dict[str, Any]:
    cleaned = {k: v for k, v in item.items() if not k.startswith("_")}
    return clean_record_strings(cleaned)


def write_outputs(outputs: dict[str, list[dict[str, Any]]], report_rows: list[dict[str, Any]], total_input: int) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    # IMPORTANT: cap first, then write JSON and validation counts from the capped output.
    outputs = anchor_sort_and_cap(outputs, report_rows)

    for region, filename in OUTPUT_FILES.items():
        path = OUTPUT_DIR / filename
        payload = [clean_for_json(item) for item in outputs[region]]

        # HARD STOP: do not write user-facing JSON if encoding garbage remains.
        payload_text = json.dumps(payload, ensure_ascii=False)
        bad_markers = ["Â£", "Â", "â€“", "â€”", "â€", "Ã"]
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

    # Short summary report
    report_path = OUTPUT_DIR / "validation-report.csv"
    dropped_count = sum(1 for r in report_rows if r["decision"] == "DROPPED")
    included_count = sum(1 for r in report_rows if r["decision"] == "INCLUDED")

    with report_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["metric", "value"])
        writer.writeheader()
        writer.writerow({"metric": "total rows input", "value": total_input})
        writer.writerow({"metric": "total rows included", "value": included_count})
        writer.writerow({"metric": "total rows dropped", "value": dropped_count})
        for region in ["West Yorkshire", "South Yorkshire"]:
            writer.writerow({"metric": f"total rows output - {region}", "value": len(outputs[region])})
            ids = "; ".join(item["job_id"] for item in outputs[region])
            writer.writerow({"metric": f"job_id included - {region}", "value": ids})

    # Full audit report: this is the one to review daily
    decision_path = OUTPUT_DIR / "decision-report.csv"
    fieldnames = [
        "decision", "excel_row", "job_id", "title", "town", "region",
        "employment_type", "salary_text", "reason",
        "apply_url_present", "description_present",
    ]
    with decision_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # Included rows first, then dropped rows. This makes daily QA much faster.
        writer.writerows(sorted(report_rows, key=lambda r: (r["decision"] != "INCLUDED", r["region"], r["town"], r["title"])))


def main() -> int:
    if not INPUT_DIR.exists():
        INPUT_DIR.mkdir()
        raise SystemExit("Created /input folder. Put the JobG8 export and lookup file in it, then run again.")

    job_file = find_input_file(JOB_FILE_KEYWORDS)
    lookup_file = find_input_file(LOOKUP_FILE_KEYWORDS, exclude=job_file)

    print(f"Reading JobG8 export: {job_file}")
    job_df = read_table(job_file)
    validate_job_columns(job_df)

    print(f"Reading lookup file: {lookup_file}")
    lookup_df = read_table(lookup_file)
    lookup = build_lookup(lookup_df)

    outputs, report_rows = process(job_df, lookup)
    write_outputs(outputs, report_rows, len(job_df))

    print("Done.")
    print(f"Input rows: {len(job_df)}")
    print(f"West Yorkshire output: {REGION_CAPS['West Yorkshire']} max; check validation-report.csv for actual count")
    print(f"South Yorkshire output: {REGION_CAPS['South Yorkshire']} max; check validation-report.csv for actual count")
    print(f"Dropped rows: {sum(1 for r in report_rows if r['decision'] == 'DROPPED')}")
    print("Files written to /output")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except pd.errors.ParserError as exc:
        raise SystemExit(f"STOP: row parsing error: {exc}") from exc
    except Exception as exc:
        raise SystemExit(f"STOP: unexpected error: {exc}") from exc

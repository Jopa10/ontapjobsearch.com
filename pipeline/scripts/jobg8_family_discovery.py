from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

TITLE_COL = "/Job/Position"
DESCRIPTION_COL = "/Job/Description"
AREA_COL = "/Job/Area"
LOCATION_COL = "/Job/Location"
DISPLAY_REF_COL = "/Job/DisplayReference"
SALARY_MIN_COL = "/Job/SalaryMinimum"
SALARY_MAX_COL = "/Job/SalaryMaximum"
SALARY_PERIOD_COL = "/Job/SalaryPeriod"
CLASSIFICATION_COL = "/Job/Classification"
AREA_UNUSABLE_VALUES = {"", "not specified", "unknown", "city"}
DESCRIPTION_SALARY_PATTERN = re.compile(
    r"£\s*(?P<low>\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?P<low_k>k)?"
    r"(?:\s*(?:-|–|—|to)\s*£?\s*(?P<high>\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?P<high_k>k)?)?"
    r"\s*(?P<period>per\s+(?:hour|hr|day|week|month|annum|year)|an?\s+(?:hour|day|week|month|year)|p\s*/?\s*[had]|p\.?\s*a\.?|hourly|daily|weekly|monthly|annually)",
    re.IGNORECASE,
)


def norm(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def latest_feed(input_dir: Path) -> Path:
    files = sorted(p for p in input_dir.iterdir() if p.suffix.lower() in {".xlsx", ".xls", ".xlsm"})
    if not files:
        raise SystemExit(f"No Excel feeds found in {input_dir}")
    dated = [(p, re.search(r"(20\d{2}-\d{2}-\d{2})", p.stem)) for p in files]
    dated = [(p, m.group(1)) for p, m in dated if m]
    return max(dated, key=lambda x: x[1])[0] if dated else files[-1]


def compile_many(patterns: list[str]) -> list[re.Pattern[str]]:
    return [re.compile(p, re.IGNORECASE) for p in patterns]


def any_match(patterns: list[re.Pattern[str]], value: str) -> bool:
    return any(p.search(value) for p in patterns)


def parse_salary(value: object) -> float | None:
    s = norm(value)
    if not s:
        return None
    s = re.sub(r"[^0-9.\-]", "", s.replace(",", ""))
    try:
        n = float(s)
    except ValueError:
        return None
    return n if n > 0 and math.isfinite(n) else None


def annual_factor(period: object) -> float | None:
    p = norm(period).casefold()
    if not p:
        return None
    if any(k in p for k in ("annum", "annual", "year", "yearly")):
        return 1.0
    if "month" in p:
        return 12.0
    if "week" in p:
        return 52.0
    if "day" in p:
        return 260.0
    if "hour" in p:
        return 1950.0
    if re.fullmatch(r"p\s*/?\s*h", p):
        return 1950.0
    if re.fullmatch(r"p\s*/?\s*d", p):
        return 260.0
    if re.fullmatch(r"p\.?\s*a\.?", p):
        return 1.0
    return None


def annualise(value: object, period: object) -> float | None:
    n = parse_salary(value)
    factor = annual_factor(period)
    return n * factor if n is not None and factor is not None else None


def description_annualised_max(description: object) -> float | None:
    estimates: list[float] = []
    for match in DESCRIPTION_SALARY_PATTERN.finditer(norm(description)):
        raw = match.group("high") or match.group("low")
        value = float(raw.replace(",", ""))
        if (match.group("high_k") if match.group("high") else match.group("low_k")):
            value *= 1000
        factor = annual_factor(match.group("period"))
        if factor is not None:
            estimates.append(value * factor)
    return max(estimates) if estimates else None


def find_classification_col(columns: list[str]) -> str | None:
    if CLASSIFICATION_COL in columns:
        return CLASSIFICATION_COL
    matches = [c for c in columns if "classification" in c.casefold()]
    return matches[0] if matches else None


def load_geo_lookups(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    area_df = pd.read_excel(path, dtype=str).fillna("")
    if not {"Area", "Cluster"}.issubset(area_df.columns):
        return {}, {}
    area_lookup = {
        norm(row["Area"]).casefold(): norm(row["Cluster"])
        for _, row in area_df.iterrows()
        if norm(row["Area"]) and norm(row["Cluster"])
    }
    try:
        fallback_df = pd.read_excel(path, sheet_name="LocationFallback", dtype=str).fillna("")
    except ValueError:
        return area_lookup, {}
    fallback = {
        norm(row["Location"]).casefold(): norm(row["Cluster"])
        for _, row in fallback_df.iterrows()
        if norm(row.get("Status", "")).casefold() == "auto"
        and norm(row.get("Location", ""))
        and norm(row.get("Cluster", ""))
    }
    return area_lookup, fallback


def ontap_region(area: object, location: object, area_lookup: dict[str, str], fallback: dict[str, str]) -> str:
    a = norm(area).casefold()
    loc = norm(location).casefold()
    if a in AREA_UNUSABLE_VALUES:
        return fallback.get(loc, "Other / Unknown")
    return area_lookup.get(a, "Other / Unknown")


def load_assessable_markets(path: Path) -> tuple[set[str], dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    markets = set(data.get("regions", {}).keys())
    rollups = {str(k): str(v) for k, v in data.get("detail_rollups", {}).items()}
    expected = data.get("region_count")
    if expected is not None and int(expected) != len(markets):
        raise SystemExit(f"Assessable-market config says {expected} regions but contains {len(markets)}")
    return markets, rollups


def dedupe_key(row: dict[str, Any]) -> str:
    ref = norm(row.get("display_reference", ""))
    if ref:
        return f"ref:{ref.casefold()}"
    return "fallback:" + "|".join([
        norm(row.get("title", "")).casefold(),
        norm(row.get("location", "")).casefold(),
        norm(row.get("jobg8_classification", "")).casefold(),
    ])


def content_dedupe_key(title: object, location: object, description: object) -> str:
    basis = "|".join([
        re.sub(r"\W+", " ", norm(title).casefold()).strip(),
        re.sub(r"\W+", " ", norm(description).casefold()).strip()[:1200],
        re.sub(r"\W+", " ", norm(location).casefold()).strip(),
    ])
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


def salary_bucket(annual_min: float | None, annual_max: float | None, hard_max: float) -> str:
    vals = [v for v in (annual_min, annual_max) if v is not None]
    if not vals:
        return "missing/unknown"
    if max(vals) > hard_max:
        return f">£{hard_max:,.0f} OUT"
    midpoint = sum(vals) / len(vals)
    if midpoint < 25000:
        return "<£25k"
    if midpoint <= 30000:
        return "£25k–£30k"
    if midpoint <= 40000:
        return "£30k–£40k"
    return f"£40k–£{hard_max:,.0f}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True, type=Path)
    ap.add_argument("--config", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    ap.add_argument("--geo-lookup", type=Path, default=Path("pipeline/geo/geo_lookup.xlsx"))
    ap.add_argument("--assessable-regions", type=Path, default=Path("pipeline/config/uk_assessable_regions.json"))
    args = ap.parse_args()

    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    key = cfg["family_key"]
    display_name = cfg["display_name"]
    hard_max = float(cfg.get("hard_salary_max", 50000))
    floor = int(cfg.get("viability_floor", 100))

    broad_title = compile_many(cfg.get("broad_title_patterns", []))
    description_context = compile_many(cfg.get("description_title_context_patterns", []))
    likely_in = compile_many(cfg.get("likely_in_title_patterns", []))
    borderline = compile_many(cfg.get("borderline_title_patterns", []))
    borderline_override = compile_many(cfg.get("borderline_override_title_patterns", []))
    specialist_out = compile_many(cfg.get("specialist_out_title_patterns", []))
    description_signals = [s.casefold() for s in cfg.get("description_signals", [])]
    description_min_hits = int(cfg.get("description_min_hits", 2))

    feed = latest_feed(args.input_dir)
    raw = pd.read_excel(feed, dtype=str).fillna("")
    if TITLE_COL not in raw.columns:
        raise SystemExit(f"Feed missing required title column {TITLE_COL}")

    classification_col = find_classification_col(list(raw.columns))
    area_lookup, fallback = load_geo_lookups(args.geo_lookup)
    assessable_markets, detail_rollups = load_assessable_markets(args.assessable_regions)

    rows: list[dict[str, Any]] = []
    for _, source in raw.iterrows():
        title = norm(source.get(TITLE_COL, ""))
        description = norm(source.get(DESCRIPTION_COL, ""))
        dlow = description.casefold()
        desc_hits = [s for s in description_signals if s in dlow]
        title_hit = any_match(broad_title, title)
        description_hit = len(desc_hits) >= description_min_hits and any_match(description_context, title)
        if not (title_hit or description_hit):
            continue

        period = norm(source.get(SALARY_PERIOD_COL, ""))
        annual_min = annualise(source.get(SALARY_MIN_COL, ""), period)
        annual_max = annualise(source.get(SALARY_MAX_COL, ""), period)
        description_annual_max = description_annualised_max(description)
        salary_evidence_source = "structured" if annual_min is not None or annual_max is not None else "description_fallback" if description_annual_max is not None else "missing"
        salary_out = any(v is not None and v > hard_max for v in (annual_min, annual_max, description_annual_max))

        if salary_out:
            provisional = "OUT_SALARY"
            reason = f"annualised salary exceeds £{hard_max:,.0f}"
        elif any_match(specialist_out, title):
            provisional = "OUT_SPECIALIST"
            reason = "specialist/senior title boundary"
        elif any_match(borderline_override, title):
            provisional = "BORDERLINE"
            reason = "mixed/ambiguous title requires advert-context review"
        elif any_match(likely_in, title):
            provisional = "LIKELY_IN"
            reason = "family title is a strong inclusion signal"
        elif any_match(borderline, title):
            provisional = "BORDERLINE"
            reason = "title needs advert-context review"
        else:
            provisional = "BORDERLINE"
            reason = "description-led family signal needs advert review"

        area = norm(source.get(AREA_COL, ""))
        location = norm(source.get(LOCATION_COL, ""))
        geo_cluster = ontap_region(area, location, area_lookup, fallback)
        assessable_market = detail_rollups.get(geo_cluster, geo_cluster)
        market_status = "YES" if assessable_market in assessable_markets else "NO"
        row = {
            "display_reference": norm(source.get(DISPLAY_REF_COL, "")),
            "title": title,
            "area": area,
            "location": location,
            "ontap_geo_cluster": geo_cluster,
            "assessable_market": assessable_market,
            "in_uk_market_universe": market_status,
            "jobg8_classification": norm(source.get(classification_col, "")) if classification_col else "",
            "salary_minimum_raw": norm(source.get(SALARY_MIN_COL, "")),
            "salary_maximum_raw": norm(source.get(SALARY_MAX_COL, "")),
            "salary_period": period,
            "annualised_minimum_estimate": annual_min,
            "annualised_maximum_estimate": annual_max,
            "description_annualised_maximum_estimate": description_annual_max,
            "salary_evidence_source": salary_evidence_source,
            "salary_bucket": salary_bucket(annual_min, annual_max if annual_max is not None else description_annual_max, hard_max),
            "discovery_source": "TITLE" if title_hit else "DESCRIPTION",
            "description_signal_count": len(desc_hits),
            "description_signals": "; ".join(desc_hits),
            "provisional_decision": provisional,
            "provisional_reason": reason,
            "description_excerpt": description[:700],
            "content_dedupe_key": content_dedupe_key(title, location, description),
        }
        row["dedupe_key"] = dedupe_key(row)
        rows.append(row)

    out = pd.DataFrame(rows)
    if out.empty:
        raise SystemExit(f"{display_name} discovery produced no candidates")

    out["is_duplicate"] = out.duplicated("dedupe_key", keep="first")
    out["is_content_duplicate"] = out.duplicated("content_dedupe_key", keep="first")
    ref_deduped = out.loc[~out["is_duplicate"]].copy()
    content_unique = out.loc[~out["is_duplicate"] & ~out["is_content_duplicate"]].copy()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    raw_csv = args.output_dir / f"jobg8-{key.replace('_', '-')}-discovery-current.csv"
    summary_md = args.output_dir / f"jobg8-{key.replace('_', '-')}-discovery-current.md"
    out.to_csv(raw_csv, index=False, encoding="utf-8-sig")

    decision_counts = Counter(content_unique["provisional_decision"])
    likely_n = decision_counts.get("LIKELY_IN", 0)
    borderline_n = decision_counts.get("BORDERLINE", 0)
    out_n = decision_counts.get("OUT_SPECIALIST", 0) + decision_counts.get("OUT_SALARY", 0)
    estimate = likely_n + round(borderline_n * 0.5)
    lower = likely_n
    upper = likely_n + borderline_n
    if upper < floor:
        viability = "STOP / VERY THIN"
    elif estimate < floor:
        viability = "CAUTION / LIKELY BELOW GATE"
    elif lower >= floor:
        viability = "GO / SCALE CLEAR"
    else:
        viability = "GO TO BOUNDARY SAMPLE / SCALE PLAUSIBLE"

    salary_counts = content_unique["salary_bucket"].value_counts()
    class_counts = content_unique["jobg8_classification"].replace("", "(blank)").value_counts().head(20)
    market_counts = content_unique["assessable_market"].replace("", "Other / Unknown").value_counts().head(30)
    assessable_yes = int((content_unique["in_uk_market_universe"] == "YES").sum())
    assessable_no = len(content_unique) - assessable_yes

    reference_dupes = int(out["is_duplicate"].sum())
    content_dupes = int((~out["is_duplicate"] & out["is_content_duplicate"]).sum())
    lines = [
        f"# JobG8 {display_name} family discovery", "",
        f"Feed: **{feed.name}**",
        f"Jobs in feed: **{len(raw):,}**",
        f"Raw broad possible universe before exclusions/dedupe: **{len(out):,}**",
        f"Reference-key duplicates within broad universe: **{reference_dupes:,}**",
        f"Reference-deduped broad universe: **{len(ref_deduped):,}**",
        f"Additional cross-reference content duplicates: **{content_dupes:,}**",
        f"Content-unique broad universe: **{len(content_unique):,}**", "",
        "This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.",
        "All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.",
        f"Salary rule applied diagnostically: **over £{hard_max:,.0f} = OUT; exactly £{hard_max:,.0f} is not excluded; missing salary is retained.**", "",
        "## Early volume viability gate", "",
        f"Provisional LIKELY_IN: **{likely_n:,}**",
        f"Provisional BORDERLINE: **{borderline_n:,}**",
        f"Provisional OUT (specialist/salary): **{out_n:,}**",
        f"Estimated genuine inventory before deep advert review: **~{estimate:,}** (working range **{lower:,}–{upper:,}**).",
        f"Viability floor: **~{floor:,} genuine jobs nationally**.",
        f"Early verdict: **{viability}**.", "",
        "## Provisional decision breakdown", "", "| Decision | Content-unique jobs |", "|---|---:|",
    ]
    for decision, count in decision_counts.most_common():
        lines.append(f"| {decision} | {count:,} |")

    lines += ["", "## Salary distribution — content-unique broad universe", "", "| Salary bucket | Jobs |", "|---|---:|"]
    for bucket, count in salary_counts.items():
        lines.append(f"| {bucket} | {count:,} |")

    lines += ["", "## JobG8 classifications feeding the seam", "", f"Classification column: **{classification_col or 'NONE'}**", "", "| JobG8 classification | Jobs |", "|---|---:|"]
    for name, count in class_counts.items():
        lines.append(f"| {str(name).replace('|', '/')} | {count:,} |")

    lines += [
        "", "## Geography — evidence only, not an occupational gate", "",
        f"Canonical UK assessment universe: **{len(assessable_markets):,} markets**.",
        f"Content-unique candidates mapping into that UK market universe: **{assessable_yes:,}**.",
        f"Content-unique candidates outside it or unresolved: **{assessable_no:,}**.",
        "The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.",
        "Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.", "",
        "| Assessable market / geo result | Jobs | In UK market universe? |", "|---|---:|---|",
    ]
    for market, count in market_counts.items():
        lines.append(f"| {str(market).replace('|', '/')} | {count:,} | {'YES' if market in assessable_markets else 'NO'} |")

    lines += [
        "", "## Next gate", "",
        "If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.",
        "If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.",
    ]
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(summary_md.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

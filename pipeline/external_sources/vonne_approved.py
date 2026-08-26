"""Build an explicitly approved VONNE output after an exact same-day review.

This is a separate approval stage from ``vonne_poc``.  It re-fetches the live
VONNE vacancy set, repeats the geography and duplicate checks, requires the
same vacancy fingerprint and explicit select/exclude decisions for every
reviewable vacancy, then writes only short Ontap-authored records assembled
from factual source fields.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import tempfile
import urllib.parse
from datetime import datetime, time as datetime_time
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

from external_sources.northeast_jobs_poc import (
    COMBINED_TARGET_REGION,
    ManualDecisionState,
    clean_text,
    deduplicate_within_source,
    load_geo_lookup,
    load_jobg8_candidates,
)
from external_sources.vonne_poc import (
    LIST_URL,
    VonneVacancy,
    build_vacancies,
    classify,
    deduplicate_jobg8,
    deduplicate_nejobs,
    fetch_text,
    load_manual_decisions_from_markdown,
    load_nejobs_candidates,
    parse_listing,
    review_fingerprint,
    review_row,
    vacancy_review_fingerprint,
    write_csv,
    write_summary,
)

APPROVAL_CONFIRMATION = "PUBLISH"
MAX_UNDECIDED_VACANCIES = 10
DEFAULT_APPROVED_JSON = Path("output-external/vonne-admin-service.json")
LONDON = ZoneInfo("Europe/London")


def parse_vonne_deadline(value: str) -> datetime | None:
    """Parse only date formats observed in factual VONNE deadline fields."""
    text = clean_text(value)
    if not text:
        return None
    text = text.replace("–", "-").replace("—", "-")
    formats = (
        ("%A, %B %d, %Y - %H:%M", False),
        ("%A, %b %d, %Y - %H:%M", False),
        ("%d %B %Y - %H:%M", False),
        ("%d %b %Y - %H:%M", False),
        ("%d %B %Y", True),
        ("%d %b %Y", True),
        ("%Y-%m-%dT%H:%M:%S%z", False),
        ("%Y-%m-%dT%H:%M:%S", False),
        ("%Y-%m-%d", True),
    )
    for date_format, date_only in formats:
        try:
            parsed = datetime.strptime(text, date_format)
        except ValueError:
            continue
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=LONDON)
        else:
            parsed = parsed.astimezone(LONDON)
        if date_only:
            parsed = datetime.combine(
                parsed.date(),
                datetime_time(23, 59, 59),
                tzinfo=LONDON,
            )
        return parsed
    return None


def source_date_iso(value: str) -> str:
    parsed = parse_vonne_deadline(value)
    return parsed.date().isoformat() if parsed else ""


def source_deadline_iso(value: str) -> str:
    parsed = parse_vonne_deadline(value)
    return parsed.isoformat(timespec="seconds") if parsed else ""


def vacancy_is_open(
    vacancy: VonneVacancy,
    *,
    now: datetime | None = None,
) -> bool:
    deadline = parse_vonne_deadline(vacancy.closing_date)
    if deadline is None:
        return False
    current = now or datetime.now(LONDON)
    if current.tzinfo is None:
        current = current.replace(tzinfo=LONDON)
    return deadline >= current.astimezone(LONDON)


def append_referral_parameters(url: str) -> str:
    parsed = urllib.parse.urlsplit(clean_text(url))
    retained = [
        (key, value)
        for key, value in urllib.parse.parse_qsl(
            parsed.query,
            keep_blank_values=True,
        )
        if key.casefold() not in {"utm_source", "utm_medium", "utm_campaign"}
    ]
    retained.extend(
        (
            ("utm_source", "ontap"),
            ("utm_medium", "referral"),
            ("utm_campaign", "vonne_external"),
        )
    )
    return urllib.parse.urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            urllib.parse.urlencode(retained),
            parsed.fragment,
        )
    )


def public_location(vacancy: VonneVacancy) -> str:
    location = clean_text(vacancy.location)
    based = clean_text(vacancy.based)
    location_key = location.casefold()
    based_key = based.casefold()
    generic_based = {
        "regionwide",
        "region wide",
        "hybrid",
        "home-based",
        "home based",
        "remote",
        "not stated",
    }
    broad_locations = generic_based | {
        "tyne and wear",
        "north east",
        "north-east",
    }
    if based and based_key not in generic_based and location_key in broad_locations:
        suffix = ""
        if location_key == "hybrid":
            suffix = " (hybrid)"
        elif location_key in {"home-based", "home based", "remote"}:
            suffix = " (home-based)"
        elif location_key in {"regionwide", "region wide"}:
            suffix = " / Regionwide"
        return based + suffix
    if location_key == "hybrid":
        return "North East (hybrid)"
    if location_key in {"home-based", "home based", "remote"}:
        return "North East (home-based)"
    return location or based or COMBINED_TARGET_REGION


def working_arrangement(vacancy: VonneVacancy) -> dict[str, str]:
    evidence = " ".join(
        value
        for value in (
            clean_text(vacancy.location),
            clean_text(vacancy.based),
            clean_text(vacancy.hours),
        )
        if value
    )
    key = evidence.casefold()
    if "hybrid" in key:
        return {
            "working_arrangement": "hybrid",
            "working_arrangement_text": "Hybrid working indicated",
            "working_arrangement_evidence": (
                "The source vacancy's factual location or based field "
                "indicates hybrid working."
            ),
        }
    if any(marker in key for marker in ("home-based", "home based", "remote")):
        return {
            "working_arrangement": "partly_remote",
            "working_arrangement_text": "Home-based working indicated",
            "working_arrangement_evidence": (
                "The source vacancy's factual location or based field "
                "indicates home-based working."
            ),
        }
    return {
        "working_arrangement": "onsite_or_not_stated",
        "working_arrangement_text": "",
        "working_arrangement_evidence": "",
    }


def vacancy_summary(vacancy: VonneVacancy) -> str:
    opening = (
        f"{clean_text(vacancy.title)} with "
        f"{clean_text(vacancy.employer)} in {public_location(vacancy)}"
    )
    facts = [
        clean_text(vacancy.contract_type),
        clean_text(vacancy.hours),
        clean_text(vacancy.salary_text),
    ]
    fact_text = "; ".join(value for value in facts if value)
    return f"{opening}. {fact_text}." if fact_text else f"{opening}."


def vacancy_description(vacancy: VonneVacancy) -> str:
    employer = clean_text(vacancy.employer) or "The named employer"
    location = public_location(vacancy)
    title = clean_text(vacancy.title)
    terms = [
        clean_text(vacancy.contract_type),
        clean_text(vacancy.role_type),
        clean_text(vacancy.hours),
    ]
    terms = [value for value in terms if value]
    lines = [
        f"{employer} is recruiting for this vacancy in {location}.",
        f"The advertised position is {title}."
        + (f" The listed working terms are {'; '.join(terms)}." if terms else ""),
    ]
    salary = clean_text(vacancy.salary_text)
    if salary:
        lines.append(f"The advertised salary is {salary}.")
    closing = clean_text(vacancy.closing_date)
    if closing:
        lines.append(f"The stated application deadline is {closing}.")
    lines.append(
        "Use the original VONNE advert to check the complete duties, person "
        "specification and application requirements."
    )
    return "\n\n".join(lines)


def vacancy_to_published_job(vacancy: VonneVacancy) -> dict[str, str]:
    row = {
        "job_id": f"vonne-{vacancy.source_job_id}",
        "title": clean_text(vacancy.title),
        "company": clean_text(vacancy.employer),
        "location": public_location(vacancy),
        "region": COMBINED_TARGET_REGION,
        "country": "UK",
        "category": "Admin/Service – Office Support",
        "employment_type": clean_text(vacancy.contract_type),
        "salary_min": "",
        "salary_max": "",
        "salary_text": clean_text(vacancy.salary_text),
        "work_pattern": clean_text(vacancy.hours),
        "posted_date": "",
        "closing_date": source_date_iso(vacancy.closing_date),
        "closing_datetime": source_deadline_iso(vacancy.closing_date),
        "summary": vacancy_summary(vacancy),
        "description": vacancy_description(vacancy),
        "apply_url": append_referral_parameters(vacancy.source_url),
        "source": "VONNE",
    }
    row.update(working_arrangement(vacancy))
    return row


LEGACY_REVIEW_FIELDS = (
    "title",
    "salary_text",
    "employer",
    "location",
    "based",
    "closing_date",
    "contract_type",
    "role_type",
    "hours",
    "role_description",
    "classification",
    "classification_reason",
    "geography_status",
    "geography_reason",
    "ontap_geography",
    "jobg8_check",
    "jobg8_candidate_title",
    "jobg8_candidate_employer",
    "jobg8_match_score",
    "nejobs_check",
    "nejobs_candidate_title",
    "nejobs_candidate_employer",
    "nejobs_match_score",
    "vonne_duplicate_check",
    "source_job_id",
    "source_url",
    "detail_status",
)


def legacy_review_fingerprint(row: dict[str, str]) -> str:
    """Fingerprint the fields available in pre-change VONNE review CSVs."""
    payload = {
        field: clean_text(row.get(field, ""))
        for field in LEGACY_REVIEW_FIELDS
    }
    serialised = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(serialised.encode("utf-8")).hexdigest()


def load_reviewed_vacancy_fingerprints(
    summary_path: Path,
    report_path: Path,
) -> dict[str, str]:
    """Load per-job review evidence, with one safe legacy CSV transition."""
    markers: dict[str, str] = {}
    if summary_path.exists():
        try:
            text = summary_path.read_text(encoding="utf-8-sig")
        except OSError:
            text = ""
        for block in re.findall(
            r"(?ms)^---\s*$\n(.*?)^---\s*$",
            text,
        ):
            id_match = re.search(
                r"(?mi)^source_job_id:\s*([^\s]+)\s*$",
                block,
            )
            fingerprint_match = re.search(
                r"(?mi)^vacancy_fingerprint:\s*([a-f0-9]{64})\s*$",
                block,
            )
            if id_match and fingerprint_match:
                markers[clean_text(id_match.group(1))] = (
                    "full:" + fingerprint_match.group(1)
                )
        if markers:
            return markers

    if not report_path.exists():
        return markers
    try:
        with report_path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as handle:
            for row in csv.DictReader(handle):
                source_job_id = clean_text(row.get("source_job_id", ""))
                if not source_job_id:
                    continue
                fingerprint = clean_text(
                    row.get("vacancy_fingerprint", "")
                )
                if re.fullmatch(r"[a-f0-9]{64}", fingerprint):
                    markers[source_job_id] = "full:" + fingerprint
                else:
                    markers[source_job_id] = (
                        "legacy:" + legacy_review_fingerprint(row)
                    )
    except OSError:
        return {}
    return markers


def reviewed_marker_matches(
    vacancy: VonneVacancy,
    marker: str,
) -> bool:
    if marker.startswith("full:"):
        return marker == "full:" + vacancy_review_fingerprint(vacancy)
    if marker.startswith("legacy:"):
        return marker == "legacy:" + legacy_review_fingerprint(
            review_row(vacancy)
        )
    return False


def publication_withheld_ids(
    vacancies: Iterable[VonneVacancy],
    decisions: ManualDecisionState,
    reviewed_fingerprints: dict[str, str] | None = None,
) -> set[str]:
    """Return undecided or changed jobs that must fail closed individually."""
    rows = list(vacancies)
    current_review_ids = {
        vacancy.source_job_id
        for vacancy in rows
        if vacancy.classification != "HARD_PASS"
    }
    withheld = (
        current_review_ids
        - decisions.selections
        - decisions.exclusions
    )
    if decisions.review_fingerprint == review_fingerprint(rows):
        return withheld

    markers = reviewed_fingerprints or {}
    by_id = {vacancy.source_job_id: vacancy for vacancy in rows}
    for source_job_id in decisions.selections & current_review_ids:
        marker = markers.get(source_job_id, "")
        if not marker or not reviewed_marker_matches(
            by_id[source_job_id],
            marker,
        ):
            withheld.add(source_job_id)
    return withheld


def approval_errors(
    vacancies: Iterable[VonneVacancy],
    decisions: ManualDecisionState,
    *,
    review_date: str,
    failures: Iterable[str],
    reviewed_fingerprints: dict[str, str] | None = None,
    max_undecided: int = MAX_UNDECIDED_VACANCIES,
) -> list[str]:
    """Validate the source while isolating a small undecided job queue."""
    rows = list(vacancies)
    errors: list[str] = []
    if decisions.review_date != review_date:
        errors.append("the Markdown review is not dated today")
    if decisions.load_warning:
        errors.append(decisions.load_warning)
    if not decisions.review_fingerprint:
        errors.append("the Markdown review has no vacancy-set fingerprint")

    current_review_ids = {
        vacancy.source_job_id
        for vacancy in rows
        if vacancy.classification != "HARD_PASS"
    }
    withheld = publication_withheld_ids(
        rows,
        decisions,
        reviewed_fingerprints,
    )
    if len(withheld) > max_undecided:
        errors.append(
            f"{len(withheld)} VONNE vacancies are undecided or changed, "
            f"exceeding the job-level quarantine limit of {max_undecided} "
            "(withheld IDs: " + ", ".join(sorted(withheld)) + ")"
        )

    failures_list = list(failures)
    if failures_list:
        errors.append(
            f"{len(failures_list)} detail page(s) failed; approved output is blocked"
        )

    by_id = {vacancy.source_job_id: vacancy for vacancy in rows}
    safe_selected_ids = (
        decisions.selections & current_review_ids
    ) - withheld
    for source_job_id in sorted(safe_selected_ids):
        vacancy = by_id[source_job_id]
        missing = [
            label
            for label, value in (
                ("title", vacancy.title),
                ("employer", vacancy.employer),
                ("location", vacancy.location or vacancy.based),
                ("closing date", vacancy.closing_date),
                ("source URL", vacancy.source_url),
            )
            if not clean_text(value)
        ]
        if missing:
            errors.append(
                f"selected VONNE ID {source_job_id} is missing factual fields: "
                + ", ".join(missing)
            )
        if parse_vonne_deadline(vacancy.closing_date) is None:
            errors.append(
                f"selected VONNE ID {source_job_id} has an unparseable closing date"
            )
        if vacancy.duplicate_status == "DUPLICATE":
            errors.append(
                f"selected VONNE ID {source_job_id} is a confirmed JobG8 duplicate"
            )
        if vacancy.nejobs_duplicate_status == "DUPLICATE":
            errors.append(
                f"selected VONNE ID {source_job_id} is a confirmed NEJobs duplicate"
            )
    return errors


def approved_output_rows(
    vacancies: Iterable[VonneVacancy],
    decisions: ManualDecisionState,
    *,
    now: datetime | None = None,
    withheld_ids: Iterable[str] = (),
) -> list[dict[str, str]]:
    withheld = set(withheld_ids)
    selected = [
        vacancy
        for vacancy in vacancies
        if vacancy.source_job_id in decisions.selections
        and vacancy.source_job_id not in withheld
        and vacancy.classification != "HARD_PASS"
        and vacancy_is_open(vacancy, now=now)
    ]
    rows = [vacancy_to_published_job(vacancy) for vacancy in selected]
    return sorted(
        rows,
        key=lambda row: (
            row["closing_date"],
            row["title"].casefold(),
            row["job_id"],
        ),
    )


def write_json_atomic(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    handle, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as temp:
            temp.write(content)
            temp.flush()
            os.fsync(temp.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobg8", type=Path, default=Path("input/jobg8.xlsx"))
    parser.add_argument(
        "--geo-lookup",
        type=Path,
        default=Path("geo/geo_lookup.xlsx"),
    )
    parser.add_argument(
        "--nejobs-json",
        type=Path,
        default=Path("output-external/northeast-jobs-admin-service.json"),
    )
    parser.add_argument("--listing-file", type=Path)
    parser.add_argument("--details-dir", type=Path)
    parser.add_argument("--fetch-live", action="store_true")
    parser.add_argument("--acknowledge-source-terms", action="store_true")
    parser.add_argument("--request-interval", type=float, default=0.5)
    parser.add_argument("--max-detail-requests", type=int, default=60)
    parser.add_argument("--salary-review-threshold", type=float, default=30_000)
    parser.add_argument(
        "--report-csv",
        type=Path,
        default=Path("reviews/external/vonne-review.csv"),
    )
    parser.add_argument(
        "--summary-md",
        type=Path,
        default=Path("reviews/external/vonne-summary.md"),
    )
    parser.add_argument(
        "--approved-json",
        type=Path,
        default=DEFAULT_APPROVED_JSON,
    )
    parser.add_argument("--write-approved-json", action="store_true")
    parser.add_argument("--confirm-approved", default="")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.write_approved_json:
        raise SystemExit(
            "STOP: this module is the approval stage; add --write-approved-json "
            "only after reviewing today's VONNE summary."
        )
    if args.confirm_approved != APPROVAL_CONFIRMATION:
        raise SystemExit("STOP: approval confirmation must be exactly PUBLISH.")
    if args.fetch_live and not args.acknowledge_source_terms:
        raise SystemExit(
            "STOP: live fetching requires explicit acknowledgement that "
            "VONNE's source terms have been reviewed."
        )
    if not args.fetch_live and args.listing_file is None:
        raise SystemExit(
            "STOP: provide --listing-file or explicitly opt into --fetch-live."
        )

    if args.listing_file:
        listing_text = args.listing_file.read_text(encoding="utf-8")
        listing_source = str(args.listing_file)
    else:
        listing_text = fetch_text(LIST_URL)
        listing_source = LIST_URL
    items = parse_listing(listing_text)
    if not items:
        raise SystemExit(
            "STOP: no VONNE listings parsed; source structure may have changed."
        )

    area_map, fallback_map = load_geo_lookup(args.geo_lookup)
    vacancies, counts, failures = build_vacancies(
        items,
        area_map=area_map,
        fallback_map=fallback_map,
        details_dir=args.details_dir,
        fetch_live=args.fetch_live,
        request_interval=max(args.request_interval, 0.0),
        max_detail_requests=max(args.max_detail_requests, 0),
    )
    jobg8_jobs = load_jobg8_candidates(
        args.jobg8,
        area_map,
        fallback_map,
    )
    nejobs_jobs = load_nejobs_candidates(args.nejobs_json)
    for vacancy in vacancies:
        deduplicate_jobg8(vacancy, jobg8_jobs)
        deduplicate_nejobs(vacancy, nejobs_jobs)
    deduplicate_within_source(vacancies)
    for vacancy in vacancies:
        classify(vacancy, args.salary_review_threshold)

    review_date = datetime.now(LONDON).date().isoformat()
    decisions = load_manual_decisions_from_markdown(
        args.summary_md,
        review_date,
    )
    reviewed_fingerprints = load_reviewed_vacancy_fingerprints(
        args.summary_md,
        args.report_csv,
    )
    write_csv(args.report_csv, vacancies, decisions)
    write_summary(
        args.summary_md,
        counts=counts,
        vacancies=vacancies,
        decisions=decisions,
        review_date=review_date,
        jobg8_count=len(jobg8_jobs),
        nejobs_count=len(nejobs_jobs),
        listing_source=listing_source,
        failures=failures,
    )

    errors = approval_errors(
        vacancies,
        decisions,
        review_date=review_date,
        failures=failures,
        reviewed_fingerprints=reviewed_fingerprints,
    )
    if errors:
        raise SystemExit(
            "STOP: VONNE approved output was not written:\n- "
            + "\n- ".join(errors)
        )

    withheld = publication_withheld_ids(
        vacancies,
        decisions,
        reviewed_fingerprints,
    )
    rows = approved_output_rows(
        vacancies,
        decisions,
        withheld_ids=withheld,
    )
    write_json_atomic(args.approved_json, rows)
    if withheld:
        print(
            f"VONNE warning: withheld {len(withheld)} undecided or changed "
            "vacancy(s): " + ", ".join(sorted(withheld))
        )
    print(
        f"Approved VONNE output wrote {len(rows)} open selected jobs to "
        f"{args.approved_json}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

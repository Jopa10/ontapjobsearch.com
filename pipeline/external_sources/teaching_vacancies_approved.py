"""Build explicitly approved Teaching Vacancies output after an exact review.

The review workflow remains read-only. This approval stage re-fetches the same
bounded West Yorkshire search, requires the same review date, reviewable IDs and
factual/classification fingerprint, then writes only the selected, still-open
vacancies. Blank POSS rows remain unpublished.
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
import urllib.parse
from datetime import datetime, time as datetime_time
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

from external_sources import teaching_vacancies_etl as etl
from external_sources import teaching_vacancies_poc as poc

APPROVAL_CONFIRMATION = "PUBLISH"
DEFAULT_APPROVED_JSON = Path(
    "output-external/west-yorkshire-teaching-vacancies-admin-service.json"
)
SOURCE_CODE = "Teaching Vacancies"
REGION = "Yorkshire - West"
LONDON = ZoneInfo("Europe/London")


def parse_source_datetime(
    value: str,
    *,
    end_of_day_when_date_only: bool = False,
) -> datetime | None:
    text = poc.clean(value)
    if not text:
        return None
    candidate = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        parsed = None
    if parsed is None:
        for date_format in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%d %H:%M"):
            try:
                parsed = datetime.strptime(text, date_format)
            except ValueError:
                continue
            if (
                end_of_day_when_date_only
                and date_format in ("%Y-%m-%d", "%d/%m/%Y")
            ):
                parsed = datetime.combine(
                    parsed.date(),
                    datetime_time(23, 59, 59),
                )
            break
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=LONDON)
    return parsed.astimezone(LONDON)


def source_date_iso(value: str) -> str:
    parsed = parse_source_datetime(value)
    return parsed.date().isoformat() if parsed else ""


def source_deadline_iso(value: str) -> str:
    parsed = parse_source_datetime(value, end_of_day_when_date_only=True)
    return parsed.isoformat(timespec="seconds") if parsed else ""


def vacancy_is_open(
    vacancy: poc.Vacancy,
    *,
    now: datetime | None = None,
) -> bool:
    deadline = parse_source_datetime(
        vacancy.closing_date,
        end_of_day_when_date_only=True,
    )
    if deadline is None:
        return False
    current = now or datetime.now(LONDON)
    if current.tzinfo is None:
        current = current.replace(tzinfo=LONDON)
    return deadline >= current.astimezone(LONDON)


def append_referral_parameters(url: str) -> str:
    parsed = urllib.parse.urlsplit(poc.clean(url))
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
            ("utm_campaign", "teaching_vacancies_external"),
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


def public_location(value: str) -> str:
    location = poc.clean(value)
    return poc.clean(location.split(",", 1)[0]) or location


def humanise_employment_type(value: str) -> str:
    text = poc.clean(value).replace("_", " ").casefold()
    return text[:1].upper() + text[1:] if text else ""


def working_arrangement(vacancy: poc.Vacancy) -> dict[str, str]:
    evidence = " ".join(
        value
        for value in (
            poc.clean(vacancy.location),
            poc.clean(vacancy.description_excerpt),
        )
        if value
    )
    key = evidence.casefold()
    if "hybrid" in key:
        return {
            "working_arrangement": "hybrid",
            "working_arrangement_text": "Hybrid working indicated",
            "working_arrangement_evidence": (
                "The source vacancy's factual location or advert text "
                "indicates hybrid working."
            ),
        }
    if any(marker in key for marker in ("home-based", "home based", "remote")):
        return {
            "working_arrangement": "partly_remote",
            "working_arrangement_text": "Home-based working indicated",
            "working_arrangement_evidence": (
                "The source vacancy's factual location or advert text "
                "indicates home-based working."
            ),
        }
    return {
        "working_arrangement": "onsite_or_not_stated",
        "working_arrangement_text": "",
        "working_arrangement_evidence": "",
    }


def vacancy_summary(vacancy: poc.Vacancy) -> str:
    opening = (
        f"{poc.clean(vacancy.title)} with {poc.clean(vacancy.employer)} "
        f"in {public_location(vacancy.location)}"
    )
    facts = [
        humanise_employment_type(vacancy.employment_type),
        poc.clean(vacancy.salary_text),
    ]
    fact_text = "; ".join(value for value in facts if value)
    return f"{opening}. {fact_text}." if fact_text else f"{opening}."


def vacancy_description(vacancy: poc.Vacancy) -> str:
    employer = poc.clean(vacancy.employer) or "The named school or trust"
    title = poc.clean(vacancy.title)
    location = public_location(vacancy.location)
    lines = [
        f"{employer} is recruiting for this vacancy in {location}.",
        f"The advertised position is {title}.",
    ]
    employment_type = humanise_employment_type(vacancy.employment_type)
    if employment_type:
        lines.append(f"The source lists the employment type as {employment_type}.")
    salary = poc.clean(vacancy.salary_text)
    if salary:
        lines.append(f"The advertised salary or pay scale is {salary}.")
    closing = poc.clean(vacancy.closing_date)
    if closing:
        lines.append(f"The stated application deadline is {closing}.")
    lines.append(
        "Use the original Teaching Vacancies advert to check the complete "
        "duties, person specification and application requirements."
    )
    return "\n\n".join(lines)


def vacancy_to_published_job(vacancy: poc.Vacancy) -> dict[str, str]:
    row = {
        "job_id": f"teaching-vacancies-{vacancy.source_job_id}",
        "title": poc.clean(vacancy.title),
        "company": poc.clean(vacancy.employer),
        "location": public_location(vacancy.location),
        "region": REGION,
        "country": "UK",
        "category": "Admin/Service – Office Support",
        "employment_type": humanise_employment_type(vacancy.employment_type),
        "salary_min": "",
        "salary_max": "",
        "salary_text": poc.clean(vacancy.salary_text),
        "work_pattern": "",
        "posted_date": source_date_iso(vacancy.posted_date),
        "closing_date": source_date_iso(vacancy.closing_date),
        "closing_datetime": source_deadline_iso(vacancy.closing_date),
        "summary": vacancy_summary(vacancy),
        "description": vacancy_description(vacancy),
        "apply_url": append_referral_parameters(vacancy.source_url),
        "source": SOURCE_CODE,
    }
    row.update(working_arrangement(vacancy))
    return row


def approval_errors(
    vacancies: Iterable[poc.Vacancy],
    decisions: poc.ManualDecisionState,
    *,
    review_date: str,
    failures: Iterable[str],
) -> list[str]:
    rows = list(vacancies)
    errors: list[str] = []
    if decisions.review_date != review_date:
        errors.append("the Markdown review is not dated today")
    if decisions.load_warning:
        errors.append(decisions.load_warning)

    current_review_ids = {
        vacancy.source_job_id
        for vacancy in rows
        if vacancy.classification != "HARD_PASS"
    }
    if decisions.reviewed_ids != current_review_ids:
        added = sorted(current_review_ids - decisions.reviewed_ids)
        removed = sorted(decisions.reviewed_ids - current_review_ids)
        detail: list[str] = []
        if added:
            detail.append("new IDs: " + ", ".join(added))
        if removed:
            detail.append("missing IDs: " + ", ".join(removed))
        errors.append(
            "the live reviewable Teaching Vacancies set differs from the reviewed set"
            + (f" ({'; '.join(detail)})" if detail else "")
        )

    current_fingerprint = poc.review_fingerprint(rows)
    if not decisions.review_fingerprint:
        errors.append("the Markdown review has no vacancy-set fingerprint")
    elif decisions.review_fingerprint != current_fingerprint:
        errors.append(
            "the live Teaching Vacancies facts or classifications differ from "
            "the reviewed vacancy-set fingerprint"
        )

    failures_list = list(failures)
    if failures_list:
        errors.append(
            f"{len(failures_list)} detail page(s) failed; approved output is blocked"
        )

    by_id = {vacancy.source_job_id: vacancy for vacancy in rows}
    selected_ids = {
        vacancy.source_job_id
        for vacancy in rows
        if poc.final_decision_for(vacancy, decisions) == "SELECTED"
    }
    for source_job_id in sorted(selected_ids):
        vacancy = by_id[source_job_id]
        missing = [
            label
            for label, value in (
                ("title", vacancy.title),
                ("employer", vacancy.employer),
                ("location", vacancy.location),
                ("salary or pay scale", vacancy.salary_text),
                ("closing date", vacancy.closing_date),
                ("source URL", vacancy.source_url),
            )
            if not poc.clean(value)
        ]
        if missing:
            errors.append(
                f"selected Teaching Vacancies ID {source_job_id} is missing factual fields: "
                + ", ".join(missing)
            )
        if parse_source_datetime(
            vacancy.closing_date,
            end_of_day_when_date_only=True,
        ) is None:
            errors.append(
                f"selected Teaching Vacancies ID {source_job_id} has an "
                "unparseable closing date"
            )
        if vacancy.jobg8_check == "DUPLICATE":
            errors.append(
                f"selected Teaching Vacancies ID {source_job_id} is a confirmed "
                "JobG8 duplicate"
            )
    return errors


def approved_output_rows(
    vacancies: Iterable[poc.Vacancy],
    decisions: poc.ManualDecisionState,
    *,
    now: datetime | None = None,
) -> list[dict[str, str]]:
    selected = [
        vacancy
        for vacancy in vacancies
        if poc.final_decision_for(vacancy, decisions) == "SELECTED"
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
    parser.add_argument("--fetch-live", action="store_true")
    parser.add_argument("--max-pages", type=int, default=2)
    parser.add_argument(
        "--jobg8-json",
        type=Path,
        default=Path("output-admin-service/west-yorkshire-admin-service.json"),
    )
    parser.add_argument(
        "--summary-md",
        type=Path,
        default=Path(
            "reviews/external/west-yorkshire-teaching-vacancies-summary.md"
        ),
    )
    parser.add_argument(
        "--approved-json",
        type=Path,
        default=DEFAULT_APPROVED_JSON,
    )
    parser.add_argument("--write-approved-json", action="store_true")
    parser.add_argument("--confirm-approved", default="")
    return parser.parse_args(argv)


def fetch_review_set(
    *,
    max_pages: int,
    jobg8_json: Path,
) -> tuple[list[poc.Vacancy], list[str]]:
    etl.install_patches()
    urls = poc.live_urls(max_pages)
    parsed: list[poc.Vacancy] = []
    failures: list[str] = []
    for url in urls:
        try:
            parsed.append(poc.parse_jobposting(poc.request_text(url), url))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"{url} — {type(exc).__name__}")
    reviewed = poc.process(parsed, poc.load_jobg8(jobg8_json))
    return reviewed, failures


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.write_approved_json:
        raise SystemExit(
            "STOP: this module is the approval stage; add --write-approved-json "
            "only after reviewing today's Teaching Vacancies summary."
        )
    if args.confirm_approved != APPROVAL_CONFIRMATION:
        raise SystemExit("STOP: approval confirmation must be exactly PUBLISH.")
    if not args.fetch_live:
        raise SystemExit("STOP: Teaching Vacancies approval requires --fetch-live.")

    review_date = datetime.now(LONDON).date().isoformat()
    decisions = poc.load_manual_decisions_from_markdown(
        args.summary_md,
        review_date,
    )
    vacancies, failures = fetch_review_set(
        max_pages=max(args.max_pages, 1),
        jobg8_json=args.jobg8_json,
    )
    errors = approval_errors(
        vacancies,
        decisions,
        review_date=review_date,
        failures=failures,
    )
    if errors:
        raise SystemExit(
            "STOP: Teaching Vacancies approved output was not written:\n- "
            + "\n- ".join(errors)
        )

    rows = approved_output_rows(vacancies, decisions)
    write_json_atomic(args.approved_json, rows)
    print(
        f"Approved Teaching Vacancies output wrote {len(rows)} open selected jobs "
        f"to {args.approved_json}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

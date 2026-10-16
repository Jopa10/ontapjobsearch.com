#!/usr/bin/env python3
"""Send one daily digest of new JobG8 CPC jobs matching Brevo alert contacts."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import html
import hmac
import json
import os
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

BREVO_API = "https://api.brevo.com/v3"
CPC_HOST = "www.jobg8.com"
CPC_PATH = "/traffic.aspx"
PAGE_SIZE = 500
MAX_JOBS_PER_EMAIL = 20


class DeliveryError(RuntimeError):
    pass


def normalise(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    plain = "".join(char for char in decomposed if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", plain)).strip()


def is_cpc_job(source: str, apply_url: str) -> bool:
    try:
        parts = urlsplit(apply_url)
    except ValueError:
        return False
    return (
        source.strip().casefold() == "jobg8"
        and parts.scheme.casefold() == "https"
        and parts.hostname is not None
        and parts.hostname.casefold() == CPC_HOST
        and parts.path.casefold() == CPC_PATH
    )


def _salary_range(value: str) -> tuple[float, float, str] | None:
    lowered = value.casefold()
    numbers = []
    for raw in re.findall(r"(?<![a-z])\d[\d,]*(?:\.\d+)?\s*k?", lowered):
        multiplier = 1000 if raw.endswith("k") else 1
        number = float(raw.rstrip("k").replace(",", "")) * multiplier
        numbers.append(number)
    if not numbers:
        return None

    period = ""
    for key, label in (
        (r"\b(?:hour|hourly|per hour|p\.?h\.?)\b", "hour"),
        (r"\b(?:day|daily|per day)\b", "day"),
        (r"\b(?:week|weekly|per week)\b", "week"),
        (r"\b(?:month|monthly|per month)\b", "month"),
        (r"\b(?:year|yearly|annual|annually|per year|p\.?a\.?)\b", "year"),
    ):
        if re.search(key, lowered):
            period = label
            break
    return min(numbers), max(numbers), period


def _salary_matches(preference: str, job_salary: str) -> bool:
    preferred = _salary_range(preference)
    advertised = _salary_range(job_salary)
    # Keep jobs with no comparable published salary; do not invent an amount.
    if not preferred or not advertised:
        return True
    preferred_low, preferred_high, preferred_period = preferred
    job_low, job_high, job_period = advertised
    if preferred_period and job_period and preferred_period != job_period:
        return False
    return job_low <= preferred_high and job_high >= preferred_low


def matches_alert(contact_attributes: dict[str, Any], job: dict[str, Any]) -> bool:
    role = normalise(str(contact_attributes.get("ALERT_ROLE") or ""))
    location = normalise(str(contact_attributes.get("ALERT_LOCATION") or ""))
    if not role or not location:
        return False

    role_terms = role.split()
    job_text = normalise(" ".join(
        str(job.get(field) or "")
        for field in ("title", "category", "description", "full_description")
    ))
    if not all(term in job_text for term in role_terms):
        return False

    job_location = normalise(str(job.get("location") or ""))
    job_region = normalise(str(job.get("region") or ""))
    if not any(location in candidate or candidate in location for candidate in (job_location, job_region) if candidate):
        return False

    preferred_salary = str(contact_attributes.get("ALERT_SALARY") or "")
    job_salary = " ".join(
        str(job.get(field) or "")
        for field in ("salary_text", "salary_min", "salary_max", "salary_period")
    )
    return _salary_matches(preferred_salary, job_salary)


def new_cpc_jobs(report_path: Path, app_dir: Path, report_date: str) -> list[dict[str, Any]]:
    new_ids: set[str] = set()
    with report_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if (
                row.get("first_seen_date") == report_date
                and row.get("tracking_kind") == "newly_published"
                and row.get("source", "").strip().casefold() == "jobg8"
                and row.get("job_id")
            ):
                new_ids.add(row["job_id"].strip())

    if not new_ids:
        return []

    jobs: dict[str, dict[str, Any]] = {}
    for path in app_dir.rglob("*.json"):
        if "_city-pages" in path.parts:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        rows = data if isinstance(data, list) else [data]
        for row in rows:
            if not isinstance(row, dict):
                continue
            job_id = str(row.get("job_id") or "").strip()
            if job_id not in new_ids or job_id in jobs:
                continue
            if not is_cpc_job(str(row.get("source") or ""), str(row.get("apply_url") or "")):
                continue
            row["ontap_url"] = "https://www.ontapjobsearch.com/jobs/" + urllib.parse.quote(job_id, safe="")
            jobs[job_id] = row
    return sorted(jobs.values(), key=lambda job: (str(job.get("title") or "").casefold(), str(job.get("job_id") or "")))


def _brevo_request(method: str, endpoint: str, api_key: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        BREVO_API + endpoint,
        data=data,
        method=method,
        headers={"api-key": api_key, "accept": "application/json", "content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read()
    except urllib.error.HTTPError as error:
        raise DeliveryError(f"Brevo returned HTTP {error.code} for {method} {endpoint.split('?')[0]}") from error
    except (urllib.error.URLError, TimeoutError) as error:
        raise DeliveryError(f"Brevo request failed for {method} {endpoint.split('?')[0]}") from error
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as error:
        raise DeliveryError("Brevo returned an unreadable response") from error
    return parsed if isinstance(parsed, dict) else {}


def _contacts(api_key: str, list_id: int) -> list[dict[str, Any]]:
    contacts: list[dict[str, Any]] = []
    offset = 0
    while True:
        result = _brevo_request(
            "GET",
            f"/contacts/lists/{list_id}/contacts?limit={PAGE_SIZE}&offset={offset}",
            api_key,
        )
        page = result.get("contacts", [])
        if not isinstance(page, list):
            raise DeliveryError("Brevo returned an invalid contact page")
        contacts.extend(contact for contact in page if isinstance(contact, dict))
        if len(page) < PAGE_SIZE:
            return contacts
        offset += len(page)


def _unsubscribe_token(email: str, secret: str) -> str:
    payload = base64.urlsafe_b64encode(
        json.dumps({"email": email.casefold(), "version": 1}, separators=(",", ":")).encode("utf-8")
    ).rstrip(b"=").decode("ascii")
    signature = hmac.new(secret.encode("utf-8"), payload.encode("ascii"), hashlib.sha256).digest()
    signed = base64.urlsafe_b64encode(signature).rstrip(b"=").decode("ascii")
    return f"{payload}.{signed}"


def _email_html(jobs: list[dict[str, Any]], unsubscribe_url: str) -> tuple[str, str]:
    rows_html = []
    rows_text = []
    for job in jobs[:MAX_JOBS_PER_EMAIL]:
        title = html.escape(str(job.get("title") or "CPC job"))
        location = html.escape(str(job.get("location") or job.get("region") or "Location not listed"))
        employer = html.escape(str(job.get("company") or job.get("advertiser_name") or ""))
        salary = html.escape(str(job.get("salary_text") or ""))
        url = html.escape(str(job.get("ontap_url") or ""), quote=True)
        detail = " · ".join(item for item in (employer, location, salary) if item)
        rows_html.append(
            f'<li style="margin:0 0 18px"><a href="{url}" style="color:#1d4ed8;font-weight:700">{title}</a>'
            f'<div style="color:#475569;font-size:14px;margin-top:4px">{detail}</div></li>'
        )
        rows_text.append(f"{title} — {detail}\n{job.get('ontap_url', '')}")

    html_body = (
        '<div style="max-width:620px;margin:0 auto;font:16px/1.5 Arial,sans-serif;color:#171717">'
        "<h1 style='font-size:22px'>New CPC jobs matching your alert</h1>"
        "<p>Here are new jobs published on Ontap that match your saved preferences.</p>"
        f"<ul style='padding-left:20px'>{''.join(rows_html)}</ul>"
        f'<p style="font-size:12px;color:#64748b">You receive this because you asked for CPC job alerts on Ontap. '
        f'<a href="{html.escape(unsubscribe_url, quote=True)}">Unsubscribe</a></p></div>'
    )
    text_body = (
        "New CPC jobs matching your alert\n\n"
        + "\n\n".join(rows_text)
        + f"\n\nUnsubscribe: {unsubscribe_url}\n"
    )
    return html_body, text_body


def send_digest(
    contact: dict[str, Any],
    jobs: list[dict[str, Any]],
    *,
    report_date: str,
    api_key: str,
    sender_email: str,
    unsubscribe_secret: str,
) -> bool:
    email = str(contact.get("email") or "").strip()
    attributes = contact.get("attributes") if isinstance(contact.get("attributes"), dict) else {}
    if not email or contact.get("emailBlacklisted") is True:
        return False
    if attributes.get("ALERT_LAST_SENT_DATE") == report_date:
        return False
    matches = [job for job in jobs if matches_alert(attributes, job)]
    if not matches:
        return False

    token = _unsubscribe_token(email, unsubscribe_secret)
    unsubscribe_url = f"https://www.ontapjobsearch.com/job-alerts/unsubscribe?token={token}"
    html_body, text_body = _email_html(matches, unsubscribe_url)
    _brevo_request(
        "POST",
        "/smtp/email",
        api_key,
        {
            "sender": {"name": "Ontap Job Search", "email": sender_email},
            "to": [{"email": email}],
            "subject": f"{len(matches)} new CPC job{'s' if len(matches) != 1 else ''} matching your alert",
            "htmlContent": html_body,
            "textContent": text_body,
        },
    )
    contact_id = contact.get("id")
    if contact_id is None:
        raise DeliveryError("Brevo contact page omitted a contact ID")
    _brevo_request(
        "PUT",
        f"/contacts/{urllib.parse.quote(email, safe='')}",
        api_key,
        {"attributes": {"ALERT_LAST_SENT_DATE": report_date}},
    )
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Send daily CPC job-alert digests.")
    parser.add_argument("--date", required=True, help="UTC report date in YYYY-MM-DD format")
    parser.add_argument("--app-dir", type=Path, default=Path("app"))
    parser.add_argument("--reports-dir", type=Path, default=Path("pipeline/reports-daily"))
    args = parser.parse_args()

    if os.environ.get("CPC_JOB_ALERTS_ENABLED", "").lower() != "true":
        print("CPC alerts are disabled; no email was sent.")
        return 0

    api_key = os.environ.get("BREVO_API_KEY", "")
    secret = os.environ.get("JOB_ALERTS_UNSUBSCRIBE_SECRET", "")
    sender_email = os.environ.get("BREVO_SENDER_EMAIL", "")
    try:
        list_id = int(os.environ.get("BREVO_JOB_ALERTS_LIST_ID", ""))
    except ValueError:
        list_id = 0
    if not api_key or not secret or not sender_email or list_id <= 0:
        raise DeliveryError("CPC alerts are enabled but Brevo or unsubscribe settings are incomplete")

    report_path = args.reports_dir / f"newly-published-jobs-{args.date}.csv"
    if not report_path.is_file():
        raise DeliveryError(f"New-job report is missing for {args.date}")
    jobs = new_cpc_jobs(report_path, args.app_dir, args.date)
    contacts = _contacts(api_key, list_id)
    sent = 0
    errors = 0
    for contact in contacts:
        try:
            if send_digest(
                contact,
                jobs,
                report_date=args.date,
                api_key=api_key,
                sender_email=sender_email,
                unsubscribe_secret=secret,
            ):
                sent += 1
                time.sleep(0.15)
        except DeliveryError as error:
            errors += 1
            print(f"Alert send failed: {error}")
    print(f"CPC alert delivery for {args.date}: {sent} sent; {errors} failed; {len(jobs)} new CPC jobs; {len(contacts)} contacts.")
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DeliveryError as error:
        print(f"ERROR: {error}")
        raise SystemExit(1)

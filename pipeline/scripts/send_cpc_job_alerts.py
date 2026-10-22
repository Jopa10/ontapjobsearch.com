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
PRIVATE_TEST_EMAIL = "jpbt801@gmail.com"
PRIVATE_TEST_ORIGIN = "https://ontapjobsearchcom-git-feat-cpc-job-alerts-brevo-ontap1.vercel.app"


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
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                raw = response.read()
            break
        except urllib.error.HTTPError as error:
            retryable = error.code == 429 or (method != "POST" and error.code in {500, 502, 503, 504})
            if not retryable or attempt == 3:
                raise DeliveryError(f"Brevo returned HTTP {error.code} for {method} {endpoint.split('?')[0]}") from error
            retry_after = error.headers.get("Retry-After", "")
            delay = int(retry_after) if retry_after.isdigit() else 2 ** attempt
            time.sleep(min(delay, 30))
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
            return [
                contact for contact in contacts
                if list_id not in (contact.get("listUnsubscribed") or [])
            ]
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
        salary_value = str(job.get("salary_text") or "").strip()
        if not salary_value:
            low, high = str(job.get("salary_min") or "").strip(), str(job.get("salary_max") or "").strip()
            period = str(job.get("salary_period") or "").strip()
            if low or high:
                salary_value = " - ".join(value for value in (low, high) if value)
                salary_value = " ".join(value for value in (salary_value, period) if value)
        salary = html.escape(salary_value)
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
    site_url: str = "https://www.ontapjobsearch.com",
    private_test: bool = False,
) -> bool:
    email = str(contact.get("email") or "").strip()
    if private_test and (email.casefold() != PRIVATE_TEST_EMAIL or site_url != PRIVATE_TEST_ORIGIN):
        raise DeliveryError("Private daily delivery is restricted to the fixed test address and Preview")
    attributes = contact.get("attributes") if isinstance(contact.get("attributes"), dict) else {}
    if not email or contact.get("emailBlacklisted") is True:
        return False
    if attributes.get("ALERT_LAST_SENT_DATE") == report_date:
        return False
    matches = [{**job, "ontap_url": site_url + "/jobs/" + urllib.parse.quote(str(job["job_id"]), safe="")}
               for job in jobs if matches_alert(attributes, job)][:MAX_JOBS_PER_EMAIL]
    if not matches:
        return False

    token = _unsubscribe_token(email, unsubscribe_secret)
    unsubscribe_url = f"{site_url}/job-alerts/unsubscribe?token={token}"
    html_body, text_body = _email_html(matches, unsubscribe_url)
    _brevo_request(
        "POST",
        "/smtp/email",
        api_key,
        {
            "sender": {"name": "Ontap Job Search", "email": sender_email},
            "to": [{"email": email}],
            "subject": ("[Private daily test] " if private_test else "") + f"{len(matches)} new CPC job{'s' if len(matches) != 1 else ''} matching your alert",
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



def send_private_test(email: str, site_url: str, app_dir: Path, *, api_key: str,
                      list_id: int, sender_email: str, secret: str) -> None:
    """Send one clearly labelled sample, without listing or updating other contacts."""
    parts = urlsplit(site_url)
    if (parts.scheme != "https" or not parts.hostname
            or not parts.hostname.endswith(".vercel.app")
            or parts.username or parts.password or parts.port
            or parts.path not in ("", "/") or parts.query or parts.fragment):
        raise DeliveryError("Private tests require an HTTPS Vercel Preview origin")
    email = email.strip().casefold()
    if not re.fullmatch(r"[^\s@,;]+@[^\s@,;]+\.[^\s@,;]+", email):
        raise DeliveryError("Private tests require exactly one email address")
    contact = _brevo_request("GET", "/contacts/" + urllib.parse.quote(email, safe=""), api_key)
    if (str(contact.get("email") or "").casefold() != email
            or list_id not in (contact.get("listIds") or [])
            or list_id in (contact.get("listUnsubscribed") or [])
            or contact.get("emailBlacklisted") is True):
        raise DeliveryError("Test recipient must be an active member of the alert list")
    attributes = contact.get("attributes") or {}
    if not attributes.get("ALERT_CONSENT_AT") or not attributes.get("ALERT_CONSENT_VERSION"):
        raise DeliveryError("Test recipient has no saved alert consent")
    job_id = str(attributes.get("ALERT_JOB_ID") or "")
    sample = None
    for path in app_dir.rglob("*.json"):
        if "_city-pages" in path.parts:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for row in data if isinstance(data, list) else [data]:
            if (isinstance(row, dict) and job_id and str(row.get("job_id") or "") == job_id
                    and is_cpc_job(str(row.get("source") or ""), str(row.get("apply_url") or ""))):
                sample = {**row, "ontap_url": site_url.rstrip("/") + "/jobs/" + urllib.parse.quote(job_id, safe="")}
                break
        if sample:
            break
    if not sample:
        raise DeliveryError("The signup job is missing from this checkout; no test sent")
    if not matches_alert(attributes, sample):
        raise DeliveryError("The signup job no longer matches the saved preferences")
    unsubscribe = site_url.rstrip("/") + "/job-alerts/unsubscribe?token=" + _unsubscribe_token(email, secret)
    html_body, text_body = _email_html([sample], unsubscribe)
    notice = "PRIVATE TEST: this sample uses the job you signed up from, not a newly matched vacancy."
    _brevo_request("POST", "/smtp/email", api_key, {
        "sender": {"name": "Ontap Jobs", "email": sender_email},
        "to": [{"email": email}],
        "subject": "[Private test] Your Ontap job alert",
        "htmlContent": "<p>" + notice + "</p>" + html_body,
        "textContent": notice + "\n\n" + text_body,
    })
    print("Private test accepted by Brevo for the single requested recipient; no daily-send state changed.")



def private_daily_test(args: argparse.Namespace, *, api_key: str, list_id: int,
                       sender_email: str, secret: str) -> None:
    """Exercise the real daily report/matcher/digest for one active test contact."""
    if list_id != 3:
        raise DeliveryError("Private daily tests require list ID 3")
    if os.environ.get("GITHUB_REF") != "refs/heads/feat/cpc-job-alerts-brevo":
        raise DeliveryError("Private daily tests require the feature branch")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date or ""):
        raise DeliveryError("A report date in YYYY-MM-DD format is required")
    report = args.reports_dir / f"newly-published-jobs-{args.date}.csv"
    if not report.is_file():
        raise DeliveryError("The requested daily new-jobs report is missing")
    contact = _brevo_request("GET", "/contacts/" + urllib.parse.quote(PRIVATE_TEST_EMAIL, safe=""), api_key)
    attrs = contact.get("attributes") or {}
    if (str(contact.get("email") or "").casefold() != PRIVATE_TEST_EMAIL
            or 3 not in (contact.get("listIds") or [])
            or 3 in (contact.get("listUnsubscribed") or [])
            or contact.get("emailBlacklisted") is True
            or not attrs.get("ALERT_CONSENT_AT") or not attrs.get("ALERT_CONSENT_VERSION")):
        raise DeliveryError("The test address must have an active, consented signup in list 3")
    jobs = new_cpc_jobs(report, args.app_dir, args.date)
    matches = [job for job in jobs if matches_alert(attrs, job)]
    print(f"Private daily matching: {len(jobs)} new CPC jobs; {len(matches)} matches; maximum 20 in a digest.")
    for job in matches[:MAX_JOBS_PER_EMAIL]:
        print(f"Match: {job.get('title', '')} | {job.get('location', '')} | {job.get('job_id', '')}")
    if args.dry_run:
        print("Dry run: no email sent and no contact state changed.")
        return
    sent = send_digest(contact, jobs, report_date=args.date, api_key=api_key,
                       sender_email=sender_email, unsubscribe_secret=secret,
                       site_url=PRIVATE_TEST_ORIGIN, private_test=True)
    print("Private daily digest accepted by Brevo." if sent else
          "No email sent: no matching jobs or this report date was already sent.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Send daily CPC job-alert digests.")
    parser.add_argument("--date", help="UTC report date in YYYY-MM-DD format")
    parser.add_argument("--app-dir", type=Path, default=Path("app"))
    parser.add_argument("--reports-dir", type=Path, default=Path("pipeline/reports-daily"))
    parser.add_argument("--test-recipient", help="Send one labelled sample to this opted-in contact only")
    parser.add_argument("--test-site-url", help="HTTPS Vercel Preview origin for test links")
    parser.add_argument("--private-daily-test", action="store_true", help="Real daily matching for the fixed private test contact only")
    parser.add_argument("--dry-run", action="store_true", help="Private daily test: match without sending or updating state")
    args = parser.parse_args()
    if args.private_daily_test and (args.test_recipient or args.test_site_url):
        parser.error("Private daily tests cannot be combined with sample mode")
    if args.dry_run and not args.private_daily_test:
        parser.error("--dry-run requires --private-daily-test")
    if bool(args.test_recipient) != bool(args.test_site_url):
        parser.error("--test-recipient and --test-site-url must be used together")
    if not args.test_recipient and not args.date:
        parser.error("--date is required for daily delivery")

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

    if args.private_daily_test:
        private_daily_test(args, api_key=api_key, list_id=list_id, sender_email=sender_email, secret=secret)
        return 0

    if args.test_recipient:
        send_private_test(args.test_recipient, args.test_site_url, args.app_dir,
                          api_key=api_key, list_id=list_id, sender_email=sender_email, secret=secret)
        return 0

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
                time.sleep(0.5)
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

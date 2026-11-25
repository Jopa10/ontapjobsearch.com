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
PRIVATE_TEST_EMAILS = (PRIVATE_TEST_EMAIL,)
PRIVATE_TEST_ORIGIN = "https://ontapjobsearchcom-git-feat-cpc-job-alerts-clean-ontap1.vercel.app"


class DeliveryError(RuntimeError):
    pass


class BrevoNotFound(DeliveryError):
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


# Alert groups are deliberately narrower than publication families. Unknown titles
# fail closed; description text never establishes a role match.
ROLE_GROUPS = {
    "general_admin": ("admin assistant", "administrative assistant", "administrator", "office administrator", "office assistant"),
    "reception": ("receptionist", "front desk receptionist", "front of house receptionist", "reception administrator"),
    "bookkeeping": ("bookkeeper", "book keeper", "accounts bookkeeper"),
    "finance_assistant": ("finance assistant", "accounts assistant", "accounting assistant"),
    "assistant_accountant": ("assistant accountant", "assistant management accountant"),
    "customer_service": ("customer service advisor", "customer service adviser", "customer service assistant", "customer service representative"),
    "payroll": ("payroll assistant", "payroll administrator", "payroll officer"),
    "credit_control": ("credit controller", "credit control assistant", "credit control administrator"),
    "ledger": tuple(f"{area} {level}" for area in
                    ("purchase ledger", "sales ledger", "accounts payable", "accounts receivable")
                    for level in ("clerk", "assistant", "administrator")),
    "vehicle_service": ("service advisor", "service adviser", "vehicle service advisor", "vehicle service adviser",
                        "automotive service advisor", "automotive service adviser"),
    "hr_support": ("hr assistant", "hr administrator", "human resources assistant", "human resources administrator"),
    "recruitment_support": ("recruitment assistant", "recruitment administrator", "recruitment coordinator"),
    "legal_assistant": ("legal assistant",),
    "paralegal": ("paralegal",),
    "legal_secretary": ("legal secretary", "legal pa"),
    "marketing_support": ("marketing assistant", "marketing administrator", "marketing coordinator"),
    "support_worker": ("support worker",),
}


def _role_group(value: str) -> str | None:
    # Accept harmless contract/work-pattern adornments, not arbitrary specialist
    # prefixes (e.g. Linux Systems Administrator) or mixed-role combinations.
    title = normalise(value)
    # Strip complete duration/contract qualifiers before individual work-pattern
    # words, so "12 Month Contract" cannot leave unmatched duration tokens.
    title = re.sub(
        r"\b\d{1,2}\s*(?:months?|weeks?|years?)\s*(?:fixed term\s*)?(?:contract|ftc)\b",
        " ", title,
    )
    title = re.sub(r"\b(?:part time|full time|temporary|permanent|contract|fixed term|ftc|temp|hybrid|remote)\b", " ", title)
    title = re.sub(r"\s+", " ", title).strip()
    direct = [group for group, titles in ROLE_GROUPS.items() if title in titles]
    if len(direct) == 1:
        return direct[0]
    # An explicit separated workplace qualifier is permitted for receptionist
    # titles, e.g. Receptionist - Dental Practice. No generic word search.
    base = re.split(r"\s+[-–—|]\s+|\s*\(", value, maxsplit=1)[0]
    if normalise(base) != normalise(value):
        clean_base = normalise(base)
        clean_base = re.sub(r"\b(?:part time|full time|temporary|permanent|contract|fixed term|temp)\b", " ", clean_base)
        clean_base = re.sub(r"\s+", " ", clean_base).strip()
        if clean_base in ROLE_GROUPS["reception"]:
            return "reception"
    return None


def _place(value: str) -> str:
    return normalise(value.replace("&", " and "))


def _region_catalog() -> dict[str, str]:
    # Reuse governed market names/slugs, not a new nearby/catchment list.
    path = Path(__file__).resolve().parents[1] / "config" / "uk_assessable_regions.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    aliases = {}
    for name, detail in data.get("regions", {}).items():
        aliases[_place(name)] = _place(name)
        aliases[_place(str(detail.get("slug") or ""))] = _place(name)
    return aliases


def _location_matches(preference: str, job: dict[str, Any]) -> bool:
    wanted = _place(preference)
    if not wanted:
        return False
    regions = _region_catalog()
    region = _place(str(job.get("region") or ""))
    # Exact recognised region selection; never expand a city to its region.
    if wanted in regions:
        return regions[wanted] == regions.get(region, region)
    location = str(job.get("location") or "")
    # A comma-qualified city (Leeds, West Yorkshire) is still Leeds. A broad
    # region or a different place containing the same word is not that city.
    return wanted == _place(location) or wanted == _place(location.split(",")[0])


def _salary_range(value: str) -> tuple[float, float, str] | None:
    text = value.casefold().replace("£", "")
    periods = []
    for pattern, label in (
        (r"\b(?:hour|hourly|ph)\b|(?<=\d)ph\b|p\.?h\.?", "hour"),
        (r"\b(?:day|daily)\b", "day"),
        (r"\b(?:week|weekly)\b", "week"),
        (r"\b(?:month|monthly)\b", "month"),
        (r"\b(?:year|yearly|annual|annually|annum|pa)\b|p\.a\.", "year"),
    ):
        found = re.search(pattern, text)
        if found:
            periods.append((found.start(), label))
    period = min(periods)[1] if periods else ""
    # Only the pay expression, not hours, days, bonuses or numeric pay grades.
    if re.search(r"\b(?:grade|point|band)\b", text) and not re.search(r"£|\d\s*k\b", value.casefold()):
        return None
    match = re.search(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)\s*(k)?"
                      r"(?:\s*(?:-|–|—|to)\s*(?:£\s*)?(\d[\d,]*(?:\.\d+)?)\s*(k)?)?", text)
    if not match:
        return None
    low = float(match[1].replace(",", ""))
    high = float((match[3] or match[1]).replace(",", ""))
    if match[2] or (match[4] and low < 1000):
        low *= 1000
    if match[4] or (match[2] and high < 1000):
        high *= 1000
    if low <= 0 or high <= 0:
        return None
    if not period and min(low, high) >= 1000:
        period = "year"
    if not period:
        return None
    return min(low, high), max(low, high), period


def _salary_text(job: dict[str, Any]) -> str:
    text = str(job.get("salary_text") or "").strip()
    if text:
        return text
    values = [str(job.get(field) or "").strip() for field in ("salary_min", "salary_max")]
    values = [value for value in values if value and value != "0"]
    return " ".join(filter(None, (" - ".join(values), str(job.get("salary_period") or "")))) if values else ""


def _weekly_hours(job: dict[str, Any]) -> float | None:
    text = " ".join(str(job.get(field) or "") for field in
                    ("work_pattern", "employment_type", "description", "full_description"))
    values = {float(value) for value in re.findall(
        r"(?<![\d.\-–])\b(\d{1,2}(?:\.\d+)?)\s*(?:hours?|hrs?)\s*(?:per|a|/)\s*week\b", text, re.I)}
    # Ranges or conflicting hours require review; never choose an endpoint.
    if re.search(r"\d\s*(?:-|–|to)\s*\d+(?:\.\d+)?\s*(?:hours?|hrs?)", text, re.I):
        return None
    return next(iter(values)) if len(values) == 1 and 0 < next(iter(values)) <= 60 else None


def _salary_decision(preference: str, job: dict[str, Any]) -> tuple[bool, str]:
    preferred = _salary_range(preference)
    raw = _salary_text(job)
    advertised = _salary_range(raw)
    if not advertised:
        if re.search(r"£\s*\d|\d\s*k\b", raw, re.I):
            return True, raw + " · Salary not comparable with your preference"
        return True, "Salary not stated"
    label = raw
    low, high, period = advertised
    # Only use explicitly identified actual pay when both FTE and actual appear.
    actual = re.search(r"(?:actual(?: annual)?(?: salary| pay| earnings)?|pro rata salary)\s*:?\s*(.+)", raw, re.I)
    fte = bool(re.search(r"\bfte\b|full.time equivalent|pro.rata", raw, re.I))
    if actual and (parsed := _salary_range(actual[1] + " per year")):
        low, high, period = parsed
        fte = False
    if fte:
        # Converting FTE requires both the actual and full-time weekly hours.
        hours = _weekly_hours(job)
        evidence = " ".join(str(job.get(field) or "") for field in ("work_pattern", "description", "full_description"))
        full_hours = re.search(r"full[\s-]*time(?:\s+(?:week|hours|equivalent|basis|of|is))*\s*[:=]?\s*(\d{1,2}(?:\.\d+)?)\s*(?:hours?|hrs?)", evidence, re.I)
        if period == "year" and hours and full_hours and 0 < hours <= float(full_hours[1]) <= 60:
            factor = hours / float(full_hours[1])
            low, high = low * factor, high * factor
            label += f" · Actual part-time pay: £{low:,.0f}–£{high:,.0f} per year"
        else:
            return True, raw + " · Full-time equivalent—actual part-time pay unclear"
    if not preferred:
        return True, label
    # The saved salary is a minimum threshold. A job matches when its advertised
    # range reaches that amount; older saved ranges use their lower end as the floor.
    p_low, _p_high, p_period = preferred
    if p_period != period:
        hours = _weekly_hours(job)
        if hours and {p_period, period} == {"hour", "year"}:
            if period == "hour":
                low, high, period = low * hours * 52, high * hours * 52, "year"
            else:
                p_low, p_high = p_low * hours * 52, p_high * hours * 52
                p_period = "year"
        else:
            return True, label + " · Salary not comparable with your preference"
    return high >= p_low, label


def _salary_matches(preference: str, job_salary: str) -> bool:
    return _salary_decision(preference, {"salary_text": job_salary})[0]


def _matches_single_alert(contact_attributes: dict[str, Any], job: dict[str, Any]) -> bool:
    role = _role_group(str(contact_attributes.get("ALERT_ROLE") or ""))
    if role is None or role != _role_group(str(job.get("title") or "")):
        return False
    city_match = _location_matches(str(contact_attributes.get("ALERT_LOCATION") or ""), job)
    region = str(contact_attributes.get("ALERT_REGION") or "")
    region_match = bool(region and _location_matches(region, job))
    if not (city_match or region_match):
        return False
    return _salary_decision(str(contact_attributes.get("ALERT_SALARY") or ""), job)[0]


def alert_preferences(attributes: dict[str, Any]) -> list[dict[str, Any]]:
    raw = attributes.get("ALERT_PREFERENCES")
    if raw is None or raw == "":
        return [attributes]
    try:
        values = json.loads(raw)
    except (ValueError, TypeError) as error:
        raise DeliveryError("Saved alert preferences are unreadable; no email sent") from error
    if (not isinstance(values, list) or len(values) > 10
            or any(not isinstance(p, dict)
                   or not isinstance(p.get("role"), str) or not p["role"].strip()
                   or not isinstance(p.get("location"), str) or not p["location"].strip()
                   or not isinstance(p.get("salary"), str)
                   or ("region" in p and not isinstance(p.get("region"), str)) for p in values)):
        raise DeliveryError("Saved alert preferences are invalid; no email sent")
    return [{"ALERT_ROLE": p["role"], "ALERT_LOCATION": p["location"],
             "ALERT_SALARY": p["salary"], "ALERT_REGION": p.get("region", "")} for p in values]


def matches_alert(contact_attributes: dict[str, Any], job: dict[str, Any]) -> bool:
    return any(_matches_single_alert(p, job) for p in alert_preferences(contact_attributes))


def matching_jobs(attributes: dict[str, Any], jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    preferences = alert_preferences(attributes)
    matches = {}
    for job in jobs:
        job_id = str(job.get("job_id") or "")
        if not job_id or job_id in matches:
            continue
        preference = next((p for p in preferences if _matches_single_alert(p, job)), None)
        if preference is not None:
            matches[job_id] = {**job, "_alert_salary_label":
                              _salary_decision(str(preference.get("ALERT_SALARY") or ""), job)[1]}
    return list(matches.values())


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
        if "_city-pages" in path.parts and "configured-slices" not in path.parts:
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
            if error.code == 404:
                raise BrevoNotFound("Brevo resource not found") from error
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
        salary = html.escape(str(job.get("_alert_salary_label") or _salary_decision("", job)[1]))
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
    if private_test and (email.casefold() not in PRIVATE_TEST_EMAILS or site_url != PRIVATE_TEST_ORIGIN):
        raise DeliveryError("Private daily delivery is restricted to the fixed test address and Preview")
    attributes = contact.get("attributes") if isinstance(contact.get("attributes"), dict) else {}
    if not email or contact.get("emailBlacklisted") is True:
        return False
    if attributes.get("ALERT_LAST_SENT_DATE") == report_date:
        return False
    # Current new vacancies may be newer than the private Preview inventory.
    job_origin = "https://www.ontapjobsearch.com" if private_test else site_url
    matches = [{**job, "ontap_url": job_origin + "/jobs/" + urllib.parse.quote(str(job["job_id"]), safe="")}
               for job in matching_jobs(attributes, jobs)][:MAX_JOBS_PER_EMAIL]
    if not matches:
        return False

    token = _unsubscribe_token(email, unsubscribe_secret)
    unsubscribe_url = f"{site_url}/job-alerts/unsubscribe?token={token}"
    html_body, text_body = _email_html(matches, unsubscribe_url)
    contact_id = contact.get("id")
    if contact_id is None:
        raise DeliveryError("Brevo contact page omitted a contact ID")

    # Claim this recipient/date before the external send. The private post-publish
    # workflow is serialized, so the next run sees this marker even if Brevo
    # accepted the email but the runner lost its response.
    contact_endpoint = f"/contacts/{urllib.parse.quote(email, safe='')}"
    previous_sent_date = str(attributes.get("ALERT_LAST_SENT_DATE") or "")
    _brevo_request(
        "PUT",
        contact_endpoint,
        api_key,
        {"attributes": {"ALERT_LAST_SENT_DATE": report_date}},
    )
    refreshed = _brevo_request("GET", contact_endpoint, api_key)
    refreshed_attributes = refreshed.get("attributes") if isinstance(refreshed.get("attributes"), dict) else {}
    if refreshed_attributes.get("ALERT_LAST_SENT_DATE") != report_date:
        raise DeliveryError("Brevo did not retain the daily-send marker; no email sent")

    private_headers = {}
    if private_test:
        import uuid
        private_headers = {"headers": {"idempotencyKey": str(uuid.uuid5(uuid.NAMESPACE_URL, f"ontap-private-daily:{email.casefold()}:{report_date}"))}}
    try:
        _brevo_request(
            "POST",
            "/smtp/email",
            api_key,
            {
                **private_headers,
                "sender": {"name": "Ontap Jobs", "email": sender_email},
                "to": [{"email": email}],
                "subject": ("[Private daily test] " if private_test else "") + f"{len(matches)} new CPC job{'s' if len(matches) != 1 else ''} matching your alert",
                "htmlContent": html_body,
                "textContent": text_body,
            },
        )
    except DeliveryError as error:
        # A definite HTTP rejection means no message was accepted, so release
        # the claim for a retry. Keep the claim on timeouts/5xx: delivery may
        # have succeeded even though the runner did not receive confirmation.
        rejected = re.search(r"Brevo returned HTTP 4\d{2} for POST /smtp/email", str(error))
        if rejected:
            try:
                _brevo_request(
                    "PUT",
                    contact_endpoint,
                    api_key,
                    {"attributes": {"ALERT_LAST_SENT_DATE": previous_sent_date}},
                )
            except DeliveryError as rollback_error:
                raise DeliveryError(
                    f"{error}; failed to release the daily-send marker: {rollback_error}"
                ) from error
        raise
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
        if "_city-pages" in path.parts and "configured-slices" not in path.parts:
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
    """Match Neon-saved preferences and use Brevo only for delivery/suppression."""
    if list_id != 3:
        raise DeliveryError("Private daily tests require list ID 3")
    recipient = getattr(args, "private_recipient", None) or PRIVATE_TEST_EMAIL
    if recipient not in PRIVATE_TEST_EMAILS:
        raise DeliveryError("Private delivery requires an approved test address")
    verified_sha = getattr(args, "verified_production_sha", None)
    native_publish = (
        os.environ.get("GITHUB_REF") == "refs/heads/main"
        and os.environ.get("GITHUB_WORKFLOW") == "Send private CPC job alerts after publish"
        and bool(re.fullmatch(r"[0-9a-f]{40}", verified_sha or ""))
    )
    preview_branch = os.environ.get("GITHUB_REF") in {
        "refs/heads/feat/cpc-alert-neon-signup",
        "refs/heads/feat/cpc-job-alerts-clean",
    }
    if not preview_branch and not native_publish:
        raise DeliveryError("Private daily tests require the Preview feature branch or verified private post-publish workflow")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date or ""):
        raise DeliveryError("A report date in YYYY-MM-DD format is required")
    matched_sample = getattr(args, "private_matching_sample", False)
    if matched_sample:
        from datetime import datetime, timezone
        if (not preview_branch
                or os.environ.get("GITHUB_WORKFLOW") != "Private CPC daily matching test"
                or args.dry_run
                or args.date != datetime.now(timezone.utc).date().isoformat()):
            raise DeliveryError("Matched samples require today's report and the private Preview workflow")
    report = args.reports_dir / f"newly-published-jobs-{args.date}.csv"
    if not report.is_file():
        raise DeliveryError("The requested daily new-jobs report is missing")

    try:
        contact = _brevo_request("GET", "/contacts/" + urllib.parse.quote(recipient, safe=""), api_key)
    except BrevoNotFound as error:
        raise DeliveryError("The approved test address is not active in Brevo") from error
    if (str(contact.get("email") or "").casefold() != recipient
            or 3 not in (contact.get("listIds") or [])
            or 3 in (contact.get("listUnsubscribed") or [])
            or contact.get("emailBlacklisted") is True):
        raise DeliveryError("Brevo suppression status blocks this private test address")

    attrs = contact.get("attributes") if isinstance(contact.get("attributes"), dict) else {}
    if preview_branch:
        preferences_file = getattr(args, "neon_preferences_file", None)
        if not preferences_file or not Path(preferences_file).is_file():
            raise DeliveryError("The Preview Neon preference read is missing; no email sent")
        try:
            neon = json.loads(Path(preferences_file).read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise DeliveryError("Preview Neon preferences are unreadable; no email sent") from error
        preferences = neon.get("preferences") if isinstance(neon, dict) else None
        if (str(neon.get("email") or "").casefold() != recipient
                or neon.get("consentAction") != "granted"
                or not isinstance(neon.get("userId"), str)
                or not isinstance(neon.get("userEmailId"), str)
                or not isinstance(neon.get("subscriberId"), str)
                or not isinstance(preferences, list) or not preferences or len(preferences) > 10
                or any(not isinstance(p, dict)
                       or not isinstance(p.get("role"), str) or not p["role"].strip()
                       or not isinstance(p.get("location"), str) or not p["location"].strip()
                       or not isinstance(p.get("salary"), str)
                       or ("region" in p and not isinstance(p.get("region"), str))
                       for p in preferences)):
            raise DeliveryError("Preview Neon has no active, consented preferences for the approved address")
        match_attributes = {
            "ALERT_PREFERENCES": json.dumps([
                {key: p[key] for key in ("role", "location", "salary", "region") if key in p}
                for p in preferences
            ]),
            "ALERT_ROLE": preferences[0]["role"],
            "ALERT_LOCATION": preferences[0]["location"],
            "ALERT_SALARY": preferences[0]["salary"],
            "ALERT_REGION": preferences[0].get("region", ""),
        }
        print("Neon user identity and consent verified; saved preference count: " + str(len(preferences)))
        print("Private saved preferences from Neon: " + json.dumps(preferences, ensure_ascii=True))
    else:
        # Keep the existing Production private sender unchanged until a separate
        # Production migration and email rollout are explicitly approved.
        if not attrs.get("ALERT_CONSENT_AT") or not attrs.get("ALERT_CONSENT_VERSION"):
            raise DeliveryError("The Production private test contact lacks consent")
        match_attributes = attrs
    print("Private recipient: " + recipient)
    jobs = new_cpc_jobs(report, args.app_dir, args.date)
    matches = matching_jobs(match_attributes, jobs)
    print(f"Private daily matching: {len(jobs)} new CPC jobs; {len(matches)} matches; maximum 20 in a digest.")
    for job in matches[:MAX_JOBS_PER_EMAIL]:
        print(f"Match: {job.get('title', '')} | {job.get('location', '')} | {job.get('job_id', '')}")
    if args.dry_run:
        print("Dry run: no email sent and no contact state changed.")
        return
    if matched_sample or os.environ.get("GITHUB_REF") == "refs/heads/feat/cpc-alert-neon-signup":
        if not matches:
            if matched_sample:
                raise DeliveryError("No new matching vacancies; no private matched sample sent")
            print("No email sent: no matching jobs.")
            return
        import uuid
        sample_jobs = [
            {**job,
             "ontap_url": "https://www.ontapjobsearch.com/jobs/" + urllib.parse.quote(str(job["job_id"]), safe="")}
            for job in matches[:MAX_JOBS_PER_EMAIL]
        ]
        unsubscribe = PRIVATE_TEST_ORIGIN + "/job-alerts/unsubscribe?token=" + _unsubscribe_token(recipient, secret)
        body_html, body_text = _email_html(sample_jobs, unsubscribe)
        notice = "PRIVATE MATCHING TEST: today's new jobs matched using preferences saved in Preview Neon. This sample does not change daily delivery state."
        if matched_sample:
            identity = json.dumps([args.date, recipient, preferences,
                                   [job["job_id"] for job in sample_jobs]], sort_keys=True)
            key_name = "ontap-private-matched-sample:" + identity
            subject = f"[Private matching test] {len(sample_jobs)} jobs matching your alert"
            body_html, body_text = "<p>" + notice + "</p>" + body_html, notice + "\n\n" + body_text
        else:
            key_name = f"ontap-preview-private-daily:{recipient}:{args.date}"
            noun = "job" if len(sample_jobs) == 1 else "jobs"
            subject = f"[Private daily test] {len(sample_jobs)} new CPC {noun} matching your alert"
        import subprocess

        key = str(uuid.uuid5(uuid.NAMESPACE_URL, key_name))

        def record(action, **payload):
            return subprocess.run(
                ["node", str(Path(__file__).with_name("record_neon_alert_sample.mjs"))],
                input=json.dumps({"action": action, "key": key, **payload}),
                text=True, check=True, stdout=subprocess.PIPE,
            ).stdout

        recommendations = []
        for job in sample_jobs:
            preference = next(
                p for p in preferences
                if matches_alert({"ALERT_ROLE": p["role"], "ALERT_LOCATION": p["location"],
                                  "ALERT_SALARY": p["salary"], "ALERT_REGION": p.get("region", "")}, job)
            )
            recommendations.append({"publicId": str(job["job_id"]), "preferenceId": preference["preferenceId"]})
        if record("reserve", matches=recommendations).strip() == "already-sent":
            print("Already sent — skipped")
            return
        try:
            result = _brevo_request("POST", "/smtp/email", api_key, {
                "headers": {"idempotencyKey": key},
                "sender": {"name": "Ontap Jobs", "email": sender_email},
                "to": [{"email": recipient}],
                "subject": subject,
                "htmlContent": body_html,
                "textContent": body_text,
            })
            message_id = result.get("messageId")
            if not isinstance(message_id, str) or not message_id.strip():
                raise DeliveryError("Brevo returned no message ID for the private Preview alert")
        except Exception:
            record("uncertain")
            raise
        record("sent", messageId=message_id)
        print("Private Preview alert accepted by Brevo and recorded in Neon: " + message_id)
        return
    delivery_contact = {**contact, "attributes": {**(contact.get("attributes") or {}), **match_attributes}}
    sent = send_digest(delivery_contact, jobs, report_date=args.date, api_key=api_key,
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
    parser.add_argument("--verified-production-sha", help="Verified deployed inventory SHA, required by the native private workflow")
    parser.add_argument("--private-recipient", choices=PRIVATE_TEST_EMAILS, help="Approved private test address only")
    parser.add_argument("--private-daily-test", action="store_true", help="Real daily matching for the fixed private test contact only")
    parser.add_argument("--private-matching-sample", action="store_true", help="One labelled matched sample to the fixed private contact; daily state unchanged")
    parser.add_argument("--dry-run", action="store_true", help="Private daily test: match without sending or updating state")
    parser.add_argument("--neon-preferences-file", type=Path, help="JSON result from the restricted Preview Neon reader")
    args = parser.parse_args()
    if args.private_recipient and not args.private_daily_test:
        parser.error("--private-recipient requires --private-daily-test")
    if args.private_matching_sample and (not args.private_daily_test or args.dry_run):
        parser.error("--private-matching-sample requires --private-daily-test without --dry-run")
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

    if os.environ.get("CPC_JOB_ALERTS_LIVE_ENABLED", "").lower() != "true":
        print("Live CPC job alerts are disabled; private checks passed, no public email was sent.")
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

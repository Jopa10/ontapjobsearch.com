from __future__ import annotations

import html
import math
import re
from dataclasses import dataclass

SELECTED_CLASSIFICATIONS = {"HIGH_CONFIDENCE", "ELASTIC_FIT"}
SENIORITY_TERMS = ("senior", "head", "lead", "manager", "director")
COL = {
    "display_reference": "/Job/DisplayReference", "sender_reference": "/Job/SenderReference",
    "title": "/Job/Position", "advertiser": "/Job/AdvertiserName",
    "advertiser_type": "/Job/AdvertiserType", "area": "/Job/Area",
    "location": "/Job/Location", "application_url": "/Job/ApplicationURL",
    "description": "/Job/Description", "employment_type": "/Job/EmploymentType",
    "work_hours": "/Job/WorkHours", "salary_minimum": "/Job/SalaryMinimum",
    "salary_maximum": "/Job/SalaryMaximum", "salary_period": "/Job/SalaryPeriod",
    "salary_additional": "/Job/SalaryAdditional",
}

SIGNALS = {
    "fully remote": r"\bfully\s+remote\b", "100% remote": r"\b100\s*%\s*remote\b",
    "entirely remote": r"\bentirely\s+remote\b", "remote only": r"\bremote[- ]only\b",
    "permanent homeworking": r"\bpermanent(?:ly)?\s+home\s*working\b",
    "fully home based": r"\bfully\s+home[- ]?based\b", "home based": r"\bhome[- ]?based\b",
    "work from home": r"\bwork(?:ing)?[-\s]+from[-\s]+home\b",
    "homeworking": r"\bhome\s*working\b", "remote working": r"\bremote\s+working\b",
    "remote role": r"\bremote\s+(?:role|position|job|opportunity)\b",
    "location remote": r"\blocation\s*[:\-]?\s*remote\b", "remote": r"\bremote\b",
    "hybrid": r"\bhybrid\b",
}
NEGATIVE = [
    r"\b(?:not|isn['’]?t|is not)\s+(?:a\s+)?remote\s+(?:role|position|job)\b",
    r"\bremote(?:\s+or\s+hybrid)?\s+working\s+(?:is|are)\s+not\s+available\b",
    r"\b(?:unable|not able)\s+to\s+offer\s+(?:remote|home|hybrid)\s+working\b",
    r"\bunable\s+to\s+accept.{0,80}\bremote(?:.{0,40}hybrid)?\s+working\b",
    r"\bno\s+(?:remote|home|hybrid)\s+working\b", r"\boffice[- ]based\s+only\b",
    r"\bfully\s+onsite\b", r"\bbased\s+fully\s+onsite\b",
]
BUSINESS = [
    r"\bbuild\s+(?:something|a\s+business|your\s+own)\b",
    r"\b(?:start|build|create|run)\s+your\s+own\s+(?:virtual\s+assistant\s+)?business\b",
    r"\bvirtual\s+assistant\s+business\b", r"\bstep[- ]by[- ]step\s+programme\b",
    r"\bfinancial\s+freedom\b", r"\bcharge\s+(?:your\s+)?clients?\b",
    r"\bfranchise\s+opportunit(?:y|ies)\b", r"\bself[- ]employment\s+opportunit(?:y|ies)\b",
    r"\bpay\s+for\s+(?:the\s+)?(?:training|programme|course)\b",
]
FALSE_POSITIVE = [
    r"\bdue\s+to\s+the\s+remote\s+location\b",
    r"\bremote\s+(?:site|sites|area|areas|community|communities|island|location)\b",
    r"\b(?:manage|managing|support|supporting|lead|leading|oversee|overseeing)\s+(?:a\s+)?remote\s+team\b",
    r"\bremote\s+(?:clients?|customers?|workers?|employees?|colleagues?)\b",
    r"\bremote\s+(?:access|desktop|support|monitoring|diagnostics?|systems?|technology|technologies)\b",
    r"\bremote\s+tutor[- ](?:led|lead)\s+(?:training|sessions?)\b",
    r"\bremote\s+training\s+(?:sessions?|delivery)\b",
    r"\b(?:clients?|service\s+users?|patients?)['’]?\s+homes\b", r"\bhome\s+visits?\b",
    r"\bhomecare\b|\bhome\s+care\b|\bdomiciliary\b",
    r"\bworking[- ]from[- ]home\s+allowance\b", r"\bwork[- ]from[- ]home\s+allowance\b",
]
HYBRID = [
    r"\bhybrid\b", r"\b\d+\s+days?\s+(?:in|at|from)\s+(?:the\s+)?office\b",
    r"\b\d+\s+days?\s+(?:working\s+)?from\s+home\b",
    r"\b(?:one|two|three|four|five)\s+days?\s+(?:working\s+)?from\s+home\b",
    r"\b(?:occasional|some)\s+(?:remote|home)\s*working\b",
    r"\bup\s+to\s+\d+\s+days?\s+(?:working\s+)?from\s+home\b",
    r"\bpredominantly\s+office[- ]based\b", r"\bregular\s+(?:office|onsite|on-site)\s+attendance\b",
    r"\boffice[- ]based.{0,180}home[- ]?based\b", r"\bhome[- ]?based.{0,180}office[- ]based\b",
]
AFTER_CONDITION = [
    r"\b(?:remote|home|hybrid)\s+working\s+(?:after|following)\s+(?:training|induction|probation|a\s+qualifying\s+period)\b",
    r"\bafter\s+(?:training|induction|probation).{0,80}\b(?:remote|home|hybrid)\b",
    r"\b(?:training|induction|probation).{0,80}\b(?:then|thereafter|subsequently)\s+(?:work|working)\s+from\s+home\b",
]
REMOTE_OPTION = [
    r"\bremote\s*,?\s*hybrid\s+or\s+office[- ]based\b",
    r"\bremote\s+or\s+hybrid\s+or\s+office[- ]based\b",
    r"\b(?:fully\s+)?remote\s+(?:is|as)\s+(?:an\s+)?option\b",
    r"\bchoice\s+of\s+(?:remote|homeworking|home-based).{0,60}(?:hybrid|office)\b",
]
LOCATION_RESTRICTED = [
    r"\bmust\s+(?:live|reside|be\s+based)\s+(?:within|in|near)\b",
    r"\bwithin\s+\d+\s+(?:minutes?|miles?|km)\s+(?:drive|travel|travelling|traveling|of)\b",
    r"\bapplicants?\s+must\s+be\s+based\s+in\b", r"\bhome[- ]based\s+but\s+(?:must|required\s+to)\b",
]
FULLY_REMOTE = [
    r"\bfully\s+remote\b", r"\b100\s*%\s*remote\b", r"\bentirely\s+remote\b",
    r"\bremote[- ]only\b", r"\bpermanent(?:ly)?\s+home\s*working\b",
    r"\bfully\s+home[- ]?based\b", r"\bhome[- ]?based\s+(?:role|position|job|opportunity)\b",
    r"\([^)]*home[- ]?based[^)]*\)", r"\blocation\s*[:\-]?\s*home[- ]?based\b",
    r"\b(?:role|position|job|opportunity)\s+(?:is|will\s+be)\s+home[- ]?based\b",
    r"\bwork(?:ing)?\s+from\s+home\s+(?:full[- ]?time|five\s+days?\s+a\s+week)\b",
    r"\bwork(?:ing)?\s+fully\s+remotely\b", r"\bwork\s+remotely\s+from\s+anywhere\s+in\s+the\s+uk\b",
    r"\buk[- ]wide\s+remote\b", r"\blocation\s*[:\-]?\s*remote\b", r"\bworking\s+remotely\b",
]
UK_WIDE = [r"\banywhere\s+in\s+the\s+uk\b", r"\buk[- ]wide\b", r"\bacross\s+the\s+uk\b", r"\blocation\s*[:\-]?\s*remote\b"]
SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9£])|\s*[\r\n]+\s*")
TAG = re.compile(r"<[^>]+>")

@dataclass(frozen=True)
class RemoteDecision:
    classification: str; reason_code: str; matched_terms: str; evidence: str
    scope: str; routine_office_attendance: str; manual_review_required: bool

def norm_text(value: object) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)): return ""
    return re.sub(r"\s+", " ", str(value).strip())

def norm_key(value: object) -> str: return norm_text(value).casefold()

def fix_encoding(value: object) -> str:
    text = norm_text(value)
    candidates = [text]
    for enc in ("latin1", "cp1252"):
        try: candidates.append(text.encode(enc).decode("utf-8"))
        except (UnicodeEncodeError, UnicodeDecodeError): pass
    markers = ("Â", "Ã", "â€", "â€“", "â€”", "â€¢", "â€¦", "�")
    text = min(candidates, key=lambda s: sum(s.count(m) for m in markers))
    return text.replace("Â£", "£").replace("â€“", "–").replace("â€”", "—").replace("â€™", "'")

def clean_description(value: object) -> str:
    return norm_text(TAG.sub(" ", html.unescape(fix_encoding(value))))

def normalise_url(value: object) -> str: return norm_text(value).rstrip("/").casefold()

def matches(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text, re.I | re.S) for p in patterns)

def evidence_for(text: str, patterns: list[str]) -> str:
    compiled = [re.compile(p, re.I | re.S) for p in patterns]
    sentences = [norm_text(s) for s in SPLIT.split(text) if norm_text(s)]
    for i, sentence in enumerate(sentences):
        if any(p.search(sentence) for p in compiled):
            if len(sentence) < 45 and i + 1 < len(sentences): sentence += " " + sentences[i + 1]
            return sentence[:1200]
    return ""

def classify_remote(title: str, description: str, area: str = "", location: str = "") -> RemoteDecision:
    text = norm_text(" ".join(map(clean_description, (title, description, area, location))))
    terms = "; ".join(k for k, p in SIGNALS.items() if re.search(p, text, re.I))
    def out(c, r, pats, scope="NOT_APPLICABLE", office="unknown", review=False):
        return RemoteDecision(c, r, terms, evidence_for(text, pats), scope, office, review)
    if matches(text, NEGATIVE): return out("EXPLICITLY_NOT_REMOTE", "explicit_negative_remote_statement", NEGATIVE, office="yes")
    if matches(text, BUSINESS): return out("BUSINESS_OPPORTUNITY_OR_TRAINING", "business_or_training_offer_not_vacancy", BUSINESS)
    if matches(text, AFTER_CONDITION): return out("REMOTE_AFTER_TRAINING_OR_PROBATION", "remote_only_after_condition", AFTER_CONDITION, "NOT_STATED", "yes")
    if matches(text, REMOTE_OPTION):
        return out("REMOTE_OPTION_AVAILABLE", "fully_remote_is_explicit_option", REMOTE_OPTION, "UK_WIDE" if matches(text, UK_WIDE) else "NOT_STATED", "no")
    if matches(text, HYBRID): return out("HYBRID_OR_PARTIAL_REMOTE", "hybrid_or_regular_office_attendance", HYBRID, "NOT_STATED", "yes")
    if matches(text, FULLY_REMOTE):
        if matches(text, LOCATION_RESTRICTED):
            return out("FULLY_REMOTE_LOCATION_RESTRICTED", "fully_remote_with_geographic_restriction", FULLY_REMOTE + LOCATION_RESTRICTED, "LOCATION_RESTRICTED", "no")
        return out("FULLY_REMOTE_CONFIRMED", "clear_fully_remote_working_arrangement", FULLY_REMOTE, "UK_WIDE", "no")
    if terms and matches(text, FALSE_POSITIVE): return out("REMOTE_MENTION_FALSE_POSITIVE", "remote_term_describes_other_context", FALSE_POSITIVE)
    if terms: return out("AMBIGUOUS_REMOTE_REVIEW", "remote_signal_without_clear_working_arrangement", list(SIGNALS.values()), "NOT_STATED", review=True)
    return RemoteDecision("NO_REMOTE_SIGNAL", "no_relevant_remote_wording", "", "", "NOT_APPLICABLE", "unknown", False)

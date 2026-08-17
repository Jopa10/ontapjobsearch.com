from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Mapping

VALID_ACTIONS = {"", "select", "exclude"}


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


@dataclass(frozen=True)
class ReviewItem:
    source: str
    source_job_id: str
    title: str
    employer: str = ""
    location: str = ""
    region: str = ""
    category: str = ""
    salary: str = ""
    closing_date: str = ""
    reason: str = ""
    source_url: str = ""

    def fingerprint(self) -> str:
        payload = {
            "source": clean(self.source),
            "source_job_id": clean(self.source_job_id),
            "title": clean(self.title),
            "employer": clean(self.employer),
            "location": clean(self.location),
            "region": clean(self.region),
            "category": clean(self.category),
            "salary": clean(self.salary),
            "closing_date": clean(self.closing_date),
            "reason": clean(self.reason),
            "source_url": clean(self.source_url),
        }
        encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class SourceResult:
    key: str
    label: str
    state: str
    review_date: str
    items: tuple[ReviewItem, ...] = ()
    note: str = ""
    publish_workflow: str = ""

    @property
    def needs_attention(self) -> bool:
        return self.state not in {"OK", "FUTURE"}


@dataclass(frozen=True)
class ParsedDecision:
    action: str
    item: ReviewItem
    fingerprint: str


def item_from_mapping(source: str, row: Mapping[str, object], **overrides: object) -> ReviewItem:
    data = {
        "source": source,
        "source_job_id": clean(row.get("source_job_id") or row.get("job_id")),
        "title": clean(row.get("title")),
        "employer": clean(row.get("employer")),
        "location": clean(row.get("location") or row.get("town")),
        "region": clean(row.get("ontap_region") or row.get("ontap_geography") or row.get("region")),
        "category": clean(row.get("category")),
        "salary": clean(row.get("salary_text") or row.get("salary")),
        "closing_date": clean(row.get("closing_date")),
        "reason": clean(row.get("classification_reason") or row.get("reason")),
        "source_url": clean(row.get("source_url")),
    }
    for key, value in overrides.items():
        if key in data:
            data[key] = clean(value)
    if not data["source_job_id"]:
        raise ValueError(f"{source} review row has no stable job ID")
    return ReviewItem(**data)

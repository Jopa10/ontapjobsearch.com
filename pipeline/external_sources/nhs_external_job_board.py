"""Production boundary for the NHS External Job Board vacancy feed.

NHSBSA publicly lists an "NHS Jobs External Job Board Vacancy API
specification", which is the production interface Ontap is designing around.

The public NHSBSA page does not expose the machine-readable endpoint/auth/schema
in HTML, so this module deliberately does not guess them. Instead it freezes
Ontap's side of the contract now: whatever NHS transport is supplied must map
into this canonical record. Once the official endpoint/credentials/specification
are available, only the transport/decoder implementation should need changing.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Protocol

SOURCE = "NHS Jobs"


@dataclass(frozen=True)
class NHSExternalVacancy:
    source_job_id: str
    title: str
    employer: str
    locations: tuple[str, ...]
    salary_text: str = ""
    job_reference: str = ""
    employment_type: str = ""
    posted_date: str = ""
    closing_date: str = ""
    source_url: str = ""
    apply_url: str = ""
    description: str = ""
    source: str = SOURCE

    def to_ontap_row(self) -> dict[str, Any]:
        if not self.source_job_id.strip():
            raise ValueError("NHS external vacancy has no source_job_id")
        if not self.title.strip():
            raise ValueError("NHS external vacancy has no title")
        if not self.employer.strip():
            raise ValueError("NHS external vacancy has no employer")

        source_url = self.source_url.strip()
        apply_url = self.apply_url.strip() or source_url
        return {
            "job_id": f"nhs-{self.source_job_id.strip()}",
            "source_job_id": self.source_job_id.strip(),
            "source": SOURCE,
            "title": self.title.strip(),
            "company": self.employer.strip(),
            "advertiser_name": self.employer.strip(),
            "location": ", ".join(value.strip() for value in self.locations if value.strip()),
            "salary": self.salary_text.strip(),
            "job_reference": self.job_reference.strip(),
            "employment_type": self.employment_type.strip(),
            "posted_date": self.posted_date.strip(),
            "closing_date": self.closing_date.strip(),
            "source_url": source_url,
            "apply_url": apply_url,
            "description": self.description.strip(),
        }


class NHSExternalJobBoardTransport(Protocol):
    """Small seam around the official NHS job-board interface."""

    def fetch_records(self) -> Iterable[Mapping[str, Any]]:
        ...


class NHSExternalJobBoardDecoder(Protocol):
    """Maps one official API record into Ontap's stable NHS boundary record."""

    def decode(self, record: Mapping[str, Any]) -> NHSExternalVacancy:
        ...


class NHSExternalJobBoardAdapter:
    def __init__(
        self,
        transport: NHSExternalJobBoardTransport,
        decoder: NHSExternalJobBoardDecoder,
    ) -> None:
        self.transport = transport
        self.decoder = decoder

    def fetch(self) -> list[NHSExternalVacancy]:
        output: list[NHSExternalVacancy] = []
        seen: set[str] = set()

        for raw in self.transport.fetch_records():
            vacancy = self.decoder.decode(raw)
            source_id = vacancy.source_job_id.strip()
            if not source_id:
                raise ValueError("official NHS record decoded without source_job_id")
            if source_id in seen:
                continue
            seen.add(source_id)
            output.append(vacancy)

        return output

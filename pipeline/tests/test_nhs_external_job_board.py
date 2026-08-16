from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from external_sources.nhs_external_job_board import (
    NHSExternalJobBoardAdapter,
    NHSExternalVacancy,
)


class FakeTransport:
    def fetch_records(self):
        return [
            {"id": "C123", "title": "Administrator"},
            {"id": "C123", "title": "Administrator"},
            {"id": "C124", "title": "Receptionist"},
        ]


class FakeDecoder:
    def decode(self, record):
        return NHSExternalVacancy(
            source_job_id=record["id"],
            title=record["title"],
            employer="Example NHS Trust",
            locations=("Newcastle upon Tyne",),
            source_url=f"https://www.jobs.nhs.uk/candidate/jobadvert/{record['id']}",
        )


def test_adapter_dedupes_on_official_source_identity() -> None:
    rows = NHSExternalJobBoardAdapter(FakeTransport(), FakeDecoder()).fetch()

    assert [row.source_job_id for row in rows] == ["C123", "C124"]


def test_canonical_row_uses_stable_nhs_id_and_external_apply_route() -> None:
    vacancy = NHSExternalVacancy(
        source_job_id="C123",
        title="Administrator",
        employer="Example NHS Trust",
        locations=("Newcastle upon Tyne",),
        salary_text="£25,000",
        source_url="https://www.jobs.nhs.uk/candidate/jobadvert/C123",
    )

    row = vacancy.to_ontap_row()

    assert row["job_id"] == "nhs-C123"
    assert row["source"] == "NHS Jobs"
    assert row["apply_url"] == vacancy.source_url
    assert row["company"] == "Example NHS Trust"

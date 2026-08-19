from __future__ import annotations

import pytest
from external_sources import teaching_vacancies_discovery as discovery
from external_sources import teaching_vacancies_poc as poc
from external_sources.regional_contracts import DiscoveryRecord

def listing(url: str) -> DiscoveryRecord:
    row = DiscoveryRecord(source=discovery.SOURCE, source_job_id='', canonical_url=url)
    row.add_provenance(route='route', query='query', page=1)
    return row

def vacancy(url: str) -> poc.Vacancy:
    return poc.Vacancy(
        source_job_id='TV-1', title='Administrator', employer='Example School',
        location='London', salary_text='£25,000', posted_date='2026-08-19',
        closing_date='2026-08-31', employment_type='FULL_TIME',
        description_excerpt='Administrative duties', source_url=url,
    )

def test_confirmed_404_after_listing_is_omitted() -> None:
    gone = 'https://teaching-vacancies.service.gov.uk/jobs/gone'
    live = 'https://teaching-vacancies.service.gov.uk/jobs/live'
    def request_text(url: str) -> str:
        if url == gone:
            raise OSError('Teaching Vacancies request failed after 4 attempts — HTTP Error 404: Not Found')
        return '<html></html>'
    records = discovery.detail_records(
        (listing(gone), listing(live)),
        request_text=request_text,
        parse_detail=lambda _document, url: vacancy(url),
    )
    assert len(records) == 1
    assert records[0].canonical_url == live

def test_non_404_detail_failure_still_blocks_run() -> None:
    url = 'https://teaching-vacancies.service.gov.uk/jobs/broken'
    with pytest.raises(ValueError, match='detail fetch was incomplete'):
        discovery.detail_records(
            (listing(url),),
            request_text=lambda _url: (_ for _ in ()).throw(OSError('HTTP Error 500')),
            parse_detail=lambda _document, detail_url: vacancy(detail_url),
        )

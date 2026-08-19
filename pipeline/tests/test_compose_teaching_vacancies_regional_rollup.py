from __future__ import annotations

import pytest
from external_sources.compose_teaching_vacancies_regional import current_base_contract

def row(job_id: str, region: str, source: str) -> dict:
    return {'job_id': job_id, 'region': region, 'source': source}

def test_north_east_public_rollup_accepts_detailed_external_regions() -> None:
    region, base, teaching = current_base_contract([
        row('jobg8-1', 'North East', 'JobG8'),
        row('nejobs-1', 'North East - Tyneside, Wearside & Northumberland', 'NEJobs'),
        row('vonne-1', 'North East - County Durham & Darlington/Hartlepool', 'VONNE'),
    ])
    assert region == 'North East'
    assert len(base) == 3
    assert teaching == []

def test_unrelated_mixed_regions_remain_blocked() -> None:
    with pytest.raises(ValueError, match='blank or mixed'):
        current_base_contract([
            row('jobg8-1', 'North East', 'JobG8'),
            row('jobg8-2', 'Yorkshire - West', 'JobG8'),
        ])

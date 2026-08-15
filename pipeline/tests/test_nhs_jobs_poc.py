from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from external_sources import nhs_jobs_poc as nhs

SAMPLE_XML = b'''<?xml version="1.0" encoding="UTF-8"?>
<searchResults>
  <totalPages>2</totalPages>
  <totalResults>101</totalResults>
  <vacancyDetails>
    <id>C123</id>
    <title>Administrative Assistant</title>
    <employer>Example NHS Trust</employer>
    <locations><location>Newcastle upon Tyne, NE1 1AA</location></locations>
    <salary>\xc2\xa325,000 to \xc2\xa327,000 a year</salary>
    <reference>ABC123</reference>
    <type>Permanent</type>
    <closeDate>2026-08-31</closeDate>
    <postDate>2026-08-15</postDate>
    <url>https://www.jobs.nhs.uk/candidate/jobadvert/C123</url>
  </vacancyDetails>
</searchResults>'''


def test_parse_xml_and_classify() -> None:
    rows, pages, total = nhs.parse_xml(SAMPLE_XML)
    assert pages == 2
    assert total == 101
    assert len(rows) == 1
    vacancy = rows[0]
    assert vacancy.source_job_id == "C123"
    assert vacancy.locations == "Newcastle upon Tyne, NE1 1AA"
    assert nhs.classify(vacancy)[0] == "HC"


def test_jobg8_duplicate_becomes_hard_pass() -> None:
    rows, _pages, _total = nhs.parse_xml(SAMPLE_XML)
    jobs = [{"title": "Administrative Assistant", "company": "Example NHS Trust"}]
    reviewed = nhs.process(rows, jobs, date(2026, 8, 15))
    assert reviewed[0].jobg8_check == "DUPLICATE"
    assert reviewed[0].final_decision == "HARD_PASS"


def test_closed_vacancy_is_removed() -> None:
    rows, _pages, _total = nhs.parse_xml(SAMPLE_XML)
    rows[0].closing_date = "2026-08-14"
    assert nhs.process(rows, [], date(2026, 8, 15)) == []

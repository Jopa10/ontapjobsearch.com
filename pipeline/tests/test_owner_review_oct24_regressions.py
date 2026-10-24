from datetime import date
from pathlib import Path
import pytest
from pipeline.external_sources.teaching_vacancies_poc import Vacancy, classify
from pipeline.tests.test_service_admin_owner_selection_rules import make_job, run_rows
from review_hub import adapters, master_review
from review_hub.contracts import SourceResult, ReviewItem

@pytest.mark.parametrize('title,pay', [('Service Advisor',38000),('Service Advisor',40000),('Project Coordinator',40000),('HR Coordinator',38000),('Finance Assistant',40000),('Document Controller',45000)])
def test_jobg8_owner_examples_pass(title,pay):
    jobs,_=run_rows([make_job('example',title,pay,'General office administration and records.')])
    assert jobs['example']['_review_required']==''

@pytest.mark.parametrize('title', ['Asset Management Coordinator','Salesforce Administrator','Sales Support Team Lead','Senior Office Administrator','Chief Financial & Operations Officer'])
def test_jobg8_owner_exclusions(title):
    jobs,_=run_rows([make_job('example',title,38000,'General office administration and records.')])
    assert 'example' not in jobs

@pytest.mark.parametrize('title,pay,expected', [('Exams Manager (part time)','£22,545','HARD_PASS'),('Deputy Office Manager','£27,000','HARD_PASS'),('Governance Manager','£27,511','HARD_PASS'),('Senior Pupil Services Officer','£29,070','HARD_PASS'),('Chief Financial & Operations Officer','£110,000','HARD_PASS'),('Exam & Data Assistant','D','HARD_PASS'),('Finance Officer','£30,000 - £35,000 FTE','HC'),('Receptionist','£25,583','HC'),('Finance Manager (part time)','£30,000','POSS')])
def test_tv_examples(title,pay,expected):
    assert classify(Vacancy(title=title,salary_text=pay,geography_status='IN_SCOPE'))[0]==expected

@pytest.mark.parametrize('key',['teaching_vacancies','nhs','vonne','nejobs'])
def test_external_loader_failure_cannot_remove_jobg8(monkeypatch,key):
    good=SourceResult('jobg8','JobG8','OK','2026-10-24',publish_workflow='jobg8.yml')
    def good_loader(today): return good
    def bad_loader(today): raise ValueError('malformed source file')
    bad_loader.__name__='load_'+key
    monkeypatch.setattr(adapters,'SOURCE_LOADERS',(good_loader,bad_loader))
    assert adapters.load_all_sources(date(2026,10,24))[0] is good
    assert adapters.load_all_sources(date(2026,10,24))[1].state=='ERROR'

@pytest.mark.parametrize('key',['teaching_vacancies','nhs','vonne','nejobs'])
def test_malformed_external_review_preserves_jobg8_publish(tmp_path,monkeypatch,key):
    today=date(2026,10,24)
    good=SourceResult('jobg8','JobG8','OK',today.isoformat(),publish_workflow='jobg8.yml')
    bad=SourceResult(key,key,'OK',today.isoformat(),publish_workflow='external.yml')
    path=tmp_path/'review.md'
    path.write_text(f'review_date: {today}\n---\naction: sel\nsource_key: {key}\nsource_job_id: bad\ntitle: Broken\n---\n')
    monkeypatch.setattr(master_review,'load_all_sources',lambda _: [good,bad])
    plan=master_review.apply_master(path,today=today)
    assert key in plan['isolated_sources']
    assert [row['source'] for row in plan['publish']]==['jobg8']

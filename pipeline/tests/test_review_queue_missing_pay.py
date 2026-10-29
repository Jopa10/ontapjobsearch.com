from datetime import date
from pathlib import Path
import csv
import pytest
from review_hub import adapters
from pipeline.scripts.pipeline_refinement import missing_owner_salary_should_exclude
from pipeline.tests.test_service_admin_owner_selection_rules import make_job, run_rows

@pytest.mark.parametrize('title', ['Administrator','Service Advisor','Document Controller','Receptionist','Finance Assistant'])
def test_blank_pay_is_allowed_without_becoming_a_review(title):
    jobs,reports=run_rows([make_job('blank',title,'','Office records and customer enquiries.')])
    assert 'blank' in jobs
    assert jobs['blank']['_review_required']==''

def test_senior_part_time_unknown_earnings_retains_existing_review():
    row=make_job('part','Senior Bookkeeper (Part Time)','','20 hours per week. Maintain ledgers.')
    jobs,_=run_rows([row])
    assert jobs['part']['_review_required']=='1'

def test_non_numeric_pay_wording_not_treated_as_blank():
    assert not missing_owner_salary_should_exclude('Competitive',None)
    assert not missing_owner_salary_should_exclude('',30000)
    assert not missing_owner_salary_should_exclude('',None,part_time_finance=True)

def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

@pytest.mark.parametrize('has_evidence',[False,True])
def test_hub_filters_only_explicit_missing_pay_evidence(tmp_path,monkeypatch,has_evidence):
    monkeypatch.setattr(adapters,'PIPELINE_ROOT',tmp_path)
    row=dict(feed_date='2026-10-25',decision='POSS',job_id='x',title='Administrator',region='Kent',town='Kent',salary_text='',annual_salary_upper='',reason='Office/finance role salary is unavailable or unclear' if has_evidence else '')
    for stem in ['service-admin','support-worker']:
        write_csv(tmp_path/f'reviews/jobg8/{stem}-review.csv',[row if stem=='service-admin' else {**row,'decision':'SELECTED'}])
    result=adapters.load_jobg8(date(2026,10,25))
    assert len(result.items)==(0 if has_evidence else 1)

def test_master_summary_counts_saved_answer_separately(tmp_path):
    from review_hub import master_review
    from review_hub.contracts import ReviewItem, SourceResult
    today=date(2026,10,25)
    vacancy=ReviewItem(source='JobG8',source_job_id='x',title='Account Assistant',category='admin_service')
    result=SourceResult('jobg8','JobG8','OK',today.isoformat(),(vacancy,))
    p=tmp_path/'review.md'
    text=master_review.master_text([result],today=today)
    p.write_text(text.replace('\naction:\n','\naction: sel\n'))
    rebuilt=master_review.master_text([result],today=today,previous=p)
    assert '0 job(s) await a human decision; 1 already answered (1 review rows)' in rebuilt
    assert '\naction: select\n' in rebuilt

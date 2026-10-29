"""Owner-approved 29 October audit changes; neighbouring exclusions stay in force."""
import csv
from pathlib import Path
import pandas as pd
import pytest
from scripts import service_admin_pipeline_core as core
from pipeline.tests.test_service_admin_owner_selection_rules import make_job,run_rows

@pytest.mark.parametrize('title', ['Admin Officer (Northampton)','Administration Officer - Belfast','Admin Support Officer','Administration Clerk','Administrative Support','Office Admin - Temp','Warehouse Administrator','Engineering Administrator'])
def test_ordinary_admin_title_variants_are_eligible(title):
    assert core.classify_title(title)[0]=='HIGH_CONFIDENCE'

@pytest.mark.parametrize('title', ['Admin Manager','Senior Admin Officer','Warehouse Operative','Engineer','IT Helpdesk Administrator','Export Admin Officer','Accountant','Salesforce Administrator'])
def test_neighbouring_titles_remain_excluded(title):
    assert core.classify_title(title)[0]=='HARD_PASS'

@pytest.mark.parametrize('description,expected', [('Salary: Competitive, depending on experience','Competitive, depending on experience'),('Salary: DOE','DOE'),('Competitive salary plus pension','Competitive'),('We operate in a competitive market with excellent benefits',''),('Salary negotiable','negotiable')])
def test_only_explicit_pay_wording_is_recovered(description,expected):
    row=pd.Series(make_job('x','Administrator','',description))
    assert core.build_salary_details(row)[0]==expected

@pytest.mark.parametrize('description', ['Office records and customer enquiries.','Salary: Competitive, depending on experience. Office records.'])
def test_missing_pay_alone_does_not_drop_or_query(description):
    jobs,reports=run_rows([make_job('x','Administrator','',description)])
    assert 'x' in jobs
    assert jobs['x']['_review_required']==''
    assert reports['x']['salary_review_status']=='ok'

def test_known_high_pay_still_excluded():
    jobs,reports=run_rows([make_job('x','Administrator','', 'Salary £60,000 per year. Office administration.')])
    assert 'x' not in jobs

def test_new_approved_register_contains_all_fixed_snapshot_titles():
    register=core.load_title_register()
    for title in ['Accounting Support Clerk','Project Support Officer - Bristol','Temporary Customer Operations Executive','Service Controller and Parts Controller']:
        assert core.classify_title(title,register)[0]=='HIGH_CONFIDENCE'

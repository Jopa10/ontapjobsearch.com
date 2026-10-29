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


@pytest.mark.parametrize('title,description,expected_included', [
    ('Payroll Administrator','Pay £17.50-£19.00 per hour. Maintain payroll records.',True),
    ('Administrator','Pay £60,000 per year. Maintain office records.',False),
    ('Document Controller','Pay £46,000 per year. Maintain documents.',False),
])
def test_nonnumeric_additional_cannot_hide_numeric_description_pay(title,description,expected_included):
    row=make_job('pay-extra',title,'',description)
    row[core.COL['salary_additional']]='Plus Holiday Pay'
    text,source=core.build_salary_details(pd.Series(row))
    assert source=='description_fallback'
    assert '(Plus Holiday Pay)' in text
    jobs,reports=run_rows([row])
    assert ('pay-extra' in jobs)==expected_included
    assert reports['pay-extra']['annual_salary_upper']!=''


def test_numeric_additional_retains_priority():
    row=make_job('numeric-extra','Administrator','', 'Pay £60,000 per year.')
    row[core.COL['salary_additional']]='£30,000 per year'
    assert core.build_salary_details(pd.Series(row))==('£30,000 per year','structured')


@pytest.mark.parametrize('title',['Senior Bookkeeper (Part Time)','Senior Payroll Administrator (Part Time)','Fractional Senior Financial Controller Part-Time','Finance Manager - Part Time','Finance Team Leader - Part Time'])
def test_deferred_seniority_does_not_gain_auto_approval_from_missing_pay(title):
    row=make_job('deferred',title,'','20 hours per week. Maintain finance and payroll records.')
    jobs,reports=run_rows([row])
    assert 'deferred' not in jobs or jobs['deferred']['_review_required']=='1'



@pytest.mark.parametrize('description,expected', [
    ('£80k–£90k Fully remote Permanent, full-time Platform / Engineering', '£80,000 - £90,000 per year'),
    ('Salary: £50,000 - £60,000 FTE - Part time', '£50,000 - £60,000 per year (FTE)'),
    ('£27,000 + Flexitime + Training + Free Parking', '£27,000 per year'),
    ('Salary £28,000 - £30,000', '£28,000 - £30,000 per year'),
    ('Salary £40k–60k', '£40,000 - £60,000 per year'),
    ('Rate £20–40 per hour', '£20–£40 per hour'),
    ('Rate: £30.18ph Umbrella Co basis increasing to £39.55ph Umbrella Co basis after 13 weeks', '£30.18 per hour Umbrella Co basis increasing to £39.55 per hour'),
    ('Manage a £80k project budget and customer enquiries.', ''),
    ('£80k project budget and customer enquiries.', ''),
    ('Benefits include £100 shopping vouchers and £500 referral bonus.', ''),
])
def test_observed_salary_formats_and_non_pay_counterexamples(description, expected):
    assert core.extract_salary_from_description(description) == expected


@pytest.mark.parametrize('title,description', [
    ('Principal Database Administrator Fully Remote', '£80k–£90k Fully remote Permanent, full-time Platform / Engineering'),
    ('Administrator', 'Salary £60k - £65k'),
    ('Document Controller', 'Salary £46,000'),
    ('Group Financial Controller', 'Salary £50,000 - £60,000 FTE. Part-time 20 hours per week. The ideal candidate will be a professionally qualified accountant.'),
    ('Part time Financial Controller', '£65,000 - £70,000 FTE. ACA, ACCA or CIMA qualified, ideally with 3-5 years post qualification experience.'),
    ('Financial Controller', "Part time £42k - £46k FTE. We are looking for a qualified accountant (ACA, ACCA, CIMA or equivalent)."),
    ('Warehouse Administrator Nights', 'Operate forklifts and other heavy lifting equipment safely for materials movement.'),
    ('Warehouse Administrator', 'Experience operating forklifts and handling heavy materials safely.'),
])
def test_observed_ineligible_adverts_cannot_publish_automatically(title, description):
    jobs, reports = run_rows([make_job('blocked', title, '', description)])
    assert 'blocked' not in jobs


@pytest.mark.parametrize('title,description', [
    ('Financial Controller', 'Part-time 20 hours per week. Maintain finance records.'),
    ('Payroll Analyst', 'Part-time £30.18ph increasing to £39.55ph. Degree or equivalent. Support payroll transformation.'),
    ('Finance Assistant', 'ACCA preferred. Maintain invoices and reconciliations.'),
])
def test_specialist_or_ambiguous_finance_needs_review(title, description):
    jobs, reports = run_rows([make_job('review', title, '', description)])
    assert 'review' not in jobs or jobs['review']['_review_required'] == '1'


@pytest.mark.parametrize('title,description', [
    ('Warehouse Administrator', 'Maintain stock records, process orders and liaise with forklift drivers.'),
    ('Engineering Administrator', 'Maintain engineering audit documentation and schedule maintenance records.'),
    ('Database Records Administrator', 'Maintain office customer records using spreadsheets.'),
    ('Finance Assistant', 'AAT required. Maintain invoices and bank reconciliations.'),
    ('Payroll Administrator', 'Maintain employee payroll records and respond to enquiries.'),
    ('Credit Controller Part Time', '20 hours per week. Maintain debtor records and chase invoices.'),
])
def test_ordinary_office_counterexamples_remain_eligible(title, description):
    jobs, reports = run_rows([make_job('office', title, '', description)])
    assert 'office' in jobs
    assert jobs['office']['_review_required'] == ''

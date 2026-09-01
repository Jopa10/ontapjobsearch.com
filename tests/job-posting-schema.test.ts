import assert from 'node:assert/strict';
import test from 'node:test';
import {
  buildJobPostingSchema,
  hasCompleteJobDescription,
  isValidIsoDate,
} from '../lib/job-posting-schema';
import type { PublishedJob } from '../lib/published-jobs';

function job(overrides: Partial<PublishedJob> = {}): PublishedJob {
  return {
    job_id: 'job-1',
    title: 'Administrator',
    company: 'Example Recruitment - Agency - Permanent',
    advertiser_name: 'Example Recruitment',
    advertiser_type: 'Agency',
    location: 'Leeds',
    region: 'Yorkshire - West',
    country: 'UK',
    category: 'Admin/Service – Office Support',
    employment_type: 'Permanent',
    salary_min: '25000',
    salary_max: '28000',
    salary_period: 'Annual',
    salary_text: '£25,000 - £28,000 per year',
    work_pattern: 'Full Time',
    posted_date: '2026-08-12',
    posted_date_basis: 'ontap_first_published',
    closing_date: '',
    closing_datetime: '',
    description:
      'Example Recruitment is seeking an experienced administrator.\n\n' +
      'The role includes maintaining accurate records, answering enquiries, ' +
      'coordinating appointments and supporting the wider office team.\n\n' +
      'Applicants should have strong communication, organisation and IT skills, ' +
      'with previous office experience and the ability to manage priorities.',
    full_description: '',
    apply_url: 'https://example.com/apply/job-1',
    source: 'JobG8',
    working_arrangement: 'onsite_or_not_stated',
    working_arrangement_text: '',
    working_arrangement_evidence: '',
    slice_path: '/job-search/west-yorkshire/service-administrator-jobs',
    slice_label: 'Yorkshire - West Admin & Customer Service Jobs',
    ...overrides,
  };
}

test('stable Ontap first-published date makes a complete JobG8 job eligible', () => {
  const schema = buildJobPostingSchema(job(), 'https://www.ontapjobsearch.com/jobs/job-1');

  assert.ok(schema);
  assert.equal(schema.datePosted, '2026-08-12');
  assert.equal((schema.hiringOrganization as { name: string }).name, 'Confidential');
});

test('source date and JobG8 StartDate basis both take precedence when supplied', () => {
  for (const basis of ['source', 'jobg8_start_date']) {
    const schema = buildJobPostingSchema(
      job({ posted_date: '2026-08-01', posted_date_basis: basis }),
      'https://www.ontapjobsearch.com/jobs/job-1'
    );
    assert.equal(schema?.datePosted, '2026-08-01');
  }
});

test('NHS fractional source timestamps emit a factual Google date without inventing a timezone', () => {
  const schema = buildJobPostingSchema(
    job({
      job_id: 'nhs-5545061',
      source: 'NHS Jobs',
      company: 'Example NHS Foundation Trust',
      advertiser_name: 'Example NHS Foundation Trust',
      advertiser_type: '',
      posted_date: '2026-08-18T11:20:36.306867',
      posted_date_basis: 'source',
      closing_date: '2026-09-01',
    }),
    'https://www.ontapjobsearch.com/jobs/nhs-5545061'
  );

  assert.ok(schema);
  assert.equal(schema.datePosted, '2026-08-18');
  assert.equal(schema.validThrough, '2026-09-01T23:59:59+01:00');
});

test('fractional timezone-less timestamps remain rejected outside NHS Jobs', () => {
  const schema = buildJobPostingSchema(
    job({
      source: 'Teaching Vacancies',
      posted_date: '2026-08-18T11:20:36.306867',
      posted_date_basis: 'source',
    }),
    'https://www.ontapjobsearch.com/jobs/job-1'
  );

  assert.equal(schema, null);
});

test('teaser descriptions never emit JobPosting schema', () => {
  const description =
    'Administrator required for a busy office with varied duties and full-time hours ' +
    'click apply for full job details';
  assert.equal(hasCompleteJobDescription(description), false);
  assert.equal(
    buildJobPostingSchema(job({ description }), 'https://www.ontapjobsearch.com/jobs/job-1'),
    null
  );
});

test('invalid or unlabelled dates fail closed', () => {
  assert.equal(isValidIsoDate('2026-02-30'), false);
  assert.equal(
    buildJobPostingSchema(
      job({ posted_date_basis: '', posted_date: '2026-08-12' }),
      'https://www.ontapjobsearch.com/jobs/job-1'
    ),
    null
  );
});

test('direct employers remain named', () => {
  const schema = buildJobPostingSchema(
    job({
      company: 'Example Manufacturing Ltd - Company - Permanent',
      advertiser_name: 'Example Manufacturing Ltd',
      advertiser_type: 'Company',
    }),
    'https://www.ontapjobsearch.com/jobs/job-1'
  );

  assert.equal((schema?.hiringOrganization as { name: string }).name, 'Example Manufacturing Ltd');
});

test('fully remote jobs use Google remote fields without a false workplace', () => {
  const schema = buildJobPostingSchema(
    job({
      title: 'Training Administrator (Fully Remote)',
      location: 'London',
      description:
        job().description +
        '\n\nThis role is home-based with no geographical restriction for applicants ' +
        'who wish to apply from around the UK.',
    }),
    'https://www.ontapjobsearch.com/jobs/job-1'
  );

  assert.equal(schema?.jobLocationType, 'TELECOMMUTE');
  assert.equal((schema?.applicantLocationRequirements as { name: string }).name, 'United Kingdom');
  assert.equal('jobLocation' in (schema ?? {}), false);
});

test('generic locality is omitted while the factual region remains', () => {
  const schema = buildJobPostingSchema(
    job({ location: 'Not Specified', region: 'London' }),
    'https://www.ontapjobsearch.com/jobs/job-1'
  );
  const address = (schema?.jobLocation as { address: Record<string, string> }).address;

  assert.equal(address.addressLocality, undefined);
  assert.equal(address.addressRegion, 'London');
  assert.equal(address.addressCountry, 'GB');
});

test('valid expiry is emitted and invalid expiry fails closed', () => {
  const valid = buildJobPostingSchema(
    job({ closing_date: '2026-09-30' }),
    'https://www.ontapjobsearch.com/jobs/job-1'
  );
  assert.equal(valid?.validThrough, '2026-09-30T23:59:59+01:00');

  const invalid = buildJobPostingSchema(
    job({ closing_date: '30 September' }),
    'https://www.ontapjobsearch.com/jobs/job-1'
  );
  assert.equal(invalid, null);
});

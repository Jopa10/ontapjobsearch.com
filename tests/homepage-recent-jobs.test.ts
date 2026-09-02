import assert from 'node:assert/strict';
import test from 'node:test';
import { selectHomepageRecentJobs } from '../lib/homepage-recent-jobs';
import type { PublishedJob } from '../lib/published-jobs';

function job(
  job_id: string,
  title: string,
  category: string,
  region: string,
  posted_date = '2026-09-02',
  salary_text = '£25,000 per year'
): PublishedJob {
  return {
    job_id,
    title,
    category,
    region,
    posted_date,
    salary_text,
    slice_path: `/${region.toLowerCase()}/${category.toLowerCase()}-jobs`,
  } as PublishedJob;
}

test('homepage recent jobs prefer different roles and regions', () => {
  const selected = selectHomepageRecentJobs([
    job('5', 'GP Receptionist', 'Admin', 'London', '2026-09-02T09:00:00Z'),
    job('4', 'Medical Receptionist', 'Admin', 'London', '2026-09-02T08:59:00Z'),
    job('3', 'Support Worker', 'Support', 'Sussex'),
    job('2', 'Sales Adviser', 'Sales', 'North East'),
    job('1', 'Marketing Assistant', 'Marketing', 'Yorkshire'),
  ]);

  assert.deepEqual(
    selected.map((item) => item.job_id),
    ['5', '3', '2', '1']
  );
});

test('homepage recent jobs exclude vacancies without a clear numeric salary', () => {
  const selected = selectHomepageRecentJobs([
    job('5', 'GP Receptionist', 'Admin', 'London', '2026-09-02T09:00:00Z', ''),
    job('4', 'Office Administrator', 'Admin', 'Kent'),
    job('3', 'Support Worker', 'Support', 'Sussex'),
    job('2', 'Sales Adviser', 'Sales', 'North East'),
    job('1', 'Marketing Assistant', 'Marketing', 'Yorkshire'),
  ]);

  assert.equal(selected.length, 4);
  assert.ok(selected.every((item) => /\d/.test(item.salary_text)));
  assert.ok(!selected.some((item) => item.job_id === '5'));
});

test('homepage recent jobs fall back safely when fewer than four roles exist', () => {
  const selected = selectHomepageRecentJobs([
    job('4', 'Receptionist', 'Admin', 'London'),
    job('3', 'Administrator', 'Admin', 'Sussex'),
    job('2', 'Office Assistant', 'Admin', 'Kent'),
    job('1', 'Business Support Officer', 'Admin', 'Yorkshire'),
  ]);

  assert.equal(selected.length, 4);
  assert.equal(new Set(selected.map((item) => item.title)).size, 4);
});

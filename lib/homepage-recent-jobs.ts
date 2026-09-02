import type { PublishedJob } from '@/lib/published-jobs';

const recentWindowMs = 48 * 60 * 60 * 1000;

export function formatHomepageSalary(value: string): string {
  const cleaned = value.replaceAll('Â£', '£');
  if (!/\b(per year|per annum|annual(?:ly)?|p\.?a\.?)\b/i.test(cleaned)) return cleaned;

  return cleaned.replace(/£\s*(\d{4,})(?![\d,])/g, (_, amount: string) =>
    `£${Number(amount).toLocaleString('en-GB')}`
  );
}

function hasClearSalary(job: PublishedJob): boolean {
  return /\d/.test(job.salary_text.trim());
}

function sortNewest(jobs: PublishedJob[]): PublishedJob[] {
  return [...jobs].sort((left, right) => {
    const dateOrder = right.posted_date.localeCompare(left.posted_date);
    return dateOrder || right.job_id.localeCompare(left.job_id);
  });
}

function roleKey(job: PublishedJob): string {
  const routeRole = job.slice_path
    .split('/')
    .filter(Boolean)
    .at(-1)
    ?.replace(/-jobs$/, '');
  if (routeRole) return routeRole;

  return job.category.trim().toLowerCase() || 'other';
}

function titleKey(job: PublishedJob): string {
  return job.title
    .toLowerCase()
    .replace(/\b(gp|medical|temporary|temp|part[- ]?time|full[- ]?time|immediate start)\b/g, '')
    .replace(/[^a-z0-9]+/g, ' ')
    .trim();
}

function addDiverseJobs(candidates: PublishedJob[], selected: PublishedJob[], limit: number): void {
  const selectedIds = new Set(selected.map((job) => job.job_id));
  const roles = new Set(selected.map(roleKey));
  const regions = new Set(selected.map((job) => job.region.trim().toLowerCase()));
  const titles = new Set(selected.map(titleKey));

  const passes = [
    (job: PublishedJob) =>
      !roles.has(roleKey(job)) &&
      !regions.has(job.region.trim().toLowerCase()) &&
      !titles.has(titleKey(job)),
    (job: PublishedJob) => !roles.has(roleKey(job)) && !titles.has(titleKey(job)),
    (job: PublishedJob) =>
      !regions.has(job.region.trim().toLowerCase()) && !titles.has(titleKey(job)),
    (job: PublishedJob) => !titles.has(titleKey(job)),
    () => true,
  ];

  for (const pass of passes) {
    for (const job of candidates) {
      if (selected.length >= limit) return;
      if (selectedIds.has(job.job_id) || !pass(job)) continue;

      selected.push(job);
      selectedIds.add(job.job_id);
      roles.add(roleKey(job));
      regions.add(job.region.trim().toLowerCase());
      titles.add(titleKey(job));
    }
  }
}

export function selectHomepageRecentJobs(jobs: PublishedJob[], limit = 4): PublishedJob[] {
  if (limit <= 0 || jobs.length === 0) return [];

  const sorted = sortNewest(jobs.filter(hasClearSalary));
  if (sorted.length === 0) return [];
  const newestTimestamp = Math.max(
    ...sorted.map((job) => Date.parse(job.posted_date)).filter(Number.isFinite)
  );
  const recent = Number.isFinite(newestTimestamp)
    ? sorted.filter((job) => {
        const timestamp = Date.parse(job.posted_date);
        return Number.isFinite(timestamp) && timestamp >= newestTimestamp - recentWindowMs;
      })
    : sorted;

  const selected: PublishedJob[] = [];
  addDiverseJobs(recent, selected, limit);
  if (selected.length < limit) addDiverseJobs(sorted, selected, limit);
  return selected;
}

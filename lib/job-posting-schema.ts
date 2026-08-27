import { cleanEmployerName, employerFactLabel } from '@/lib/job-facts';
import type { PublishedJob } from '@/lib/published-jobs';

const INCOMPLETE_DESCRIPTION = /click apply for full job details|click apply for more details/i;
const GENERIC_LOCATION = /^(?:not specified|unknown|n\/?a|none)$/i;
const RELIABLE_POSTED_DATE_BASES = new Set(['source', 'jobg8_start_date', 'ontap_first_published']);

export type JobPostingSchema = Record<string, unknown>;

function text(value: unknown): string {
  return typeof value === 'string' ? value.trim() : '';
}

function isValidDateOnly(candidate: string): boolean {
  const dateOnly = candidate.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!dateOnly) return false;
  const year = Number(dateOnly[1]);
  const month = Number(dateOnly[2]);
  const day = Number(dateOnly[3]);
  const parsed = new Date(Date.UTC(year, month - 1, day));
  return (
    parsed.getUTCFullYear() === year &&
    parsed.getUTCMonth() === month - 1 &&
    parsed.getUTCDate() === day
  );
}

export function isValidIsoDate(value: string): boolean {
  const candidate = text(value);
  if (isValidDateOnly(candidate)) return true;

  if (candidate.length < 11 || !isValidDateOnly(candidate.slice(0, 10))) {
    return false;
  }

  return (
    /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:\d{2})$/.test(candidate) &&
    !Number.isNaN(Date.parse(candidate))
  );
}

export function hasCompleteJobDescription(value: string): boolean {
  const normalised = text(value).replace(/\s+/g, ' ');
  return normalised.length >= 200 && !INCOMPLETE_DESCRIPTION.test(normalised);
}

export function isFullyRemoteJob(job: PublishedJob): boolean {
  const title = text(job.title);
  const description = text(job.description);
  const combined = `${title}\n${description}`;

  if (/\b(?:fully|100%)\s+remote\b/i.test(combined)) return true;

  return (
    /\bhome[- ]based\b/i.test(combined) &&
    /\bno geographical restriction\b/i.test(description) &&
    /\b(?:around|across|within) the uk\b/i.test(description)
  );
}

function descriptionHtml(value: string): string {
  const escapeHtml = (content: string) =>
    content
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');

  return value
    .split(/\n{2,}/)
    .map((paragraph) => `<p>${escapeHtml(paragraph).replace(/\n/g, '<br>')}</p>`)
    .join('');
}

function postedDate(job: PublishedJob): string {
  const basis = text(job.posted_date_basis).toLowerCase();
  const legacyNeJobsSourceDate = job.source.toLowerCase() === 'nejobs' && !basis;

  if (
    (RELIABLE_POSTED_DATE_BASES.has(basis) || legacyNeJobsSourceDate) &&
    isValidIsoDate(job.posted_date)
  ) {
    return job.posted_date;
  }
  return '';
}

function validThrough(job: PublishedJob): string {
  if (isValidIsoDate(job.closing_datetime)) return job.closing_datetime;
  if (isValidIsoDate(job.closing_date)) {
    return `${job.closing_date.slice(0, 10)}T23:59:59+01:00`;
  }
  return '';
}

function hiringOrganizationName(job: PublishedJob): string {
  return employerFactLabel(job) === 'Recruiter'
    ? 'Confidential'
    : cleanEmployerName(job) || 'Confidential';
}

function physicalLocation(job: PublishedJob) {
  const locality = text(job.location);
  const region = text(job.region);
  if ((!locality || GENERIC_LOCATION.test(locality)) && !region) return null;

  return {
    '@type': 'Place',
    address: {
      '@type': 'PostalAddress',
      ...(!locality || GENERIC_LOCATION.test(locality) ? {} : { addressLocality: locality }),
      ...(region ? { addressRegion: region } : {}),
      addressCountry: 'GB',
    },
  };
}

export function buildJobPostingSchema(
  job: PublishedJob,
  canonicalUrl: string
): JobPostingSchema | null {
  if (!text(job.title) || !hasCompleteJobDescription(job.description)) return null;
  if (!/^https?:\/\//i.test(text(job.apply_url))) return null;

  const datePosted = postedDate(job);
  if (!datePosted) return null;

  const rawExpiry = text(job.closing_datetime) || text(job.closing_date);
  const expiry = validThrough(job);
  if (rawExpiry && !expiry) return null;

  const remote = isFullyRemoteJob(job);
  const location = remote ? null : physicalLocation(job);
  if (!remote && !location) return null;

  return {
    '@context': 'https://schema.org',
    '@type': 'JobPosting',
    title: job.title,
    description: descriptionHtml(job.description),
    datePosted,
    hiringOrganization: {
      '@type': 'Organization',
      name: hiringOrganizationName(job),
    },
    ...(remote
      ? {
          jobLocationType: 'TELECOMMUTE',
          applicantLocationRequirements: {
            '@type': 'Country',
            name: 'United Kingdom',
          },
        }
      : { jobLocation: location }),
    ...(expiry ? { validThrough: expiry } : {}),
    url: canonicalUrl,
  };
}

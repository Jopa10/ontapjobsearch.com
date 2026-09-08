import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import Papa from 'papaparse';
import { buildJobPostingSchema } from '../lib/job-posting-schema';
import { getPublishedJobs, type PublishedJob } from '../lib/published-jobs';
import {
  attemptKey,
  daysAgo,
  pacificDate,
  selectIndexingCandidates,
  type IndexingCandidate,
  type IndexingLane,
  type IndexingSource,
  type NotificationType,
} from '../lib/google-indexing-policy';

const SITE_URL = 'https://www.ontapjobsearch.com';
const ENDPOINT = 'https://indexing.googleapis.com/v3/urlNotifications:publish';
const STATE_PATH = path.join(process.cwd(), 'pipeline', 'manifests', 'google-indexing-state.json');
const FIRST_SEEN_PATH = path.join(
  process.cwd(),
  'pipeline',
  'reports-daily',
  'published-job-first-seen-history.csv'
);
const RUN_REPORT_PATH = process.env.GOOGLE_INDEXING_RUN_REPORT?.trim();
const DAILY_QUOTA = numberSetting('GOOGLE_INDEXING_DAILY_QUOTA', 200);
const NEW_JOBG8_RESERVE = numberSetting('GOOGLE_INDEXING_NEW_JOBG8_RESERVE', 160);
const NEW_NON_JOBG8_RESERVE = numberSetting('GOOGLE_INDEXING_NEW_NON_JOBG8_RESERVE', 20);
const DELETION_RESERVE = numberSetting('GOOGLE_INDEXING_DELETION_RESERVE', 20);
const SKIPPED_WINDOW_DAYS = numberSetting('GOOGLE_INDEXING_SKIPPED_WINDOW_DAYS', 7);
const RELEASE_RESERVES = /^(1|true|yes)$/i.test(
  process.env.GOOGLE_INDEXING_RELEASE_RESERVES?.trim() || 'false'
);

type SubmittedRecord = {
  fingerprint: string;
  source: IndexingSource;
  submittedAt: string;
  hasValidThrough: boolean;
};
type ObservedRecord = {
  fingerprint: string;
  source: IndexingSource;
  firstObservedDate: string;
  missingSinceDate?: string;
};
type AttemptRecord = {
  url: string;
  type: NotificationType;
  source: IndexingSource;
  lane: IndexingLane;
  attemptedAt: string;
  status: 'started' | 'success' | 'failure';
  httpStatus?: number;
};
type SkippedRecord = {
  fingerprint: string;
  source: IndexingSource;
  firstSkippedDate: string;
  postedDate: string;
  qualityScore: number;
  originalLane: 'new_jobg8' | 'new_non_jobg8';
};
type IndexingStateV2 = {
  version: 2;
  updatedAt: string;
  submitted: Record<string, SubmittedRecord>;
  observed: Record<string, ObservedRecord>;
  day: { date: string; attempts: AttemptRecord[] };
  skipped: Record<string, SkippedRecord>;
};
type LegacyState = { version: 1; updatedAt?: string; urls: Record<string, string> };
type CurrentJob = {
  job: PublishedJob;
  url: string;
  fingerprint: string;
  source: IndexingSource;
  postedDate: string;
  qualityScore: number;
  hasValidThrough: boolean;
};
type RunStatus = 'noop' | 'dry-run' | 'success' | 'partial' | 'failure';
type RunReport = {
  status: RunStatus;
  mode: 'live' | 'dry-run';
  pacificDate: string;
  dailyQuota: number;
  releaseReserves: boolean;
  eligibleLive: number;
  migratedFromV1: boolean;
  legacyDeletionsNeutralised: number;
  attemptsBeforeRun: number;
  candidates: Record<IndexingLane, number>;
  selected: Record<IndexingLane, number>;
  attempted: number;
  submitted: number;
  failed: number;
  allowanceRemaining: number;
  skippedNewToday: number;
  recentSkippedAvailable: number;
  quotaInvariantViolation: boolean;
  message: string;
};

class SubmissionError extends Error {
  constructor(
    message: string,
    readonly status: number
  ) {
    super(message);
  }
}

function numberSetting(name: string, fallback: number): number {
  const value = Number(process.env[name] || String(fallback));
  if (!Number.isInteger(value) || value < 0)
    throw new Error(`${name} must be a non-negative integer; got ${value}`);
  return value;
}

function jobUrl(jobId: string) {
  return `${SITE_URL}/jobs/${encodeURIComponent(jobId)}`;
}

function sourceGroup(source: string): IndexingSource {
  const normalised = source.trim().toLowerCase();
  if (normalised === 'jobg8') return 'jobg8';
  if (normalised === 'nhs jobs') return 'nhs';
  return 'other';
}

function inferSourceFromUrl(url: string): IndexingSource {
  const id = decodeURIComponent(url.split('/').pop() || '').toLowerCase();
  if (id.startsWith('nhs-')) return 'nhs';
  if (id.startsWith('teaching-vacancies-') || id.startsWith('nejobs-') || id.startsWith('vonne-'))
    return 'other';
  return 'jobg8';
}

function fingerprint(job: PublishedJob) {
  const schemaRelevantFields = {
    job_id: job.job_id,
    title: job.title,
    description: job.description,
    company: job.company,
    advertiser_name: job.advertiser_name,
    location: job.location,
    region: job.region,
    posted_date: job.posted_date,
    posted_date_basis: job.posted_date_basis,
    closing_date: job.closing_date,
    closing_datetime: job.closing_datetime,
    ...(sourceGroup(job.source) === 'nhs' ? { nhsSchemaVersion: 'posted-date-v1' } : {}),
  };
  return crypto.createHash('sha256').update(JSON.stringify(schemaRelevantFields)).digest('hex');
}

function qualityScore(job: PublishedJob): number {
  let score = 0;
  const employer = (job.company || job.advertiser_name).trim();
  const location = job.location.trim();
  if (employer && !/^(unknown|confidential|not specified)$/i.test(employer)) score += 4;
  if (
    location &&
    !/^(uk|united kingdom|england|scotland|wales|northern ireland|not specified|remote)$/i.test(
      location
    )
  )
    score += 4;
  if (job.description.trim().length >= 500) score += 2;
  if (job.description.trim().length >= 1_000) score += 1;
  if (/^\d{4}-\d{2}-\d{2}/.test(job.posted_date)) score += 1;
  return score;
}

function currentJobs(): Map<string, CurrentJob> {
  const current = new Map<string, CurrentJob>();
  for (const job of getPublishedJobs()) {
    const url = jobUrl(job.job_id);
    const schema = buildJobPostingSchema(job, url);
    if (!schema) continue;
    current.set(url, {
      job,
      url,
      fingerprint: fingerprint(job),
      source: sourceGroup(job.source),
      postedDate: job.posted_date,
      qualityScore: qualityScore(job),
      hasValidThrough: typeof schema.validThrough === 'string',
    });
  }
  return current;
}

function firstSeenDates(): Map<string, string> {
  if (!fs.existsSync(FIRST_SEEN_PATH)) return new Map();
  const parsed = Papa.parse<{ first_seen_date?: string; job_id?: string }>(
    fs.readFileSync(FIRST_SEEN_PATH, 'utf8'),
    {
      header: true,
      skipEmptyLines: true,
    }
  );
  return new Map(
    parsed.data
      .filter((row) => row.job_id?.trim() && /^\d{4}-\d{2}-\d{2}$/.test(row.first_seen_date || ''))
      .map((row) => [jobUrl(row.job_id!.trim()), row.first_seen_date!.trim()])
  );
}

function emptyState(date: string): IndexingStateV2 {
  return {
    version: 2,
    updatedAt: '',
    submitted: {},
    observed: {},
    day: { date, attempts: [] },
    skipped: {},
  };
}

function readRawState(): LegacyState | IndexingStateV2 | null {
  if (!fs.existsSync(STATE_PATH)) return null;
  const parsed = JSON.parse(fs.readFileSync(STATE_PATH, 'utf8')) as LegacyState | IndexingStateV2;
  if (parsed.version === 1 && parsed.urls && typeof parsed.urls === 'object') return parsed;
  if (parsed.version === 2 && parsed.submitted && parsed.observed && parsed.day && parsed.skipped)
    return parsed;
  throw new Error(`Unable to read ${STATE_PATH}: unsupported state format`);
}

function prepareState(
  raw: LegacyState | IndexingStateV2 | null,
  current: Map<string, CurrentJob>,
  date: string
) {
  if (!raw)
    return { state: emptyState(date), migratedFromV1: false, migrationFresh: new Set<string>() };
  if (raw.version === 2) {
    if (raw.day.date !== date) raw.day = { date, attempts: [] };
    return { state: raw, migratedFromV1: false, migrationFresh: new Set<string>() };
  }
  const state = emptyState(date);
  const seenDates = firstSeenDates();
  const migrationFresh = new Set<string>();
  for (const [url, hash] of Object.entries(raw.urls)) {
    state.submitted[url] = {
      fingerprint: hash,
      source: current.get(url)?.source ?? inferSourceFromUrl(url),
      submittedAt: raw.updatedAt || '',
      hasValidThrough: current.get(url)?.hasValidThrough ?? false,
    };
  }
  for (const [url, item] of current) {
    const firstSeen = seenDates.get(url);
    state.observed[url] = {
      fingerprint: item.fingerprint,
      source: item.source,
      firstObservedDate: firstSeen || daysAgo(date, SKIPPED_WINDOW_DAYS + 1),
    };
    if (firstSeen === date && !state.submitted[url]) migrationFresh.add(url);
  }
  return { state, migratedFromV1: true, migrationFresh };
}

function writeState(state: IndexingStateV2) {
  state.updatedAt = new Date().toISOString();
  state.submitted = Object.fromEntries(
    Object.entries(state.submitted).sort(([a], [b]) => a.localeCompare(b))
  );
  state.observed = Object.fromEntries(
    Object.entries(state.observed).sort(([a], [b]) => a.localeCompare(b))
  );
  state.skipped = Object.fromEntries(
    Object.entries(state.skipped).sort(([a], [b]) => a.localeCompare(b))
  );
  fs.mkdirSync(path.dirname(STATE_PATH), { recursive: true });
  fs.writeFileSync(STATE_PATH, `${JSON.stringify(state, null, 2)}\n`, 'utf8');
}

function laneCounts(items: IndexingCandidate[]): Record<IndexingLane, number> {
  const counts: Record<IndexingLane, number> = {
    new_jobg8: 0,
    new_non_jobg8: 0,
    deletion: 0,
    material_update: 0,
    recent_skipped: 0,
  };
  for (const item of items) counts[item.lane] += 1;
  return counts;
}

function buildCandidates(
  state: IndexingStateV2,
  current: Map<string, CurrentJob>,
  date: string,
  migrationFresh: Set<string>,
  migratedFromV1: boolean
) {
  let legacyDeletionsNeutralised = 0;
  const candidates: IndexingCandidate[] = [];
  for (const url of Object.keys(state.submitted)) {
    if (current.has(url)) continue;
    if (migratedFromV1) {
      delete state.submitted[url];
      delete state.observed[url];
      legacyDeletionsNeutralised += 1;
      continue;
    }
    const observed = state.observed[url] ?? {
      fingerprint: state.submitted[url].fingerprint,
      source: state.submitted[url].source,
      firstObservedDate: daysAgo(date, 1),
    };
    if (!observed.missingSinceDate) observed.missingSinceDate = date;
    state.observed[url] = observed;
    if (observed.missingSinceDate !== date) {
      delete state.submitted[url];
      delete state.observed[url];
      continue;
    }
    candidates.push({
      url,
      type: 'URL_DELETED',
      source: state.submitted[url].source,
      lane: 'deletion',
      postedDate: '',
      qualityScore: 0,
      deletionRisk: state.submitted[url].hasValidThrough ? 1 : 3,
    });
  }
  for (const [url, item] of current) {
    const observed = state.observed[url];
    const isNew = !observed || migrationFresh.has(url);
    if (isNew && !state.submitted[url]) {
      candidates.push({
        url,
        type: 'URL_UPDATED',
        source: item.source,
        lane: item.source === 'jobg8' ? 'new_jobg8' : 'new_non_jobg8',
        fingerprint: item.fingerprint,
        postedDate: item.postedDate,
        qualityScore: item.qualityScore,
        deletionRisk: 0,
      });
    } else if (observed && observed.fingerprint !== item.fingerprint) {
      candidates.push({
        url,
        type: 'URL_UPDATED',
        source: item.source,
        lane: 'material_update',
        fingerprint: item.fingerprint,
        postedDate: item.postedDate,
        qualityScore: item.qualityScore,
        deletionRisk: 0,
      });
    }
    state.observed[url] = {
      fingerprint: item.fingerprint,
      source: item.source,
      firstObservedDate: observed?.firstObservedDate || date,
    };
  }
  for (const url of Object.keys(state.observed)) {
    if (!current.has(url) && !state.submitted[url]) delete state.observed[url];
  }
  const oldestAllowed = daysAgo(date, SKIPPED_WINDOW_DAYS - 1);
  for (const [url, skipped] of Object.entries(state.skipped)) {
    const item = current.get(url);
    if (
      !item ||
      item.fingerprint !== skipped.fingerprint ||
      skipped.firstSkippedDate < oldestAllowed ||
      state.submitted[url]
    ) {
      delete state.skipped[url];
      continue;
    }
    if (candidates.some((candidate) => candidate.url === url)) continue;
    candidates.push({
      url,
      type: 'URL_UPDATED',
      source: skipped.source,
      lane: skipped.firstSkippedDate === date ? skipped.originalLane : 'recent_skipped',
      fingerprint: skipped.fingerprint,
      postedDate: skipped.postedDate,
      qualityScore: skipped.qualityScore,
      deletionRisk: 0,
    });
  }
  return { candidates, legacyDeletionsNeutralised };
}

async function submit(candidate: IndexingCandidate, token: string) {
  const response = await fetch(ENDPOINT, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: candidate.url, type: candidate.type }),
  });
  const body = await response.text();
  if (!response.ok)
    throw new SubmissionError(
      `${candidate.type} ${candidate.url} failed: HTTP ${response.status} ${body}`,
      response.status
    );
}

function writeRunReport(report: RunReport) {
  if (!RUN_REPORT_PATH) return;
  fs.mkdirSync(path.dirname(RUN_REPORT_PATH), { recursive: true });
  fs.writeFileSync(RUN_REPORT_PATH, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
}

function reportAndLog(report: RunReport) {
  writeRunReport(report);
  console.log(`Run status: ${report.status}`);
  console.log(`Pacific quota date: ${report.pacificDate}`);
  console.log(
    `Daily attempts: ${report.attemptsBeforeRun + report.attempted}/${report.dailyQuota}`
  );
  console.log(`Submitted this run: ${report.submitted}; failed: ${report.failed}`);
  console.log(`Allowance remaining: ${report.allowanceRemaining}`);
  console.log(`Candidates: ${JSON.stringify(report.candidates)}`);
  console.log(`Selected: ${JSON.stringify(report.selected)}`);
  console.log(report.message);
}

async function main() {
  const dryRun = process.argv.includes('--dry-run');
  const date = pacificDate(new Date());
  if (NEW_JOBG8_RESERVE + NEW_NON_JOBG8_RESERVE + DELETION_RESERVE > DAILY_QUOTA)
    throw new Error('Protected Google Indexing allocations exceed the daily quota');
  if (DAILY_QUOTA < 1) throw new Error('GOOGLE_INDEXING_DAILY_QUOTA must be at least 1');
  const current = currentJobs();
  const prepared = prepareState(readRawState(), current, date);
  const state = prepared.state;
  const built = buildCandidates(
    state,
    current,
    date,
    prepared.migrationFresh,
    prepared.migratedFromV1
  );
  const selected = selectIndexingCandidates(built.candidates, state.day.attempts, {
    dailyQuota: DAILY_QUOTA,
    newJobg8Reserve: NEW_JOBG8_RESERVE,
    newNonJobg8Reserve: NEW_NON_JOBG8_RESERVE,
    deletionReserve: DELETION_RESERVE,
    releaseReserves: RELEASE_RESERVES,
  });
  const attemptsBeforeRun = state.day.attempts.length;
  const quotaInvariantViolation = attemptsBeforeRun + selected.length > DAILY_QUOTA;
  if (quotaInvariantViolation)
    throw new Error('Selection would exceed the shared Pacific-day quota');
  const newCandidates = built.candidates.filter(
    (candidate) => candidate.lane === 'new_jobg8' || candidate.lane === 'new_non_jobg8'
  );
  const selectedKeys = new Set(selected.map((item) => attemptKey(item.type, item.url)));
  for (const candidate of newCandidates) {
    if (!candidate.fingerprint || state.submitted[candidate.url]) continue;
    state.skipped[candidate.url] = {
      fingerprint: candidate.fingerprint,
      source: candidate.source,
      firstSkippedDate: state.skipped[candidate.url]?.firstSkippedDate || date,
      postedDate: candidate.postedDate,
      qualityScore: candidate.qualityScore,
      originalLane: candidate.lane as 'new_jobg8' | 'new_non_jobg8',
    };
  }
  const base = {
    mode: dryRun ? ('dry-run' as const) : ('live' as const),
    pacificDate: date,
    dailyQuota: DAILY_QUOTA,
    releaseReserves: RELEASE_RESERVES,
    eligibleLive: current.size,
    migratedFromV1: prepared.migratedFromV1,
    legacyDeletionsNeutralised: built.legacyDeletionsNeutralised,
    attemptsBeforeRun,
    candidates: laneCounts(built.candidates),
    selected: laneCounts(selected),
    skippedNewToday: newCandidates.filter(
      (item) => !selectedKeys.has(attemptKey(item.type, item.url))
    ).length,
    recentSkippedAvailable: built.candidates.filter((item) => item.lane === 'recent_skipped')
      .length,
    quotaInvariantViolation,
  };
  if (dryRun) {
    for (const candidate of selected)
      console.log(`[dry-run] ${candidate.lane} ${candidate.type} ${candidate.url}`);
    reportAndLog({
      ...base,
      status: 'dry-run',
      attempted: 0,
      submitted: 0,
      failed: 0,
      allowanceRemaining: DAILY_QUOTA - attemptsBeforeRun,
      message: `[dry-run] Would attempt ${selected.length} notifications without carrying legacy updates into the new policy.`,
    });
    return;
  }
  const token = process.env.GOOGLE_INDEXING_ACCESS_TOKEN?.trim();
  if (!token) {
    const report: RunReport = {
      ...base,
      status: 'failure',
      attempted: 0,
      submitted: 0,
      failed: 0,
      allowanceRemaining: DAILY_QUOTA - attemptsBeforeRun,
      message: 'GOOGLE_INDEXING_ACCESS_TOKEN is required for a live submission.',
    };
    reportAndLog(report);
    throw new Error(report.message);
  }
  let submitted = 0;
  let failed = 0;
  let attempted = 0;
  let terminalFailure = '';
  for (const candidate of selected) {
    const attempt: AttemptRecord = {
      url: candidate.url,
      type: candidate.type,
      source: candidate.source,
      lane: candidate.lane,
      attemptedAt: new Date().toISOString(),
      status: 'started',
    };
    state.day.attempts.push(attempt);
    attempted += 1;
    writeState(state);
    try {
      await submit(candidate, token);
      attempt.status = 'success';
      submitted += 1;
      if (candidate.type === 'URL_DELETED') {
        delete state.submitted[candidate.url];
        delete state.observed[candidate.url];
      } else if (candidate.fingerprint) {
        const item = current.get(candidate.url);
        state.submitted[candidate.url] = {
          fingerprint: candidate.fingerprint,
          source: candidate.source,
          submittedAt: new Date().toISOString(),
          hasValidThrough: item?.hasValidThrough ?? false,
        };
        delete state.skipped[candidate.url];
      }
      console.log(`${candidate.lane} ${candidate.type} ${candidate.url}`);
    } catch (error) {
      failed += 1;
      attempt.status = 'failure';
      attempt.httpStatus = error instanceof SubmissionError ? error.status : undefined;
      terminalFailure = error instanceof Error ? error.message : String(error);
      console.error(terminalFailure);
      if (attempt.httpStatus === 429 || attempt.httpStatus === 403) {
        writeState(state);
        break;
      }
    }
    writeState(state);
  }
  writeState(state);
  const allowanceRemaining = DAILY_QUOTA - state.day.attempts.length;
  const status: RunStatus =
    failed > 0
      ? 'failure'
      : attempted === 0
        ? 'noop'
        : submitted < selected.length
          ? 'partial'
          : 'success';
  const report: RunReport = {
    ...base,
    status,
    attempted,
    submitted,
    failed,
    allowanceRemaining,
    message:
      terminalFailure ||
      (attempted
        ? `Attempted ${attempted} selected notifications under the shared Pacific-day allowance.`
        : 'No eligible notification was selected in this run.'),
  };
  reportAndLog(report);
  if (failed > 0) throw new Error(report.message);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exitCode = 1;
});

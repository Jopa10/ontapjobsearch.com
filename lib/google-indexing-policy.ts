export type IndexingSource = 'jobg8' | 'nhs' | 'other' | 'unknown';
export type IndexingLane =
  | 'new_jobg8'
  | 'new_non_jobg8'
  | 'deletion'
  | 'material_update'
  | 'recent_skipped';
export type NotificationType = 'URL_UPDATED' | 'URL_DELETED';

export type IndexingCandidate = {
  url: string;
  type: NotificationType;
  source: IndexingSource;
  lane: IndexingLane;
  fingerprint?: string;
  postedDate: string;
  qualityScore: number;
  deletionRisk: number;
};

export type AttemptSummary = {
  url: string;
  type: NotificationType;
  lane: IndexingLane;
};

export type SelectionConfig = {
  dailyQuota: number;
  newJobg8Reserve: number;
  newNonJobg8Reserve: number;
  deletionReserve: number;
  releaseReserves: boolean;
};

const PROTECTED_LANES: Array<{
  lane: IndexingLane;
  reserve: keyof Pick<
    SelectionConfig,
    'newJobg8Reserve' | 'newNonJobg8Reserve' | 'deletionReserve'
  >;
}> = [
  { lane: 'new_jobg8', reserve: 'newJobg8Reserve' },
  { lane: 'new_non_jobg8', reserve: 'newNonJobg8Reserve' },
  { lane: 'deletion', reserve: 'deletionReserve' },
];

const RELEASE_ORDER: IndexingLane[] = [
  'new_jobg8',
  'deletion',
  'new_non_jobg8',
  'material_update',
  'recent_skipped',
];

export function pacificDate(now: Date): string {
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Los_Angeles',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(now);
}

export function daysAgo(date: string, days: number): string {
  const parsed = new Date(`${date}T12:00:00Z`);
  parsed.setUTCDate(parsed.getUTCDate() - days);
  return parsed.toISOString().slice(0, 10);
}

export function attemptKey(type: NotificationType, url: string): string {
  return `${type} ${url}`;
}

export function compareCandidates(left: IndexingCandidate, right: IndexingCandidate): number {
  if (left.type === 'URL_DELETED' || right.type === 'URL_DELETED') {
    const risk = right.deletionRisk - left.deletionRisk;
    if (risk) return risk;
  }
  const date = right.postedDate.localeCompare(left.postedDate);
  if (date) return date;
  const quality = right.qualityScore - left.qualityScore;
  if (quality) return quality;
  return left.url.localeCompare(right.url);
}

export function selectIndexingCandidates(
  candidates: IndexingCandidate[],
  previousAttempts: AttemptSummary[],
  config: SelectionConfig
): IndexingCandidate[] {
  const attemptedKeys = new Set(
    previousAttempts.map((attempt) => attemptKey(attempt.type, attempt.url))
  );
  const selectedKeys = new Set<string>();
  const selected: IndexingCandidate[] = [];
  const attemptedByLane = new Map<IndexingLane, number>();

  for (const attempt of previousAttempts) {
    attemptedByLane.set(attempt.lane, (attemptedByLane.get(attempt.lane) ?? 0) + 1);
  }

  const available = candidates
    .filter((candidate) => !attemptedKeys.has(attemptKey(candidate.type, candidate.url)))
    .sort(compareCandidates);
  const remainingDaily = () =>
    Math.max(0, config.dailyQuota - previousAttempts.length - selected.length);

  function takeLane(lane: IndexingLane, count: number) {
    if (count <= 0 || remainingDaily() <= 0) return;
    let taken = 0;
    for (const candidate of available) {
      if (candidate.lane !== lane || selectedKeys.has(attemptKey(candidate.type, candidate.url))) {
        continue;
      }
      selected.push(candidate);
      selectedKeys.add(attemptKey(candidate.type, candidate.url));
      taken += 1;
      if (taken >= count) break;
      if (remainingDaily() <= 0) break;
    }
  }

  for (const protectedLane of PROTECTED_LANES) {
    const alreadyAttempted = attemptedByLane.get(protectedLane.lane) ?? 0;
    takeLane(protectedLane.lane, Math.max(0, config[protectedLane.reserve] - alreadyAttempted));
  }

  // A future quota increase needs only dailyQuota changed. Capacity above the
  // three protected reservations is immediately available to fresh JobG8 jobs.
  const protectedTotal =
    config.newJobg8Reserve + config.newNonJobg8Reserve + config.deletionReserve;
  const unreservedCapacity = Math.max(0, config.dailyQuota - protectedTotal);
  const protectedAlreadyAttempted = PROTECTED_LANES.reduce(
    (total, item) => total + Math.min(config[item.reserve], attemptedByLane.get(item.lane) ?? 0),
    0
  );
  const unreservedAlreadyAttempted = Math.max(
    0,
    previousAttempts.length - protectedAlreadyAttempted
  );
  takeLane('new_jobg8', Math.max(0, unreservedCapacity - unreservedAlreadyAttempted));

  if (config.releaseReserves && remainingDaily() > 0) {
    for (const lane of RELEASE_ORDER) {
      takeLane(lane, remainingDaily());
      if (remainingDaily() <= 0) break;
    }
  }

  return selected;
}

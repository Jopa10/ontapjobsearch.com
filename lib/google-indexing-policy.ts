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
  source?: IndexingSource;
};

export type SelectionConfig = {
  dailyQuota: number;
  newNonJobg8Reserve: number;
  deletionReserve: number;
};

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
  const previousDeletions = previousAttempts.filter((attempt) => attempt.type === 'URL_DELETED').length;
  const previousNonJobG8 = previousAttempts.filter(
    (attempt) => attempt.source ? attempt.source !== 'jobg8' : attempt.lane === 'new_non_jobg8'
  ).length;

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

  // Deletions retain a fixed allowance and are processed before updates.
  takeLane('deletion', Math.max(0, config.deletionReserve - previousDeletions));

  // JobG8 is the commercial priority. Every available JobG8 candidate can use
  // the remaining quota; its old 160-slot reserve is a minimum, not a ceiling.
  const isJobG8 = (candidate: IndexingCandidate) => candidate.source === 'jobg8';
  for (const candidate of available) {
    if (!isJobG8(candidate) || candidate.lane === 'deletion' || selectedKeys.has(attemptKey(candidate.type, candidate.url))) continue;
    if (remainingDaily() <= 0) break;
    selected.push(candidate);
    selectedKeys.add(attemptKey(candidate.type, candidate.url));
  }

  // Non-paying sources are capped at 10% of the 200-call daily allowance.
  // Unused JobG8 capacity is never released to them.
  const nonJobG8Remaining = Math.max(0, config.newNonJobg8Reserve - previousNonJobG8);
  for (const candidate of available) {
    if (isJobG8(candidate) || candidate.lane === 'deletion' || selectedKeys.has(attemptKey(candidate.type, candidate.url))) continue;
    if (remainingDaily() <= 0 || selected.filter((item) => !isJobG8(item) && item.lane !== 'deletion').length >= nonJobG8Remaining) break;
    selected.push(candidate);
    selectedKeys.add(attemptKey(candidate.type, candidate.url));
  }

  return selected;
}

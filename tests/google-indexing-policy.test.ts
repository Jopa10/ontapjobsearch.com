import assert from 'node:assert/strict';
import test from 'node:test';
import {
  createDeletionCandidate,
  pacificDate,
  selectIndexingCandidates,
  type IndexingCandidate,
  type IndexingLane,
} from '../lib/google-indexing-policy';

function candidates(lane: IndexingLane, count: number): IndexingCandidate[] {
  return Array.from({ length: count }, (_, index) => ({
    url: `https://www.ontapjobsearch.com/jobs/${lane}-${String(index).padStart(3, '0')}`,
    type: lane === 'deletion' ? 'URL_DELETED' : 'URL_UPDATED',
    source: lane === 'new_non_jobg8' ? 'nhs' : 'jobg8',
    lane,
    fingerprint: lane === 'deletion' ? undefined : `hash-${index}`,
    postedDate: `2026-09-${String(30 - (index % 20)).padStart(2, '0')}`,
    qualityScore: 12 - (index % 3),
    deletionRisk: lane === 'deletion' ? 3 : 0,
  }));
}

const config = {
  dailyQuota: 200,
  newNonJobg8Reserve: 20,
  deletionReserve: 20,
  partTimeJobG8DailyLimit: 25,
};

test('keeps deletion notifications queued until Google accepts them', () => {
  const url = 'https://www.ontapjobsearch.com/jobs/jobg8-queued-deletion';
  const submitted = { source: 'jobg8' as const, hasValidThrough: false };
  const observation = {
    fingerprint: 'old-fingerprint',
    source: 'jobg8' as const,
    firstObservedDate: '2026-10-01',
  };

  const firstDay = createDeletionCandidate(url, submitted, observation, '2026-10-09');
  assert.equal(firstDay.observed.missingSinceDate, '2026-10-09');
  assert.equal(firstDay.candidate.type, 'URL_DELETED');

  const nextDay = createDeletionCandidate(
    url,
    submitted,
    firstDay.observed,
    '2026-10-10'
  );
  assert.equal(nextDay.observed.missingSinceDate, '2026-10-09');
  assert.equal(nextDay.candidate.type, 'URL_DELETED');
  assert.deepEqual(selectIndexingCandidates([nextDay.candidate], [], config), [
    nextDay.candidate,
  ]);
});

test('uses JobG8 capacity first and caps non-JobG8 jobs at 20', () => {
  const selected = selectIndexingCandidates(
    [
      ...candidates('new_jobg8', 250),
      ...candidates('new_non_jobg8', 40),
      ...candidates('deletion', 40),
      ...candidates('material_update', 20),
    ],
    [],
    config
  );
  assert.equal(selected.length, 200);
  assert.equal(selected.filter((item) => item.source === 'jobg8' && item.type === 'URL_UPDATED').length, 180);
  assert.equal(selected.filter((item) => item.source !== 'jobg8' && item.type === 'URL_UPDATED').length, 0);
  assert.equal(selected.filter((item) => item.type === 'URL_DELETED').length, 20);
});

test('does not release unused JobG8 capacity to non-JobG8 jobs', () => {
  const pool = [
    ...candidates('new_jobg8', 250),
    ...candidates('new_non_jobg8', 5),
    ...candidates('deletion', 5),
  ];
  const selected = selectIndexingCandidates(pool, [], config);
  assert.equal(selected.length, 200);
  assert.equal(selected.filter((item) => item.source === 'jobg8' && item.type === 'URL_UPDATED').length, 195);
  assert.equal(selected.filter((item) => item.source !== 'jobg8' && item.type === 'URL_UPDATED').length, 0);
});

test('shares the daily allowance and never retries the same URL/type', () => {
  const pool = candidates('new_jobg8', 250);
  const previous = pool.slice(0, 150).map((item) => ({
    url: item.url,
    type: item.type,
    lane: item.lane,
  }));
  const selected = selectIndexingCandidates(pool, previous, config);
  assert.equal(selected.length, 50);
  assert.equal(
    selected.some((item) => previous.some((attempt) => attempt.url === item.url)),
    false
  );
});

test('uses the real America/Los_Angeles day across daylight-saving boundaries', () => {
  assert.equal(pacificDate(new Date('2026-03-08T07:59:59Z')), '2026-03-07');
  assert.equal(pacificDate(new Date('2026-03-08T08:00:00Z')), '2026-03-08');
  assert.equal(pacificDate(new Date('2026-11-01T06:59:59Z')), '2026-10-31');
  assert.equal(pacificDate(new Date('2026-11-01T07:00:00Z')), '2026-11-01');
});

test('uses a future quota increase without changing the protected allocations', () => {
  const selected = selectIndexingCandidates(
    [
      ...candidates('new_jobg8', 2_000),
      ...candidates('new_non_jobg8', 30),
      ...candidates('deletion', 30),
    ],
    [],
    { ...config, dailyQuota: 1_500 }
  );
  assert.equal(selected.length, 1_500);
  assert.equal(selected.filter((item) => item.source === 'jobg8' && item.type === 'URL_UPDATED').length, 1_480);
  assert.equal(selected.filter((item) => item.source !== 'jobg8' && item.type === 'URL_UPDATED').length, 0);
  assert.equal(selected.filter((item) => item.lane === 'deletion').length, 20);
});

test('retains future protected slots after an earlier high-quota push run', () => {
  const earlier = candidates('new_jobg8', 500).map((item) => ({
    url: item.url,
    type: item.type,
    lane: item.lane,
  }));
  const selected = selectIndexingCandidates(candidates('new_jobg8', 2_000), earlier, {
    ...config,
    dailyQuota: 1_500,
  });
  assert.equal(selected.length, 1_000);
  assert.equal(earlier.length + selected.length, 1_500);
});


test('prioritises up to 25 part-time JobG8 URLs without exceeding the daily quota', () => {
  const partTime = Array.from({ length: 35 }, (_, index) => ({
    ...candidates('new_jobg8', 1)[0],
    url: `https://www.ontapjobsearch.com/jobs/part-time-${String(index).padStart(2, '0')}`,
    partTimeJobG8Priority: true,
    popularPartTimeMarket: index < 10,
    postedDate: `2026-11-${String(25 - (index % 20)).padStart(2, '0')}`,
    partTimeQueueDate: '2026-11-25',
  }));
  const selected = selectIndexingCandidates(
    [...partTime, ...candidates('new_jobg8', 175), ...candidates('new_non_jobg8', 20)],
    [],
    config
  );

  assert.equal(selected.length, 200);
  assert.equal(selected.filter((item) => item.partTimeJobG8Priority).length, 25);
  assert.equal(selected.filter((item) => item.source !== 'jobg8' && item.type === 'URL_UPDATED').length, 0);
});

test('processes older part-time batches first, then popular markets and newest jobs', () => {
  const partTime = [
    { ...candidates('new_jobg8', 1)[0], url: 'https://example.com/older-batch-popular-newest', partTimeJobG8Priority: true, popularPartTimeMarket: true, partTimeQueueDate: '2026-11-20', postedDate: '2026-11-19' },
    { ...candidates('new_jobg8', 1)[0], url: 'https://example.com/older-batch-popular-older', partTimeJobG8Priority: true, popularPartTimeMarket: true, partTimeQueueDate: '2026-11-20', postedDate: '2026-11-18' },
    { ...candidates('new_jobg8', 1)[0], url: 'https://example.com/older-batch-other-market', partTimeJobG8Priority: true, popularPartTimeMarket: false, partTimeQueueDate: '2026-11-20', postedDate: '2026-11-25' },
    { ...candidates('new_jobg8', 1)[0], url: 'https://example.com/new-batch-popular', partTimeJobG8Priority: true, popularPartTimeMarket: true, partTimeQueueDate: '2026-11-25', postedDate: '2026-11-25' },
  ];
  const selected = selectIndexingCandidates(partTime, [], {
    ...config,
    dailyQuota: 2,
    deletionReserve: 0,
    partTimeJobG8DailyLimit: 2,
  });

  assert.deepEqual(selected.map((item) => item.url), [
    'https://example.com/older-batch-popular-newest',
    'https://example.com/older-batch-popular-older',
  ]);
});

test('counts earlier part-time submissions against the Pacific-day cap', () => {
  const previouslySubmitted = Array.from({ length: 25 }, (_, index) => ({
    url: `https://www.ontapjobsearch.com/jobs/already-sent-${index}`,
    type: 'URL_UPDATED' as const,
    lane: 'new_jobg8' as const,
    source: 'jobg8' as const,
    partTimeJobG8Priority: true,
  }));
  const selected = selectIndexingCandidates(
    [
      ...Array.from({ length: 10 }, (_, index) => ({
        ...candidates('new_jobg8', 1)[0],
        url: `https://www.ontapjobsearch.com/jobs/part-time-new-${index}`,
        partTimeJobG8Priority: true,
      })),
      ...candidates('new_jobg8', 3),
    ],
    previouslySubmitted,
    { ...config, dailyQuota: 30 }
  );

  assert.equal(selected.filter((item) => item.partTimeJobG8Priority).length, 0);
  assert.equal(selected.length, 3);
});

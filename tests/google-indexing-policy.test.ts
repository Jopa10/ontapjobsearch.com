import assert from 'node:assert/strict';
import test from 'node:test';
import {
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
  newJobg8Reserve: 160,
  newNonJobg8Reserve: 20,
  deletionReserve: 20,
  releaseReserves: false,
};

test('preserves the agreed 160/20/20 allocations on push runs', () => {
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
  assert.deepEqual(
    Object.fromEntries(
      [...new Set(selected.map((item) => item.lane))].map((lane) => [
        lane,
        selected.filter((item) => item.lane === lane).length,
      ])
    ),
    { new_jobg8: 160, new_non_jobg8: 20, deletion: 20 }
  );
});

test('releases unused reservations only in the final scheduled/manual run', () => {
  const pool = [
    ...candidates('new_jobg8', 250),
    ...candidates('new_non_jobg8', 5),
    ...candidates('deletion', 5),
  ];
  assert.equal(selectIndexingCandidates(pool, [], config).length, 170);
  const released = selectIndexingCandidates(pool, [], { ...config, releaseReserves: true });
  assert.equal(released.length, 200);
  assert.equal(released.filter((item) => item.lane === 'new_jobg8').length, 190);
});

test('shares the daily allowance and never retries the same URL/type', () => {
  const pool = candidates('new_jobg8', 250);
  const previous = pool.slice(0, 150).map((item) => ({
    url: item.url,
    type: item.type,
    lane: item.lane,
  }));
  const selected = selectIndexingCandidates(pool, previous, { ...config, releaseReserves: true });
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
  assert.equal(selected.filter((item) => item.lane === 'new_jobg8').length, 1_460);
  assert.equal(selected.filter((item) => item.lane === 'new_non_jobg8').length, 20);
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
  assert.equal(selected.length, 960);
  assert.equal(earlier.length + selected.length, 1_460);
});

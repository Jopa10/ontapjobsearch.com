import type { Metadata } from 'next';
import Link from 'next/link';
import generatedJobs from '@/generated/published-jobs-search.json';
import { searchJobs } from '@/lib/job-search';
import type { PublishedJob } from '@/lib/published-jobs';

export const metadata: Metadata = {
  title: 'Search UK Jobs | Ontap Job Search',
  description:
    'Search current Ontap jobs by role, keyword and location. Results are generated from the current published job supply.',
  robots: {
    index: false,
    follow: true,
  },
};

export const preferredRegion = 'lhr1';

type SearchParams = Promise<Record<string, string | string[] | undefined>>;
type CorrectionScope = 'query' | 'location';
type CorrectionVocabularies = Record<CorrectionScope, Map<string, number>>;

type SearchResolution = {
  formQuery: string;
  formLocation: string;
  searchQuery: string;
  searchLocation: string;
  reinterpreted: boolean;
};

const jobs = generatedJobs as PublishedJob[];
let correctionVocabularyCache: CorrectionVocabularies | undefined;
const correctionResultCache = new Map<string, string>();

function firstValue(value: string | string[] | undefined): string {
  return Array.isArray(value) ? value[0] || '' : value || '';
}

function cleanSalary(value: string): string {
  return value.replaceAll('Â£', '£');
}

function getJobPath(jobId: string): string {
  return `/jobs/${encodeURIComponent(jobId)}`;
}

function normaliseToken(value: string): string {
  return value
    .normalize('NFKD')
    .replace(/\p{Diacritic}/gu, '')
    .toLowerCase()
    .replace(/[^a-z0-9]/g, '');
}

function wordTokens(value: string): string[] {
  return value
    .normalize('NFKD')
    .replace(/\p{Diacritic}/gu, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .trim()
    .split(/\s+/)
    .filter(Boolean);
}

function fieldContainsAllWords(value: string, wanted: string[]): boolean {
  if (!wanted.length) return false;
  const available = new Set(wordTokens(value));
  return wanted.every((token) => available.has(token));
}

function inputEvidence(value: string): { role: boolean; geo: boolean } {
  const wanted = wordTokens(value);
  if (!wanted.length) return { role: false, geo: false };

  let role = false;
  let geo = false;

  for (const job of jobs) {
    if (
      !role &&
      [job.title, job.category, job.slice_label].some((field) => fieldContainsAllWords(field, wanted))
    ) {
      role = true;
    }

    if (
      !geo &&
      [job.location, job.region].some((field) => fieldContainsAllWords(field, wanted))
    ) {
      geo = true;
    }

    if (role && geo) break;
  }

  return { role, geo };
}

function roleAliases(value: string): string {
  return value
    .replace(/\boffice\b/gi, 'admin')
    .replace(/\bclerical\b/gi, 'admin')
    .replace(/\s+/g, ' ')
    .trim();
}

function damerauLevenshtein(a: string, b: string): number {
  if (a === b) return 0;
  if (!a.length) return b.length;
  if (!b.length) return a.length;

  const matrix = Array.from({ length: a.length + 1 }, () =>
    new Array<number>(b.length + 1).fill(0)
  );
  for (let i = 0; i <= a.length; i += 1) matrix[i][0] = i;
  for (let j = 0; j <= b.length; j += 1) matrix[0][j] = j;

  for (let i = 1; i <= a.length; i += 1) {
    for (let j = 1; j <= b.length; j += 1) {
      const substitution = a[i - 1] === b[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,
        matrix[i][j - 1] + 1,
        matrix[i - 1][j - 1] + substitution
      );

      if (
        i > 1 &&
        j > 1 &&
        a[i - 1] === b[j - 2] &&
        a[i - 2] === b[j - 1]
      ) {
        matrix[i][j] = Math.min(matrix[i][j], matrix[i - 2][j - 2] + 1);
      }
    }
  }

  return matrix[a.length][b.length];
}

function addVocabularyValue(counts: Map<string, number>, value: string) {
  for (const rawToken of value.split(/\s+/)) {
    const token = normaliseToken(rawToken);
    if (token.length < 4) continue;
    counts.set(token, (counts.get(token) || 0) + 1);
  }
}

function correctionVocabularies(): CorrectionVocabularies {
  if (correctionVocabularyCache) return correctionVocabularyCache;

  const query = new Map<string, number>();
  const location = new Map<string, number>();

  for (const job of jobs) {
    for (const value of [job.title, job.category, job.slice_label, job.company, job.advertiser_name]) {
      addVocabularyValue(query, value);
    }

    for (const value of [job.location, job.region]) {
      addVocabularyValue(query, value);
      addVocabularyValue(location, value);
    }
  }

  correctionVocabularyCache = { query, location };
  correctionResultCache.clear();
  return correctionVocabularyCache;
}

function correctSearchText(input: string, scope: CorrectionScope): string {
  const trimmed = input.trim();
  if (!trimmed) return trimmed;

  const cacheKey = `${scope}:${trimmed.toLowerCase()}`;
  const cached = correctionResultCache.get(cacheKey);
  if (cached !== undefined) return cached;

  const vocabulary = correctionVocabularies()[scope];
  const corrected = trimmed.split(/\s+/).map((rawToken) => {
    const token = normaliseToken(rawToken);
    if (token.length < 4 || vocabulary.has(token)) return rawToken;

    const allowedDistance = token.length >= 8 ? 2 : 1;
    const candidates: Array<{ token: string; distance: number; count: number }> = [];

    for (const [candidate, count] of vocabulary) {
      if (candidate[0] !== token[0]) continue;
      if (Math.abs(candidate.length - token.length) > allowedDistance) continue;

      const distance = damerauLevenshtein(token, candidate);
      if (distance <= allowedDistance) candidates.push({ token: candidate, distance, count });
    }

    candidates.sort((a, b) => a.distance - b.distance || b.count - a.count || a.token.localeCompare(b.token));
    if (!candidates.length) return rawToken;

    const best = candidates[0];
    const runnerUp = candidates[1];
    if (runnerUp && runnerUp.distance === best.distance) return rawToken;

    return best.token;
  }).join(' ');

  if (correctionResultCache.size >= 500) correctionResultCache.clear();
  correctionResultCache.set(cacheKey, corrected);
  return corrected;
}

function resolveSearchInputs(originalQuery: string, originalLocation: string): SearchResolution {
  const queryAsQuery = correctSearchText(originalQuery, 'query');
  const queryAsLocation = correctSearchText(originalQuery, 'location');
  const locationAsQuery = correctSearchText(originalLocation, 'query');
  const locationAsLocation = correctSearchText(originalLocation, 'location');

  const queryEvidence = inputEvidence(queryAsQuery);
  const locationRoleEvidence = inputEvidence(locationAsQuery);

  let formQuery = queryAsQuery;
  let formLocation = locationAsLocation;
  let reinterpreted = false;

  // Be forgiving when the user puts the place in the first box and the role in
  // the second. Role evidence wins over polluted source location fields: a few
  // bad location strings containing words such as "admin" must not block the swap.
  if (
    queryAsQuery &&
    originalLocation &&
    queryEvidence.geo &&
    !queryEvidence.role &&
    locationRoleEvidence.role
  ) {
    formQuery = locationAsQuery;
    formLocation = queryAsLocation;
    reinterpreted = true;
  } else if (
    !queryAsQuery &&
    originalLocation &&
    locationRoleEvidence.role
  ) {
    // A role typed into the location box should still behave as a role search.
    formQuery = locationAsQuery;
    formLocation = '';
    reinterpreted = true;
  }

  return {
    formQuery,
    formLocation,
    searchQuery: roleAliases(formQuery),
    searchLocation: formLocation,
    reinterpreted,
  };
}

function SearchForm({ query, location }: { query: string; location: string }) {
  return (
    <form method="get" action="/jobs/search" className="grid gap-3 sm:grid-cols-[1fr_1fr_auto] sm:items-end">
      <label className="min-w-0" htmlFor="job-search-query">
        <span className="mb-1 block px-1 text-xs font-semibold text-gray-500">Role or keyword</span>
        <input
          id="job-search-query"
          name="q"
          type="search"
          defaultValue={query}
          autoCorrect="on"
          spellCheck={true}
          placeholder="e.g. Administrator, Customer Service, PA"
          className="w-full min-w-0 rounded-lg border border-gray-300 bg-white px-4 py-3 text-base text-gray-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        />
      </label>

      <label className="min-w-0" htmlFor="job-search-location">
        <span className="mb-1 block px-1 text-xs font-semibold text-gray-500">Location</span>
        <input
          id="job-search-location"
          name="location"
          type="search"
          defaultValue={location}
          autoCorrect="on"
          spellCheck={true}
          placeholder="e.g. Newcastle, Surrey, Leeds"
          className="w-full min-w-0 rounded-lg border border-gray-300 bg-white px-4 py-3 text-base text-gray-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        />
      </label>

      <button
        type="submit"
        className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white transition hover:bg-blue-700"
      >
        Search jobs →
      </button>
    </form>
  );
}

function ResultCard({ job }: { job: PublishedJob }) {
  const company = job.company || job.advertiser_name;

  return (
    <article className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
      <h2 className="text-lg font-semibold leading-snug text-gray-900">
        <Link href={getJobPath(job.job_id)} className="hover:text-blue-700">
          {job.title}
        </Link>
      </h2>

      <p className="mt-1 text-sm text-gray-600">
        {[company, job.location].filter(Boolean).join(' • ')}
      </p>

      {job.salary_text ? (
        <p className="mt-2 text-sm font-semibold text-gray-900">{cleanSalary(job.salary_text)}</p>
      ) : null}

      <div className="mt-4 flex flex-wrap items-center gap-3 text-sm">
        <Link href={getJobPath(job.job_id)} className="font-semibold text-blue-700 hover:text-blue-900">
          View job →
        </Link>
        {job.slice_path && job.slice_path !== '/browse-jobs' ? (
          <Link href={job.slice_path} className="text-gray-600 hover:text-blue-700">
            More {job.region || 'current'} jobs
          </Link>
        ) : null}
      </div>
    </article>
  );
}

export default async function Page({ searchParams }: { searchParams: SearchParams }) {
  const params = await searchParams;
  const originalQuery = firstValue(params.q).trim();
  const originalLocation = firstValue(params.location).trim();
  const searched = Boolean(originalQuery || originalLocation);

  const resolved = resolveSearchInputs(originalQuery, originalLocation);
  const matches = searchJobs(jobs, resolved.searchQuery, resolved.searchLocation);
  const visibleMatches = matches.slice(0, 60);

  const spellingCorrected = !resolved.reinterpreted && (
    resolved.formQuery !== originalQuery || resolved.formLocation !== originalLocation
  );

  return (
    <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
      <nav className="mb-4 text-sm text-gray-500" aria-label="Breadcrumb">
        <Link href="/" className="hover:text-blue-700">
          Home
        </Link>
        <span className="mx-2">/</span>
        <span className="text-gray-700">Search jobs</span>
      </nav>

      <div className="rounded-2xl border border-gray-200 bg-gray-50 p-5 sm:p-6">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900">Search current jobs</h1>
        <p className="mt-2 max-w-3xl text-gray-600">
          Search Ontap's current published jobs by role, keyword and location. No account required.
        </p>
      </div>

      <div className="sticky top-2 z-20 mt-3 rounded-xl border border-gray-200 bg-white/95 p-3 shadow-md backdrop-blur">
        <SearchForm query={resolved.formQuery} location={resolved.formLocation} />
        {spellingCorrected ? (
          <p className="mt-2 px-1 text-sm text-gray-600">
            Spelling corrected to {[resolved.formQuery && `“${resolved.formQuery}”`, resolved.formLocation && `in ${resolved.formLocation}`].filter(Boolean).join(' ')}.
          </p>
        ) : resolved.reinterpreted ? (
          <p className="mt-2 px-1 text-sm text-gray-600">
            Interpreted as {[resolved.formQuery && `“${resolved.formQuery}”`, resolved.formLocation && `in ${resolved.formLocation}`].filter(Boolean).join(' ')}.
          </p>
        ) : null}
      </div>

      {!searched ? (
        <section className="py-12 text-center">
          <h2 className="text-xl font-semibold text-gray-900">Enter a role, keyword or location</h2>
          <p className="mt-2 text-gray-600">
            Or <Link href="/browse-jobs" className="font-medium text-blue-700">browse jobs by role and region</Link>.
          </p>
        </section>
      ) : (
        <section className="mt-8">
          <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
            <div>
              <h2 className="text-2xl font-semibold tracking-tight text-gray-900">
                {matches.length} matching job{matches.length === 1 ? '' : 's'}
              </h2>
              <p className="mt-1 text-sm text-gray-600">
                {[resolved.formQuery && `“${resolved.formQuery}”`, resolved.formLocation && `in ${resolved.formLocation}`].filter(Boolean).join(' ')}
              </p>
            </div>
            <Link href="/browse-jobs" className="text-sm font-semibold text-blue-700 hover:text-blue-900">
              Browse all job pages →
            </Link>
          </div>

          {visibleMatches.length > 0 ? (
            <>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {visibleMatches.map((job) => (
                  <ResultCard key={job.job_id} job={job} />
                ))}
              </div>
              {matches.length > visibleMatches.length ? (
                <p className="mt-5 text-sm text-gray-500">
                  Showing the first {visibleMatches.length} matches. Add a more specific role or location to narrow the results.
                </p>
              ) : null}
            </>
          ) : (
            <div className="rounded-xl border border-gray-200 bg-gray-50 p-8 text-center">
              <h2 className="text-xl font-semibold text-gray-900">No current matches found</h2>
              <p className="mt-2 text-gray-600">
                Try a broader job title or location, or browse the current regional job pages.
              </p>
              <Link
                href="/browse-jobs"
                className="mt-5 inline-block rounded-lg bg-blue-600 px-5 py-2.5 font-semibold text-white hover:bg-blue-700"
              >
                Browse jobs →
              </Link>
            </div>
          )}
        </section>
      )}
    </main>
  );
}

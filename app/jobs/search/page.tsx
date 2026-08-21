import type { Metadata } from 'next';
import Link from 'next/link';
import { searchJobs } from '@/lib/job-search';
import {
  getJobPath,
  getPublishedJobs,
  type PublishedJob,
} from '@/lib/published-jobs';

export const metadata: Metadata = {
  title: 'Search UK Jobs | Ontap Job Search',
  description:
    'Search current Ontap jobs by role, keyword and location. Results are generated from the current published job supply.',
  robots: {
    index: false,
    follow: true,
  },
};

type SearchParams = Promise<Record<string, string | string[] | undefined>>;

type CorrectionScope = 'query' | 'location';

function firstValue(value: string | string[] | undefined): string {
  return Array.isArray(value) ? value[0] || '' : value || '';
}

function cleanSalary(value: string): string {
  return value.replaceAll('Â£', '£');
}

function normaliseToken(value: string): string {
  return value
    .normalize('NFKD')
    .replace(/\p{Diacritic}/gu, '')
    .toLowerCase()
    .replace(/[^a-z0-9]/g, '');
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

function correctionVocabulary(jobs: PublishedJob[], scope: CorrectionScope): Map<string, number> {
  const counts = new Map<string, number>();

  for (const job of jobs) {
    const values = scope === 'location'
      ? [job.location, job.region]
      : [job.title, job.category, job.company, job.advertiser_name, job.location, job.region];

    for (const value of values) {
      for (const rawToken of value.split(/\s+/)) {
        const token = normaliseToken(rawToken);
        if (token.length < 4) continue;
        counts.set(token, (counts.get(token) || 0) + 1);
      }
    }
  }

  return counts;
}

function correctSearchText(input: string, jobs: PublishedJob[], scope: CorrectionScope): string {
  if (!input.trim()) return input.trim();

  const vocabulary = correctionVocabulary(jobs, scope);
  const corrected = input.trim().split(/\s+/).map((rawToken) => {
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
  });

  return corrected.join(' ');
}

function SearchForm({ query, location }: { query: string; location: string }) {
  return (
    <form method="get" action="/jobs/search" className="grid gap-3 sm:grid-cols-[1fr_1fr_auto]">
      <label className="sr-only" htmlFor="job-search-query">
        Role or keyword
      </label>
      <input
        id="job-search-query"
        name="q"
        type="search"
        defaultValue={query}
        autoCorrect="on"
        spellCheck={true}
        placeholder="e.g. Administrator, Customer Service, PA"
        className="min-w-0 rounded-lg border border-gray-300 bg-white px-4 py-3 text-base text-gray-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
      />

      <label className="sr-only" htmlFor="job-search-location">
        Location
      </label>
      <input
        id="job-search-location"
        name="location"
        type="search"
        defaultValue={location}
        autoCorrect="on"
        spellCheck={true}
        placeholder="e.g. Newcastle, Surrey, Leeds"
        className="min-w-0 rounded-lg border border-gray-300 bg-white px-4 py-3 text-base text-gray-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
      />

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

  const jobs = getPublishedJobs();
  const query = correctSearchText(originalQuery, jobs, 'query');
  const location = correctSearchText(originalLocation, jobs, 'location');
  const corrected = query !== originalQuery || location !== originalLocation;

  const matches = searchJobs(jobs, query, location);
  const visibleMatches = matches.slice(0, 60);

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
        <SearchForm query={query} location={location} />
        {corrected ? (
          <p className="mt-2 px-1 text-sm text-gray-600">
            Spelling corrected to {[query && `“${query}”`, location && `in ${location}`].filter(Boolean).join(' ')}.
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
                {[query && `“${query}”`, location && `in ${location}`].filter(Boolean).join(' ')}
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
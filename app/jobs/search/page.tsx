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

function firstValue(value: string | string[] | undefined): string {
  return Array.isArray(value) ? value[0] || '' : value || '';
}

function cleanSalary(value: string): string {
  return value.replaceAll('Â£', '£');
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
  const query = firstValue(params.q).trim();
  const location = firstValue(params.location).trim();
  const searched = Boolean(query || location);

  const matches = searchJobs(getPublishedJobs(), query, location);
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
        <div className="mt-5">
          <SearchForm query={query} location={location} />
        </div>
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

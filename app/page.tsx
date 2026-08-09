import type { Metadata } from 'next';
import Link from 'next/link';
import {
  getCityPageJobs,
  newcastleServiceAdministratorPage,
} from '@/lib/city-page-data';
import {
  getJobPath,
  getPublishedJobs,
  type PublishedJob,
} from '@/lib/published-jobs';

const canonicalUrl = 'https://www.ontapjobsearch.com/';

export const metadata: Metadata = {
  title: 'UK Jobs by Role and Region | Ontap Job Search',
  description:
    'Search and browse current UK admin, office support, customer service and support worker jobs by role and region. Updated daily with direct application links.',
  alternates: { canonical: canonicalUrl },
};

type RegionLink = {
  label: string;
  href: string;
  count: number;
};

const adminRegionRoutes = [
  { label: 'North East', href: '/north-east/service-administrator-jobs' },
  { label: 'Hampshire', href: '/hampshire/service-administrator-jobs' },
  { label: 'Coventry & Warwickshire', href: '/coventry-warwickshire/service-administrator-jobs' },
  { label: 'Sussex', href: '/sussex/service-administrator-jobs' },
  { label: 'Surrey', href: '/surrey/service-administrator-jobs' },
  { label: 'Kent', href: '/kent/service-administrator-jobs' },
  { label: 'West Yorkshire', href: '/west-yorkshire/service-administrator-jobs' },
  { label: 'South Yorkshire', href: '/south-yorkshire/service-administrator-jobs' },
  { label: 'North Yorkshire', href: '/north-yorkshire/service-administrator-jobs' },
  { label: 'Central & Inner London', href: '/london/service-administrator-jobs' },
  { label: 'Outer London', href: '/london/outer-service-administrator-jobs' },
];

const supportWorkerRoutes = [
  { label: 'North East', href: '/north-east/support-worker' },
  { label: 'Hampshire', href: '/hampshire/support-worker' },
  { label: 'Sussex', href: '/sussex/support-worker' },
  { label: 'West Yorkshire', href: '/west-yorkshire/support-worker' },
  { label: 'South Yorkshire', href: '/south-yorkshire/support-worker' },
  { label: 'South Cumbria', href: '/cumbria-south/support-worker' },
];

function cleanSalary(value: string): string {
  return value.replaceAll('Â£', '£');
}

function countBySlice(jobs: PublishedJob[], slicePath: string): number {
  return jobs.reduce((count, job) => count + (job.slice_path === slicePath ? 1 : 0), 0);
}

function withCounts(
  jobs: PublishedJob[],
  routes: Array<{ label: string; href: string }>
): RegionLink[] {
  return routes
    .map((route) => ({ ...route, count: countBySlice(jobs, route.href) }))
    .filter((route) => route.count > 0);
}

function SearchPanel({ totalJobs }: { totalJobs: number }) {
  return (
    <section
      aria-labelledby="homepage-search-heading"
      className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm"
    >
      <h2 id="homepage-search-heading" className="text-lg font-semibold text-gray-900">
        Search jobs by role, keyword or location
      </h2>

      <form method="get" action="/jobs/search" className="mt-3 grid gap-2.5">
        <label className="sr-only" htmlFor="homepage-job-query">
          Role or keyword
        </label>
        <div className="relative">
          <svg
            aria-hidden="true"
            className="pointer-events-none absolute left-3.5 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-4.35-4.35m1.35-5.15a6.5 6.5 0 11-13 0 6.5 6.5 0 0113 0z"
            />
          </svg>
          <input
            id="homepage-job-query"
            name="q"
            type="search"
            placeholder="e.g. Administrator, Customer Service, PA"
            className="w-full rounded-lg border border-gray-300 bg-white py-2.5 pl-11 pr-4 text-base text-gray-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <label className="sr-only" htmlFor="homepage-job-location">
          Location
        </label>
        <div className="relative">
          <svg
            aria-hidden="true"
            className="pointer-events-none absolute left-3.5 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 21s6-5.1 6-11a6 6 0 10-12 0c0 5.9 6 11 6 11z"
            />
            <circle cx="12" cy="10" r="2" strokeWidth={2} />
          </svg>
          <input
            id="homepage-job-location"
            name="location"
            type="search"
            placeholder="e.g. Newcastle, Surrey, Leeds"
            className="w-full rounded-lg border border-gray-300 bg-white py-2.5 pl-11 pr-4 text-base text-gray-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <button
          type="submit"
          className="rounded-lg bg-blue-600 px-5 py-2.5 font-semibold text-white transition hover:bg-blue-700"
        >
          Search jobs →
        </button>
      </form>

      <p className="mt-2 text-center text-xs text-gray-500">
        {totalJobs.toLocaleString('en-GB')} current jobs • No account needed
      </p>
    </section>
  );
}

function RegionGrid({ regions }: { regions: RegionLink[] }) {
  return (
    <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {regions.map((region) => (
        <Link
          key={region.href}
          href={region.href}
          className="group flex min-h-16 items-center justify-between gap-3 rounded-lg border border-gray-200 bg-white px-3 py-2 transition hover:border-blue-300 hover:bg-blue-50"
        >
          <span>
            <span className="block text-sm font-semibold leading-snug text-gray-900 group-hover:text-blue-800">
              {region.label}
            </span>
            <span className="mt-0.5 block text-xs text-gray-500">
              {region.count} current job{region.count === 1 ? '' : 's'}
            </span>
          </span>
          <span aria-hidden="true" className="text-blue-600">
            →
          </span>
        </Link>
      ))}
    </div>
  );
}

function CurrentJobCard({ job }: { job: PublishedJob }) {
  const company = job.company || job.advertiser_name;

  return (
    <article className="border-b border-gray-200 py-2.5 last:border-b-0">
      <Link href={getJobPath(job.job_id)} className="group block">
        <div className="flex items-start justify-between gap-4">
          <div className="min-w-0">
            <h3 className="font-semibold leading-snug text-gray-900 group-hover:text-blue-700">
              {job.title}
            </h3>
            <p className="mt-0.5 text-sm leading-snug text-gray-600">
              {[company, job.location].filter(Boolean).join(' • ')}
            </p>
            {job.salary_text ? (
              <p className="mt-0.5 text-sm font-medium text-gray-800">{cleanSalary(job.salary_text)}</p>
            ) : null}
          </div>
          <span aria-hidden="true" className="mt-1 shrink-0 text-blue-600">
            →
          </span>
        </div>
      </Link>
    </article>
  );
}

export default function Page() {
  const jobs = getPublishedJobs();
  const adminRegions = withCounts(jobs, adminRegionRoutes);
  const supportWorkerRegions = withCounts(jobs, supportWorkerRoutes);
  const newcastleJobs = getCityPageJobs(newcastleServiceAdministratorPage);

  if (newcastleJobs.length >= newcastleServiceAdministratorPage.minimumJobs) {
    adminRegions.splice(1, 0, {
      label: 'Newcastle',
      href: newcastleServiceAdministratorPage.route,
      count: newcastleJobs.length,
    });
  }

  const currentJobs = jobs.slice(0, 4);

  return (
    <>
      <style>{`
        body:has(main[data-homepage]) footer > div {
          padding-top: 1.75rem;
          padding-bottom: 1.75rem;
        }

        body:has(main[data-homepage]) footer > div > div:first-child {
          gap: 1rem;
        }

        body:has(main[data-homepage]) footer h3,
        body:has(main[data-homepage]) footer h4 {
          margin-bottom: 0.5rem;
        }

        body:has(main[data-homepage]) footer > div > div:last-child {
          margin-top: 1.25rem;
          padding-top: 1rem;
        }
      `}</style>

      <main data-homepage>
        <section className="border-b border-gray-100 bg-gradient-to-b from-white to-gray-50">
          <div className="mx-auto grid max-w-7xl gap-4 px-4 py-4 sm:px-6 lg:grid-cols-[1.2fr_0.8fr] lg:items-center lg:px-8 lg:py-5">
            <div>
              <h1 className="max-w-3xl text-3xl font-bold leading-[1.04] tracking-tight text-gray-950 sm:text-4xl">
                Find admin, office support and customer service jobs across the UK
              </h1>
              <p className="mt-2 max-w-2xl text-base leading-7 text-gray-600 sm:text-lg">
                Curated UK jobs, updated daily. Browse by role and region, or search the current job supply directly.
              </p>
              <div className="mt-2 flex flex-wrap gap-x-5 gap-y-1 text-sm font-medium text-gray-600">
                <span>Apply direct</span>
                <span>No signup</span>
                <span>Updated daily</span>
              </div>
            </div>

            <SearchPanel totalJobs={jobs.length} />
          </div>
        </section>

        <div className="mx-auto max-w-7xl px-4 py-3 sm:px-6 lg:px-8">
          <section aria-labelledby="browse-role-heading">
            <div className="flex flex-wrap items-end justify-between gap-2">
              <div>
                <h2 id="browse-role-heading" className="text-2xl font-bold tracking-tight text-gray-900">
                  Browse by role and region
                </h2>
                <p className="mt-0.5 text-sm text-gray-600">
                  Regional pages stay compact here as Ontap adds more coverage.
                </p>
              </div>
              <Link href="/browse-jobs" className="text-sm font-semibold text-blue-700 hover:text-blue-900">
                View all job pages →
              </Link>
            </div>

            <div className="mt-3 grid gap-3 lg:grid-cols-[1fr_270px]">
              <div id="admin-regions" className="rounded-xl border border-gray-200 bg-gray-50 p-3.5 sm:p-4">
                <div className="mb-3">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Admin, office support & customer service
                  </h3>
                  <p className="mt-0.5 text-sm text-gray-600">Current regional job pages</p>
                </div>
                {adminRegions.length > 0 ? <RegionGrid regions={adminRegions} /> : null}
              </div>

              <div id="support-worker-regions" className="rounded-xl border border-gray-200 bg-white p-3.5 sm:p-4">
                <h3 className="text-lg font-semibold text-gray-900">Support worker jobs</h3>
                <p className="mt-0.5 text-sm text-gray-600">Current regional supply</p>
                <div className="mt-3 grid gap-1.5">
                  {supportWorkerRegions.map((region) => (
                    <Link
                      key={region.href}
                      href={region.href}
                      className="flex items-center justify-between rounded-lg border border-gray-200 px-3 py-2 text-sm transition hover:border-blue-300 hover:bg-blue-50"
                    >
                      <span>
                        <span className="font-semibold text-gray-900">{region.label}</span>
                        <span className="ml-2 text-xs text-gray-500">{region.count}</span>
                      </span>
                      <span aria-hidden="true" className="text-blue-600">→</span>
                    </Link>
                  ))}
                </div>
              </div>
            </div>
          </section>

          <section className="mt-5 grid gap-3 lg:grid-cols-[1fr_300px]" aria-labelledby="current-jobs-heading">
            <div className="rounded-xl border border-gray-200 bg-white p-4">
              <div className="flex items-center justify-between gap-3">
                <h2 id="current-jobs-heading" className="text-xl font-bold text-gray-900">Current jobs</h2>
                <Link href="/jobs/search?q=&location=" className="text-sm font-semibold text-blue-700 hover:text-blue-900">
                  Search jobs →
                </Link>
              </div>
              <div className="mt-1">
                {currentJobs.map((job) => (
                  <CurrentJobCard key={job.job_id} job={job} />
                ))}
              </div>
            </div>

            <aside className="rounded-xl border border-blue-100 bg-blue-50 p-4">
              <h2 className="text-lg font-semibold text-gray-900">Built for a quicker job search</h2>
              <div className="mt-3 grid gap-3 text-sm leading-snug text-gray-700">
                <div>
                  <div className="font-semibold text-gray-900">Apply direct</div>
                  <p className="mt-0.5">Ontap sends you towards the employer application route.</p>
                </div>
                <div>
                  <div className="font-semibold text-gray-900">No signup</div>
                  <p className="mt-0.5">Browse and search without creating an account.</p>
                </div>
                <div>
                  <div className="font-semibold text-gray-900">Fresh regional pages</div>
                  <p className="mt-0.5">Current job supply is refreshed as new roles are published.</p>
                </div>
              </div>
            </aside>
          </section>
        </div>
      </main>
    </>
  );
}

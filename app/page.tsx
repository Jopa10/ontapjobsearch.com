import type { Metadata } from 'next';
import Link from 'next/link';
import {
  cityPageDefinitions,
  getCityPageJobs,
  isCityPageActive,
} from '@/lib/city-page-data';
import { getPublishedDynamicSlices } from '@/lib/configured-job-slices';
import {
  getJobPath,
  getPublishedJobs,
  type PublishedJob,
} from '@/lib/published-jobs';
import { selectHomepageRecentJobs } from '@/lib/homepage-recent-jobs';

const canonicalUrl = 'https://www.ontapjobsearch.com/';
const homepageCityMinimumJobs = 4;

export const metadata: Metadata = {
  title: 'UK Jobs by Role and Region | Ontap Job Search',
  description:
    'Search and browse current UK admin, office support, customer service, sales advisor, marketing, HR, recruitment, legal assistant, paralegal and support worker jobs by role and region. Updated daily with direct application links.',
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
  { label: 'London', href: '/london/service-administrator-jobs' },
];

const supportWorkerRoutes = [
  { label: 'North East', href: '/north-east/support-worker' },
  { label: 'Hampshire', href: '/hampshire/support-worker' },
  { label: 'Sussex', href: '/sussex/support-worker' },
  { label: 'West Yorkshire', href: '/west-yorkshire/support-worker' },
  { label: 'South Yorkshire', href: '/south-yorkshire/support-worker' },
  { label: 'South Cumbria', href: '/cumbria-south/support-worker' },
];

const customerSalesHomepageLabels: Record<string, string> = {
  London: 'London',
  'Greater Manchester - Manchester & Salford': 'Manchester & Salford',
  'Yorkshire - West': 'West Yorkshire',
};

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

function publishedDynamicAdminLinks(jobs: PublishedJob[]): RegionLink[] {
  return getPublishedDynamicSlices()
    .filter((slice) => slice.category === 'admin_service')
    .map((slice) => ({
      label: slice.region,
      href: slice.route,
      count: countBySlice(jobs, slice.route),
    }))
    .filter((route) => route.count > 0)
    .sort((left, right) => left.label.localeCompare(right.label, 'en-GB'));
}

function publishedDynamicCustomerSalesLinks(jobs: PublishedJob[]): RegionLink[] {
  return getPublishedDynamicSlices()
    .filter((slice) => slice.category === 'customer_sales')
    .map((slice) => ({
      label: customerSalesHomepageLabels[slice.region] ?? slice.region,
      href: slice.route,
      count: countBySlice(jobs, slice.route),
    }))
    .filter((route) => route.count > 0)
    .sort((left, right) => left.label.localeCompare(right.label, 'en-GB'));
}

function publishedDynamicLegalLinks(jobs: PublishedJob[]): RegionLink[] {
  return getPublishedDynamicSlices()
    .filter((slice) => slice.category === 'legal_assistant_paralegal')
    .map((slice) => ({
      label: slice.region,
      href: slice.route,
      count: countBySlice(jobs, slice.route),
    }))
    .filter((route) => route.count > 0)
    .sort((left, right) => left.label.localeCompare(right.label, 'en-GB'));
}

function publishedDynamicMarketingLinks(jobs: PublishedJob[]): RegionLink[] {
  return getPublishedDynamicSlices()
    .filter((slice) => slice.category === 'marketing')
    .map((slice) => ({
      label: slice.region,
      href: slice.route,
      count: countBySlice(jobs, slice.route),
    }))
    .filter((route) => route.count > 0)
    .sort((left, right) => left.label.localeCompare(right.label, 'en-GB'));
}

function publishedDynamicHrRecruitmentLinks(jobs: PublishedJob[]): RegionLink[] {
  return getPublishedDynamicSlices()
    .filter((slice) => slice.category === 'hr_recruitment')
    .map((slice) => ({
      label: slice.region,
      href: slice.route,
      count: countBySlice(jobs, slice.route),
    }))
    .filter((route) => route.count > 0)
    .sort((left, right) => left.label.localeCompare(right.label, 'en-GB'));
}

function activeCityLinks(kind: 'admin' | 'support'): RegionLink[] {
  return cityPageDefinitions
    .filter((definition) => isCityPageActive(definition))
    .filter((definition) =>
      kind === 'admin'
        ? definition.parentRoute.endsWith('/service-administrator-jobs')
        : definition.parentRoute.endsWith('/support-worker')
    )
    .map((definition) => ({
      label: definition.displayName,
      href: definition.route,
      count: getCityPageJobs(definition).length,
    }))
    .filter((route) => route.count >= homepageCityMinimumJobs)
    .sort((left, right) => left.label.localeCompare(right.label, 'en-GB'));
}

function SearchPanel({ totalJobs }: { totalJobs: number }) {
  return (
    <section
      aria-labelledby="homepage-search-heading"
      className="rounded-2xl border border-white/70 bg-white p-5 shadow-2xl shadow-blue-950/20 sm:p-6"
    >
      <h2 id="homepage-search-heading" className="text-xl font-bold text-gray-950">
        Search by role or keyword
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
            placeholder="e.g. Administrator, Paralegal, Sales Advisor"
            className="w-full rounded-xl border border-gray-300 bg-white py-3 pl-11 pr-4 text-base text-gray-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
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
            placeholder="Town, city or region"
            className="w-full rounded-xl border border-gray-300 bg-white py-3 pl-11 pr-4 text-base text-gray-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <button
          type="submit"
          className="rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700"
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

function CompactRegionLinks({ regions }: { regions: RegionLink[] }) {
  return (
    <div className="mt-3 grid gap-1.5">
      {regions.map((region) => (
        <Link
          key={region.href}
          href={region.href}
          className="flex items-center justify-between rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm transition hover:border-blue-300 hover:bg-blue-50"
        >
          <span>
            <span className="font-semibold text-gray-900">{region.label}</span>
            <span className="ml-2 text-xs text-gray-500">{region.count}</span>
          </span>
          <span aria-hidden="true" className="text-blue-600">→</span>
        </Link>
      ))}
    </div>
  );
}

function RecentJobCard({ job }: { job: PublishedJob }) {
  const company = job.company || job.advertiser_name;

  return (
    <article className="h-full rounded-xl border border-gray-200 bg-white p-4 shadow-sm transition hover:-translate-y-0.5 hover:border-blue-300 hover:shadow-md">
      <Link href={getJobPath(job.job_id)} className="group flex h-full flex-col">
        <div className="mb-3 flex items-center justify-between gap-3">
          <span className="rounded-md bg-amber-100 px-2 py-1 text-xs font-bold text-amber-800">New</span>
          <span className="text-xs text-gray-500">View job →</span>
        </div>
        <h3 className="font-bold leading-snug text-gray-950 group-hover:text-blue-700">{job.title}</h3>
        <p className="mt-2 text-sm leading-snug text-gray-600">{company}</p>
        <p className="mt-1 text-sm text-gray-500">{job.location}</p>
        {job.salary_text ? (
          <p className="mt-auto pt-3 text-sm font-bold text-amber-700">{cleanSalary(job.salary_text)}</p>
        ) : null}
      </Link>
    </article>
  );
}

export default function Page() {
  const jobs = getPublishedJobs();
  const adminRegions = [
    ...withCounts(jobs, adminRegionRoutes),
    ...publishedDynamicAdminLinks(jobs),
    ...activeCityLinks('admin'),
  ];
  const customerSalesRegions = publishedDynamicCustomerSalesLinks(jobs);
  const legalRegions = publishedDynamicLegalLinks(jobs);
  const marketingRegions = publishedDynamicMarketingLinks(jobs);
  const hrRecruitmentRegions = publishedDynamicHrRecruitmentLinks(jobs);
  const supportWorkerRegions = [
    ...withCounts(jobs, supportWorkerRoutes),
    ...activeCityLinks('support'),
  ];
  const currentJobs = selectHomepageRecentJobs(jobs, 4);

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
        <section className="relative overflow-hidden bg-gradient-to-br from-blue-950 via-blue-800 to-blue-600 text-white">
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-0 opacity-20"
            style={{
              backgroundImage: 'radial-gradient(rgba(255,255,255,0.65) 1px, transparent 1px)',
              backgroundSize: '26px 26px',
              maskImage: 'linear-gradient(to bottom, black, transparent)',
            }}
          />
          <div className="relative mx-auto grid max-w-7xl gap-8 px-4 py-9 sm:px-6 sm:py-11 lg:grid-cols-[1.15fr_0.85fr] lg:items-center lg:px-8 lg:py-12">
            <div>
              <div className="inline-flex items-center gap-2 rounded-full border border-white/20 bg-white/10 px-3 py-1.5 text-sm font-semibold text-blue-50">
                <span className="h-2 w-2 rounded-full bg-emerald-400" />
                {jobs.length.toLocaleString('en-GB')} jobs live today
              </div>
              <h1 className="mt-5 max-w-3xl text-4xl font-black leading-[0.98] tracking-tight text-white sm:text-5xl lg:text-6xl">
                Find work that fits.
                <span className="mt-1 block text-blue-200">Apply direct.</span>
              </h1>
              <p className="mt-5 max-w-2xl text-base leading-7 text-blue-100 sm:text-lg">
                Curated UK jobs across admin, service and support roles — updated daily.
              </p>
              <div className="mt-4 flex flex-wrap gap-x-5 gap-y-2 text-sm font-semibold text-white">
                {['Apply direct', 'No signup', 'Updated daily'].map((promise) => (
                  <span key={promise} className="inline-flex items-center gap-2">
                    <span aria-hidden="true" className="grid h-5 w-5 place-items-center rounded-full border border-blue-300 text-xs">✓</span>
                    {promise}
                  </span>
                ))}
              </div>
            </div>

            <SearchPanel totalJobs={jobs.length} />
          </div>
        </section>

        <section className="border-b border-gray-200 bg-gray-50" aria-labelledby="recent-jobs-heading">
          <div className="mx-auto max-w-7xl px-4 py-5 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between gap-3">
              <h2 id="recent-jobs-heading" className="text-xl font-bold text-gray-950">
                Recently added
              </h2>
              <Link href="/jobs/search?q=&location=" className="text-sm font-semibold text-blue-700 hover:text-blue-900">
                View all jobs →
              </Link>
            </div>
            <div className="mt-3 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              {currentJobs.map((job) => (
                <RecentJobCard key={job.job_id} job={job} />
              ))}
            </div>
          </div>
        </section>

        <div className="mx-auto max-w-7xl px-4 py-5 sm:px-6 lg:px-8">
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
                  <p className="mt-0.5 text-sm text-gray-600">Current regional and city job pages</p>
                </div>
                {adminRegions.length > 0 ? <RegionGrid regions={adminRegions} /> : null}
              </div>

              <div className="grid content-start gap-3">
                {hrRecruitmentRegions.length > 0 ? (
                  <div id="hr-recruitment-regions" className="rounded-xl border border-blue-100 bg-blue-50 p-3.5 sm:p-4">
                    <h3 className="text-lg font-semibold text-gray-900">HR & Recruitment</h3>
                    <p className="mt-0.5 text-sm text-gray-600">Current live regional pages</p>
                    <CompactRegionLinks regions={hrRecruitmentRegions} />
                  </div>
                ) : null}

                {marketingRegions.length > 0 ? (
                  <div id="marketing-regions" className="rounded-xl border border-blue-100 bg-blue-50 p-3.5 sm:p-4">
                    <h3 className="text-lg font-semibold text-gray-900">Marketing</h3>
                    <p className="mt-0.5 text-sm text-gray-600">Current live regional pages</p>
                    <CompactRegionLinks regions={marketingRegions} />
                  </div>
                ) : null}

                {legalRegions.length > 0 ? (
                  <div id="legal-regions" className="rounded-xl border border-blue-100 bg-blue-50 p-3.5 sm:p-4">
                    <h3 className="text-lg font-semibold text-gray-900">Legal Assistant & Paralegal</h3>
                    <p className="mt-0.5 text-sm text-gray-600">Current live regional pages</p>
                    <CompactRegionLinks regions={legalRegions} />
                  </div>
                ) : null}

                {customerSalesRegions.length > 0 ? (
                  <div id="customer-sales-regions" className="rounded-xl border border-blue-100 bg-blue-50 p-3.5 sm:p-4">
                    <h3 className="text-lg font-semibold text-gray-900">Customer Sales & Sales Advisor</h3>
                    <p className="mt-0.5 text-sm text-gray-600">Current live regional pages</p>
                    <CompactRegionLinks regions={customerSalesRegions} />
                  </div>
                ) : null}

                <div id="support-worker-regions" className="rounded-xl border border-gray-200 bg-white p-3.5 sm:p-4">
                  <h3 className="text-lg font-semibold text-gray-900">Support worker jobs</h3>
                  <p className="mt-0.5 text-sm text-gray-600">Current regional and city supply</p>
                  <CompactRegionLinks regions={supportWorkerRegions} />
                </div>
              </div>
            </div>
          </section>

        </div>
      </main>
    </>
  );
}

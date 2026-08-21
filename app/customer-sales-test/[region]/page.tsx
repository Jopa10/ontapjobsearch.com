import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  CUSTOMER_SALES_TEST_SLICES,
  getCustomerSalesTestSlice,
} from "@/lib/customer-sales-test";

export const metadata: Metadata = {
  title: "Customer Sales Proof Test | Ontap Job Search",
  description: "Branch-only inspection page for the proposed Ontap Customer Sales / Sales Advisor family.",
  robots: { index: false, follow: false },
};

export function generateStaticParams() {
  return CUSTOMER_SALES_TEST_SLICES.map((slice) => ({ region: slice.slug }));
}

type PageProps = {
  params: Promise<{ region: string }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
};

function first(value: string | string[] | undefined) {
  return Array.isArray(value) ? value[0] || "" : value || "";
}

function cleanSalary(value?: string) {
  return (value || "").replaceAll("Â£", "£");
}

function text(value?: string) {
  return (value || "").trim();
}

function percent(value: number) {
  return `${Math.round(value * 100)}%`;
}

export default async function Page({ params, searchParams }: PageProps) {
  const { region } = await params;
  const slice = getCustomerSalesTestSlice(region);
  if (!slice) notFound();

  const query = first((await searchParams).q).trim().toLowerCase();
  const jobs = query
    ? slice.jobs.filter((job) =>
        [job.title, job.company, job.advertiser_name, job.location, job.description, job.full_description]
          .filter(Boolean)
          .join(" ")
          .toLowerCase()
          .includes(query)
      )
    : slice.jobs;

  return (
    <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
      <nav className="mb-5 text-sm text-gray-500" aria-label="Breadcrumb">
        <Link href="/customer-sales-test" className="hover:text-blue-700">
          Customer Sales proof test
        </Link>
        <span className="mx-2">/</span>
        <span className="text-gray-700">{slice.label}</span>
      </nav>

      <section className="rounded-2xl border border-amber-200 bg-amber-50 p-5 sm:p-6">
        <p className="text-xs font-bold uppercase tracking-wide text-amber-800">Governed proof slice · branch only · noindex</p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight text-gray-900">
          {slice.label} Customer Sales / Sales Advisor Jobs
        </h1>
        <p className="mt-3 max-w-4xl text-gray-700">
          Genuine selling, conversion, retention and renewal roles in office, contact-centre, home and hybrid settings.
          A job may also fit Service Admin; overlap is deliberately allowed. This page is for quality inspection only.
        </p>
      </section>

      <section className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4" aria-label="Proof slice QA summary">
        <div className="rounded-xl border border-gray-200 bg-white p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">Jobs</p>
          <p className="mt-1 text-2xl font-bold text-gray-900">{slice.jobs.length}</p>
        </div>
        <div className="rounded-xl border border-gray-200 bg-white p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">Employers</p>
          <p className="mt-1 text-2xl font-bold text-gray-900">{slice.stats.employerCount}</p>
        </div>
        <div className="rounded-xl border border-gray-200 bg-white p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">Duplicate groups</p>
          <p className="mt-1 text-2xl font-bold text-gray-900">{slice.stats.duplicateGroups.length}</p>
        </div>
        <div className="rounded-xl border border-gray-200 bg-white p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">Campaign employers</p>
          <p className="mt-1 text-2xl font-bold text-gray-900">{slice.stats.campaignEmployers.length}</p>
        </div>
      </section>

      <section className="mt-5 grid gap-4 lg:grid-cols-2">
        <div className="rounded-xl border border-gray-200 bg-white p-5">
          <h2 className="text-lg font-semibold text-gray-900">Employer concentration</h2>
          {slice.stats.topEmployers.length ? (
            <div className="mt-3 space-y-2">
              {slice.stats.topEmployers.slice(0, 8).map((employer) => (
                <div key={employer.name} className="flex items-center justify-between gap-3 text-sm">
                  <span className="min-w-0 truncate text-gray-700">{employer.name}</span>
                  <span className="shrink-0 font-semibold text-gray-900">
                    {employer.count} · {percent(employer.share)}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="mt-3 text-sm text-gray-500">No current jobs.</p>
          )}
          {slice.stats.dominantEmployer ? (
            <p className="mt-4 rounded-lg bg-amber-50 p-3 text-sm text-amber-900">
              Concentration flag: {slice.stats.dominantEmployer.name} supplies {percent(slice.stats.dominantEmployer.share)} of this slice.
            </p>
          ) : (
            <p className="mt-4 text-sm text-gray-500">No single employer supplies 40% or more of this slice.</p>
          )}
        </div>

        <div className="rounded-xl border border-gray-200 bg-white p-5">
          <h2 className="text-lg font-semibold text-gray-900">Classification / campaign checks</h2>
          <div className="mt-3 flex flex-wrap gap-2">
            {slice.stats.classificationCounts.map((item) => (
              <span key={item.classification} className="rounded-full border border-gray-200 bg-gray-50 px-3 py-1 text-xs font-semibold text-gray-700">
                {item.classification}: {item.count}
              </span>
            ))}
          </div>
          <div className="mt-4 text-sm text-gray-600">
            {slice.stats.campaignEmployers.length ? (
              <>
                <p className="font-semibold text-gray-900">Possible campaign concentration (3+ jobs):</p>
                <ul className="mt-2 list-disc space-y-1 pl-5">
                  {slice.stats.campaignEmployers.map((item) => (
                    <li key={item.name}>{item.name}: {item.count} jobs ({percent(item.share)})</li>
                  ))}
                </ul>
              </>
            ) : (
              <p>No employer currently has 3+ jobs in this proof slice.</p>
            )}
          </div>
          <div className="mt-4 text-sm text-gray-600">
            {slice.stats.duplicateGroups.length ? (
              <>
                <p className="font-semibold text-gray-900">Exact employer/title/location duplicate groups:</p>
                <ul className="mt-2 list-disc space-y-1 pl-5">
                  {slice.stats.duplicateGroups.map((group) => (
                    <li key={group.key}>{group.title} · {group.employer} · {group.location}: {group.count}</li>
                  ))}
                </ul>
              </>
            ) : (
              <p>No exact employer/title/location duplicate groups detected.</p>
            )}
          </div>
        </div>
      </section>

      <form method="get" className="mt-5 flex gap-2 rounded-xl border border-gray-200 bg-white p-3 shadow-sm">
        <label htmlFor="sales-test-search" className="sr-only">Search this test slice</label>
        <input
          id="sales-test-search"
          type="search"
          name="q"
          defaultValue={query}
          placeholder="Search title, employer, location or advert text"
          className="min-w-0 flex-1 rounded-lg border border-gray-300 px-4 py-2.5 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        />
        <button className="rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700">
          Search
        </button>
      </form>

      <div className="mt-4 flex flex-wrap gap-2 text-sm">
        {CUSTOMER_SALES_TEST_SLICES.map((item) => (
          <Link
            key={item.slug}
            href={`/customer-sales-test/${item.slug}`}
            className={`rounded-full border px-3 py-1.5 font-medium ${
              item.slug === slice.slug
                ? "border-blue-600 bg-blue-50 text-blue-800"
                : "border-gray-300 bg-white text-gray-700 hover:border-blue-300 hover:text-blue-700"
            }`}
          >
            {item.label}
          </Link>
        ))}
      </div>

      <section className="mt-7">
        <div className="mb-4 flex items-end justify-between gap-4">
          <div>
            <h2 className="text-2xl font-semibold text-gray-900">
              {jobs.length} visible job{jobs.length === 1 ? "" : "s"}
            </h2>
            {query ? <p className="mt-1 text-sm text-gray-500">Filtered by “{query}”</p> : null}
          </div>
          {query ? (
            <Link href={`/customer-sales-test/${slice.slug}`} className="text-sm font-semibold text-blue-700">
              Clear search
            </Link>
          ) : null}
        </div>

        {jobs.length ? (
          <div className="grid gap-4 md:grid-cols-2">
            {jobs.map((job) => {
              const company = text(job.company) || text(job.advertiser_name);
              const description = text(job.full_description) || text(job.description);
              return (
                <article key={job.job_id} className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
                  <h2 className="text-lg font-semibold leading-snug text-gray-900">{job.title}</h2>
                  <p className="mt-1 text-sm text-gray-600">
                    {[company, text(job.location)].filter(Boolean).join(" • ")}
                  </p>
                  {job.salary_text ? (
                    <p className="mt-2 text-sm font-semibold text-gray-900">{cleanSalary(job.salary_text)}</p>
                  ) : null}
                  {job.working_arrangement_text || job.working_arrangement ? (
                    <p className="mt-2 text-xs font-medium uppercase tracking-wide text-gray-500">
                      {job.working_arrangement_text || job.working_arrangement}
                    </p>
                  ) : null}
                  <div className="mt-3 flex flex-wrap gap-2 text-xs">
                    {job.customer_sales_classification ? (
                      <span className="rounded-full bg-blue-50 px-2.5 py-1 font-semibold text-blue-800">
                        {job.customer_sales_classification}
                      </span>
                    ) : null}
                    <span className="rounded-full bg-gray-100 px-2.5 py-1 font-medium text-gray-600">Service Admin overlap permitted</span>
                  </div>
                  {job.customer_sales_reason ? (
                    <p className="mt-3 text-xs leading-5 text-gray-500">Selector: {job.customer_sales_reason}</p>
                  ) : null}
                  {description ? (
                    <p className="mt-3 line-clamp-6 text-sm leading-6 text-gray-600">{description}</p>
                  ) : null}
                  <div className="mt-4 flex items-center justify-between gap-3 border-t border-gray-100 pt-4">
                    <span className="text-xs text-gray-400">{job.source || "JobG8"} · {job.job_id}</span>
                    <a
                      href={job.apply_url}
                      target="_blank"
                      rel="noreferrer"
                      className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700"
                    >
                      Apply / inspect advert →
                    </a>
                  </div>
                </article>
              );
            })}
          </div>
        ) : (
          <div className="rounded-xl border border-gray-200 bg-gray-50 p-8 text-center">
            <h2 className="text-xl font-semibold text-gray-900">No matching proof jobs</h2>
            <p className="mt-2 text-gray-600">
              This page is for inspecting the agreed Customer Sales family, not for setting final production thresholds.
            </p>
          </div>
        )}
      </section>

      <aside className="mt-8 rounded-xl border border-gray-200 bg-gray-50 p-4 text-sm text-gray-600">
        This page reads branch-only Customer Sales output generated from the current raw JobG8 feed. It does not
        publish a LIVE family, alter the production daily pipeline, add sitemap entries, change the recurring 33-region
        assessment, or change main.
      </aside>
    </main>
  );
}

import westYorkshireJobs from './west-yorkshire/support-worker.json';
import southYorkshireJobs from './south-yorkshire/support-worker.json';

type Job = {
  title?: string;
  company?: string;
  location?: string;
  salary_text?: string;
  apply_url?: string;
};

function cleanMojibakeCurrency(text: string) {
  return text.replaceAll('Â£', '£');
}

function formatSalaryText(text: string) {
  return cleanMojibakeCurrency(text).replace(/£(\d{4,})(?=\s|$)/g, (_, amount) => {
    return `£${Number(amount).toLocaleString('en-GB')}`;
  });
}

function MiniJobCard({ job, sliceUrl }: { job: Job; sliceUrl: string }) {
  return (
    <article className="rounded-lg border border-gray-200 bg-white p-2 leading-tight">
      <h3 className="mb-0.5 text-sm font-semibold leading-snug">{job.title}</h3>

      <p className="mb-1 text-xs leading-snug text-gray-600">
        {job.company} • {job.location}
      </p>

      {job.salary_text && (
        <p className="mb-1 text-xs font-semibold leading-snug">
          {formatSalaryText(job.salary_text)}
        </p>
      )}

      <a href={sliceUrl} className="text-xs font-medium text-blue-700 hover:text-blue-900">
        View role →
      </a>
    </article>
  );
}

const popularSearches = [
  {
    label: 'West Yorkshire support worker jobs',
    href: '/west-yorkshire/support-worker',
  },
  {
    label: 'South Yorkshire support worker jobs',
    href: '/south-yorkshire/support-worker',
  },
  {
    label: 'Browse all jobs',
    href: '/jobs/all',
  },
];

function RegionBlock({
  title,
  intro,
  ctaText,
  sliceUrl,
  jobs,
}: {
  title: string;
  intro: string;
  ctaText: string;
  sliceUrl: string;
  jobs: Job[];
}) {
  return (
    <section className="rounded-xl border border-gray-200 p-2.5 hover:border-blue-300 hover:bg-blue-50">
      <h2 className="mb-1 text-lg font-semibold leading-tight">{title}</h2>

      <p className="mb-2 text-sm leading-snug text-gray-600">{intro}</p>

      <a
        href={sliceUrl}
        className="inline-block rounded-lg bg-blue-600 px-3 py-1.5 text-sm font-medium text-white"
      >
        {ctaText}
      </a>

      <div className="mt-2 grid gap-1.5">
        {jobs.slice(0, 2).map((job) => (
          <MiniJobCard
            key={`${job.title}-${job.company}-${job.location}`}
            job={job}
            sliceUrl={sliceUrl}
          />
        ))}
      </div>
    </section>
  );
}

export default function Page() {
  return (
    <>
      <style>{`
        body:has(main[data-homepage]) footer {
          margin-top: 0.75rem;
        }

        body:has(main[data-homepage]) footer > div {
          padding-top: 0.75rem;
          padding-bottom: 0.75rem;
        }

        body:has(main[data-homepage]) footer > div > div:first-child {
          gap: 0.5rem;
        }

        body:has(main[data-homepage]) footer > div > div:first-child > div:first-child,
        body:has(main[data-homepage]) footer h4,
        body:has(main[data-homepage]) footer > div > div:last-child {
          display: none;
        }

        body:has(main[data-homepage]) footer ul {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem 1rem;
        }

        body:has(main[data-homepage]) footer ul > :not([hidden]) ~ :not([hidden]) {
          margin-top: 0;
        }

        @media (min-width: 768px) {
          body:has(main[data-homepage]) footer {
            margin-top: 1rem;
          }

          body:has(main[data-homepage]) footer > div {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
          }

          body:has(main[data-homepage]) footer > div > div:first-child {
            display: flex;
            justify-content: center;
          }
        }
      `}</style>

      <main data-homepage className="mx-auto max-w-6xl px-6 py-5">
        <h1 className="max-w-3xl text-4xl font-bold tracking-tight mb-2">
          Yorkshire Support Worker Jobs
        </h1>

        <p className="max-w-3xl text-lg text-gray-700 mb-2">
          Live support worker roles across West and South Yorkshire.
        </p>

        <p className="max-w-3xl text-sm text-gray-600 mb-2">
          Updated daily • Apply directly on employer websites • No signup required
        </p>
        <div className="mb-3 flex flex-wrap gap-1.5 text-sm">
          <span className="rounded-full bg-gray-100 px-3 py-1 text-gray-700">Updated daily</span>

          <span className="rounded-full bg-gray-100 px-3 py-1 text-gray-700">
            West & South Yorkshire roles
          </span>

          <span className="rounded-full bg-gray-100 px-3 py-1 text-gray-700">
            Direct employer applications
          </span>

          <span className="rounded-full bg-gray-100 px-3 py-1 text-gray-700">
            No signup required
          </span>
        </div>

        <div className="grid gap-3 md:grid-cols-2">
          <RegionBlock
            title="West Yorkshire Support Worker Jobs"
            intro="Current Leeds and West Yorkshire support worker roles, updated daily."
            ctaText="View West Yorkshire jobs →"
            sliceUrl="/west-yorkshire/support-worker"
            jobs={westYorkshireJobs}
          />

          <RegionBlock
            title="South Yorkshire Support Worker Jobs"
            intro="Current Sheffield and South Yorkshire support worker roles, updated daily."
            ctaText="View South Yorkshire jobs →"
            sliceUrl="/south-yorkshire/support-worker"
            jobs={southYorkshireJobs}
          />
        </div>

        <section className="mt-4 rounded-xl border border-gray-100 bg-gray-50 p-3">
          <h2 className="mb-2 text-base font-semibold text-gray-800">
            Popular support worker searches
          </h2>

          <div className="flex flex-wrap gap-2">
            {popularSearches.map((search) => (
              <a
                key={search.href}
                href={search.href}
                className="rounded-full border border-gray-200 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 hover:border-blue-200 hover:text-blue-700"
              >
                {search.label}
              </a>
            ))}
          </div>
        </section>
      </main>
    </>
  );
}

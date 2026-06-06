import westYorkshireSupportWorkerJobs from './west-yorkshire/support-worker.json';
import southYorkshireSupportWorkerJobs from './south-yorkshire/support-worker.json';
import westYorkshireServiceAdministratorJobs from './west-yorkshire/service-administrator-jobs.json';
import southYorkshireServiceAdministratorJobs from './south-yorkshire/service-administrator-jobs.json';
import northEastServiceAdministratorJobs from './north-east/service-administrator-jobs.json';

type Job = {
  title?: string;
  company?: string;
  location?: string;
  salary_text?: string;
  apply_url?: string;
};

type SliceCard = {
  title: string;
  intro: string;
  ctaText: string;
  sliceUrl: string;
  jobs: Job[];
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
    label: 'West Yorkshire service administrator jobs',
    href: '/west-yorkshire/service-administrator-jobs',
  },
  {
    label: 'South Yorkshire service administrator jobs',
    href: '/south-yorkshire/service-administrator-jobs',
  },
  {
    label: 'North East service administrator jobs',
    href: '/north-east/service-administrator-jobs',
  },
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
    href: '/browse-jobs',
  },
];

const supportWorkerSlices: SliceCard[] = [
  {
    title: 'West Yorkshire Support Worker Jobs',
    intro:
      'Paused / limited current supply while suitable support-worker roles are low in West Yorkshire.',
    ctaText: 'Check West Yorkshire page →',
    sliceUrl: '/west-yorkshire/support-worker',
    jobs: westYorkshireSupportWorkerJobs,
  },
  {
    title: 'South Yorkshire Support Worker Jobs',
    intro:
      'Paused / limited current supply while suitable support-worker roles are low in South Yorkshire.',
    ctaText: 'Check South Yorkshire page →',
    sliceUrl: '/south-yorkshire/support-worker',
    jobs: southYorkshireSupportWorkerJobs,
  },
];

const serviceAdministratorSlices: SliceCard[] = [
  {
    title: 'West Yorkshire Service Administrator Jobs',
    intro:
      'Current service administrator, customer service administrator and office support roles across West Yorkshire.',
    ctaText: 'View West Yorkshire jobs →',
    sliceUrl: '/west-yorkshire/service-administrator-jobs',
    jobs: westYorkshireServiceAdministratorJobs,
  },
  {
    title: 'South Yorkshire Service Administrator Jobs',
    intro:
      'Current service administrator, customer service administrator and office support roles across South Yorkshire.',
    ctaText: 'View South Yorkshire jobs →',
    sliceUrl: '/south-yorkshire/service-administrator-jobs',
    jobs: southYorkshireServiceAdministratorJobs,
  },
  {
    title: 'North East Service Administrator Jobs',
    intro:
      'Current service administrator, customer service administrator and office support roles across Newcastle and the North East.',
    ctaText: 'View North East jobs →',
    sliceUrl: '/north-east/service-administrator-jobs',
    jobs: northEastServiceAdministratorJobs,
  },
];

const futureSupportWorkerRegions = ['Lancashire', 'Greater Manchester', 'Cumbria', 'North East'];

function SliceCardGrid({ cards }: { cards: SliceCard[] }) {
  return (
    <div className="grid gap-3 md:grid-cols-2">
      {cards.map((card) => (
        <section
          key={card.sliceUrl}
          className="rounded-xl border border-gray-200 p-2.5 hover:border-blue-300 hover:bg-blue-50"
        >
          <h3 className="mb-1 text-lg font-semibold leading-tight">{card.title}</h3>

          <p className="mb-2 text-sm leading-snug text-gray-600">{card.intro}</p>

          <a
            href={card.sliceUrl}
            className="inline-block rounded-lg bg-blue-600 px-3 py-1.5 text-sm font-medium text-white"
          >
            {card.ctaText}
          </a>

          <div className="mt-2 grid gap-1.5">
            {card.jobs.slice(0, 1).map((job) => (
              <MiniJobCard
                key={`${card.sliceUrl}-${job.title}-${job.company}-${job.location}`}
                job={job}
                sliceUrl={card.sliceUrl}
              />
            ))}
          </div>
        </section>
      ))}
    </div>
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
        <h1 className="mb-2 max-w-3xl text-4xl font-bold tracking-tight">
          Admin, office support and customer-service jobs
        </h1>

        <p className="mb-2 max-w-3xl text-lg text-gray-700">
          Current service administrator, office support and customer-service roles across Yorkshire and the North East. Updated daily; apply directly on employer sites.
        </p>

        <section className="mb-4">
          <h2 className="mb-2 text-2xl font-semibold tracking-tight">
            Active service administrator jobs
          </h2>
          <SliceCardGrid cards={serviceAdministratorSlices} />
        </section>

        <section>
          <h2 className="mb-2 text-2xl font-semibold tracking-tight">
            Support worker jobs — paused / limited current supply
          </h2>
          <SliceCardGrid cards={supportWorkerSlices} />

          <p className="mt-2 text-xs text-gray-500">
            Support-worker pages are still available, but current supply is limited. Next regions
            planned: {futureSupportWorkerRegions.join(', ')}.
          </p>
        </section>

        <section className="mt-4 rounded-xl border border-gray-100 bg-gray-50 p-3">
          <h2 className="mb-2 text-base font-semibold text-gray-800">Popular job searches</h2>

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

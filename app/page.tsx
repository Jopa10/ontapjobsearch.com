import westYorkshireSupportWorkerJobs from './west-yorkshire/support-worker.json';
import southYorkshireSupportWorkerJobs from './south-yorkshire/support-worker.json';
import northEastSupportWorkerJobs from './north-east/support-worker-jobs.json';
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

type RegionLink = {
  label: string;
  href: string;
  status?: 'active' | 'limited';
  count?: number;
};

type RoleFamilyCard = {
  eyebrow: string;
  title: string;
  description: string;
  browseHref: string;
  browseText: string;
  regionLinks: RegionLink[];
  featuredJobs: Job[];
  featuredHref: string;
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
    <article className="rounded-lg border border-gray-200 bg-white p-3 leading-tight">
      <h3 className="mb-1 text-sm font-semibold leading-snug text-gray-900">{job.title}</h3>

      <p className="mb-1 text-xs leading-snug text-gray-600">
        {job.company} • {job.location}
      </p>

      {job.salary_text && (
        <p className="mb-1.5 text-xs font-semibold leading-snug text-gray-900">
          {formatSalaryText(job.salary_text)}
        </p>
      )}

      <a href={sliceUrl} className="text-xs font-medium text-blue-700 hover:text-blue-900">
        View job page →
      </a>
    </article>
  );
}

const adminRegionLinks: RegionLink[] = [
  {
    label: 'West Yorkshire',
    href: '/west-yorkshire/service-administrator-jobs',
    status: 'active',
    count: westYorkshireServiceAdministratorJobs.length,
  },
  {
    label: 'South Yorkshire',
    href: '/south-yorkshire/service-administrator-jobs',
    status: 'active',
    count: southYorkshireServiceAdministratorJobs.length,
  },
  {
    label: 'North East',
    href: '/north-east/service-administrator-jobs',
    status: 'active',
    count: northEastServiceAdministratorJobs.length,
  },
];

const supportRegionLinks: RegionLink[] = [
  {
    label: 'North East',
    href: '/north-east/support-worker',
    status: 'active',
    count: northEastSupportWorkerJobs.length,
  },
  {
    label: 'West Yorkshire',
    href: '/west-yorkshire/support-worker',
    status: 'limited',
    count: westYorkshireSupportWorkerJobs.length,
  },
  {
    label: 'South Yorkshire',
    href: '/south-yorkshire/support-worker',
    status: 'limited',
    count: southYorkshireSupportWorkerJobs.length,
  },
];

const roleFamilies: RoleFamilyCard[] = [
  {
    eyebrow: 'Most active',
    title: 'Admin, office support & customer service',
    description:
      'Service administrator, customer service administrator and office support pages grouped by region.',
    browseHref: '/browse-jobs#admin-office-support-customer-service',
    browseText: 'View all admin regions',
    regionLinks: adminRegionLinks,
    featuredJobs: westYorkshireServiceAdministratorJobs.slice(0, 1),
    featuredHref: '/west-yorkshire/service-administrator-jobs',
  },
  {
    eyebrow: 'Growing directory',
    title: 'Support worker & care roles',
    description:
      'Support worker and care-role pages retained as the directory expands, with limited pages clearly marked.',
    browseHref: '/browse-jobs#support-worker-care-roles',
    browseText: 'View all support worker regions',
    regionLinks: supportRegionLinks,
    featuredJobs: northEastSupportWorkerJobs.slice(0, 1),
    featuredHref: '/north-east/support-worker',
  },
];

const recentlyAddedJobs = [
  ...westYorkshireServiceAdministratorJobs.slice(0, 1),
  ...southYorkshireServiceAdministratorJobs.slice(0, 1),
  ...northEastServiceAdministratorJobs.slice(0, 1),
];

function StatusPill({ status }: { status?: RegionLink['status'] }) {
  if (status === 'limited') {
    return (
      <span className="rounded-full border border-amber-200 bg-amber-50 px-2 py-0.5 text-[11px] font-semibold text-amber-700">
        Limited
      </span>
    );
  }

  return (
    <span className="rounded-full border border-green-200 bg-green-50 px-2 py-0.5 text-[11px] font-semibold text-green-700">
      Active
    </span>
  );
}

function RoleFamilyCard({ family }: { family: RoleFamilyCard }) {
  return (
    <section className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm transition hover:border-blue-300 hover:shadow-md">
      <div className="mb-4 flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-blue-700">
            {family.eyebrow}
          </p>
          <h2 className="text-2xl font-bold tracking-tight text-gray-900">{family.title}</h2>
        </div>
        <a
          href={family.browseHref}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          {family.browseText} →
        </a>
      </div>

      <p className="mb-4 text-sm leading-6 text-gray-600">{family.description}</p>

      <div className="grid gap-2">
        {family.regionLinks.map((region) => (
          <a
            key={region.href}
            href={region.href}
            className="flex items-center justify-between gap-3 rounded-xl border border-gray-200 bg-gray-50 px-3 py-2 text-sm font-medium text-gray-800 hover:border-blue-200 hover:bg-blue-50"
          >
            <span>{region.label}</span>
            <span className="flex items-center gap-2 text-xs text-gray-500">
              {typeof region.count === 'number' ? `${region.count} jobs` : null}
              <StatusPill status={region.status} />
            </span>
          </a>
        ))}
      </div>

      {family.featuredJobs.length > 0 ? (
        <div className="mt-4 border-t border-gray-100 pt-4">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-gray-500">
            Featured current job
          </p>
          {family.featuredJobs.map((job) => (
            <MiniJobCard
              key={`${family.featuredHref}-${job.title}-${job.company}-${job.location}`}
              job={job}
              sliceUrl={family.featuredHref}
            />
          ))}
        </div>
      ) : null}
    </section>
  );
}

export default function Page() {
  return (
    <main data-homepage className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
      <section className="mb-8 rounded-2xl border border-gray-200 bg-gray-50 px-5 py-8 sm:px-8">
        <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-blue-700">
          Ontap Job Search
        </p>
        <h1 className="mb-3 max-w-3xl text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
          Curated jobs by role and region
        </h1>
        <p className="max-w-2xl text-lg leading-8 text-gray-700">
          Current jobs, checked daily. No signup required.
        </p>
        <div className="mt-5 flex flex-wrap gap-3">
          <a
            href="/browse-jobs"
            className="rounded-lg bg-blue-600 px-5 py-2.5 text-base font-medium text-white hover:bg-blue-700"
          >
            Browse jobs by role →
          </a>
          <a
            href="/west-yorkshire/service-administrator-jobs"
            className="rounded-lg border border-gray-300 bg-white px-5 py-2.5 text-base font-medium text-gray-800 hover:border-blue-300 hover:text-blue-700"
          >
            View active admin jobs
          </a>
        </div>
      </section>

      <section aria-label="Browse role families" className="grid gap-5 lg:grid-cols-2">
        {roleFamilies.map((family) => (
          <RoleFamilyCard key={family.title} family={family} />
        ))}
      </section>

      <section className="mt-8 grid gap-5 lg:grid-cols-[1.5fr_1fr]">
        <div className="rounded-xl border border-gray-200 bg-white p-4">
          <div className="mb-3 flex items-center justify-between gap-3">
            <h2 className="text-lg font-semibold tracking-tight text-gray-900">Recently added</h2>
            <a href="/browse-jobs" className="text-sm font-medium text-blue-700 hover:text-blue-900">
              Browse directory →
            </a>
          </div>
          <div className="grid gap-2 md:grid-cols-3">
            {recentlyAddedJobs.map((job) => (
              <MiniJobCard
                key={`recent-${job.title}-${job.company}-${job.location}`}
                job={job}
                sliceUrl="/browse-jobs#admin-office-support-customer-service"
              />
            ))}
          </div>
        </div>

        <aside className="rounded-xl border border-gray-100 bg-gray-50 p-4">
          <h2 className="mb-2 text-base font-semibold text-gray-800">How Ontap works</h2>
          <ul className="space-y-2 text-sm leading-6 text-gray-600">
            <li>• Pages focus on specific role families in specific regions.</li>
            <li>• Job lists are checked daily and link to employer application pages.</li>
            <li>• Limited pages stay visible but lower priority until supply improves.</li>
          </ul>
        </aside>
      </section>
    </main>
  );
}

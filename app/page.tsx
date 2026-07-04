import westYorkshireSupportWorkerJobs from './west-yorkshire/support-worker.json';
import southYorkshireSupportWorkerJobs from './south-yorkshire/support-worker.json';
import northEastSupportWorkerJobs from './north-east/support-worker-jobs.json';
import westYorkshireServiceAdministratorJobs from './west-yorkshire/service-administrator-jobs.json';
import southYorkshireServiceAdministratorJobs from './south-yorkshire/service-administrator-jobs.json';
import northEastServiceAdministratorJobs from './north-east/service-administrator-jobs.json';

type RegionLink = {
  label: string;
  href: string;
  count: number;
};

type RoleFamily = {
  title: string;
  intro: string;
  browseHref: string;
  browseText: string;
  regions: RegionLink[];
};

const roleFamilies: RoleFamily[] = [
  {
    title: 'Admin, office support & customer service',
    intro: 'Service administrator, customer service and office support jobs grouped by region.',
    browseHref: '/browse-jobs#admin-office-support-customer-service',
    browseText: 'Browse admin regions',
    regions: [
      {
        label: 'West Yorkshire',
        href: '/west-yorkshire/service-administrator-jobs',
        count: westYorkshireServiceAdministratorJobs.length,
      },
      {
        label: 'South Yorkshire',
        href: '/south-yorkshire/service-administrator-jobs',
        count: southYorkshireServiceAdministratorJobs.length,
      },
      {
        label: 'North East',
        href: '/north-east/service-administrator-jobs',
        count: northEastServiceAdministratorJobs.length,
      },
    ],
  },
  {
    title: 'Support worker & care roles',
    intro: 'Support worker and care-role pages grouped by region.',
    browseHref: '/browse-jobs#support-worker-care-roles',
    browseText: 'Browse support worker regions',
    regions: [
      {
        label: 'West Yorkshire',
        href: '/west-yorkshire/support-worker',
        count: westYorkshireSupportWorkerJobs.length,
      },
      {
        label: 'South Yorkshire',
        href: '/south-yorkshire/support-worker',
        count: southYorkshireSupportWorkerJobs.length,
      },
      {
        label: 'North East',
        href: '/north-east/support-worker',
        count: northEastSupportWorkerJobs.length,
      },
    ],
  },
];

function RegionRow({ region }: { region: RegionLink }) {
  return (
    <a
      href={region.href}
      className="flex items-center justify-between gap-3 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-800 hover:border-blue-300 hover:bg-blue-50 hover:text-blue-700"
    >
      <span>{region.label}</span>
      <span className="text-xs font-normal text-gray-500">{region.count} jobs</span>
    </a>
  );
}

function RoleFamilySection({ family }: { family: RoleFamily }) {
  return (
    <section className="rounded-xl border border-gray-200 bg-gray-50 p-3">
      <div className="mb-2 flex flex-wrap items-end justify-between gap-2">
        <div>
          <h2 className="text-lg font-semibold tracking-tight text-gray-900">{family.title}</h2>
          <p className="mt-0.5 text-sm leading-5 text-gray-600">{family.intro}</p>
        </div>
        <a href={family.browseHref} className="text-sm font-medium text-blue-700 hover:text-blue-900">
          {family.browseText} →
        </a>
      </div>

      <div className="grid gap-1.5 md:grid-cols-3">
        {family.regions.map((region) => (
          <RegionRow key={region.href} region={region} />
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
        <header className="mb-4">
          <h1 className="mb-1 max-w-3xl text-3xl font-bold tracking-tight sm:text-4xl">
            Curated jobs by role and region
          </h1>
          <p className="max-w-3xl text-base text-gray-700">
            Current jobs, checked daily. No signup required.
          </p>
        </header>

        <div className="grid gap-3">
          {roleFamilies.map((family) => (
            <RoleFamilySection key={family.title} family={family} />
          ))}
        </div>

        <p className="mt-4 rounded-lg border border-gray-100 bg-gray-50 px-3 py-2 text-sm text-gray-600">
          Choose a role family, pick a region, then apply directly on employer sites. For the full
          directory, visit{' '}
          <a href="/browse-jobs" className="font-medium text-blue-700 hover:text-blue-900">
            Browse Jobs
          </a>
          .
        </p>
      </main>
    </>
  );
}

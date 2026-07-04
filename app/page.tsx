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

type RoleFamilyCard = {
  title: string;
  description: string;
  browseHref: string;
  browseText: string;
  regionLinks: RegionLink[];
};

const adminRegionLinks: RegionLink[] = [
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
];

const supportRegionLinks: RegionLink[] = [
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
];

const roleFamilies: RoleFamilyCard[] = [
  {
    title: 'Admin, office support & customer service',
    description: 'Service administrator, customer service and office support jobs by region.',
    browseHref: '/browse-jobs#admin-office-support-customer-service',
    browseText: 'View all admin regions',
    regionLinks: adminRegionLinks,
  },
  {
    title: 'Support worker & care roles',
    description: 'Support worker and care roles by region, checked with the rest of the directory.',
    browseHref: '/browse-jobs#support-worker-care-roles',
    browseText: 'View all support worker regions',
    regionLinks: supportRegionLinks,
  },
];

function RoleFamilyCard({ family }: { family: RoleFamilyCard }) {
  return (
    <section className="rounded-xl border border-gray-200 bg-white p-3 shadow-sm transition hover:border-blue-300">
      <div className="mb-2 flex flex-wrap items-start justify-between gap-2">
        <div className="min-w-0">
          <h2 className="text-lg font-bold tracking-tight text-gray-900">{family.title}</h2>
          <p className="mt-0.5 text-sm leading-5 text-gray-600">{family.description}</p>
        </div>
        <a
          href={family.browseHref}
          className="shrink-0 text-sm font-medium text-blue-700 hover:text-blue-900"
        >
          {family.browseText} →
        </a>
      </div>

      <div className="grid gap-1.5">
        {family.regionLinks.map((region) => (
          <a
            key={region.href}
            href={region.href}
            className="flex items-center justify-between rounded-lg border border-gray-200 bg-gray-50 px-3 py-2 text-sm font-medium text-gray-800 hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700"
          >
            <span>{region.label}</span>
            <span className="text-xs font-normal text-gray-500">{region.count} jobs</span>
          </a>
        ))}
      </div>
    </section>
  );
}

export default function Page() {
  return (
    <main data-homepage className="mx-auto max-w-6xl px-4 py-5 sm:px-6 lg:px-8">
      <header className="mb-4">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
          Curated jobs by role and region
        </h1>
        <p className="mt-1 text-base leading-6 text-gray-700">
          Current jobs, checked daily. No signup required.
        </p>
      </header>

      <section aria-label="Browse role families" className="grid gap-3">
        {roleFamilies.map((family) => (
          <RoleFamilyCard key={family.title} family={family} />
        ))}
      </section>

      <section className="mt-4 rounded-lg border border-gray-100 bg-gray-50 px-4 py-3 text-sm leading-6 text-gray-600">
        <span className="font-semibold text-gray-800">How Ontap works:</span> choose a role family,
        pick a region, then apply directly on employer sites.
      </section>
    </main>
  );
}

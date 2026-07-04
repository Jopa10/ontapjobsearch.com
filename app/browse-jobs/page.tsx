import westYorkshireSupportWorkerJobs from '../west-yorkshire/support-worker.json';
import southYorkshireSupportWorkerJobs from '../south-yorkshire/support-worker.json';
import northEastSupportWorkerJobs from '../north-east/support-worker-jobs.json';
import westYorkshireServiceAdministratorJobs from '../west-yorkshire/service-administrator-jobs.json';
import southYorkshireServiceAdministratorJobs from '../south-yorkshire/service-administrator-jobs.json';
import northEastServiceAdministratorJobs from '../north-east/service-administrator-jobs.json';

type DirectoryPage = {
  region: string;
  href: string;
  count: number;
  status: 'active' | 'limited';
};

type RoleFamily = {
  id: string;
  title: string;
  summary: string;
  activePages: DirectoryPage[];
  limitedPages: DirectoryPage[];
};

const roleFamilies: RoleFamily[] = [
  {
    id: 'admin-office-support-customer-service',
    title: 'Admin, office support & customer service',
    summary:
      'Service administrator, customer service administrator and office support pages with the strongest current supply.',
    activePages: [
      {
        region: 'West Yorkshire',
        href: '/west-yorkshire/service-administrator-jobs',
        count: westYorkshireServiceAdministratorJobs.length,
        status: 'active',
      },
      {
        region: 'South Yorkshire',
        href: '/south-yorkshire/service-administrator-jobs',
        count: southYorkshireServiceAdministratorJobs.length,
        status: 'active',
      },
      {
        region: 'North East',
        href: '/north-east/service-administrator-jobs',
        count: northEastServiceAdministratorJobs.length,
        status: 'active',
      },
    ],
    limitedPages: [],
  },
  {
    id: 'support-worker-care-roles',
    title: 'Support worker & care roles',
    summary:
      'Support worker pages grouped separately so live regions can grow without changing the directory structure.',
    activePages: [
      {
        region: 'North East',
        href: '/north-east/support-worker',
        count: northEastSupportWorkerJobs.length,
        status: 'active',
      },
    ],
    limitedPages: [
      {
        region: 'West Yorkshire',
        href: '/west-yorkshire/support-worker',
        count: westYorkshireSupportWorkerJobs.length,
        status: 'limited',
      },
      {
        region: 'South Yorkshire',
        href: '/south-yorkshire/support-worker',
        count: southYorkshireSupportWorkerJobs.length,
        status: 'limited',
      },
    ],
  },
];

function StatusPill({ status }: { status: DirectoryPage['status'] }) {
  if (status === 'limited') {
    return (
      <span className="rounded-full border border-amber-200 bg-amber-50 px-2 py-0.5 text-[11px] font-semibold text-amber-700">
        Limited current availability
      </span>
    );
  }

  return (
    <span className="rounded-full border border-green-200 bg-green-50 px-2 py-0.5 text-[11px] font-semibold text-green-700">
      Active
    </span>
  );
}

function DirectoryRow({ page, muted = false }: { page: DirectoryPage; muted?: boolean }) {
  return (
    <a
      href={page.href}
      className={`flex flex-col gap-2 rounded-xl border px-4 py-3 transition sm:flex-row sm:items-center sm:justify-between ${
        muted
          ? 'border-gray-200 bg-gray-50 text-gray-700 hover:border-amber-200 hover:bg-amber-50'
          : 'border-gray-200 bg-white text-gray-900 shadow-sm hover:border-blue-300 hover:bg-blue-50'
      }`}
    >
      <div>
        <h3 className="text-base font-semibold leading-tight">{page.region}</h3>
        <p className="mt-1 text-sm text-gray-600">{page.count} current jobs • View region page</p>
      </div>
      <div className="flex items-center gap-2">
        <StatusPill status={page.status} />
        <span className="text-sm font-medium text-blue-700">Open →</span>
      </div>
    </a>
  );
}

function RoleFamilySection({ family }: { family: RoleFamily }) {
  return (
    <section id={family.id} className="scroll-mt-20 rounded-2xl border border-gray-200 bg-gray-50 p-4 sm:p-5">
      <div className="mb-4">
        <h2 className="text-2xl font-bold tracking-tight text-gray-900">{family.title}</h2>
        <p className="mt-1 max-w-3xl text-sm leading-6 text-gray-600">{family.summary}</p>
      </div>

      <div className="grid gap-2">
        {family.activePages.map((page) => (
          <DirectoryRow key={page.href} page={page} />
        ))}
      </div>

      {family.limitedPages.length > 0 ? (
        <div className="mt-5 border-t border-gray-200 pt-4">
          <h3 className="mb-2 text-sm font-semibold uppercase tracking-wide text-gray-500">
            Limited current availability
          </h3>
          <div className="grid gap-2">
            {family.limitedPages.map((page) => (
              <DirectoryRow key={page.href} page={page} muted />
            ))}
          </div>
        </div>
      ) : null}
    </section>
  );
}

export default function Page() {
  return (
    <main className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="mb-8">
        <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-blue-700">
          Browse jobs
        </p>
        <h1 className="mb-3 text-4xl font-bold tracking-tight text-gray-900">
          Jobs by role family and region
        </h1>
        <p className="max-w-3xl text-base leading-7 text-gray-600">
          A scalable directory for Ontap region pages. Active pages are listed first inside each role
          family, with lower-priority pages kept available under limited current availability.
        </p>
      </div>

      <nav aria-label="Role families" className="mb-6 flex flex-wrap gap-2">
        {roleFamilies.map((family) => (
          <a
            key={family.id}
            href={`#${family.id}`}
            className="rounded-full border border-gray-200 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 hover:border-blue-200 hover:text-blue-700"
          >
            {family.title}
          </a>
        ))}
      </nav>

      <div className="grid gap-6">
        {roleFamilies.map((family) => (
          <RoleFamilySection key={family.id} family={family} />
        ))}
      </div>
    </main>
  );
}

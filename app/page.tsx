type RegionLink = {
  label: string;
  href: string;
};

type RoleFamily = {
  title: string;
  description: string;
  cta: string;
  ctaHref: string;
  viewAllHref: string;
  icon: string;
  regions: RegionLink[];
};

const roleFamilies: RoleFamily[] = [
  {
    title: 'Admin, office support & customer service',
    description: 'Administrator, office-support and customer-service roles across the UK.',
    cta: 'Browse admin jobs',
    ctaHref: '/west-yorkshire/service-administrator-jobs',
    viewAllHref: '/browse-jobs',
    icon: 'A',
    regions: [
      { label: 'West Yorkshire', href: '/west-yorkshire/service-administrator-jobs' },
      { label: 'South Yorkshire', href: '/south-yorkshire/service-administrator-jobs' },
      { label: 'North East', href: '/north-east/service-administrator-jobs' },
      { label: 'Surrey', href: '/browse-jobs' },
    ],
  },
  {
    title: 'Support worker & care roles',
    description: 'Support-worker, residential-care and community-support roles across the UK.',
    cta: 'Browse support worker jobs',
    ctaHref: '/north-east/support-worker',
    viewAllHref: '/browse-jobs',
    icon: 'S',
    regions: [
      { label: 'North East', href: '/north-east/support-worker' },
      { label: 'Sussex', href: '/browse-jobs' },
      { label: 'Hampshire', href: '/browse-jobs' },
      { label: 'Cumbria', href: '/cumbria/support-worker' },
    ],
  },
];

const howOntapWorks = [
  {
    icon: '⌕',
    title: 'We find live job pages',
  },
  {
    icon: '✓',
    title: 'We check them daily',
  },
  {
    icon: '↗',
    title: 'We organise them by role and region',
  },
];

function RoleFamilyCard({ family }: { family: RoleFamily }) {
  return (
    <section className="rounded-2xl border border-[#dbe3ee] bg-white p-5 shadow-sm transition hover:border-blue-200 hover:shadow-md">
      <div className="flex gap-4">
        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-blue-100 bg-blue-50 text-sm font-extrabold text-blue-700">
          {family.icon}
        </div>

        <div className="min-w-0 flex-1">
          <h2 className="text-lg font-extrabold leading-tight text-gray-900">{family.title}</h2>
          <p className="mt-1 text-sm leading-6 text-gray-600">{family.description}</p>

          <a
            href={family.ctaHref}
            className="mt-4 inline-flex rounded-lg bg-blue-600 px-4 py-2 text-sm font-bold text-white shadow-sm transition hover:bg-blue-700"
          >
            {family.cta}
          </a>
        </div>
      </div>

      <div className="my-4 border-t border-gray-100" />

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="min-w-0">
          <div className="mb-2 text-xs font-bold uppercase tracking-wide text-gray-500">
            Popular regions
          </div>
          <div className="flex flex-wrap gap-2">
            {family.regions.map((region) => (
              <a
                key={`${family.title}-${region.href}-${region.label}`}
                href={region.href}
                className="rounded-full border border-gray-200 bg-gray-50 px-3 py-1 text-xs font-semibold text-gray-700 transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700"
              >
                {region.label}
              </a>
            ))}
          </div>
        </div>

        <a
          href={family.viewAllHref}
          className="shrink-0 text-sm font-bold text-blue-700 transition hover:text-blue-900"
        >
          View all →
        </a>
      </div>
    </section>
  );
}

export default function Page() {
  return (
    <main data-homepage className="mx-auto w-full max-w-[1180px] px-4 py-8 sm:px-6 lg:px-8">
      <section className="rounded-2xl border border-[#dbe3ee] bg-gradient-to-br from-white via-white to-blue-50/50 p-5 shadow-sm sm:p-6">
        <div className="max-w-3xl">
          <p className="mb-2 text-xs font-bold uppercase tracking-[0.18em] text-blue-700">
            Ontap Job Search
          </p>
          <h1 className="text-3xl font-extrabold leading-tight tracking-tight text-gray-900 sm:text-4xl">
            Curated jobs by role and region
          </h1>
          <p className="mt-2 text-base leading-7 text-gray-600">
            Current jobs, checked daily. No signup required.
          </p>
        </div>
      </section>

      <div className="mt-4 grid gap-4 lg:grid-cols-2">
        {roleFamilies.map((family) => (
          <RoleFamilyCard key={family.title} family={family} />
        ))}
      </div>

      <section className="mt-4 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
        <div className="grid gap-3 md:grid-cols-3">
          {howOntapWorks.map((step) => (
            <div key={step.title} className="flex items-center gap-3 rounded-xl bg-gray-50 px-3 py-3">
              <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-white text-sm font-extrabold text-blue-700 shadow-sm">
                {step.icon}
              </span>
              <span className="text-sm font-bold text-gray-800">{step.title}</span>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}

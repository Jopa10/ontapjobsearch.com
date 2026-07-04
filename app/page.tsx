type RegionChip = {
  label: string;
  href: string;
};

type RoleFamilyCard = {
  tone: 'blue' | 'green';
  heading: string;
  description: string;
  ctaText: string;
  ctaHref: string;
  regions: RegionChip[];
  viewAllHref: string;
};

type RecentJobCard = {
  title: string;
  company: string;
  region: string;
  type: string;
  href: string;
};

const roleFamilies: RoleFamilyCard[] = [
  {
    tone: 'blue',
    heading: 'Admin, office & customer service',
    description: 'Administrator, office and customer-service roles across the UK.',
    ctaText: 'Browse admin jobs',
    ctaHref: '/west-yorkshire/service-administrator-jobs',
    viewAllHref: '/browse-jobs',
    regions: [
      { label: 'West Yorkshire', href: '/west-yorkshire/service-administrator-jobs' },
      { label: 'South Yorkshire', href: '/south-yorkshire/service-administrator-jobs' },
      { label: 'North East', href: '/north-east/service-administrator-jobs' },
      { label: 'Surrey', href: '/browse-jobs' },
    ],
  },
  {
    tone: 'green',
    heading: 'Support worker & care roles',
    description: 'Support-worker, residential-care and community-support roles across the UK.',
    ctaText: 'Browse support worker jobs',
    ctaHref: '/north-east/support-worker',
    viewAllHref: '/browse-jobs',
    regions: [
      { label: 'North East', href: '/north-east/support-worker' },
      { label: 'Sussex', href: '/browse-jobs' },
      { label: 'Hampshire', href: '/browse-jobs' },
      { label: 'Cumbria', href: '/browse-jobs' },
    ],
  },
];

const recentJobs: RecentJobCard[] = [
  {
    title: 'Administrator',
    company: 'Bright Futures Ltd',
    region: 'Surrey',
    type: 'Full-time',
    href: '/west-yorkshire/service-administrator-jobs',
  },
  {
    title: 'Support Worker',
    company: 'Care Together',
    region: 'Hampshire',
    type: 'Part-time',
    href: '/north-east/support-worker',
  },
  {
    title: 'Customer Service Advisor',
    company: 'Connect Services',
    region: 'West Yorkshire',
    type: 'Full-time',
    href: '/west-yorkshire/service-administrator-jobs',
  },
];

function AdminIcon() {
  return (
    <svg aria-hidden="true" className="h-12 w-12" viewBox="0 0 48 48" fill="none">
      <path
        d="M10 35h28M16 35v-5h16v5M12 13h24v17H12V13Z"
        stroke="currentColor"
        strokeWidth="2.4"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M19 24c1.4-2 3-3 5-3s3.6 1 5 3"
        stroke="currentColor"
        strokeWidth="2.4"
        strokeLinecap="round"
      />
      <circle cx="24" cy="18" r="3" stroke="currentColor" strokeWidth="2.4" />
    </svg>
  );
}

function SupportIcon() {
  return (
    <svg aria-hidden="true" className="h-12 w-12" viewBox="0 0 48 48" fill="none">
      <path
        d="M16 25c-3-3-3.5-7.5-.7-10.2 2.6-2.5 6.4-1.7 8.7 1.2 2.3-2.9 6.1-3.7 8.7-1.2 2.8 2.7 2.3 7.2-.7 10.2L24 33l-8-8Z"
        stroke="currentColor"
        strokeWidth="2.4"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M11 28v7l9 5M37 28v7l-9 5"
        stroke="currentColor"
        strokeWidth="2.4"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function ArrowIcon() {
  return (
    <svg aria-hidden="true" className="h-4 w-4" viewBox="0 0 16 16" fill="none">
      <path
        d="M6 3.5 10.5 8 6 12.5"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function RoleCard({ card }: { card: RoleFamilyCard }) {
  const isGreen = card.tone === 'green';
  const cardClass = isGreen
    ? 'border-emerald-100 bg-gradient-to-br from-emerald-50/80 via-white to-emerald-50/70 shadow-emerald-950/5'
    : 'border-blue-100 bg-gradient-to-br from-blue-50/80 via-white to-slate-50 shadow-blue-950/5';
  const iconClass = isGreen ? 'bg-emerald-100 text-emerald-700' : 'bg-blue-100 text-blue-700';
  const buttonClass = isGreen
    ? 'bg-emerald-700 hover:bg-emerald-800 focus-visible:outline-emerald-700'
    : 'bg-blue-700 hover:bg-blue-800 focus-visible:outline-blue-700';
  const chipClass = isGreen
    ? 'border-emerald-200 bg-emerald-50 text-emerald-900 hover:border-emerald-300'
    : 'border-slate-200 bg-white text-slate-700 hover:border-blue-200';

  return (
    <section className={`rounded-xl border p-4 shadow-sm ${cardClass}`}>
      <div className="flex gap-4">
        <div
          className={`flex h-16 w-16 shrink-0 items-center justify-center rounded-full ${iconClass}`}
        >
          {isGreen ? <SupportIcon /> : <AdminIcon />}
        </div>
        <div className="min-w-0">
          <h2 className="text-xl font-bold leading-tight tracking-tight text-slate-950 lg:whitespace-nowrap">
            {card.heading}
          </h2>
          <p className="mt-2 max-w-none text-sm leading-5 text-slate-700 xl:whitespace-nowrap">
            {card.description}
          </p>
          <a
            className={`mt-3 inline-flex items-center gap-2 rounded-md px-3 py-1.5 text-xs font-bold text-white shadow-sm transition ${buttonClass}`}
            href={card.ctaHref}
          >
            {card.ctaText}
            <ArrowIcon />
          </a>
        </div>
      </div>

      <div className="mt-4 border-t border-slate-200 pt-3">
        <div className="flex flex-wrap items-center gap-2">
          <span className="mr-1 text-sm font-semibold text-slate-950">Popular regions</span>
          {card.regions.map((region) => (
            <a
              key={region.label}
              href={region.href}
              className={`rounded-md border px-2.5 py-1 text-xs font-medium transition ${chipClass}`}
            >
              {region.label}
            </a>
          ))}
          <a
            href={card.viewAllHref}
            className="ml-auto text-sm font-semibold text-blue-700 hover:text-blue-900"
          >
            View all
          </a>
        </div>
      </div>
    </section>
  );
}

export default function Page() {
  return (
    <main className="bg-white">
      <section id="about" className="mx-auto max-w-6xl px-4 pb-8 pt-9 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-950 sm:text-4xl">
            Curated jobs by role and region
          </h1>
          <p className="mt-2 text-base text-slate-600">
            Current jobs, checked daily. No signup required.
          </p>
        </div>

        <div className="mt-7 grid gap-6 lg:grid-cols-2">
          {roleFamilies.map((card) => (
            <RoleCard key={card.heading} card={card} />
          ))}
        </div>

        <section className="mt-9" aria-labelledby="recently-added-heading">
          <div className="mb-4 flex items-center justify-between gap-4">
            <h2
              id="recently-added-heading"
              className="flex items-center gap-3 text-xl font-bold text-slate-950"
            >
              <span className="inline-flex h-5 w-5 items-center justify-center rounded-full border-2 border-slate-950 text-slate-950">
                <span className="h-1.5 w-1.5 rounded-full bg-slate-950" />
              </span>
              Recently added jobs
            </h2>
            <a
              href="/browse-jobs"
              className="inline-flex items-center gap-2 text-sm font-bold text-blue-700 hover:text-blue-900"
            >
              View all recent jobs <ArrowIcon />
            </a>
          </div>

          <div className="grid gap-5 md:grid-cols-3">
            {recentJobs.map((job) => (
              <a
                key={`${job.title}-${job.company}`}
                href={job.href}
                className="group rounded-lg border border-slate-200 bg-white p-5 shadow-sm transition hover:border-blue-200 hover:shadow-md"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h3 className="text-lg font-bold text-slate-950">{job.title}</h3>
                    <p className="mt-2 text-sm text-slate-600">
                      {job.company} <span className="px-2">•</span> {job.region}
                    </p>
                    <p className="mt-4 text-sm text-slate-600">
                      {job.type} <span className="px-2">•</span> Added today
                    </p>
                  </div>
                  <span className="mt-12 text-slate-950 transition group-hover:translate-x-0.5">
                    <ArrowIcon />
                  </span>
                </div>
              </a>
            ))}
          </div>
        </section>

        <section
          id="how-it-works"
          className="mt-9 rounded-xl bg-slate-50 px-6 py-4"
          aria-labelledby="how-ontap-works-heading"
        >
          <h2 id="how-ontap-works-heading" className="text-center text-xl font-bold text-slate-950">
            How Ontap works
          </h2>
          <div className="mt-4 grid gap-4 md:grid-cols-3 md:divide-x md:divide-slate-200">
            {[
              'We find live job pages',
              'We check them daily',
              'We organise them by role and region',
            ].map((step, index) => (
              <div key={step} className="flex items-center gap-4 px-4 py-2">
                <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center text-blue-700">
                  <svg aria-hidden="true" className="h-9 w-9" viewBox="0 0 40 40" fill="none">
                    {index === 0 && (
                      <path
                        d="M18 28a10 10 0 1 1 7.1-2.9L32 32"
                        stroke="currentColor"
                        strokeWidth="2.4"
                        strokeLinecap="round"
                      />
                    )}
                    {index === 1 && (
                      <path
                        d="M20 5 31 10v9c0 7-4.5 12-11 16C13.5 31 9 26 9 19v-9l11-5Z"
                        stroke="currentColor"
                        strokeWidth="2.4"
                        strokeLinejoin="round"
                      />
                    )}
                    {index === 2 && (
                      <>
                        <path
                          d="M20 35s10-9.2 10-19A10 10 0 0 0 10 16c0 9.8 10 19 10 19Z"
                          stroke="currentColor"
                          strokeWidth="2.4"
                          strokeLinejoin="round"
                        />
                        <circle cx="20" cy="16" r="3" stroke="currentColor" strokeWidth="2.4" />
                      </>
                    )}
                  </svg>
                </span>
                <p className="text-sm leading-5 text-slate-700">
                  <strong className="text-slate-950">
                    {index + 1}. {step}
                  </strong>
                </p>
              </div>
            ))}
          </div>
        </section>
      </section>
    </main>
  );
}

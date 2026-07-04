type RegionLink = {
  label: string;
  href: string;
};

type RoleFamily = {
  title: string;
  text: string;
  links: RegionLink[];
};

const roleFamilies: RoleFamily[] = [
  {
    title: 'Admin, office support & customer service',
    text: 'Browse current admin, office-support and customer-service jobs by region.',
    links: [
      { label: 'West Yorkshire', href: '/west-yorkshire/service-administrator-jobs' },
      { label: 'South Yorkshire', href: '/south-yorkshire/service-administrator-jobs' },
      { label: 'North East', href: '/north-east/service-administrator-jobs' },
      { label: 'View all admin jobs', href: '/browse-jobs' },
    ],
  },
  {
    title: 'Support worker & care roles',
    text: 'Browse current support-worker, residential-care and community-support roles by region.',
    links: [
      { label: 'North East', href: '/north-east/support-worker' },
      { label: 'View all support worker jobs', href: '/browse-jobs' },
    ],
  },
];

const howOntapWorks = [
  'Choose a role family',
  'Open a regional job page',
  'Apply directly on employer sites',
];

function RoleFamilyCard({ family }: { family: RoleFamily }) {
  return (
    <section className="rounded-xl border border-[#dbe3ee] bg-white p-4">
      <h2 className="text-lg font-extrabold leading-tight text-gray-900">{family.title}</h2>
      <p className="mt-1 text-sm leading-6 text-gray-600">{family.text}</p>

      <div className="mt-3 flex flex-wrap gap-2">
        {family.links.map((link) => (
          <a
            key={`${family.title}-${link.href}-${link.label}`}
            href={link.href}
            className="rounded-lg border border-gray-200 bg-gray-50 px-3 py-1.5 text-sm font-semibold text-blue-700 transition hover:border-blue-300 hover:bg-blue-50 hover:text-blue-900"
          >
            {link.label} →
          </a>
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

      <main data-homepage className="mx-auto max-w-[1180px] px-4 py-9">
        <header className="mb-4 max-w-3xl">
          <h1 className="text-[28px] font-extrabold leading-tight tracking-tight text-gray-900">
            Curated jobs by role and region
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Current jobs, checked daily. No signup required.
          </p>
        </header>

        <div className="grid gap-3 md:grid-cols-2">
          {roleFamilies.map((family) => (
            <RoleFamilyCard key={family.title} family={family} />
          ))}
        </div>

        <section className="mt-4 rounded-xl border border-gray-100 bg-gray-50 p-3">
          <h2 className="text-sm font-extrabold text-gray-800">How Ontap works</h2>
          <div className="mt-2 flex flex-wrap gap-2">
            {howOntapWorks.map((item) => (
              <span
                key={item}
                className="rounded-full border border-gray-200 bg-white px-3 py-1 text-xs font-semibold text-gray-600"
              >
                {item}
              </span>
            ))}
          </div>
        </section>
      </main>
    </>
  );
}

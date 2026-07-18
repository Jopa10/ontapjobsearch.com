import westYorkshireSupportWorkerJobs from '../west-yorkshire/support-worker.json';
import southYorkshireSupportWorkerJobs from '../south-yorkshire/support-worker.json';
import northEastSupportWorkerJobs from '../north-east/support-worker-jobs.json';
import sussexSupportWorkerJobs from '../sussex/support-worker.json';
import cumbriaSouthSupportWorkerJobs from '../cumbria-south/support-worker.json';

type BrowseCard = {
  title: string;
  href: string;
  description: string;
  status: string;
  statusClassName: string;
};

type BrowseSection = {
  heading: string;
  intro: string;
  featuredCards?: BrowseCard[];
  cards: BrowseCard[];
};

const activeStatusClassName = 'border-green-200 bg-green-50 text-green-700';
const pausedStatusClassName = 'border-amber-200 bg-amber-50 text-amber-700';

const getSupportWorkerStatus = (
  jobs: unknown[],
  region: string
): Pick<BrowseCard, 'description' | 'status' | 'statusClassName'> => {
  if (jobs.length > 0) {
    return {
      description: `Current support-worker roles are available across ${region}, with employer-site application links.`,
      status: 'Active current supply',
      statusClassName: activeStatusClassName,
    };
  }

  return {
    description: `Support-worker page retained for ${region}. Current support-worker JSON is empty, so supply is paused or limited.`,
    status: 'Paused / limited current supply',
    statusClassName: pausedStatusClassName,
  };
};

const westYorkshireSupportWorkerStatus = getSupportWorkerStatus(
  westYorkshireSupportWorkerJobs,
  'West Yorkshire'
);
const southYorkshireSupportWorkerStatus = getSupportWorkerStatus(
  southYorkshireSupportWorkerJobs,
  'South Yorkshire'
);
const northEastSupportWorkerStatus = getSupportWorkerStatus(
  northEastSupportWorkerJobs,
  'North East'
);
const sussexSupportWorkerStatus = getSupportWorkerStatus(sussexSupportWorkerJobs, 'Sussex');
const southCumbriaSupportWorkerStatus = getSupportWorkerStatus(
  cumbriaSouthSupportWorkerJobs,
  'South Cumbria'
);

const jobSections: BrowseSection[] = [
  {
    heading: 'Active admin, service administrator and customer-service jobs',
    intro: 'These pages are the current active offer and contain live admin-service job supply.',
    featuredCards: [
      {
        title: 'Central & Inner London Admin & Cust. Service Jobs',
        href: '/london/service-administrator-jobs',
        description:
          'Service administrator, customer service administrator and office support roles across Central and Inner London.',
        status: 'Active current supply',
        statusClassName: activeStatusClassName,
      },
      {
        title: 'Outer London Admin & Cust. Service Jobs',
        href: '/london/outer-service-administrator-jobs',
        description:
          'Service administrator, customer service administrator and office support roles across Outer London.',
        status: 'Active current supply',
        statusClassName: activeStatusClassName,
      },
    ],
    cards: [
      {
        title: 'West Yorkshire Admin & Customer Service Jobs',
        href: '/west-yorkshire/service-administrator-jobs',
        description:
          'Service administrator, customer service administrator and office support roles across Leeds and West Yorkshire.',
        status: 'Active current supply',
        statusClassName: activeStatusClassName,
      },
      {
        title: 'South Yorkshire Admin & Customer Service Jobs',
        href: '/south-yorkshire/service-administrator-jobs',
        description:
          'Service administrator, customer service administrator and office support roles across Sheffield and South Yorkshire.',
        status: 'Active current supply',
        statusClassName: activeStatusClassName,
      },
      {
        title: 'North East Admin & Customer Service Jobs',
        href: '/north-east/service-administrator-jobs',
        description:
          'Service administrator, customer service administrator and office support roles across Newcastle and the North East.',
        status: 'Active current supply',
        statusClassName: activeStatusClassName,
      },
      {
        title: 'Hampshire Admin & Customer Service Jobs',
        href: '/hampshire/service-administrator-jobs',
        description:
          'Service administrator, customer service administrator and office support roles across Hampshire.',
        status: 'Active current supply',
        statusClassName: activeStatusClassName,
      },
    ],
  },
  {
    heading: 'Support worker jobs',
    intro:
      'Current support-worker pages are listed below. Individual pages show whether supply is active or temporarily limited.',
    cards: [
      {
        title: 'West Yorkshire Support Worker Jobs',
        href: '/west-yorkshire/support-worker',
        ...westYorkshireSupportWorkerStatus,
      },
      {
        title: 'South Yorkshire Support Worker Jobs',
        href: '/south-yorkshire/support-worker',
        ...southYorkshireSupportWorkerStatus,
      },
      {
        title: 'North East Support Worker Jobs',
        href: '/north-east/support-worker',
        ...northEastSupportWorkerStatus,
      },
      {
        title: 'Sussex Support Worker Jobs',
        href: '/sussex/support-worker',
        ...sussexSupportWorkerStatus,
      },
      {
        title: 'South Cumbria Support Worker Jobs',
        href: '/cumbria-south/support-worker',
        ...southCumbriaSupportWorkerStatus,
      },
    ],
  },
];

function BrowseCardLink({ card }: { card: BrowseCard }) {
  return (
    <a
      href={card.href}
      className="block rounded-xl border border-gray-200 bg-white p-4 text-gray-900 transition hover:border-blue-300 hover:bg-blue-50"
    >
      <div className="mb-3 flex flex-wrap items-start justify-between gap-2">
        <h3 className="text-lg font-semibold leading-tight">{card.title}</h3>
        <span
          className={`rounded-full border px-2.5 py-1 text-xs font-semibold ${card.statusClassName}`}
        >
          {card.status}
        </span>
      </div>

      <p className="text-sm leading-6 text-gray-600">{card.description}</p>

      <div className="mt-3 text-sm font-medium text-blue-700">View page →</div>
    </a>
  );
}

export default function Page() {
  return (
    <main className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8">
      <h1 className="mb-3 text-3xl font-bold tracking-tight text-gray-900">Browse Jobs</h1>

      <p className="mb-8 max-w-3xl text-base text-gray-600">
        Browse current job pages. Admin, service administrator and customer-service pages are listed
        first because they are the main active offer right now.
      </p>

      <div className="grid gap-8">
        {jobSections.map((section) => (
          <section key={section.heading}>
            <div className="mb-3">
              <h2 className="text-2xl font-semibold tracking-tight text-gray-900">
                {section.heading}
              </h2>
              <p className="mt-1 text-sm text-gray-600">{section.intro}</p>
            </div>

            <div className="grid gap-3 md:grid-cols-2">
              {section.cards.map((card) => (
                <BrowseCardLink key={card.href} card={card} />
              ))}
            </div>

            {section.featuredCards ? (
              <div className="mt-3 rounded-xl border border-gray-200 bg-gray-50 p-3">
                <div className="mb-3 border-b border-gray-200 pb-2 text-sm font-semibold text-gray-600">
                  London admin & customer-service jobs
                </div>
                <div className="grid gap-3 md:grid-cols-2">
                  {section.featuredCards.map((card) => (
                    <BrowseCardLink key={card.href} card={card} />
                  ))}
                </div>
              </div>
            ) : null}
          </section>
        ))}
      </div>
    </main>
  );
}

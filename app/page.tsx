import westYorkshireJobs from './west-yorkshire/support-worker.json';
import southYorkshireJobs from './south-yorkshire/support-worker.json';

type Job = {
  title?: string;
  company?: string;
  location?: string;
  salary_text?: string;
  apply_url?: string;
};

const stripHtml = (text = '') =>
  text
    .replace(/Â£/g, '£')
    .replace(/<[^>]*>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

function MiniJobCard({ job, sliceUrl }: { job: Job; sliceUrl: string }) {
  return (
    <article className="rounded-lg border border-gray-200 bg-white p-3">
      <h3 className="text-base font-semibold mb-1">{job.title}</h3>

      <p className="text-sm text-gray-600 mb-2">
        {job.company} • {job.location}
      </p>

      {job.salary_text && (
        <p className="text-sm font-semibold mb-3">{stripHtml(job.salary_text)}</p>
      )}

      <a href={sliceUrl} className="text-sm font-medium text-blue-700 hover:text-blue-900">
        View role →
      </a>
    </article>
  );
}

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
    <section className="rounded-xl border border-gray-200 p-4 hover:border-blue-300 hover:bg-blue-50">
      <h2 className="text-xl font-semibold mb-1">{title}</h2>

      <p className="text-gray-600 mb-4">{intro}</p>

      <a
        href={sliceUrl}
        className="inline-block rounded-lg bg-blue-600 px-4 py-2 font-medium text-white"
      >
        {ctaText}
      </a>

      <div className="mt-4 grid gap-3">
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
    <main className="mx-auto max-w-6xl px-6 py-8">
      <h1 className="max-w-3xl text-4xl font-bold tracking-tight mb-4">
        Yorkshire Support Worker Jobs
      </h1>

      <p className="max-w-3xl text-lg text-gray-700 mb-3">
        Live support worker roles across West and South Yorkshire.
      </p>

      <p className="max-w-3xl text-sm text-gray-600 mb-4">
        Updated daily • Apply directly on employer websites • No signup required
      </p>
      <div className="flex flex-wrap gap-2 mb-4 text-sm">
        <span className="rounded-full bg-gray-100 px-3 py-1 text-gray-700">Updated daily</span>

        <span className="rounded-full bg-gray-100 px-3 py-1 text-gray-700">
          West & South Yorkshire roles
        </span>

        <span className="rounded-full bg-gray-100 px-3 py-1 text-gray-700">
          Direct employer applications
        </span>

        <span className="rounded-full bg-gray-100 px-3 py-1 text-gray-700">No signup required</span>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
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
    </main>
  );
}

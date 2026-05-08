import westYorkshireJobs from "./west-yorkshire/support-worker.json";
import southYorkshireJobs from "./south-yorkshire/support-worker.json";

type Job = {
  title?: string;
  company?: string;
  location?: string;
  salary_text?: string;
  summary?: string;
  description?: string;
  apply_url?: string;
};

const stripHtml = (text = "") =>
  text
    .replace(/Â£/g, "£")
    .replace(/<[^>]*>/g, " ")
    .replace(/\s+/g, " ")
    .trim();

const getSummary = (job: Job) =>
  job.summary || stripHtml(job.description).slice(0, 180);

function FeaturedJobCard({
  job,
  region,
  sliceUrl,
}: {
  job: Job;
  region: string;
  sliceUrl: string;
}) {
  return (
    <article className="rounded-xl border border-gray-200 p-5">
      <p className="text-sm font-medium text-gray-500 mb-2">{region}</p>

      <h3 className="text-xl font-semibold mb-1">{job.title}</h3>

      <p className="text-gray-600 mb-2">
        {job.company} • {job.location}
      </p>

      {job.salary_text && (
        <p className="font-semibold mb-3">{job.salary_text}</p>
      )}

      <p className="text-gray-700 mb-4">{getSummary(job)}</p>

      <a
        href={sliceUrl}
        className="inline-block rounded-lg bg-blue-600 px-4 py-2 font-medium text-white"
      >
        View role
      </a>
    </article>
  );
}

export default function Page() {
  const westJob = westYorkshireJobs[0];
  const southJob = southYorkshireJobs[0];

  return (
    <main className="mx-auto max-w-4xl px-6 py-10">
      <h1 className="text-4xl font-bold tracking-tight mb-4">
        Yorkshire Support Worker Jobs
      </h1>

      <p className="text-lg text-gray-700 mb-3">
        Live support worker roles across West and South Yorkshire.
      </p>

      <p className="text-sm text-gray-600 mb-6">
        Updated daily • Apply directly on employer websites • No signup required
      </p>

    <a
  href="/jobs/all"
  className="inline-block rounded-lg bg-blue-600 px-5 py-3 text-lg font-medium text-white mb-8"
>
  Browse all current jobs →
</a>

      <section className="mb-10">
        <h2 className="text-2xl font-bold mb-4">Latest live roles</h2>

        <div className="grid gap-4">
          <FeaturedJobCard
            job={westJob}
            region="West Yorkshire"
            sliceUrl="/west-yorkshire/support-worker"
          />

          <FeaturedJobCard
            job={southJob}
            region="South Yorkshire"
            sliceUrl="/south-yorkshire/support-worker"
          />
        </div>
      </section>

      <section className="grid gap-4">
        <a
          href="/west-yorkshire/support-worker"
          className="block rounded-xl border border-gray-200 p-5 hover:border-blue-300 hover:bg-blue-50"
        >
          <h2 className="text-xl font-semibold mb-1">
            West Yorkshire Support Worker Jobs
          </h2>
          <p className="text-gray-600">
            Current Leeds and West Yorkshire support worker roles, updated daily.
          </p>
        </a>

        <a
          href="/south-yorkshire/support-worker"
          className="block rounded-xl border border-gray-200 p-5 hover:border-blue-300 hover:bg-blue-50"
        >
          <h2 className="text-xl font-semibold mb-1">
            South Yorkshire Support Worker Jobs
          </h2>
          <p className="text-gray-600">
            Current Sheffield and South Yorkshire support worker roles, updated daily.
          </p>
        </a>
      </section>
    </main>
  );
}

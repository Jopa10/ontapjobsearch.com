import jobs from "@/data/leeds-admin-officer.json";

export const metadata = {
  title: "Ontap — Admin Officer jobs in Leeds",
  description: "Public sector and charity Admin Officer roles in Leeds.",
};

type Job = {
  id?: string;
  title: string;
  company?: string;
  location?: string;
  applyUrl?: string;
  url?: string;
  redirectUrl?: string;
};

export default function Page() {
  return (
    <main className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Admin Officer jobs in Leeds</h1>

      <div className="space-y-4">
        {(jobs as Job[]).map((job, i) => {
          const applyHref = job.applyUrl || job.url || job.redirectUrl;

          return (
            <div key={job.id ?? i} className="border rounded-lg p-4">
              <h2 className="font-semibold text-lg">{job.title}</h2>

              {(job.company || job.location) && (
                <p className="text-sm text-gray-600">
                  {job.company}
                  {job.company && job.location ? " – " : ""}
                  {job.location}
                </p>
              )}

              {applyHref && (
                <a
                  href={applyHref}
                  target="_blank"
                  rel="noopener noreferrer nofollow"
                  className="inline-flex mt-3 items-center rounded-md px-4 py-2 font-medium border"
                >
                  Apply
                </a>
              )}
            </div>
          );
        })}
      </div>
    </main>
  );
}




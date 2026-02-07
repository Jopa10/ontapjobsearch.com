export const metadata = {
  title: "Ontap – Support Worker jobs in Leeds",
  description: "Public sector and charity Admin Officer roles in Leeds.",
};

type Job = {
  id: string;
  title: string;
  company: string;
  location: string;
  applyUrl?: string;
  url?: string;
  redirectUrl?: string;
};

const jobs: Job[] = [
  {
    id: "1",
    title: "Admin Officer",
    company: "Leeds City Council",
    location: "Leeds",
    applyUrl:
      "https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID=cGFnZWFjdGlvbj12aWV3dmFjYnlqb2JsaXN0JmpvYmxpc3Rfdmlld192YWM9MTk4NTE1OSZzZWFyY2hwYWdlPTExJnVzZXJzZWFyY2hjb250ZXh0PTE3MjY2OTc0MSZzZWFyY2hzb3J0PWNsb3Npbmcmb3duZXJ0eXBlPWZhaXImcGFnZWNsYXNzPUpvYnMmb3duZXI9NTA3MDAwMCZyZXFzaWc9MTc3MDQ2NTU1OS01NDFlODIyYTA3MWQ1ZTYwNTI2YWJmZjdhM2NlOTQzNGIyMjVkYzZi",
  },
  {
    id: "2",
    title: "Senior Admin Officer",
    company: "NHS Trust",
    location: "Leeds",
    applyUrl:
      "https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID=cGFnZWFjdGlvbj12aWV3dmFjYnlqb2JsaXN0JmpvYmxpc3Rfdmlld192YWM9MTk4NTE1OSZzZWFyY2hwYWdlPTExJnVzZXJzZWFyY2hjb250ZXh0PTE3MjY2OTc0MSZzZWFyY2hzb3J0PWNsb3Npbmcmb3duZXJ0eXBlPWZhaXImcGFnZWNsYXNzPUpvYnMmb3duZXI9NTA3MDAwMCZyZXFzaWc9MTc3MDQ2NTU1OS01NDFlODIyYTA3MWQ1ZTYwNTI2YWJmZjdhM2NlOTQzNGIyMjVkYzZi",
  },
];

export default function Page() {
  return (
    <main className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Admin Officer jobs in Leeds</h1>

      <div className="space-y-4">
        {jobs.map((job) => {
          const applyHref = job.applyUrl || job.url || job.redirectUrl;

          return (
            <div key={job.id} className="border rounded-lg p-4">
              <h2 className="font-semibold text-lg">{job.title}</h2>

              {(job.company || job.location) && (
                <p className="text-sm text-gray-600">
                  {job.company} {job.company && job.location ? "•" : ""}{" "}
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

export const metadata = {
  title: "Ontap — Admin Officer jobs in Leeds",
  description: "Public sector and charity Admin Officer roles in Leeds.",
};

type Job = {
  id: string;
  title: string;
  organisation: string;
  location: string;
  salary: string;
  contract: string;
  closingDate: string;
  reference?: string;
  url: string;
};

const featuredJob: Job = {
  id: "leeds-adminoff-001",
  title: "Admin Officer (Patient Services)",
  organisation: "Leeds Teaching Hospitals NHS Trust",
  location: "Leeds (St James’s University Hospital)",
  salary: "£22,816 – £24,336 (Band 3)",
  contract: "Permanent • Full-time",
  closingDate: "18 Feb 2026",
  reference: "LTHT/PS/2411",
  url: "#",
};

const similarJobs: Job[] = [
  {
    id: "leeds-adminoff-002",
    title: "Administrative Officer (Business Support)",
    organisation: "Leeds City Council",
    location: "Leeds (Civic Hall)",
    salary: "£23,114 – £24,496",
    contract: "Permanent • Full-time",
    closingDate: "20 Feb 2026",
    reference: "LCC/BS/0192",
    url: "#",
  },
  {
    id: "leeds-adminoff-003",
    title: "Admin Officer (Community Services)",
    organisation: "NHS West Yorkshire Integrated Care Board",
    location: "Leeds (Hybrid)",
    salary: "£25,147 – £27,596 (Band 4)",
    contract: "Fixed-term (12 months) • Full-time",
    closingDate: "21 Feb 2026",
    reference: "WYICB/CS/0440",
    url: "#",
  },
  {
    id: "leeds-adminoff-004",
    title: "Admin Officer (Student Services)",
    organisation: "University of Leeds",
    location: "Leeds",
    salary: "£23,700 – £25,200",
    contract: "Permanent • Full-time",
    closingDate: "23 Feb 2026",
    reference: "UOL/SS/1128",
    url: "#",
  },
  {
    id: "leeds-adminoff-005",
    title: "Admin Officer (Housing Repairs)",
    organisation: "Leeds Federated Housing Association",
    location: "Leeds",
    salary: "£22,000 – £24,000",
    contract: "Permanent • Full-time",
    closingDate: "24 Feb 2026",
    reference: "LFHA/HR/0077",
    url: "#",
  },
  {
    id: "leeds-adminoff-006",
    title: "Admin Officer (Safeguarding Support)",
    organisation: "Barnardo’s",
    location: "Leeds (Hybrid)",
    salary: "£23,500",
    contract: "Permanent • Part-time (30 hrs)",
    closingDate: "25 Feb 2026",
    reference: "BAR/SAFE/318",
    url: "#",
  },
  {
    id: "leeds-adminoff-007",
    title: "Admin Officer (Operations Support)",
    organisation: "West Yorkshire Police",
    location: "Leeds (Carr Gate)",
    salary: "£24,462 – £25,878",
    contract: "Permanent • Full-time",
    closingDate: "26 Feb 2026",
    reference: "WYP/OPS/2081",
    url: "#",
  },
];

function JobMeta({ job }: { job: Job }) {
  return (
    <dl>
      <div>
        <dt>Organisation</dt>
        <dd>{job.organisation}</dd>
      </div>
      <div>
        <dt>Location</dt>
        <dd>{job.location}</dd>
      </div>
      <div>
        <dt>Salary</dt>
        <dd>{job.salary}</dd>
      </div>
      <div>
        <dt>Contract</dt>
        <dd>{job.contract}</dd>
      </div>
      <div>
        <dt>Closing date</dt>
        <dd>{job.closingDate}</dd>
      </div>
      {job.reference ? (
        <div>
          <dt>Reference</dt>
          <dd>{job.reference}</dd>
        </div>
      ) : null}
    </dl>
  );
}

export default function Page() {
  return (
    <main style={{ maxWidth: 860, margin: "0 auto", padding: "24px 16px" }}>
      <header style={{ marginBottom: 20 }}>
        <h1 style={{ margin: "0 0 8px" }}>Admin Officer jobs in Leeds</h1>
        <p style={{ margin: 0 }}>
          A minimal Phase-1 slice page (static mock data). One featured role plus similar roles.
        </p>
      </header>

      <section aria-labelledby="featured" style={{ marginBottom: 28 }}>
        <h2 id="featured" style={{ margin: "0 0 12px" }}>
          Featured role
        </h2>

        <article style={{ border: "1px solid #ddd", borderRadius: 8, padding: 16 }}>
          <h3 style={{ margin: "0 0 6px" }}>{featuredJob.title}</h3>
          <JobMeta job={featuredJob} />
          <p style={{ margin: "12px 0 0" }}>
            <a href={featuredJob.url}>View job</a>
          </p>
        </article>
      </section>

      <section aria-labelledby="similar">
        <h2 id="similar" style={{ margin: "0 0 12px" }}>
          Similar jobs
        </h2>

        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
          {similarJobs.map((job) => (
            <li key={job.id} style={{ marginBottom: 12 }}>
              <article style={{ border: "1px solid #eee", borderRadius: 8, padding: 14 }}>
                <h3 style={{ margin: "0 0 6px" }}>{job.title}</h3>
                <JobMeta job={job} />
                <p style={{ margin: "12px 0 0" }}>
                  <a href={job.url}>View job</a>
                </p>
              </article>
            </li>
          ))}
        </ul>
      </section>

      <footer style={{ marginTop: 28, fontSize: 14 }}>
        <p style={{ margin: 0 }}>Note: This page uses static mock jobs only (Phase-1).</p>
      </footer>
    </main>
  );
}


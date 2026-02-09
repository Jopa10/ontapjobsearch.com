export const metadata = {
  title: "Ontap – Administrator jobs in Leeds",
  description: "Public sector and charity Administrator roles in Leeds.",
};

type Job = {
  id: string;
  title: string;
  company: string;
  location: string;
  applyUrl?: string;
};

const jobs: Job[] = [
  {
    id: "1",
    title: "Administrator",
    company: "Leeds City Council",
    location: "Leeds",
    applyUrl: "#",
  },
  {
    id: "2",
    title: "Senior Administrator Officer",
    company: "NHS Trust",
    location: "Leeds",
    applyUrl: "#",
  },
];

export default function Page() {
  return (
    <main style={{ maxWidth: 800, margin: "40px auto", padding: 20 }}>
      <h1>Administrator jobs in Leeds</h1>

      {jobs.map((job) => (
        <div
          key={job.id}
          style={{
            border: "1px solid #ccc",
            borderRadius: 12,
            padding: 20,
            marginTop: 20,
          }}
        >
          <h2>{job.title}</h2>
          <p>
            {job.company} – {job.location}
          </p>
          <button>Apply</button>
        </div>
      ))}
    </main>
  );
}


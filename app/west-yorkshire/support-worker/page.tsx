import fs from "node:fs";
import path from "node:path";
import TrainingLink from "@/components/traininglink";

type JobRow = {
  job_id: string;
  title: string;
  company: string;
  location: string;
  region: string;
  country: string;
  category: string;
  employment_type: string;
  advertiser_type: string;
  salary_min: string;
  salary_max: string;
  salary_period: string;
  salary_text: string;
  work_pattern: string;
  posted_date: string;
  closing_date: string;
  summary: string;
  description: string;
  full_description: string;
  apply_url: string;
  source: string;
};

function readJobsJson(): JobRow[] {
  const filePath = path.join(
    process.cwd(),
    "app",
    "west-yorkshire",
    "support-worker.json"
  );

  const parsed = JSON.parse(fs.readFileSync(filePath, "utf8"));

  return parsed.map((r: any) => ({
    job_id: r.job_id || r["/Job/DisplayReference"] || "",
    title: r.title || r["/Job/Position"] || "",
    company: r.company || r["/Job/AdvertiserName"] || "",
    location: r.location || r["/Job/Area"] || "",
    region: r.region || "West Yorkshire",
    country: "UK",
    category: r.category || "",
    employment_type: r.employment_type || r["/Job/EmploymentType"] || "",
    advertiser_type: r.advertiser_type || r["/Job/AdvertiserType"] || "",
    salary_min: r.salary_min || r["/Job/SalaryMinimum"] || "",
    salary_max: r.salary_max || r["/Job/SalaryMaximum"] || "",
    salary_period: r.salary_period || r["/Job/SalaryPeriod"] || "",
    salary_text: r.salary_text || r["/Job/SalaryAdditional"] || "",
    work_pattern: r.work_pattern || r["/Job/EmploymentType"] || "",
    posted_date: r.posted_date || "",
    closing_date: r.closing_date || "",
    summary: r.summary || "",
    description: r.description || "",
    full_description:
      r.full_description || r.description || r["/Job/Description"] || "",
    apply_url: r.apply_url || r["/Job/ApplicationURL"] || "",
    source: "JobG8",
  }));
}

function cleanText(value: string) {
  return (value || "").replace(/\s+/g, " ").trim();
}

function stripHtml(html: string) {
  return (html || "").replace(/<[^>]+>/g, "").trim();
}

function getSummary(job: JobRow) {
  if (job.summary) return cleanText(job.summary);
  return stripHtml(job.full_description || "").slice(0, 140);
}

function getFullDescription(job: JobRow) {
  return stripHtml(job.full_description || "");
}

function formatSalary(job: JobRow) {
  return job.salary_text || "";
}

const training = [
  {
    title: "Care Certificate Online Course",
    provider: "CareSkills Academy",
    description:
      "Covers all 16 Care Certificate standards. Entry-level care training.",
    link: "https://careskillsacademy.co.uk/courses/care-certificate/",
  },
  {
    title: "Moving and Handling of People",
    provider: "TutorCare",
    description:
      "Patient handling training for care roles. Reduces injury risk.",
    link: "https://tutorcare.co.uk/courses/moving-and-handling-of-people/",
  },
  {
    title: "PMVA – Prevention and Management of Violence and Aggression",
    provider: "Occuteach",
    description:
      "Covers de-escalation and safe intervention techniques in care settings.",
    link: "https://occuteach.co.uk/courses/pmva-prevention-and-management-of-violence-and-aggression/",
  },
];

export default function Page() {
  const jobs = readJobsJson();

  return (
    <main style={{ maxWidth: 1180, margin: "36px auto", padding: "0 16px" }}>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "250px 1fr",
          columnGap: 20,
          alignItems: "start",
        }}
      >
        <aside
          style={{
            alignSelf: "start",
            position: "sticky",
            top: 24,
          }}
        >
          <div style={{ fontWeight: 800, marginBottom: 6 }}>
            Get started faster
          </div>

          <p style={{ fontSize: 13, color: "#666", marginBottom: 10 }}>
            Useful courses that may help strengthen early care applications.
          </p>

          <div style={{ display: "grid", gap: 8 }}>
            {training.map((item, idx) => (
              <div
                key={idx}
                style={{
                  border: "1px solid #e5e7eb",
                  borderRadius: 10,
                  padding: "10px 12px",
                  background: "#f9fafb",
                }}
              >
                <div style={{ fontWeight: 700, fontSize: 14 }}>
                  {item.title}
                </div>

                <div style={{ fontSize: 12, color: "#666" }}>
                  {item.provider}
                </div>

                <div style={{ fontSize: 12, color: "#666", margin: "6px 0" }}>
                  {item.description}
                </div>

                <TrainingLink
                  href={item.link}
                  title={item.title}
                  provider={item.provider}
                />
              </div>
            ))}
          </div>
        </aside>

        <div>
          <div style={{ marginBottom: 14 }}>
            <h1
              style={{
                fontSize: 28,
                fontWeight: 800,
                marginBottom: 6,
              }}
            >
              West Yorkshire Support Worker Roles
            </h1>

            <p style={{ color: "#6b7280", fontSize: 14 }}>
              Updated daily • Latest update: Fri 17th April, PM • Roles across
              West Yorkshire • Apply on employer sites
            </p>
          </div>

          <div style={{ display: "grid", gap: 10 }}>
            {jobs.map((j, idx) => (
              <div
                key={idx}
                style={{
                  border: "1px solid #dbe3ee",
                  borderRadius: 12,
                  padding: "14px 16px",
                  background: "#fff",
                }}
              >
                <div style={{ fontWeight: 800, fontSize: 16 }}>
                  {j.title}
                </div>

                <div style={{ fontSize: 13, color: "#555", marginBottom: 4 }}>
                  {j.company} • {j.location}
                </div>

                <div style={{ fontWeight: 600, marginBottom: 6 }}>
                  {formatSalary(j)}
                </div>

                <div style={{ fontSize: 13, color: "#666", marginBottom: 8 }}>
                  {getSummary(j)}
                </div>

                <details>
                  <summary
                    style={{
                      fontSize: 13,
                      color: "#2563eb",
                      cursor: "pointer",
                    }}
                  >
                    View full job description
                  </summary>
                  <div style={{ marginTop: 6, fontSize: 13 }}>
                    {getFullDescription(j)}
                  </div>
                </details>

                <a
                  href={j.apply_url}
                  target="_blank"
                  rel="noreferrer"
                  style={{
                    display: "inline-block",
                    marginTop: 10,
                    background: "#2563eb",
                    color: "#fff",
                    padding: "6px 12px",
                    borderRadius: 6,
                  }}
                >
                  Apply Now
                </a>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}



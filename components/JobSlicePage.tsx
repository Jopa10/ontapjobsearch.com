import fs from "node:fs";
import path from "node:path";
import TrainingLink from "@/components/traininglink";
import ApplyButton from "@/components/ApplyButton";

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

type JobSlicePageProps = {
  jsonPath: string[];
  region: string;
  title: string;
  latestUpdate: string;
  anchorTown?: string;
};

function readJobsJson(jsonPath: string[], region: string): JobRow[] {
  const filePath = path.join(process.cwd(), ...jsonPath);
  const parsed = JSON.parse(fs.readFileSync(filePath, "utf8"));

  return parsed.map((r: any) => ({
    job_id: r.job_id || r["/Job/DisplayReference"] || "",
    title: r.title || r["/Job/Position"] || "",
    company: r.company || r["/Job/AdvertiserName"] || "",
    location: r.location || r["/Job/Area"] || "",
    region: r.region || region,
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

function decodeMojibake(value: string) {
  return (value || "")
    .replace(/Â£/g, "£")
    .replace(/Â/g, "")
    .replace(/â€“/g, "–")
    .replace(/â€”/g, "—")
    .replace(/â€˜/g, "‘")
    .replace(/â€™/g, "’")
    .replace(/â€œ/g, "“")
    .replace(/â€/g, "”")
    .replace(/â€¢/g, "•")
    .replace(/&amp;/gi, "&")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'")
    .replace(/&pound;/gi, "£")
    .replace(/&ndash;/gi, "–")
    .replace(/&mdash;/gi, "—")
    .replace(/&bull;/gi, "•")
    .replace(/&nbsp;/gi, " ");
}

function cleanText(value: string) {
  return decodeMojibake(value)
    .replace(/^\s*[\?\uFFFD]\s+(?=[A-Z])/g, "")
    .replace(/\n\s*[\?\uFFFD]\s+(?=[A-Z])/g, "\n")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n[ \t]+/g, "\n")
    .replace(/[ \t]{2,}/g, " ")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function formatSalary(job: JobRow) {
  const salary = job.salary_text ? cleanText(job.salary_text) : "";

  return salary.replace(/£(\d{4,})(?=\s|$)/g, (_, amount) => {
    return "£" + Number(amount).toLocaleString("en-GB");
  });
}

function stripHtml(html: string) {
  if (!html) return "";

  return cleanText(
    decodeMojibake(html)
      .replace(/\r\n/g, "\n")
      .replace(/\r/g, "\n")
      .replace(/<br\s*\/?>/gi, "\n")
      .replace(/<\/p>/gi, "\n\n")
      .replace(/<\/div>/gi, "\n")
      .replace(/<\/h[1-6]>/gi, "\n\n")
      .replace(/<\/ul>/gi, "\n")
      .replace(/<\/ol>/gi, "\n")
      .replace(/<\/li>/gi, "\n")
      .replace(/<li[^>]*>/gi, "• ")
    .replace(/<[^>]+>/g, "")
.replace(/\n{2,}/g, "\n\n")
  );
}

function removeDuplicateStart(full: string, summary: string) {
  const fullText = cleanText(full);
  const summaryText = cleanText(summary);

  if (!fullText) return "";
  if (!summaryText) return fullText;

  if (summaryText.length < 120 && fullText.startsWith(summaryText)) {
    const stripped = fullText.slice(summaryText.length).trimStart();
    return stripped || fullText;
  }

  return fullText;
}

function getSummary(job: JobRow) {
  const summary = cleanText(job.summary);
  if (summary) return summary;

  const fallbackSource = stripHtml(job.full_description || job.description || "");
  if (!fallbackSource) return "";

 let fallbackSummary = fallbackSource.split(/(?<=[.?!])\s+/).slice(0,2).join(' ').trim();

// hard clean
fallbackSummary = fallbackSummary.replace(/[\s\n]+/g, ' ');
fallbackSummary = fallbackSummary.replace(/[^a-zA-Z0-9\.\)\]]+$/g, '');

return fallbackSummary;
}

function getFullDescription(job: JobRow) {
  const source = job.full_description || job.description || "";
  const cleanedDescription = stripHtml(source);
  const summary = getSummary(job);

  if (!cleanedDescription) return "";

  return removeDuplicateStart(cleanedDescription, summary);
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

export default function JobSlicePage({
  jsonPath,
  region,
  title,
  latestUpdate,
  anchorTown,
}: JobSlicePageProps) {
  const jobs = readJobsJson(jsonPath, region);

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
        <aside style={{ alignSelf: "start", position: "sticky", top: 24 }}>
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
            <h1 style={{ fontSize: 28, fontWeight: 800, marginBottom: 6 }}>
              {title}
            </h1>

            <p style={{ color: "#6b7280", fontSize: 14 }}>
              Updated daily • Latest update: {latestUpdate} • Roles across{" "}
              {region} • Apply on employer sites
            </p>
          </div>

          <div style={{ display: "grid", gap: 10 }}>
            {jobs.map((j, idx) => {
              const summary = getSummary(j);
              const fullDescription = getFullDescription(j);

              return (
                <div
                  key={j.job_id || idx}
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
                    {anchorTown && j.location === anchorTown && (
                      <span
                        style={{
                          marginLeft: 6,
                          padding: "2px 6px",
                          fontSize: 11,
                          borderRadius: 6,
                          background: "#e0f2fe",
                          color: "#0369a1",
                        }}
                      >
                        {anchorTown}
                      </span>
                    )}
                  </div>

                  <div style={{ fontWeight: 600, marginBottom: 6 }}>
                    {formatSalary(j)}
                  </div>

                  {summary ? (
                    <div
                      style={{
                        fontSize: 13,
                        color: "#666",
                        marginBottom: 8,
                     lineHeight: 1.5,
                      }}
                    >
                      {summary}
                    </div>
                  ) : null}

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

                    <div
                      style={{
                        marginTop: 8,
                        fontSize: 14,
                        whiteSpace: "pre-line",
                        lineHeight: 1.5,
                      }}
                    >
                      {fullDescription}
                    </div>
                  </details>

                  <div style={{ marginTop: 12 }}>
                    <ApplyButton
                      apply_url={j.apply_url}
                      job_id={j.job_id}
                      title={j.title}
                      location={j.location}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </main>
  );
}




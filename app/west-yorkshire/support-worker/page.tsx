import fs from "node:fs";
import path from "node:path";

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

type TrainingRow = {
  title: string;
  provider: string;
  description: string;
  link: string;
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

function readTrainingJson(): TrainingRow[] {
  const filePath = path.join(
    process.cwd(),
    "app",
    "training",
    "training.json"
  );

  return JSON.parse(fs.readFileSync(filePath, "utf8"));
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
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n[ \t]+/g, "\n")
    .replace(/[ \t]{2,}/g, " ")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
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

  return fallbackSource.slice(0, 140).trim();
}

function getFullDescription(job: JobRow) {
  const source = job.full_description || job.description || "";
  const cleanedDescription = stripHtml(source);
  const summary = getSummary(job);

  if (!cleanedDescription) return "";

  return removeDuplicateStart(cleanedDescription, summary);
}

function formatSalary(job: JobRow) {
  return job.salary_text ? cleanText(job.salary_text) : "";
}

function getEmployerType(name: string, advertiserType?: string) {
  if (/agency/i.test(advertiserType || "")) return "Agency";
  return "";
}

export default function Page() {
  const jobs = readJobsJson();
  const training = readTrainingJson();

  return (
    <main style={{ maxWidth: 1180, margin: "36px auto", padding: "0 16px" }}>
      <h1
        style={{
          fontSize: 28,
          fontWeight: 800,
          letterSpacing: "-0.02em",
          color: "#111827",
          marginBottom: 8,
        }}
      >
        West Yorkshire Support Worker Roles
      </h1>

      <p
        style={{
          color: "#6b7280",
          marginBottom: 22,
          fontSize: 15,
          lineHeight: 1.5,
        }}
      >
        Updated daily • Latest update: Wed 15th April, PM • Roles across West
        Yorkshire • Apply on employer sites
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "250px 1fr",
          gap: 20,
          alignItems: "start",
        }}
      >
        <aside
          style={{
            paddingTop: 0,
            alignSelf: "start",
            position: "sticky",
            top: 24,
          }}
        >
          <div
            style={{
              fontSize: 15,
              fontWeight: 800,
              marginBottom: 5,
              color: "#111827",
              lineHeight: 1.3,
            }}
          >
            Get started faster
          </div>

          <p
            style={{
              fontSize: 13,
              lineHeight: 1.45,
              color: "#6b7280",
              marginBottom: 10,
            }}
          >
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
                <div
                  style={{
                    fontWeight: 700,
                    fontSize: 14,
                    lineHeight: 1.3,
                    marginBottom: 3,
                    color: "#111827",
                  }}
                >
                  {item.title}
                </div>

                <div
                  style={{
                    fontSize: 12,
                    color: "#6b7280",
                    marginBottom: 6,
                  }}
                >
                  {item.provider}
                </div>

                <div
                  style={{
                    fontSize: 12,
                    color: "#6b7280",
                    lineHeight: 1.45,
                    marginBottom: 8,
                  }}
                >
                  {item.description}
                </div>

                <a
                  href={item.link}
                  target="_blank"
                  rel="noreferrer"
                  style={{
                    display: "inline-block",
                    fontSize: 12,
                    color: "#2563eb",
                    textDecoration: "none",
                    fontWeight: 500,
                  }}
                >
                  Course details
                </a>
              </div>
            ))}
          </div>
        </aside>

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
                  background: "#ffffff",
                  boxShadow: "0 1px 2px rgba(16, 24, 40, 0.04)",
                }}
              >
                <div
                  style={{
                    fontWeight: 800,
                    fontSize: 17,
                    lineHeight: 1.3,
                    color: "#111827",
                    marginBottom: 4,
                  }}
                >
                  {j.title}
                </div>

                <div
                  style={{
                    fontSize: 14,
                    color: "#374151",
                    lineHeight: 1.45,
                    marginBottom: 4,
                  }}
                >
                  {j.company} • {getEmployerType(j.company, j.advertiser_type) || j.advertiser_type || "Company"} • {j.employment_type} • {j.location}
                  {j.location === "Leeds" && (
                    <span
                      style={{
                        marginLeft: 8,
                        padding: "2px 7px",
                        fontSize: 11,
                        fontWeight: 600,
                        borderRadius: 999,
                        background: "#e0f2fe",
                        color: "#0369a1",
                        verticalAlign: "middle",
                      }}
                    >
                      Leeds
                    </span>
                  )}
                </div>

                <div
                  style={{
                    marginBottom: 8,
                    fontSize: 14,
                    fontWeight: 600,
                    color: "#111827",
                  }}
                >
                  {formatSalary(j)}
                </div>

                {summary ? (
                  <div
                    style={{
                      fontSize: 14,
                      color: "#6b7280",
                      marginBottom: 8,
                      lineHeight: 1.45,
                      display: "-webkit-box",
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: "vertical",
                      overflow: "hidden",
                      maxWidth: "94%",
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
                      marginTop: 2,
                      marginBottom: 0,
                      fontWeight: 500,
                    }}
                  >
                    View full job description
                  </summary>

                  <div
                    style={{
                      fontSize: 14,
                      whiteSpace: "pre-line",
                      marginTop: 8,
                      lineHeight: 1.55,
                      color: "#374151",
                    }}
                  >
                    {fullDescription}
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
                    padding: "7px 14px",
                    borderRadius: 8,
                    textDecoration: "none",
                    fontWeight: 700,
                    fontSize: 15,
                    boxShadow: "0 1px 2px rgba(37, 99, 235, 0.18)",
                  }}
                >
                  Apply Now
                </a>
              </div>
            );
          })}
        </div>
      </div>
    </main>
  );
}



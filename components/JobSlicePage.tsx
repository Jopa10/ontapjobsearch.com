import fs from "node:fs";
import path from "node:path";
import TrainingLink from "@/components/traininglink";
import ApplyButton from "@/components/ApplyButton";
import styles from "@/components/JobSlicePage.module.css";

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

type TrainingItem = {
  title: string;
  provider: string;
  description: string;
  link: string;
};

type JobSlicePageProps = {
  jsonPath: string[];
  region: string;
  title: string;
  latestUpdate: string;
  anchorTown?: string;
  introText?: string;
  trainingHeading?: string;
  trainingSubheading?: string;
  trainingItems?: TrainingItem[];
};

function readJobsJson(jsonPath: string[], region: string): JobRow[] {
  const filePath = path.join(process.cwd(), ...jsonPath);

  if (!fs.existsSync(filePath)) return [];

  let parsed: any;
  try {
    parsed = JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return [];
  }

  if (!Array.isArray(parsed) || parsed.length === 0) return [];

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

function truncateAtWord(value: string, maxChars: number) {
  if (value.length <= maxChars) return value;

  const clipped = value.slice(0, maxChars);
  const wordBoundary = clipped.lastIndexOf(" ");
  const safeClip = (wordBoundary > 0 ? clipped.slice(0, wordBoundary) : clipped).trim();
  return `${safeClip}…`;
}

function getSummary(job: JobRow) {
  const summarySource = cleanText(job.summary);
  const fallbackSource = stripHtml(job.full_description || job.description || "");
  const baseSource = summarySource || fallbackSource;
  if (!baseSource) return "";

  const collapsed = baseSource.replace(/\s+/g, " ").trim();
  if (!collapsed) return "";

  const sentenceParts = collapsed.split(/(?<=[.!?])\s+/);
  const firstSentence = sentenceParts[0]?.trim() || "";

  if (firstSentence && firstSentence.length <= 220) {
    return firstSentence;
  }

  return truncateAtWord(collapsed, 220);
}

function getFullDescription(job: JobRow) {
  const source = job.full_description || job.description || "";
  const cleanedDescription = stripHtml(source);

  if (!cleanedDescription) return "";

  return cleanedDescription;
}

const careTraining: TrainingItem[] = [
  {
    title: "Care Certificate Online Course",
    provider: "SCIE",
    description:
      "Self-paced online training covering the Care Certificate standards for new care workers.",
    link: "https://www.scie.org.uk/e-learning/care-certificate/",
  },
  {
    title: "Moving and Handling Online Training",
    provider: "Caredemy",
    description:
      "Online moving and handling training for carers and support workers with downloadable certification.",
    link: "https://caredemy.co.uk/product/safe-moving-handling-online-training-course/",
  },
  {
    title: "Care Certificate Course",
    provider: "CPD Online College",
    description:
      "Flexible online Care Certificate course designed for entry-level health and social care roles.",
    link: "https://cpdonline.co.uk/course/care-certificate/",
  },
  {
    title: "Online Care Certificate Training",
    provider: "ProTrainings UK",
    description:
      "Complete the Care Certificate online with self-paced learning and instant course access.",
    link: "https://www.protrainings.uk/courses/216-care-certificate",
  },
];

export default function JobSlicePage({
  jsonPath,
  region,
  title,
  latestUpdate,
  anchorTown,
  introText,
  trainingHeading,
  trainingSubheading,
  trainingItems,
}: JobSlicePageProps) {
  const jobs = readJobsJson(jsonPath, region);
  const sidebarItems = trainingItems || careTraining;

  return (
    <main style={{ maxWidth: 1180, margin: "36px auto", padding: "0 16px" }}>
      <div className={styles.layout}>
        <aside className={styles.sidebar}>
          <div style={{ fontWeight: 800, marginBottom: 6 }}>
            {trainingHeading || "Get started faster"}
          </div>

          <p style={{ fontSize: 13, color: "#666", marginBottom: 10 }}>
            {trainingSubheading ||
              "Useful online courses commonly requested in care and support roles"}
          </p>

          <div style={{ display: "grid", gap: 8 }}>
            {sidebarItems.map((item, idx) => (
              <div
                key={idx}
                style={{
                  border: "1px solid #e5e7eb",
                  borderRadius: 10,
                  padding: "10px 12px",
                  background: "#f9fafb",
                }}
              >
                <div style={{ fontWeight: 700, fontSize: 14 }}>{item.title}</div>
                <div style={{ fontSize: 12, color: "#666" }}>{item.provider}</div>
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

        <div className={styles.content}>
          <div style={{ marginBottom: 14 }}>
            <h1 style={{ fontSize: 28, fontWeight: 800, marginBottom: 6 }}>
              {title}
            </h1>

            <p style={{ color: "#6b7280", fontSize: 14 }}>
              {introText ||
                `Updated daily • Latest update: ${latestUpdate} • Roles across ${region} • Apply on employer sites`}
            </p>
          </div>

          <div style={{ display: "grid", gap: 10 }}>
            {jobs.length === 0 ? (
              <div
                style={{
                  border: "1px solid #dbe3ee",
                  borderRadius: 12,
                  padding: "14px 16px",
                  background: "#fff",
                  color: "#555",
                }}
              >
                <div style={{ fontWeight: 700, marginBottom: 6 }}>
                  No current suitable jobs
                </div>

                <div style={{ fontSize: 14, color: "#666", lineHeight: 1.5 }}>
                  We’ve paused this page while suitable roles are limited. Please check back soon, or browse current admin, service and customer-service roles.
                </div>
              </div>
            ) : null}

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
                  <div style={{ fontWeight: 800, fontSize: 16 }}>{j.title}</div>

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

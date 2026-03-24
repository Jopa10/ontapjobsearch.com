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

function readJobsJson(): JobRow[] {
  const filePath = path.join(
    process.cwd(),
    "app",
    "yorkshire",
    "support-worker.json"
  );

  const parsed = JSON.parse(fs.readFileSync(filePath, "utf8"));

  return parsed.map((r: any) => ({
    job_id:
      r.job_id ||
      r.display_reference ||
      r.jobdisplayreference ||
      r["/Job/DisplayReference"] ||
      "",
    title:
      r.title ||
      r.jobtitle ||
      r.position ||
      r.jobposition ||
      r["/Job/Position"] ||
      "",
    company:
      r.company ||
      r.companyname ||
      r.advertiser_name ||
      r.jobadvertisername ||
      r["/Job/AdvertiserName"] ||
      "",
    location:
      r.location ||
      r.joblocation ||
      r.area ||
      r.jobarea ||
      r["/Job/Area"] ||
      r["/Job/Location"] ||
      "",
    region: r.region || r["/Job/Location"] || "",
    country: r.country || r.jobcountry || r["/Job/Country"] || "",
    category:
      r.category ||
      r.jobcategory ||
      r.classification ||
      r.jobclassification ||
      r["/Job/Classification"] ||
      "",
    employment_type:
      r.employment_type ||
      r.jobtype ||
      r.jobemploymenttype ||
      r["/Job/EmploymentType"] ||
      "",
    advertiser_type:
      r.advertiser_type ||
      r.advertisertype ||
      r.jobadvertisertype ||
      r["/Job/AdvertiserType"] ||
      "",
    salary_min:
      r.salary_min ||
      r.jobsalaryminimum ||
      r["/Job/SalaryMinimum"] ||
      "",
    salary_max:
      r.salary_max ||
      r.jobsalarymaximum ||
      r["/Job/SalaryMaximum"] ||
      "",
    salary_period:
      r.salary_period ||
      r.jobsalaryperiod ||
      r["/Job/SalaryPeriod"] ||
      "",
    salary_text:
      r.salary_text ||
      r.salaryadditional ||
      r.jobsalaryadditional ||
      r["/Job/SalaryAdditional"] ||
      r.otherdetails ||
      "",
    work_pattern:
      r.work_pattern ||
      r.jobworkhours ||
      r.jobemploymenttype ||
      r["/Job/EmploymentType"] ||
      "",
    posted_date: r.posted_date || r["/Job/PostedDate"] || "",
    closing_date: r.closing_date || r["/Job/ClosingDate"] || "",
    summary: r.summary || "",
    description: r.description || "",
    full_description:
      r.full_description ||
      r.jobdescription ||
      r["/Job/Description"] ||
      r.description ||
      "",
    apply_url:
      r["/Job/ApplicationURL"] ||
      r.jobapplicationurl ||
      r.apply_url ||
      "",
    source: r.source || "",
  }));
}

function decodeMojibake(value: string) {
  return (value || "")
    .replace(/Â£/g, "£")
    .replace(/â€“/g, "–")
    .replace(/â€”/g, "—")
    .replace(/â€˜/g, "‘")
    .replace(/â€™/g, "’")
    .replace(/â€œ/g, "“")
    .replace(/â€/g, "”")
    .replace(/Â/g, "");
}

function cleanText(value: string) {
  return decodeMojibake(value || "").replace(/\s+/g, " ").trim();
}

function stripHtml(html: string) {
  if (!html) return "";

  return decodeMojibake(html)
    .replace(/<img[^>]*>/gi, "")
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<\/p>/gi, "\n\n")
    .replace(/<\/div>/gi, "\n")
    .replace(/<\/li>/gi, "\n")
    .replace(/<li[^>]*>/gi, "• ")
    .replace(/<\/ul>/gi, "\n")
    .replace(/<\/ol>/gi, "\n")
    .replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function escapeRegExp(value: string) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function removeLeadingDuplicate(fullText: string, summaryText: string) {
  if (!fullText || !summaryText) return fullText;

  const cleanSummary = cleanText(summaryText);
  const cleanFull = cleanText(fullText);

  if (cleanFull.startsWith(cleanSummary)) {
    return cleanFull.slice(cleanSummary.length).trim().replace(/^[-–—:,\s]+/, "");
  }

  const summaryRegex = new RegExp("^" + escapeRegExp(cleanSummary) + "[-–—:,\s]*", "i");
  return cleanFull.replace(summaryRegex, "").trim();
}

function getSummaryText(job: JobRow) {
  return cleanText(job.summary || "");
}

function getFullDescription(job: JobRow) {
  const fullText = stripHtml(job.full_description || "");
  const summaryText = getSummaryText(job);
  return removeLeadingDuplicate(fullText, summaryText);
}

function formatNumber(value: string) {
  const num = Number(value);
  if (!Number.isFinite(num)) return "";
  return num.toLocaleString(undefined, {
    maximumFractionDigits: num % 1 === 0 ? 0 : 2,
  });
}

function formatSalary(job: JobRow) {
  const min = Number(job.salary_min);
  const max = Number(job.salary_max);
  const hasMin = Number.isFinite(min) && job.salary_min !== "";
  const hasMax = Number.isFinite(max) && job.salary_max !== "";
  const period = (job.salary_period || "").toLowerCase();

  if (hasMin && hasMax) {
    if (min === max) {
      return `£${formatNumber(job.salary_min)}${period ? ` per ${period}` : ""}`;
    }

    return `£${formatNumber(job.salary_min)}–£${formatNumber(job.salary_max)}${period ? ` per ${period}` : ""}`;
  }

  if (hasMin) {
    return `£${formatNumber(job.salary_min)}${period ? ` per ${period}` : ""}`;
  }

  if (hasMax) {
    return `£${formatNumber(job.salary_max)}${period ? ` per ${period}` : ""}`;
  }

  return cleanText(job.salary_text || "");
}

function getEmployerType(name: string, advertiserType?: string) {
  if (/agency/i.test(advertiserType || "")) return "Agency";
  if (/NHS|Hospital|Trust/i.test(name)) return "NHS";
  if (/Surgery|Medical Centre|GP/i.test(name)) return "GP Practice";
  if (/University/i.test(name)) return "University";
  if (/Council|City Council/i.test(name)) return "Council";
  return "Private";
}

export default function TestJobsPage() {
  const jobs = readJobsJson();

  return (
    <main style={{ maxWidth: 980, margin: "40px auto", padding: "0 16px" }}>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            name: "Yorkshire Support-worker Jobs",
            url: "https://www.ontapjobsearch.com/yorkshire/support-worker",
          }),
        }}
      />

      <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 6 }}>
        Yorkshire Support-worker Roles
      </h1>

      <p
        style={{
          fontSize: 14,
          fontWeight: 600,
          color: "#334155",
          marginBottom: 8,
        }}
      >
        Last updated: 24th March 2026
      </p>

      <p style={{ color: "#555", marginBottom: 20 }}>
        Updated daily • Roles across West Yorkshire for Support-workers • Apply on employer sites
      </p>

      <div style={{ display: "grid", gap: 12 }}>
        {jobs.map((j, idx) => {
          const summaryText = getSummaryText(j);
          const fullDescription = getFullDescription(j);
          const salaryDisplay = formatSalary(j);
          const href = j.apply_url || "#";

          return (
            <div
              key={j.job_id || `${j.title}-${idx}`}
              style={{
                border: "1px solid #e5e7eb",
                borderRadius: 10,
                padding: 14,
              }}
            >
              <div style={{ marginBottom: 4 }}>
                <a
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    fontSize: 18,
                    fontWeight: 700,
                    color: "#111",
                    textDecoration: "none",
                    pointerEvents: j.apply_url ? "auto" : "none",
                    opacity: j.apply_url ? 1 : 0.6,
                  }}
                >
                  {j.title}
                </a>
              </div>

              <div style={{ marginBottom: 4 }}>
                <span
                  style={{
                    fontSize: 12,
                    fontWeight: 600,
                    color: "#475569",
                  }}
                >
                  {getEmployerType(j.company, j.advertiser_type)}
                </span>
              </div>

              <div style={{ fontSize: 14, color: "#555", marginBottom: 2 }}>
                {j.company} • {j.location}
              </div>

              <div style={{ fontSize: 13, color: "#6b7280", marginBottom: 6 }}>
                {j.work_pattern}
              </div>

              {salaryDisplay && (
                <div
                  style={{
                    fontSize: 15,
                    fontWeight: 600,
                    color: "#111",
                    marginBottom: 8,
                  }}
                >
                  {salaryDisplay}
                </div>
              )}

              {summaryText && (
                <div
                  style={{
                    fontSize: 14,
                    color: "#555",
                    marginBottom: 8,
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                  }}
                  title={summaryText}
                >
                  {summaryText}
                </div>
              )}

              {fullDescription && (
                <details style={{ marginBottom: 12 }}>
                  <summary
                    style={{
                      fontSize: 13,
                      color: "#2563eb",
                      cursor: "pointer",
                      marginBottom: 8,
                    }}
                  >
                    View full job description
                  </summary>
                  <div
                    style={{
                      fontSize: 14,
                      color: "#555",
                      lineHeight: 1.6,
                      whiteSpace: "pre-wrap",
                    }}
                  >
                    {fullDescription}
                  </div>
                </details>
              )}

              <div style={{ marginTop: 8 }}>
                <a
                  href={href}
                  target="_blank"
                  rel="noreferrer"
                  style={{
                    display: "inline-block",
                    background: "#2563eb",
                    color: "white",
                    padding: "6px 12px",
                    borderRadius: 6,
                    fontSize: 14,
                    textDecoration: "none",
                    pointerEvents: j.apply_url ? "auto" : "none",
                    opacity: j.apply_url ? 1 : 0.6,
                  }}
                >
                  Apply Now
                </a>
              </div>
            </div>
          );
        })}
      </div>
    </main>
  );
}

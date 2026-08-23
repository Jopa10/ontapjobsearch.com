import Link from "next/link";
import ApplyButton from "@/components/ApplyButton";
import JobFacts from "@/components/JobFacts";
import { sourceLabel } from "@/lib/job-facts";
import { getJobPath } from "@/lib/published-jobs";
import { classifyJobSector, findNthJobSectorIndex } from "@/lib/job-sector";
import SectorBadge from "@/components/SectorBadge";
import SectorSwitchBanner from "@/components/SectorSwitchBanner";
import { Fragment } from "react";

export type DetailedJob = {
  job_id: string;
  title: string;
  company: string;
  advertiser_name: string;
  advertiser_type: string;
  location: string;
  region: string;
  employment_type: string;
  salary_text: string;
  work_pattern: string;
  working_arrangement: string;
  working_arrangement_text: string;
  posted_date: string;
  posted_date_basis: string;
  closing_date: string;
  summary: string;
  description: string;
  full_description: string;
  apply_url: string;
  source: string;
};

type DetailedJobListProps = {
  jobs: DetailedJob[];
  anchorTown?: string;
  sectorFilterEnabled?: boolean;
};

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

function getSummary(job: DetailedJob) {
  const summarySource = cleanText(job.summary);
  const fallbackSource = stripHtml(job.full_description || job.description || "");
  const baseSource = summarySource || fallbackSource;
  if (!baseSource) return "";
  const collapsed = baseSource.replace(/\s+/g, " ").trim();
  if (!collapsed) return "";
  const firstSentence = collapsed.split(/(?<=[.!?])\s+/)[0]?.trim() || "";
  return firstSentence && firstSentence.length <= 220
    ? firstSentence
    : truncateAtWord(collapsed, 220);
}

function externalApplicationSource(source: string) {
  const normalised = source.trim();
  if (!normalised || normalised.toLowerCase() === "jobg8") return "";
  return sourceLabel(normalised);
}

export default function DetailedJobList({
  jobs,
  anchorTown,
  sectorFilterEnabled = false,
}: DetailedJobListProps) {
  const fifthBusinessIndex = findNthJobSectorIndex(jobs, "business", 5);

  return (
    <div style={{ display: "grid", gap: 10 }}>
      {jobs.map((job, index) => {
        const summary = getSummary(job);
        const applicationSource = externalApplicationSource(job.source);
        const sector = classifyJobSector(job);

        return (
          <Fragment key={job.job_id || index}>
            <article
              data-job-sector={sectorFilterEnabled ? sector.sector : undefined}
              style={{
                border: "1px solid #dbe3ee",
                borderRadius: 12,
                padding: "14px 16px",
                background: "#fff",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", flexWrap: "wrap", gap: 7 }}>
                <span style={{ fontWeight: 800, fontSize: 16 }}>{job.title}</span>
                {sectorFilterEnabled && sector.label ? (
                  <SectorBadge label={sector.label} />
                ) : null}
              </div>
              <JobFacts job={job} anchorTown={anchorTown} />

            {summary ? (
              <div style={{ fontSize: 13, color: "#666", marginBottom: 8, lineHeight: 1.5 }}>
                {summary}
              </div>
            ) : null}

            <Link
              href={getJobPath(job.job_id)}
              style={{ fontSize: 13, color: "#2563eb", textDecoration: "none" }}
            >
              View full job description →
            </Link>

            {applicationSource ? (
              <div style={{ marginTop: 8, color: "#6b7280", fontSize: 12, lineHeight: 1.4 }}>
                Original vacancy on {applicationSource}
              </div>
            ) : null}

            <div style={{ marginTop: applicationSource ? 6 : 12 }}>
              <ApplyButton
                apply_url={job.apply_url}
                job_id={job.job_id}
                title={job.title}
                employer={job.company}
                location={job.location}
                region={job.region}
                source={job.source}
              />
            </div>
            </article>
            {sectorFilterEnabled && index === 4 ? (
              <SectorSwitchBanner audience="all" />
            ) : null}
            {sectorFilterEnabled && index === fifthBusinessIndex ? (
              <SectorSwitchBanner audience="business" />
            ) : null}
          </Fragment>
        );
      })}
    </div>
  );
}

import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import ApplyButton from "@/components/ApplyButton";
import WorkingArrangementBadge from "@/components/WorkingArrangementBadge";
import {
  getJobPath,
  getPublishedJob,
  getPublishedJobs,
  type PublishedJob,
} from "@/lib/published-jobs";

const siteUrl = "https://www.ontapjobsearch.com";

type PageProps = {
  params: Promise<{ id: string }>;
};

export const dynamicParams = false;

export function generateStaticParams() {
  return getPublishedJobs().map((job) => ({ id: job.job_id }));
}

function cleanCompanyName(job: PublishedJob) {
  const parts = job.company.split(" - ").map((part) => part.trim()).filter(Boolean);
  if (parts.length > 1 && parts.at(-1) === job.employment_type) parts.pop();
  if (parts.length > 1 && /^(agency|direct employer|employer)$/i.test(parts.at(-1) || "")) {
    parts.pop();
  }
  return parts.join(" - ") || job.company || "confidential";
}

function validPostedDate(value: string) {
  return /^\d{4}-\d{2}-\d{2}(?:T.*)?$/.test(value);
}

function formatClosingDate(value: string) {
  const match = value.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!match) return value;

  const date = new Date(
    Date.UTC(Number(match[1]), Number(match[2]) - 1, Number(match[3]), 12)
  );
  return new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).format(date);
}

function externalSourceLabel(source: string) {
  if (source.toLowerCase() === "nejobs") return "North East Jobs";
  return source;
}

function isExternalSource(source: string) {
  return Boolean(source && source.toLowerCase() !== "jobg8");
}

function hasCompleteDescription(value: string) {
  const normalised = value.replace(/\s+/g, " ").trim();
  return (
    normalised.length >= 200 &&
    !/click apply for full job details|click apply for more details/i.test(normalised)
  );
}

function descriptionHtml(value: string) {
  const escapeHtml = (text: string) =>
    text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");

  return value
    .split(/\n{2,}/)
    .map((paragraph) => `<p>${escapeHtml(paragraph).replace(/\n/g, "<br>")}</p>`)
    .join("");
}

function jobPostingSchema(job: PublishedJob, canonicalUrl: string) {
  if (!validPostedDate(job.posted_date) || !hasCompleteDescription(job.description)) return null;

  const schema: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": "JobPosting",
    title: job.title,
    description: descriptionHtml(job.description),
    datePosted: job.posted_date,
    hiringOrganization: {
      "@type": "Organization",
      name: cleanCompanyName(job),
    },
    jobLocation: {
      "@type": "Place",
      address: {
        "@type": "PostalAddress",
        addressLocality: job.location,
        addressRegion: job.region,
        addressCountry: "GB",
      },
    },
    url: canonicalUrl,
  };

  if (validPostedDate(job.closing_date)) {
    schema.validThrough = `${job.closing_date.slice(0, 10)}T23:59:59+01:00`;
  }

  return schema;
}

function metaDescription(job: PublishedJob) {
  const summary = job.description.replace(/\s+/g, " ").trim();
  const prefix = `${job.title} in ${job.location}. `;
  if (!summary) return `${job.title} in ${job.location}. View the full job description and apply.`;
  return `${prefix}${summary}`.slice(0, 160).trimEnd();
}

function formatSalary(value: string) {
  if (!value) return "";
  if (!/\bper year\b|\bper annum\b/i.test(value)) return value;

  return value.replace(/£\s*(\d[\d,]*(?:\.\d+)?)/g, (match, amount: string) => {
    const numeric = Number(amount.replace(/,/g, ""));
    return Number.isFinite(numeric) ? `£${Math.round(numeric).toLocaleString("en-GB")}` : match;
  });
}

function moreJobsLabel(value: string) {
  const label = value.replace(/\s+(?:roles|jobs)$/i, "").trim();
  return label.toLowerCase() === "browse" ? "View more jobs" : `View more ${label} jobs`;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { id } = await params;
  const job = getPublishedJob(id);
  if (!job) return {};

  const canonicalUrl = `${siteUrl}${getJobPath(job.job_id)}`;
  return {
    title: `${job.title} in ${job.location} | Ontap Job Search`,
    description: metaDescription(job),
    alternates: { canonical: canonicalUrl },
    robots: { index: true, follow: true },
  };
}

export default async function JobPage({ params }: PageProps) {
  const { id } = await params;
  const job = getPublishedJob(id);
  if (!job) notFound();

  const canonicalUrl = `${siteUrl}${getJobPath(job.job_id)}`;
  const schema = jobPostingSchema(job, canonicalUrl);

  return (
    <div style={{ maxWidth: 920, margin: "36px auto", padding: "0 16px" }}>
      {schema ? (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schema).replace(/</g, "\\u003c") }}
        />
      ) : null}

      <nav aria-label="More job listings" style={{ marginBottom: 18 }}>
        <Link
          href={job.slice_path}
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 7,
            color: "#1d4ed8",
            fontSize: 16,
            fontWeight: 700,
            textDecoration: "none",
          }}
        >
          <span>{moreJobsLabel(job.slice_label)}</span>
          <span aria-hidden="true">→</span>
        </Link>
      </nav>

      <article
        style={{
          border: "1px solid #dbe3ee",
          borderRadius: 12,
          padding: "22px 24px",
          background: "#fff",
        }}
      >
        <h1 style={{ fontSize: 28, fontWeight: 800, lineHeight: 1.2, marginBottom: 8 }}>
          {job.title}
        </h1>

        <div style={{ color: "#555", marginBottom: 10 }}>
          {job.company} • {job.location}
          <WorkingArrangementBadge
            workingArrangement={job.working_arrangement}
            workingArrangementText={job.working_arrangement_text}
          />
        </div>

        {job.salary_text ? (
          <div style={{ fontSize: 18, fontWeight: 700, marginBottom: 18 }}>
            {formatSalary(job.salary_text)}
          </div>
        ) : null}

        {job.closing_date ? (
          <div style={{ color: "#555", marginTop: -10, marginBottom: 12 }}>
            Closes {formatClosingDate(job.closing_date)}
          </div>
        ) : null}

        {isExternalSource(job.source) ? (
          <div style={{ color: "#6b7280", fontSize: 14, marginBottom: 18 }}>
            Source: {externalSourceLabel(job.source)}
          </div>
        ) : null}

        <div style={{ marginBottom: 22 }}>
          <ApplyButton
            apply_url={job.apply_url}
            job_id={job.job_id}
            title={job.title}
            employer={job.company}
            location={job.location}
            region={job.region}
            source={job.source}
            slice_path={job.slice_path}
          />
        </div>

        <h2 style={{ fontSize: 21, fontWeight: 800, marginBottom: 12 }}>
          {isExternalSource(job.source) ? "Role overview" : "Job description"}
        </h2>
        <div style={{ whiteSpace: "pre-line", lineHeight: 1.6, color: "#374151" }}>
          {job.description}
        </div>

        {isExternalSource(job.source) ? (
          <div
            style={{
              marginTop: 18,
              padding: "10px 12px",
              borderRadius: 8,
              background: "#f3f4f6",
              color: "#4b5563",
              fontSize: 13,
              lineHeight: 1.5,
            }}
          >
            This is an Ontap-written summary of the vacancy’s factual details.
            Check the original advert for the complete role information and
            application requirements.
          </div>
        ) : null}

        <div style={{ marginTop: 24 }}>
          <ApplyButton
            apply_url={job.apply_url}
            job_id={job.job_id}
            title={job.title}
            employer={job.company}
            location={job.location}
            region={job.region}
            source={job.source}
            slice_path={job.slice_path}
          />
        </div>

        <div style={{ marginTop: 20, paddingTop: 18, borderTop: "1px solid #e5e7eb" }}>
          <Link
            href={job.slice_path}
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 7,
              color: "#1d4ed8",
              fontSize: 16,
              fontWeight: 700,
              textDecoration: "none",
            }}
          >
            <span>{moreJobsLabel(job.slice_label)}</span>
            <span aria-hidden="true">→</span>
          </Link>
        </div>
      </article>
    </div>
  );
}

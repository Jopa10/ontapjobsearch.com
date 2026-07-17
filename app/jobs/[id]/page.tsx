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

  return {
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

      <nav style={{ fontSize: 13, marginBottom: 18, color: "#6b7280" }}>
        <Link href="/browse-jobs" style={{ color: "#2563eb" }}>
          Browse jobs
        </Link>
        <span aria-hidden="true"> / </span>
        <span>{job.title}</span>
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

        <div style={{ marginBottom: 22 }}>
          <ApplyButton
            apply_url={job.apply_url}
            job_id={job.job_id}
            title={job.title}
            location={job.location}
          />
        </div>

        <h2 style={{ fontSize: 21, fontWeight: 800, marginBottom: 12 }}>Job description</h2>
        <div style={{ whiteSpace: "pre-line", lineHeight: 1.6, color: "#374151" }}>
          {job.description}
        </div>

        <div style={{ marginTop: 24 }}>
          <ApplyButton
            apply_url={job.apply_url}
            job_id={job.job_id}
            title={job.title}
            location={job.location}
          />
        </div>
      </article>
    </div>
  );
}

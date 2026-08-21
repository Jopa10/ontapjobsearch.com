import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import ApplyButton from "@/components/ApplyButton";
import JobDescription from "@/components/JobDescription";
import JobFacts from "@/components/JobFacts";
import MoreJobsNearby from "@/components/MoreJobsNearby";
import TransferableFitCard from "@/components/TransferableFitCard";
import { getActiveCityPageForJob } from "@/lib/city-page-data";
import { cleanEmployerName, sourceLabel } from "@/lib/job-facts";
import {
  getJobPath,
  getPublishedJob,
  getPublishedJobs,
  type PublishedJob,
} from "@/lib/published-jobs";
import { getRelatedJobs } from "@/lib/related-jobs";
import { getTransferableFit } from "@/lib/transferable-fit";
import styles from "./job-page.module.css";

const siteUrl = "https://www.ontapjobsearch.com";

type PageProps = {
  params: Promise<{ id: string }>;
};

type ListingLink = {
  href: string;
  label: string;
};

export const dynamicParams = false;

export function generateStaticParams() {
  return getPublishedJobs().map((job) => ({ id: job.job_id }));
}

function validPostedDate(value: string) {
  return /^\d{4}-\d{2}-\d{2}(?:T.*)?$/.test(value);
}

function validClosingDateTime(value: string) {
  return (
    /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})$/.test(value) &&
    !Number.isNaN(Date.parse(value))
  );
}

function isExternalSource(source: string) {
  return Boolean(source && source.toLowerCase() !== "jobg8");
}

function isNhsSource(source: string) {
  return source.trim().toLowerCase() === "nhs jobs";
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
  if (!hasCompleteDescription(job.description)) return null;

  const schema: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": "JobPosting",
    title: job.title,
    description: descriptionHtml(job.description),
    hiringOrganization: {
      "@type": "Organization",
      name: cleanEmployerName(job) || "Confidential",
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

  const sourceDateIsReliable =
    job.posted_date_basis === "source" ||
    (job.source.toLowerCase() === "nejobs" && !job.posted_date_basis);
  if (sourceDateIsReliable && validPostedDate(job.posted_date)) {
    schema.datePosted = job.posted_date;
  }

  if (validClosingDateTime(job.closing_datetime)) {
    schema.validThrough = job.closing_datetime;
  } else if (validPostedDate(job.closing_date)) {
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

function moreJobsLabel(value: string) {
  const label = value.replace(/\s+(?:roles|jobs)$/i, "").trim();
  return label.toLowerCase() === "browse" ? "View more jobs" : `View more ${label} jobs`;
}

function ListingLinks({
  primary,
  secondary,
}: {
  primary: ListingLink;
  secondary?: ListingLink;
}) {
  const links = [primary, secondary].filter((link): link is ListingLink => Boolean(link));

  return (
    <div style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: "10px 20px" }}>
      {links.map((link, index) => (
        <Link
          key={link.href}
          href={link.href}
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 7,
            color: index === 0 ? "#1d4ed8" : "#475569",
            fontSize: index === 0 ? 16 : 14,
            fontWeight: index === 0 ? 700 : 600,
            textDecoration: "none",
          }}
        >
          <span>{link.label}</span>
          <span aria-hidden="true">→</span>
        </Link>
      ))}
    </div>
  );
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
  const applicationSource = isExternalSource(job.source) ? sourceLabel(job.source) : "";
  const transferableFit = getTransferableFit(job.job_id);
  const publishedJobs = getPublishedJobs();
  const cityPage = getActiveCityPageForJob(job.job_id);
  const cityJobIds = new Set(
    cityPage?.jobs.flatMap((cityJob) =>
      typeof cityJob.job_id === "string" ? [cityJob.job_id] : []
    ) ?? []
  );
  const relatedPool = cityPage
    ? publishedJobs.filter((candidate) => cityJobIds.has(candidate.job_id))
    : publishedJobs;
  const relatedJobs = getRelatedJobs(job, relatedPool);
  const regionalJobsLabel = moreJobsLabel(job.slice_label);
  const cityJobsLabel = cityPage
    ? moreJobsLabel(cityPage.definition.listingLabel)
    : "";
  const primaryListing: ListingLink = cityPage
    ? { href: cityPage.definition.route, label: cityJobsLabel }
    : { href: job.slice_path, label: regionalJobsLabel };
  const secondaryListing: ListingLink | undefined = cityPage
    ? { href: job.slice_path, label: regionalJobsLabel }
    : undefined;

  return (
    <div className={styles.page}>
      {schema ? (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schema).replace(/</g, "\\u003c") }}
        />
      ) : null}

      <nav aria-label="More job listings" style={{ marginBottom: 18 }}>
        <ListingLinks primary={primaryListing} secondary={secondaryListing} />
      </nav>

      <div
        className={`${styles.contentGrid} ${
          relatedJobs.length || transferableFit ? "" : styles.singleColumn
        }`}
      >
        <article className={styles.article}>
          <h1 style={{ fontSize: 28, fontWeight: 800, lineHeight: 1.2, marginBottom: 8 }}>
            {job.title}
          </h1>

          <JobFacts job={job} variant="detail" />

          {applicationSource ? (
            <div
              style={{
                color: "#6b7280",
                fontSize: 13,
                lineHeight: 1.4,
                marginTop: -8,
                marginBottom: 7,
              }}
            >
              Original vacancy on {applicationSource}
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

          {transferableFit ? (
            <div className={styles.mobileTransferableFit}>
              <TransferableFitCard
                fit={transferableFit}
                jobId={job.job_id}
                title={job.title}
                employer={job.company}
                location={job.location}
                region={job.region}
                source={job.source}
                slicePath={job.slice_path}
                placement="mobile"
              />
            </div>
          ) : null}

          <h2 style={{ fontSize: 21, fontWeight: 800, marginBottom: 12 }}>
            {isExternalSource(job.source) ? "Role overview" : "Job description"}
          </h2>
          <JobDescription value={job.description} source={job.source} />

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
              {isNhsSource(job.source) ? (
                <>
                  This overview is taken from the public NHS Jobs advert. Check the
                  original advert for the complete role information, person specification
                  and application requirements.
                </>
              ) : (
                <>
                  This is an Ontap-written summary of the vacancy’s factual details.
                  Check the original advert for the complete role information and
                  application requirements.
                </>
              )}
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
            <ListingLinks primary={primaryListing} secondary={secondaryListing} />
          </div>
        </article>

        {relatedJobs.length || transferableFit ? (
          <aside className={styles.sidebar} aria-label="Related job information">
            {relatedJobs.length ? (
              <MoreJobsNearby
                jobs={relatedJobs}
                allJobsPath={primaryListing.href}
                allJobsLabel={primaryListing.label}
                intro={
                  cityPage
                    ? `Other current roles on the ${cityPage.definition.listingLabel} page.`
                    : undefined
                }
                secondaryAllJobsPath={secondaryListing?.href}
                secondaryAllJobsLabel={secondaryListing?.label}
              />
            ) : null}

            {transferableFit ? (
              <div
                className={styles.desktopTransferableFit}
                style={{ marginTop: relatedJobs.length ? 16 : 0 }}
              >
                <TransferableFitCard
                  fit={transferableFit}
                  jobId={job.job_id}
                  title={job.title}
                  employer={job.company}
                  location={job.location}
                  region={job.region}
                  source={job.source}
                  slicePath={job.slice_path}
                  placement="desktop"
                />
              </div>
            ) : null}
          </aside>
        ) : null}
      </div>
    </div>
  );
}

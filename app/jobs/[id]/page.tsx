import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import ApplyButton from "@/components/ApplyButton";
import JobDescription from "@/components/JobDescription";
import JobFacts from "@/components/JobFacts";
import MoreJobsNearby from "@/components/MoreJobsNearby";
import TransferableFitCard from "@/components/TransferableFitCard";
import { getActiveCityPageForJob } from "@/lib/city-page-data";
import { sourceLabel } from "@/lib/job-facts";
import { buildJobPostingSchema } from "@/lib/job-posting-schema";
import {
  getJobPath,
  getPublishedJob,
  getPublishedJobs,
  type PublishedJob,
} from "@/lib/published-jobs";
import { getDiscoveryRecommendations } from "@/lib/discovery-recommendations";
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

// Keep published jobs pre-rendered while allowing removed URLs to reach the useful segment 404.\nexport const dynamicParams = true;

export function generateStaticParams() {
  return getPublishedJobs().map((job) => ({ id: job.job_id }));
}

function isExternalSource(source: string) {
  return Boolean(source && source.toLowerCase() !== "jobg8");
}

function isNhsSource(source: string) {
  return source.trim().toLowerCase() === "nhs jobs";
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
  const schema = buildJobPostingSchema(job, canonicalUrl);
  const applicationSource = isExternalSource(job.source) ? sourceLabel(job.source) : "";
  const transferableFit = getTransferableFit(job.job_id);
  const publishedJobs = getPublishedJobs();
  const cityPage = getActiveCityPageForJob(job.job_id);
  const discoveryJobs = getDiscoveryRecommendations(job, publishedJobs);
  const regionalJobsLabel = moreJobsLabel(job.slice_label);
  const cityJobsLabel = cityPage
    ? moreJobsLabel(cityPage.definition.listingLabel)
    : "";
  const discoveryFallback: ListingLink = { href: job.slice_path, label: regionalJobsLabel };
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

      <div className={styles.contentGrid}>
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

        <aside className={styles.sidebar} aria-label="Related job information">
          <MoreJobsNearby
            jobs={discoveryJobs}
            allJobsPath={discoveryJobs.length ? primaryListing.href : discoveryFallback.href}
            allJobsLabel={discoveryJobs.length ? primaryListing.label : discoveryFallback.label}
            secondaryAllJobsPath={discoveryJobs.length ? secondaryListing?.href : undefined}
            secondaryAllJobsLabel={discoveryJobs.length ? secondaryListing?.label : undefined}
          />

          {transferableFit ? (
            <div
              className={styles.desktopTransferableFit}
              style={{ marginTop: 16 }}
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
      </div>
    </div>
  );
}

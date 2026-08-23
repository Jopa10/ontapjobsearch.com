import fs from "node:fs";
import path from "node:path";
import Link from "next/link";
import DetailedJobList from "@/components/DetailedJobList";
import JobViewSwitcher from "@/components/JobViewSwitcher";
import QuickJobList from "@/components/QuickJobList";
import { orderJobsForDisplay } from "@/lib/job-display-order";
import { normaliseJobTitle } from "@/lib/job-title";
import TrainingLink from "@/components/traininglink";
import styles from "@/components/JobSlicePage.module.css";
import { classifyJobSector } from "@/lib/job-sector";

type JobRow = {
  job_id: string;
  title: string;
  company: string;
  advertiser_name: string;
  advertiser_type: string;
  location: string;
  region: string;
  country: string;
  category: string;
  employment_type: string;
  salary_min: string;
  salary_max: string;
  salary_period: string;
  salary_text: string;
  work_pattern: string;
  working_arrangement: string;
  working_arrangement_text: string;
  working_arrangement_evidence: string;
  posted_date: string;
  posted_date_basis: string;
  closing_date: string;
  summary: string;
  description: string;
  full_description: string;
  apply_url: string;
  source: string;
  hc_tier: string;
  switchability: string;
  at_a_glance_attributes: string[];
};

type TrainingItem = {
  title: string;
  provider: string;
  description: string;
  link: string;
};

type RelatedPage = {
  href: string;
  prompt: string;
  label: string;
};

type BrowseLinks = {
  heading: string;
  intro?: string;
  compact?: boolean;
  links: Array<{
    href: string;
    label: string;
  }>;
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
  jobFilter?: (job: JobRow) => boolean;
  relatedPage?: RelatedPage;
  browseLinks?: BrowseLinks;
  sectorFilterEnabled?: boolean;
};

function stringList(value: unknown): string[] {
  if (!Array.isArray(value)) return [];
  return value
    .filter((item): item is string => typeof item === "string")
    .map((item) => item.trim())
    .filter(Boolean);
}

function readJobsJson(jsonPath: string[], region: string): JobRow[] {
  const filePath = path.join(process.cwd(), ...jsonPath);
  if (!fs.existsSync(filePath)) return [];

  let parsed: unknown;
  try {
    parsed = JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return [];
  }

  if (!Array.isArray(parsed) || parsed.length === 0) return [];

  return parsed
    .filter((row): row is Record<string, unknown> => Boolean(row && typeof row === "object"))
    .map((row) => ({
      job_id: String(row.job_id || row["/Job/DisplayReference"] || ""),
      title: normaliseJobTitle(String(row.title || row["/Job/Position"] || "")),
      company: String(row.company || row["/Job/AdvertiserName"] || ""),
      advertiser_name: String(row.advertiser_name || row["/Job/AdvertiserName"] || ""),
      advertiser_type: String(row.advertiser_type || row["/Job/AdvertiserType"] || ""),
      location: String(row.location || row["/Job/Area"] || ""),
      region: String(row.region || region),
      country: String(row.country || "UK"),
      category: String(row.category || ""),
      employment_type: String(row.employment_type || row["/Job/EmploymentType"] || ""),
      salary_min: String(row.salary_min || row["/Job/SalaryMinimum"] || ""),
      salary_max: String(row.salary_max || row["/Job/SalaryMaximum"] || ""),
      salary_period: String(row.salary_period || row["/Job/SalaryPeriod"] || ""),
      salary_text: String(row.salary_text || row["/Job/SalaryAdditional"] || ""),
      work_pattern: String(row.work_pattern || row["/Job/WorkHours"] || ""),
      working_arrangement: String(row.working_arrangement || ""),
      working_arrangement_text: String(row.working_arrangement_text || ""),
      working_arrangement_evidence: String(row.working_arrangement_evidence || ""),
      posted_date: String(row.posted_date || ""),
      posted_date_basis: String(row.posted_date_basis || ""),
      closing_date: String(row.closing_date || ""),
      summary: String(row.summary || ""),
      description: String(row.description || ""),
      full_description: String(
        row.full_description || row.description || row["/Job/Description"] || ""
      ),
      apply_url: String(row.apply_url || row["/Job/ApplicationURL"] || ""),
      source: String(row.source || "JobG8"),
      hc_tier: String(row.hc_tier || ""),
      switchability: String(row.switchability || ""),
      at_a_glance_attributes: stringList(row.at_a_glance_attributes),
    }));
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

function RelatedPageLink({ relatedPage }: { relatedPage: RelatedPage }) {
  return (
    <div className={styles.relatedPanel}>
      <div className={styles.relatedCopy}>
        <div className={styles.relatedEyebrow}>More jobs nearby</div>
        <p className={styles.relatedPrompt}>{relatedPage.prompt}</p>
      </div>
      <Link href={relatedPage.href} className={styles.relatedLink}>
        {relatedPage.label} →
      </Link>
    </div>
  );
}

function BrowseLinksPanel({ browseLinks }: { browseLinks: BrowseLinks }) {
  if (!browseLinks.links.length) return null;

  return (
    <nav
      className={`${styles.browsePanel} ${browseLinks.compact ? styles.compactBrowsePanel : ""}`}
      aria-label={browseLinks.heading}
    >
      <div>
        <div
          className={
            browseLinks.compact ? styles.compactBrowseHeading : styles.relatedEyebrow
          }
        >
          {browseLinks.heading}
        </div>
        {browseLinks.intro && !browseLinks.compact ? (
          <p className={styles.relatedPrompt}>{browseLinks.intro}</p>
        ) : null}
      </div>
      <div className={styles.browseLinkList}>
        {browseLinks.links.map((link) => (
          <Link key={link.href} href={link.href} className={styles.relatedLink}>
            {link.label} →
          </Link>
        ))}
      </div>
    </nav>
  );
}

function EmptyJobs() {
  return (
    <div
      style={{
        border: "1px solid #dbe3ee",
        borderRadius: 12,
        padding: "14px 16px",
        background: "#fff",
        color: "#555",
      }}
    >
      <div style={{ fontWeight: 700, marginBottom: 6 }}>No current suitable jobs</div>
      <div style={{ fontSize: 14, color: "#666", lineHeight: 1.5 }}>
        We’ve paused this page while suitable roles are limited. Please check back soon,
        or browse current admin, service and customer-service roles.
      </div>
    </div>
  );
}

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
  jobFilter,
  relatedPage,
  browseLinks,
  sectorFilterEnabled = false,
}: JobSlicePageProps) {
  const allJobs = readJobsJson(jsonPath, region);
  const filteredJobs = jobFilter ? allJobs.filter(jobFilter) : allJobs;
  const jobs = orderJobsForDisplay(filteredJobs);
  const sidebarItems = trainingItems || careTraining;
  const publicJobCount = jobs.filter(
    (job) => classifyJobSector(job).sector === "public"
  ).length;
  const sectorCounts = {
    all: jobs.length,
    business: jobs.length - publicJobCount,
    public: publicJobCount,
  };

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
            {sidebarItems.map((item) => (
              <div
                key={`${item.provider}-${item.title}`}
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
            <h1 style={{ fontSize: 28, fontWeight: 800, marginBottom: 6 }}>{title}</h1>
            <p style={{ color: "#6b7280", fontSize: 14 }}>
              {introText ||
                `Updated daily • Latest update: ${latestUpdate} • Roles across ${region} • Apply on employer sites`}
            </p>
          </div>

          {browseLinks ? (
            <div style={{ marginBottom: 12 }}>
              <BrowseLinksPanel browseLinks={browseLinks} />
            </div>
          ) : null}

          {relatedPage ? (
            <div style={{ marginBottom: 12 }}>
              <RelatedPageLink relatedPage={relatedPage} />
            </div>
          ) : null}

          {jobs.length ? (
            <JobViewSwitcher
              sectorFilterEnabled={sectorFilterEnabled}
              sectorCounts={sectorCounts}
              quickView={
                <QuickJobList jobs={jobs} sectorFilterEnabled={sectorFilterEnabled} />
              }
              detailedView={
                <DetailedJobList
                  jobs={jobs}
                  anchorTown={anchorTown}
                  sectorFilterEnabled={sectorFilterEnabled}
                />
              }
            />
          ) : (
            <EmptyJobs />
          )}

          {relatedPage ? (
            <div style={{ marginTop: 14 }}>
              <RelatedPageLink relatedPage={relatedPage} />
            </div>
          ) : null}
        </div>
      </div>
    </main>
  );
}

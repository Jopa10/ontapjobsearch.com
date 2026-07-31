import type { Metadata } from "next";
import Link from "next/link";
import AtAGlance from "@/components/AtAGlance";
import JobFacts from "@/components/JobFacts";
import { getAtAGlanceAttributes } from "@/lib/at-a-glance-preview";
import { getJobPath, getPublishedJobs } from "@/lib/published-jobs";

export const metadata: Metadata = {
  title: "At a glance preview | Ontap Job Search",
  robots: { index: false, follow: false },
};

export default function AtAGlancePreviewPage() {
  const jobs = getPublishedJobs()
    .map((job) => ({
      job,
      attributes: getAtAGlanceAttributes(job.job_id),
    }))
    .filter(({ attributes }) => attributes.length >= 2)
    .sort((left, right) => {
      const categoryOrder = left.job.category.localeCompare(right.job.category);
      if (categoryOrder) return categoryOrder;
      const regionOrder = left.job.region.localeCompare(right.job.region);
      if (regionOrder) return regionOrder;
      return left.job.title.localeCompare(right.job.title);
    });

  return (
    <main style={{ maxWidth: 820, margin: "36px auto", padding: "0 16px" }}>
      <div style={{ marginBottom: 18 }}>
        <div
          style={{
            display: "inline-block",
            padding: "3px 8px",
            borderRadius: 999,
            background: "#f3f4f6",
            color: "#4b5563",
            fontSize: 12,
            fontWeight: 700,
            marginBottom: 8,
          }}
        >
          Review preview — not live
        </div>
        <h1 style={{ fontSize: 28, fontWeight: 800, marginBottom: 6 }}>
          Compact “At a glance” job cards
        </h1>
        <p style={{ color: "#6b7280", fontSize: 14, lineHeight: 1.5 }}>
          {jobs.length} current vacancies have enough direct duty evidence to
          show this line. Other vacancies would simply omit it.
        </p>
      </div>

      <div style={{ display: "grid", gap: 10 }}>
        {jobs.map(({ job, attributes }) => (
          <article
            key={job.job_id}
            style={{
              border: "1px solid #dbe3ee",
              borderRadius: 12,
              padding: "14px 16px",
              background: "#fff",
            }}
          >
            <div style={{ fontWeight: 800, fontSize: 16 }}>{job.title}</div>

            <JobFacts job={job} />

            <AtAGlance attributes={attributes} />

            <Link
              href={getJobPath(job.job_id)}
              style={{
                fontSize: 13,
                color: "#2563eb",
                textDecoration: "none",
              }}
            >
              View full job description →
            </Link>

            <div style={{ marginTop: 12 }}>
              <span
                style={{
                  display: "inline-block",
                  border: 0,
                  borderRadius: 8,
                  padding: "9px 14px",
                  background: "#111827",
                  color: "#fff",
                  fontSize: 14,
                  fontWeight: 700,
                }}
              >
                Apply for this job
              </span>
            </div>
          </article>
        ))}
      </div>
    </main>
  );
}

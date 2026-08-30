import Link from "next/link";
import { getJobPath, getPublishedJobs } from "@/lib/published-jobs";
import styles from "./job-page.module.css";

export default function JobNotFound() {
  const currentJobs = getPublishedJobs().slice(0, 6);

  return (
    <div className={styles.page}>
      <div className={`${styles.contentGrid} ${styles.singleColumn}`}>
        <article className={styles.article}>
          <p style={{ color: "#64748b", fontSize: 14, fontWeight: 700, marginBottom: 8 }}>
            JOB NO LONGER AVAILABLE
          </p>
          <h1 style={{ fontSize: 28, fontWeight: 800, lineHeight: 1.2, marginBottom: 12 }}>
            This job has expired
          </h1>
          <p style={{ color: "#475569", lineHeight: 1.6, marginBottom: 20 }}>
            The vacancy has been removed, but Ontap has other current jobs you can view now.
          </p>

          <div style={{ display: "flex", flexWrap: "wrap", gap: 12, marginBottom: 28 }}>
            <Link
              href="/browse-jobs"
              style={{
                background: "#1d4ed8",
                borderRadius: 8,
                color: "#ffffff",
                fontWeight: 700,
                padding: "11px 16px",
                textDecoration: "none",
              }}
            >
              Browse current jobs
            </Link>
            <Link
              href="/"
              style={{
                border: "1px solid #cbd5e1",
                borderRadius: 8,
                color: "#334155",
                fontWeight: 700,
                padding: "10px 16px",
                textDecoration: "none",
              }}
            >
              Return home
            </Link>
          </div>

          {currentJobs.length ? (
            <section aria-labelledby="current-jobs-heading">
              <h2 id="current-jobs-heading" style={{ fontSize: 21, fontWeight: 800, marginBottom: 12 }}>
                Current jobs on Ontap
              </h2>
              <ul style={{ display: "grid", gap: 10, listStyle: "none", margin: 0, padding: 0 }}>
                {currentJobs.map((job) => (
                  <li key={job.job_id} style={{ borderTop: "1px solid #e2e8f0", paddingTop: 10 }}>
                    <Link
                      href={getJobPath(job.job_id)}
                      style={{ color: "#1d4ed8", fontWeight: 700, textDecoration: "none" }}
                    >
                      {job.title}
                    </Link>
                    <div style={{ color: "#64748b", fontSize: 14, marginTop: 3 }}>
                      {job.location}
                    </div>
                  </li>
                ))}
              </ul>
            </section>
          ) : null}
        </article>
      </div>
    </div>
  );
}

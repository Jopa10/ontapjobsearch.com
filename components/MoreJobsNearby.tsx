import Link from "next/link";
import styles from "@/components/MoreJobsNearby.module.css";
import { formatSalary } from "@/lib/job-facts";
import { getJobPath, type PublishedJob } from "@/lib/published-jobs";

type MoreJobsNearbyProps = {
  jobs: Array<PublishedJob & { distance_miles?: number }>;
  allJobsPath: string;
  allJobsLabel: string;
  intro?: string;
  heading?: string;
  emptyMessage?: string;
  secondaryAllJobsPath?: string;
  secondaryAllJobsLabel?: string;
};

export default function MoreJobsNearby({
  jobs,
  allJobsPath,
  allJobsLabel,
  intro = "Approved role matches within 15 straight-line miles. Locations shown are where the jobs are based.",
  heading = "Suitable jobs nearby",
  emptyMessage = "No approved close match is available at the moment. Browse the relevant regional jobs instead.",
  secondaryAllJobsPath,
  secondaryAllJobsLabel,
}: MoreJobsNearbyProps) {
  return (
    <section className={styles.panel}>
      <h2 className={styles.heading}>{heading}</h2>
      <p className={styles.intro}>{intro}</p>

      {jobs.length ? (
        <ul className={styles.list}>
          {jobs.map((job) => {
            const salary = formatSalary(job.salary_text) || "Salary not stated";
            const distance = typeof job.distance_miles === "number"
              ? job.distance_miles < 0.05
                ? "Same town"
                : `${job.distance_miles.toFixed(1)} miles away`
              : "";
            const terms = [salary, job.employment_type, distance].filter(Boolean).join(" · ");

            return (
              <li key={job.job_id} className={styles.item}>
                <Link
                  href={getJobPath(job.job_id)}
                  className={styles.jobLink}
                  aria-label={`${job.location}: ${job.title}. View full job details`}
                >
                  <span className={styles.roleLine}>
                    <span className={styles.location}>
                      {job.location || "Location not stated"}
                    </span>
                    <span aria-hidden="true">—</span>
                    <span className={styles.title}>{job.title}</span>
                  </span>
                  <span className={styles.factLine}>
                    <span>{terms}</span>
                    <span className={styles.arrow} aria-hidden="true">→</span>
                  </span>
                </Link>
              </li>
            );
          })}
        </ul>
      ) : (
        <p className={styles.intro}>{emptyMessage}</p>
      )}

      <Link href={allJobsPath} className={styles.allJobsLink}>
        <span>{allJobsLabel}</span>
        <span aria-hidden="true">→</span>
      </Link>

      {secondaryAllJobsPath && secondaryAllJobsLabel ? (
        <Link
          href={secondaryAllJobsPath}
          className={`${styles.allJobsLink} ${styles.secondaryAllJobsLink}`}
        >
          <span>{secondaryAllJobsLabel}</span>
          <span aria-hidden="true">→</span>
        </Link>
      ) : null}
    </section>
  );
}

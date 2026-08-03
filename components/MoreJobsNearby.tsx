import Link from "next/link";
import styles from "@/components/MoreJobsNearby.module.css";
import { formatSalary } from "@/lib/job-facts";
import { getJobPath, type PublishedJob } from "@/lib/published-jobs";

type MoreJobsNearbyProps = {
  jobs: PublishedJob[];
  allJobsPath: string;
  allJobsLabel: string;
  intro?: string;
  secondaryAllJobsPath?: string;
  secondaryAllJobsLabel?: string;
};

export default function MoreJobsNearby({
  jobs,
  allJobsPath,
  allJobsLabel,
  intro = "Other current roles in this area and category.",
  secondaryAllJobsPath,
  secondaryAllJobsLabel,
}: MoreJobsNearbyProps) {
  return (
    <section className={styles.panel}>
      <h2 className={styles.heading}>More jobs nearby</h2>
      <p className={styles.intro}>{intro}</p>

      <ul className={styles.list}>
        {jobs.map((job) => {
          const salary = formatSalary(job.salary_text) || "Salary not stated";
          const terms = [salary, job.employment_type].filter(Boolean).join(" · ");

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

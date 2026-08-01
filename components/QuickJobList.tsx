import Link from "next/link";
import {
  cleanEmployerName,
  employerFactLabel,
  formatSalary,
} from "@/lib/job-facts";
import { getJobPath } from "@/lib/published-jobs";
import styles from "@/components/QuickJobList.module.css";

export type QuickJob = {
  job_id: string;
  title: string;
  company: string;
  advertiser_name: string;
  advertiser_type: string;
  location: string;
  employment_type: string;
  salary_text: string;
  at_a_glance_attributes: string[];
};

type QuickJobListProps = {
  jobs: QuickJob[];
};

export default function QuickJobList({ jobs }: QuickJobListProps) {
  return (
    <div className={styles.shell}>
      {jobs.map((job) => {
        const employer = cleanEmployerName(job);
        const employerLabel = employerFactLabel(job);
        const salary = formatSalary(job.salary_text) || "Salary not stated";
        const terms = [salary, job.employment_type].filter(Boolean).join(" · ");
        const attributes = job.at_a_glance_attributes.slice(0, 4);

        return (
          <Link
            key={job.job_id}
            href={getJobPath(job.job_id)}
            className={styles.row}
            aria-label={`${job.location}: ${job.title}. View full job details`}
          >
            <span className={styles.topLine}>
              <span className={styles.location}>{job.location || "Location not stated"}</span>
              <span className={styles.dash} aria-hidden="true">—</span>
              <span className={styles.title}>{job.title}</span>
              <span className={styles.terms}>{terms}</span>
              <span className={styles.arrow} aria-hidden="true">→</span>
            </span>

            <span className={styles.bottomLine}>
              <span className={styles.employer}>
                {employer ? `${employerLabel}: ${employer}` : "Employer not stated"}
              </span>
              {attributes.length ? (
                <span className={styles.tags}>
                  {attributes.map((attribute) => (
                    <span className={styles.tag} key={attribute}>
                      {attribute}
                    </span>
                  ))}
                </span>
              ) : null}
            </span>
          </Link>
        );
      })}
    </div>
  );
}

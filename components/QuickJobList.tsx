import {
  cleanEmployerName,
  employerFactLabel,
  formatSalary,
} from "@/lib/job-facts";
import { getAtAGlanceAttributes } from "@/lib/at-a-glance-preview";
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

function displayLocation(location: string) {
  const value = location.trim();
  if (/\bwideopen\b/i.test(value)) return "Wideopen";
  if (/^south tyneside council$/i.test(value)) return "South Tyneside";
  return value || "Location not stated";
}

function displayTitle(title: string) {
  return title
    .replace(/^[A-Z]{2,}\d+(?:\/\d+)?\s*-\s*/i, "")
    .trim();
}

export default function QuickJobList({ jobs }: QuickJobListProps) {
  return (
    <div className={styles.shell}>
      {jobs.map((job) => {
        const employer = cleanEmployerName(job);
        const employerLabel = employerFactLabel(job);
        const salary = formatSalary(job.salary_text) || "Salary not stated";
        const terms = [salary, job.employment_type].filter(Boolean).join(" · ");
        const location = displayLocation(job.location);
        const title = displayTitle(job.title);
        const attributes = (
          job.at_a_glance_attributes.length
            ? job.at_a_glance_attributes
            : getAtAGlanceAttributes(job.job_id)
        ).slice(0, 4);

        return (
          <a
            key={job.job_id}
            href={getJobPath(job.job_id)}
            className={styles.row}
            aria-label={`${location}: ${title}. View full job details`}
          >
            <span className={styles.topLine}>
              <span className={styles.location} title={job.location}>
                {location}
              </span>
              <span className={styles.dash} aria-hidden="true">—</span>
              <span className={styles.title} title={job.title}>
                {title}
              </span>
              <span className={styles.terms} title={terms}>
                {terms}
              </span>
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
          </a>
        );
      })}
    </div>
  );
}

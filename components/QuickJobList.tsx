import {
  cleanEmployerName,
  employerFactLabel,
  formatSalary,
} from "@/lib/job-facts";
import { getJobPath } from "@/lib/published-jobs";
import { classifyJobSector, findNthJobSectorIndex } from "@/lib/job-sector";
import SectorBadge from "@/components/SectorBadge";
import SectorSwitchBanner from "@/components/SectorSwitchBanner";
import ResultsJobLink from "@/components/ResultsJobLink";
import { Fragment } from "react";
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
  source: string;
  summary?: string;
  description?: string;
  full_description?: string;
};

type QuickJobListProps = {
  jobs: QuickJob[];
  sectorFilterEnabled?: boolean;
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

export default function QuickJobList({
  jobs,
  sectorFilterEnabled = false,
}: QuickJobListProps) {
  const fifthBusinessIndex = findNthJobSectorIndex(jobs, "business", 5);

  return (
    <div className={styles.shell}>
      {jobs.map((job, index) => {
        const employer = cleanEmployerName(job);
        const employerLabel = employerFactLabel(job);
        const salary = formatSalary(job.salary_text) || "Salary not stated";
        const terms = [salary, job.employment_type].filter(Boolean).join(" · ");
        const location = displayLocation(job.location);
        const title = displayTitle(job.title);
        const sector = classifyJobSector(job);

        return (
          <Fragment key={job.job_id}>
            <ResultsJobLink
              href={getJobPath(job.job_id)}
              className={styles.row}
              data-job-sector={sectorFilterEnabled ? sector.sector : undefined}
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
                {sectorFilterEnabled && sector.label ? (
                  <span className={styles.tags}>
                    <SectorBadge label={sector.label} />
                  </span>
                ) : null}
              </span>
            </ResultsJobLink>
            {sectorFilterEnabled && index === 4 ? (
              <SectorSwitchBanner audience="all" />
            ) : null}
            {sectorFilterEnabled && index === fifthBusinessIndex ? (
              <SectorSwitchBanner audience="business" />
            ) : null}
          </Fragment>
        );
      })}
    </div>
  );
}

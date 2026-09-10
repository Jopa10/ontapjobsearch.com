"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import styles from "@/components/MoreJobsNearby.module.css";
import { savedLocationJobsEvent } from "@/components/SavedLocationJobs";
import { formatSalary } from "@/lib/job-facts";
import type { PublishedJob } from "@/lib/published-jobs";

type NearbyJob = Pick<PublishedJob, "job_id" | "title" | "location" | "salary_text" | "employment_type"> & {
  distance_miles?: number;
};

function getJobPath(jobId: string): string {
  return `/jobs/${encodeURIComponent(jobId)}`;
}

type MoreJobsNearbyProps = {
  jobs: NearbyJob[];
  jobId?: string;
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
  jobId,
  allJobsPath,
  allJobsLabel,
  intro = "Approved role matches within 15 straight-line miles. Locations shown are where the jobs are based.",
  heading = "Suitable jobs nearby",
  emptyMessage = "No approved close match is available at the moment. Browse the relevant regional jobs instead.",
  secondaryAllJobsPath,
  secondaryAllJobsLabel,
}: MoreJobsNearbyProps) {
  const [displayJobs, setDisplayJobs] = useState(jobs);
  const [savedTown, setSavedTown] = useState("");
  const [displayPath, setDisplayPath] = useState(allJobsPath);
  const [displayLabel, setDisplayLabel] = useState(allJobsLabel);

  useEffect(() => {
    function update(event: Event) {
      const detail = (event as CustomEvent<{
        jobId?: string;
        clear?: boolean;
        location?: { town?: string };
        jobs?: NearbyJob[];
        searchPath?: string;
      }>).detail;
      if (detail.jobId !== jobId) return;
      if (detail.clear) {
        setDisplayJobs(jobs);
        setSavedTown("");
        setDisplayPath(allJobsPath);
        setDisplayLabel(allJobsLabel);
        return;
      }
      if (!detail.location?.town) return;
      setDisplayJobs(detail.jobs ?? []);
      setSavedTown(detail.location.town);
      if (detail.searchPath) {
        setDisplayPath(detail.searchPath);
        setDisplayLabel(`View all jobs near ${detail.location.town}`);
      }
    }
    window.addEventListener(savedLocationJobsEvent, update);
    return () => window.removeEventListener(savedLocationJobsEvent, update);
  }, [allJobsLabel, allJobsPath, jobId, jobs]);

  return (
    <section className={styles.panel}>
      <h2 className={styles.heading}>{heading}</h2>
      <p className={styles.intro}>{savedTown ? `Approved role matches within 15 straight-line miles of ${savedTown}.` : intro}</p>

      {displayJobs.length ? (
        <ul className={styles.list}>
          {displayJobs.map((job) => {
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
        <p className={styles.intro}>{savedTown ? `No approved close role match is available near ${savedTown} at the moment.` : emptyMessage}</p>
      )}

      <Link href={displayPath} className={styles.allJobsLink}>
        <span>{displayLabel}</span>
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

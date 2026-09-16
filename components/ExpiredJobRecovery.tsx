"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import SavedLocationJobs from "@/components/SavedLocationJobs";
import styles from "@/app/jobs/[id]/job-page.module.css";

type RecoveryJob = {
  jobId: string;
  title: string;
  location: string;
  href: string;
};

type RecoveryPayload = {
  job: { jobId: string; title: string; location: string };
  displayLocation: string;
  primaryLink: { href: string; label: string };
  secondaryLink: { href: string; label: string };
  recommendations: RecoveryJob[];
};

export default function ExpiredJobRecovery({
  fallbackJobs,
}: {
  fallbackJobs: RecoveryJob[];
}) {
  const pathname = usePathname();
  const jobId = useMemo(() => {
    const value = pathname.match(/^\/jobs\/(.+)$/)?.[1] ?? "";
    try {
      return decodeURIComponent(value);
    } catch {
      return value;
    }
  }, [pathname]);
  const [recovery, setRecovery] = useState<RecoveryPayload | null>(null);

  useEffect(() => {
    if (!jobId) return;
    const controller = new AbortController();
    fetch(`/api/jobs/expired-recovery/${encodeURIComponent(jobId)}`, {
      signal: controller.signal,
      cache: "no-store",
    })
      .then((response) => (response.ok ? response.json() : null))
      .then((payload: RecoveryPayload | null) => setRecovery(payload))
      .catch((error: unknown) => {
        if (!(error instanceof DOMException && error.name === "AbortError")) {
          setRecovery(null);
        }
      });
    return () => controller.abort();
  }, [jobId]);

  const recommendations = recovery?.recommendations.length
    ? recovery.recommendations
    : fallbackJobs;

  return (
    <main className={styles.expiredPage}>
      <article className={styles.expiredPanel}>
        <p className={styles.expiredEyebrow}>JOB NO LONGER AVAILABLE</p>
        <h1 className={styles.expiredTitle}>This job has expired</h1>
        <p className={styles.expiredIntro}>
          {recovery
            ? `The ${recovery.job.title} vacancy in ${recovery.displayLocation} has closed. Here are relevant current jobs.`
            : "The vacancy has been removed, but Ontap has other current jobs you can view now."}
        </p>

        <div className={styles.expiredActions}>
          <Link
            href={recovery?.primaryLink.href ?? "/browse-jobs"}
            className={styles.expiredPrimaryAction}
          >
            {recovery?.primaryLink.label ?? "Browse current jobs"}
          </Link>
          {recovery && recovery.secondaryLink.href !== recovery.primaryLink.href ? (
            <Link href={recovery.secondaryLink.href} className={styles.expiredSecondaryAction}>
              {recovery.secondaryLink.label}
            </Link>
          ) : (
            <Link href="/" className={styles.expiredSecondaryAction}>Return home</Link>
          )}
        </div>

        <SavedLocationJobs jobId={recovery?.job.jobId} />

        {recommendations.length ? (
          <section aria-labelledby="current-jobs-heading">
            <h2 id="current-jobs-heading" className={styles.expiredJobsHeading}>
              {recovery ? "Relevant current jobs" : "Current jobs on Ontap"}
            </h2>
            <ul className={styles.expiredJobsGrid}>
              {recommendations.map((job) => (
                <li key={job.jobId} className={styles.expiredJobCard}>
                  <Link href={job.href} className={styles.expiredJobLink}>{job.title}</Link>
                  <div className={styles.expiredJobLocation}>{job.location}</div>
                </li>
              ))}
            </ul>
          </section>
        ) : null}
      </article>
    </main>
  );
}

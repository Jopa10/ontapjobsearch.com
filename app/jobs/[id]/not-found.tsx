import { headers } from "next/headers";
import Link from "next/link";
import SavedLocationJobs from "@/components/SavedLocationJobs";
import { getExpiredJobRecovery } from "@/lib/expired-job-recovery";
import { getJobPath, getPublishedJobs } from "@/lib/published-jobs";
import styles from "./job-page.module.css";

export default async function JobNotFound() {
  const pathname = (await headers()).get("x-ontap-pathname") ?? "";
  const jobId = pathname.match(/^\/jobs\/(.+)$/)?.[1] ?? "";
  const currentJobs = getPublishedJobs();
  const recovery = getExpiredJobRecovery(jobId, currentJobs);
  const recommendations = recovery?.recommendations ?? currentJobs.slice(0, 6);

  return (
    <main className={styles.expiredPage}>
      <article className={styles.expiredPanel}>
        <p className={styles.expiredEyebrow}>JOB NO LONGER AVAILABLE</p>
        <h1 className={styles.expiredTitle}>This job has expired</h1>
        <p className={styles.expiredIntro}>
          {recovery
            ? `The ${recovery.job.title} vacancy in ${recovery.cityPage?.displayName ?? recovery.job.location} has closed. Here are relevant current jobs.`
            : "The vacancy has been removed, but Ontap has other current jobs you can view now."}
        </p>

        <div className={styles.expiredActions}>
          <Link href={recovery?.primaryLink.href ?? "/browse-jobs"} className={styles.expiredPrimaryAction}>
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

        <SavedLocationJobs jobId={recovery?.job.job_id} />

        {recommendations.length ? (
          <section aria-labelledby="current-jobs-heading">
            <h2 id="current-jobs-heading" className={styles.expiredJobsHeading}>
              {recovery ? "Relevant current jobs" : "Current jobs on Ontap"}
            </h2>
            <ul className={styles.expiredJobsGrid}>
              {recommendations.map((job) => (
                <li key={job.job_id} className={styles.expiredJobCard}>
                  <Link href={getJobPath(job.job_id)} className={styles.expiredJobLink}>{job.title}</Link>
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

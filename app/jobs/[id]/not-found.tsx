import ExpiredJobRecovery from "@/components/ExpiredJobRecovery";
import { getJobPath, getPublishedJobs } from "@/lib/published-jobs";

export default function JobNotFound() {
  const currentJobs = getPublishedJobs();
  const fallbackJobs = currentJobs.slice(0, 6).map((job) => ({
    jobId: job.job_id,
    title: job.title,
    location: job.location,
    href: getJobPath(job.job_id),
  }));

  return <ExpiredJobRecovery fallbackJobs={fallbackJobs} />;
}

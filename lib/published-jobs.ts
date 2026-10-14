import publishedJobsData from "@/generated/published-jobs.json";
import canonicalJobIdsData from "@/generated/published-job-canonical-ids.json";
import type { PublishedJob } from "@/lib/published-jobs-source";

export type { PublishedJob } from "@/lib/published-jobs-source";

const publishedJobs = publishedJobsData as PublishedJob[];
const publishedJobsById = new Map(publishedJobs.map((job) => [job.job_id, job]));
const canonicalJobIds = canonicalJobIdsData as Record<string, string>;

export function getPublishedJobs(): PublishedJob[] {
  return publishedJobs;
}

export function getPublishedCanonicalIds(): Record<string, string> {
  return canonicalJobIds;
}

export function decodePublishedJobId(jobId: string): string {
  try {
    return decodeURIComponent(jobId);
  } catch {
    return jobId;
  }
}

export function getPublishedJob(jobId: string): PublishedJob | undefined {
  return publishedJobsById.get(decodePublishedJobId(jobId));
}

export function getCanonicalPublishedJobId(jobId: string): string {
  const decodedJobId = decodePublishedJobId(jobId);
  return canonicalJobIds[decodedJobId] ?? decodedJobId;
}

export function getJobPath(jobId: string): string {
  return `/jobs/${encodeURIComponent(jobId)}`;
}

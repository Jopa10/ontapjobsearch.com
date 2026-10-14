export function getJobPath(jobId: string): string {
  return `/jobs/${encodeURIComponent(jobId)}`;
}

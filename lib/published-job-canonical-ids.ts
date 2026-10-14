import generatedCanonicalIds from "@/generated/published-job-canonical-ids.json";

function decodePublishedJobId(jobId: string): string {
  try {
    return decodeURIComponent(jobId);
  } catch {
    return jobId;
  }
}

export function getCanonicalPublishedJobId(jobId: string): string {
  const decodedJobId = decodePublishedJobId(jobId);
  return generatedCanonicalIds[decodedJobId] ?? decodedJobId;
}

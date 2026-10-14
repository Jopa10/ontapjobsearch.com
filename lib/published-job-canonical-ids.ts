import generatedCanonicalIds from "@/generated/published-job-canonical-ids.json";

const canonicalIds = generatedCanonicalIds as Record<string, string>;

function decodePublishedJobId(jobId: string): string {
  try {
    return decodeURIComponent(jobId);
  } catch {
    return jobId;
  }
}

export function getCanonicalPublishedJobId(jobId: string): string {
  const decodedJobId = decodePublishedJobId(jobId);
  return canonicalIds[decodedJobId] ?? decodedJobId;
}

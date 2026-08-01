import type { PublishedJob } from "@/lib/published-jobs";

function normalise(value: string): string {
  return value.trim().toLowerCase();
}

function relatedRank(current: PublishedJob, candidate: PublishedJob): number | null {
  const sameSlice =
    Boolean(current.slice_path) && candidate.slice_path === current.slice_path;
  const sameRegion =
    Boolean(current.region) && normalise(candidate.region) === normalise(current.region);
  const sameCategory =
    Boolean(current.category) &&
    normalise(candidate.category) === normalise(current.category);
  const sameLocation =
    Boolean(current.location) &&
    normalise(candidate.location) === normalise(current.location);

  if (!sameSlice && !(sameRegion && sameCategory)) return null;
  if (sameSlice && sameLocation) return 0;
  if (sameRegion && sameCategory && sameLocation) return 1;
  if (sameSlice) return 2;
  return 3;
}

export function getRelatedJobs(
  current: PublishedJob,
  jobs: PublishedJob[],
  limit = 6
): PublishedJob[] {
  return jobs
    .filter((candidate) => candidate.job_id !== current.job_id)
    .map((candidate) => ({
      candidate,
      rank: relatedRank(current, candidate),
    }))
    .filter(
      (entry): entry is { candidate: PublishedJob; rank: number } =>
        entry.rank !== null
    )
    .sort((a, b) => {
      if (a.rank !== b.rank) return a.rank - b.rank;

      const locationOrder = a.candidate.location.localeCompare(
        b.candidate.location,
        "en-GB",
        { sensitivity: "base" }
      );
      if (locationOrder) return locationOrder;

      const titleOrder = a.candidate.title.localeCompare(
        b.candidate.title,
        "en-GB",
        { sensitivity: "base" }
      );
      if (titleOrder) return titleOrder;

      return a.candidate.job_id.localeCompare(b.candidate.job_id);
    })
    .slice(0, Math.max(0, limit))
    .map(({ candidate }) => candidate);
}

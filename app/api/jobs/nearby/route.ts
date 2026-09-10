import { NextResponse } from "next/server";
import {
  getDiscoveryRecommendationsForLocation,
  getJobsNearApprovedLocation,
  getNearestApprovedLocation,
  resolveApprovedLocation,
} from "@/lib/discovery-recommendations";
import { getPublishedJob, getPublishedJobs } from "@/lib/published-jobs";

type NearbyRequest = {
  latitude?: unknown;
  longitude?: unknown;
  location?: unknown;
  region?: unknown;
  jobId?: unknown;
};

function text(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

export async function POST(request: Request) {
  let body: NearbyRequest;
  try {
    body = await request.json() as NearbyRequest;
  } catch {
    return NextResponse.json({ error: "Invalid request." }, { status: 400 });
  }

  const latitude = Number(body.latitude);
  const longitude = Number(body.longitude);
  const suppliedLocation = text(body.location);
  const suppliedRegion = text(body.region);
  const location = suppliedLocation
    ? resolveApprovedLocation(suppliedLocation, suppliedRegion)
    : getNearestApprovedLocation(latitude, longitude);
  if (!location) {
    return NextResponse.json({ error: "We could not match that location to an Ontap area." }, { status: 422 });
  }

  const jobs = getPublishedJobs();
  const nearbyJobs = getJobsNearApprovedLocation(jobs, location);
  const current = getPublishedJob(text(body.jobId));
  const suitableJobs = current
    ? getDiscoveryRecommendationsForLocation(current, jobs, location, 6)
    : [];

  return NextResponse.json({
    location: { town: location.location, region: location.region },
    count: nearbyJobs.length,
    suitableJobs: suitableJobs.map((job) => ({
      job_id: job.job_id,
      title: job.title,
      location: job.location,
      salary_text: job.salary_text,
      employment_type: job.employment_type,
      distance_miles: job.distance_miles,
    })),
  });
}

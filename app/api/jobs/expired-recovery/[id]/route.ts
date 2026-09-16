import { NextResponse } from "next/server";
import { getExpiredJobRecovery } from "@/lib/expired-job-recovery";
import { getJobPath, getPublishedJobs } from "@/lib/published-jobs";

type RouteProps = {
  params: Promise<{ id: string }>;
};

export async function GET(_request: Request, { params }: RouteProps) {
  const { id } = await params;
  const recovery = getExpiredJobRecovery(id, getPublishedJobs());
  if (!recovery) {
    return NextResponse.json({ error: "Expired job not found" }, { status: 404 });
  }

  return NextResponse.json({
    job: {
      jobId: recovery.job.job_id,
      title: recovery.job.title,
      location: recovery.job.location,
    },
    displayLocation: recovery.cityPage?.displayName ?? recovery.job.location,
    primaryLink: recovery.primaryLink,
    secondaryLink: recovery.secondaryLink,
    recommendations: recovery.recommendations.map((job) => ({
      jobId: job.job_id,
      title: job.title,
      location: job.location,
      href: getJobPath(job.job_id),
    })),
  });
}

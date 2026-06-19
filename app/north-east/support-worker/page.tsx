import type { Metadata } from "next";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";

const routeKey = "north-east/support-worker";
const canonicalUrl = "https://www.ontapjobsearch.com/north-east/support-worker";

export const metadata: Metadata = {
  title: "North East Support Worker Jobs | Ontap Job Search",
  description:
    "Browse current support worker jobs across Newcastle and the North East, updated daily with employer-site application links.",
  alternates: {
    canonical: canonicalUrl,
  },
};

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "north-east", "support-worker-jobs.json"]}
      region="North East"
      title="North East Support Worker Roles"
      latestUpdate={getJobPageStatus(routeKey)}
      anchorTown="Newcastle"
    />
  );
}

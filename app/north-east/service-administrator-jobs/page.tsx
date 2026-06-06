import type { Metadata } from "next";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";

const routeKey = "north-east/service-administrator-jobs";
const canonicalUrl = "https://www.ontapjobsearch.com/north-east/service-administrator-jobs";

export const metadata: Metadata = {
  title: "North East Service Administrator Jobs | Ontap Job Search",
  description:
    "Browse service administrator, customer service administrator and office support jobs across Newcastle and the North East.",
  alternates: {
    canonical: canonicalUrl,
  },
};

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "north-east", "service-administrator-jobs.json"]}
      region="North East"
      title="North East Service Administrator Jobs"
      latestUpdate={getJobPageStatus(routeKey)}
      anchorTown="Newcastle"
    />
  );
}

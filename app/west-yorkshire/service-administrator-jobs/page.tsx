import type { Metadata } from "next";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";

const routeKey = "west-yorkshire/service-administrator-jobs";
const canonicalUrl = "https://www.ontapjobsearch.com/west-yorkshire/service-administrator-jobs";

export const metadata: Metadata = {
  title: "West Yorkshire Service Administrator Jobs | Ontap Job Search",
  description:
    "Browse service administrator, customer service administrator and office support jobs across Leeds and West Yorkshire.",
  alternates: {
    canonical: canonicalUrl,
  },
};

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "west-yorkshire", "service-administrator-jobs.json"]}
      region="West Yorkshire"
      title="West Yorkshire Service Administrator Jobs"
      latestUpdate={getJobPageStatus(routeKey)}
      anchorTown="Leeds"
    />
  );
}

import type { Metadata } from "next";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";

const routeKey = "west-yorkshire/support-worker";
const canonicalUrl = "https://www.ontapjobsearch.com/west-yorkshire/support-worker";

export const metadata: Metadata = {
  title: "West Yorkshire Support Worker Jobs | Ontap Job Search",
  description:
    "Browse current support worker jobs across Leeds and West Yorkshire, updated daily with employer-site application links.",
  alternates: {
    canonical: canonicalUrl,
  },
};

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "west-yorkshire", "support-worker.json"]}
      region="West Yorkshire"
      title="West Yorkshire Support Worker Roles"
      latestUpdate={getJobPageStatus(routeKey)}
      anchorTown="Leeds"
      relatedPage={{
        href: "/south-yorkshire/support-worker",
        prompt: "Also searching around South Yorkshire?",
        label: "View South Yorkshire support-worker jobs",
      }}
    />
  );
}


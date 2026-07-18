import type { Metadata } from "next";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";

const routeKey = "south-yorkshire/support-worker";
const canonicalUrl = "https://www.ontapjobsearch.com/south-yorkshire/support-worker";

export const metadata: Metadata = {
  title: "South Yorkshire Support Worker Jobs | Ontap Job Search",
  description:
    "Browse current support worker jobs across Sheffield and South Yorkshire, updated daily with employer-site application links.",
  alternates: {
    canonical: canonicalUrl,
  },
};

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "south-yorkshire", "support-worker.json"]}
      region="South Yorkshire"
      title="South Yorkshire Support Worker Roles"
      latestUpdate={getJobPageStatus(routeKey)}
      anchorTown="Sheffield"
      relatedPage={{
        href: "/west-yorkshire/support-worker",
        prompt: "Also searching around West Yorkshire?",
        label: "View West Yorkshire support-worker jobs",
      }}
    />
  );
}


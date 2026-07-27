import type { Metadata } from "next";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";

const routeKey = "hampshire/support-worker";
const canonicalUrl = "https://www.ontapjobsearch.com/hampshire/support-worker";

export const metadata: Metadata = {
  title: "Hampshire Support Worker Jobs | Ontap Job Search",
  description:
    "Browse current support worker jobs across Southampton and Hampshire, updated daily with employer-site application links.",
  alternates: { canonical: canonicalUrl },
};

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "hampshire", "support-worker.json"]}
      region="Hampshire"
      title="Hampshire Support Worker Roles"
      latestUpdate={getJobPageStatus(routeKey)}
      anchorTown="Southampton"
    />
  );
}

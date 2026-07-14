import type { Metadata } from "next";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";

const routeKey = "sussex/support-worker";
const canonicalUrl = "https://www.ontapjobsearch.com/sussex/support-worker";

export const metadata: Metadata = {
  title: "Sussex Support Worker Jobs | Ontap Job Search",
  description:
    "Browse current support worker jobs across Brighton and Sussex, updated daily with employer-site application links.",
  alternates: { canonical: canonicalUrl },
};

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "sussex", "support-worker.json"]}
      region="Sussex"
      title="Sussex Support Worker Roles"
      latestUpdate={getJobPageStatus(routeKey)}
      anchorTown="Brighton"
    />
  );
}

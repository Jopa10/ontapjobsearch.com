import type { Metadata } from "next";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";

const routeKey = "cumbria-south/support-worker";
const canonicalUrl = "https://www.ontapjobsearch.com/cumbria-south/support-worker";

export const metadata: Metadata = {
  title: "South Cumbria Support Worker Jobs | Ontap Job Search",
  description:
    "Browse current support worker jobs across Barrow-in-Furness, Kendal, Ulverston and South Cumbria, updated daily with employer-site application links.",
  alternates: { canonical: canonicalUrl },
};

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "cumbria-south", "support-worker.json"]}
      region="South Cumbria"
      title="South Cumbria Support Worker Roles"
      latestUpdate={getJobPageStatus(routeKey)}
      anchorTown="Barrow-in-Furness"
    />
  );
}

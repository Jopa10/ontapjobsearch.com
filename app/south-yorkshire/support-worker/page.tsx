import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";

const routeKey = "south-yorkshire/support-worker";

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "south-yorkshire", "support-worker.json"]}
      region="South Yorkshire"
      title="South Yorkshire Support Worker Roles"
      latestUpdate={getJobPageStatus(routeKey)}
      anchorTown="Sheffield"
    />
  );
}

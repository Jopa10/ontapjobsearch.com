import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";

const routeKey = "west-yorkshire/support-worker";

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "west-yorkshire", "support-worker.json"]}
      region="West Yorkshire"
      title="West Yorkshire Support Worker Roles"
      latestUpdate={getJobPageStatus(routeKey)}
      anchorTown="Leeds"
    />
  );
}



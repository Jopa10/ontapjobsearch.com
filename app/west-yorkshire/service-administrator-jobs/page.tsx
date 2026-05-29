import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";

const routeKey = "west-yorkshire/service-administrator-jobs";

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

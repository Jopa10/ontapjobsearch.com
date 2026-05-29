import JobSlicePage from "@/components/JobSlicePage";

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "west-yorkshire", "service-administrator-jobs.json"]}
      region="West Yorkshire"
      title="West Yorkshire Service Administrator Jobs"
      latestUpdate="Updated Fri 29th May, AM"
      anchorTown="Leeds"
    />
  );
}

import JobSlicePage from "@/components/JobSlicePage";

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "west-yorkshire", "support-worker.json"]}
      region="West Yorkshire"
      title="West Yorkshire Support Worker Roles"
      latestUpdate="Thu 14th May, AM"
      anchorTown="Leeds"
    />
  );
}



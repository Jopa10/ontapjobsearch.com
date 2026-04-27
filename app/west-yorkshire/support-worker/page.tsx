import JobSlicePage from "@/components/JobSlicePage";

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "west-yorkshire", "support-worker.json"]}
      region="West Yorkshire"
      title="West Yorkshire Support Worker Roles"
      latestUpdate="Mon 27th April, AM"
      anchorTown="Leeds"
    />
  );
}



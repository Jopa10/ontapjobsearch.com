import JobSlicePage from "@/components/JobSlicePage";

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "south-yorkshire", "support-worker.json"]}
      region="South Yorkshire"
      title="South Yorkshire Support Worker Roles"
      latestUpdate="Sat 16th May, AM"
      anchorTown="Sheffield"
    />
  );
}

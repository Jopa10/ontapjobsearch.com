import JobSlicePage from "@/components/JobSlicePage";

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "south-yorkshire", "support-worker.json"]}
      region="South Yorkshire"
      title="South Yorkshire Support Worker Roles"
      latestUpdate="Checked Thu 28th May, AM"
      anchorTown="Sheffield"
    />
  );
}

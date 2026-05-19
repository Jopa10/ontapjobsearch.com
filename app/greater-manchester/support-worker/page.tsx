import JobSlicePage from "@/components/JobSlicePage";

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "greater-manchester", "support-worker.json"]}
      region="Greater Manchester"
      title="Greater Manchester Support Worker Roles"
      latestUpdate="Tue 19th May, AM"
      anchorTown="Manchester"
    />
  );
}

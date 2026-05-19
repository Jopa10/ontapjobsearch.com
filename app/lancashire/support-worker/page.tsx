import JobSlicePage from "@/components/JobSlicePage";

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "lancashire", "support-worker.json"]}
      region="Lancashire"
      title="Lancashire Support Worker Roles"
      latestUpdate="Tue 19th May, AM"
      anchorTown="Preston"
    />
  );
}

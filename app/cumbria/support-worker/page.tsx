import JobSlicePage from "@/components/JobSlicePage";

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "cumbria", "support-worker.json"]}
      region="Cumbria"
      title="Cumbria Support Worker Roles"
      latestUpdate="Tue 19th May, AM"
      anchorTown="Carlisle"
    />
  );
}

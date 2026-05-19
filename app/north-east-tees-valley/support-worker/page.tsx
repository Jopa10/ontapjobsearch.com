import JobSlicePage from "@/components/JobSlicePage";

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "north-east-tees-valley", "support-worker.json"]}
      region="North East - Tees Valley"
      title="North East - Tees Valley Support Worker Roles"
      latestUpdate="Tue 19th May, AM"
      anchorTown="Middlesbrough"
    />
  );
}

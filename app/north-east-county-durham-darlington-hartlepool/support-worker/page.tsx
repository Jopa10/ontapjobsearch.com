import JobSlicePage from "@/components/JobSlicePage";

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={[
        "app",
        "north-east-county-durham-darlington-hartlepool",
        "support-worker.json",
      ]}
      region="North East - County Durham & Darlington/Hartlepool"
      title="North East - County Durham & Darlington/Hartlepool Support Worker Roles"
      latestUpdate="Tue 19th May, AM"
      anchorTown="Durham"
    />
  );
}

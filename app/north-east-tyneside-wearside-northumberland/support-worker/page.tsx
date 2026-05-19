import JobSlicePage from "@/components/JobSlicePage";

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={[
        "app",
        "north-east-tyneside-wearside-northumberland",
        "support-worker.json",
      ]}
      region="North East - Tyneside, Wearside & Northumberland"
      title="North East - Tyneside, Wearside & Northumberland Support Worker Roles"
      latestUpdate="Tue 19th May, AM"
      anchorTown="Newcastle upon Tyne"
    />
  );
}

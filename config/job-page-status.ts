export const jobPageStatus = {
  defaultStatus: "Updated",
  defaultDate: "Fri 29th May, AM",

  checkedRoutes: [
    "west-yorkshire/support-worker",
    "south-yorkshire/support-worker",
  ],
};

export function getJobPageStatus(routeKey: string) {
  const status = jobPageStatus.checkedRoutes.includes(routeKey)
    ? "Checked"
    : jobPageStatus.defaultStatus;

  return `${status} ${jobPageStatus.defaultDate}`;
}

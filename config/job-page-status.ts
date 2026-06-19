export const jobPageStatus = {
  defaultStatus: "Updated",
  defaultDate: "Fri 19th June, AM",

  routeStatus: {
    "west-yorkshire/support-worker": "Checked",
    "south-yorkshire/support-worker": "Checked",
    "north-east/support-worker": "Checked",
    "west-yorkshire/service-administrator-jobs": "Checked",
    "south-yorkshire/service-administrator-jobs": "",
  },
};

export function getJobPageStatus(routeKey: string) {
  const routeStatus =
    jobPageStatus.routeStatus[routeKey as keyof typeof jobPageStatus.routeStatus];

  const status = routeStatus || jobPageStatus.defaultStatus;

  return `${status} ${jobPageStatus.defaultDate}`;
}

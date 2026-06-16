export const jobPageStatus = {
  defaultStatus: "Updated",
  defaultDate: "Tue 16th June, AM",

  routeStatus: {
    "west-yorkshire/support-worker": "Checked",
    "south-yorkshire/support-worker": "Checked",
    "west-yorkshire/service-administrator-jobs": "",
    "south-yorkshire/service-administrator-jobs": "",
  },
};

export function getJobPageStatus(routeKey: string) {
  const routeStatus =
    jobPageStatus.routeStatus[routeKey as keyof typeof jobPageStatus.routeStatus];

  const status = routeStatus || jobPageStatus.defaultStatus;

  return `${status} ${jobPageStatus.defaultDate}`;
}

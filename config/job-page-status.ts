export const jobPageStatus = {
  defaultStatus: "Updated",
  defaultDate: "Mon 22nd June, AM",

  routeStatus: {
    "west-yorkshire/support-worker": "Updated",
    "south-yorkshire/support-worker": "Updated",
    "north-east/support-worker": "Updated",
    "west-yorkshire/service-administrator-jobs": "Updated",
    "south-yorkshire/service-administrator-jobs": "Updated",
  },
};

export function getJobPageStatus(routeKey: string) {
  const routeStatus =
    jobPageStatus.routeStatus[routeKey as keyof typeof jobPageStatus.routeStatus];

  const status = routeStatus || jobPageStatus.defaultStatus;

  return `${status} ${jobPageStatus.defaultDate}`;
}

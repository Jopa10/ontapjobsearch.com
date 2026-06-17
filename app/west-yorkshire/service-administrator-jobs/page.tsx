import type { Metadata } from "next";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";

const routeKey = "west-yorkshire/service-administrator-jobs";
const canonicalUrl = "https://www.ontapjobsearch.com/west-yorkshire/service-administrator-jobs";

export const metadata: Metadata = {
  title: "West Yorkshire Service Administrator Jobs | Ontap Job Search",
  description:
    "Browse service administrator, customer service administrator and office support jobs across Leeds and West Yorkshire.",
  alternates: {
    canonical: canonicalUrl,
  },
};

const adminTraining = [
  {
    title: "Business Administration Level 2",
    provider: "OpenLearn",
    description:
      "Foundational office administration learning for scheduling, communication and records tasks.",
    link: "https://www.open.edu/openlearn/money-business/business-studies/introduction-business-administration/content-section-0",
  },
  {
    title: "Customer Service Skills",
    provider: "Alison",
    description:
      "Practical customer service training useful for service-administrator and front-office roles.",
    link: "https://alison.com/course/customer-service-skills",
  },
  {
    title: "Excel for Administrative Work",
    provider: "Microsoft Learn",
    description:
      "Build spreadsheet and reporting skills commonly required in office support roles.",
    link: "https://learn.microsoft.com/training/",
  },
];

export default function Page() {
  return (
    <JobSlicePage
      jsonPath={["app", "west-yorkshire", "service-administrator-jobs.json"]}
      region="West Yorkshire"
      title="West Yorkshire Service Administrator Jobs"
      latestUpdate={getJobPageStatus(routeKey)}
      anchorTown="Leeds"
      trainingHeading="Boost your admin applications"
      trainingSubheading="Useful online learning commonly requested for service-administrator and office support roles"
      trainingItems={adminTraining}
    />
  );
}

import type { Metadata } from "next";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";

const routeKey = "west-yorkshire/service-administrator-jobs";
const canonicalUrl = "https://www.ontapjobsearch.com/west-yorkshire/service-administrator-jobs";

export const metadata: Metadata = {
  title: "Admin and Office Jobs in West Yorkshire | Ontap",
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
  const latestUpdate = getJobPageStatus(routeKey);

  return (
    <JobSlicePage
      jsonPath={["app", "west-yorkshire", "service-administrator-jobs.json"]}
      region="West Yorkshire"
      title="Admin, Office, Reception and Customer Service Jobs in West Yorkshire"
      latestUpdate={latestUpdate}
      introText={`Browse current administration, office support, reception and customer service jobs across West Yorkshire, plus accounts and finance support roles with a substantial administrative element. Jobs are checked and updated daily. Latest update: ${latestUpdate} • Apply on employer sites`}
      anchorTown="Leeds"
      relatedPage={{
        href: "/south-yorkshire/service-administrator-jobs",
        prompt: "Also searching around South Yorkshire?",
        label: "View South Yorkshire admin & customer-service jobs",
      }}
      trainingHeading="Boost your admin applications"
      trainingSubheading="Useful online learning commonly requested for service-administrator and office support roles"
      trainingItems={adminTraining}
    />
  );
}
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";
import {
  isCityPageActive,
  newcastleServiceAdministratorPage,
} from "@/lib/city-page-data";

const routeKey = "newcastle/service-administrator-jobs";
const canonicalUrl =
  "https://www.ontapjobsearch.com/newcastle/service-administrator-jobs";

export const metadata: Metadata = {
  title: "Newcastle Admin & Customer Service Jobs | Ontap Job Search",
  description:
    "Browse current admin, office support and customer-service jobs across Newcastle and its normal commuting catchment.",
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
  if (!isCityPageActive(newcastleServiceAdministratorPage)) notFound();

  const latestUpdate = getJobPageStatus(routeKey);

  return (
    <JobSlicePage
      jsonPath={[...newcastleServiceAdministratorPage.jsonPath]}
      region="Newcastle"
      title="Newcastle Admin & Customer Service Jobs"
      latestUpdate={latestUpdate}
      introText={`Current admin, office-support and customer-service jobs across Newcastle and its normal commuting catchment. Jobs are checked and updated daily. Latest update: ${latestUpdate} • Apply on employer sites`}
      anchorTown="Newcastle"
      trainingHeading="Boost your admin applications"
      trainingSubheading="Useful online learning commonly requested for service-administrator and office support roles"
      trainingItems={adminTraining}
      relatedPage={{
        href: "/north-east/service-administrator-jobs",
        prompt: "Looking across the wider region?",
        label: "View all North East jobs",
      }}
    />
  );
}

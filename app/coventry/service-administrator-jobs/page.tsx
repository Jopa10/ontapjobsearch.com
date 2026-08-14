import type { Metadata } from "next";
import { notFound } from "next/navigation";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";
import { getCityPageDefinitionByRoute, isCityPageActive } from "@/lib/city-page-data";

const route = "/coventry/service-administrator-jobs";
const routeKey = route.slice(1);
const definition = getCityPageDefinitionByRoute(route);
const canonicalUrl = `https://www.ontapjobsearch.com${route}`;

const adminTraining = [
  {
    title: "Business Administration Level 2",
    provider: "OpenLearn",
    description: "Foundational office administration learning for scheduling, communication and records tasks.",
    link: "https://www.open.edu/openlearn/money-business/business-studies/introduction-business-administration/content-section-0",
  },
  {
    title: "Customer Service Skills",
    provider: "Alison",
    description: "Practical customer service training useful for service-administrator and front-office roles.",
    link: "https://alison.com/course/customer-service-skills",
  },
  {
    title: "Excel for Administrative Work",
    provider: "Microsoft Learn",
    description: "Build spreadsheet and reporting skills commonly required in office support roles.",
    link: "https://learn.microsoft.com/training/",
  },
];

export const metadata: Metadata = {
  title: "Coventry Admin & Customer Service Jobs | Ontap Job Search",
  description: "Browse current admin and customer-service jobs across Coventry and its approved local employment market.",
  alternates: { canonical: canonicalUrl },
};

export default function Page() {
  if (!definition || !isCityPageActive(definition)) notFound();
  const latestUpdate = getJobPageStatus(routeKey);

  return (
    <JobSlicePage
      jsonPath={[...definition.jsonPath]}
      region="Coventry"
      title="Coventry Admin & Customer Service Jobs"
      latestUpdate={latestUpdate}
      introText={`Current admin and customer-service jobs across Coventry and its approved local employment market. Jobs are checked and updated daily. Latest update: ${latestUpdate} • Apply on employer sites`}
      anchorTown="Coventry"
      trainingHeading="Boost your admin applications"
      trainingSubheading="Useful online learning commonly requested for service-administrator and office support roles"
      trainingItems={adminTraining}
      relatedPage={{
        href: "/coventry-warwickshire/service-administrator-jobs",
        prompt: "Looking across the wider region?",
        label: "View all regional jobs",
      }}
    />
  );
}

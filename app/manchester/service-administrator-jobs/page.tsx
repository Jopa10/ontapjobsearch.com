import type { Metadata } from "next";
import { notFound } from "next/navigation";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";
import { getCityPageDefinitionByRoute, isCityPageActive } from "@/lib/city-page-data";

const route = "/manchester/service-administrator-jobs";
const definition = getCityPageDefinitionByRoute(route);
const canonicalUrl = `https://www.ontapjobsearch.com${route}`;

export const metadata: Metadata = {
  title: "Admin and Office Jobs in Manchester | Ontap",
  description: "Browse current admin and office jobs across Manchester and its approved local employment market.",
  alternates: { canonical: canonicalUrl },
};

export default function Page() {
  if (!definition || !isCityPageActive(definition)) notFound();
  const latestUpdate = getJobPageStatus(route.slice(1));
  return <JobSlicePage jsonPath={[...definition.jsonPath]} region="Manchester" title="Admin, Office, Reception and Customer Service Jobs in Manchester" latestUpdate={latestUpdate} introText={`Browse current administration, office support, reception and customer service jobs across Manchester and its approved local employment market, plus accounts and finance support roles with a substantial administrative element. Jobs are checked and updated daily. Latest update: ${latestUpdate} • Apply on employer sites`} anchorTown="Manchester" relatedPage={{href:"/job-search/manchester-salford/service-administrator-jobs",prompt:"Looking across the wider region?",label:"View all regional jobs"}} />;
}


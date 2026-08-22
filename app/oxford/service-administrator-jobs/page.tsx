import type { Metadata } from "next";
import { notFound } from "next/navigation";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";
import { getCityPageDefinitionByRoute, isCityPageActive } from "@/lib/city-page-data";

const route = "/oxford/service-administrator-jobs";
const definition = getCityPageDefinitionByRoute(route);
const canonicalUrl = `https://www.ontapjobsearch.com${route}`;

export const metadata: Metadata = {
  title: "Oxford Admin & Customer Service Jobs | Ontap Job Search",
  description: "Browse current admin and customer-service jobs across Oxford and its approved local employment market.",
  alternates: { canonical: canonicalUrl },
};

export default function Page() {
  if (!definition || !isCityPageActive(definition)) notFound();
  const latestUpdate = getJobPageStatus(route.slice(1));
  return <JobSlicePage jsonPath={[...definition.jsonPath]} region="Oxford" title="Oxford Admin & Customer Service Jobs" latestUpdate={latestUpdate} introText={`Current admin and customer-service jobs across Oxford and its approved local employment market. Jobs are checked and updated daily. Latest update: ${latestUpdate} • Apply on employer sites`} anchorTown="Oxford" relatedPage={{href:"/job-search/oxfordshire/service-administrator-jobs",prompt:"Looking across the wider region?",label:"View all regional jobs"}} />;
}


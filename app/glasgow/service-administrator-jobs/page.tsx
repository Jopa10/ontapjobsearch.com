import type { Metadata } from "next";
import { notFound } from "next/navigation";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";
import { getCityPageDefinitionByRoute, isCityPageActive } from "@/lib/city-page-data";

const route = "/glasgow/service-administrator-jobs";
const definition = getCityPageDefinitionByRoute(route);
const canonicalUrl = `https://www.ontapjobsearch.com${route}`;

export const metadata: Metadata = { title: "Admin and office jobs in Glasgow | Ontap Job Search", description: "Browse current admin and office jobs across Glasgow and its approved local employment market.", alternates: { canonical: canonicalUrl } };

export default function Page() {
  if (!definition || !isCityPageActive(definition)) notFound();
  const latestUpdate = getJobPageStatus(route.slice(1));
  return <JobSlicePage jsonPath={[...definition.jsonPath]} region="Glasgow" title="Admin and office jobs in Glasgow" latestUpdate={latestUpdate} introText={`Current admin and office jobs across Glasgow and its approved local employment market. Jobs are checked and updated daily. Latest update: ${latestUpdate} • Apply on employer sites`} anchorTown="Glasgow" relatedPage={{href:"/job-search/glasgow/service-administrator-jobs",prompt:"Looking across the wider region?",label:"View all regional jobs"}} />;
}

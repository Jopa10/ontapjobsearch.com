import type { Metadata } from "next";
import { notFound } from "next/navigation";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";
import { getCityPageDefinitionByRoute, isCityPageActive } from "@/lib/city-page-data";

const route = "/bristol/service-administrator-jobs";
const definition = getCityPageDefinitionByRoute(route);
const canonicalUrl = `https://www.ontapjobsearch.com${route}`;

export const metadata: Metadata = {
  title: "Admin and Office Jobs in Bristol | Ontap",
  description: "Browse current admin and office jobs across Bristol and its approved local employment market.",
  alternates: { canonical: canonicalUrl },
};

export default function Page() {
  if (!definition || !isCityPageActive(definition)) notFound();
  const latestUpdate = getJobPageStatus(route.slice(1));
  return <JobSlicePage jsonPath={[...definition.jsonPath]} region="Bristol" title="Admin, Office, Reception and Customer Service Jobs in Bristol" latestUpdate={latestUpdate} introText={`Browse current administration, office support, reception and customer service jobs across Bristol and its approved local employment market, plus accounts and finance support roles with a substantial administrative element. Jobs are checked and updated daily. Latest update: ${latestUpdate} • Apply on employer sites`} anchorTown="Bristol" relatedPage={{href:"/job-search/bristol-bath/service-administrator-jobs",prompt:"Looking across the wider region?",label:"View all regional jobs"}} />;
}


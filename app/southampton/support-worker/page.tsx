import type { Metadata } from "next";
import { notFound } from "next/navigation";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";
import { getCityPageDefinitionByRoute, isCityPageActive } from "@/lib/city-page-data";

const route = "/southampton/support-worker";
const routeKey = route.slice(1);
const definition = getCityPageDefinitionByRoute(route);
const canonicalUrl = `https://www.ontapjobsearch.com${route}`;

export const metadata: Metadata = {
  title: "Southampton Support Worker Jobs | Ontap Job Search",
  description: "Browse current support worker jobs across Southampton and its approved local employment market.",
  alternates: { canonical: canonicalUrl },
};

export default function Page() {
  if (!definition || !isCityPageActive(definition)) notFound();
  const latestUpdate = getJobPageStatus(routeKey);

  return (
    <JobSlicePage
      jsonPath={[...definition.jsonPath]}
      region="Southampton"
      title="Southampton Support Worker Jobs"
      latestUpdate={latestUpdate}
      introText={`Current support worker jobs across Southampton and its approved local employment market. Jobs are checked and updated daily. Latest update: ${latestUpdate} • Apply on employer sites`}
      anchorTown="Southampton"
      relatedPage={{
        href: "/hampshire/support-worker",
        prompt: "Looking across the wider region?",
        label: "View all regional jobs",
      }}
    />
  );
}

import type { Metadata } from "next";
import { notFound } from "next/navigation";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";
import {
  getPublishedDynamicSlice,
  getPublishedDynamicSlices,
} from "@/lib/configured-job-slices";

const siteUrl = "https://www.ontapjobsearch.com";

type PageProps = {
  params: Promise<{ region: string; category: string }>;
};

const officeTraining = [
  {
    title: "Microsoft 365 training",
    provider: "Microsoft Learn",
    description:
      "Refresh Excel, Outlook and everyday office-productivity skills used across many admin, finance, customer-service and HR roles.",
    link: "https://learn.microsoft.com/training/",
  },
];

export const dynamicParams = false;

export function generateStaticParams() {
  return getPublishedDynamicSlices().map((slice) => ({
    region: slice.regionSlug,
    category: slice.categorySlug,
  }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { region, category } = await params;
  const slice = getPublishedDynamicSlice(region, category);
  if (!slice) return {};
  const canonical = `${siteUrl}${slice.route}`;
  return {
    title: `${slice.title} | Ontap Job Search`,
    description: `Browse current ${slice.displayLabel.toLowerCase()} jobs across ${slice.region}. Apply on employer sites.`,
    alternates: { canonical },
  };
}

export default async function Page({ params }: PageProps) {
  const { region, category } = await params;
  const slice = getPublishedDynamicSlice(region, category);
  if (!slice) notFound();

  const routeKey = `job-search/${slice.regionSlug}/${slice.categorySlug}`;
  const latestUpdate = getJobPageStatus(routeKey);
  const isSupport = slice.category === "support_worker";

  return (
    <JobSlicePage
      jsonPath={[
        "app",
        "_city-pages",
        "configured-slices",
        slice.regionSlug,
        `${slice.categorySlug}.json`,
      ]}
      region={slice.region}
      title={slice.title}
      latestUpdate={latestUpdate}
      anchorTown={slice.anchorTown}
      introText={`Updated daily • Latest update: ${latestUpdate} • Roles across ${slice.region} • Apply on employer sites`}
      {...(isSupport
        ? {}
        : {
            trainingHeading: "Useful office skills",
            trainingSubheading:
              "Practical digital skills used across many office-based roles",
            trainingItems: officeTraining,
          })}
    />
  );
}

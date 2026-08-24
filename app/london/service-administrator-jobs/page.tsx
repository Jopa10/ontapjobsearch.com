import type { Metadata } from "next";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";
import { isLondonJob } from "@/lib/london-job-area";

const routeKey = "london/service-administrator-jobs";
const canonicalUrl = "https://www.ontapjobsearch.com/london/service-administrator-jobs";

export const metadata: Metadata = {
  title: "London Admin & Customer Service Jobs | Ontap Job Search",
  description:
    "Browse service administrator, customer service administrator and office support jobs across London, with optional Central, North, East, South and West London views.",
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

const londonAreaLinks = [
  { href: "/london/central-service-administrator-jobs", label: "Central" },
  { href: "/london/north-service-administrator-jobs", label: "North & NW" },
  { href: "/london/east-service-administrator-jobs", label: "East & NE" },
  { href: "/london/south-service-administrator-jobs", label: "South & SE" },
  { href: "/london/west-service-administrator-jobs", label: "West & SW" },
];

export default function Page() {
  const latestUpdate = getJobPageStatus(routeKey);

  return (
    <JobSlicePage
      jsonPath={["app", "london", "service-administrator-jobs.json"]}
      region="London"
      title="London Admin & Customer Service Jobs"
      latestUpdate={latestUpdate}
      introText={`Updated daily • Latest update: ${latestUpdate} • Roles across London • Apply on employer sites`}
      anchorTown="London"
      jobFilter={isLondonJob}
      sectorFilterEnabled
      compactPageSpacing
      softPageBackground
      relatedPage={{
        href: "/job-search/london/paralegal-jobs",
        prompt: "Looking for legal support work in London?",
        label: "Paralegal jobs",
      }}
      browseLinks={{
        heading: "Browse London by area",
        intro: "Use an area when the vacancy gives a reliable London location; otherwise it stays on this London-wide page.",
        compact: true,
        links: londonAreaLinks,
      }}
      trainingHeading="Boost your admin applications"
      trainingSubheading="Useful online learning commonly requested for service-administrator and office support roles"
      trainingItems={adminTraining}
    />
  );
}

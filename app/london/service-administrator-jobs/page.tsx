import type { Metadata } from "next";
import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";
import { isCentralInnerLondonJob } from "@/lib/london-job-area";

const routeKey = "london/service-administrator-jobs";
const canonicalUrl = "https://www.ontapjobsearch.com/london/service-administrator-jobs";

export const metadata: Metadata = {
  title: "Central & Inner London Admin & Customer Service Jobs | Ontap Job Search",
  description:
    "Browse service administrator, customer service administrator and office support jobs across Central and Inner London.",
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
      jsonPath={["app", "london", "service-administrator-jobs.json"]}
      region="Central & Inner London"
      title="Central & Inner London Admin & Customer Service Jobs"
      latestUpdate={latestUpdate}
      introText={`Updated daily • Latest update: ${latestUpdate} • Roles across Central and Inner London • Apply on employer sites`}
      anchorTown="London"
      jobFilter={isCentralInnerLondonJob}
      relatedPage={{
        href: "/london/outer-service-administrator-jobs",
        prompt: "Looking beyond central London?",
        label: "View Outer London jobs",
      }}
      trainingHeading="Boost your admin applications"
      trainingSubheading="Useful online learning commonly requested for service-administrator and office support roles"
      trainingItems={adminTraining}
    />
  );
}

import JobSlicePage from "@/components/JobSlicePage";
import { getJobPageStatus } from "@/config/job-page-status";
import {
  isCentralLondonJob,
  isEastLondonJob,
  isNorthLondonJob,
  isSouthLondonJob,
  isWestLondonJob,
  type LondonJobLocationInput,
  type LondonSubArea,
} from "@/lib/london-job-area";

type AreaDetails = {
  routeKey: string;
  region: string;
  title: string;
  description: string;
  filter: (job: LondonJobLocationInput) => boolean;
};

export const londonAreaDetails: Record<LondonSubArea, AreaDetails> = {
  central: {
    routeKey: "london/central-service-administrator-jobs",
    region: "Central London",
    title: "Central London Admin & Customer Service Jobs",
    description:
      "Browse service administrator, customer service administrator and office support jobs with reliable Central London location evidence.",
    filter: isCentralLondonJob,
  },
  north: {
    routeKey: "london/north-service-administrator-jobs",
    region: "North & North-West London",
    title: "North & North-West London Admin & Customer Service Jobs",
    description:
      "Browse service administrator, customer service administrator and office support jobs across North and North-West London.",
    filter: isNorthLondonJob,
  },
  east: {
    routeKey: "london/east-service-administrator-jobs",
    region: "East & North-East London",
    title: "East & North-East London Admin & Customer Service Jobs",
    description:
      "Browse service administrator, customer service administrator and office support jobs across East and North-East London.",
    filter: isEastLondonJob,
  },
  south: {
    routeKey: "london/south-service-administrator-jobs",
    region: "South & South-East London",
    title: "South & South-East London Admin & Customer Service Jobs",
    description:
      "Browse service administrator, customer service administrator and office support jobs across South and South-East London.",
    filter: isSouthLondonJob,
  },
  west: {
    routeKey: "london/west-service-administrator-jobs",
    region: "West & South-West London",
    title: "West & South-West London Admin & Customer Service Jobs",
    description:
      "Browse service administrator, customer service administrator and office support jobs across West and South-West London.",
    filter: isWestLondonJob,
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

export default function LondonAdminAreaPage({ area }: { area: LondonSubArea }) {
  const details = londonAreaDetails[area];
  const latestUpdate = getJobPageStatus(details.routeKey);

  return (
    <JobSlicePage
      jsonPath={["app", "london", "service-administrator-jobs.json"]}
      region={details.region}
      title={details.title}
      latestUpdate={latestUpdate}
      introText={`Updated daily • Latest update: ${latestUpdate} • Roles across ${details.region} • Apply on employer sites`}
      anchorTown="London"
      jobFilter={details.filter}
      relatedPage={{
        href: "/london/service-administrator-jobs",
        prompt: "Want to see all current London roles, including jobs without a precise sub-area?",
        label: "View all London jobs",
      }}
      trainingHeading="Boost your admin applications"
      trainingSubheading="Useful online learning commonly requested for service-administrator and office support roles"
      trainingItems={adminTraining}
    />
  );
}

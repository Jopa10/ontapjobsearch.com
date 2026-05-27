import JobSlicePage from "@/components/JobSlicePage";

export const metadata = {
  title: "Ontap – Service administrator jobs in South Yorkshire",
  description:
    "Service administrator, customer service administrator, office support and admin roles in South Yorkshire.",
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
  return (
    <JobSlicePage
      jsonPath={["app", "south-yorkshire", "service-administrator-jobs.json"]}
      region="South Yorkshire"
      title="Service administrator jobs in South Yorkshire"
      latestUpdate="Checked Wed 27th May, AM"
      anchorTown="Sheffield"
      introText="Updated daily • Latest update: Checked Wed 27th May, AM • Service administrator, customer service administrator, office support and admin roles across South Yorkshire • Apply on employer sites"
      trainingHeading="Boost your admin applications"
      trainingSubheading="Useful online learning commonly requested for service-administrator and office support roles"
      trainingItems={adminTraining}
    />
  );
}

export type TransferableFit = {
  similarRoles: string[];
  usefulExperience: string[];
  plainEnglish: string;
};

const TRIAL_FITS: Record<string, TransferableFit> = {
  "teaching-vacancies-business-support-officer-2ea7277a-9574-40f3-acf2-2f61fc716fd1": {
    similarRoles: [
      "Office Administrator",
      "Receptionist",
      "Administrative Assistant",
    ],
    usefulExperience: [
      "updating records and systems",
      "producing documents and reports",
      "handling enquiries and dealing with different people",
    ],
    plainEnglish:
      "This is mainly an office administration role helping the school run day to day, with data, paperwork, stakeholder contact and some reception work.",
  },
  "teaching-vacancies-attendance-officer-1cc7b9ae-114c-4858-8cb8-4caae38307df": {
    similarRoles: [
      "Customer Service Adviser",
      "Case Administrator",
      "Records Administrator",
    ],
    usefulExperience: [
      "maintaining accurate records",
      "following up issues with customers or clients",
      "handling sensitive conversations",
      "coordinating with different people",
    ],
    plainEnglish:
      "This is an administration and people-contact role: monitoring attendance, following up concerns, keeping records accurate and dealing with families, staff and outside organisations.",
  },
  "teaching-vacancies-data-and-exams-officer-park-high-school-stanmore": {
    similarRoles: [
      "Data Administrator",
      "Reporting Administrator",
      "Operations Coordinator",
    ],
    usefulExperience: [
      "maintaining accurate data",
      "producing reports and information",
      "managing deadlines",
      "coordinating complex processes",
    ],
    plainEnglish:
      "This is a data administration and operational coordination role, with responsibility for keeping school information accurate and helping run the examinations process.",
  },
  "teaching-vacancies-ehcp-administrator-lime-academy-ravensbourne": {
    similarRoles: [
      "Case Administrator",
      "Records Administrator",
      "Service Coordinator",
    ],
    usefulExperience: [
      "managing confidential records",
      "coordinating paperwork and deadlines",
      "dealing with customers or service users",
      "liaising with different organisations",
    ],
    plainEnglish:
      "This is mainly a case administration role supporting pupils with Education, Health and Care Plans, keeping records accurate and coordinating information between families, school staff and other services.",
  },
  "teaching-vacancies-administrator-and-cover-coordinator": {
    similarRoles: [
      "Office Administrator",
      "Scheduling Coordinator",
      "Operations Administrator",
    ],
    usefulExperience: [
      "diary or schedule management",
      "coordinating staff cover",
      "maintaining records",
      "handling last-minute changes",
    ],
    plainEnglish:
      "This is an administration and scheduling role, with responsibility for organising staff cover as well as general school administration.",
  },
  "teaching-vacancies-pupil-records-administrator": {
    similarRoles: [
      "Records Administrator",
      "Data Administrator",
      "Office Administrator",
    ],
    usefulExperience: [
      "maintaining accurate records",
      "data entry and checking",
      "handling confidential information",
      "updating systems",
    ],
    plainEnglish:
      "This is a records and data administration role focused on keeping pupil information accurate, complete and up to date.",
  },
  "teaching-vacancies-wg6-administrator-wilmington-grammar-school-for-girls": {
    similarRoles: [
      "Office Administrator",
      "Team Administrator",
      "Business Support Administrator",
    ],
    usefulExperience: [
      "general office administration",
      "handling enquiries",
      "maintaining records",
      "coordinating routine tasks",
    ],
    plainEnglish:
      "Despite the unfamiliar title, this is essentially an administrative support role within the school.",
  },
  "teaching-vacancies-administrative-assistant-welfare-reception-attendance": {
    similarRoles: [
      "Receptionist",
      "Customer Service Administrator",
      "Office Administrator",
    ],
    usefulExperience: [
      "front-desk enquiries",
      "maintaining records",
      "handling sensitive conversations",
      "general administration",
    ],
    plainEnglish:
      "This combines reception and office administration with pupil attendance and welfare support.",
  },
  "teaching-vacancies-hr-administrator-the-diocese-of-canterbury-academies-trust": {
    similarRoles: [
      "HR Administrator",
      "People Administrator",
      "Recruitment Administrator",
    ],
    usefulExperience: [
      "employee records",
      "recruitment administration",
      "confidential information",
      "HR systems and paperwork",
    ],
    plainEnglish:
      "This is a conventional HR administration role carried out within a schools trust rather than a private company.",
  },
  "teaching-vacancies-receptionist-nore-academy": {
    similarRoles: [
      "Receptionist",
      "Front of House Assistant",
      "Customer Service Adviser",
    ],
    usefulExperience: [
      "handling enquiries",
      "greeting visitors",
      "phone and email communication",
      "routine administration",
    ],
    plainEnglish:
      "This is a front-of-house and customer-service role in a school setting, with some general administrative duties.",
  },
};

export function getTransferableFit(jobId: string): TransferableFit | undefined {
  return TRIAL_FITS[jobId];
}

export function getTransferableFitTrialJobIds(): string[] {
  return Object.keys(TRIAL_FITS);
}

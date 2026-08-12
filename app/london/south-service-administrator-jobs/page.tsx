import type { Metadata } from "next";
import LondonAdminAreaPage, {
  londonAreaDetails,
} from "@/components/LondonAdminAreaPage";

const details = londonAreaDetails.south;
const canonicalUrl =
  "https://www.ontapjobsearch.com/london/south-service-administrator-jobs";

export const metadata: Metadata = {
  title: `${details.title} | Ontap Job Search`,
  description: details.description,
  alternates: { canonical: canonicalUrl },
};

export default function Page() {
  return <LondonAdminAreaPage area="south" />;
}

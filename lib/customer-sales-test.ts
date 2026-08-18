import fs from "node:fs";
import path from "node:path";

export type CustomerSalesTestJob = {
  job_id: string;
  title: string;
  company?: string;
  advertiser_name?: string;
  location?: string;
  region?: string;
  salary_text?: string;
  employment_type?: string;
  description?: string;
  full_description?: string;
  working_arrangement?: string;
  working_arrangement_text?: string;
  apply_url: string;
  source?: string;
  customer_sales_classification?: string;
  customer_sales_reason?: string;
};

export type CustomerSalesTestSlice = {
  slug: string;
  label: string;
  sourceFile: string;
};

export const CUSTOMER_SALES_TEST_SLICES: CustomerSalesTestSlice[] = [
  {
    slug: "hampshire",
    label: "Hampshire",
    sourceFile: "pipeline/output-customer-sales-test/hampshire.json",
  },
  {
    slug: "manchester-salford",
    label: "Manchester & Salford",
    sourceFile: "pipeline/output-customer-sales-test/manchester-salford.json",
  },
  {
    slug: "west-yorkshire",
    label: "West Yorkshire",
    sourceFile: "pipeline/output-customer-sales-test/west-yorkshire.json",
  },
];

function clean(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function readJobs(relativeFile: string): CustomerSalesTestJob[] {
  const filePath = path.join(process.cwd(), relativeFile);
  if (!fs.existsSync(filePath)) return [];

  try {
    const parsed = JSON.parse(fs.readFileSync(filePath, "utf8"));
    if (!Array.isArray(parsed)) return [];
    return parsed.filter((row): row is CustomerSalesTestJob => {
      if (!row || typeof row !== "object") return false;
      const job = row as Record<string, unknown>;
      return Boolean(clean(job.job_id) && clean(job.title) && clean(job.apply_url));
    });
  } catch {
    return [];
  }
}

export function getCustomerSalesTestSlice(slug: string) {
  const slice = CUSTOMER_SALES_TEST_SLICES.find((item) => item.slug === slug);
  if (!slice) return undefined;

  const jobs = readJobs(slice.sourceFile).sort((a, b) => {
    const aRank = a.customer_sales_classification === "HIGH_CONFIDENCE" ? 0 : 1;
    const bRank = b.customer_sales_classification === "HIGH_CONFIDENCE" ? 0 : 1;
    if (aRank !== bRank) return aRank - bRank;
    return a.title.localeCompare(b.title);
  });

  return { ...slice, jobs };
}

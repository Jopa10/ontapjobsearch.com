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
  customer_sales_overlap_policy?: string;
};

export type CustomerSalesTestSlice = {
  slug: string;
  label: string;
  sourceFile: string;
};

export type CustomerSalesEmployerMetric = {
  name: string;
  count: number;
  share: number;
};

export type CustomerSalesDuplicateGroup = {
  key: string;
  count: number;
  title: string;
  employer: string;
  location: string;
};

export const CUSTOMER_SALES_TEST_SLICES: CustomerSalesTestSlice[] = [
  { slug: "hampshire", label: "Hampshire", sourceFile: "pipeline/output-customer-sales-test/hampshire.json" },
  { slug: "manchester-salford", label: "Manchester & Salford", sourceFile: "pipeline/output-customer-sales-test/manchester-salford.json" },
  { slug: "west-yorkshire", label: "West Yorkshire", sourceFile: "pipeline/output-customer-sales-test/west-yorkshire.json" },
];

function clean(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function normalise(value: unknown): string {
  return clean(value).toLowerCase().replace(/\s+/g, " ");
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

function summariseJobs(jobs: CustomerSalesTestJob[]) {
  const employerCounts = new Map<string, { name: string; count: number }>();
  const duplicateCounts = new Map<string, CustomerSalesDuplicateGroup>();
  const classificationCounts = new Map<string, number>();

  for (const job of jobs) {
    const employer = clean(job.advertiser_name) || clean(job.company) || "Unknown employer";
    const employerKey = normalise(employer) || "unknown employer";
    const existingEmployer = employerCounts.get(employerKey);
    employerCounts.set(employerKey, {
      name: existingEmployer?.name || employer,
      count: (existingEmployer?.count || 0) + 1,
    });

    const classification = clean(job.customer_sales_classification) || "UNCLASSIFIED";
    classificationCounts.set(classification, (classificationCounts.get(classification) || 0) + 1);

    const title = clean(job.title);
    const location = clean(job.location);
    const duplicateKey = [normalise(employer), normalise(title), normalise(location)].join("|");
    const existingDuplicate = duplicateCounts.get(duplicateKey);
    duplicateCounts.set(duplicateKey, {
      key: duplicateKey,
      count: (existingDuplicate?.count || 0) + 1,
      title,
      employer,
      location,
    });
  }

  const topEmployers: CustomerSalesEmployerMetric[] = [...employerCounts.values()]
    .map((item) => ({
      ...item,
      share: jobs.length ? item.count / jobs.length : 0,
    }))
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));

  const duplicateGroups = [...duplicateCounts.values()]
    .filter((group) => group.count > 1)
    .sort((a, b) => b.count - a.count || a.title.localeCompare(b.title));

  const campaignEmployers = topEmployers.filter((item) => item.count >= 3);
  const dominantEmployer = topEmployers.find((item) => item.share >= 0.4);

  return {
    employerCount: employerCounts.size,
    topEmployers,
    campaignEmployers,
    dominantEmployer,
    duplicateGroups,
    classificationCounts: [...classificationCounts.entries()]
      .map(([classification, count]) => ({ classification, count }))
      .sort((a, b) => b.count - a.count || a.classification.localeCompare(b.classification)),
  };
}

export function getCustomerSalesTestSlice(slug: string) {
  const slice = CUSTOMER_SALES_TEST_SLICES.find((item) => item.slug === slug);
  if (!slice) return undefined;
  const jobs = readJobs(slice.sourceFile).sort((a, b) => {
    const aRank = a.customer_sales_classification === "DIRECT_SALES" ? 0 : 1;
    const bRank = b.customer_sales_classification === "DIRECT_SALES" ? 0 : 1;
    if (aRank !== bRank) return aRank - bRank;
    return a.title.localeCompare(b.title);
  });
  return { ...slice, jobs, stats: summariseJobs(jobs) };
}

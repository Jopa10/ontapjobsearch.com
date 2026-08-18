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
};

export type CustomerSalesTestSlice = {
  slug: string;
  label: string;
  sourceFiles: string[];
  regionMatches: string[];
};

export const CUSTOMER_SALES_TEST_SLICES: CustomerSalesTestSlice[] = [
  {
    slug: "hampshire",
    label: "Hampshire",
    sourceFiles: ["app/hampshire/service-administrator-jobs.json"],
    regionMatches: ["hampshire"],
  },
  {
    slug: "manchester-salford",
    label: "Manchester & Salford",
    sourceFiles: [
      "app/_city-pages/configured-slices/manchester-salford/service-administrator-jobs.json",
      "pipeline/output-admin-service/manchester-salford-admin-service.json",
    ],
    regionMatches: ["manchester & salford", "manchester and salford", "greater manchester - manchester & salford"],
  },
  {
    slug: "west-yorkshire",
    label: "West Yorkshire",
    sourceFiles: [
      "app/west-yorkshire/service-administrator-jobs.json",
      "pipeline/output-admin-service/west-yorkshire-admin-service.json",
    ],
    regionMatches: ["west yorkshire", "yorkshire - west"],
  },
];

const STRONG_TITLE_TERMS = [
  "sales advisor",
  "sales adviser",
  "customer sales",
  "sales consultant",
  "telesales",
  "inside sales",
  "inbound sales",
  "outbound sales",
  "sales agent",
  "telephone sales",
  "new business advisor",
  "new business adviser",
  "retention advisor",
  "retention adviser",
  "renewals advisor",
  "renewals adviser",
];

const POSSIBLE_TITLE_TERMS = [
  "customer advisor",
  "customer adviser",
  "customer account advisor",
  "customer account adviser",
  "client advisor",
  "client adviser",
  "membership advisor",
  "membership adviser",
  "contact centre advisor",
  "contact centre adviser",
];

const SALES_EVIDENCE_TERMS = [
  "sales target",
  "sales targets",
  "sales opportunity",
  "sales opportunities",
  "convert enquiries",
  "convert inquiries",
  "conversion target",
  "conversion targets",
  "upsell",
  "up-sell",
  "cross-sell",
  "cross sell",
  "warm leads",
  "warm enquiries",
  "warm inquiries",
  "inbound enquiries",
  "inbound inquiries",
  "outbound calls",
  "commission",
  "bonus for sales",
  "new business",
];

const OFFICE_EVIDENCE_TERMS = [
  "contact centre",
  "contact center",
  "call centre",
  "call center",
  "office based",
  "office-based",
  "telephone",
  "phone",
  "inbound",
  "outbound",
  "hybrid",
  "work from home",
  "working from home",
  "remote",
];

const HARD_EXCLUDE_TERMS = [
  "field sales",
  "door to door",
  "door-to-door",
  "territory sales",
  "area sales",
  "regional sales",
  "car sales",
  "vehicle sales",
  "showroom",
  "retail sales",
  "sales administrator",
  "sales administration",
  "sales support administrator",
  "sales ledger",
  "business development manager",
  "account manager",
  "sales manager",
];

function clean(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function lower(value: unknown): string {
  return clean(value).toLowerCase();
}

function includesAny(text: string, terms: string[]): boolean {
  return terms.some((term) => text.includes(term));
}

function isCustomerSalesJob(job: CustomerSalesTestJob): boolean {
  const title = lower(job.title);
  const description = `${lower(job.full_description)} ${lower(job.description)}`;
  const combined = `${title} ${description}`;

  if (includesAny(title, HARD_EXCLUDE_TERMS)) return false;

  const strongTitle = includesAny(title, STRONG_TITLE_TERMS);
  const possibleTitle = includesAny(title, POSSIBLE_TITLE_TERMS);
  const salesEvidence = includesAny(combined, SALES_EVIDENCE_TERMS);

  if (!strongTitle && !(possibleTitle && salesEvidence)) return false;

  const arrangement = `${lower(job.working_arrangement)} ${lower(job.working_arrangement_text)}`;
  const officeEvidence = includesAny(combined, OFFICE_EVIDENCE_TERMS) ||
    includesAny(arrangement, ["hybrid", "remote", "home"]);

  // Strongly sales-led titles can survive missing workplace wording because many
  // JobG8 adverts omit it. Borderline customer-advisor titles must show both
  // genuine sales evidence and an office/contact-centre/home signal.
  return strongTitle || officeEvidence;
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

  const byId = new Map<string, CustomerSalesTestJob>();
  for (const file of slice.sourceFiles) {
    for (const job of readJobs(file)) {
      const region = lower(job.region);
      const location = lower(job.location);
      const inRegion = slice.regionMatches.some(
        (match) => region.includes(match) || location.includes(match)
      );
      if (!inRegion || !isCustomerSalesJob(job)) continue;
      if (!byId.has(job.job_id)) byId.set(job.job_id, job);
    }
  }

  const jobs = [...byId.values()].sort((a, b) => {
    const aStrong = includesAny(lower(a.title), STRONG_TITLE_TERMS) ? 0 : 1;
    const bStrong = includesAny(lower(b.title), STRONG_TITLE_TERMS) ? 0 : 1;
    if (aStrong !== bStrong) return aStrong - bStrong;
    return lower(a.title).localeCompare(lower(b.title));
  });

  return { ...slice, jobs };
}

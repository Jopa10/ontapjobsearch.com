import fs from "node:fs";
import path from "node:path";
import {
  cityPageDefinitions,
  getCityPageJobs,
  isCityPageActive,
  type CityPageDefinition,
} from "@/lib/city-page-data";
import { type PublishedJob } from "@/lib/published-jobs";
import { getDiscoveryRecommendations } from "@/lib/discovery-recommendations";

type LedgerJob = Pick<PublishedJob, "job_id" | "title" | "location" | "region" | "category" | "source">;

export type ExpiredJobRecovery = {
  job: LedgerJob;
  cityPage?: CityPageDefinition;
  primaryLink: { href: string; label: string };
  secondaryLink: { href: string; label: string };
  recommendations: PublishedJob[];
};

const LEDGER_PATH = path.join(process.cwd(), "pipeline", "reports-daily", "published-job-first-seen-history.csv");
const ROLE_RULES_PATH = path.join(process.cwd(), "pipeline", "registers", "role_relationships.csv");

function normalise(value: string): string {
  return value.toLocaleLowerCase("en-GB").replace(/[^a-z0-9]+/g, " ").trim();
}

function parseCsv(input: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let value = "";
  let quoted = false;
  for (let index = 0; index < input.length; index += 1) {
    const char = input[index];
    if (quoted) {
      if (char === '"' && input[index + 1] === '"') {
        value += '"';
        index += 1;
      } else if (char === '"') quoted = false;
      else value += char;
    } else if (char === '"') quoted = true;
    else if (char === ",") {
      row.push(value);
      value = "";
    } else if (char === "\n") {
      row.push(value.replace(/\r$/, ""));
      rows.push(row);
      row = [];
      value = "";
    } else value += char;
  }
  if (value || row.length) rows.push([...row, value.replace(/\r$/, "")]);
  return rows;
}

export function getFormerPublishedJob(jobId: string): LedgerJob | undefined {
  if (!fs.existsSync(LEDGER_PATH)) return undefined;
  const [header, ...rows] = parseCsv(fs.readFileSync(LEDGER_PATH, "utf8"));
  const columns = new Map(header?.map((name, index) => [name, index]) ?? []);
  const read = (row: string[], name: string) => row[columns.get(name) ?? -1]?.trim() ?? "";
  let decodedId = jobId;
  try { decodedId = decodeURIComponent(jobId); } catch { /* Retain the supplied ID. */ }
  const row = rows.find((candidate) => read(candidate, "job_id") === decodedId);
  if (!row) return undefined;
  return {
    job_id: decodedId,
    title: read(row, "title"),
    location: read(row, "location"),
    region: read(row, "region"),
    category: read(row, "category"),
    source: read(row, "source"),
  };
}

function cityFor(job: LedgerJob): CityPageDefinition | undefined {
  const location = normalise(job.location.split(",")[0] ?? job.location);
  return cityPageDefinitions.find((definition) =>
    isCityPageActive(definition) && normalise(definition.displayName) === location
  );
}

function categoryFamily(category: string): string {
  const value = normalise(category);
  if (value.includes("admin service") || value.includes("office support")) return "admin_service";
  if (value.includes("customer service") || value.includes("contact centre")) return "customer_service_contact_centre";
  if (value.includes("customer sales") || value.includes("sales advisor")) return "customer_sales";
  if (value.includes("hr") || value.includes("recruitment")) return "hr_recruitment";
  if (value.includes("support worker")) return "support_worker";
  return value.replace(/ /g, "_");
}

function governedTargetFamilies(title: string): Set<string> {
  if (!fs.existsSync(ROLE_RULES_PATH)) return new Set();
  const [header, ...rows] = parseCsv(fs.readFileSync(ROLE_RULES_PATH, "utf8"));
  const columns = new Map(header?.map((name, index) => [name, index]) ?? []);
  const read = (row: string[], name: string) => row[columns.get(name) ?? -1]?.trim() ?? "";
  return new Set(rows
    .filter((row) => normalise(read(row, "source_role")) === normalise(title))
    .filter((row) => read(row, "status") === "APPROVED" && read(row, "active").toUpperCase() === "TRUE")
    .map((row) => read(row, "target_family"))
    .filter(Boolean));
}

function asPublishedJob(job: LedgerJob, slicePath: string, sliceLabel: string): PublishedJob {
  return {
    ...job,
    company: "", advertiser_name: "", advertiser_type: "", country: "UK",
    employment_type: "", salary_min: "", salary_max: "", salary_period: "",
    salary_text: "", work_pattern: "", posted_date: "", posted_date_basis: "",
    closing_date: "", closing_datetime: "", description: "", full_description: "",
    apply_url: "", working_arrangement: "", working_arrangement_text: "",
    working_arrangement_evidence: "", slice_path: slicePath, slice_label: sliceLabel,
  };
}

export function getExpiredJobRecovery(jobId: string, currentJobs: PublishedJob[]): ExpiredJobRecovery | undefined {
  const job = getFormerPublishedJob(jobId);
  if (!job) return undefined;
  const cityPage = cityFor(job);
  const regionJobs = currentJobs.filter((candidate) => normalise(candidate.region) === normalise(job.region));
  const regional = regionJobs[0];
  const regionalHref = cityPage?.parentRoute ?? regional?.slice_path ?? "/browse-jobs";
  const regionalLabel = regional?.slice_label || job.region || "current jobs";
  const source = asPublishedJob(job, regionalHref, regionalLabel);
  const nearby = getDiscoveryRecommendations(source, currentJobs, 6);
  const cityIds = new Set(cityPage ? getCityPageJobs(cityPage).map((candidate) => candidate.job_id) : []);
  const sameCity = currentJobs.filter((candidate) => cityIds.has(candidate.job_id));
  const targetFamilies = governedTargetFamilies(job.title);
  const relevantCity = sameCity.filter((candidate) => targetFamilies.has(categoryFamily(candidate.category)));
  const sameFamilyRegional = regionJobs.filter((candidate) =>
    normalise(candidate.category) === normalise(job.category) && candidate.job_id !== job.job_id
  );
  const recommendations = [...nearby, ...relevantCity, ...sameFamilyRegional, ...sameCity, ...regionJobs]
    .filter((candidate, index, all) => all.findIndex((row) => row.job_id === candidate.job_id) === index)
    .slice(0, 6);
  return {
    job,
    cityPage,
    primaryLink: cityPage
      ? { href: cityPage.route, label: `View ${cityPage.displayName} admin jobs` }
      : { href: regionalHref, label: `View ${regionalLabel}` },
    secondaryLink: {
      href: regionalHref,
      label: `View ${(job.region.split(" - ")[0] || job.region || "regional")} jobs`,
    },
    recommendations,
  };
}

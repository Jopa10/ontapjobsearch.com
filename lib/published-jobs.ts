import fs from "node:fs";
import path from "node:path";
import { isLondonJob } from "@/lib/london-job-area";
import { normaliseJobTitle } from "@/lib/job-title";
import {
  getConfiguredSliceBySlugs,
  getPublishedDynamicSlices,
} from "@/lib/configured-job-slices";

export type PublishedJob = {
  job_id: string;
  title: string;
  company: string;
  advertiser_name: string;
  advertiser_type: string;
  location: string;
  region: string;
  country: string;
  category: string;
  employment_type: string;
  salary_min: string;
  salary_max: string;
  salary_period: string;
  salary_text: string;
  work_pattern: string;
  posted_date: string;
  posted_date_basis: string;
  closing_date: string;
  closing_datetime: string;
  description: string;
  full_description: string;
  apply_url: string;
  source: string;
  working_arrangement: string;
  working_arrangement_text: string;
  working_arrangement_evidence: string;
  slice_path: string;
  slice_label: string;
};

const APP_DIRECTORY = path.join(process.cwd(), "app");
const DERIVED_CITY_DATA_DIRECTORY = "_city-pages";
const CONFIGURED_CITY_DATA_PREFIX = "_city-pages/configured-slices/";

function text(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function jsonFiles(directory: string): string[] {
  if (!fs.existsSync(directory)) return [];

  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    if (entry.isDirectory() && entry.name === DERIVED_CITY_DATA_DIRECTORY) return [];

    const entryPath = path.join(directory, entry.name);
    if (entry.isDirectory()) return jsonFiles(entryPath);
    return entry.isFile() && entry.name.endsWith(".json") ? [entryPath] : [];
  });
}

function isPublishedJob(value: unknown): value is Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return false;
  const row = value as Record<string, unknown>;
  return Boolean(text(row.job_id) && text(row.title) && text(row.apply_url));
}

function sourceSlice(
  filePath: string,
  region: string,
  row: Record<string, unknown>
) {
  const jsonRoute = path
    .relative(APP_DIRECTORY, filePath)
    .replace(/\\/g, "/")
    .replace(/\.json$/, "");
  const candidates = [jsonRoute];

  if (jsonRoute.startsWith(CONFIGURED_CITY_DATA_PREFIX)) {
    const parts = jsonRoute.split("/");
    const regionSlug = parts[2];
    const categorySlug = parts[3];
    const configured = getConfiguredSliceBySlugs(regionSlug, categorySlug);
    if (configured) {
      return { path: configured.route, label: configured.title };
    }
  }

  if (jsonRoute === "london/service-administrator-jobs") {
    const londonJob = {
      title: normaliseJobTitle(text(row.title)),
      location: text(row.location),
      description: text(row.full_description) || text(row.description),
    };

    if (!isLondonJob(londonJob)) {
      return {
        path: "/browse-jobs",
        label: "Browse jobs",
      };
    }

    // Keep the job-detail backlink stable on the London-wide parent. The
    // London sub-area pages are filtered views of the same underlying feed.
    return {
      path: "/london/service-administrator-jobs",
      label: "London Admin & Customer Service Jobs",
    };
  }

  if (jsonRoute.endsWith("-jobs")) {
    candidates.push(jsonRoute.slice(0, -"-jobs".length));
  }

  for (const route of candidates) {
    const pagePath = path.join(APP_DIRECTORY, ...route.split("/"), "page.tsx");
    if (!fs.existsSync(pagePath)) continue;

    let label = region ? `${region} Jobs` : "Browse jobs";
    try {
      const pageSource = fs.readFileSync(pagePath, "utf8");
      const titleMatch = pageSource.match(/\btitle="([^"]+)"/);
      if (titleMatch) label = titleMatch[1];
    } catch {
      // The route still exists, so retain the region-based fallback label.
    }

    if (route.endsWith("/service-administrator-jobs")) {
      label = `${region || "London"} Admin & Customer Service Jobs`;
    }

    return { path: `/${route}`, label };
  }

  return { path: "/browse-jobs", label: "Browse jobs" };
}

function normaliseJob(row: Record<string, unknown>, filePath: string): PublishedJob {
  const description = text(row.full_description) || text(row.description);
  const slice = sourceSlice(filePath, text(row.region), row);

  return {
    job_id: text(row.job_id),
    title: normaliseJobTitle(text(row.title)),
    company: text(row.company),
    advertiser_name: text(row.advertiser_name),
    advertiser_type: text(row.advertiser_type),
    location: text(row.location),
    region: text(row.region),
    country: text(row.country) || "UK",
    category: text(row.category),
    employment_type: text(row.employment_type),
    salary_min: text(row.salary_min),
    salary_max: text(row.salary_max),
    salary_period: text(row.salary_period),
    salary_text: text(row.salary_text),
    work_pattern: text(row.work_pattern),
    posted_date: text(row.posted_date),
    posted_date_basis: text(row.posted_date_basis),
    closing_date: text(row.closing_date),
    closing_datetime: text(row.closing_datetime),
    description,
    full_description: description,
    apply_url: text(row.apply_url),
    source: text(row.source) || "JobG8",
    working_arrangement: text(row.working_arrangement),
    working_arrangement_text: text(row.working_arrangement_text),
    working_arrangement_evidence: text(row.working_arrangement_evidence),
    slice_path: slice.path,
    slice_label: slice.label,
  };
}

function addPublishedFile(filePath: string, byId: Map<string, PublishedJob>) {
  let parsed: unknown;
  try {
    parsed = JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return;
  }

  if (!Array.isArray(parsed)) return;
  for (const row of parsed) {
    if (!isPublishedJob(row)) continue;
    const job = normaliseJob(row, filePath);
    if (job.region.toLowerCase() === "london" && !isLondonJob(job)) {
      continue;
    }
    if (!byId.has(job.job_id)) byId.set(job.job_id, job);
  }
}

let cachedJobs: PublishedJob[] | undefined;

export function getPublishedJobs(): PublishedJob[] {
  if (cachedJobs) return cachedJobs;

  const byId = new Map<string, PublishedJob>();

  // Established static slice JSON. Derived city data is intentionally skipped by
  // jsonFiles(), as before.
  for (const filePath of jsonFiles(APP_DIRECTORY).sort()) {
    addPublishedFile(filePath, byId);
  }

  // Configured slice data lives under the otherwise-skipped _city-pages tree so
  // the existing city-data commit stage can carry it safely. Only LIVE,
  // non-empty configured slices are admitted here.
  for (const slice of getPublishedDynamicSlices()) {
    addPublishedFile(slice.dataFilePath, byId);
  }

  cachedJobs = [...byId.values()].sort((a, b) => a.job_id.localeCompare(b.job_id));
  return cachedJobs;
}

export function decodePublishedJobId(jobId: string): string {
  try {
    return decodeURIComponent(jobId);
  } catch {
    return jobId;
  }
}

export function getPublishedJob(jobId: string): PublishedJob | undefined {
  const decodedJobId = decodePublishedJobId(jobId);
  return getPublishedJobs().find((job) => job.job_id === decodedJobId);
}

export function getJobPath(jobId: string): string {
  return `/jobs/${encodeURIComponent(jobId)}`;
}

import fs from "node:fs";
import path from "node:path";
import { getLondonJobArea } from "@/lib/london-job-area";

export type PublishedJob = {
  job_id: string;
  title: string;
  company: string;
  location: string;
  region: string;
  country: string;
  category: string;
  employment_type: string;
  salary_min: string;
  salary_max: string;
  salary_text: string;
  posted_date: string;
  description: string;
  full_description: string;
  apply_url: string;
  source: string;
  working_arrangement: string;
  working_arrangement_text: string;
  slice_path: string;
  slice_label: string;
};

const APP_DIRECTORY = path.join(process.cwd(), "app");

function text(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function jsonFiles(directory: string): string[] {
  if (!fs.existsSync(directory)) return [];

  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
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

  if (jsonRoute === "london/service-administrator-jobs") {
    const londonArea = getLondonJobArea({
      title: text(row.title),
      location: text(row.location),
      description: text(row.full_description) || text(row.description),
    });

    if (londonArea === "outer") {
      return {
        path: "/london/outer-service-administrator-jobs",
        label: "Outer London Admin & Customer Service Jobs",
      };
    }

    return {
      path: "/london/service-administrator-jobs",
      label: "Central & Inner London Admin & Customer Service Jobs",
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
    title: text(row.title),
    company: text(row.company),
    location: text(row.location),
    region: text(row.region),
    country: text(row.country) || "UK",
    category: text(row.category),
    employment_type: text(row.employment_type),
    salary_min: text(row.salary_min),
    salary_max: text(row.salary_max),
    salary_text: text(row.salary_text),
    posted_date: text(row.posted_date),
    description,
    full_description: description,
    apply_url: text(row.apply_url),
    source: text(row.source) || "JobG8",
    working_arrangement: text(row.working_arrangement),
    working_arrangement_text: text(row.working_arrangement_text),
    slice_path: slice.path,
    slice_label: slice.label,
  };
}

let cachedJobs: PublishedJob[] | undefined;

export function getPublishedJobs(): PublishedJob[] {
  if (cachedJobs) return cachedJobs;

  const byId = new Map<string, PublishedJob>();

  for (const filePath of jsonFiles(APP_DIRECTORY).sort()) {
    let parsed: unknown;
    try {
      parsed = JSON.parse(fs.readFileSync(filePath, "utf8"));
    } catch {
      continue;
    }

    if (!Array.isArray(parsed)) continue;
    for (const row of parsed) {
      if (!isPublishedJob(row)) continue;
      const job = normaliseJob(row, filePath);
      if (!byId.has(job.job_id)) byId.set(job.job_id, job);
    }
  }

  cachedJobs = [...byId.values()].sort((a, b) => a.job_id.localeCompare(b.job_id));
  return cachedJobs;
}

export function getPublishedJob(jobId: string): PublishedJob | undefined {
  return getPublishedJobs().find((job) => job.job_id === jobId);
}

export function getJobPath(jobId: string): string {
  return `/jobs/${encodeURIComponent(jobId)}`;
}

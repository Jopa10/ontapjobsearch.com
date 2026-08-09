import fs from "node:fs";
import path from "node:path";

export type CityPageJob = {
  job_id?: string;
  title?: string;
  company?: string;
  location?: string;
  salary_text?: string;
  employment_type?: string;
  posted_date?: string;
  description?: string;
  full_description?: string;
  apply_url?: string;
  [key: string]: unknown;
};

export type CityPageDefinition = {
  key: string;
  route: string;
  listingLabel: string;
  jsonPath: readonly string[];
  /** Retention gate used by existing navigation/sitemap code. Active pages use 0. */
  minimumJobs: number;
  /** Human-approval launch threshold; this does not delist an active page. */
  launchMinimumJobs?: number;
  /** Explicit activation is the permanent-page switch. */
  active?: boolean;
};

export type ActiveCityPage = {
  definition: CityPageDefinition;
  jobs: CityPageJob[];
};

export const newcastleServiceAdministratorPage: CityPageDefinition = {
  key: "newcastle-service-administrator",
  route: "/newcastle/service-administrator-jobs",
  listingLabel: "Newcastle Admin & Customer Service jobs",
  jsonPath: ["app", "_city-pages", "newcastle", "service-administrator-jobs.json"],
  minimumJobs: 0,
  launchMinimumJobs: 6,
  active: true,
};

export const cityPageDefinitions: readonly CityPageDefinition[] = [
  newcastleServiceAdministratorPage,
];

function usableJob(value: unknown): value is CityPageJob {
  if (!value || typeof value !== "object" || Array.isArray(value)) return false;
  const row = value as CityPageJob;
  return Boolean(
    typeof row.job_id === "string" &&
      row.job_id.trim() &&
      typeof row.title === "string" &&
      row.title.trim()
  );
}

export function getCityPageJobs(
  definition: CityPageDefinition = newcastleServiceAdministratorPage
): CityPageJob[] {
  const filePath = path.join(process.cwd(), ...definition.jsonPath);
  if (!fs.existsSync(filePath)) return [];

  try {
    const parsed: unknown = JSON.parse(fs.readFileSync(filePath, "utf8"));
    if (!Array.isArray(parsed)) return [];
    return parsed.filter(usableJob);
  } catch {
    return [];
  }
}

export function cityPageContainsJob(
  definition: CityPageDefinition,
  jobs: CityPageJob[],
  jobId: string
): boolean {
  if (definition.active === false) return false;
  if (definition.active !== true && jobs.length < definition.minimumJobs) return false;
  return jobs.some((job) => job.job_id === jobId);
}

export function getActiveCityPageForJob(jobId: string): ActiveCityPage | null {
  for (const definition of cityPageDefinitions) {
    const jobs = getCityPageJobs(definition);
    if (cityPageContainsJob(definition, jobs, jobId)) {
      return { definition, jobs };
    }
  }
  return null;
}

export function isCityPageActive(
  definition: CityPageDefinition = newcastleServiceAdministratorPage
): boolean {
  if (definition.active === true) return true;
  if (definition.active === false) return false;
  return getCityPageJobs(definition).length >= definition.minimumJobs;
}

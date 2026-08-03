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
  jsonPath: readonly string[];
  minimumJobs: number;
};

export const newcastleServiceAdministratorPage: CityPageDefinition = {
  key: "newcastle-service-administrator",
  route: "/newcastle/service-administrator-jobs",
  jsonPath: ["app", "_city-pages", "newcastle", "service-administrator-jobs.json"],
  minimumJobs: 8,
};

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

export function isCityPageActive(
  definition: CityPageDefinition = newcastleServiceAdministratorPage
): boolean {
  return getCityPageJobs(definition).length >= definition.minimumJobs;
}

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
  displayName: string;
  categoryLabel: string;
  route: string;
  listingLabel: string;
  jsonPath: readonly string[];
  parentRoute: string;
  /** Retention gate used by existing navigation/sitemap code. Active pages use 0. */
  minimumJobs: number;
  /** Human-approval launch threshold; this does not delist an active page. */
  launchMinimumJobs?: number;
  /** Explicit activation is the permanent-page switch. */
  active?: boolean;
};

export type CityPageBreadcrumb = {
  cityLabel: string;
  cityRoute: string;
  parentLabel: string;
  parentRoute: string;
  roleLabel: string;
  roleRoute: string;
};

export type ActiveCityPage = {
  definition: CityPageDefinition;
  jobs: CityPageJob[];
};

type TechnicalCityPage = {
  city_key?: unknown;
  display_name?: unknown;
  category_label?: unknown;
  parent_page?: unknown;
  output_json?: unknown;
  route?: unknown;
  minimum_live_jobs?: unknown;
  launch_minimum_live_jobs?: unknown;
  lifecycle_state?: unknown;
};

function usableText(value: unknown): value is string {
  return typeof value === "string" && Boolean(value.trim());
}

function parentRouteFromPage(value: string): string {
  const configuredPrefix = "app/_city-pages/configured-slices/";
  if (value.startsWith(configuredPrefix)) {
    return `/job-search/${value.slice(configuredPrefix.length).replace(/\.json$/, "")}`;
  }
  let route = `/${value.replace(/^app\//, "").replace(/\.json$/, "")}`;
  if (route.endsWith("/support-worker-jobs")) route = route.replace(/-jobs$/, "");
  return route;
}

const parentLabels: Record<string, string> = {
  "birmingham-solihull": "Birmingham & Solihull",
  "bristol-bath": "Bristol & Bath",
  "cardiff-vale": "Cardiff & Vale",
  "coventry-warwickshire": "Coventry & Warwickshire",
  "east-yorkshire": "East Yorkshire",
  "edinburgh-lothians": "Edinburgh & Lothians",
  glasgow: "Glasgow",
  hampshire: "Hampshire",
  "manchester-salford": "Manchester & Salford",
  "merseyside-liverpool": "Merseyside & Liverpool",
  "north-east": "North East",
  "north-yorkshire": "North Yorkshire",
  "northern-ireland-east": "Northern Ireland East",
  oxfordshire: "Oxfordshire",
  "south-yorkshire": "South Yorkshire",
  sussex: "Sussex",
  "warrington-halton": "Warrington & Halton",
  "west-yorkshire": "West Yorkshire",
};

function parentLabelFromRoute(route: string): string {
  const parts = route.split("/").filter(Boolean);
  const regionSlug = parts[0] === "job-search" ? parts[1] : parts[0];
  return (
    parentLabels[regionSlug] ||
    regionSlug
      .split("-")
      .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
      .join(" ")
  );
}

function roleBreadcrumb(
  categoryLabel: string
): Pick<CityPageBreadcrumb, "roleLabel" | "roleRoute"> {
  if (categoryLabel.toLowerCase().includes("support worker")) {
    return {
      roleLabel: "Support Worker jobs",
      roleRoute: "/browse-jobs#support-worker-jobs",
    };
  }
  return {
    roleLabel: "Service Administrator jobs",
    roleRoute: "/browse-jobs#admin-service-jobs",
  };
}

function normalisedJsonPath(jsonPath: readonly string[]): string {
  return jsonPath.join("/");
}

function definitionFromTechnical(row: TechnicalCityPage): CityPageDefinition | null {
  if (
    !usableText(row.city_key) ||
    !usableText(row.display_name) ||
    !usableText(row.category_label) ||
    !usableText(row.parent_page) ||
    !usableText(row.output_json) ||
    !usableText(row.route)
  ) {
    return null;
  }

  const active = row.lifecycle_state === "active";
  const launchMinimumJobs =
    typeof row.launch_minimum_live_jobs === "number"
      ? row.launch_minimum_live_jobs
      : typeof row.minimum_live_jobs === "number"
        ? row.minimum_live_jobs
        : 6;

  return {
    key: row.city_key,
    displayName: row.display_name,
    categoryLabel: row.category_label,
    route: row.route,
    listingLabel: `${row.display_name} ${row.category_label}`,
    jsonPath: row.output_json.split("/").filter(Boolean),
    parentRoute: parentRouteFromPage(row.parent_page),
    minimumJobs: active ? 0 : launchMinimumJobs,
    launchMinimumJobs,
    active,
  };
}

function loadCityPageDefinitions(): CityPageDefinition[] {
  const registerPath = path.join(
    process.cwd(),
    "pipeline",
    "city_pages",
    "city-page-register.json"
  );
  if (!fs.existsSync(registerPath)) return [];

  try {
    const parsed: unknown = JSON.parse(fs.readFileSync(registerPath, "utf8"));
    if (!Array.isArray(parsed)) return [];
    return parsed
      .filter((row): row is TechnicalCityPage => Boolean(row && typeof row === "object"))
      .map(definitionFromTechnical)
      .filter((row): row is CityPageDefinition => Boolean(row));
  } catch {
    return [];
  }
}

const legacyNewcastleFallback: CityPageDefinition = {
  key: "newcastle-service-administrator",
  displayName: "Newcastle",
  categoryLabel: "admin and customer-service jobs",
  route: "/newcastle/service-administrator-jobs",
  listingLabel: "Newcastle Admin & Customer Service jobs",
  jsonPath: ["app", "_city-pages", "newcastle", "service-administrator-jobs.json"],
  parentRoute: "/north-east/service-administrator-jobs",
  minimumJobs: 0,
  launchMinimumJobs: 6,
  active: true,
};

const loadedDefinitions = loadCityPageDefinitions();

export const cityPageDefinitions: readonly CityPageDefinition[] = loadedDefinitions.length
  ? loadedDefinitions
  : [legacyNewcastleFallback];

export const newcastleServiceAdministratorPage: CityPageDefinition =
  cityPageDefinitions.find((row) => row.key === "newcastle-service-administrator") ||
  legacyNewcastleFallback;

export function getCityPageDefinitionByRoute(route: string): CityPageDefinition | null {
  return cityPageDefinitions.find((definition) => definition.route === route) || null;
}

export function getCityPageDefinitionByJsonPath(
  jsonPath: readonly string[]
): CityPageDefinition | null {
  const target = normalisedJsonPath(jsonPath);
  return (
    cityPageDefinitions.find((definition) => normalisedJsonPath(definition.jsonPath) === target) ||
    null
  );
}

export function getActiveCityLinksForParentJsonPath(
  jsonPath: readonly string[]
): Array<{ href: string; label: string }> {
  const target = normalisedJsonPath(jsonPath);
  return cityPageDefinitions
    .filter((definition) => definition.active === true)
    .filter((definition) => {
      const registerParentPath = definition.parentRoute.startsWith("/job-search/")
        ? `app/_city-pages/configured-slices/${definition.parentRoute.slice("/job-search/".length)}.json`
        : `app${definition.parentRoute}.json`;
      return registerParentPath === target;
    })
    .map((definition) => ({ href: definition.route, label: definition.displayName }))
    .sort((left, right) => left.label.localeCompare(right.label, "en-GB"));
}

export function getCityPageBreadcrumb(jsonPath: readonly string[]): CityPageBreadcrumb | null {
  const definition = getCityPageDefinitionByJsonPath(jsonPath);
  if (!definition || definition.active !== true) return null;
  return {
    cityLabel: definition.displayName,
    cityRoute: definition.route,
    parentLabel: parentLabelFromRoute(definition.parentRoute),
    parentRoute: definition.parentRoute,
    ...roleBreadcrumb(definition.categoryLabel),
  };
}

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

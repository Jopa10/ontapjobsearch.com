import fs from "node:fs";
import path from "node:path";
import { cityPageDefinitions, getKnownRegionLabel } from "@/lib/city-page-data";
import { getLiveConfiguredSlices } from "@/lib/configured-job-slices";

const ROOT = process.cwd();
const ADMIN_ROUTE = "service-administrator-jobs";

export type AiTipsSource = {
  /** Validated query key used by /ai-tips?from=... */
  slug: string;
  /** Human-readable listing name without the word “jobs”. */
  label: string;
  href: string;
  regionSlug: string;
};
type SourceRecord = AiTipsSource & { jsonPath: string };

type Catalog = {
  categories?: Record<string, { route_slug?: string; display_label?: string }>;
  regions?: Record<string, { slug?: string }>;
};

function cleanJsonPath(parts: readonly string[]): string {
  return parts.join("/").replace(/\\/g, "/");
}

function sourceKey(regionSlug: string, categorySlug: string): string {
  return categorySlug === ADMIN_ROUTE ? regionSlug : `${regionSlug}--${categorySlug}`;
}

function displayName(region: string, category: string, categorySlug: string): string {
  const role = category.replace(/\s+jobs?$/i, "").trim();
  return categorySlug === ADMIN_ROUTE ? region : `${region} ${role}`;
}

let cachedRecords: SourceRecord[] | undefined;

function getSourceRecords(): SourceRecord[] {
  if (cachedRecords) return cachedRecords;
  const records = new Map<string, SourceRecord>();
  const add = (record: SourceRecord) => {
    if (record.slug && record.label && record.href && record.jsonPath) {
      records.set(record.jsonPath, record);
    }
  };

  // Dynamic listings are governed by the LIVE register. Their published page
  // route is the return destination, and the query key is built from known slugs.
  for (const item of getLiveConfiguredSlices()) {
    const staticRoute = `/${item.regionSlug}/${item.categorySlug}`;
    const hasStaticPage = fs.existsSync(
      path.join(ROOT, "app", item.regionSlug, item.categorySlug, "page.tsx")
    );
    const source: AiTipsSource = {
      slug: sourceKey(item.regionSlug, item.categorySlug),
      label: displayName(
        getKnownRegionLabel(item.regionSlug) ?? item.region,
        item.displayLabel,
        item.categorySlug
      ),
      href: hasStaticPage ? staticRoute : item.route,
      regionSlug: item.regionSlug,
    };
    add({ ...source, jsonPath: cleanJsonPath(path.relative(ROOT, item.dataFilePath).split(path.sep)) });
    // Static pages may use the same generated data at the traditional path.
    if (hasStaticPage) {
      const staticData = path.join(ROOT, "app", item.regionSlug, `${item.categorySlug}.json`);
      if (fs.existsSync(staticData)) add({ ...source, jsonPath: `app/${item.regionSlug}/${item.categorySlug}.json` });
    }
  }

  // Static regional routes are also valid sources, including regions/categories
  // that are not served through the dynamic configured-slice route.
  const catalogPath = path.join(ROOT, "pipeline", "config", "job_slice_catalog.json");
  try {
    const catalog = JSON.parse(fs.readFileSync(catalogPath, "utf8")) as Catalog;
    for (const [region, regionMeta] of Object.entries(catalog.regions ?? {})) {
      const regionSlug = regionMeta.slug;
      if (!regionSlug) continue;
      for (const category of Object.values(catalog.categories ?? {})) {
        const categorySlug = category.route_slug;
        if (!categorySlug) continue;
        const pagePath = path.join(ROOT, "app", regionSlug, categorySlug, "page.tsx");
        if (!fs.existsSync(pagePath)) continue;
        const dataCandidates = [
          `${categorySlug}.json`,
          `${categorySlug.replace(/-jobs$/, "")}.json`,
          `${categorySlug}-jobs.json`,
        ];
        const dataFile = dataCandidates
          .map((name) => path.join(ROOT, "app", regionSlug, name))
          .find((candidate) => fs.existsSync(candidate));
        if (!dataFile) continue;
        const categoryLabel = category.display_label ?? categorySlug;
        const source: AiTipsSource = {
          slug: sourceKey(regionSlug, categorySlug),
          label: displayName(
            getKnownRegionLabel(regionSlug) ?? region,
            categoryLabel,
            categorySlug
          ),
          href: `/${regionSlug}/${categorySlug}`,
          regionSlug,
        };
        add({ ...source, jsonPath: cleanJsonPath(path.relative(ROOT, dataFile).split(path.sep)) });
      }
    }
  } catch {
    // A missing catalogue disables fallback source discovery without affecting the page.
  }

  // City pages have explicitly activated routes and their own source data paths.
  for (const definition of cityPageDefinitions) {
    if (definition.active !== true) continue;
    const routeParts = definition.route.split("/").filter(Boolean);
    const regionSlug = routeParts[0];
    const categorySlug = routeParts[1];
    if (!regionSlug || !categorySlug) continue;
    const source: AiTipsSource = {
      slug: sourceKey(regionSlug, categorySlug),
      label: definition.displayName,
      href: definition.route,
      regionSlug,
    };
    add({ ...source, jsonPath: cleanJsonPath(definition.jsonPath) });
  }

  cachedRecords = [...records.values()];
  return cachedRecords;
}

export function getAiTipsSourceForJsonPath(jsonPath: readonly string[]): AiTipsSource | undefined {
  const target = cleanJsonPath(jsonPath);
  return getSourceRecords().find((source) => source.jsonPath === target);
}

export function getAiTipsSourceBySlug(slug: string): AiTipsSource | undefined {
  // Retain legacy ?from=<region-slug> for admin pages while requiring an exact
  // registry match for every source key.
  return getSourceRecords().find((source) => source.slug === slug);
}

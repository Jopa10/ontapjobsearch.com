import fs from "node:fs";
import path from "node:path";
import { cityPageDefinitions } from "@/lib/city-page-data";
import { getLiveConfiguredSlices } from "@/lib/configured-job-slices";

const ROOT = process.cwd();
const ADMIN_ROUTE = "service-administrator-jobs";

export type AiTipsSource = { slug: string; label: string; href: string };
type SourceRecord = AiTipsSource & { jsonPath: string };

function cleanJsonPath(parts: readonly string[]): string {
  return parts.join("/").replace(/\\/g, "/");
}

function categoryIsAdmin(label: string): boolean {
  return /admin|office|service administrator/i.test(label);
}

function sourceSlugFromRoute(route: string): string | undefined {
  const parts = route.split("/").filter(Boolean);
  if (parts.at(-1) !== ADMIN_ROUTE) return undefined;
  return parts[0] === "job-search" ? parts[1] : parts[0];
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

  for (const item of getLiveConfiguredSlices()) {
    if (item.categorySlug !== ADMIN_ROUTE) continue;
    const jsonPath = cleanJsonPath(path.relative(ROOT, item.dataFilePath).split(path.sep));
    const staticRoute = `/${item.regionSlug}/${ADMIN_ROUTE}`;
    const hasStaticPage = fs.existsSync(path.join(ROOT, "app", item.regionSlug, ADMIN_ROUTE, "page.tsx"));
    const source = {
      slug: item.regionSlug,
      label: item.region,
      href: hasStaticPage ? staticRoute : item.route,
    };
    add({ ...source, jsonPath });
    add({ ...source, jsonPath: `app/${item.regionSlug}/${ADMIN_ROUTE}.json` });
  }

  const catalogPath = path.join(ROOT, "pipeline", "config", "job_slice_catalog.json");
  try {
    const catalog = JSON.parse(fs.readFileSync(catalogPath, "utf8")) as {
      regions?: Record<string, { slug?: string }>;
    };
    for (const [label, item] of Object.entries(catalog.regions ?? {})) {
      const slug = item.slug;
      if (!slug) continue;
      const jsonPath = `app/${slug}/${ADMIN_ROUTE}.json`;
      const pagePath = path.join(ROOT, "app", slug, ADMIN_ROUTE, "page.tsx");
      if (!fs.existsSync(pagePath) || !fs.existsSync(path.join(ROOT, jsonPath))) continue;
      add({ slug, label, href: `/${slug}/${ADMIN_ROUTE}`, jsonPath });
    }
  } catch {
    // A missing catalog disables contextual links without blocking the page.
  }

  for (const definition of cityPageDefinitions) {
    if (definition.active !== true || !categoryIsAdmin(definition.categoryLabel)) continue;
    const slug = sourceSlugFromRoute(definition.route);
    if (!slug) continue;
    add({
      slug,
      label: definition.displayName,
      href: definition.route,
      jsonPath: cleanJsonPath(definition.jsonPath),
    });
  }

  cachedRecords = [...records.values()];
  return cachedRecords;
}

export function getAiTipsSourceForJsonPath(jsonPath: readonly string[]): AiTipsSource | undefined {
  const target = cleanJsonPath(jsonPath);
  return getSourceRecords().find((source) => source.jsonPath === target);
}

export function getAiTipsSourceBySlug(slug: string): AiTipsSource | undefined {
  return getSourceRecords().find((source) => source.slug === slug);
}

import fs from "node:fs";
import path from "node:path";

export type ConfiguredSlice = {
  region: string;
  category: string;
  regionSlug: string;
  categorySlug: string;
  anchorTown: string;
  displayLabel: string;
  title: string;
  route: string;
  dataFilePath: string;
};

type Catalog = {
  categories: Record<
    string,
    {
      route_slug: string;
      output_dir: string;
      file_suffix: string;
      display_label: string;
      category_label: string;
    }
  >;
  regions: Record<string, { slug: string; anchor_town: string }>;
};

const ROOT = process.cwd();
const CATALOG_PATH = path.join(ROOT, "pipeline", "config", "job_slice_catalog.json");
const REGISTER_PATH = path.join(
  ROOT,
  "pipeline",
  "registers",
  "region_category_slice_register.csv"
);

function readCatalog(): Catalog {
  return JSON.parse(fs.readFileSync(CATALOG_PATH, "utf8")) as Catalog;
}

function parseCsvLine(line: string): string[] {
  const cells: string[] = [];
  let current = "";
  let quoted = false;
  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    if (char === '"') {
      if (quoted && line[index + 1] === '"') {
        current += '"';
        index += 1;
      } else {
        quoted = !quoted;
      }
    } else if (char === "," && !quoted) {
      cells.push(current.trim());
      current = "";
    } else {
      current += char;
    }
  }
  cells.push(current.trim());
  return cells;
}

function livePairs(): Array<{ region: string; category: string }> {
  const lines = fs
    .readFileSync(REGISTER_PATH, "utf8")
    .replace(/^\uFEFF/, "")
    .split(/\r?\n/)
    .filter(Boolean);
  if (lines.shift() !== "region,category,status") {
    throw new Error("Invalid region/category slice register header");
  }
  return lines.flatMap((line) => {
    const [region, category, status] = parseCsvLine(line);
    return status === "LIVE" ? [{ region, category }] : [];
  });
}

function hasStaticPage(regionSlug: string, categorySlug: string): boolean {
  return fs.existsSync(path.join(ROOT, "app", regionSlug, categorySlug, "page.tsx"));
}

function dataFileHasJobs(filePath: string): boolean {
  if (!fs.existsSync(filePath)) return false;
  try {
    const parsed = JSON.parse(fs.readFileSync(filePath, "utf8"));
    return Array.isArray(parsed) && parsed.length > 0;
  } catch {
    return false;
  }
}

function buildSlice(region: string, category: string): ConfiguredSlice | undefined {
  const catalog = readCatalog();
  const regionMeta = catalog.regions[region];
  const categoryMeta = catalog.categories[category];
  if (!regionMeta || !categoryMeta) return undefined;
  const regionSlug = regionMeta.slug;
  const categorySlug = categoryMeta.route_slug;
  return {
    region,
    category,
    regionSlug,
    categorySlug,
    anchorTown: regionMeta.anchor_town,
    displayLabel: categoryMeta.display_label,
    title: `${region} ${categoryMeta.display_label} Jobs`,
    route: `/job-search/${regionSlug}/${categorySlug}`,
    dataFilePath: path.join(
      ROOT,
      "app",
      "_slice-data",
      regionSlug,
      `${categorySlug}.json`
    ),
  };
}

export function getLiveConfiguredSlices(): ConfiguredSlice[] {
  return livePairs()
    .map(({ region, category }) => buildSlice(region, category))
    .filter((slice): slice is ConfiguredSlice => Boolean(slice));
}

export function getPublishedDynamicSlices(): ConfiguredSlice[] {
  return getLiveConfiguredSlices()
    .filter((slice) => !hasStaticPage(slice.regionSlug, slice.categorySlug))
    .filter((slice) => dataFileHasJobs(slice.dataFilePath))
    .sort((left, right) => left.title.localeCompare(right.title, "en-GB"));
}

export function getPublishedDynamicSlice(
  regionSlug: string,
  categorySlug: string
): ConfiguredSlice | undefined {
  return getPublishedDynamicSlices().find(
    (slice) => slice.regionSlug === regionSlug && slice.categorySlug === categorySlug
  );
}

export function getConfiguredSliceBySlugs(
  regionSlug: string,
  categorySlug: string
): ConfiguredSlice | undefined {
  return getLiveConfiguredSlices().find(
    (slice) => slice.regionSlug === regionSlug && slice.categorySlug === categorySlug
  );
}

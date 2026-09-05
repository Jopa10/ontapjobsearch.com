import fs from "node:fs";
import path from "node:path";
import type { PublishedJob } from "@/lib/published-jobs";

type CsvRow = Record<string, string>;

type Place = {
  location: string;
  region: string;
  latitude: number;
  longitude: number;
};

type RoleRule = {
  sourceRole: string;
  targetRole: string;
  direction: string;
  sourceSectors: Set<string>;
  targetSector: string;
  priority: number;
};

type SectorRule = {
  id: string;
  field: string;
  type: string;
  value: string;
  sector: string;
  priority: number;
};

export type DiscoveryRecommendation = PublishedJob & {
  distance_miles: number;
};

const ROOT = process.cwd();
const REGISTER_DIRECTORY = path.join(ROOT, "pipeline", "registers");
const MAX_DISTANCE_MILES = 15;
const EARTH_RADIUS_MILES = 3958.7613;

const BROAD_OR_UNUSABLE_LOCATIONS = new Set([
  "bedfordshire", "berkshire", "buckinghamshire", "cambridgeshire", "cheshire",
  "city", "county durham", "derbyshire", "devon", "dorset", "essex",
  "gloucestershire", "hampshire", "hertfordshire", "kent", "lancashire",
  "leicestershire", "lincolnshire", "merseyside", "norfolk", "northamptonshire",
  "not specified", "nottinghamshire", "oxfordshire", "shropshire", "somerset",
  "staffordshire", "suffolk", "surrey", "sussex", "tyne and wear",
  "warwickshire", "wiltshire", "worcestershire", "yorkshire",
]);

function normalise(value: string | undefined): string {
  return (value ?? "")
    .toLocaleLowerCase("en-GB")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

function isApproved(row: CsvRow): boolean {
  return row.status === "APPROVED" && row.active.toUpperCase() === "TRUE" && row.approval_status === "APPROVED";
}

function parseCsv(input: string): CsvRow[] {
  const records: string[][] = [];
  let row: string[] = [];
  let value = "";
  let quoted = false;

  for (let index = 0; index < input.length; index += 1) {
    const char = input[index];
    if (quoted) {
      if (char === '"' && input[index + 1] === '"') {
        value += '"';
        index += 1;
      } else if (char === '"') {
        quoted = false;
      } else {
        value += char;
      }
      continue;
    }
    if (char === '"') {
      quoted = true;
    } else if (char === ",") {
      row.push(value);
      value = "";
    } else if (char === "\n") {
      row.push(value.replace(/\r$/, ""));
      records.push(row);
      row = [];
      value = "";
    } else {
      value += char;
    }
  }
  if (value || row.length) {
    row.push(value.replace(/\r$/, ""));
    records.push(row);
  }

  const [header, ...data] = records;
  if (!header) return [];
  return data
    .filter((record) => record.some(Boolean))
    .map((record) => Object.fromEntries(header.map((column, index) => [column, record[index] ?? ""])));
}

function readRegister(name: string): CsvRow[] {
  return parseCsv(fs.readFileSync(path.join(REGISTER_DIRECTORY, name), "utf8"));
}

function employerIdentity(job: PublishedJob): string {
  return (job.advertiser_name || job.company)
    .replace(/\s+-\s+(?:Agency|Company)\s+-\s+.*$/i, "")
    .trim();
}

function matchSectorRule(rule: SectorRule, job: PublishedJob): boolean {
  if (rule.type === "fallback") return true;
  const identity = employerIdentity(job);
  const value = rule.field === "source"
    ? job.source
    : rule.field === "advertiser_type"
      ? job.advertiser_type
      : rule.field === "employer_identity"
        ? identity
        : rule.field === "combined_text"
          ? [job.company, job.advertiser_name, job.description, job.full_description].join(" ")
          : "";
  if (!value) return false;
  if (rule.type === "exact") return normalise(value) === normalise(rule.value);
  if (rule.type === "regex") {
    try {
      return new RegExp(rule.value, "i").test(value);
    } catch {
      return false;
    }
  }
  return false;
}

function haversineMiles(left: Place, right: Place): number {
  const radians = (value: number) => (value * Math.PI) / 180;
  const dLatitude = radians(right.latitude - left.latitude);
  const dLongitude = radians(right.longitude - left.longitude);
  const a = Math.sin(dLatitude / 2) ** 2
    + Math.cos(radians(left.latitude)) * Math.cos(radians(right.latitude)) * Math.sin(dLongitude / 2) ** 2;
  return EARTH_RADIUS_MILES * 2 * Math.asin(Math.sqrt(a));
}

function placeKey(place: Place): string {
  return `${normalise(place.location)}|${normalise(place.region)}`;
}

function resolvePlace(rawLocation: string, region: string, placesByName: Map<string, Place[]>): Place | undefined {
  const key = normalise(rawLocation);
  if (!key || BROAD_OR_UNUSABLE_LOCATIONS.has(key) || key.endsWith(" council")) return undefined;
  const choose = (candidates: Place[] | undefined): Place | undefined => {
    if (!candidates?.length) return undefined;
    const sameRegion = candidates.filter((candidate) => normalise(candidate.region) === normalise(region));
    if (sameRegion.length === 1) return sameRegion[0];
    if (normalise(region) === "north east") {
      const northEast = candidates.filter((candidate) => normalise(candidate.region).startsWith("north east"));
      if (northEast.length === 1) return northEast[0];
    }
    if (candidates.length === 1) return candidates[0];
    const coordinateCount = new Set(candidates.map((candidate) => `${candidate.latitude},${candidate.longitude}`)).size;
    return coordinateCount === 1 ? candidates[0] : undefined;
  };

  const direct = choose(placesByName.get(key));
  if (direct) return direct;
  for (const segment of rawLocation.split(",").map((value) => value.trim())) {
    const match = choose(placesByName.get(normalise(segment)));
    if (match) return match;
  }
  if (!rawLocation.includes(",") && !/\b[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}\b/i.test(rawLocation)) return undefined;

  const contained = [...placesByName.entries()]
    .filter(([name]) => name.length >= 5 && new RegExp(`(^| )${name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}( |$)`).test(key))
    .flatMap(([, candidates]) => candidates);
  if (!contained.length) return undefined;
  const longest = Math.max(...contained.map((candidate) => normalise(candidate.location).length));
  return choose(contained.filter((candidate) => normalise(candidate.location).length === longest));
}

function newestFirst(left: PublishedJob, right: PublishedJob): number {
  const leftTime = Date.parse(left.posted_date);
  const rightTime = Date.parse(right.posted_date);
  if (Number.isFinite(leftTime) && Number.isFinite(rightTime) && leftTime !== rightTime) return rightTime - leftTime;
  if (Number.isFinite(leftTime) !== Number.isFinite(rightTime)) return Number.isFinite(rightTime) ? 1 : -1;
  return left.job_id.localeCompare(right.job_id);
}

let cachedRules:
  | {
    roleRules: RoleRule[];
    sectorRules: SectorRule[];
    placesByName: Map<string, Place[]>;
    excludedPairs: Set<string>;
  }
  | undefined;

function loadRules() {
  if (cachedRules) return cachedRules;
  const roleRules = readRegister("role_relationships.csv")
    .filter(isApproved)
    .map((row): RoleRule => ({
      sourceRole: normalise(row.source_role),
      targetRole: normalise(row.target_role),
      direction: row.direction,
      sourceSectors: new Set(row.source_sector_scope.split("|").map(normalise)),
      targetSector: normalise(row.target_sector_scope),
      priority: Number(row.priority),
    }));
  const sectorRules = readRegister("employer_sector_rules.csv")
    .filter(isApproved)
    .map((row): SectorRule => ({
      id: row.rule_id,
      field: row.match_field,
      type: row.match_type,
      value: row.match_value,
      sector: normalise(row.sector),
      priority: Number(row.priority),
    }))
    .sort((left, right) => left.priority - right.priority || left.id.localeCompare(right.id));
  const placesByName = new Map<string, Place[]>();
  for (const row of readRegister("canonical_location_coordinates.csv").filter(isApproved)) {
    const latitude = Number(row.latitude);
    const longitude = Number(row.longitude);
    if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) continue;
    const place: Place = { location: row.canonical_location, region: row.canonical_region, latitude, longitude };
    const key = normalise(place.location);
    placesByName.set(key, [...(placesByName.get(key) ?? []), place]);
  }
  const excludedPairs = new Set(
    readRegister("city_nearby_rules.csv")
      .filter((row) => isApproved(row) && row.action === "EXCLUDE")
      .map((row) => `${normalise(row.anchor_location)}|${normalise(row.anchor_region)}>${normalise(row.nearby_location)}|${normalise(row.nearby_region)}`),
  );
  cachedRules = { roleRules, sectorRules, placesByName, excludedPairs };
  return cachedRules;
}

export function classifyDiscoverySector(job: PublishedJob): string {
  const { sectorRules } = loadRules();
  return sectorRules.find((rule) => matchSectorRule(rule, job))?.sector ?? "unknown";
}

/**
 * Returns only evidenced private-sector targets. The landing job's published
 * family can safely drive same-family discovery even when its employer sector
 * is unknown, because no recommendation target can be public or unknown.
 */
export function getDiscoveryRecommendations(
  current: PublishedJob,
  jobs: PublishedJob[],
  limit = 6,
): DiscoveryRecommendation[] {
  const { roleRules, placesByName, excludedPairs } = loadRules();
  const sourceSector = classifyDiscoverySector(current);
  const sourceRole = normalise(current.title);
  const sourceFamily = normalise(current.category);
  const sourcePlace = resolvePlace(current.location, current.region, placesByName);
  if (!sourcePlace) return [];

  const applicableRules = roleRules.filter((rule) =>
    rule.direction === "ONE_WAY_PUBLIC_TO_PRIVATE"
      && rule.sourceRole === sourceRole
      && (sourceSector === "unknown" || rule.sourceSectors.has(sourceSector))
      && rule.targetSector === "private sector"
  );
  const targetPriorities = new Map<string, number>();
  for (const rule of applicableRules) {
    const existing = targetPriorities.get(rule.targetRole);
    if (existing === undefined || rule.priority < existing) targetPriorities.set(rule.targetRole, rule.priority);
  }

  return jobs
    .filter((candidate) => candidate.job_id !== current.job_id)
    .map((candidate) => {
      const candidateRole = normalise(candidate.title);
      const sameFamily = Boolean(sourceFamily) && normalise(candidate.category) === sourceFamily;
      const explicitPriority = targetPriorities.get(candidateRole);
      const priority = sameFamily && candidateRole === sourceRole
        ? 0
        : explicitPriority ?? (sameFamily ? 10 : undefined);
      const targetPlace = resolvePlace(candidate.location, candidate.region, placesByName);
      if (priority === undefined || !targetPlace || classifyDiscoverySector(candidate) !== "private sector") return undefined;
      if (excludedPairs.has(`${placeKey(sourcePlace)}>${placeKey(targetPlace)}`)) return undefined;
      const distance = haversineMiles(sourcePlace, targetPlace);
      if (distance > MAX_DISTANCE_MILES) return undefined;
      return { ...candidate, distance_miles: distance, priority };
    })
    .filter((candidate): candidate is DiscoveryRecommendation & { priority: number } => Boolean(candidate))
    .sort((left, right) => left.priority - right.priority
      || left.distance_miles - right.distance_miles
      || newestFirst(left, right))
    .slice(0, Math.max(0, limit))
    .map(({ priority: _priority, ...candidate }) => candidate);
}

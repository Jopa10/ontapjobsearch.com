import fs from 'node:fs';
import path from 'node:path';
import register from '@/pipeline/city_pages/broad-city-page-register.json';
import { getPublishedJobs, type PublishedJob } from '@/lib/published-jobs';
import { getPublishedDynamicSlices } from '@/lib/configured-job-slices';

export type BroadCityDefinition = {
  display_name: string;
  slug: string;
  region: string;
  route: string;
  lifecycle_state: 'active';
};

export const broadCityDefinitions = register as BroadCityDefinition[];

function normalisePlace(value: string): string {
  return value.replace(/\s+/g, ' ').trim().toLocaleLowerCase('en-GB');
}

export function locationCandidates(value: string): string[] {
  const clean = value
    .replace(/\s*\((?:[^)]*\b(?:hybrid|remote|home[- ]based|working)\b[^)]*)\)\s*$/i, '')
    .trim();
  return [...new Set([clean, clean.includes(',') ? clean.split(',', 1)[0].trim() : ''].filter(Boolean))];
}

export function isExactCityJob(job: Pick<PublishedJob, 'location'>, city: BroadCityDefinition): boolean {
  const cityKey = normalisePlace(city.display_name);
  return locationCandidates(job.location).some((candidate) => normalisePlace(candidate) === cityKey);
}

type NearbyRule = {
  anchor: string;
  region: string;
  nearby: string;
  active: boolean;
  approved: boolean;
  include: boolean;
};

type Coordinates = { latitude: number; longitude: number };

function parseCsvLine(line: string): string[] {
  const values: string[] = [];
  let value = '';
  let quoted = false;
  for (let index = 0; index < line.length; index += 1) {
    const character = line[index];
    if (character === '"' && quoted && line[index + 1] === '"') {
      value += '"';
      index += 1;
    } else if (character === '"') {
      quoted = !quoted;
    } else if (character === ',' && !quoted) {
      values.push(value);
      value = '';
    } else {
      value += character;
    }
  }
  values.push(value);
  return values;
}

function approvedNearbyRules(): NearbyRule[] {
  const filePath = path.join(process.cwd(), 'pipeline', 'registers', 'city_nearby_rules.csv');
  if (!fs.existsSync(filePath)) return [];
  const [headerLine, ...lines] = fs.readFileSync(filePath, 'utf8').split(/\r?\n/).filter(Boolean);
  if (!headerLine) return [];
  const headers = parseCsvLine(headerLine);
  return lines.map((line) => {
    const row = Object.fromEntries(headers.map((header, index) => [header, parseCsvLine(line)[index] ?? '']));
    return {
      anchor: row.anchor_location,
      region: row.anchor_region,
      nearby: row.nearby_location,
      active: row.active.toUpperCase() === 'TRUE',
      approved: row.status.toUpperCase() === 'APPROVED' && row.approval_status.toUpperCase() === 'APPROVED',
      include: row.action.toLowerCase() === 'include',
    };
  });
}

function approvedCoordinates(): Map<string, Coordinates> {
  const filePath = path.join(process.cwd(), 'pipeline', 'registers', 'canonical_location_coordinates.csv');
  if (!fs.existsSync(filePath)) return new Map();
  const [headerLine, ...lines] = fs.readFileSync(filePath, 'utf8').split(/\r?\n/).filter(Boolean);
  if (!headerLine) return new Map();
  const headers = parseCsvLine(headerLine);
  return new Map(lines.flatMap((line): Array<[string, Coordinates]> => {
    const values = parseCsvLine(line);
    const row = Object.fromEntries(headers.map((header, index) => [header, values[index] ?? '']));
    const latitude = Number(row.latitude);
    const longitude = Number(row.longitude);
    if (row.active.toUpperCase() !== 'TRUE' || row.status.toUpperCase() !== 'APPROVED' || row.approval_status.toUpperCase() !== 'APPROVED') return [];
    if (!row.canonical_location || !Number.isFinite(latitude) || !Number.isFinite(longitude)) return [];
    return [[normalisePlace(row.canonical_location), { latitude, longitude }]];
  }));
}

export function distanceMiles(from: Coordinates, to: Coordinates): number {
  const radians = (degrees: number) => degrees * Math.PI / 180;
  const latitudeDelta = radians(to.latitude - from.latitude);
  const longitudeDelta = radians(to.longitude - from.longitude);
  const a = Math.sin(latitudeDelta / 2) ** 2
    + Math.cos(radians(from.latitude)) * Math.cos(radians(to.latitude)) * Math.sin(longitudeDelta / 2) ** 2;
  return 3958.8 * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

export function getBroadCityJobs(city: BroadCityDefinition): { exact: PublishedJob[]; nearby: PublishedJob[] } {
  const jobs = getPublishedJobs();
  const exactLocationById = new Map(
    jobs.filter((job) => isExactCityJob(job, city)).map((job) => [job.job_id, job.location])
  );
  for (const slice of getPublishedDynamicSlices()) {
    let rows: unknown;
    try {
      rows = JSON.parse(fs.readFileSync(slice.dataFilePath, 'utf8'));
    } catch {
      continue;
    }
    if (!Array.isArray(rows)) continue;
    for (const row of rows) {
      if (!row || typeof row !== 'object') continue;
      const candidate = row as Record<string, unknown>;
      const jobId = typeof candidate.job_id === 'string' ? candidate.job_id.trim() : '';
      const location = typeof candidate.location === 'string' ? candidate.location.trim() : '';
      if (jobId && isExactCityJob({ location }, city)) exactLocationById.set(jobId, location);
    }
  }
  const exact = jobs
    .filter((job) => exactLocationById.has(job.job_id))
    .map((job) => ({ ...job, location: exactLocationById.get(job.job_id) ?? job.location }));
  const exactIds = new Set(exact.map((job) => job.job_id));
  const coordinates = approvedCoordinates();
  const anchorCoordinates = coordinates.get(normalisePlace(city.display_name));
  const nearbyPlaces = new Set(
    approvedNearbyRules()
      .filter((rule) => rule.active && rule.approved && rule.include)
      .filter((rule) => normalisePlace(rule.anchor) === normalisePlace(city.display_name))
      .filter((rule) => normalisePlace(rule.region) === normalisePlace(city.region))
      .filter((rule) => {
        const nearbyCoordinates = coordinates.get(normalisePlace(rule.nearby));
        return Boolean(anchorCoordinates && nearbyCoordinates && distanceMiles(anchorCoordinates, nearbyCoordinates) <= 15);
      })
      .map((rule) => normalisePlace(rule.nearby))
  );
  const nearby = jobs
    .filter((job) => !exactIds.has(job.job_id))
    .filter((job) => locationCandidates(job.location).some((candidate) => nearbyPlaces.has(normalisePlace(candidate))))
    .slice(0, 6);
  return { exact, nearby };
}

export function getBroadCityDefinition(slug: string): BroadCityDefinition | undefined {
  return broadCityDefinitions.find((city) => city.slug === slug && city.lifecycle_state === 'active');
}

export function getRegionSearchPath(region: string): string {
  return `/jobs/search?location=${encodeURIComponent(region)}`;
}

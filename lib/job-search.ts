import type { PublishedJob } from "./published-jobs";

type MatchKind = "title" | "location" | "region" | "category" | "company" | "description" | "combined";

type FieldMatch = {
  score: number;
  kind: MatchKind;
};

type SearchFieldData = {
  text: string;
  tokens: string[];
};

type GeoSearchFieldData = SearchFieldData & {
  geoTokens: string[];
};

export type PublishedJobSearchData = {
  title: SearchFieldData;
  location: GeoSearchFieldData;
  region: GeoSearchFieldData;
  category: SearchFieldData;
  company: SearchFieldData;
  description: SearchFieldData;
  combined: SearchFieldData;
  sliceLabel: SearchFieldData;
};

export type SearchablePublishedJob = PublishedJob & {
  _search?: PublishedJobSearchData;
};

export type SearchInputEvidence = {
  roleMatches: number;
  geoMatches: number;
};

const TOKEN_ALIASES: Record<string, string> = {
  administrators: "admin",
  administrator: "admin",
  administrative: "admin",
  admins: "admin",
  admn: "admin",
  cust: "customer",
  srv: "service",
  supp: "support",
  wrkr: "worker",
  services: "service",
  accounts: "account",
  accounting: "account",
  financial: "finance",
  finances: "finance",
  recruitment: "recruit",
  recruiter: "recruit",
  recruiters: "recruit",
  recruiting: "recruit",
  resources: "resource",
  coordinators: "coordinator",
  advisers: "advisor",
  adviser: "advisor",
  advisors: "advisor",
  assistants: "assistant",
  temporary: "temp",
  warehousing: "warehouse",
};

const LOCATION_TOKEN_ALIASES: Record<string, string> = {
  ncl: "newcastle",
};

// These concepts need a strong role anchor rather than matching incidental
// wording in a description. Admin may also be supported by Ontap's curated
// admin/service category, so searches such as "Newcastle admin" can surface
// the wider curated office/admin family while literal admin titles still rank
// highest. Customer-service and reception searches remain title-anchored.
const TITLE_REQUIRED_ROLE_TOKENS = new Set(["admin", "customerservice", "reception"]);

const jobSearchDataCache = new WeakMap<object, PublishedJobSearchData>();
const corpusCache = new WeakMap<object, { geoVocabulary: string[] }>();

function normalise(value: string): string {
  return value
    .normalize("NFKD")
    .replace(/\p{Diacritic}/gu, "")
    .toLowerCase()
    .replace(/\bco[-\s]?ordinator\b/g, "coordinator")
    .replace(/&/g, " and ")
    .replace(/[\/_-]+/g, " ")
    .replace(/[^a-z0-9+£.\s]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function simpleWords(value: string): string[] {
  return value
    .normalize("NFKD")
    .replace(/\p{Diacritic}/gu, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim()
    .split(/\s+/)
    .filter(Boolean);
}

function cleanToken(token: string): string {
  return token.replace(/^\.+|\.+$/g, "");
}

function canonicalToken(token: string): string {
  const clean = cleanToken(token);
  return TOKEN_ALIASES[clean] || clean;
}

function damerauLevenshtein(a: string, b: string): number {
  if (a === b) return 0;
  if (!a.length) return b.length;
  if (!b.length) return a.length;

  const matrix = Array.from({ length: a.length + 1 }, () => new Array<number>(b.length + 1).fill(0));
  for (let i = 0; i <= a.length; i += 1) matrix[i][0] = i;
  for (let j = 0; j <= b.length; j += 1) matrix[0][j] = j;

  for (let i = 1; i <= a.length; i += 1) {
    for (let j = 1; j <= b.length; j += 1) {
      const substitution = a[i - 1] === b[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,
        matrix[i][j - 1] + 1,
        matrix[i - 1][j - 1] + substitution
      );

      if (
        i > 1 &&
        j > 1 &&
        a[i - 1] === b[j - 2] &&
        a[i - 2] === b[j - 1]
      ) {
        matrix[i][j] = Math.min(matrix[i][j], matrix[i - 2][j - 2] + 1);
      }
    }
  }

  return matrix[a.length][b.length];
}

const KNOWN_ROLE_TOKENS = [...new Set([...Object.keys(TOKEN_ALIASES), ...Object.values(TOKEN_ALIASES)])];

function canonicalQueryToken(token: string): string {
  const clean = cleanToken(token);
  const exact = TOKEN_ALIASES[clean];
  if (exact) return exact;
  const locationAlias = LOCATION_TOKEN_ALIASES[clean];
  if (locationAlias) return locationAlias;
  if (clean.length < 4) return clean;

  let bestToken = clean;
  let bestDistance = Number.POSITIVE_INFINITY;

  for (const known of KNOWN_ROLE_TOKENS) {
    const distance = damerauLevenshtein(clean, known);
    const maxLength = Math.max(clean.length, known.length);
    let allowedDistance = maxLength >= 10 ? 3 : maxLength >= 7 ? 2 : 1;

    if (maxLength >= 10 && clean.slice(0, 4) === known.slice(0, 4)) {
      allowedDistance = 4;
    }

    if (distance <= allowedDistance && distance < bestDistance) {
      bestDistance = distance;
      bestToken = TOKEN_ALIASES[known] || known;
    }
  }

  return bestToken;
}

function applyPhraseAliases(text: string): string {
  return text
    .replace(/\bcustomer services?\b/g, " customerservice ")
    .replace(/\bcustomer support\b/g, " customerservice ")
    .replace(/\bhuman resources?\b/g, " hr ")
    .replace(/\bpersonal assistant\b/g, " pa ")
    .replace(/\bexecutive assistant\b/g, " ea ")
    .replace(/\bcontact cent(?:re|er)\b/g, " contactcentre ")
    .replace(/\bfront of house\b/g, " reception ")
    .replace(/\bsupport worker\b/g, " supportworker ")
    .replace(/\s+/g, " ")
    .trim();
}

function queryTokensFromNormalised(text: string): string[] {
  const canonicalText = text
    .split(/\s+/)
    .filter(Boolean)
    .map(canonicalQueryToken)
    .join(" ");

  return applyPhraseAliases(canonicalText).split(/\s+/).filter(Boolean);
}

function candidateTokensFromNormalised(text: string): string[] {
  const tokens = text.split(/\s+/).filter(Boolean).map(canonicalToken);
  const aliases: string[] = [];

  if (/\bcustomer services?\b/.test(text) || /\bcustomer support\b/.test(text)) aliases.push("customerservice");
  if (/\bhuman resources?\b/.test(text)) aliases.push("hr");
  if (/\bpersonal assistant\b/.test(text)) aliases.push("pa");
  if (/\bexecutive assistant\b/.test(text)) aliases.push("ea");
  if (/\bcontact cent(?:re|er)\b/.test(text)) aliases.push("contactcentre");
  if (/\bfront of house\b/.test(text)) aliases.push("reception");
  if (/\bsupport worker\b/.test(text)) aliases.push("supportworker");

  return [...tokens, ...aliases];
}

function buildField(value: string): SearchFieldData {
  const text = normalise(value);
  return { text, tokens: candidateTokensFromNormalised(text) };
}

function buildGeoField(value: string): GeoSearchFieldData {
  const text = normalise(value);
  return {
    text,
    tokens: candidateTokensFromNormalised(text),
    geoTokens: text.split(/\s+/).filter(Boolean),
  };
}

export function buildPublishedJobSearchData(job: PublishedJob): PublishedJobSearchData {
  const company = `${job.company} ${job.advertiser_name}`;
  const description = job.description.slice(0, 2200);
  const combined = `${job.title} ${job.company} ${job.advertiser_name} ${job.location} ${job.region} ${job.category}`;

  return {
    title: buildField(job.title),
    location: buildGeoField(job.location),
    region: buildGeoField(job.region),
    category: buildField(job.category),
    company: buildField(company),
    description: buildField(description),
    combined: buildField(combined),
    sliceLabel: buildField(job.slice_label),
  };
}

function searchData(job: SearchablePublishedJob): PublishedJobSearchData {
  if (job._search) return job._search;

  const cached = jobSearchDataCache.get(job);
  if (cached) return cached;

  const built = buildPublishedJobSearchData(job);
  jobSearchDataCache.set(job, built);
  return built;
}

type PreparedQuery = {
  raw: string;
  text: string;
  tokens: string[];
  geoTokens: string[];
  requiredRoleTokens: string[];
};

function prepareQuery(value: string): PreparedQuery {
  const raw = value.trim();
  const text = normalise(raw);
  const tokens = queryTokensFromNormalised(text);
  return {
    raw,
    text,
    tokens,
    geoTokens: text.split(/\s+/).filter(Boolean),
    requiredRoleTokens: tokens.filter((token) => TITLE_REQUIRED_ROLE_TOKENS.has(token)),
  };
}

function levenshtein(a: string, b: string): number {
  if (a === b) return 0;
  if (!a.length) return b.length;
  if (!b.length) return a.length;

  const previous = Array.from({ length: b.length + 1 }, (_, index) => index);
  const current = new Array<number>(b.length + 1);

  for (let i = 1; i <= a.length; i += 1) {
    current[0] = i;
    for (let j = 1; j <= b.length; j += 1) {
      const substitution = a[i - 1] === b[j - 1] ? 0 : 1;
      current[j] = Math.min(
        previous[j] + 1,
        current[j - 1] + 1,
        previous[j - 1] + substitution
      );
    }
    for (let j = 0; j <= b.length; j += 1) previous[j] = current[j];
  }

  return previous[b.length];
}

function tokenMatches(query: string, candidate: string): boolean {
  if (!query || !candidate) return false;
  if (query === candidate) return true;

  if (query.length >= 4 && candidate.startsWith(query)) return true;
  if (candidate.length >= 4 && query.startsWith(candidate) && candidate.length >= query.length - 2) return true;

  if (query.length < 4 || candidate.length < 4) return false;
  const maxDistance = Math.max(query.length, candidate.length) >= 8 ? 2 : 1;
  if (Math.abs(query.length - candidate.length) > maxDistance) return false;
  return levenshtein(query, candidate) <= maxDistance;
}

function isOrderedSubsequence(query: string, candidate: string): boolean {
  let queryIndex = 0;
  for (const char of candidate) {
    if (char === query[queryIndex]) queryIndex += 1;
    if (queryIndex === query.length) return true;
  }
  return false;
}

function commonPrefixLength(a: string, b: string): number {
  let index = 0;
  while (index < a.length && index < b.length && a[index] === b[index]) index += 1;
  return index;
}

function geoTokenMatchQuality(query: string, candidate: string): number {
  const cleanQuery = LOCATION_TOKEN_ALIASES[query] || query;
  if (!cleanQuery || !candidate) return 0;
  if (cleanQuery === candidate) return 1000;

  const prefix = commonPrefixLength(cleanQuery, candidate);

  if (cleanQuery.length >= 3 && candidate.startsWith(cleanQuery)) {
    return 900 + Math.min(cleanQuery.length, 20);
  }

  if (
    candidate.length >= 4 &&
    cleanQuery.startsWith(candidate) &&
    candidate.length >= cleanQuery.length - 2
  ) {
    return 875 + Math.min(candidate.length, 20);
  }

  if (
    cleanQuery.length >= 5 &&
    candidate.length > cleanQuery.length &&
    prefix >= 2 &&
    isOrderedSubsequence(cleanQuery, candidate)
  ) {
    return 800 + Math.min(prefix, 20);
  }

  if (cleanQuery.length >= 4 && candidate.length >= 4 && prefix >= 2) {
    const maxDistance = Math.max(cleanQuery.length, candidate.length) >= 8 ? 2 : 1;
    const distance = damerauLevenshtein(cleanQuery, candidate);
    if (Math.abs(cleanQuery.length - candidate.length) <= maxDistance && distance <= maxDistance) {
      return 700 - distance * 20 + Math.min(prefix * 5, 50);
    }
  }

  return 0;
}

function allTokensMatch(wanted: string[], available: string[]): boolean {
  if (!wanted.length) return false;
  return wanted.every((token) => available.some((candidateToken) => tokenMatches(token, candidateToken)));
}

function allGeoTokensMatch(wanted: string[], available: string[]): boolean {
  if (!wanted.length) return false;
  return wanted.every((token) => available.some((candidateToken) => geoTokenMatchQuality(token, candidateToken) > 0));
}

function scoreField(query: PreparedQuery, field: SearchFieldData, scores: [number, number, number, number]): number {
  if (!query.raw || !field.text) return 0;
  const [exact, starts, contains, token] = scores;

  if (field.text === query.text) return exact;
  if (field.text.startsWith(`${query.text} `) || query.text.startsWith(`${field.text} `)) return starts;
  if (field.text.includes(query.text)) return contains;
  if (allTokensMatch(query.tokens, field.tokens)) return token;
  return 0;
}

function scoreGeoField(query: PreparedQuery, field: GeoSearchFieldData, scores: [number, number, number, number]): number {
  if (!query.raw || !field.text) return 0;
  const [exact, starts, contains, token] = scores;

  if (field.text === query.text) return exact;
  if (field.text.startsWith(`${query.text} `) || query.text.startsWith(`${field.text} `)) return starts;
  if (field.text.includes(query.text) && query.text.length >= 4) return contains;
  if (allGeoTokensMatch(query.geoTokens, field.geoTokens)) return token;
  return 0;
}

function bestGeoMatch(job: SearchablePublishedJob, query: PreparedQuery): FieldMatch {
  const data = searchData(job);
  const fields: Array<[MatchKind, GeoSearchFieldData, [number, number, number, number]]> = [
    ["location", data.location, [230, 205, 180, 160]],
    ["region", data.region, [225, 200, 175, 155]],
  ];

  let best: FieldMatch = { score: 0, kind: "location" };
  for (const [kind, field, scores] of fields) {
    const score = scoreGeoField(query, field, scores);
    if (score > best.score) best = { score, kind };
  }
  return best;
}

function bestMatch(job: SearchablePublishedJob, query: PreparedQuery): FieldMatch {
  const data = searchData(job);
  const fields: Array<[MatchKind, SearchFieldData, [number, number, number, number]]> = [
    ["title", data.title, [240, 215, 190, 165]],
    ["location", data.location, [230, 205, 180, 160]],
    ["region", data.region, [225, 200, 175, 155]],
    ["category", data.category, [145, 130, 120, 110]],
    ["company", data.company, [105, 95, 85, 75]],
    ["description", data.description, [50, 45, 38, 32]],
  ];

  let best: FieldMatch = { score: 0, kind: "description" };
  for (const [kind, field, scores] of fields) {
    const score = scoreField(query, field, scores);
    if (score > best.score) best = { score, kind };

    // No later field can beat an exact title match.
    if (best.score === 240) break;
  }

  if (allTokensMatch(query.tokens, data.combined.tokens) && best.score < 150) {
    best = { score: 150, kind: "combined" };
  }

  return best;
}

function preferredBonus(kind: MatchKind, preferred: "role" | "location"): number {
  if (preferred === "role" && (kind === "title" || kind === "category")) return 12;
  if (preferred === "location" && (kind === "location" || kind === "region")) return 12;
  return 0;
}

function titleSupportsRequiredRoleTokens(query: PreparedQuery, job: SearchablePublishedJob): boolean {
  if (!query.requiredRoleTokens.length) return true;

  const data = searchData(job);
  return query.requiredRoleTokens.every((token) => {
    if (data.title.tokens.some((candidateToken) => tokenMatches(token, candidateToken))) return true;
    if (token !== "admin") return false;
    return data.category.tokens.some((candidateToken) => tokenMatches(token, candidateToken));
  });
}

function hasRoleAnchor(jobs: SearchablePublishedJob[], query: PreparedQuery): boolean {
  return jobs.some((job) => {
    const data = searchData(job);
    const titleScore = scoreField(query, data.title, [240, 215, 190, 165]);
    const categoryScore = scoreField(query, data.category, [145, 130, 120, 110]);
    return Math.max(titleScore, categoryScore) >= 30;
  });
}

function getGeoVocabulary(jobs: SearchablePublishedJob[]): string[] {
  const cached = corpusCache.get(jobs);
  if (cached) return cached.geoVocabulary;

  const available = new Set<string>();
  for (const job of jobs) {
    const data = searchData(job);
    data.location.geoTokens.forEach((token) => available.add(token));
    data.region.geoTokens.forEach((token) => available.add(token));
  }

  const geoVocabulary = [...available];
  corpusCache.set(jobs, { geoVocabulary });
  return geoVocabulary;
}

function resolveGeoQuery(jobs: SearchablePublishedJob[], input: string): string {
  const wanted = normalise(input).split(/\s+/).filter(Boolean);
  if (!wanted.length) return input;

  const available = getGeoVocabulary(jobs);
  const resolved = wanted.map((queryToken) => {
    const alias = LOCATION_TOKEN_ALIASES[queryToken];
    if (alias) return alias;

    let bestToken = queryToken;
    let bestQuality = 0;

    for (const candidate of available) {
      const quality = geoTokenMatchQuality(queryToken, candidate);
      if (quality > bestQuality) {
        bestQuality = quality;
        bestToken = candidate;
      }
    }

    return bestQuality >= 650 ? bestToken : queryToken;
  });

  return resolved.join(" ");
}

export function searchInputEvidence(jobs: SearchablePublishedJob[], value: string): SearchInputEvidence {
  const wanted = simpleWords(value);
  if (!wanted.length) return { roleMatches: 0, geoMatches: 0 };

  let roleMatches = 0;
  let geoMatches = 0;

  for (const job of jobs) {
    const data = searchData(job);
    const roleFields = [data.title.text, data.category.text, data.sliceLabel.text];
    const geoFields = [data.location.text, data.region.text];

    if (roleFields.some((field) => {
      const available = new Set(simpleWords(field));
      return wanted.every((token) => available.has(token));
    })) {
      roleMatches += 1;
    }

    if (geoFields.some((field) => {
      const available = new Set(simpleWords(field));
      return wanted.every((token) => available.has(token));
    })) {
      geoMatches += 1;
    }
  }

  return { roleMatches, geoMatches };
}

export function searchJobs(
  jobs: SearchablePublishedJob[],
  query: string,
  location: string
): SearchablePublishedJob[] {
  let roleQuery = query.trim();
  let effectiveLocation = location.trim();

  if (roleQuery && !effectiveLocation) {
    const rawTokens = normalise(roleQuery).split(/\s+/).filter(Boolean);
    const geoTokenIndexes = new Set<number>();

    rawTokens.forEach((token, index) => {
      const preparedToken = prepareQuery(token);
      if (
        !hasRoleAnchor(jobs, preparedToken) &&
        jobs.some((job) => bestGeoMatch(job, preparedToken).score >= 30)
      ) {
        geoTokenIndexes.add(index);
      }
    });

    if (geoTokenIndexes.size > 0) {
      effectiveLocation = rawTokens.filter((_, index) => geoTokenIndexes.has(index)).join(" ");
      roleQuery = rawTokens.filter((_, index) => !geoTokenIndexes.has(index)).join(" ");
    }
  }

  if (effectiveLocation) {
    effectiveLocation = resolveGeoQuery(jobs, effectiveLocation);
  }

  const preparedRole = prepareQuery(roleQuery);
  const preparedLocation = prepareQuery(effectiveLocation);
  const locationActsAsGeo =
    Boolean(effectiveLocation) &&
    jobs.some((job) => bestGeoMatch(job, preparedLocation).score >= 30);

  const inputs = [
    { query: preparedRole, preferred: "role" as const },
    { query: preparedLocation, preferred: "location" as const },
  ].filter(({ query: prepared }) => Boolean(prepared.raw));

  if (!inputs.length) return [];

  const ranked: Array<{ job: SearchablePublishedJob; score: number }> = [];

  for (const job of jobs) {
    let score = 0;
    const kinds: MatchKind[] = [];
    let rejected = false;

    for (const input of inputs) {
      const inputActsAsRole =
        input.preferred === "role" ||
        (input.preferred === "location" && !locationActsAsGeo);

      if (inputActsAsRole && !titleSupportsRequiredRoleTokens(input.query, job)) {
        rejected = true;
        break;
      }

      const match =
        input.preferred === "location" && locationActsAsGeo
          ? bestGeoMatch(job, input.query)
          : bestMatch(job, input.query);

      if (match.score < 30) {
        rejected = true;
        break;
      }

      score += match.score + preferredBonus(match.kind, input.preferred);
      kinds.push(match.kind);
    }

    if (rejected) continue;

    if (
      inputs.length > 1 &&
      kinds.some((kind) => kind === "title" || kind === "category") &&
      kinds.some((kind) => kind === "location" || kind === "region")
    ) {
      score += 15;
    }

    ranked.push({ job, score });
  }

  ranked.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    const dateCompare = (b.job.posted_date || "").localeCompare(a.job.posted_date || "");
    if (dateCompare !== 0) return dateCompare;
    return a.job.title.localeCompare(b.job.title);
  });

  return ranked.map(({ job }) => job);
}

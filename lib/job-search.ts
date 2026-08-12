import type { PublishedJob } from "./published-jobs";

type MatchKind = "title" | "location" | "region" | "category" | "company" | "description" | "combined";

type FieldMatch = {
  score: number;
  kind: MatchKind;
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

// These concepts are narrow enough that a role search should be supported by
// the job title itself, rather than merely by the wider curated slice/category.
// Support-worker searches deliberately stay broader because Ontap's curated
// support supply includes equivalent care-assistant titles.
const TITLE_REQUIRED_ROLE_TOKENS = new Set(["admin", "customerservice", "reception"]);

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

    // Long, recognisably same-stem words can survive several omitted letters
    // (e.g. "admistrtr" -> "administrator") without making short tokens loose.
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

function queryTokens(value: string): string[] {
  const canonicalText = normalise(value)
    .split(/\s+/)
    .filter(Boolean)
    .map(canonicalQueryToken)
    .join(" ");

  return applyPhraseAliases(canonicalText).split(/\s+/).filter(Boolean);
}

function candidateTokens(value: string): string[] {
  const text = normalise(value);
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

function geoTokenMatches(query: string, candidate: string): boolean {
  return geoTokenMatchQuality(query, candidate) > 0;
}

function resolveGeoQuery(jobs: PublishedJob[], input: string): string {
  const wanted = normalise(input).split(/\s+/).filter(Boolean);
  if (!wanted.length) return input;

  const available = new Set<string>();
  for (const job of jobs) {
    for (const value of [job.location, job.region]) {
      normalise(value).split(/\s+/).filter(Boolean).forEach((token) => available.add(token));
    }
  }

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

function allTokensMatch(query: string, candidate: string): boolean {
  const wanted = queryTokens(query);
  if (!wanted.length) return false;
  const available = candidateTokens(candidate);
  return wanted.every((token) => available.some((candidateToken) => tokenMatches(token, candidateToken)));
}

function titleSupportsRequiredRoleTokens(query: string, title: string): boolean {
  const required = queryTokens(query).filter((token) => TITLE_REQUIRED_ROLE_TOKENS.has(token));
  if (!required.length) return true;

  const available = candidateTokens(title);
  return required.every((token) => available.some((candidateToken) => tokenMatches(token, candidateToken)));
}

function allGeoTokensMatch(query: string, candidate: string): boolean {
  const wanted = normalise(query).split(/\s+/).filter(Boolean);
  if (!wanted.length) return false;
  const available = normalise(candidate).split(/\s+/).filter(Boolean);
  return wanted.every((token) => available.some((candidateToken) => geoTokenMatches(token, candidateToken)));
}

function scoreField(query: string, value: string, scores: [number, number, number, number]): number {
  if (!query.trim() || !value.trim()) return 0;
  const q = normalise(query);
  const field = normalise(value);
  const [exact, starts, contains, token] = scores;

  if (field === q) return exact;
  if (field.startsWith(`${q} `) || q.startsWith(`${field} `)) return starts;
  if (field.includes(q)) return contains;
  if (allTokensMatch(query, value)) return token;
  return 0;
}

function scoreGeoField(query: string, value: string, scores: [number, number, number, number]): number {
  if (!query.trim() || !value.trim()) return 0;
  const q = normalise(query);
  const field = normalise(value);
  const [exact, starts, contains, token] = scores;

  if (field === q) return exact;
  if (field.startsWith(`${q} `) || q.startsWith(`${field} `)) return starts;
  if (field.includes(q) && q.length >= 4) return contains;
  if (allGeoTokensMatch(query, value)) return token;
  return 0;
}

function bestGeoMatch(job: PublishedJob, input: string): FieldMatch {
  const fields: Array<[MatchKind, string, [number, number, number, number]]> = [
    ["location", job.location, [230, 205, 180, 160]],
    ["region", job.region, [225, 200, 175, 155]],
  ];

  let best: FieldMatch = { score: 0, kind: "location" };
  for (const [kind, value, scores] of fields) {
    const score = scoreGeoField(input, value, scores);
    if (score > best.score) best = { score, kind };
  }
  return best;
}

function bestMatch(job: PublishedJob, input: string): FieldMatch {
  const fields: Array<[MatchKind, string, [number, number, number, number]]> = [
    ["title", job.title, [240, 215, 190, 165]],
    ["location", job.location, [230, 205, 180, 160]],
    ["region", job.region, [225, 200, 175, 155]],
    ["category", job.category, [145, 130, 120, 110]],
    ["company", `${job.company} ${job.advertiser_name}`, [105, 95, 85, 75]],
    ["description", job.description.slice(0, 2200), [50, 45, 38, 32]],
  ];

  let best: FieldMatch = { score: 0, kind: "description" };
  for (const [kind, value, scores] of fields) {
    const score = scoreField(input, value, scores);
    if (score > best.score) best = { score, kind };
  }

  const combined = `${job.title} ${job.location} ${job.region}`;
  if (allTokensMatch(input, combined) && best.score < 150) {
    best = { score: 150, kind: "combined" };
  }

  return best;
}

function preferredBonus(kind: MatchKind, preferred: "role" | "location"): number {
  if (preferred === "role" && (kind === "title" || kind === "category")) return 12;
  if (preferred === "location" && (kind === "location" || kind === "region")) return 12;
  return 0;
}

export function searchJobs(jobs: PublishedJob[], query: string, location: string): PublishedJob[] {
  let roleQuery = query.trim();
  let effectiveLocation = location.trim();

  // A rushed one-box search such as "cust srv ncl" or "west york admin"
  // should still separate a recognisable place from the role terms. Only infer
  // geography when the dedicated location box is empty.
  if (roleQuery && !effectiveLocation) {
    const rawTokens = normalise(roleQuery).split(/\s+/).filter(Boolean);
    const geoTokenIndexes = new Set<number>();

    rawTokens.forEach((token, index) => {
      if (jobs.some((job) => bestGeoMatch(job, token).score >= 30)) {
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

  const locationActsAsGeo = Boolean(effectiveLocation) && jobs.some((job) => bestGeoMatch(job, effectiveLocation).score >= 30);

  const inputs = [
    { value: roleQuery, preferred: "role" as const },
    { value: effectiveLocation, preferred: "location" as const },
  ].filter(({ value }) => Boolean(value));

  if (!inputs.length) return [];

  const ranked = jobs.flatMap((job) => {
    let score = 0;
    const kinds: MatchKind[] = [];

    for (const input of inputs) {
      const inputActsAsRole = input.preferred === "role" || (input.preferred === "location" && !locationActsAsGeo);
      if (inputActsAsRole && !titleSupportsRequiredRoleTokens(input.value, job.title)) return [];

      const match =
        input.preferred === "location" && locationActsAsGeo
          ? bestGeoMatch(job, input.value)
          : bestMatch(job, input.value);
      if (match.score < 30) return [];
      score += match.score + preferredBonus(match.kind, input.preferred);
      kinds.push(match.kind);
    }

    if (
      inputs.length > 1 &&
      kinds.some((kind) => kind === "title" || kind === "category") &&
      kinds.some((kind) => kind === "location" || kind === "region")
    ) {
      score += 15;
    }

    return [{ job, score }];
  });

  ranked.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    const dateCompare = (b.job.posted_date || "").localeCompare(a.job.posted_date || "");
    if (dateCompare !== 0) return dateCompare;
    return a.job.title.localeCompare(b.job.title);
  });

  return ranked.map(({ job }) => job);
}
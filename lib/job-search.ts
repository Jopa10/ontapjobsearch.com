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

function canonicalToken(token: string): string {
  const clean = token.replace(/^\.+|\.+$/g, "");
  return TOKEN_ALIASES[clean] || clean;
}

function queryTokens(value: string): string[] {
  let text = normalise(value);
  text = text
    .replace(/\bcustomer services?\b/g, " customerservice ")
    .replace(/\bcustomer support\b/g, " customerservice ")
    .replace(/\bhuman resources?\b/g, " hr ")
    .replace(/\bpersonal assistant\b/g, " pa ")
    .replace(/\bexecutive assistant\b/g, " ea ")
    .replace(/\bcontact cent(?:re|er)\b/g, " contactcentre ")
    .replace(/\bfront of house\b/g, " reception ")
    .replace(/\bsupport worker\b/g, " supportworker ");

  return text.split(/\s+/).filter(Boolean).map(canonicalToken);
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

function allTokensMatch(query: string, candidate: string): boolean {
  const wanted = queryTokens(query);
  if (!wanted.length) return false;
  const available = candidateTokens(candidate);
  return wanted.every((token) => available.some((candidateToken) => tokenMatches(token, candidateToken)));
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
  const inputs = [
    { value: query.trim(), preferred: "role" as const },
    { value: location.trim(), preferred: "location" as const },
  ].filter(({ value }) => Boolean(value));

  if (!inputs.length) return [];

  const ranked = jobs.flatMap((job) => {
    let score = 0;
    const kinds: MatchKind[] = [];

    for (const input of inputs) {
      const match = bestMatch(job, input.value);
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

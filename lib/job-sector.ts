export type JobSector = "business" | "public";

export type JobSectorLabel =
  | "NHS / GP"
  | "School"
  | "Council"
  | "Charity"
  | "Public service";

export type SectorJobInput = {
  title?: string;
  company?: string;
  advertiser_name?: string;
  source?: string;
  summary?: string;
  description?: string;
  full_description?: string;
};

export type JobSectorResult = {
  sector: JobSector;
  label?: JobSectorLabel;
};

function combinedText(job: SectorJobInput) {
  return [
    job.title,
    job.company,
    job.advertiser_name,
    job.summary,
    job.description,
    job.full_description,
  ]
    .filter(Boolean)
    .join(" ");
}

function identityText(job: SectorJobInput) {
  return [job.title, job.company, job.advertiser_name].filter(Boolean).join(" ");
}

/**
 * A deliberately conservative first-pass classifier. Known public-sector feeds
 * are authoritative; JobG8 roles move only when their wording is explicit.
 * Everything uncertain stays in the business and agency view.
 */
export function classifyJobSector(job: SectorJobInput): JobSectorResult {
  const source = (job.source || "").trim().toLowerCase();

  if (source === "nhs jobs") return { sector: "public", label: "NHS / GP" };
  if (source === "teaching vacancies") return { sector: "public", label: "School" };
  if (source === "vonne") return { sector: "public", label: "Charity" };

  const identity = identityText(job);
  const text = combinedText(job);

  if (/\b(?:nhs|national health service|gp surgery|general practice)\b/i.test(identity)) {
    return { sector: "public", label: "NHS / GP" };
  }
  if (/\b(?:borough|county|district|city|parish|town) council\b|\blocal authority\b/i.test(identity)) {
    return { sector: "public", label: "Council" };
  }
  if (/\b(?:registered charity|charitable organisation|charity sector|voluntary sector|non-profit|not-for-profit|hospice)\b/i.test(text)) {
    return { sector: "public", label: "Charity" };
  }
  if (/\b(?:civil service|government department|police service|fire and rescue service)\b/i.test(identity)) {
    return { sector: "public", label: "Public service" };
  }

  return { sector: "business" };
}

export function findNthJobSectorIndex(
  jobs: SectorJobInput[],
  sector: JobSector,
  occurrence: number,
) {
  if (occurrence < 1) return -1;

  let matches = 0;
  for (const [index, job] of jobs.entries()) {
    if (classifyJobSector(job).sector !== sector) continue;
    matches += 1;
    if (matches === occurrence) return index;
  }
  return -1;
}

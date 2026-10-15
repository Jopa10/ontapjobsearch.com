import fs from "node:fs";
import path from "node:path";
import { normaliseJobTitle } from "@/lib/job-title";
import { getCanonicalPublishedJobId } from "@/lib/published-job-canonical-ids";

export type JobRow = {
  job_id: string;
  title: string;
  company: string;
  advertiser_name: string;
  advertiser_type: string;
  location: string;
  region: string;
  country: string;
  category: string;
  employment_type: string;
  salary_min: string;
  salary_max: string;
  salary_period: string;
  salary_text: string;
  work_pattern: string;
  working_arrangement: string;
  working_arrangement_text: string;
  working_arrangement_evidence: string;
  posted_date: string;
  posted_date_basis: string;
  closing_date: string;
  summary: string;
  description: string;
  full_description: string;
  apply_url: string;
  source: string;
  hc_tier: string;
  switchability: string;
};


function readJobsJson(jsonPath: readonly string[], region: string): JobRow[] {
  const filePath = path.join(process.cwd(), ...jsonPath);
  if (!fs.existsSync(filePath)) return [];

  let parsed: unknown;
  try {
    parsed = JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return [];
  }

  if (!Array.isArray(parsed) || parsed.length === 0) return [];

  return parsed
    .filter((row): row is Record<string, unknown> => Boolean(row && typeof row === "object"))
    .map((row) => ({
      job_id: String(row.job_id || row["/Job/DisplayReference"] || ""),
      title: normaliseJobTitle(String(row.title || row["/Job/Position"] || "")),
      company: String(row.company || row["/Job/AdvertiserName"] || ""),
      advertiser_name: String(row.advertiser_name || row["/Job/AdvertiserName"] || ""),
      advertiser_type: String(row.advertiser_type || row["/Job/AdvertiserType"] || ""),
      location: String(row.location || row["/Job/Area"] || ""),
      region: String(row.region || region),
      country: String(row.country || "UK"),
      category: String(row.category || ""),
      employment_type: String(row.employment_type || row["/Job/EmploymentType"] || ""),
      salary_min: String(row.salary_min || row["/Job/SalaryMinimum"] || ""),
      salary_max: String(row.salary_max || row["/Job/SalaryMaximum"] || ""),
      salary_period: String(row.salary_period || row["/Job/SalaryPeriod"] || ""),
      salary_text: String(row.salary_text || row["/Job/SalaryAdditional"] || ""),
      work_pattern: String(row.work_pattern || row["/Job/WorkHours"] || ""),
      working_arrangement: String(row.working_arrangement || ""),
      working_arrangement_text: String(row.working_arrangement_text || ""),
      working_arrangement_evidence: String(row.working_arrangement_evidence || ""),
      posted_date: String(row.posted_date || ""),
      posted_date_basis: String(row.posted_date_basis || ""),
      closing_date: String(row.closing_date || ""),
      summary: String(row.summary || ""),
      description: String(row.description || ""),
      full_description: String(
        row.full_description || row.description || row["/Job/Description"] || ""
      ),
      apply_url: String(row.apply_url || row["/Job/ApplicationURL"] || ""),
      source: String(row.source || "JobG8"),
      hc_tier: String(row.hc_tier || ""),
      switchability: String(row.switchability || ""),
    }));
}

function canonicaliseJobRows(jobs: JobRow[]): JobRow[] {
  const byCanonicalId = new Map<string, JobRow>();
  for (const job of jobs) {
    const job_id = getCanonicalPublishedJobId(job.job_id);
    if (!byCanonicalId.has(job_id)) byCanonicalId.set(job_id, { ...job, job_id });
  }
  return [...byCanonicalId.values()];
}


// Counts and listing pages must use the same membership and duplicate handling.
export function getJobSliceJobs(
  jsonPath: readonly string[],
  region: string,
  jobFilter?: (job: JobRow) => boolean
): JobRow[] {
  const jobs = canonicaliseJobRows(readJobsJson(jsonPath, region));
  return jobFilter ? jobs.filter(jobFilter) : jobs;
}

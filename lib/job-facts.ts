export type JobFactsInput = {
  company?: string;
  advertiser_name?: string;
  advertiser_type?: string;
  location?: string;
  employment_type?: string;
  salary_text?: string;
  work_pattern?: string;
  working_arrangement?: string;
  working_arrangement_text?: string;
  posted_date?: string;
  posted_date_basis?: string;
  closing_date?: string;
  source?: string;
};

export type JobFact = {
  key:
    | "employer"
    | "location"
    | "salary"
    | "contract"
    | "work_pattern"
    | "working_arrangement"
    | "posted"
    | "closing";
  label: string;
  value: string;
};

function text(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

export function sourceLabel(value: string): string {
  const source = text(value);
  if (!source) return "";
  if (source.toLowerCase() === "nejobs") return "North East Jobs";
  return source;
}

export function cleanEmployerName(job: JobFactsInput): string {
  const explicit = text(job.advertiser_name);
  if (explicit) return explicit;

  const company = text(job.company);
  if (!company) return "";

  const parts = company
    .split(" - ")
    .map((part) => part.trim())
    .filter(Boolean);
  const employmentType = text(job.employment_type);

  if (parts.length > 1 && employmentType && parts.at(-1) === employmentType) {
    parts.pop();
  }
  if (
    parts.length > 1 &&
    /^(agency|company|direct employer|employer)$/i.test(parts.at(-1) || "")
  ) {
    parts.pop();
  }

  return parts.join(" - ") || company;
}

export function employerFactLabel(job: JobFactsInput): string {
  const advertiserType = text(job.advertiser_type);
  const combinedCompany = text(job.company);
  if (/agency/i.test(advertiserType) || /\s-\sagency(?:\s-|$)/i.test(combinedCompany)) {
    return "Advertiser";
  }
  return "Employer";
}

export function formatSalary(value: string): string {
  let salary = text(value)
    .replace(/Â£/g, "£")
    .replace(/Â/g, "")
    .replace(/â€“/g, "–")
    .replace(/â€”/g, "—")
    .replace(/&pound;/gi, "£")
    .replace(/&ndash;/gi, "–")
    .replace(/&mdash;/gi, "—")
    .replace(/&nbsp;/gi, " ");

  if (!salary) return "";

  if (/\bper year\b|\bper annum\b/i.test(salary)) {
    salary = salary.replace(/£\s*(\d[\d,]*(?:\.\d+)?)/g, (match, amount) => {
      const numeric = Number(amount.replace(/,/g, ""));
      if (!Number.isFinite(numeric)) return match;
      return `£${Math.round(numeric).toLocaleString("en-GB")}`;
    });
  } else {
    salary = salary.replace(/£\s*(\d{4,})(?=\s|[-–—,;.)]|$)/g, (_, amount) => {
      const numeric = Number(amount);
      return Number.isFinite(numeric)
        ? `£${Math.round(numeric).toLocaleString("en-GB")}`
        : `£${amount}`;
    });
  }

  return salary.replace(/\){2,}$/g, ")").replace(/\s{2,}/g, " ").trim();
}

export function formatJobDate(value: string): string {
  const match = text(value).match(/^(\d{4})-(\d{2})-(\d{2})(?:T.*)?$/);
  if (!match) return "";

  const date = new Date(
    Date.UTC(Number(match[1]), Number(match[2]) - 1, Number(match[3]), 12)
  );
  if (Number.isNaN(date.getTime())) return "";

  return new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).format(date);
}

function usableWorkPattern(job: JobFactsInput): string {
  const workPattern = text(job.work_pattern);
  if (!workPattern) return "";
  if (/^please see (?:the )?advert(?: text)?$/i.test(workPattern)) return "";
  if (workPattern.toLowerCase() === text(job.employment_type).toLowerCase()) return "";
  return workPattern;
}

function workingArrangement(job: JobFactsInput): string {
  const arrangement = text(job.working_arrangement).toLowerCase();
  if (!new Set(["hybrid", "partly_remote"]).has(arrangement)) return "";
  return text(job.working_arrangement_text) || "Hybrid working";
}

export function buildJobFacts(job: JobFactsInput): JobFact[] {
  const facts: JobFact[] = [];
  const employer = cleanEmployerName(job);
  const location = text(job.location);
  const salary = formatSalary(text(job.salary_text));
  const contract = text(job.employment_type);
  const workPattern = usableWorkPattern(job);
  const arrangement = workingArrangement(job);
  const posted = formatJobDate(text(job.posted_date));
  const postedBasis = text(job.posted_date_basis).toLowerCase();
  const closing = formatJobDate(text(job.closing_date));

  if (employer) facts.push({ key: "employer", label: employerFactLabel(job), value: employer });
  if (location) facts.push({ key: "location", label: "Location", value: location });
  if (salary) facts.push({ key: "salary", label: "Salary", value: salary });
  if (contract) facts.push({ key: "contract", label: "Contract", value: contract });
  if (workPattern) facts.push({ key: "work_pattern", label: "Work pattern", value: workPattern });
  if (arrangement) {
    facts.push({
      key: "working_arrangement",
      label: "Working arrangement",
      value: arrangement,
    });
  }
  if (posted && postedBasis === "source") {
    facts.push({ key: "posted", label: "Posted", value: posted });
  } else if (posted && postedBasis === "ontap_first_published") {
    facts.push({ key: "posted", label: "First listed by Ontap", value: posted });
  } else if (posted && text(job.source).toLowerCase() === "nejobs") {
    // Backwards-compatible safety for approved external records published before
    // the explicit date-basis marker was introduced.
    facts.push({ key: "posted", label: "Posted", value: posted });
  }
  if (closing) facts.push({ key: "closing", label: "Closing date", value: closing });

  return facts;
}

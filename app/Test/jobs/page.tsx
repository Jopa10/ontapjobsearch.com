import fs from "node:fs";
import path from "node:path";

type JobRow = {
  job_id: string;
  title: string;
  company: string;
  location: string;
  region: string;
  country: string;
  category: string;
  employment_type: string;
  salary_min: string;
  salary_max: string;
  salary_text: string;
  posted_date: string;
  description: string;
  apply_url: string;
  source: string;
};

// Minimal CSV parser that handles quoted fields + commas inside quotes
function parseCsv(csvText: string): Record<string, string>[] {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let inQuotes = false;

  for (let i = 0; i < csvText.length; i++) {
    const c = csvText[i];
    const next = csvText[i + 1];

    if (c === '"') {
      if (inQuotes && next === '"') {
        field += '"'; // escaped quote
        i++;
      } else {
        inQuotes = !inQuotes;
      }
      continue;
    }

    if (!inQuotes && c === ",") {
      row.push(field);
      field = "";
      continue;
    }

    if (!inQuotes && (c === "\n" || c === "\r")) {
      // handle CRLF
      if (c === "\r" && next === "\n") i++;
      row.push(field);
      field = "";
      rows.push(row);
      row = [];
      continue;
    }

    field += c;
  }

  // last field
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }

  if (rows.length < 2) return [];

  const headers = rows[0].map((h) => h.trim());
  return rows
    .slice(1)
    .filter((r) => r.some((cell) => (cell ?? "").trim() !== ""))
    .map((r) => {
      const obj: Record<string, string> = {};
      headers.forEach((h, idx) => {
        obj[h] = (r[idx] ?? "").trim();
      });
      return obj;
    });
}

function readJobsCsv(): JobRow[] {
  const filePath = path.join(process.cwd(), "data", "jobs.csv");
  const csv = fs.readFileSync(filePath, "utf8");
  const parsed = parseCsv(csv);

  return parsed.map((r) => ({
    job_id: r.job_id || "",
    title: r.title || "",
    company: r.company || "",
    location: r.location || "",
    region: r.region || "",
    country: r.country || "",
    category: r.category || "",
    employment_type: r.employment_type || "",
    salary_min: r.salary_min || "",
    salary_max: r.salary_max || "",
    salary_text: r.salary_text || "",
    posted_date: r.posted_date || "",
    description: r.description || "",
    apply_url: r.apply_url || "",
    source: r.source || "",
  }));
}

export default function TestJobsPage() {
  const jobs = readJobsCsv();

  return (
    <main style={{ maxWidth: 980, margin: "40px auto", padding: "0 16px" }}>
      <h1>Test Jobs (CSV)</h1>
      <p>
        Loaded <b>{jobs.length}</b> jobs from <code>data/jobs.csv</code>
      </p>

      <div style={{ display: "grid", gap: 12 }}>
        {jobs.map((j) => (
          <div
            key={j.job_id}
            style={{
              border: "1px solid #e5e7eb",
              borderRadius: 10,
              padding: 14,
            }}
          >
            <div style={{ fontSize: 18, fontWeight: 700 }}>{j.title}</div>
            <div style={{ marginTop: 6 }}>
              <b>{j.company}</b> — {j.location}
            </div>
            <div style={{ marginTop: 6, opacity: 0.85 }}>
              {j.salary_text ? j.salary_text : ""}
              {j.salary_text && j.employment_type ? " · " : ""}
              {j.employment_type ? j.employment_type : ""}
              {j.posted_date ? ` · Posted ${j.posted_date}` : ""}
            </div>

            <div style={{ marginTop: 10 }}>
              <a href={j.apply_url} target="_blank" rel="noreferrer">
                Apply (external)
              </a>
              <span style={{ marginLeft: 12, opacity: 0.7 }}>
                Job ID: {j.job_id}
              </span>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}

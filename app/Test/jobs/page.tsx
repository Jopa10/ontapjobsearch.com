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
  const filePath = path.join(process.cwd(), "data", "leeds-feb26-slice.json");
  const parsed = JSON.parse(fs.readFileSync(filePath, "utf8"));
  
  return parsed.map((r: any) => ({
  job_id: r.job_id || r.jobapplicationurl || "",
  title: r.title || r.jobtitle || "",
  company: r.company || r.companyname || "",
  location: r.location || r.joblocation || "",
  region: r.region || "",
  country: r.country || "",
  category: r.category || r.jobcategory || "",
  employment_type: r.employment_type || r.jobtype || "",
  salary_min: r.salary_min || "",
  salary_max: r.salary_max || "",
  salary_text: r.salary_text || r.otherdetails || "",
  posted_date: r.posted_date || "",
  description: r.description || r.jobdescription || "",
  apply_url: r.apply_url || r.jobapplicationurl || "",
  source: r.source || ""
}));
}

export default function TestJobsPage() {
  const jobs = readJobsCsv();

  return (
    <main style={{ maxWidth: 980, margin: "40px auto", padding: "0 16px" }}>
      Test Jobs (CSV) → Test Jobs (JSON)
      <p>
        data/jobs.csv → data/leeds-feb26-slice.json
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
        <div style={{ fontSize: 18, fontWeight: 700, marginBottom: 4 }}>
  {j.title}
</div>

<div style={{ fontSize: 14, color: "#555", marginBottom: 8 }}>
  {j.company} • {j.location}
  {j.posted_date ? ` • Closes ${j.posted_date}` : ""}
  {j.salary_text ? ` • ${j.salary_text}` : ""}
</div>

<div style={{ marginTop: 8 }}>
  <a
    href={j.apply_url}
    target="_blank"
    rel="noreferrer"
    style={{
      display: "inline-block",
      background: "#2563eb",
      color: "white",
      padding: "6px 12px",
      borderRadius: 6,
      fontSize: 14,
      textDecoration: "none"
    }}
  >
    Apply Now
  </a>
  <span style={{ marginLeft: 12, fontSize: 12, opacity: 0.6 }}>
  Job ID: {j.job_id}
</span>
</div>
          </div>
        ))}
      </div>
    </main>
  );
}

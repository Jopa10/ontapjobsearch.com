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
  closing_date: string;
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
  closing_date: r.closing_date || "",
  description: r.description || r.jobdescription || "",
  apply_url: r.apply_url || r.jobapplicationurl || "",
  source: r.source || ""
}));
}
function getEmployerType(name: string) {
  if (/NHS|Hospital|Trust/i.test(name)) return "NHS";
  if (/Surgery|Medical Centre|GP/i.test(name)) return "GP Practice";
  if (/University/i.test(name)) return "University";
  if (/Council|City Council/i.test(name)) return "Council";
  return "Private";
}
export default function TestJobsPage() {
  const jobs = readJobsCsv();

  return (
    <main style={{ maxWidth: 980, margin: "40px auto", padding: "0 16px" }}>
      <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 6 }}>
  Leeds NHS Admin Jobs
</h1>
 <p style={{ 
  fontSize: 14, 
  fontWeight: 600, 
  color: "#334155", 
  marginBottom: 8 
}}>
  Last updated: 5 March 2026
</p>
<p style={{ color: "#555", marginBottom: 20 }}>
  Updated daily • Roles across Leeds hospitals and NHS services • Apply on employer sites
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
<div style={{ marginBottom: 4 }}>
  <span style={{
    fontSize: 12,
    fontWeight: 600,
    color: "#475569"
  }}>
    {getEmployerType(j.company)}
  </span>
</div>
<div style={{ fontSize: 14, color: "#555", marginBottom: 8 }}>
  {j.company} • {j.location}
  {j.closing_date ? ` • Closes ${j.closing_date}` : ""}
  {j.salary_min && j.salary_max
  ? ` • £${Number(j.salary_min).toLocaleString()}–£${Number(j.salary_max).toLocaleString()}`
  : j.salary_text
  ? ` • ${j.salary_text}`
  : ""}
</div>
            <div
  style={{
    fontSize: 14,
    color: "#555",
    marginBottom: 12,
    overflow: "hidden",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
  }}
  title={j.description || ""}
>
  {j.description ? j.description.replace(/\s+/g, " ").trim() : ""}
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
</div>
          </div>
        ))}
      </div>
    </main>
  );
}

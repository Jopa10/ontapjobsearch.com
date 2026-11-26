import { Pool } from "pg";
import { writeFile } from "node:fs/promises";

const EMAIL = "jpbt801@gmail.com";
const expectedBranch = "refs/heads/feat/cpc-alert-neon-signup";
if (process.env.GITHUB_REF !== expectedBranch ||
    process.env.GITHUB_WORKFLOW !== "Private CPC daily matching test") {
  throw new Error("Neon alert reads are restricted to the Preview private-test workflow.");
}
const email = String(process.argv[2] || "").trim().toLowerCase();
if (email !== EMAIL) throw new Error("Neon alert reads allow only the approved private test recipient.");
if (process.env.ONTAP_EMAIL_PREVIEW_NEON_PROJECT_ID !== "withered-bread-65990253") {
  throw new Error("The private sender is limited to the approved Preview Neon project.");
}
const connectionString = process.env.ONTAP_EMAIL_PREVIEW_DATABASE_URL;
if (!connectionString) throw new Error("Preview Neon connection is not configured for this GitHub environment.");
const connection = new URL(connectionString);
if (!/^ep-summer-sky-bj8rt5vi(?:-pooler)?\.c-3\.eu-west-2\.aws\.neon\.tech$/.test(connection.hostname) ||
    connection.pathname !== "/neondb" ||
    !["require", "verify-full"].includes(connection.searchParams.get("sslmode") || "")) {
  throw new Error("The private sender requires TLS to the approved Neon host.");
}

const pool = new Pool({ connectionString, max: 1, idleTimeoutMillis: 5000, connectionTimeoutMillis: 8000 });
try {
  const result = await pool.query(
    "SELECT ue.email, ue.user_id, ue.id AS user_email_id, s.id AS subscriber_id, " +
    "p.id AS preference_id, p.criteria, p.signup_job_public_id " +
    "FROM ontap_shadow.user_emails ue " +
    "JOIN ontap_shadow.subscribers s ON s.user_email_id = ue.id AND s.user_id = ue.user_id " +
    "JOIN ontap_shadow.subscriber_preferences p ON p.subscriber_id = s.id AND p.user_id = ue.user_id " +
    "JOIN LATERAL (SELECT c.action FROM ontap_shadow.consent_history c " +
    "WHERE c.user_email_id = ue.id AND c.purpose = 'cpc_job_alerts' " +
    "ORDER BY c.occurred_at DESC, c.id DESC LIMIT 1) latest_consent ON latest_consent.action = 'granted' " +
    "WHERE ue.email_key = lower(trim($1)) AND ue.alert_status = 'active' " +
    "AND s.status = 'active' AND p.active = true ORDER BY p.created_at, p.id LIMIT 10",
    [email],
  );
  if (!result.rows.length) throw new Error("No active, consented alert preferences were found in Preview Neon.");
  const first = result.rows[0];
  const preferences = result.rows.map(row => {
    const criteria = typeof row.criteria === "string" ? JSON.parse(row.criteria) : row.criteria;
    if (!criteria || typeof criteria.role !== "string" || !criteria.role.trim() ||
        typeof criteria.location !== "string" || !criteria.location.trim() ||
        typeof criteria.salary !== "string" ||
        (criteria.region != null && typeof criteria.region !== "string")) {
      throw new Error("Preview Neon contains invalid alert criteria; no email will be sent.");
    }
    return { role: criteria.role, location: criteria.location, salary: criteria.salary,
      ...(typeof criteria.region === "string" && criteria.region.trim() ? { region: criteria.region.trim() } : {}),
      preferenceId: String(row.preference_id), signupJobPublicId: row.signup_job_public_id || null };
  });
  const output = JSON.stringify({
    email: String(first.email).toLowerCase(), userId: String(first.user_id),
    userEmailId: String(first.user_email_id), subscriberId: String(first.subscriber_id),
    consentAction: "granted", preferences,
  });
  const outputFile = process.env.NEON_ALERT_PREFERENCES_OUTPUT;
  if (!outputFile) throw new Error("A temporary output file is required for the private Neon read.");
  await writeFile(outputFile, output, { mode: 0o600 });
} finally {
  await pool.end();
}

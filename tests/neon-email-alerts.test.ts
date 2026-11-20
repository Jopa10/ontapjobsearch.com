import assert from "node:assert/strict";
import test from "node:test";
import { saveJobAlertSignupToNeon, activateJobAlertSignupInNeon, type AlertDbPool } from "../lib/neon-email-alerts";
import { JOB_ALERT_CONSENT_TEXT, JOB_ALERT_CONSENT_VERSION } from "../lib/job-alert-consent";

const env = { VERCEL_ENV: "preview", VERCEL_GIT_COMMIT_REF: "feat/cpc-alert-neon-signup",
  ONTAP_SHADOW_DATABASE_URL: "postgres://preview-only.invalid/test" };
const signup = { email: " JNABON1108@gmail.com ", role: "Accounts Assistant", location: "Leeds",
  salary: "£27,000", region: "West Yorkshire", jobId: "12345", source: "JobG8",
  signupAttemptId: "1b7d1d7e-47fb-4a72-9c88-9a06df9d4c2b", signupDevice: "mobile" as const,
  consentText: JOB_ALERT_CONSENT_TEXT, consentVersion: JOB_ALERT_CONSENT_VERSION,
  consentSource: "apply_job_alert_signup" };
function fakePool() {
  const statements: { sql: string; values?: unknown[] }[] = [];
  const client = { async query(sql: string, values?: unknown[]) {
    statements.push({ sql, values });
    if (sql.includes("SELECT id, user_id FROM ontap_shadow.user_emails")) return { rows: [] };
    if (sql.includes("INSERT INTO ontap_shadow.subscribers")) return { rows: [{ id: values?.[0] }], rowCount: 1 };
    if (sql.includes("SELECT id FROM ontap_shadow.jobs")) return { rows: [] };
    if (sql.includes("INSERT INTO ontap_shadow.subscriber_preferences")) return { rows: [{ id: values?.[0] }], rowCount: 1 };
    if (sql.includes("INSERT INTO ontap_shadow.consent_history")) return { rows: [{ id: values?.[0] }], rowCount: 1 };
    if (sql.includes("UPDATE ontap_shadow.subscribers")) return { rows: [], rowCount: 1 };
    return { rows: [], rowCount: 1 };
  }, release() {} };
  return { statements, pool: { async connect() { return client; } } as AlertDbPool };
}
test("signup stores linked user, address, preference, clicked job and consent in one transaction", async () => {
  const f = fakePool();
  const result = await saveJobAlertSignupToNeon(signup, { env, pool: f.pool, now: () => new Date("2026-11-18T08:00:00Z") });
  assert.match(result.userId, /^[0-9a-f-]{36}$/i);
  assert.match(result.userEmailId, /^[0-9a-f-]{36}$/i);
  assert.equal(f.statements[0].sql, "BEGIN");
  assert.equal(f.statements.at(-1)?.sql, "COMMIT");
  assert.ok(f.statements.some(s => s.sql.includes("INSERT INTO ontap_shadow.users")));
  assert.ok(f.statements.some(s => s.sql.includes("INSERT INTO ontap_shadow.user_emails") && s.values?.[2] === "jnabon1108@gmail.com"));
  const preference = f.statements.find(s => s.sql.includes("INSERT INTO ontap_shadow.subscriber_preferences"));
  assert.equal(JSON.parse(String(preference?.values?.[4])).region, "West Yorkshire");
  assert.equal(preference?.values?.[6], "12345");
  const consent = f.statements.find(s => s.sql.includes("INSERT INTO ontap_shadow.consent_history"));
  assert.equal(consent?.values?.[4], JOB_ALERT_CONSENT_TEXT);
  assert.equal(consent?.values?.[8], signup.signupAttemptId);
  assert.equal(consent?.values?.[9], "mobile");
});
test("activation is Preview-branch-only and follows provider acceptance", async () => {
  const f = fakePool();
  await activateJobAlertSignupInNeon(signup.email, { env, pool: f.pool });
  assert.ok(f.statements.some(s => s.sql.includes("UPDATE ontap_shadow.user_emails SET alert_status = 'active'")));
  assert.ok(f.statements.some(s => s.sql.includes("UPDATE ontap_shadow.subscribers SET status = 'active'")));
  await assert.rejects(saveJobAlertSignupToNeon(signup, { env: { ...env, VERCEL_ENV: "production" }, pool: f.pool }), /dedicated Preview test branch/);
});

import assert from "node:assert/strict";
import test from "node:test";
import { AlertPreferenceLimitError, getJobAlertPreferencesFromNeon, saveJobAlertSignupToNeon, activateJobAlertSignupInNeon, type AlertDbPool } from "../lib/neon-email-alerts";
import { JOB_ALERT_CONSENT_TEXT, JOB_ALERT_CONSENT_VERSION } from "../lib/job-alert-consent";

const env = { VERCEL_ENV: "preview", VERCEL_GIT_COMMIT_REF: "feat/cpc-alert-neon-signup",
  ONTAP_SHADOW_DATABASE_URL: "postgres://test:test@ep-preview.neon.tech/ontap?sslmode=require", ONTAP_SHADOW_NEON_PROJECT_ID: "noisy-fire-97386602" };
const signup = { email: " JNABON1108@gmail.com ", role: "Accounts Assistant", location: "Leeds",
  salary: "£27,000", region: "West Yorkshire", jobId: "12345", source: "JobG8",
  signupAttemptId: "1b7d1d7e-47fb-4a72-9c88-9a06df9d4c2b", signupDevice: "mobile" as const,
  consentText: JOB_ALERT_CONSENT_TEXT, consentVersion: JOB_ALERT_CONSENT_VERSION,
  consentSource: "apply_job_alert_signup" };
function fakePool(currentPreferences: Record<string, unknown>[] = []) {
  const statements: { sql: string; values?: unknown[] }[] = [];
  const client = { async query(sql: string, values?: unknown[]) {
    statements.push({ sql, values });
    if (sql.includes("SELECT id, user_id, alert_status FROM ontap_shadow.user_emails")) return { rows: [] };
    if (sql.includes("SELECT id, preference_key, criteria FROM ontap_shadow.subscriber_preferences")) return { rows: currentPreferences };
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

test("signup caps active preferences at ten in Neon and reports the existing alerts", async () => {
  const existing = Array.from({ length: 10 }, (_, index) => ({
    id: "pref-" + index, preference_key: "key-" + index,
    criteria: { role: "Accounts Assistant", location: "Town " + index, salary: "" },
  }));
  const f = fakePool(existing);
  await assert.rejects(saveJobAlertSignupToNeon(
    { ...signup, signupAttemptId: "aa000000-0000-4000-8000-000000000001" },
    { env, pool: f.pool },
  ), AlertPreferenceLimitError);
  assert.ok(!f.statements.some(s => s.sql.includes("INSERT INTO ontap_shadow.subscriber_preferences")));
});

test("GitHub readback is restricted to one active, consented Neon address", async () => {
  let readSql = "";
  const pool: AlertDbPool = {
    async connect() {
      return {
        async query(sql: string, values?: unknown[]) {
          readSql = sql;
          assert.deepEqual(values, ["jpbt801@gmail.com"]);
          return { rows: [{
            email: "jpbt801@gmail.com", user_id: "user-1", user_email_id: "email-1",
            subscriber_id: "subscriber-1", preference_id: "preference-1",
            criteria: { role: "Accounts Assistant", location: "Leeds", salary: "" },
            signup_job_id: "job-1", signup_job_public_id: "public-job-1",
          }] };
        },
        release() {},
      };
    },
  };
  const result = await getJobAlertPreferencesFromNeon(" JPBT801@gmail.com ", { env, pool });
  assert.equal(result?.userId, "user-1");
  assert.equal(result?.preferences[0].signupJobPublicId, "public-job-1");
  assert.match(readSql, /latest_consent[.]action = 'granted'/);
  assert.match(readSql, /p[.]active = true/);
  assert.match(readSql, /LIMIT 10/);
});


import { createHash, randomUUID } from "node:crypto";
import { Pool } from "pg";
import { ALERT_SIGNUP_TEST_BRANCH } from "./private-job-alert-test";

type Env = Record<string, string | undefined>;
type Row = Record<string, unknown>;
type QueryResult = { rows: Row[]; rowCount?: number | null };
type DbClient = {
  query(text: string, values?: unknown[]): Promise<QueryResult>;
  release(): void;
};
export type AlertDbPool = { connect(): Promise<DbClient> };

export class AlertPreferenceLimitError extends Error {}

export type NeonAlertPreference = { role: string; location: string; salary: string; region?: string; preferenceId: string; signupJobId: string | null; signupJobPublicId: string | null };
export type NeonAlertSignup = { email: string; userId: string; userEmailId: string; subscriberId: string; preferences: NeonAlertPreference[] };

type Signup = {
  email: string; role: string; location: string; salary: string; region?: string;
  jobId: string; source: string; signupAttemptId: string; signupDevice: "mobile" | "laptop" | "unknown";
  consentText: string; consentVersion: string; consentSource: string;
};

const globalPool = globalThis as typeof globalThis & { __ontapAlertSignupPool?: Pool };

function requirePreviewDatabase(env: Env): string {
  if (env.VERCEL_ENV !== "preview" || env.VERCEL_GIT_COMMIT_REF !== ALERT_SIGNUP_TEST_BRANCH) {
    throw new Error("Email-alert Neon writes are limited to the dedicated Preview test branch.");
  }
  if (env.ONTAP_SHADOW_NEON_PROJECT_ID !== "noisy-fire-97386602") {
    throw new Error("Email-alert writes are limited to the approved Preview Neon project.");
  }
  const url = env.ONTAP_SHADOW_DATABASE_URL;
  if (!url) throw new Error("Preview Neon connection is not configured.");
  const parsed = new URL(url);
  if (!parsed.hostname.endsWith(".neon.tech") ||
      !["require", "verify-full"].includes(parsed.searchParams.get("sslmode") || "")) {
    throw new Error("Preview Neon connection must use TLS and the approved Neon host.");
  }
  return url;
}

function poolFor(url: string): AlertDbPool {
  globalPool.__ontapAlertSignupPool ??= new Pool({
    connectionString: url, max: 1, idleTimeoutMillis: 5_000, connectionTimeoutMillis: 8_000,
  });
  return globalPool.__ontapAlertSignupPool as unknown as AlertDbPool;
}

function normalized(value: string): string {
  return value.trim().replace(/\s+/g, " ").toLowerCase();
}

function preferenceKey(signup: Signup): string {
  return createHash("sha256").update(JSON.stringify([
    normalized(signup.role), normalized(signup.location), normalized(signup.salary),
  ])).digest("hex");
}

export async function saveJobAlertSignupToNeon(
  signup: Signup,
  { env, pool, now = () => new Date() }: { env: Env; pool?: AlertDbPool; now?: () => Date },
): Promise<{ userId: string; userEmailId: string; subscriberId: string; preferenceId: string; consentId: string; alertCount: number; unchanged: boolean }> {
  const url = requirePreviewDatabase(env);
  const db = pool || poolFor(url);
  const client = await db.connect();
  const email = signup.email.trim().toLowerCase();
  const emailKey = normalized(email);
  const createdAt = now().toISOString();
  const key = preferenceKey(signup);
  const criteria = { role: signup.role.trim(), location: signup.location.trim(), salary: signup.salary.trim(), region: signup.region || null };
  const consentId = randomUUID();

  try {
    await client.query("BEGIN");
    await client.query("SELECT pg_advisory_xact_lock(hashtext($1))", [emailKey]);

    const identity = (await client.query(
      "SELECT id, user_id, alert_status FROM ontap_shadow.user_emails WHERE email_key = $1 FOR UPDATE", [emailKey],
    )).rows[0];
    let userId: string;
    let userEmailId: string;
    const wasActive = identity?.alert_status === "active";

    if (identity) {
      userId = String(identity.user_id);
      userEmailId = String(identity.id);
      await client.query(
        "UPDATE ontap_shadow.user_emails SET email = $2, alert_status = 'pending', updated_at = $3 WHERE id = $1",
        [userEmailId, email, createdAt],
      );
    } else {
      userId = randomUUID();
      userEmailId = randomUUID();
      await client.query("INSERT INTO ontap_shadow.users (id, created_at) VALUES ($1, $2)", [userId, createdAt]);
      await client.query(
        "INSERT INTO ontap_shadow.user_emails (id, user_id, email, email_key, alert_status, created_at, updated_at) VALUES ($1, $2, $3, $4, 'pending', $5, $5)",
        [userEmailId, userId, email, emailKey, createdAt],
      );
    }

    const subscriber = (await client.query(
      "INSERT INTO ontap_shadow.subscribers (id, email, email_key, status, created_at, updated_at, user_id, user_email_id) " +
      "VALUES ($1, $2, $3, 'pending', $4, $4, $5, $6) " +
      "ON CONFLICT (email_key) DO UPDATE SET email = EXCLUDED.email, status = 'pending', updated_at = EXCLUDED.updated_at " +
      "WHERE ontap_shadow.subscribers.user_id = EXCLUDED.user_id RETURNING id",
      [randomUUID(), email, emailKey, createdAt, userId, userEmailId],
    )).rows[0];
    if (!subscriber) throw new Error("The alert address is already linked to a different user record.");
    const subscriberId = String(subscriber.id);

    const job = (await client.query("SELECT id FROM ontap_shadow.jobs WHERE public_id = $1", [signup.jobId])).rows[0];
    const signupJobId = job ? String(job.id) : null;

    const currentPreferences = (await client.query(
      "SELECT id, preference_key, criteria FROM ontap_shadow.subscriber_preferences WHERE subscriber_id = $1 AND active = true FOR UPDATE",
      [subscriberId],
    )).rows;
    const currentPreference = currentPreferences.find(row => String(row.preference_key) === key);
    if (!currentPreference && currentPreferences.length >= 10) {
      throw new AlertPreferenceLimitError("You already have 10 saved alerts. Your existing alerts have been kept.");
    }
    const savedCriteriaRaw = currentPreference?.criteria;
    const savedCriteriaValue = typeof savedCriteriaRaw === "string" ? JSON.parse(savedCriteriaRaw) : savedCriteriaRaw;
    const savedCriteria = savedCriteriaValue && typeof savedCriteriaValue === "object" && !Array.isArray(savedCriteriaValue)
      ? savedCriteriaValue as Record<string, unknown>
      : null;
    const unchanged = Boolean(wasActive && currentPreference && savedCriteria &&
      String(savedCriteria.role || "") === criteria.role &&
      String(savedCriteria.location || "") === criteria.location &&
      String(savedCriteria.salary || "") === criteria.salary &&
      String(savedCriteria.region || "") === String(criteria.region || ""));

    const preference = (await client.query(
      "INSERT INTO ontap_shadow.subscriber_preferences " +
      "(id, subscriber_id, user_id, preference_key, criteria, signup_job_id, signup_job_public_id, active, created_at, updated_at) " +
      "VALUES ($1, $2, $3, $4, $5::jsonb, $6, $7, true, $8, $8) " +
      "ON CONFLICT (subscriber_id, preference_key) DO UPDATE SET user_id = EXCLUDED.user_id, criteria = EXCLUDED.criteria, " +
      "signup_job_id = COALESCE(EXCLUDED.signup_job_id, ontap_shadow.subscriber_preferences.signup_job_id), " +
      "signup_job_public_id = EXCLUDED.signup_job_public_id, active = true, updated_at = EXCLUDED.updated_at RETURNING id",
      [randomUUID(), subscriberId, userId, key, JSON.stringify(criteria), signupJobId, signup.jobId, createdAt],
    )).rows[0];
    if (!preference) throw new Error("The alert preference could not be saved.");

    const consent = (await client.query(
      "INSERT INTO ontap_shadow.consent_history " +
      "(id, subscriber_id, user_email_id, purpose, action, wording_version, wording_text, source, occurred_at, evidence, idempotency_key, signup_device) " +
      "VALUES ($1, $2, $3, 'cpc_job_alerts', 'granted', $4, $5, $6, $7, $8::jsonb, $9, $10) " +
      "ON CONFLICT (idempotency_key) DO NOTHING RETURNING id",
      [consentId, subscriberId, userEmailId, signup.consentVersion, signup.consentText, signup.consentSource, createdAt,
        JSON.stringify({ signupAttemptId: signup.signupAttemptId, sourceJobPublicId: signup.jobId, preferenceKey: key }),
        signup.signupAttemptId, signup.signupDevice],
    )).rows[0];
    await client.query("COMMIT");

    return {
      userId, userEmailId, subscriberId, preferenceId: String(preference.id),
      consentId: consent ? String(consent.id) : consentId,
      alertCount: currentPreferences.length + (currentPreference ? 0 : 1), unchanged,
    };
  } catch (error) {
    await client.query("ROLLBACK").catch(() => undefined);
    throw error;
  } finally {
    client.release();
  }
}

export async function getJobAlertPreferencesFromNeon(
  email: string,
  { env, pool }: { env: Env; pool?: AlertDbPool },
): Promise<NeonAlertSignup | null> {
  const url = requirePreviewDatabase(env);
  const client = await (pool || poolFor(url)).connect();
  const emailKey = normalized(email);
  try {
    const rows = (await client.query(
      "SELECT ue.email, ue.user_id, ue.id AS user_email_id, s.id AS subscriber_id, " +
      "p.id AS preference_id, p.criteria, p.signup_job_id, p.signup_job_public_id " +
      "FROM ontap_shadow.user_emails ue " +
      "JOIN ontap_shadow.subscribers s ON s.user_email_id = ue.id AND s.user_id = ue.user_id " +
      "JOIN ontap_shadow.subscriber_preferences p ON p.subscriber_id = s.id AND p.user_id = ue.user_id " +
      "JOIN LATERAL (SELECT c.action FROM ontap_shadow.consent_history c " +
      "WHERE c.user_email_id = ue.id AND c.purpose = 'cpc_job_alerts' " +
      "ORDER BY c.occurred_at DESC, c.id DESC LIMIT 1) latest_consent ON latest_consent.action = 'granted' " +
      "WHERE ue.email_key = $1 AND ue.alert_status = 'active' AND s.status = 'active' AND p.active = true " +
      "ORDER BY p.created_at, p.id LIMIT 10",
      [emailKey],
    )).rows;
    if (!rows.length) return null;
    const preferences = rows.map(row => {
      const rawCriteria = typeof row.criteria === "string" ? JSON.parse(row.criteria) : row.criteria;
      const criteria = rawCriteria && typeof rawCriteria === "object" && !Array.isArray(rawCriteria)
        ? rawCriteria as Record<string, unknown>
        : null;
      if (!criteria || typeof criteria.role !== "string" || !criteria.role.trim() ||
          typeof criteria.location !== "string" || !criteria.location.trim() ||
          typeof criteria.salary !== "string" ||
          (criteria.region != null && typeof criteria.region !== "string")) {
        throw new Error("Saved Neon alert preferences are invalid.");
      }
      return {
        role: criteria.role, location: criteria.location, salary: criteria.salary,
        ...(typeof criteria.region === "string" && criteria.region.trim() ? { region: criteria.region.trim() } : {}),
        preferenceId: String(row.preference_id), signupJobId: row.signup_job_id ? String(row.signup_job_id) : null,
        signupJobPublicId: row.signup_job_public_id ? String(row.signup_job_public_id) : null,
      };
    });
    const first = rows[0];
    return { email: String(first.email), userId: String(first.user_id), userEmailId: String(first.user_email_id),
      subscriberId: String(first.subscriber_id), preferences };
  } finally {
    client.release();
  }
}

export async function unsubscribeJobAlertInNeon(
  email: string,
  { env, pool, now = () => new Date() }: { env: Env; pool?: AlertDbPool; now?: () => Date },
): Promise<void> {
  const url = requirePreviewDatabase(env);
  const client = await (pool || poolFor(url)).connect();
  const emailKey = normalized(email);
  try {
    await client.query("BEGIN");
    await client.query("SELECT pg_advisory_xact_lock(hashtext($1))", [emailKey]);
    const row = (await client.query(
      "SELECT ue.id AS user_email_id, s.id AS subscriber_id, c.id AS latest_consent_id, " +
      "c.action AS latest_consent_action, c.wording_version, c.wording_text " +
      "FROM ontap_shadow.user_emails ue JOIN ontap_shadow.subscribers s ON s.user_email_id = ue.id " +
      "LEFT JOIN LATERAL (SELECT id, action, wording_version, wording_text FROM ontap_shadow.consent_history " +
      "WHERE user_email_id = ue.id AND purpose = 'cpc_job_alerts' ORDER BY occurred_at DESC, id DESC LIMIT 1) c ON true " +
      "WHERE ue.email_key = $1 FOR UPDATE OF ue, s",
      [emailKey],
    )).rows[0];
    if (!row) { await client.query("COMMIT"); return; }
    const occurredAt = now().toISOString();
    await client.query(
      "UPDATE ontap_shadow.user_emails SET alert_status = 'unsubscribed', updated_at = $2 WHERE id = $1",
      [row.user_email_id, occurredAt],
    );
    await client.query(
      "UPDATE ontap_shadow.subscribers SET status = 'unsubscribed', updated_at = $2 WHERE id = $1",
      [row.subscriber_id, occurredAt],
    );
    await client.query(
      "UPDATE ontap_shadow.subscriber_preferences SET active = false, updated_at = $2 WHERE subscriber_id = $1",
      [row.subscriber_id, occurredAt],
    );
    if (row.latest_consent_action === "granted" && row.latest_consent_id) {
      const id = randomUUID();
      const key = "withdrawn:" + String(row.latest_consent_id);
      await client.query(
        "INSERT INTO ontap_shadow.consent_history " +
        "(id, subscriber_id, user_email_id, purpose, action, wording_version, wording_text, source, occurred_at, evidence, idempotency_key, signup_device) " +
        "SELECT $1, $2, $3, 'cpc_job_alerts', 'withdrawn', $4, $5, 'job_alerts_unsubscribe', $6, jsonb_build_object('withdrawsConsentId', $7), $8, 'unknown' " +
        "WHERE NOT EXISTS (SELECT 1 FROM ontap_shadow.consent_history WHERE idempotency_key = $8)",
        [id, row.subscriber_id, row.user_email_id, row.wording_version || "v1",
          row.wording_text || "Job-alert email consent withdrawn by unsubscribe link.", occurredAt,
          row.latest_consent_id, key],
      );
    }
    await client.query("COMMIT");
  } catch (error) {
    await client.query("ROLLBACK").catch(() => undefined);
    throw error;
  } finally {
    client.release();
  }
}

export async function activateJobAlertSignupInNeon(
  email: string,
  { env, pool }: { env: Env; pool?: AlertDbPool },
): Promise<void> {
  const url = requirePreviewDatabase(env);
  const client = await (pool || poolFor(url)).connect();
  const emailKey = normalized(email);
  try {
    await client.query("BEGIN");
    await client.query(
      "UPDATE ontap_shadow.user_emails SET alert_status = 'active', updated_at = now() WHERE email_key = $1",
      [emailKey],
    );
    const result = await client.query(
      "UPDATE ontap_shadow.subscribers SET status = 'active', updated_at = now() WHERE email_key = $1 AND status = 'pending'",
      [emailKey],
    );
    if (result.rowCount !== 1) throw new Error("The saved alert could not be activated in Preview Neon.");
    await client.query("COMMIT");
  } catch (error) {
    await client.query("ROLLBACK").catch(() => undefined);
    throw error;
  } finally {
    client.release();
  }
}

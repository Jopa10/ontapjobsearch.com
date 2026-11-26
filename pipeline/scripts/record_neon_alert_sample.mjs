import { randomUUID } from "node:crypto";
import { readFile } from "node:fs/promises";
import { Pool } from "pg";

const env = process.env;
if (env.GITHUB_REF !== "refs/heads/feat/cpc-alert-neon-signup" ||
    env.GITHUB_WORKFLOW !== "Private CPC daily matching test" ||
    env.ONTAP_EMAIL_PREVIEW_NEON_PROJECT_ID !== "withered-bread-65990253") {
  throw new Error("Alert sample writes require the private Preview workflow.");
}
const url = new URL(env.ONTAP_EMAIL_PREVIEW_DATABASE_URL);
if (!/^ep-summer-sky-bj8rt5vi(?:-pooler)?\.c-3\.eu-west-2\.aws\.neon\.tech$/.test(url.hostname) ||
    url.pathname !== "/neondb" || !["require", "verify-full"].includes(url.searchParams.get("sslmode"))) {
  throw new Error("Alert sample writes require the verified Preview database and TLS.");
}

const saved = JSON.parse(await readFile(env.NEON_ALERT_PREFERENCES_OUTPUT, "utf8"));
if (saved.email !== "jpbt801@gmail.com" || saved.consentAction !== "granted") {
  throw new Error("Alert sample writes require the approved recipient's consent.");
}
let input = "";
for await (const chunk of process.stdin.setEncoding("utf8")) input += chunk;
const payload = JSON.parse(input);
const pool = new Pool({ connectionString: url.href, connectionTimeoutMillis: 8000 });
const client = await pool.connect();
try {
  if (payload.action === "reserve") {
    await client.query("BEGIN");
    const reserved = await client.query(`
      INSERT INTO ontap_shadow.emails_sent
        (id, subscriber_id, user_id, user_email_id, idempotency_key, status)
      SELECT $1, s.id, e.user_id, e.id, $2, 'sending'
      FROM ontap_shadow.subscribers s
      JOIN ontap_shadow.user_emails e ON e.id = s.user_email_id AND e.user_id = s.user_id
      WHERE s.id = $3 AND e.user_id = $4 AND e.id = $5 AND e.email_key = $6
        AND s.status = 'active' AND e.alert_status = 'active'
        AND (SELECT action FROM ontap_shadow.consent_history
             WHERE user_email_id = e.id AND purpose = 'cpc_job_alerts'
             ORDER BY occurred_at DESC, id DESC LIMIT 1) = 'granted'
      ON CONFLICT (idempotency_key) DO NOTHING RETURNING id
    `, [randomUUID(), payload.key, saved.subscriberId, saved.userId, saved.userEmailId, saved.email]);
    const id = reserved.rows[0]?.id;
    if (!id) {
      const existing = await client.query(`
        SELECT status FROM ontap_shadow.emails_sent
        WHERE idempotency_key = $1 AND subscriber_id = $2 AND user_id = $3 AND user_email_id = $4
      `, [payload.key, saved.subscriberId, saved.userId, saved.userEmailId]);
      if (existing.rows[0]?.status !== "sent") {
        throw new Error("This sample has an unresolved send or the signup is no longer active.");
      }
    }
    for (const match of id ? payload.matches : []) {
      const result = await client.query(`
        INSERT INTO ontap_shadow.job_recommendations
          (id, email_id, subscriber_id, user_id, user_email_id, preference_id,
           signup_job_id, recommended_job_id, reason, matcher_revision, matching_evidence)
        SELECT $1, $2, p.subscriber_id, p.user_id, $3, p.id, p.signup_job_id, j.id,
               'private_alert_match', $4, jsonb_build_object('public_job_id', j.public_id)
        FROM ontap_shadow.subscriber_preferences p
        CROSS JOIN ontap_shadow.jobs j
        WHERE p.id = $5 AND p.subscriber_id = $6 AND p.user_id = $7 AND p.active
          AND j.public_id = $8
      `, [randomUUID(), id, saved.userEmailId, env.GITHUB_SHA, match.preferenceId,
        saved.subscriberId, saved.userId, match.publicId]);
      if (result.rowCount !== 1) throw new Error("A matched job or its saved preference is missing in Preview Neon.");
    }
    await client.query("COMMIT");
    if (!id) console.log("already-sent");
  } else if (payload.action === "sent" || payload.action === "uncertain") {
    const result = await client.query(`
      UPDATE ontap_shadow.emails_sent
      SET status = $1, provider_message_id = $2,
          sent_at = CASE WHEN $1 = 'sent' THEN now() END,
          error_code = CASE WHEN $1 = 'uncertain' THEN 'brevo_result_unconfirmed' END
      WHERE idempotency_key = $3 AND user_email_id = $4 AND status = 'sending'
    `, [payload.action, payload.messageId ?? null, payload.key, saved.userEmailId]);
    if (result.rowCount !== 1) throw new Error("Could not update the reserved Preview send.");
  } else {
    throw new Error("Unknown Preview send recording action.");
  }
} catch (error) {
  if (payload.action === "reserve") await client.query("ROLLBACK");
  throw error;
} finally {
  client.release();
  await pool.end();
}

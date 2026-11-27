import { randomUUID } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
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
let transactionOpen = false;
try {
  if (payload.action === "reserve") {
    await client.query("BEGIN");
    transactionOpen = true;
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
    if (id) {
      for (const job of payload.jobs || []) {
        if (!job.publicId || !job.title || !/^\d{4}-\d{2}-\d{2}$/.test(job.reportDate || "")) {
          throw new Error("Preview recommendation job details are incomplete.");
        }
        await client.query(`
          INSERT INTO ontap_shadow.jobs
            (id, public_id, title, employer, location, region, salary_text,
             first_seen, last_seen, publication_status)
          VALUES ($1, $2, $3, $4, $5, $6, $7, $8::date, $8::date, 'published')
          ON CONFLICT (public_id) DO UPDATE SET
            title = EXCLUDED.title, employer = EXCLUDED.employer,
            location = EXCLUDED.location, region = EXCLUDED.region,
            salary_text = EXCLUDED.salary_text,
            last_seen = GREATEST(ontap_shadow.jobs.last_seen, EXCLUDED.last_seen),
            inactive_since = NULL, publication_status = 'published'
        `, [randomUUID(), job.publicId, job.title, job.employer || null,
          job.location || null, job.region || null, job.salaryText || null, job.reportDate]);
      }
    }
    for (const match of id ? payload.matches : []) {
      const reason = match.reason || "private_alert_match";
      let result;
      if (reason === "private_manual_addition") {
        result = await client.query(`
          INSERT INTO ontap_shadow.job_recommendations
            (id, email_id, subscriber_id, user_id, user_email_id, preference_id,
             signup_job_id, recommended_job_id, reason, matcher_revision, matching_evidence)
          SELECT $1, $2, $3, $4, $5, NULL, NULL, j.id, $6, $7,
                 jsonb_build_object('public_job_id', j.public_id, 'manual_selection', true)
          FROM ontap_shadow.jobs j
          WHERE j.public_id = $8
        `, [randomUUID(), id, saved.subscriberId, saved.userId, saved.userEmailId,
          reason, env.GITHUB_SHA, match.publicId]);
      } else if (reason === "private_alert_match") {
        result = await client.query(`
          INSERT INTO ontap_shadow.job_recommendations
            (id, email_id, subscriber_id, user_id, user_email_id, preference_id,
             signup_job_id, recommended_job_id, reason, matcher_revision, matching_evidence)
          SELECT $1, $2, p.subscriber_id, p.user_id, $3, p.id, signup_job.id, j.id,
                 $4, $5, jsonb_build_object('public_job_id', j.public_id)
          FROM ontap_shadow.subscriber_preferences p
          JOIN ontap_shadow.jobs j ON j.public_id = $8
          LEFT JOIN ontap_shadow.jobs signup_job ON signup_job.public_id = p.signup_job_public_id
          WHERE p.id = $6 AND p.subscriber_id = $7 AND p.user_id = $9 AND p.active
        `, [randomUUID(), id, saved.userEmailId, reason, env.GITHUB_SHA,
          match.preferenceId, saved.subscriberId, match.publicId, saved.userId]);
      } else {
        throw new Error("Unknown private recommendation reason.");
      }
      if (result.rowCount !== 1) throw new Error("A recommendation job or its saved preference is missing in Preview Neon.");
    }
    await client.query("COMMIT");
    transactionOpen = false;
    if (!id) console.log("already-sent");
  } else if (payload.action === "openWindow") {
    const result = await client.query(`
      INSERT INTO ontap_shadow.private_email_send_windows (report_date)
      SELECT $1::date
      WHERE EXISTS (
        SELECT 1 FROM ontap_shadow.user_emails e
        JOIN ontap_shadow.subscribers s ON s.user_email_id = e.id AND s.user_id = e.user_id
        WHERE e.id = $2 AND e.user_id = $3 AND e.email_key = $4
          AND e.alert_status = 'active' AND s.status = 'active'
          AND (SELECT c.action FROM ontap_shadow.consent_history c
               WHERE c.user_email_id = e.id AND c.purpose = 'cpc_job_alerts'
               ORDER BY c.occurred_at DESC, c.id DESC LIMIT 1) = 'granted'
      )
      ON CONFLICT (report_date) DO NOTHING RETURNING report_date
    `, [payload.reportDate, saved.userEmailId, saved.userId, saved.email]);
    if (result.rowCount !== 1) throw new Error("The Preview selection window already exists or the signup is inactive.");
    console.log("Opened the one-hour Preview manual-selection window.");
  } else if (payload.action === "stageManualSelections") {
    if (!Array.isArray(payload.publicIds) || payload.publicIds.length > 20 ||
        payload.publicIds.some(id => typeof id !== "string" || !/^[A-Za-z0-9_-]{1,100}$/.test(id))) {
      throw new Error("Manual selections must be up to 20 published CPC job IDs.");
    }
    await client.query("BEGIN");
    transactionOpen = true;
    const window = await client.query(`
      SELECT report_date FROM ontap_shadow.private_email_send_windows
      WHERE report_date = $1::date AND status = 'open'
        AND opened_at >= now() - interval '1 hour'
      FOR UPDATE
    `, [payload.reportDate]);
    if (window.rowCount !== 1) throw new Error("The one-hour Preview selection window is closed.");
    const uniquePublicIds = [...new Set(payload.publicIds)];
    const existing = await client.query(`
      SELECT public_job_id FROM ontap_shadow.private_email_manual_selections
      WHERE report_date = $1::date AND user_email_id = $2
    `, [payload.reportDate, saved.userEmailId]);
    const totalUnique = new Set([
      ...existing.rows.map(row => row.public_job_id),
      ...uniquePublicIds,
    ]);
    if (totalUnique.size > 20) {
      throw new Error("The one-hour window allows up to 20 distinct manual jobs in total.");
    }
    for (const publicId of uniquePublicIds) {
      const result = await client.query(`
        INSERT INTO ontap_shadow.private_email_manual_selections
          (report_date, user_email_id, public_job_id)
        SELECT $1::date, $2, $3
        WHERE EXISTS (
          SELECT 1 FROM ontap_shadow.user_emails e
          JOIN ontap_shadow.subscribers s ON s.user_email_id = e.id AND s.user_id = e.user_id
          WHERE e.id = $2 AND e.user_id = $4 AND e.email_key = $5
            AND e.alert_status = 'active' AND s.status = 'active'
            AND (SELECT c.action FROM ontap_shadow.consent_history c
                 WHERE c.user_email_id = e.id AND c.purpose = 'cpc_job_alerts'
                 ORDER BY c.occurred_at DESC, c.id DESC LIMIT 1) = 'granted'
        )
        ON CONFLICT (report_date, user_email_id, public_job_id) DO NOTHING
      `, [payload.reportDate, saved.userEmailId, publicId, saved.userId, saved.email]);
      if (result.rowCount !== 1 && result.rowCount !== 0) {
        throw new Error("Could not stage a Preview manual selection.");
      }
    }
    await client.query("COMMIT");
    transactionOpen = false;
    console.log("Manual Preview selections saved.");
  } else if (payload.action === "closeWindow") {
    if (!process.env.NEON_ALERT_MANUAL_SELECTION_OUTPUT) {
      throw new Error("A temporary output file is required for the Preview selections.");
    }
    await client.query("BEGIN");
    transactionOpen = true;
    const window = await client.query(`
      SELECT status, opened_at FROM ontap_shadow.private_email_send_windows
      WHERE report_date = $1::date FOR UPDATE
    `, [payload.reportDate]);
    if (window.rowCount !== 1) throw new Error("No Preview selection window exists for this report.");
    if (window.rows[0].status === "open") {
      const closed = await client.query(`
        UPDATE ontap_shadow.private_email_send_windows
        SET status = 'closed', closed_at = now()
        WHERE report_date = $1::date AND opened_at <= now() - interval '1 hour'
        RETURNING report_date
      `, [payload.reportDate]);
      if (closed.rowCount !== 1) throw new Error("The one-hour Preview selection window has not elapsed.");
    } else if (window.rows[0].status !== "closed") {
      throw new Error("The Preview selection window is already being sent or sent.");
    }
    const selected = await client.query(`
      SELECT public_job_id FROM ontap_shadow.private_email_manual_selections
      WHERE report_date = $1::date AND user_email_id = $2
      ORDER BY selected_at, public_job_id
    `, [payload.reportDate, saved.userEmailId]);
    await client.query("COMMIT");
    transactionOpen = false;
    await writeFile(process.env.NEON_ALERT_MANUAL_SELECTION_OUTPUT,
      JSON.stringify(selected.rows.map(row => row.public_job_id)), { mode: 0o600 });
    console.log("Closed the selection window; saved manual job count: " + selected.rowCount);
  } else if (payload.action === "sent" || payload.action === "uncertain") {
    const result = await client.query(`
      UPDATE ontap_shadow.emails_sent
      SET status = $1, provider_message_id = $2,
          sent_at = CASE WHEN $1 = 'sent' THEN now() END,
          error_code = CASE WHEN $1 = 'uncertain' THEN 'brevo_result_unconfirmed' END
      WHERE idempotency_key = $3 AND user_email_id = $4 AND status = 'sending'
    `, [payload.action, payload.messageId ?? null, payload.key, saved.userEmailId]);
    if (result.rowCount !== 1) throw new Error("Could not update the reserved Preview send.");
    if (payload.action === "sent" && payload.reportDate) {
      await client.query(`
        UPDATE ontap_shadow.private_email_send_windows
        SET status = 'sent', closed_at = COALESCE(closed_at, now())
        WHERE report_date = $1::date AND status = 'closed'
      `, [payload.reportDate]);
    }
  } else {
    throw new Error("Unknown Preview send recording action.");
  }
} catch (error) {
  if (transactionOpen) await client.query("ROLLBACK");
  throw error;
} finally {
  client.release();
  await pool.end();
}

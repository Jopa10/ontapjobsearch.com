import { createHash, createHmac } from "node:crypto";

export const PRIVATE_TEST_EMAIL = "jpbt801@gmail.com";
export const PRIVATE_TEST_EMAILS: readonly string[] = [PRIVATE_TEST_EMAIL, "jnabon1108@gmail.com"];
const TEST_BRANCH = "feat/cpc-job-alerts-brevo";

type Env = Record<string, string | undefined>;
type SampleJob = { job_id: string; title: string; location: string; source: string; apply_url: string };
type Dependencies = {
  env: Env;
  findJob: (id: string) => SampleJob | undefined;
  fetcher?: typeof fetch;
};

export function privateTestEnabled(env: Env): boolean {
  return env.VERCEL_ENV === "preview" &&
    env.VERCEL_GIT_COMMIT_REF === TEST_BRANCH &&
    env.CPC_JOB_ALERTS_ENABLED === "true" &&
    env.BREVO_JOB_ALERTS_LIST_ID === "3";
}

function escapeHtml(value: string): string {
  return value.replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]!);
}

export async function sendPrivatePreviewTest({ env, findJob, fetcher = fetch }: Dependencies): Promise<void> {
  if (!privateTestEnabled(env)) throw new Error("Private test is available only on the test Preview branch.");
  const apiKey = env.BREVO_API_KEY;
  const secret = env.JOB_ALERTS_UNSUBSCRIBE_SECRET;
  const sender = env.BREVO_SENDER_EMAIL;
  const host = env.VERCEL_URL;
  if (!apiKey || !secret || !sender || !host || !/^[a-z0-9-]+\.vercel\.app$/i.test(host)) {
    throw new Error("The Preview email settings are incomplete.");
  }
  const origin = "https://" + host;
  const api = async (path: string, init: RequestInit = {}) => fetcher("https://api.brevo.com/v3" + path, {
    ...init,
    headers: { "api-key": apiKey, "content-type": "application/json", accept: "application/json" },
    signal: AbortSignal.timeout(8_000),
    cache: "no-store",
  });
  const response = await api("/contacts/" + encodeURIComponent(PRIVATE_TEST_EMAIL));
  if (!response.ok) throw new Error("Could not read the test contact from Brevo.");
  const contact = await response.json();
  if (contact.email?.toLowerCase() !== PRIVATE_TEST_EMAIL || contact.emailBlacklisted ||
      !Array.isArray(contact.listIds) || !contact.listIds.includes(3) ||
      contact.listUnsubscribed?.includes(3) ||
      !contact.attributes?.ALERT_CONSENT_AT || !contact.attributes?.ALERT_CONSENT_VERSION) {
    throw new Error("The test address must have an active signup in the private test list.");
  }
  const attributes = contact.attributes;
  const job = findJob(String(attributes.ALERT_JOB_ID || ""));
  if (!job || job.source.trim().toLowerCase() !== "jobg8") {
    throw new Error("The signup job is missing from this Preview. Sign up again using a current JobG8 job.");
  }
  const destination = new URL(job.apply_url);
  if (destination.protocol !== "https:" || destination.hostname !== "www.jobg8.com" ||
      destination.pathname.toLowerCase() !== "/traffic.aspx") {
    throw new Error("The signup job is not an eligible JobG8 job.");
  }
  const payload = Buffer.from(JSON.stringify({ email: PRIVATE_TEST_EMAIL, version: 1 })).toString("base64url");
  const signature = createHmac("sha256", secret).update(payload, "ascii").digest("base64url");
  const unsubscribe = origin + "/job-alerts/unsubscribe?token=" + payload + "." + signature;
  const jobUrl = origin + "/jobs/" + encodeURIComponent(job.job_id);
  const role = String(attributes.ALERT_ROLE || job.title);
  const location = String(attributes.ALERT_LOCATION || job.location);
  const salary = String(attributes.ALERT_SALARY || "");
  const subject = "[Private test] Your Ontap job alert";
  const notice = "This is a private delivery test using the job you signed up from, not a newly matched vacancy.";
  // Brevo deduplicates matching UUID keys for 30 minutes; never retry POST automatically.
  const digest = createHash("sha256").update("ontap-private-test:" + PRIVATE_TEST_EMAIL + ":" + host).digest("hex");
  const idempotencyKey = digest.slice(0, 8) + "-" + digest.slice(8, 12) + "-4" + digest.slice(13, 16) +
    "-8" + digest.slice(17, 20) + "-" + digest.slice(20, 32);
  const sent = await api("/smtp/email", {
    method: "POST",
    body: JSON.stringify({
      sender: { name: "Ontap Jobs", email: sender },
      to: [{ email: PRIVATE_TEST_EMAIL }],
      subject,
      headers: { idempotencyKey },
      htmlContent: '<div style="max-width:620px;margin:auto;font:16px/1.5 Arial,sans-serif;color:#171717">' +
        "<h1>Your Ontap job alert — private test</h1><p>" + notice + "</p>" +
        "<p>Saved preferences: " + escapeHtml([role, location, salary].filter(Boolean).join(" · ")) + "</p>" +
        '<p><a href="' + escapeHtml(jobUrl) + '">' + escapeHtml(job.title) + "</a> — " + escapeHtml(job.location) + "</p>" +
        '<p style="font-size:12px">You asked for matching job alerts. <a href="' + escapeHtml(unsubscribe) + '">Unsubscribe</a></p></div>',
      textContent: notice + "\n\nSaved preferences: " + [role, location, salary].filter(Boolean).join(" · ") +
        "\n\n" + job.title + " — " + job.location + "\n" + jobUrl + "\n\nUnsubscribe: " + unsubscribe,
    }),
  });
  if (!sent.ok) {
    const result = await sent.json().catch(() => ({}));
    if (result.code === "duplicate_parameter") throw new Error("A test was already requested recently. Check your inbox and spam folder.");
    throw new Error("Brevo did not accept the test email. Check Transactional email logs in Brevo.");
  }
}

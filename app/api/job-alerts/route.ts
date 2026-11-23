import { NextRequest, NextResponse } from "next/server";
import { getPublishedJob } from "@/lib/published-jobs";
import { isCpcJobAlertEligible } from "@/lib/cpc-job-alerts";
import { AlertLimitError, activateBrevoJobAlertDelivery, PRIVATE_SIGNUP_TEST_EMAILS } from "@/lib/job-alert-signup";
import { privateTestEnabled } from "@/lib/private-job-alert-test";
import { isValidJobAlertConsent, JOB_ALERT_CONSENT_TEXT, JOB_ALERT_CONSENT_VERSION } from "@/lib/job-alert-consent";
import { AlertPreferenceLimitError, saveJobAlertSignupToNeon, activateJobAlertSignupInNeon } from "@/lib/neon-email-alerts";

export const runtime = "nodejs";

const MAX_BODY_BYTES = 8_000;

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value && typeof value === "object" && !Array.isArray(value));
}

function shortText(value: unknown, maxLength = 120): string {
  return typeof value === "string" ? value.trim().slice(0, maxLength) : "";
}

function signupDevice(userAgent: string | null): "mobile" | "laptop" | "unknown" {
  if (!userAgent) return "unknown";
  return /android|iphone|ipad|ipod|mobile|tablet/i.test(userAgent) ? "mobile" : "laptop";
}

export async function POST(request: NextRequest) {
  if (!privateTestEnabled(process.env)) {
    return NextResponse.json({ error: "Job alerts are not available just yet." }, { status: 503 });
  }
  const origin = request.headers.get("origin");
  if (!origin || origin !== new URL(request.url).origin) {
    return NextResponse.json({ error: "Request could not be verified." }, { status: 403 });
  }
  if (Number(request.headers.get("content-length") || 0) > MAX_BODY_BYTES) {
    return NextResponse.json({ error: "Request is too large." }, { status: 413 });
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Please check your details and try again." }, { status: 400 });
  }
  if (!isRecord(body)) {
    return NextResponse.json({ error: "Please check your details and try again." }, { status: 400 });
  }

  if (typeof body.website === "string" && body.website.trim()) {
    return NextResponse.json({ ok: true }, { status: 202 });
  }

  const email = shortText(body.email, 254).toLowerCase();
  const signupAttemptId = shortText(body.signupAttemptId, 36);
  if (!PRIVATE_SIGNUP_TEST_EMAILS.includes(email) || !isValidJobAlertConsent(body.consent, signupAttemptId)) {
    return NextResponse.json({ error: "Please confirm consent to job-alert emails and check your details." }, { status: 400 });
  }
  const jobId = shortText(body.jobId, 100);
  const role = shortText(body.role);
  const location = shortText(body.location);
  const salary = shortText(body.salary);

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !jobId || !role || !location) {
    return NextResponse.json({ error: "Enter a valid email, role and location." }, { status: 400 });
  }

  const job = getPublishedJob(jobId);
  if (!job || !isCpcJobAlertEligible(job.source, job.apply_url)) {
    return NextResponse.json({ error: "Alerts are not available for this job." }, { status: 400 });
  }

  const apiKey = process.env.BREVO_API_KEY;
  const listId = Number(process.env.BREVO_JOB_ALERTS_LIST_ID);
  if (!apiKey || !Number.isInteger(listId) || listId <= 0) {
    return NextResponse.json({ error: "Job alerts are not available just yet." }, { status: 503 });
  }

  try {
    const alert = { email, role, location, salary, region: body.includeRegion === true && job.region !== location ? job.region : "", jobId: job.job_id, source: job.source };
    const saved = await saveJobAlertSignupToNeon({
      ...alert, signupAttemptId, signupDevice: signupDevice(request.headers.get("user-agent")), consentText: JOB_ALERT_CONSENT_TEXT,
      consentVersion: JOB_ALERT_CONSENT_VERSION, consentSource: "apply_job_alert_signup",
    }, { env: process.env });
    const result = await activateBrevoJobAlertDelivery({ ...alert, signupAttemptId }, {
      env: process.env, alertCount: saved.alertCount, unchanged: saved.unchanged,
    });
    if (!result.subscriptionActive) throw new Error("Brevo did not confirm active delivery.");
    await activateJobAlertSignupInNeon(email, { env: process.env });
    if (!result.confirmationSent && !result.unchanged) {
      console.warn("Alert saved in Neon; signup confirmation is pending retry.");
    }
    return NextResponse.json({ ...result, neonSaved: true, userId: saved.userId });
  } catch (error) {
    if (error instanceof AlertLimitError || error instanceof AlertPreferenceLimitError) return NextResponse.json({ error: error.message }, { status: 409 });
    console.error("Preview job-alert signup or Neon write failed");
    return NextResponse.json({ error: "We couldn't save your alert just now. Please try again." }, { status: 502 });
  }
}

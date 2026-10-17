import { NextRequest, NextResponse } from "next/server";
import { getPublishedJob } from "@/lib/published-jobs";
import { isCpcJobAlertEligible } from "@/lib/cpc-job-alerts";

export const runtime = "nodejs";

const BREVO_CONTACTS_URL = "https://api.brevo.com/v3/contacts";
const CONSENT_VERSION = "cpc-job-alert-v1";
const MAX_BODY_BYTES = 8_000;

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value && typeof value === "object" && !Array.isArray(value));
}

function shortText(value: unknown, maxLength = 120): string {
  return typeof value === "string" ? value.trim().slice(0, maxLength) : "";
}

export async function POST(request: NextRequest) {
  if (process.env.CPC_JOB_ALERTS_ENABLED !== "true") {
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

  const attributes = {
    ALERT_ROLE: role,
    ALERT_LOCATION: location,
    ALERT_SALARY: salary,
    ALERT_JOB_ID: job.job_id,
    ALERT_SOURCE: job.source,
    ALERT_CONSENT_AT: new Date().toISOString(),
    ALERT_CONSENT_VERSION: CONSENT_VERSION,
  };

  try {
    const response = await fetch(BREVO_CONTACTS_URL, {
      method: "POST",
      headers: { "api-key": apiKey, "content-type": "application/json", accept: "application/json" },
      body: JSON.stringify({ email, attributes, listIds: [listId], updateEnabled: true }),
      signal: AbortSignal.timeout(8_000),
      cache: "no-store",
    });
    if (!response.ok) {
      console.error("Brevo job-alert contact upsert failed", response.status);
      return NextResponse.json({ error: "We couldn’t save your alert just now." }, { status: 502 });
    }
    return NextResponse.json({ ok: true });
  } catch (error) {
    console.error("Brevo job-alert request failed", error);
    return NextResponse.json({ error: "We couldn’t save your alert just now." }, { status: 502 });
  }
}

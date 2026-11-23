import { createHash, createHmac } from "node:crypto";
import { privateTestEnabled } from "./private-job-alert-test";
import { JOB_ALERT_CONSENT_VERSION } from "./job-alert-consent";

export const PRIVATE_SIGNUP_TEST_EMAILS: readonly string[] = ["jpbt801@gmail.com", "jnabon1108@gmail.com", "elbt801@gmail.com"];

type Env = Record<string, string | undefined>;
export type Preferences = { role: string; location: string; salary: string; region?: string };
type Signup = Preferences & { email: string; jobId: string; source: string };
type Contact = {
  email?: string; emailBlacklisted?: boolean; listIds?: number[]; listUnsubscribed?: number[];
  attributes?: Record<string, unknown>;
};
export const MAX_ALERTS = 10;
export const PREFERENCES_ATTRIBUTE = "ALERT_PREFERENCES";
export class AlertLimitError extends Error {}
function preferenceKey(value: Preferences): string {
  return JSON.stringify([value.role, value.location, value.salary].map(v => v.trim().replace(/\s+/g, " ").toLowerCase()));
}
export function savedAlerts(attrs: Record<string, unknown>): Preferences[] {
  const raw = attrs[PREFERENCES_ATTRIBUTE];
  if (raw !== undefined && raw !== null && raw !== "") {
    let parsed: unknown;
    try { parsed = JSON.parse(String(raw)); } catch { throw new Error("Saved alerts are unreadable."); }
    if (!Array.isArray(parsed) || parsed.length > MAX_ALERTS ||
        parsed.some(p => !p || typeof p.role !== "string" || !p.role.trim() ||
          typeof p.location !== "string" || !p.location.trim() || typeof p.salary !== "string" || (p.region !== undefined && typeof p.region !== "string"))) {
      throw new Error("Saved alerts are invalid.");
    }
    return parsed.map(p => ({ role: p.role, location: p.location, salary: p.salary, ...(typeof p.region === "string" && p.region.trim() ? { region: p.region.trim() } : {}) }));
  }
  return attrs.ALERT_ROLE && attrs.ALERT_LOCATION ? [{
    role: String(attrs.ALERT_ROLE), location: String(attrs.ALERT_LOCATION), salary: String(attrs.ALERT_SALARY || ""), ...(attrs.ALERT_REGION ? { region: String(attrs.ALERT_REGION) } : {}),
  }] : [];
}
const STATE = "ALERT_CONFIRMATION_STATE";
const API = "https://api.brevo.com/v3";
const VERSION = JOB_ALERT_CONSENT_VERSION;

function escapeHtml(value: string): string {
  return value.replace(/[&<>"']/g, character => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[character]!);
}

function uuid(value: string): string {
  const hex = createHash("sha256").update(value).digest("hex");
  return hex.slice(0, 8) + "-" + hex.slice(8, 12) + "-4" + hex.slice(13, 16) +
    "-8" + hex.slice(17, 20) + "-" + hex.slice(20, 32);
}

export function confirmationContent(preferences: Preferences, unsubscribe: string, updated: boolean) {
  const subject = updated ? "Your Ontap job alert is updated" : "Your Ontap job alert is saved";
  const details = [
    ["Role", preferences.role], ["Location", preferences.region ? preferences.location + " + " + preferences.region : preferences.location],
    ["Salary", preferences.salary || "No salary filter"],
  ];
  const explanation = "We'll email you when new matching jobs are published. No new matches means no email. You can save up to 10 alerts using this email. Each different signup adds an alert; identical preferences are saved only once. Matches are combined into one daily email, with duplicate jobs removed. Unsubscribe stops all your alerts.";
  return {
    subject,
    textContent: subject + "\n\n" + details.map(([name, value]) => name + ": " + value).join("\n") +
      "\n\n" + explanation + "\n\nUnsubscribe: " + unsubscribe,
    htmlContent: '<div style="max-width:620px;margin:auto;font:16px/1.5 Arial,sans-serif;color:#171717">' +
      "<h1 style='font-size:22px'>" + subject + "</h1><p>Your saved preferences:</p><ul>" +
      details.map(([name, value]) => "<li><strong>" + name + ":</strong> " + escapeHtml(value) + "</li>").join("") +
      "</ul><p>" + explanation + '</p><p style="font-size:12px"><a href="' +
      escapeHtml(unsubscribe) + '">Unsubscribe from Ontap job alerts</a></p></div>',
  };
}

/** Save preferences, then confirm once. Confirmation failure never discards signup. */
export async function saveJobAlert(
  signup: Signup,
  { env, fetcher = fetch, now = () => new Date() }:
  { env: Env; fetcher?: typeof fetch; now?: () => Date },
): Promise<{ ok: true; confirmationSent: boolean; subscriptionActive: boolean; unchanged: boolean; alertCount: number }> {
  // Public signup remains explicitly gated; Preview remains restricted to the approved private testers.
  const production = env.VERCEL_ENV === "production";
  if (production ? env.CPC_JOB_ALERTS_LIVE_ENABLED !== "true" :
      (!privateTestEnabled(env) || !PRIVATE_SIGNUP_TEST_EMAILS.includes(signup.email.trim().toLowerCase()))) {
    throw new Error("Job-alert signup is not enabled for this environment.");
  }
  const key = env.BREVO_API_KEY;
  const secret = env.JOB_ALERTS_UNSUBSCRIBE_SECRET;
  const sender = env.BREVO_SENDER_EMAIL;
  const listId = Number(env.BREVO_JOB_ALERTS_LIST_ID);
  if (!key || !secret || !sender) throw new Error("Job-alert email settings are incomplete.");
  const host = env.VERCEL_URL;
  if (!host || !/^[a-z0-9-]+\.vercel\.app$/i.test(host)) throw new Error("Invalid Preview origin.");
  const origin = "https://" + host;
  const email = signup.email.trim().toLowerCase();
  const call = (path: string, init: RequestInit = {}) => fetcher(API + path, {
    ...init, headers: { "api-key": key, "content-type": "application/json", accept: "application/json" },
    signal: AbortSignal.timeout(8_000), cache: "no-store",
  });
  const read = await call("/contacts/" + encodeURIComponent(email));
  if (!read.ok && read.status !== 404) throw new Error("Could not check the saved alert.");
  const previous: Contact = read.ok ? await read.json() : {};
  const attrs = previous.attributes || {};
  if (previous.email && previous.email.toLowerCase() !== email) throw new Error("Contact identity mismatch.");
  // Do not silently override Brevo's global blacklist.
  if (previous.emailBlacklisted) throw new Error("This address is blocked from email. Check its Brevo status.");
  const active = previous.listIds?.includes(listId) && !previous.listUnsubscribed?.includes(listId) &&
    Boolean(attrs.ALERT_CONSENT_AT && attrs.ALERT_CONSENT_VERSION);
  const previousAlerts = savedAlerts(attrs);
  const existingIndex = previousAlerts.findIndex(p => preferenceKey(p) === preferenceKey(signup));
  const exists = existingIndex >= 0;
  const same = Boolean(active && exists && (previousAlerts[existingIndex]?.region || "") === (signup.region || ""));
  if (!exists && previousAlerts.length >= MAX_ALERTS) {
    throw new AlertLimitError("You already have 10 saved alerts. Your existing alerts have been kept.");
  }
  const alerts = exists
    ? previousAlerts.map((p, index) => {
        if (index !== existingIndex) return p;
        const { region: _oldRegion, ...withoutRegion } = p;
        return signup.region ? { ...withoutRegion, region: signup.region } : withoutRegion;
      })
    : [...previousAlerts, { role: signup.role, location: signup.location, salary: signup.salary, ...(signup.region ? { region: signup.region } : {}) }];
  const encodedAlerts = JSON.stringify(alerts);
  const alertCount = alerts.length;
  const state = String(attrs[STATE] || "");
  if (same && /^sent:[a-f0-9-]{36}$/.test(state)) {
    return { ok: true, confirmationSent: false, subscriptionActive: true, unchanged: true, alertCount };
  }
  const pending = same && /^pending-(?:saved|updated):[a-f0-9-]{36}$/.test(state);
  const confirmationKey = pending ? state.split(":")[1] : uuid(JSON.stringify([
    "ontap-signup-confirmation-v1", email, signup.role, signup.location, signup.salary, state,
  ]));
  const updated = pending ? state.startsWith("pending-updated:") : Boolean(active && !same);
  const pendingState = (updated ? "pending-updated:" : "pending-saved:") + confirmationKey;
  const attributes = {
    [PREFERENCES_ATTRIBUTE]: encodedAlerts,
    ALERT_ROLE: signup.role, ALERT_LOCATION: signup.location, ALERT_SALARY: signup.salary,
    ...(signup.region ? { ALERT_REGION: signup.region } : {}),
    ALERT_JOB_ID: signup.jobId, ALERT_SOURCE: signup.source,
    ALERT_CONSENT_AT: same ? attrs.ALERT_CONSENT_AT : now().toISOString(),
    ALERT_CONSENT_VERSION: VERSION,
    [STATE]: pendingState,
  };
  const saved = await call("/contacts", {
    method: "POST", body: JSON.stringify({ email, attributes, listIds: [listId], updateEnabled: true }),
  });
  if (!saved.ok) throw new Error("We couldn't save your alert just now.");
  // Provider must persist the marker before any send, otherwise fail closed.
  const verified = await call("/contacts/" + encodeURIComponent(email));
  const contact: Contact = verified.ok ? await verified.json() : {};
  if (contact.attributes?.[PREFERENCES_ATTRIBUTE] !== encodedAlerts) {
    throw new Error("Your alerts could not be verified after saving. Please try again.");
  }
  if (contact.attributes?.[STATE] !== pendingState || contact.email?.toLowerCase() !== email ||
      contact.emailBlacklisted || !contact.listIds?.includes(listId) || contact.listUnsubscribed?.includes(listId) ||
      contact.attributes?.ALERT_ROLE !== signup.role || contact.attributes?.ALERT_LOCATION !== signup.location ||
      String(contact.attributes?.ALERT_SALARY || "") !== signup.salary ||
      (signup.region ? contact.attributes?.ALERT_REGION !== signup.region : false)) {
    return { ok: true, confirmationSent: false, subscriptionActive: false, unchanged: same, alertCount };
  }
  const payload = Buffer.from(JSON.stringify({ email, version: 1 })).toString("base64url");
  const signature = createHmac("sha256", secret).update(payload, "ascii").digest("base64url");
  const unsubscribe = origin + "/job-alerts/unsubscribe?token=" + payload + "." + signature;
  const content = confirmationContent(signup, unsubscribe, updated);
  try {
    const sent = await call("/smtp/email", {
      method: "POST", body: JSON.stringify({
        sender: { name: "Ontap Jobs", email: sender }, to: [{ email }],
        ...content, headers: { idempotencyKey: confirmationKey },
      }),
    });
    let accepted = sent.ok;
    if (!accepted) {
      const error = await sent.json().catch(() => ({}));
      // A retry after an accepted send can return Brevo's duplicate-key response.
      accepted = error.code === "duplicate_parameter";
    }
    if (!accepted) return { ok: true, confirmationSent: false, subscriptionActive: true, unchanged: same, alertCount };
    await call("/contacts/" + encodeURIComponent(email), {
      method: "PUT", body: JSON.stringify({ attributes: { [STATE]: "sent:" + confirmationKey } }),
    });
    return { ok: true, confirmationSent: true, subscriptionActive: true, unchanged: same, alertCount };
  } catch {
    // Pending marker permits a later retry with the same idempotency key.
    return { ok: true, confirmationSent: false, subscriptionActive: true, unchanged: same, alertCount };
  }
}

/**
 * Add the explicitly consented address to Brevo for delivery, then send its
 * confirmation. Preference criteria and consent are canonical in Preview Neon;
 * this function never reads or writes those values in Brevo.
 */
export async function activateBrevoJobAlertDelivery(
  signup: Signup & { signupAttemptId: string },
  { env, alertCount, unchanged, fetcher = fetch, now = () => new Date() }:
  { env: Env; alertCount: number; unchanged: boolean; fetcher?: typeof fetch; now?: () => Date },
): Promise<{ ok: true; confirmationSent: boolean; subscriptionActive: boolean; unchanged: boolean; alertCount: number }> {
  if (env.VERCEL_ENV !== "preview" || !privateTestEnabled(env) ||
      !PRIVATE_SIGNUP_TEST_EMAILS.includes(signup.email.trim().toLowerCase())) {
    throw new Error("Brevo alert delivery is restricted to the private Preview signup.");
  }
  const key = env.BREVO_API_KEY;
  const secret = env.JOB_ALERTS_UNSUBSCRIBE_SECRET;
  const sender = env.BREVO_SENDER_EMAIL;
  const listId = Number(env.BREVO_JOB_ALERTS_LIST_ID);
  const host = env.VERCEL_URL;
  if (!key || !secret || !sender || listId !== 3 || !host || !/^[a-z0-9-]+\.vercel\.app$/i.test(host)) {
    throw new Error("Private Preview email settings are incomplete.");
  }
  const email = signup.email.trim().toLowerCase();
  const origin = "https://" + host;
  const call = (path: string, init: RequestInit = {}) => fetcher(API + path, {
    ...init, headers: { "api-key": key, "content-type": "application/json", accept: "application/json" },
    signal: AbortSignal.timeout(8_000), cache: "no-store",
  });
  const read = await call("/contacts/" + encodeURIComponent(email));
  if (!read.ok && read.status !== 404) throw new Error("Could not check Brevo delivery status.");
  const previous: Contact = read.ok ? await read.json() : {};
  if (previous.email && previous.email.toLowerCase() !== email) throw new Error("Contact identity mismatch.");
  if (previous.emailBlacklisted) throw new Error("This address is blocked from email. Check its Brevo status.");

  const attrs = previous.attributes || {};
  const active = previous.listIds?.includes(listId) && !previous.listUnsubscribed?.includes(listId);
  const state = String(attrs[STATE] || "");
  if (unchanged && active && /^sent:[a-f0-9-]{36}$/.test(state)) {
    return { ok: true, confirmationSent: false, subscriptionActive: true, unchanged: true, alertCount };
  }
  const retryPending = unchanged && active && /^pending-(?:saved|updated):[a-f0-9-]{36}$/.test(state);
  const confirmationKey = retryPending ? state.split(":")[1] :
    uuid(JSON.stringify(["ontap-signup-confirmation-v2", email, signup.signupAttemptId]));
  const pendingState = retryPending ? state :
    (active && !unchanged ? "pending-updated:" : "pending-saved:") + confirmationKey;
  const saved = await call("/contacts", {
    method: "POST",
    body: JSON.stringify({ email, listIds: [listId], updateEnabled: true, attributes: { [STATE]: pendingState } }),
  });
  if (!saved.ok) throw new Error("Brevo could not activate delivery for this address.");
  const verified = await call("/contacts/" + encodeURIComponent(email));
  const contact: Contact = verified.ok ? await verified.json() : {};
  if (contact.email?.toLowerCase() !== email || contact.emailBlacklisted ||
      !contact.listIds?.includes(listId) || contact.listUnsubscribed?.includes(listId) ||
      contact.attributes?.[STATE] !== pendingState) {
    return { ok: true, confirmationSent: false, subscriptionActive: false, unchanged, alertCount };
  }

  const tokenPayload = Buffer.from(JSON.stringify({ email, version: 1 })).toString("base64url");
  const signature = createHmac("sha256", secret).update(tokenPayload, "ascii").digest("base64url");
  const unsubscribe = origin + "/job-alerts/unsubscribe?token=" + tokenPayload + "." + signature;
  const content = confirmationContent(signup, unsubscribe, active && !unchanged);
  try {
    const sent = await call("/smtp/email", {
      method: "POST", body: JSON.stringify({
        sender: { name: "Ontap Jobs", email: sender }, to: [{ email }],
        ...content, headers: { idempotencyKey: confirmationKey },
      }),
    });
    let accepted = sent.ok;
    if (!accepted) {
      const error = await sent.json().catch(() => ({}));
      accepted = error.code === "duplicate_parameter";
    }
    if (!accepted) return { ok: true, confirmationSent: false, subscriptionActive: true, unchanged, alertCount };
    await call("/contacts/" + encodeURIComponent(email), {
      method: "PUT", body: JSON.stringify({ attributes: { [STATE]: "sent:" + confirmationKey } }),
    });
    return { ok: true, confirmationSent: true, subscriptionActive: true, unchanged, alertCount };
  } catch {
    return { ok: true, confirmationSent: false, subscriptionActive: true, unchanged, alertCount };
  }
}

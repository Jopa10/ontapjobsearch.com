export const JOB_ALERT_CONSENT_VERSION = "cpc-alert-consent-2026-11-18-v1";
export const JOB_ALERT_CONSENT_TEXT =
  "Send me daily Ontap job-alert emails for these preferences; I can unsubscribe at any time.";

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export function isValidJobAlertConsent(consent: unknown, signupAttemptId: unknown): boolean {
  return consent === true && typeof signupAttemptId === "string" && UUID.test(signupAttemptId);
}

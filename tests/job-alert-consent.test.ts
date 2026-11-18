import assert from "node:assert/strict";
import test from "node:test";
import { isValidJobAlertConsent, JOB_ALERT_CONSENT_TEXT, JOB_ALERT_CONSENT_VERSION } from "../lib/job-alert-consent";

test("consent is required and tied to a valid signup attempt", () => {
  assert.equal(isValidJobAlertConsent(false, "1b7d1d7e-47fb-4a72-9c88-9a06df9d4c2b"), false);
  assert.equal(isValidJobAlertConsent(true, ""), false);
  assert.equal(isValidJobAlertConsent(true, "not-a-uuid"), false);
  assert.equal(isValidJobAlertConsent(true, "1b7d1d7e-47fb-4a72-9c88-9a06df9d4c2b"), true);
  assert.equal(JOB_ALERT_CONSENT_TEXT, "Send me daily Ontap job-alert emails for these preferences; I can unsubscribe at any time.");
  assert.match(JOB_ALERT_CONSENT_VERSION, /^cpc-alert-consent-/);
});

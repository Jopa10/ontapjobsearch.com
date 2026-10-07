import assert from "node:assert/strict";
import test from "node:test";
import { buildSessionReferralParameters, initializeSessionReferral, sessionReferralForApplyClick } from "../lib/session-referral";

function memoryStorage() {
  const values = new Map<string, string>();
  return { getItem: (key: string) => values.get(key) ?? null, setItem: (key: string, value: string) => values.set(key, value) };
}

test("captures hostname and UTM source without retaining the referrer URL", () => {
  assert.deepEqual(buildSessionReferralParameters("https://www.chatgpt.com/c/private", "?utm_source=ChatGPT"), {
    entry_referrer_host: "chatgpt.com", entry_utm_source: "ChatGPT", entry_source_type: "chatgpt",
  });
});

test("keeps the referral for an active session and resets it after the timeout", () => {
  const storage = memoryStorage();
  initializeSessionReferral(storage, "https://chatgpt.com/", "", 1000);
  assert.equal(sessionReferralForApplyClick(storage, "", "", 2000).entry_referrer_host, "chatgpt.com");
  assert.equal(initializeSessionReferral(storage, "", "", 31 * 60 * 1000).entry_referrer_host, "(direct)");
});

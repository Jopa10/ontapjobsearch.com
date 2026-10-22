import assert from "node:assert/strict";
import { createHmac } from "node:crypto";
import test from "node:test";
import { privateTestEnabled, sendPrivatePreviewTest, PRIVATE_TEST_EMAIL } from "../lib/private-job-alert-test";

const env = {
  VERCEL_ENV: "preview",
  VERCEL_GIT_COMMIT_REF: "feat/cpc-job-alerts-brevo",
  VERCEL_URL: "ontap-test.vercel.app",
  CPC_JOB_ALERTS_ENABLED: "true",
  BREVO_JOB_ALERTS_LIST_ID: "3",
  BREVO_API_KEY: "fake-key",
  JOB_ALERTS_UNSUBSCRIBE_SECRET: "fake-secret",
  BREVO_SENDER_EMAIL: "jobs@ontapjobsearch.com",
};
const contact = {
  email: PRIVATE_TEST_EMAIL, listIds: [3], emailBlacklisted: false,
  attributes: { ALERT_JOB_ID: "123", ALERT_ROLE: "HR Officer", ALERT_LOCATION: "Warwick",
    ALERT_SALARY: "£38000 - £40000 per year", ALERT_CONSENT_AT: "2026-10-22", ALERT_CONSENT_VERSION: "v1" },
};
const job = { job_id: "123", title: "HR Officer <sample>", location: "Warwick",
  source: "JobG8", apply_url: "https://www.jobg8.com/Traffic.aspx?x" };

test("production, other branches and lists cannot send or call Brevo", async () => {
  for (const overrides of [{ VERCEL_ENV: "production" }, { VERCEL_ENV: "development" },
    { VERCEL_GIT_COMMIT_REF: "main" }, { BREVO_JOB_ALERTS_LIST_ID: "2" }, { CPC_JOB_ALERTS_ENABLED: "false" }]) {
    const settings = { ...env, ...overrides };
    assert.equal(privateTestEnabled(settings), false);
    await assert.rejects(sendPrivatePreviewTest({ env: settings, findJob: () => job,
      fetcher: async () => { throw new Error("Must not reach Brevo"); } }), /Preview branch/);
  }
});

test("only the fixed opted-in contact is read and emailed, with valid Preview unsubscribe", async () => {
  const calls: { url: string; init?: RequestInit }[] = [];
  const fetcher: typeof fetch = async (input, init) => {
    calls.push({ url: String(input), init });
    return Response.json(calls.length === 1 ? contact : { messageId: "test-id" });
  };
  await sendPrivatePreviewTest({ env, findJob: () => job, fetcher });
  assert.equal(calls.length, 2);
  assert.equal(calls[0].url, "https://api.brevo.com/v3/contacts/jpbt801%40gmail.com");
  assert.equal(calls[1].url, "https://api.brevo.com/v3/smtp/email");
  const body = JSON.parse(String(calls[1].init?.body));
  assert.deepEqual(body.to, [{ email: PRIVATE_TEST_EMAIL }]);
  assert.match(body.subject, /Private test/);
  assert.match(body.htmlContent, /HR Officer &lt;sample&gt;/);
  assert.match(body.textContent, /https:\/\/ontap-test.vercel.app\/jobs\/123/);
  assert.doesNotMatch(body.textContent, /www\.ontapjobsearch\.com/);
  assert.match(body.headers.idempotencyKey, /^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-8[a-f0-9]{3}-[a-f0-9]{12}$/);
  const url = new URL(body.textContent.split("Unsubscribe: ")[1]);
  const [payload, signature] = url.searchParams.get("token")!.split(".");
  assert.equal(createHmac("sha256", env.JOB_ALERTS_UNSUBSCRIBE_SECRET).update(payload, "ascii").digest("base64url"), signature);
  assert.deepEqual(JSON.parse(Buffer.from(payload, "base64url").toString()), { email: PRIVATE_TEST_EMAIL, version: 1 });
});

test("nonmembers, unsubscribed, blocklisted and contacts without consent never receive a POST", async () => {
  for (const invalid of [{ ...contact, listIds: [2] }, { ...contact, listUnsubscribed: [3] },
    { ...contact, emailBlacklisted: true }, { ...contact, email: "other@example.com" },
    { ...contact, attributes: {} }]) {
    let count = 0;
    await assert.rejects(sendPrivatePreviewTest({ env, findJob: () => job,
      fetcher: async () => { count++; return Response.json(invalid); } }), /active signup/);
    assert.equal(count, 1);
  }
});

test("missing and non-CPC signup jobs fail before sending", async () => {
  for (const candidate of [undefined, { ...job, apply_url: "https://example.com/apply" }]) {
    let count = 0;
    await assert.rejects(sendPrivatePreviewTest({ env, findJob: () => candidate,
      fetcher: async () => { count++; return Response.json(contact); } }), /signup job/);
    assert.equal(count, 1);
  }
});

test("Brevo send failures are not retried", async () => {
  let count = 0;
  await assert.rejects(sendPrivatePreviewTest({ env, findJob: () => job,
    fetcher: async () => { count++; return count === 1 ? Response.json(contact) : Response.json({}, { status: 500 }); } }),
    /did not accept/);
  assert.equal(count, 2);
});

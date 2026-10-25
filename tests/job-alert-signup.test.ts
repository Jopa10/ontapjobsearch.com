import assert from "node:assert/strict";
import { createHmac } from "node:crypto";
import test from "node:test";
import { confirmationContent, saveJobAlert } from "../lib/job-alert-signup";

const env = {
  VERCEL_ENV: "preview", VERCEL_GIT_COMMIT_REF: "feat/cpc-job-alerts-brevo",
  VERCEL_URL: "ontap-test.vercel.app", CPC_JOB_ALERTS_ENABLED: "true",
  BREVO_JOB_ALERTS_LIST_ID: "3", BREVO_API_KEY: "fake",
  JOB_ALERTS_UNSUBSCRIBE_SECRET: "fake", BREVO_SENDER_EMAIL: "jobs@ontapjobsearch.com",
};
const signup = {
  email: "jpbt801@gmail.com", role: "Accounts Assistant", location: "London", salary: "£27000 - £30000 per year",
  jobId: "2074737", source: "JobG8",
};
type Contact = { email: string; listIds: number[]; listUnsubscribed?: number[]; emailBlacklisted?: boolean;
  attributes: Record<string, unknown> };
const existing = (): Contact => ({
  email: signup.email, listIds: [3], attributes: {
    ALERT_ROLE: signup.role, ALERT_LOCATION: signup.location, ALERT_SALARY: signup.salary,
    ALERT_JOB_ID: signup.jobId, ALERT_CONSENT_AT: "2026-10-25T10:00:00.000Z", ALERT_CONSENT_VERSION: "v1",
    ALERT_LAST_SENT_DATE: "2026-10-24",
  },
});
function fake(initial: Contact | undefined, failure = "") {
  let contact = initial ? structuredClone(initial) : undefined;
  const calls: { url: string; method: string; body: any }[] = [];
  const fetcher: typeof fetch = async (input, init) => {
    const url = String(input);
    const method = init?.method || "GET";
    const body = init?.body ? JSON.parse(String(init.body)) : undefined;
    calls.push({ url, method, body });
    if (url.endsWith("/smtp/email")) {
      if (failure === "throw") throw new Error("timeout");
      if (failure === "send") return Response.json({}, { status: 500 });
      return Response.json({ messageId: "fake-id" });
    }
    if (method === "GET") return contact ? Response.json(contact) : Response.json({}, { status: 404 });
    if (method === "POST" && failure === "save") return Response.json({}, { status: 500 });
    if (method === "POST") {
      contact = { email: body.email, listIds: body.listIds, attributes: { ...contact?.attributes, ...body.attributes } };
      if (failure === "marker") delete contact.attributes.ALERT_CONFIRMATION_STATE;
      return Response.json({}, { status: 201 });
    }
    if (method === "PUT") {
      if (contact) Object.assign(contact.attributes, body.attributes);
      return Response.json({});
    }
    throw new Error("Unexpected request");
  };
  return { fetcher, calls, get contact() { return contact; } };
}

test("first signup sends a saved confirmation only after preferences and marker persist", async () => {
  const f = fake(undefined);
  const result = await saveJobAlert(signup, { env, fetcher: f.fetcher });
  assert.equal(result.confirmationSent, true);
  assert.deepEqual(f.calls.map(c => c.method), ["GET", "POST", "GET", "POST", "PUT"]);
  const sent = f.calls.find(c => c.url.endsWith("/smtp/email"))!.body;
  assert.equal(sent.subject, "Your Ontap job alert is saved");
  assert.deepEqual(sent.to, [{ email: signup.email }]);
  assert.match(sent.textContent, /Accounts Assistant/);
  assert.match(sent.textContent, /London/);
  assert.match(sent.textContent, /£27000/);
  assert.match(sent.textContent, /No new matches means no email/);
  const unsubscribe = new URL(sent.textContent.split("Unsubscribe: ")[1]);
  const [payload, signature] = unsubscribe.searchParams.get("token")!.split(".");
  assert.equal(createHmac("sha256", "fake").update(payload, "ascii").digest("base64url"), signature);
  assert.equal(unsubscribe.origin, "https://ontap-test.vercel.app");
  assert.match(String(f.contact?.attributes.ALERT_CONFIRMATION_STATE), /^sent:/);
});

test("existing signup without a marker can use the same job and address for its first confirmation", async () => {
  const f = fake(existing());
  assert.equal((await saveJobAlert(signup, { env, fetcher: f.fetcher })).confirmationSent, true);
  assert.equal(f.calls.find(c => c.url.endsWith("/smtp/email"))!.body.subject, "Your Ontap job alert is saved");
  assert.equal(f.contact?.attributes.ALERT_LAST_SENT_DATE, "2026-10-24");
});

test("identical repeat signup sends no email and makes no writes", async () => {
  const f = fake(existing());
  await saveJobAlert(signup, { env, fetcher: f.fetcher });
  const before = f.calls.length;
  const result = await saveJobAlert(signup, { env, fetcher: f.fetcher });
  assert.equal(result.unchanged, true);
  assert.equal(result.confirmationSent, false);
  assert.deepEqual(f.calls.slice(before).map(c => c.method), ["GET"]);
});

test("changed preferences send an updated confirmation with a different key", async () => {
  const f = fake(existing());
  await saveJobAlert(signup, { env, fetcher: f.fetcher });
  await saveJobAlert({ ...signup, salary: "" }, { env, fetcher: f.fetcher });
  const mails = f.calls.filter(c => c.url.endsWith("/smtp/email"));
  assert.equal(mails.length, 2);
  assert.equal(mails[1].body.subject, "Your Ontap job alert is updated");
  assert.match(mails[1].body.textContent, /No salary filter/);
  assert.notEqual(mails[1].body.headers.idempotencyKey, mails[0].body.headers.idempotencyKey);
  assert.equal(f.contact?.attributes.ALERT_LAST_SENT_DATE, "2026-10-24");
});

test("failed email preserves signup and pending marker; retry uses the same key", async () => {
  const failed = fake(existing(), "send");
  const result = await saveJobAlert({ ...signup, salary: "" }, { env, fetcher: failed.fetcher });
  assert.equal(result.ok, true);
  assert.equal(result.confirmationSent, false);
  assert.match(String(failed.contact?.attributes.ALERT_CONFIRMATION_STATE), /^pending-updated:/);
  const retry = fake(failed.contact);
  await saveJobAlert({ ...signup, salary: "" }, { env, fetcher: retry.fetcher });
  const first = failed.calls.find(c => c.url.endsWith("/smtp/email"))!.body;
  const second = retry.calls.find(c => c.url.endsWith("/smtp/email"))!.body;
  assert.equal(first.headers.idempotencyKey, second.headers.idempotencyKey);
  assert.equal(second.subject, "Your Ontap job alert is updated");
});

test("save failure or missing provider marker never sends mail", async () => {
  for (const failure of ["save", "marker"]) {
    const f = fake(existing(), failure);
    if (failure === "save") await assert.rejects(saveJobAlert(signup, { env, fetcher: f.fetcher }));
    else assert.equal((await saveJobAlert(signup, { env, fetcher: f.fetcher })).confirmationSent, false);
    assert.equal(f.calls.filter(c => c.url.endsWith("/smtp/email")).length, 0);
  }
});

test("production, wrong branch, wrong list and other email addresses fail before API", async () => {
  for (const overrides of [{ VERCEL_ENV: "production" }, { VERCEL_GIT_COMMIT_REF: "main" },
    { BREVO_JOB_ALERTS_LIST_ID: "2" }, { CPC_JOB_ALERTS_ENABLED: "false" }]) {
    const f = fake(existing());
    await assert.rejects(saveJobAlert(signup, { env: { ...env, ...overrides }, fetcher: f.fetcher }));
    assert.equal(f.calls.length, 0);
  }
  const f = fake(existing());
  await assert.rejects(saveJobAlert({ ...signup, email: "other@example.com" }, { env, fetcher: f.fetcher }));
  assert.equal(f.calls.length, 0);
});

test("globally blocked addresses are not silently reactivated", async () => {
  const f = fake({ ...existing(), emailBlacklisted: true });
  await assert.rejects(saveJobAlert(signup, { env, fetcher: f.fetcher }));
  assert.equal(f.calls.length, 1);
});

test("email content escapes user input and clearly labels an absent salary preference", () => {
  const content = confirmationContent({ role: "<script>", location: "A&B", salary: "" }, "https://example.com/?a=1&b=2", false);
  assert.match(content.htmlContent, /&lt;script&gt;/);
  assert.match(content.htmlContent, /A&amp;B/);
  assert.match(content.htmlContent, /No salary filter/);
  assert.doesNotMatch(content.htmlContent, /<script>/);
});

import test from "node:test";
import assert from "node:assert/strict";
import {
  ANALYTICS_READY_EVENT,
  daysBetween,
  hasCampaignParameters,
  isLikelyAutomation,
  pageContext,
} from "../lib/analytics-client";

test("exposes a stable analytics-ready event for early client events", () => {
  assert.equal(ANALYTICS_READY_EVENT, "ontap:analytics-ready");
});

test("suppresses only explicit crawler or automation user agents", () => {
  assert.equal(isLikelyAutomation("Mozilla/5.0 Chrome/140 Safari/537.36"), false);
  assert.equal(isLikelyAutomation("Mozilla/5.0 Chrome/140", true), false);
  assert.equal(isLikelyAutomation("Mozilla/5.0 HeadlessChrome/140"), true);
  assert.equal(isLikelyAutomation("Googlebot/2.1"), true);
  assert.equal(isLikelyAutomation("Mozilla/5.0 (compatible; Bingbot/2.0)"), true);
  assert.equal(isLikelyAutomation("Mozilla/5.0 crawler-like-browser"), false);
});

test("recognises campaign parameters without treating ordinary queries as campaigns", () => {
  assert.equal(hasCampaignParameters("?utm_source=linkedin&utm_medium=organic_social"), true);
  assert.equal(hasCampaignParameters("?gclid=abc123"), true);
  assert.equal(hasCampaignParameters("?near=Newcastle"), false);
});

test("uses non-identifying page contexts and elapsed whole days", () => {
  assert.equal(pageContext("/jobs/123"), "job_detail");
  assert.equal(pageContext("/north-east/service-administrator-jobs"), "listing");
  assert.equal(pageContext("/"), "site");
  assert.equal(daysBetween(1_000, 1_000 + (2.9 * 86_400_000)), 2);
});

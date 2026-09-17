import test from "node:test";
import assert from "node:assert/strict";
import {
  daysBetween,
  hasCampaignParameters,
  isLikelyAutomation,
  pageContext,
} from "../lib/analytics-client";

test("suppresses explicit browser automation and crawler analytics only", () => {
  assert.equal(isLikelyAutomation("Mozilla/5.0 Chrome/140 Safari/537.36", false), false);
  assert.equal(isLikelyAutomation("Mozilla/5.0 HeadlessChrome/140", false), true);
  assert.equal(isLikelyAutomation("Googlebot/2.1", false), true);
  assert.equal(isLikelyAutomation("Mozilla/5.0 Chrome/140", true), true);
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

import assert from "node:assert/strict";
import test from "node:test";
import { isCpcJobAlertEligible } from "../lib/cpc-job-alerts";

test("accepts a JobG8 CPC apply link", () => {
  assert.equal(isCpcJobAlertEligible("JobG8", "https://www.jobg8.com/Traffic.aspx?abc=123"), true);
});

test("requires source and expected CPC apply endpoint to agree", () => {
  assert.equal(isCpcJobAlertEligible("WhatJobs", "https://www.jobg8.com/Traffic.aspx?x"), false);
  assert.equal(isCpcJobAlertEligible("JobG8", "https://example.com/apply"), false);
  assert.equal(isCpcJobAlertEligible("JobG8", "https://jobg8.com/Traffic.aspx?x"), false);
  assert.equal(isCpcJobAlertEligible("JobG8", "javascript:alert(1)"), false);
});

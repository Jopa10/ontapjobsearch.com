import test from "node:test";
import assert from "node:assert/strict";
import { buildCampaignUrl } from "../lib/campaign-url";

test("builds an externally publishable Ontap URL with complete campaign attribution", () => {
  assert.equal(
    buildCampaignUrl({
      url: "/north-east/service-administrator-jobs",
      source: "linkedin",
      medium: "organic_social",
      campaign: "linkedin_2026_09_17",
      content: "north_east_admin",
    }),
    "https://www.ontapjobsearch.com/north-east/service-administrator-jobs?utm_source=linkedin&utm_medium=organic_social&utm_campaign=linkedin_2026_09_17&utm_content=north_east_admin",
  );
});

test("preserves an existing query while replacing stale campaign values", () => {
  assert.equal(
    buildCampaignUrl({
      url: "/jobs/search?near=Newcastle&utm_source=old",
      source: "email",
      medium: "owned_email",
      campaign: "weekly_jobs",
    }),
    "https://www.ontapjobsearch.com/jobs/search?near=Newcastle&utm_source=email&utm_medium=owned_email&utm_campaign=weekly_jobs",
  );
});

test("refuses to create tracked links for a different website", () => {
  assert.throws(
    () => buildCampaignUrl({
      url: "https://example.com/jobs",
      source: "linkedin",
      medium: "organic_social",
      campaign: "test",
    }),
    /must point to www\.ontapjobsearch\.com/,
  );
});

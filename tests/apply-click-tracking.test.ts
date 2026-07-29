import assert from "node:assert/strict";
import test from "node:test";
// @ts-expect-error Node's native TypeScript loader requires the source extension.
import { buildApplyClickParameters } from "../lib/apply-click-tracking.ts";

test("builds job-level apply click parameters for GA4", () => {
  assert.deepEqual(
    buildApplyClickParameters(
      {
        apply_url: "https://example.com/apply/3130572494",
        job_id: "3130572494",
        title: "Accounts Administrator",
        employer: "Example Employer",
        location: "Hebburn",
        region: "Tyneside, Wearside & Northumberland",
        source: "NEJobs",
        slice_path: "/north-east/service-administrator-jobs",
      },
      "/jobs/3130572494"
    ),
    {
      job_id: "3130572494",
      job_title: "Accounts Administrator",
      job_employer: "Example Employer",
      job_location: "Hebburn",
      job_region: "Tyneside, Wearside & Northumberland",
      job_source: "NEJobs",
      slice_path: "/north-east/service-administrator-jobs",
      page_path: "/jobs/3130572494",
      link_url: "https://example.com/apply/3130572494",
      destination_url: "https://example.com/apply/3130572494",
    }
  );
});

test("uses the current slice page when no separate slice path is supplied", () => {
  const parameters = buildApplyClickParameters(
    {
      apply_url: "https://example.com/apply/1",
      job_id: "1",
      title: "Administrator",
      employer: "Example Employer",
      location: "Leeds",
      region: "West Yorkshire",
      source: "JobG8",
    },
    "/west-yorkshire/service-administrator-jobs"
  );

  assert.equal(parameters.slice_path, "/west-yorkshire/service-administrator-jobs");
  assert.equal(parameters.page_path, "/west-yorkshire/service-administrator-jobs");
});

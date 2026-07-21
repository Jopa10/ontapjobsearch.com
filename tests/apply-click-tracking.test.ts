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
        location: "Hebburn",
        region: "Tyneside, Wearside & Northumberland",
        slice_path: "/north-east/service-administrator-jobs",
      },
      "/jobs/3130572494"
    ),
    {
      job_id: "3130572494",
      job_title: "Accounts Administrator",
      job_location: "Hebburn",
      job_region: "Tyneside, Wearside & Northumberland",
      slice_path: "/north-east/service-administrator-jobs",
      page_path: "/jobs/3130572494",
      link_url: "https://example.com/apply/3130572494",
    }
  );
});

test("uses the current slice page when no separate slice path is supplied", () => {
  const parameters = buildApplyClickParameters(
    {
      apply_url: "https://example.com/apply/1",
      job_id: "1",
      title: "Administrator",
      location: "Leeds",
      region: "West Yorkshire",
    },
    "/west-yorkshire/service-administrator-jobs"
  );

  assert.equal(parameters.slice_path, "/west-yorkshire/service-administrator-jobs");
  assert.equal(parameters.page_path, "/west-yorkshire/service-administrator-jobs");
});

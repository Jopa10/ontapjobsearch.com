import assert from "node:assert/strict";
import test from "node:test";
import type { PublishedJob } from "../lib/published-jobs";
import { getRelatedJobs } from "../lib/related-jobs";

function job(overrides: Partial<PublishedJob>): PublishedJob {
  return {
    job_id: "job",
    title: "Administrator",
    company: "Example",
    advertiser_name: "",
    advertiser_type: "",
    location: "Leeds",
    region: "West Yorkshire",
    country: "UK",
    category: "Admin/Service – Office Support",
    employment_type: "Permanent",
    salary_min: "",
    salary_max: "",
    salary_period: "",
    salary_text: "£27000 per year",
    work_pattern: "",
    posted_date: "",
    posted_date_basis: "",
    closing_date: "",
    closing_datetime: "",
    description: "Description",
    full_description: "Description",
    apply_url: "https://example.com/apply",
    source: "JobG8",
    working_arrangement: "",
    working_arrangement_text: "",
    working_arrangement_evidence: "",
    slice_path: "/west-yorkshire/service-administrator",
    slice_label: "West Yorkshire Admin & Customer Service Jobs",
    ...overrides,
  };
}

test("ranks same-location and same-slice jobs before regional alternatives", () => {
  const current = job({ job_id: "current" });
  const jobs = [
    current,
    job({ job_id: "same-slice-other-location", location: "Bradford" }),
    job({
      job_id: "same-location-other-slice",
      slice_path: "/west-yorkshire/another-admin-page",
    }),
    job({ job_id: "same-location-same-slice" }),
    job({
      job_id: "same-region-category",
      location: "Wakefield",
      slice_path: "/west-yorkshire/another-admin-page",
    }),
    job({
      job_id: "wrong-category",
      category: "Support Worker",
      slice_path: "/west-yorkshire/support-worker",
    }),
    job({
      job_id: "wrong-region",
      region: "South Yorkshire",
      slice_path: "/south-yorkshire/service-administrator",
    }),
  ];

  assert.deepEqual(
    getRelatedJobs(current, jobs).map(({ job_id }) => job_id),
    [
      "same-location-same-slice",
      "same-location-other-slice",
      "same-slice-other-location",
      "same-region-category",
    ]
  );
});

test("excludes the current job and respects the requested limit", () => {
  const current = job({ job_id: "current" });
  const jobs = [
    current,
    job({ job_id: "a", location: "Bradford" }),
    job({ job_id: "b", location: "Halifax" }),
    job({ job_id: "c", location: "Wakefield" }),
  ];

  assert.deepEqual(
    getRelatedJobs(current, jobs, 2).map(({ job_id }) => job_id),
    ["a", "b"]
  );
});

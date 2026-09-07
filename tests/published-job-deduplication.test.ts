import assert from "node:assert/strict";
import test from "node:test";
import {
  deduplicatePublishedJobs,
  type PublishedJob,
} from "../lib/published-jobs";

function job(job_id: string, overrides: Partial<PublishedJob> = {}): PublishedJob {
  return {
    job_id,
    title: "Office Administrator",
    company: "Example Recruitment",
    advertiser_name: "",
    advertiser_type: "",
    location: "Leeds",
    region: "Yorkshire - West",
    country: "UK",
    category: "Service Administrator",
    employment_type: "Permanent",
    salary_min: "",
    salary_max: "",
    salary_period: "",
    salary_text: "",
    work_pattern: "Full Time",
    posted_date: "2026-09-02",
    posted_date_basis: "source",
    closing_date: "",
    closing_datetime: "",
    description: "A complete and identical vacancy description.",
    full_description: "A complete and identical vacancy description.",
    apply_url: `https://example.com/${job_id}`,
    source: "JobG8",
    working_arrangement: "",
    working_arrangement_text: "",
    working_arrangement_evidence: "",
    slice_path: "/job-search/west-yorkshire/service-administrator-jobs",
    slice_label: "Yorkshire - West Admin Jobs",
    ...overrides,
  };
}

test("identical adverts with different tracking URLs use one stable canonical job", () => {
  const result = deduplicatePublishedJobs([
    job("new-id", { posted_date: "2026-09-03" }),
    job("old-id", { posted_date: "2026-09-01" }),
  ]);

  assert.deepEqual(result.jobs.map(({ job_id }) => job_id), ["old-id"]);
  assert.equal(result.canonicalIds.get("new-id"), "old-id");
  assert.equal(result.canonicalIds.get("old-id"), "old-id");
});

test("similar adverts are retained when material content differs", () => {
  const result = deduplicatePublishedJobs([
    job("first"),
    job("second", { description: "A different vacancy description.", full_description: "A different vacancy description." }),
  ]);

  assert.deepEqual(result.jobs.map(({ job_id }) => job_id), ["first", "second"]);
});

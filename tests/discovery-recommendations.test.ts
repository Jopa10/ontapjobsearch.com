import assert from "node:assert/strict";
import test from "node:test";
import { getDiscoveryRecommendations } from "../lib/discovery-recommendations";
import type { PublishedJob } from "../lib/published-jobs";

function job(overrides: Partial<PublishedJob>): PublishedJob {
  return {
    job_id: "job",
    title: "Admin Assistant",
    company: "Royal Wolverhampton NHS Trust",
    advertiser_name: "",
    advertiser_type: "Company",
    location: "Wolverhampton",
    region: "West Midlands - Black Country",
    country: "UK",
    category: "Admin/Service – Office Support",
    employment_type: "Permanent",
    salary_min: "",
    salary_max: "",
    salary_period: "",
    salary_text: "£27000 per year",
    work_pattern: "",
    posted_date: "2026-09-05",
    posted_date_basis: "",
    closing_date: "",
    closing_datetime: "",
    description: "Routine office administration.",
    full_description: "Routine office administration.",
    apply_url: "https://example.com/apply",
    source: "NHS Jobs",
    working_arrangement: "",
    working_arrangement_text: "",
    working_arrangement_evidence: "",
    slice_path: "/browse-jobs",
    slice_label: "Browse jobs",
    ...overrides,
  };
}

test("uses approved role, sector and straight-line locality rules only", () => {
  const current = job({ job_id: "current" });
  const jobs = [
    current,
    job({ job_id: "exact-private", company: "Spire Healthcare", location: "Wolverhampton" }),
    job({
      job_id: "related-private",
      title: "Administrative Assistant",
      company: "Sky",
      location: "Walsall",
      source: "JobG8",
    }),
    job({ job_id: "public-target", company: "Royal Wolverhampton NHS Trust", location: "Wolverhampton" }),
    job({ job_id: "unknown-target", company: "Unverified Employer", location: "Wolverhampton", source: "JobG8" }),
    job({ job_id: "outside-radius", company: "Sky", location: "Carlisle", source: "JobG8" }),
  ];

  const results = getDiscoveryRecommendations(current, jobs);
  assert.deepEqual(results.map((result) => result.job_id), ["exact-private", "related-private"]);
  assert.equal(results[0].distance_miles, 0);
  assert.ok(results[1].distance_miles > 0 && results[1].distance_miles <= 15);
});

test("permits private-to-private matches but never points a private job to public work", () => {
  const current = job({ job_id: "current-private", company: "Sky", source: "JobG8" });
  const jobs = [
    current,
    job({ job_id: "private-target", company: "Spire Healthcare", location: "Wolverhampton", source: "JobG8" }),
    job({ job_id: "public-target", company: "Royal Wolverhampton NHS Trust", location: "Wolverhampton" }),
  ];

  assert.deepEqual(
    getDiscoveryRecommendations(current, jobs).map((result) => result.job_id),
    ["private-target"],
  );
});

test("uses the published family when an exact source-title relationship is absent", () => {
  const current = job({
    job_id: "harrow-school",
    title: "Receptionist & Admin Assistant",
    company: "Heathland School",
    location: "Harrow",
    region: "London",
    source: "Teaching Vacancies",
  });
  const jobs = [
    current,
    job({
      job_id: "private-receptionist",
      title: "Receptionist",
      company: "Hamberley Care Management Limited",
      location: "London",
      region: "London",
      source: "JobG8",
    }),
    job({
      job_id: "other-family",
      title: "Marketing Assistant",
      category: "Marketing",
      company: "Sky",
      location: "London",
      region: "London",
      source: "JobG8",
    }),
  ];

  assert.deepEqual(
    getDiscoveryRecommendations(current, jobs).map((result) => result.job_id),
    ["private-receptionist"],
  );
});

test("an unknown landing employer can see same-family private jobs but never public jobs", () => {
  const current = job({
    job_id: "agency-source",
    title: "Unregistered Admin Variant",
    company: "Office Angels - Agency - Permanent",
    advertiser_name: "Office Angels",
    advertiser_type: "Agency",
    source: "JobG8",
  });
  const jobs = [
    current,
    job({ job_id: "private-target", title: "Receptionist", company: "Spire Healthcare" }),
    job({ job_id: "public-target", title: "Receptionist", company: "Royal Wolverhampton NHS Trust" }),
  ];

  assert.deepEqual(
    getDiscoveryRecommendations(current, jobs).map((result) => result.job_id),
    ["private-target"],
  );
});

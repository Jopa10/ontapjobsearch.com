import assert from "node:assert/strict";
import test from "node:test";
import { searchJobs } from "../lib/job-search";
import type { PublishedJob } from "../lib/published-jobs";

function job(overrides: Partial<PublishedJob>): PublishedJob {
  return {
    job_id: "job",
    title: "Administrator",
    company: "Example Employer",
    advertiser_name: "",
    advertiser_type: "Company",
    location: "Leeds",
    region: "West Yorkshire",
    country: "UK",
    category: "Admin/Service – Office Support",
    employment_type: "Permanent",
    salary_min: "",
    salary_max: "",
    salary_period: "Annual",
    salary_text: "",
    work_pattern: "Full Time",
    posted_date: "2026-08-12",
    posted_date_basis: "ontap_first_published",
    closing_date: "",
    closing_datetime: "",
    description: "General office role.",
    full_description: "General office role.",
    apply_url: "https://example.com/apply",
    source: "JobG8",
    working_arrangement: "",
    working_arrangement_text: "",
    working_arrangement_evidence: "",
    slice_path: "/west-yorkshire/service-administrator-jobs",
    slice_label: "West Yorkshire Admin & Customer Service Jobs",
    ...overrides,
  };
}

const jobs = [
  job({
    job_id: "purchasing",
    title: "Purchasing Coordinator",
    location: "Oxfordshire",
    region: "Oxfordshire",
    company: "Euro-Projects Recruitment Ltd",
  }),
  job({ job_id: "reception", title: "Receptionist", location: "Oxford", region: "Oxfordshire" }),
  job({ job_id: "admin", title: "Administrator", location: "Didcot", region: "Oxfordshire" }),
  job({ job_id: "admin-assistant", title: "Administrative Assistant", location: "Bicester", region: "Oxfordshire" }),
  job({ job_id: "customer-service", title: "Customer Service Advisor", location: "Surrey", region: "Surrey" }),
  job({ job_id: "customer-support", title: "Customer Support Advisor", location: "Guildford", region: "Surrey" }),
  job({ job_id: "accounts", title: "Accounts Assistant", location: "London", region: "London", category: "Finance / Accounts" }),
  job({ job_id: "hr", title: "Human Resources Administrator", location: "London", region: "London", category: "HR / Recruitment" }),
  job({ job_id: "newcastle-admin", title: "Administrator", location: "Newcastle upon Tyne", region: "North East" }),
  job({ job_id: "newcastle-customer", title: "Customer Service Advisor", location: "Newcastle upon Tyne", region: "North East" }),
  job({
    job_id: "newcastle-reception",
    title: "Receptionist",
    location: "Newcastle upon Tyne",
    region: "North East",
    description: "Front desk role with customer service responsibilities.",
  }),
  job({ job_id: "leeds-admin", title: "Administrator", location: "Leeds", region: "West Yorkshire" }),
  job({
    job_id: "leeds-ledger-admin",
    title: "Sales Ledger Administrator",
    location: "Leeds",
    region: "West Yorkshire",
    category: "Finance / Accounts",
  }),
  job({
    job_id: "leeds-complaints",
    title: "Complaints Handler",
    location: "Leeds",
    region: "West Yorkshire",
    category: "Finance / Accounts",
    description: "Handles finance complaints and related administration.",
  }),
  job({ job_id: "lewes-admin", title: "Administrator", location: "Lewes", region: "Sussex" }),
  job({ job_id: "bristol-admin", title: "Administrator", location: "Bristol", region: "Bristol & Bath", description: "General admin role including employee fees and records." }),
  job({ job_id: "support-worker", title: "Support Worker", location: "Southampton", region: "Hampshire" }),
  job({
    job_id: "support-description-only",
    title: "Care Assistant",
    location: "Southampton",
    region: "Hampshire",
    description: "Provides support to residents while each key worker completes care records.",
  }),
  job({
    job_id: "description-only",
    title: "Office Coordinator",
    location: "Leeds",
    region: "West Yorkshire",
    description: "Works closely with the purchasing coordinator and wider team in London.",
  }),
  job({
    job_id: "broad-office",
    title: "Client Service Advisor",
    location: "London",
    region: "London",
    description: "An office job supporting clients and colleagues.",
  }),
];

test("a place typed into the role box searches location and region", () => {
  const ids = searchJobs(jobs, "oxfordshire", "").map(({ job_id }) => job_id);
  assert.ok(ids.includes("purchasing"));
  assert.ok(ids.includes("reception"));
  assert.ok(ids.includes("admin"));
});

test("a role typed into the location box still works", () => {
  const ids = searchJobs(jobs, "", "receptionist").map(({ job_id }) => job_id);
  assert.equal(ids[0], "reception");
});

test("common role variants and aliases are understood", () => {
  assert.ok(searchJobs(jobs, "admin", "").some(({ job_id }) => job_id === "admin-assistant"));
  assert.equal(searchJobs(jobs, "customer services", "")[0]?.job_id, "customer-service");
  assert.ok(searchJobs(jobs, "customer support", "").some(({ job_id }) => job_id === "customer-service"));
  assert.equal(searchJobs(jobs, "accounts", "")[0]?.job_id, "accounts");
  assert.equal(searchJobs(jobs, "HR", "")[0]?.job_id, "hr");
});

test("minor job-title and location typos are tolerated", () => {
  assert.equal(searchJobs(jobs, "recepitonist", "")[0]?.job_id, "reception");
  assert.ok(searchJobs(jobs, "oxforrd", "").some(({ job_id }) => job_id === "reception"));
});

test("messy admin spellings resolve to the admin concept", () => {
  assert.ok(searchJobs(jobs, "amdin", "").some(({ job_id }) => job_id === "admin"));
  assert.ok(searchJobs(jobs, "adminstrtor", "").some(({ job_id }) => job_id === "admin"));
  assert.ok(searchJobs(jobs, "admistrtr", "").some(({ job_id }) => job_id === "admin"));
});

test("common abbreviated role phrases are canonicalised before matching", () => {
  assert.equal(searchJobs(jobs, "cust srv", "")[0]?.job_id, "customer-service");
  const full = searchJobs(jobs, "support worker", "southamton").map(({ job_id }) => job_id);
  const abbreviated = searchJobs(jobs, "supp worker", "southamton").map(({ job_id }) => job_id);
  assert.deepEqual(abbreviated, full);
  assert.ok(full.includes("support-worker"));
  assert.ok(!full.includes("support-description-only"));
});

test("location abbreviations and truncations stay geographic", () => {
  assert.deepEqual(
    searchJobs(jobs, "", "ncl").map(({ job_id }) => job_id).sort(),
    ["newcastle-admin", "newcastle-customer", "newcastle-reception"].sort()
  );
  assert.deepEqual(
    searchJobs(jobs, "", "newcl").map(({ job_id }) => job_id).sort(),
    ["newcastle-admin", "newcastle-customer", "newcastle-reception"].sort()
  );
});

test("ambiguous short location typos resolve to the strongest geographic candidate", () => {
  const ids = searchJobs(jobs, "admin", "lees").map(({ job_id }) => job_id);
  assert.ok(ids.includes("leeds-admin"));
  assert.ok(ids.includes("leeds-ledger-admin"));
  assert.ok(!ids.includes("lewes-admin"));
});

test("London prefixes do not broaden into descriptions or other fields", () => {
  const expected = searchJobs(jobs, "", "london").map(({ job_id }) => job_id).sort();
  for (const input of ["lon", "lond", "londo"]) {
    assert.deepEqual(searchJobs(jobs, "", input).map(({ job_id }) => job_id).sort(), expected);
  }
  assert.ok(!expected.includes("description-only"));
});

test("mixed one-box searches infer geography instead of leaking nationally", () => {
  const customerIds = searchJobs(jobs, "cust srv ncl", "").map(({ job_id }) => job_id);
  assert.deepEqual(customerIds, ["newcastle-customer"]);

  const adminIds = searchJobs(jobs, "ardmin lees", "").map(({ job_id }) => job_id);
  assert.ok(adminIds.includes("leeds-admin"));
  assert.ok(adminIds.includes("leeds-ledger-admin"));
  assert.ok(!adminIds.includes("lewes-admin"));
  assert.ok(!adminIds.includes("bristol-admin"));
});

test("narrow role searches require title support instead of inheriting the whole curated slice", () => {
  const customerIds = searchJobs(jobs, "customer service", "newcastle").map(({ job_id }) => job_id);
  assert.deepEqual(customerIds, ["newcastle-customer"]);

  const adminIds = searchJobs(jobs, "admin", "leeds").map(({ job_id }) => job_id);
  assert.ok(adminIds.includes("leeds-admin"));
  assert.ok(adminIds.includes("leeds-ledger-admin"));
  assert.ok(!adminIds.includes("description-only"));
  assert.ok(!adminIds.includes("leeds-complaints"));

  const receptionIds = searchJobs(jobs, "reception", "newcastle").map(({ job_id }) => job_id);
  assert.deepEqual(receptionIds, ["newcastle-reception"]);
});

test("compound role searches can use category context but still need the narrow title anchor", () => {
  const ids = searchJobs(jobs, "finance admin", "leeds").map(({ job_id }) => job_id);
  assert.ok(ids.includes("leeds-ledger-admin"));
  assert.ok(!ids.includes("leeds-complaints"));
});

test("broad generic searches remain broad", () => {
  const ids = searchJobs(jobs, "office job", "london").map(({ job_id }) => job_id);
  assert.ok(ids.includes("broad-office"));
});

test("two boxes can be used normally and both constraints are respected", () => {
  const ids = searchJobs(jobs, "administrator", "oxfordshire").map(({ job_id }) => job_id);
  assert.ok(ids.includes("admin"));
  assert.ok(ids.includes("admin-assistant"));
  assert.ok(!ids.includes("hr"));
});

test("strong title/location matches rank ahead of description-only matches", () => {
  const ids = searchJobs(jobs, "purchasing coordinator", "").map(({ job_id }) => job_id);
  assert.equal(ids[0], "purchasing");
  assert.ok(ids.indexOf("description-only") > ids.indexOf("purchasing"));
});
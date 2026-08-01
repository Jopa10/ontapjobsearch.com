import assert from "node:assert/strict";
import test from "node:test";
import {
  buildJobFacts,
  cleanEmployerName,
  formatJobDate,
  formatSalary,
  sourceLabel,
} from "../lib/job-facts";

test("separates a JobG8 recruiter from duplicated contract text", () => {
  const job = {
    company: "Huntress - Agency - Temporary",
    advertiser_type: "Agency",
    employment_type: "Temporary",
    location: "Leeds",
    salary_text: "£12710 per year",
    source: "JobG8",
  };

  assert.equal(cleanEmployerName(job), "Huntress");
  assert.deepEqual(
    buildJobFacts(job).map(({ label, value }) => [label, value]),
    [
      ["Recruiter", "Huntress"],
      ["Location", "Leeds"],
      ["Salary", "£12,710 per year"],
      ["Contract", "Temporary"],
    ]
  );
});

test("keeps source available for contextual application cues but not public facts", () => {
  const facts = buildJobFacts({ company: "Example", source: "JobG8" });

  assert.equal(facts.some((fact) => fact.label === "Source"), false);
  assert.equal(sourceLabel("NEJobs"), "North East Jobs");
});

test("omits uncertain work and on-site labels", () => {
  const facts = buildJobFacts({
    company: "Example Council",
    employment_type: "Permanent",
    work_pattern: "Please see advert text",
    working_arrangement: "onsite_or_not_stated",
    posted_date: "not a date",
    source: "NEJobs",
  });

  assert.equal(facts.some((fact) => fact.key === "work_pattern"), false);
  assert.equal(facts.some((fact) => fact.key === "working_arrangement"), false);
  assert.equal(facts.some((fact) => fact.key === "posted"), false);
});

test("uses genuine work pattern, hybrid and dates when supplied", () => {
  const facts = buildJobFacts({
    advertiser_name: "Durham County Council",
    location: "Durham",
    employment_type: "Permanent",
    work_pattern: "Full time",
    working_arrangement: "hybrid",
    working_arrangement_text: "Up to 2 days from home",
    posted_date: "2026-07-10",
    posted_date_basis: "source",
    closing_date: "2026-08-09",
    source: "NEJobs",
  });

  const values = Object.fromEntries(facts.map((fact) => [fact.key, fact.value]));
  assert.equal(values.work_pattern, "Full time");
  assert.equal(values.working_arrangement, "Up to 2 days from home");
  assert.equal(values.posted, "10 July 2026");
  assert.equal(values.closing, "9 August 2026");
});

test("distinguishes source and Ontap publication dates", () => {
  const sourceFacts = buildJobFacts({
    company: "Example",
    posted_date: "2026-07-10",
    posted_date_basis: "source",
    source: "JobG8",
  });
  const ontapFacts = buildJobFacts({
    company: "Example",
    posted_date: "2026-07-11",
    posted_date_basis: "ontap_first_published",
    source: "JobG8",
  });
  const unknownFacts = buildJobFacts({
    company: "Example",
    posted_date: "2026-07-12",
    source: "JobG8",
  });

  assert.equal(sourceFacts.find((fact) => fact.key === "posted")?.label, "Posted");
  assert.equal(ontapFacts.find((fact) => fact.key === "posted")?.label, "First listed by Ontap");
  assert.equal(unknownFacts.some((fact) => fact.key === "posted"), false);
});

test("formatters reject uncertain dates and clean salaries", () => {
  assert.equal(formatJobDate("31/07/2026"), "");
  assert.equal(formatSalary("£27000 - £29000 per year"), "£27,000 - £29,000 per year");
});

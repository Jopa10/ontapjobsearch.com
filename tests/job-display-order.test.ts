import assert from "node:assert/strict";
import test from "node:test";
import { orderJobsForDisplay, type DisplayOrderJob } from "../lib/job-display-order";

type Job = DisplayOrderJob & { job_id: string };

function job(job_id: string, overrides: Partial<Job> = {}): Job {
  return {
    job_id,
    source: "JobG8",
    location: job_id,
    title: "Administrator",
    posted_date: "2026-08-20",
    ...overrides,
  };
}

test("pages with no NHS jobs keep the established location-first ordering", () => {
  const ordered = orderJobsForDisplay([
    job("z", { location: "York" }),
    job("a2", { location: "Leeds", title: "Receptionist" }),
    job("a1", { location: "Leeds", title: "Administrator" }),
  ]);
  assert.deepEqual(ordered.map(({ job_id }) => job_id), ["a1", "a2", "z"]);
});

test("accepted NHS jobs are spaced after four core jobs and Tier A remains ahead of Tier B", () => {
  const base = Array.from({ length: 8 }, (_, index) =>
    job(`base-${index + 1}`, { location: `Location ${index + 1}` })
  );
  const ordered = orderJobsForDisplay([
    ...base,
    job("nhs-b", {
      source: "NHS Jobs",
      hc_tier: "B",
      switchability: "OPEN_SWITCH",
      location: "A location",
    }),
    job("nhs-a", {
      source: "NHS Jobs",
      hc_tier: "A",
      switchability: "OPEN_SWITCH",
      location: "Z location",
    }),
  ]);

  assert.equal(ordered[4]?.job_id, "nhs-a");
  assert.equal(ordered[9]?.job_id, "nhs-b");
  assert.equal(ordered.slice(0, 4).some(({ source }) => source === "NHS Jobs"), false);
});

test("switchability and freshness only rank NHS jobs within the existing Tier priority", () => {
  const base = Array.from({ length: 12 }, (_, index) => job(`base-${index + 1}`));
  const ordered = orderJobsForDisplay([
    ...base,
    job("nhs-bridge", {
      source: "NHS Jobs",
      hc_tier: "A",
      switchability: "BRIDGEABLE",
      posted_date: "2026-08-21",
    }),
    job("nhs-open-old", {
      source: "NHS Jobs",
      hc_tier: "A",
      switchability: "OPEN_SWITCH",
      posted_date: "2026-08-18",
    }),
    job("nhs-open-new", {
      source: "NHS Jobs",
      hc_tier: "A",
      switchability: "OPEN_SWITCH",
      posted_date: "2026-08-20",
    }),
  ]);

  const nhsIds = ordered
    .filter(({ source }) => source === "NHS Jobs")
    .map(({ job_id }) => job_id);
  assert.deepEqual(nhsIds, ["nhs-open-new", "nhs-open-old", "nhs-bridge"]);
});

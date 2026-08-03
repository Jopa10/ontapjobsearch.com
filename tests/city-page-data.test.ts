import assert from "node:assert/strict";
import test from "node:test";
import {
  cityPageContainsJob,
  type CityPageDefinition,
  type CityPageJob,
} from "../lib/city-page-data";

const definition: CityPageDefinition = {
  key: "test-city-admin",
  route: "/test-city/admin-jobs",
  listingLabel: "Test City Admin jobs",
  jsonPath: ["app", "_city-pages", "test-city", "admin-jobs.json"],
  minimumJobs: 3,
};

function jobs(...ids: string[]): CityPageJob[] {
  return ids.map((job_id) => ({ job_id, title: `Job ${job_id}` }));
}

test("recognises a job only when the city page meets its live threshold", () => {
  assert.equal(cityPageContainsJob(definition, jobs("a", "b"), "a"), false);
  assert.equal(cityPageContainsJob(definition, jobs("a", "b", "c"), "a"), true);
});

test("does not assign unrelated jobs to an active city page", () => {
  assert.equal(cityPageContainsJob(definition, jobs("a", "b", "c"), "outside"), false);
});

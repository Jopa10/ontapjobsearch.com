import assert from "node:assert/strict";
import test from "node:test";
import {
  cityPageContainsJob,
  getActiveCityLinksForParentJsonPath,
  getCityPageBreadcrumb,
  type CityPageDefinition,
  type CityPageJob,
} from "../lib/city-page-data";

const definition: CityPageDefinition = {
  key: "test-city-admin",
  displayName: "Test City",
  categoryLabel: "admin and customer-service jobs",
  route: "/test-city/admin-jobs",
  listingLabel: "Test City Admin jobs",
  jsonPath: ["app", "_city-pages", "test-city", "admin-jobs.json"],
  parentRoute: "/test-region/admin-jobs",
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

test("builds the agreed role, region and city breadcrumb for York", () => {
  assert.deepEqual(
    getCityPageBreadcrumb(["app", "_city-pages", "york", "service-administrator-jobs.json"]),
    {
      cityLabel: "York",
      cityRoute: "/york/service-administrator-jobs",
      parentLabel: "North Yorkshire",
      parentRoute: "/north-yorkshire/service-administrator-jobs",
      roleLabel: "Service Administrator jobs",
      roleRoute: "/browse-jobs#admin-service-jobs",
    }
  );
});

test("regional JSON paths expose every active registered child city", () => {
  assert.deepEqual(
    getActiveCityLinksForParentJsonPath([
      "app",
      "west-yorkshire",
      "service-administrator-jobs.json",
    ]),
    [
      { href: "/bradford/service-administrator-jobs", label: "Bradford" },
      { href: "/huddersfield/service-administrator-jobs", label: "Huddersfield" },
      { href: "/leeds/service-administrator-jobs", label: "Leeds" },
    ]
  );
});

test("configured regional slices resolve to their public job-search parent route", () => {
  const breadcrumb = getCityPageBreadcrumb([
    "app",
    "_city-pages",
    "birmingham",
    "service-administrator-jobs.json",
  ]);
  assert.equal(
    breadcrumb?.parentRoute,
    "/job-search/birmingham-solihull/service-administrator-jobs"
  );
  assert.deepEqual(
    getActiveCityLinksForParentJsonPath([
      "app",
      "_city-pages",
      "configured-slices",
      "birmingham-solihull",
      "service-administrator-jobs.json",
    ]),
    [{ href: "/birmingham/service-administrator-jobs", label: "Birmingham" }]
  );
});

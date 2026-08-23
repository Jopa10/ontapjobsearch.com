import assert from "node:assert/strict";
import test from "node:test";
import { renderToStaticMarkup } from "react-dom/server";
import JobViewSwitcher from "../components/JobViewSwitcher";
import QuickJobList, { type QuickJob } from "../components/QuickJobList";
import { classifyJobSector, findNthJobSectorIndex } from "../lib/job-sector";

test("uses authoritative feeds for NHS and school classifications", () => {
  assert.deepEqual(classifyJobSector({ source: "NHS Jobs", title: "Receptionist" }), {
    sector: "public",
    label: "NHS / GP",
  });
  assert.deepEqual(
    classifyJobSector({ source: "Teaching Vacancies", title: "Administrator" }),
    { sector: "public", label: "School" },
  );
});

test("classifies only explicit JobG8 public-service or charity wording", () => {
  assert.deepEqual(
    classifyJobSector({ source: "JobG8", company: "Camden Borough Council" }),
    { sector: "public", label: "Council" },
  );
  assert.deepEqual(
    classifyJobSector({ source: "JobG8", description: "Join our registered charity" }),
    { sector: "public", label: "Charity" },
  );
  assert.deepEqual(
    classifyJobSector({ source: "JobG8", title: "Medical Receptionist" }),
    { sector: "business" },
  );
});

test("finds the fifth visible business job even when public jobs are interleaved", () => {
  const jobs = [
    { source: "JobG8" },
    { source: "JobG8" },
    { source: "NHS Jobs" },
    { source: "JobG8" },
    { source: "Teaching Vacancies" },
    { source: "JobG8" },
    { source: "JobG8" },
  ];

  assert.equal(findNthJobSectorIndex(jobs, "business", 5), 6);
});

const sampleJobs: QuickJob[] = [
  {
    job_id: "business-1",
    title: "Service Administrator",
    company: "Example Ltd",
    advertiser_name: "Example Ltd",
    advertiser_type: "Employer",
    location: "London",
    employment_type: "Permanent",
    salary_text: "£28,000 per year",
    source: "JobG8",
    at_a_glance_attributes: [],
  },
  {
    job_id: "public-1",
    title: "Medical Receptionist",
    company: "Example Practice",
    advertiser_name: "Example Practice",
    advertiser_type: "Employer",
    location: "London",
    employment_type: "Permanent",
    salary_text: "",
    source: "NHS Jobs",
    at_a_glance_attributes: [],
  },
];

test("server markup keeps all sector jobs available and visibly labels public jobs", () => {
  const html = renderToStaticMarkup(
    <JobViewSwitcher
      sectorFilterEnabled
      sectorCounts={{ all: 2, business: 1, public: 1 }}
      quickView={<QuickJobList jobs={sampleJobs} sectorFilterEnabled />}
      detailedView={
        <div>
          <article data-job-sector="business">Business detail</article>
          <article data-job-sector="public">Public detail</article>
        </div>
      }
    />,
  );

  assert.match(html, /All jobs/);
  assert.match(html, /Business &amp; agency/);
  assert.match(html, /Public service &amp; charity/);
  assert.equal((html.match(/data-job-sector="business"/g) || []).length, 2);
  assert.equal((html.match(/data-job-sector="public"/g) || []).length, 2);
  assert.match(html, /NHS \/ GP/);
});

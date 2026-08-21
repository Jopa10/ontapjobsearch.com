import fs from "node:fs";
import path from "node:path";
import { getPublishedJobs } from "../lib/published-jobs";

const target = path.join(process.cwd(), "generated", "published-jobs-search.json");
const jobs = getPublishedJobs().map((job) => ({
  ...job,
  // Search never examines beyond this point, so do not make the serverless
  // bundle carry every full advert purely for keyword matching.
  description: job.description.slice(0, 2200),
  full_description: "",
}));

fs.mkdirSync(path.dirname(target), { recursive: true });
fs.writeFileSync(target, `${JSON.stringify(jobs)}\n`, "utf8");
console.log(`Generated search index with ${jobs.length} published jobs.`);

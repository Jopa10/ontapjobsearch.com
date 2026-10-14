import fs from "node:fs";
import path from "node:path";
import { buildPublishedJobSearchData } from "../lib/job-search";
import { getPublishedCanonicalIds, getPublishedJobs } from "../lib/published-jobs-source";

const target = path.join(process.cwd(), "generated", "published-jobs-search.json");
const publishedJobsTarget = path.join(process.cwd(), "generated", "published-jobs.json");
const canonicalIdsTarget = path.join(process.cwd(), "generated", "published-job-canonical-ids.json");

const jobs = getPublishedJobs().map((job) => {
  const searchData = buildPublishedJobSearchData(job);

  return {
    ...job,
    // The search route uses the prebuilt search metadata below. Keeping the raw
    // advert body out of the serverless bundle reduces parse/startup work while
    // preserving the same title/location/category/company/description matching.
    description: "",
    full_description: "",
    _search: searchData,
  };
});

fs.mkdirSync(path.dirname(target), { recursive: true });
fs.writeFileSync(target, `${JSON.stringify(jobs)}\n`, "utf8");
fs.writeFileSync(publishedJobsTarget, `${JSON.stringify(getPublishedJobs())}\n`, "utf8");
fs.writeFileSync(canonicalIdsTarget, `${JSON.stringify(getPublishedCanonicalIds())}\n`, "utf8");
console.log(`Generated indexed search data with ${jobs.length} published jobs.`);

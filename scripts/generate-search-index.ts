import fs from "node:fs";
import path from "node:path";
import { buildPublishedJobSearchData } from "../lib/job-search";
import { getPublishedJobs } from "../lib/published-jobs";

const target = path.join(process.cwd(), "generated", "published-jobs-search.json");

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
console.log(`Generated indexed search data with ${jobs.length} published jobs.`);

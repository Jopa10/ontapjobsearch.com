export type DisplayOrderJob = {
  source?: string;
  location?: string;
  title?: string;
  hc_tier?: string;
  switchability?: string;
  posted_date?: string;
};

function normalise(value: unknown) {
  return String(value || "").trim();
}

function locationFirst<T extends DisplayOrderJob>(jobs: T[]): T[] {
  return [...jobs].sort((left, right) => {
    const locationOrder = (normalise(left.location) || "ZZZ").localeCompare(
      normalise(right.location) || "ZZZ",
      "en-GB",
      { sensitivity: "base", numeric: true }
    );
    if (locationOrder) return locationOrder;
    return normalise(left.title).localeCompare(normalise(right.title), "en-GB", {
      sensitivity: "base",
      numeric: true,
    });
  });
}

function isNhsJob(job: DisplayOrderJob) {
  return normalise(job.source).toLowerCase() === "nhs jobs";
}

function nhsTierRank(job: DisplayOrderJob) {
  const tier = normalise(job.hc_tier).toUpperCase();
  if (tier === "A") return 0;
  if (tier === "B") return 1;
  return 2;
}

function nhsSwitchRank(job: DisplayOrderJob) {
  const switchability = normalise(job.switchability).toUpperCase();
  if (switchability === "OPEN_SWITCH" || switchability === "PURE_SWITCH") return 0;
  if (switchability === "BRIDGEABLE" || switchability === "POSSIBLE_SWITCH") return 1;
  if (switchability === "NHS_EXPERIENCE_NEEDED") return 2;
  return 3;
}

function postedTime(job: DisplayOrderJob) {
  const value = normalise(job.posted_date);
  if (!value) return 0;
  const parsed = Date.parse(value);
  return Number.isNaN(parsed) ? 0 : parsed;
}

function nhsPriority<T extends DisplayOrderJob>(jobs: T[]): T[] {
  return [...jobs].sort((left, right) => {
    const tierOrder = nhsTierRank(left) - nhsTierRank(right);
    if (tierOrder) return tierOrder;

    const switchOrder = nhsSwitchRank(left) - nhsSwitchRank(right);
    if (switchOrder) return switchOrder;

    const dateOrder = postedTime(right) - postedTime(left);
    if (dateOrder) return dateOrder;

    return normalise(left.title).localeCompare(normalise(right.title), "en-GB", {
      sensitivity: "base",
      numeric: true,
    });
  });
}

/**
 * Keep the normal location-first scan for the core inventory, while treating NHS
 * as a complementary stream. Regional composition already enforces <=20% NHS;
 * putting at most one accepted NHS job after each four non-NHS jobs prevents a
 * quality-ranked NHS subset from bunching at the top of the user-facing page.
 */
export function orderJobsForDisplay<T extends DisplayOrderJob>(jobs: T[]): T[] {
  const nonNhs = locationFirst(jobs.filter((job) => !isNhsJob(job)));
  const nhs = nhsPriority(jobs.filter(isNhsJob));
  if (!nhs.length) return nonNhs;

  const output: T[] = [];
  let nhsIndex = 0;
  for (let index = 0; index < nonNhs.length; index += 1) {
    output.push(nonNhs[index]);
    if ((index + 1) % 4 === 0 && nhsIndex < nhs.length) {
      output.push(nhs[nhsIndex]);
      nhsIndex += 1;
    }
  }

  // On normal regional pages the 20% source ceiling means there should be no
  // leftovers. Keep this fail-soft for derived/special views rather than dropping jobs.
  if (nhsIndex < nhs.length) output.push(...nhs.slice(nhsIndex));
  return output;
}

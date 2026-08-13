import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { getPublishedJobs, type PublishedJob } from "../lib/published-jobs";

const SITE_URL = "https://www.ontapjobsearch.com";
const ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish";
const STATE_PATH = path.join(
  process.cwd(),
  "pipeline",
  "manifests",
  "google-indexing-state.json"
);
const MAX_NOTIFICATIONS = Number(process.env.GOOGLE_INDEXING_MAX_NOTIFICATIONS || "200");
const RUN_REPORT_PATH = process.env.GOOGLE_INDEXING_RUN_REPORT?.trim();

type NotificationType = "URL_UPDATED" | "URL_DELETED";

type Notification = {
  url: string;
  type: NotificationType;
  fingerprint?: string;
};

type IndexingState = {
  version: 1;
  updatedAt: string;
  urls: Record<string, string>;
};

type RunStatus = "noop" | "dry-run" | "success" | "backlog" | "failure";

type RunReport = {
  status: RunStatus;
  mode: "live" | "dry-run";
  eligibleLive: number;
  previouslySubmitted: number;
  pendingTotal: number;
  pendingUpdates: number;
  pendingDeletions: number;
  batchLimit: number;
  plannedThisRun: number;
  attempted: number;
  submitted: number;
  remaining: number;
  limitReached: boolean;
  zeroSubmittedWithPending: boolean;
  message: string;
};

function hasCompleteDescription(value: string) {
  const normalised = value.replace(/\s+/g, " ").trim();
  return (
    normalised.length >= 200 &&
    !/click apply for full job details|click apply for more details/i.test(normalised)
  );
}

function jobUrl(jobId: string) {
  return `${SITE_URL}/jobs/${encodeURIComponent(jobId)}`;
}

function fingerprint(job: PublishedJob) {
  const schemaRelevantFields = {
    job_id: job.job_id,
    title: job.title,
    description: job.description,
    company: job.company,
    advertiser_name: job.advertiser_name,
    location: job.location,
    region: job.region,
    posted_date: job.posted_date,
    posted_date_basis: job.posted_date_basis,
    closing_date: job.closing_date,
    closing_datetime: job.closing_datetime,
  };

  return crypto
    .createHash("sha256")
    .update(JSON.stringify(schemaRelevantFields))
    .digest("hex");
}

function loadState(): IndexingState {
  if (!fs.existsSync(STATE_PATH)) {
    return { version: 1, updatedAt: "", urls: {} };
  }

  try {
    const parsed = JSON.parse(fs.readFileSync(STATE_PATH, "utf8")) as Partial<IndexingState>;
    if (parsed.version !== 1 || !parsed.urls || typeof parsed.urls !== "object") {
      throw new Error("unsupported state format");
    }
    return {
      version: 1,
      updatedAt: typeof parsed.updatedAt === "string" ? parsed.updatedAt : "",
      urls: parsed.urls,
    };
  } catch (error) {
    throw new Error(`Unable to read ${STATE_PATH}: ${String(error)}`);
  }
}

function writeState(urls: Record<string, string>) {
  fs.mkdirSync(path.dirname(STATE_PATH), { recursive: true });
  const state: IndexingState = {
    version: 1,
    updatedAt: new Date().toISOString(),
    urls: Object.fromEntries(Object.entries(urls).sort(([a], [b]) => a.localeCompare(b))),
  };
  fs.writeFileSync(STATE_PATH, `${JSON.stringify(state, null, 2)}\n`, "utf8");
}

function writeRunReport(report: RunReport) {
  if (!RUN_REPORT_PATH) return;
  fs.mkdirSync(path.dirname(RUN_REPORT_PATH), { recursive: true });
  fs.writeFileSync(RUN_REPORT_PATH, `${JSON.stringify(report, null, 2)}\n`, "utf8");
}

function buildNotifications(state: IndexingState) {
  const current = new Map<string, string>();

  for (const job of getPublishedJobs()) {
    if (!hasCompleteDescription(job.description)) continue;
    current.set(jobUrl(job.job_id), fingerprint(job));
  }

  const notifications: Notification[] = [];

  // Deletions always go first so expired/removed jobs cannot be stranded behind updates.
  for (const url of Object.keys(state.urls).sort()) {
    if (!current.has(url)) notifications.push({ url, type: "URL_DELETED" });
  }

  // Then submit only new or materially changed eligible JobPosting pages.
  for (const [url, hash] of [...current.entries()].sort(([a], [b]) => a.localeCompare(b))) {
    if (state.urls[url] !== hash) {
      notifications.push({ url, type: "URL_UPDATED", fingerprint: hash });
    }
  }

  return { notifications, currentCount: current.size };
}

async function submit(notification: Notification, token: string) {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url: notification.url, type: notification.type }),
  });

  const body = await response.text();
  if (!response.ok) {
    throw new Error(
      `${notification.type} ${notification.url} failed: HTTP ${response.status} ${body}`
    );
  }
}

function createReportBase(
  dryRun: boolean,
  currentCount: number,
  previousCount: number,
  notifications: Notification[]
) {
  const updates = notifications.filter((item) => item.type === "URL_UPDATED").length;
  const deletions = notifications.length - updates;
  const plannedThisRun = Math.min(notifications.length, MAX_NOTIFICATIONS);

  return {
    mode: dryRun ? ("dry-run" as const) : ("live" as const),
    eligibleLive: currentCount,
    previouslySubmitted: previousCount,
    pendingTotal: notifications.length,
    pendingUpdates: updates,
    pendingDeletions: deletions,
    batchLimit: MAX_NOTIFICATIONS,
    plannedThisRun,
    limitReached: notifications.length >= MAX_NOTIFICATIONS,
  };
}

function reportAndLog(report: RunReport) {
  writeRunReport(report);
  console.log(`Run status: ${report.status}`);
  console.log(`Planned this run: ${report.plannedThisRun}`);
  console.log(`Submitted this run: ${report.submitted}`);
  console.log(`Remaining after run: ${report.remaining}`);
  if (report.limitReached) {
    console.log(`Safety limit reached: ${report.batchLimit}`);
  }
  console.log(report.message);
}

async function main() {
  const dryRun = process.argv.includes("--dry-run");

  if (!Number.isInteger(MAX_NOTIFICATIONS) || MAX_NOTIFICATIONS < 1 || MAX_NOTIFICATIONS > 200) {
    throw new Error(
      `GOOGLE_INDEXING_MAX_NOTIFICATIONS must be an integer between 1 and 200; got ${MAX_NOTIFICATIONS}`
    );
  }

  const state = loadState();
  const { notifications, currentCount } = buildNotifications(state);
  const previousCount = Object.keys(state.urls).length;
  const base = createReportBase(dryRun, currentCount, previousCount, notifications);

  console.log(`Eligible live JobPosting URLs: ${currentCount}`);
  console.log(`Previously submitted URLs: ${previousCount}`);
  console.log(`Notifications required: ${notifications.length}`);
  console.log(`  URL_UPDATED: ${base.pendingUpdates}`);
  console.log(`  URL_DELETED: ${base.pendingDeletions}`);

  if (notifications.length === 0) {
    const report: RunReport = {
      ...base,
      status: "noop",
      attempted: 0,
      submitted: 0,
      remaining: 0,
      zeroSubmittedWithPending: false,
      message: "Nothing to submit.",
    };
    reportAndLog(report);
    return;
  }

  const batch = notifications.slice(0, MAX_NOTIFICATIONS);

  if (dryRun) {
    console.log(
      `[dry-run] Would submit ${batch.length} of ${notifications.length} pending notifications this run.`
    );
    for (const notification of batch) {
      console.log(`[dry-run] ${notification.type} ${notification.url}`);
    }

    const report: RunReport = {
      ...base,
      status: "dry-run",
      attempted: 0,
      submitted: 0,
      remaining: notifications.length,
      zeroSubmittedWithPending: true,
      message:
        notifications.length > MAX_NOTIFICATIONS
          ? `[dry-run] ${notifications.length - MAX_NOTIFICATIONS} notifications would remain for later quota windows.`
          : "[dry-run] All pending notifications fit within one quota window.",
    };
    reportAndLog(report);
    return;
  }

  const token = process.env.GOOGLE_INDEXING_ACCESS_TOKEN?.trim();
  if (!token) {
    const report: RunReport = {
      ...base,
      status: "failure",
      attempted: 0,
      submitted: 0,
      remaining: notifications.length,
      zeroSubmittedWithPending: true,
      message: "GOOGLE_INDEXING_ACCESS_TOKEN is required for a live submission.",
    };
    reportAndLog(report);
    throw new Error(report.message);
  }

  const nextState = { ...state.urls };
  let submitted = 0;
  let attempted = 0;

  try {
    for (const notification of batch) {
      attempted += 1;
      await submit(notification, token);
      submitted += 1;

      if (notification.type === "URL_DELETED") {
        delete nextState[notification.url];
      } else if (notification.fingerprint) {
        nextState[notification.url] = notification.fingerprint;
      }

      // Checkpoint every confirmed success. If a later request fails, the workflow
      // can still commit all successful progress instead of resubmitting it tomorrow.
      writeState(nextState);
      console.log(`${notification.type} ${notification.url}`);
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    const report: RunReport = {
      ...base,
      status: "failure",
      attempted,
      submitted,
      remaining: notifications.length - submitted,
      zeroSubmittedWithPending: notifications.length > 0 && submitted === 0,
      message,
    };
    reportAndLog(report);
    throw error;
  }

  const remaining = notifications.length - submitted;
  const report: RunReport = {
    ...base,
    status: remaining > 0 ? "backlog" : "success",
    attempted,
    submitted,
    remaining,
    zeroSubmittedWithPending: notifications.length > 0 && submitted === 0,
    message:
      remaining > 0
        ? `Successfully submitted ${submitted} notifications; ${remaining} remain for future quota windows.`
        : `Successfully submitted ${submitted} notifications; backlog cleared.`,
  };
  reportAndLog(report);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exitCode = 1;
});

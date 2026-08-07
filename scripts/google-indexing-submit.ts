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

function buildNotifications(state: IndexingState) {
  const current = new Map<string, string>();

  for (const job of getPublishedJobs()) {
    if (!hasCompleteDescription(job.description)) continue;
    current.set(jobUrl(job.job_id), fingerprint(job));
  }

  const notifications: Notification[] = [];

  // Remove URLs that were previously eligible JobPosting pages but are no longer live/eligible.
  for (const url of Object.keys(state.urls).sort()) {
    if (!current.has(url)) notifications.push({ url, type: "URL_DELETED" });
  }

  // Submit only new or materially changed eligible JobPosting pages.
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

async function main() {
  const dryRun = process.argv.includes("--dry-run");
  const state = loadState();
  const { notifications, currentCount } = buildNotifications(state);

  console.log(`Eligible live JobPosting URLs: ${currentCount}`);
  console.log(`Previously submitted URLs: ${Object.keys(state.urls).length}`);
  console.log(`Notifications required: ${notifications.length}`);

  const updates = notifications.filter((item) => item.type === "URL_UPDATED").length;
  const deletions = notifications.length - updates;
  console.log(`  URL_UPDATED: ${updates}`);
  console.log(`  URL_DELETED: ${deletions}`);

  if (!Number.isInteger(MAX_NOTIFICATIONS) || MAX_NOTIFICATIONS < 1 || MAX_NOTIFICATIONS > 200) {
    throw new Error(
      `GOOGLE_INDEXING_MAX_NOTIFICATIONS must be an integer between 1 and 200; got ${MAX_NOTIFICATIONS}`
    );
  }

  if (notifications.length > MAX_NOTIFICATIONS) {
    throw new Error(
      `Refusing to submit ${notifications.length} notifications: run limit is ${MAX_NOTIFICATIONS}. ` +
        "No API calls were made. Reduce the eligible set or handle the backlog across quota windows."
    );
  }

  if (notifications.length === 0) {
    console.log("Nothing to submit.");
    return;
  }

  if (dryRun) {
    for (const notification of notifications) {
      console.log(`[dry-run] ${notification.type} ${notification.url}`);
    }
    return;
  }

  const token = process.env.GOOGLE_INDEXING_ACCESS_TOKEN?.trim();
  if (!token) throw new Error("GOOGLE_INDEXING_ACCESS_TOKEN is required for a live submission");

  const nextState = { ...state.urls };
  let submitted = 0;

  try {
    for (const notification of notifications) {
      await submit(notification, token);
      submitted += 1;

      if (notification.type === "URL_DELETED") {
        delete nextState[notification.url];
      } else if (notification.fingerprint) {
        nextState[notification.url] = notification.fingerprint;
      }

      console.log(`${notification.type} ${notification.url}`);
    }
  } catch (error) {
    // Preserve successful notifications so a retry does not needlessly consume quota again.
    if (submitted > 0) writeState(nextState);
    throw error;
  }

  writeState(nextState);
  console.log(`Successfully submitted ${submitted} notifications.`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exitCode = 1;
});

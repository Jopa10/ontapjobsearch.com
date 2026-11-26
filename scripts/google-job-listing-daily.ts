import { appendFileSync } from 'node:fs';
import { Pool } from 'pg';

const PROPERTY = process.env.GOOGLE_SEARCH_CONSOLE_PROPERTY || 'sc-domain:ontapjobsearch.com';
const API_ROOT = 'https://www.googleapis.com/webmasters/v3/sites';
const ROW_LIMIT = 25_000;
const MAX_DAILY_ROWS = 50_000;
const RETENTION_DAYS = 500;

type SearchRow = {
  keys?: string[];
  clicks?: number;
  impressions?: number;
  ctr?: number;
  position?: number;
};

type SearchResponse = { rows?: SearchRow[] };

type PageMetric = {
  pageUrl: string;
  clicks: number;
  impressions: number;
  ctr: number | null;
  averagePosition: number | null;
};

function required(name: string): string {
  const value = process.env[name]?.trim();
  if (!value) throw new Error(`${name} is required`);
  return value;
}

function dateInPacific(): string {
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Los_Angeles',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).formatToParts(new Date());
  const values = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return `${values.year}-${values.month}-${values.day}`;
}

function addDays(date: string, days: number): string {
  const value = new Date(`${date}T00:00:00.000Z`);
  value.setUTCDate(value.getUTCDate() + days);
  return value.toISOString().slice(0, 10);
}

function validateDate(value: string): string {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value) || Number.isNaN(Date.parse(`${value}T00:00:00Z`))) {
    throw new Error(`Invalid report date: ${value}; expected YYYY-MM-DD`);
  }
  if (new Date(`${value}T00:00:00Z`).toISOString().slice(0, 10) !== value) {
    throw new Error(`Invalid report date: ${value}`);
  }
  return value;
}

function searchUrl(): string {
  return `${API_ROOT}/${encodeURIComponent(PROPERTY)}/searchAnalytics/query`;
}

async function querySearchAnalytics(body: Record<string, unknown>): Promise<SearchRow[]> {
  const response = await fetch(searchUrl(), {
    method: 'POST',
    headers: {
      authorization: `Bearer ${required('GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN')}`,
      'content-type': 'application/json',
    },
    body: JSON.stringify({
      ...body,
      type: 'web',
      dataState: 'final',
      dimensionFilterGroups: [
        {
          groupType: 'and',
          filters: [
            { dimension: 'searchAppearance', operator: 'equals', expression: 'JOB_LISTING' },
          ],
        },
      ],
    }),
  });

  if (!response.ok) {
    const detail = (await response.text()).slice(0, 1_000);
    throw new Error(`Search Console query failed (${response.status}): ${detail}`);
  }
  const result = (await response.json()) as SearchResponse;
  return result.rows ?? [];
}

async function fetchDailyMetrics(reportDate: string): Promise<{
  clicks: number;
  impressions: number;
  pages: PageMetric[];
}> {
  const totalsRows = await querySearchAnalytics({
    startDate: reportDate,
    endDate: reportDate,
    rowLimit: 1,
  });
  const totals = totalsRows[0] ?? {};
  const pages: PageMetric[] = [];

  for (let startRow = 0; startRow < MAX_DAILY_ROWS; startRow += ROW_LIMIT) {
    const rows = await querySearchAnalytics({
      startDate: reportDate,
      endDate: reportDate,
      dimensions: ['page'],
      rowLimit: ROW_LIMIT,
      startRow,
    });

    for (const row of rows) {
      const pageUrl = row.keys?.[0];
      if (!pageUrl) throw new Error(`Search Console returned a page row without a URL for ${reportDate}`);
      pages.push({
        pageUrl,
        clicks: Number(row.clicks ?? 0),
        impressions: Number(row.impressions ?? 0),
        ctr: row.ctr == null ? null : Number(row.ctr),
        averagePosition: row.position == null ? null : Number(row.position),
      });
    }

    if (rows.length < ROW_LIMIT) break;
  }

  return {
    clicks: Number(totals.clicks ?? 0),
    impressions: Number(totals.impressions ?? 0),
    pages,
  };
}

async function replaceDailyRows(
  pool: Pool,
  reportDate: string,
  metrics: Awaited<ReturnType<typeof fetchDailyMetrics>>,
  fetchedAt: string
) {
  const pageClicks = metrics.pages.reduce((sum, page) => sum + page.clicks, 0);
  const pageImpressions = metrics.pages.reduce((sum, page) => sum + page.impressions, 0);
  const pagesReconcile = pageClicks === metrics.clicks && pageImpressions === metrics.impressions;
  const client = await pool.connect();

  try {
    await client.query('BEGIN');
    await client.query(
      'DELETE FROM ontap_shadow.google_job_listing_daily_pages WHERE report_date = $1::date',
      [reportDate]
    );
    await client.query(
      'DELETE FROM ontap_shadow.google_job_listing_daily_totals WHERE report_date = $1::date',
      [reportDate]
    );

    await client.query(
      `INSERT INTO ontap_shadow.google_job_listing_daily_totals
       (report_date, clicks, impressions, page_count, page_clicks_sum, page_impressions_sum, pages_reconcile, fetched_at)
       VALUES ($1::date, $2, $3, $4, $5, $6, $7, $8::timestamptz)`,
      [reportDate, metrics.clicks, metrics.impressions, metrics.pages.length, pageClicks, pageImpressions, pagesReconcile, fetchedAt]
    );

    for (let offset = 0; offset < metrics.pages.length; offset += 500) {
      const batch = metrics.pages.slice(offset, offset + 500);
      const values: unknown[] = [];
      const tuples = batch.map((page, index) => {
        const base = index * 7;
        values.push(reportDate, page.pageUrl, page.clicks, page.impressions, page.ctr, page.averagePosition, fetchedAt);
        return `($${base + 1}::date, $${base + 2}, $${base + 3}, $${base + 4}, $${base + 5}, $${base + 6}, $${base + 7}::timestamptz)`;
      });
      await client.query(
        `INSERT INTO ontap_shadow.google_job_listing_daily_pages
         (report_date, page_url, clicks, impressions, ctr, average_position, fetched_at)
         VALUES ${tuples.join(', ')}`,
        values
      );
    }

    await client.query('COMMIT');
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }

  return { pageClicks, pageImpressions, pagesReconcile };
}

async function reportDates(pool: Pool, manualDate: string | undefined): Promise<string[]> {
  if (manualDate) return [validateDate(manualDate)];

  const settledThrough = addDays(dateInPacific(), -3);
  const latest = await pool.query<{ latest_date: string | null }>(
    'SELECT MAX(report_date)::text AS latest_date FROM ontap_shadow.google_job_listing_daily_totals'
  );
  const previousDate = latest.rows[0]?.latest_date;
  if (!previousDate) return [settledThrough];

  const firstMissing = addDays(previousDate, 1);
  if (firstMissing > settledThrough) return [];

  const dates: string[] = [];
  for (let current = firstMissing; current <= settledThrough; current = addDays(current, 1)) {
    dates.push(current);
  }
  return dates;
}

function appendSummary(text: string) {
  const path = process.env.GITHUB_STEP_SUMMARY;
  if (path) appendFileSync(path, `${text}\n`);
}

async function main() {
  const pool = new Pool({ connectionString: required('ONTAP_NEON_PROD_DAILY_WRITE_URL'), max: 2 });
  try {
    const dates = await reportDates(pool, process.env.GOOGLE_JOB_LISTING_REPORT_DATE?.trim() || undefined);
    if (!dates.length) {
      const message = 'No new settled Pacific date is ready to collect.';
      console.log(message);
      appendSummary(`## Google Job Listing daily check\n\n${message}`);
      return;
    }

    const fetchedAt = new Date().toISOString();
    const results: Array<{
      date: string;
      clicks: number;
      impressions: number;
      pages: number;
      pageClicks: number;
      pageImpressions: number;
      pagesReconcile: boolean;
    }> = [];

    for (const reportDate of dates) {
      const metrics = await fetchDailyMetrics(reportDate);
      const reconciliation = await replaceDailyRows(pool, reportDate, metrics, fetchedAt);
      results.push({
        date: reportDate,
        clicks: metrics.clicks,
        impressions: metrics.impressions,
        pages: metrics.pages.length,
        pageClicks: reconciliation.pageClicks,
        pageImpressions: reconciliation.pageImpressions,
        pagesReconcile: reconciliation.pagesReconcile,
      });
    }

    const cutoff = addDays(dateInPacific(), -RETENTION_DAYS);
    await pool.query(
      'DELETE FROM ontap_shadow.google_job_listing_daily_pages WHERE report_date < $1::date',
      [cutoff]
    );
    await pool.query(
      'DELETE FROM ontap_shadow.google_job_listing_daily_totals WHERE report_date < $1::date',
      [cutoff]
    );

    const markdown = [
      '## Google Job Listing daily check',
      '',
      '| Pacific report date | Job Listing clicks | Impressions | URLs returned | URL click sum | URL impression sum | Reconciles |',
      '|---|---:|---:|---:|---:|---:|---|',
      ...results.map((row) => `| ${row.date} | ${row.clicks} | ${row.impressions} | ${row.pages} | ${row.pageClicks} | ${row.pageImpressions} | ${row.pagesReconcile ? 'Yes' : 'Check'} |`),
      '',
      'Results are stored in the private Production Neon `ontap_shadow` schema for the weekly Google report.',
    ].join('\n');
    console.log(markdown);
    appendSummary(markdown);

    if (results.some((row) => !row.pagesReconcile)) {
      console.warn('Search Console daily page rows did not fully reconcile to the appearance totals; both totals and URL rows were retained for review.');
    }
  } finally {
    await pool.end();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

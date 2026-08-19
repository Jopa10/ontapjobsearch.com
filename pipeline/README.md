# Ontap Pipeline

This directory contains the operational job-ingest, review, composition, reporting and publishing support used by Ontap.

For the canonical architecture, read `/SYSTEM_MAP.md`. For owner-level context, read `/SYSTEM_OVERVIEW.md`. Repository operating rules are in `/AGENTS.md`.

## Live JobG8 path

The primary JobG8 entry point is:

- `.github/workflows/run-full-jobg8-daily-process.yml`

It runs twice daily and performs the current production path:

`JobG8 feed → materialize pipeline/input/jobg8.xlsx → validate → classify/select LIVE slices → compose approved external-source jobs → enrich metadata → write pipeline outputs/reviews/reports → commit generated state`

The active category processing used by that workflow includes:

- `scripts/service_admin_pipeline_north_yorkshire.py`
- `scripts/support_worker_pipeline_live_config.py`
- shared classification/refinement logic under `scripts/`
- category and region authority under `registers/` and `config/`

The old dated monolithic May 2026 JobG8 script is no longer the production entry point and has been removed from the working tree. Git history retains it if historical inspection is ever required.

## Current JobG8 materialization

`pipeline/input/jobg8.xlsx` is the standard current-feed workbook used by pipeline code.

The main daily JobG8 workflow owns the canonical production ingest. External-source workflows that need a fresh JobG8 workbook for dedupe use the shared helper:

- `scripts/materialize_current_jobg8.py`

That helper downloads the current feed with retries, clears stale spreadsheet input files and calls the existing `jobg8_xml_adapter.py` converter with the same expected 5,000–20,000 job safety range.

Do not add another copy of the download/adapter shell sequence to a workflow. Extend the shared materializer instead.

## Daily 33-region family coverage

`.github/workflows/build-daily-region-overview.yml` remains the single recurring owner of `reports-daily/daily-region-overview.md`.

After the normal overview is built, `scripts/assess_daily_family_coverage.py` runs the existing production Service Admin and Support Worker family selectors in a diagnostic-only 33-region mode against the current JobG8 input. It uses `config/job_slice_catalog.json` for the canonical 33-region set and anchor towns, the shared geo lookup, the existing title/refinement registers, salary/context rules and same-day manual decisions.

The diagnostic pass writes `reports-daily/daily-family-coverage.csv` and replaces the NOT LIVE Service Admin / Support Worker cells in the overview with genuine assessed counts, including true zeroes. It does not change `region_category_slice_register.csv`, production output JSON, LIVE publication thresholds, review state or website publishing behaviour. Sales Advisor remains outside this mechanism until its family is formally built.

## External sources

Recurring review workflows currently include:

- NEJobs — `.github/workflows/run-nejobs-review.yml`
- VONNE — `.github/workflows/run-vonne-review.yml`
- Teaching Vacancies regional review — `.github/workflows/run-teaching-vacancies-regional-review.yml`

Approved external jobs are built by their guarded publisher workflows and composed back into the relevant JobG8 regional outputs.

The normal owner-facing publication route is:

`source reviews → pipeline/reviews/daily/ontap-daily-review.md → Apply and publish Ontap daily review → source publishers → Publish verified pages`

`apply-publish-ontap-daily-review.yml` is the orchestration point for applying completed review decisions and dispatching the required guarded publishers.

## Publishing

`publish-verified-pages.yml` is the shared final publisher. It writes the approved live JSON into the website-facing `app/` surfaces, refreshes publish metadata and live-job reporting, and maintains active city-page outputs.

Do not bypass guarded review/publish workflows by manually writing live `app/` JSON unless a separately reviewed recovery procedure explicitly requires it.

## Reviews and reports

The working distinction is:

- `reviews/` — human decision/review surfaces and persistent review state.
- `reports-daily/` — recurring operational reconciliation and live-state reporting.
- `reports/` — other persistent operational reports such as city-opportunity history.
- `reports-module1/`, `reports-module2/`, `reports-module3/` — specialist analysis/compiler outputs.
- `reports-audit/`, `reports-discovery-audit/` — diagnostic/audit outputs; these are not production publishing inputs unless a live workflow explicitly references them.

Do not commit dated failure/recovery observer files into `reports-daily/` as permanent architecture. One-off diagnostics belong in workflow logs/artifacts or Git history unless they become an intentional recurring report.

## Monthly / specialist analysis

Compiler Modules 1–3 are analysis/reporting tools, not live publishing entry points.

- Module 1: advertiser/campaign and role trends.
- Module 2: category/slice validation and supply profiling.
- Module 3: remote/WFH analysis.

Their GitHub Actions workflows are manual/specialist workflows and should remain visibly separate from the small set of recurring production workflows.

## Core data rules

- Never fabricate job data.
- Preserve job descriptions and application URLs.
- Validate input/feed shape before publishing.
- Respect the region/category slice register.
- Treat manual review decisions as controlled state, not ad-hoc second-pass code.
- Preserve approved external-source composition when rebuilding JobG8 output.
- Do not create parallel ingest, classification, review or publish mechanisms when an existing shared mechanism can be extended.

## Before changing the pipeline

1. Read `/AGENTS.md` and the relevant sections of `/SYSTEM_MAP.md`.
2. Identify the existing live workflow/script that owns the responsibility.
3. Prefer extending that mechanism to introducing another workflow or folder.
4. Add or update tests for changed behaviour.
5. Update canonical documentation in the same change when persistent architecture changes.

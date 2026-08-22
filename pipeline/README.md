# Ontap Pipeline

This directory contains the operational job-ingest, review, composition, reporting and publishing support used by Ontap.

For the canonical architecture, read `/SYSTEM_MAP.md`. For owner-level context, read `/SYSTEM_OVERVIEW.md`. Repository operating rules are in `/AGENTS.md`.

## Live JobG8 path

The primary JobG8 entry point is:

- `.github/workflows/run-full-jobg8-daily-process.yml`

It runs twice daily and performs the current production path:

`JobG8 feed → materialize pipeline/input/jobg8.xlsx → validate → classify/select LIVE slices → compose approved external-source jobs → enrich metadata → assess 33-region family coverage → write pipeline outputs/reviews/reports → commit generated state`

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

The 33-region Service Admin / Support Worker diagnostic assessment is now part of `.github/workflows/run-full-jobg8-daily-process.yml`, so it uses the exact same materialized JobG8 workbook as the production family run rather than downloading a later copy of the feed.

`scripts/assess_daily_family_coverage.py` imports the config-driven production family wrappers, reuses persistent JobG8 review decisions, the canonical geo, title/refinement registers, salary/context rules and catalog anchors, then expands those selectors in memory across all 33 canonical overview regions. It writes `reports-daily/daily-family-coverage.csv` only; it does not change the slice register, production family JSON or publishing state.

`.github/workflows/build-daily-region-overview.yml` remains the recurring owner of `reports-daily/daily-region-overview.md`. It no longer downloads JobG8 or reruns the family assessment. Instead it builds the LIVE overview from published state and then applies the already committed same-feed `daily-family-coverage.csv` to the NOT LIVE Service Admin / Support Worker cells. A numeric zero therefore means assessed zero, not unassessed. Sales Advisor remains outside this mechanism until its family is formally built.

## External sources

Recurring review workflows currently include:

- NEJobs — `.github/workflows/run-nejobs-review.yml`
- VONNE — `.github/workflows/run-vonne-review.yml`
- Teaching Vacancies regional/master review — `.github/workflows/run-teaching-vacancies-regional-review.yml`
- NHS Administrative & Clerical — `.github/workflows/refresh-nhs-admin-service-review.yml`

Teaching Vacancies discovery/routing/review state is written back by the regional/master workflow. Its `main` writeback uses full-history checkout plus pull-rebase/push retries so another workflow advancing `main` during the several-minute TV refresh does not strand a successfully generated review as stale.

NHS Jobs is a live Service Admin source. The normal full JobG8 path and the reviewed NHS publisher both use `external_sources/compose_nhs_admin_daily.py`, which refreshes current NHS inventory transactionally, reapplies valid remembered decisions, preserves non-NHS output, enforces the hard 20% regional NHS ceiling and only replaces production state after verification. HC Tier A/B rows may auto-publish when otherwise eligible; untouched NHS POSS rows are optional review opportunities and remain fail-closed.

Approved external jobs are built by their guarded publisher workflows and composed back into the relevant JobG8 regional outputs.

The normal owner-facing publication route is:

`source reviews → pipeline/reviews/daily/ontap-daily-review.md → Apply and publish Ontap daily review → source publishers → Publish verified pages`

If a source is shown as `STALE` or `MISSING`, repair/rerun that source first and then rerun `Ontap daily review` to rebuild the one master edit file. Do not interpret a stale source as zero inventory. Publication remains fail-soft where the previous approved state can safely be retained.

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

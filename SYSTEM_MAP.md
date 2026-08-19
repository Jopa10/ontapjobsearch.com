# Ontap System Map

**Last updated:** 19 August 2026  
**Status:** First architecture audit complete; target shape awaiting owner agreement.

This is the authoritative technical map of the persistent Ontap system. It is organised into five canonical buckets. Facts not verified from the repository are marked `UNKNOWN / NEEDS AUDIT` rather than inferred from chat history.

## Recent canonical changes

- 19 August 2026 — Completed the first architecture audit; verified reviewed-publication orchestration, source publisher paths, website data consumption and the dynamic slice mechanism; proposed a preserve-and-consolidate target shape in `SYSTEM_AUDIT.md`.
- 19 August 2026 — Verified the main scheduled JobG8 path, recurring external-source reviews, daily owner review and Google Indexing API path.
- 19 August 2026 — Created the five-bucket canonical system map and governance framework.

## 1. Pipeline

Purpose: how job data moves from source to published/indexed output.

Canonical stages:

`source → ingest → classify/select → review → approved output → compose → verified publish → app JSON → index`

### Main scheduled JobG8 path

Primary scheduled entry point: `.github/workflows/run-full-jobg8-daily-process.yml`.

It runs at 07:30 and 15:30 Europe/London and performs:

`JobG8 feed → jobg8_xml_adapter.py → pipeline/input/jobg8.xlsx → validation + duplicate report → LIVE slice register → service-admin/support-worker selectors → approved external-source composition → metadata enrichment → pipeline outputs/reports`

The raw validated feed is also archived to S3.

### Review / approved publication path

Owner-facing orchestrator: `.github/workflows/apply-publish-ontap-daily-review.yml`.

It reconciles the master review, requires complete decisions, fans those decisions back to source-owned review files, dispatches source-specific approved publishers sequentially, and invokes `publish-verified-pages.yml` when the shared final publish is required.

Confirmed source publisher paths include:

- JobG8 — `apply-jobg8-review-decisions.yml`, restoring the exact reviewed archived feed before rebuilding approved outputs;
- NEJobs — `build-approved-nejobs-output.yml`;
- VONNE — `build-approved-vonne-output.yml`;
- Teaching Vacancies — regional approved publisher(s), including `build-approved-teaching-vacancies-regional.yml`.

`publish-verified-pages.yml` is the final bridge from reviewed/composed pipeline outputs into user-facing `app/**.json`, live-job reports and city-page outputs.

### External-source review paths

Recurring review workflows:

- NEJobs — 06:15 daily;
- VONNE — 06:35 daily;
- Teaching Vacancies regional/master review — 06:55 daily.

NEJobs and VONNE still duplicate JobG8 download/workbook materialisation for dedupe. Consolidating this into one shared mechanism is a confirmed refactor goal.

### Core supporting areas

- `pipeline/config/`
- `pipeline/geo/`
- `pipeline/input/`
- `pipeline/scripts/`
- `pipeline/tests/`
- `pipeline/registers/`
- `pipeline/external_sources/`
- `pipeline/output-admin-service/`
- `pipeline/output-support-worker/`
- `pipeline/output-external/`
- `pipeline/reviews/`
- `pipeline/manifests/`
- `pipeline/city_pages/`

### Known superseded/stale candidates

- `pipeline/jobg8_pipeline_v7_working_2026-05-06.py` is not used by the verified main scheduled path and is a strong archive/removal candidate after final reference checks.
- `pipeline/README.md` is stale because it still presents that May script as the current stable pipeline.
- standalone manual category workflows overlap substantially with the current full/reviewed pipeline and are refactor candidates, not current canonical entry points.

## 2. Reports / diagnostics

Purpose: persistent outputs used to reconcile, inspect or monitor Ontap.

### Operational reports

- `pipeline/reviews/daily/ontap-daily-review.md` — master owner review, generated daily at 08:45 Europe/London and emailed.
- `pipeline/reports-daily/` — routine production/reconciliation reports and ledgers.
- `build-daily-region-overview.yml` refreshes `pipeline/reports-daily/daily-region-overview.md` after a successful verified publish.

### Specialist analysis

Compiler Modules 1, 2 and 3 are legitimate manual/analytical workflows and should remain conceptually separate from day-to-day production operations.

### Target reporting lifecycle

Future cleanup should distinguish:

- operational daily reports;
- deliberate specialist analysis;
- archived/one-off diagnostics.

Exact folder moves are not yet implemented.

## 3. Website / UX

Purpose: user-facing job search, job pages, navigation and presentation.

Verified structure:

- `app/` is the primary application route/data tree.
- `components/` contains reusable UI components.
- `lib/published-jobs.ts` reads published JSON from `app/`, normalises jobs, dedupes by `job_id`, and supplies the published job/search/detail layer.
- `lib/configured-job-slices.ts` reads `pipeline/config/job_slice_catalog.json` and `pipeline/registers/region_category_slice_register.csv`.
- LIVE dynamic region/category slices are therefore register/catalog driven.
- dynamic configured slice data lives under `app/_city-pages/configured-slices/`.
- `app/job-search/[region]/...` is the dynamic route family.

The existing dynamic/register-driven slice mechanism is the preferred path for future region/category expansion. Older static routes must not be removed casually because SEO/user-facing dependencies still need explicit checks during refactor.

## 4. Content / positioning

Purpose: persistent editorial, guidance and positioning structures implemented in the product/repository.

No content-architecture refactor is recommended from this audit. Persistent product content belongs here when it affects product behaviour; temporary social/campaign copy does not.

## 5. Operations / infrastructure

Purpose: workflows, scheduling, deployment, alerts, indexing integrations and persistent environment/configuration mechanisms.

### Core scheduled workflows

- `run-full-jobg8-daily-process.yml` — 07:30 and 15:30 Europe/London.
- `run-nejobs-review.yml` — 06:15 daily.
- `run-vonne-review.yml` — 06:35 daily.
- `run-teaching-vacancies-regional-review.yml` — 06:55 daily.
- `ontap-daily-review.yml` — 08:45 Europe/London daily.
- `google-indexing-api.yml` — 19:30 daily.

### Owner-triggered publication

The canonical owner-facing publication entry point is `apply-publish-ontap-daily-review.yml`; source-specific publishers are implementation details behind that orchestration where possible.

### Google Indexing API

`google-indexing-api.yml`:

- submits eligible job URLs through Google's Indexing API;
- caps each run at 200 notifications;
- persists confirmed submission state in `pipeline/manifests/google-indexing-state.json`;
- raises/updates a GitHub Issue when backlog/safety-limit/failure conditions require attention;
- closes that alert after a healthy live run clears the condition.

### Workflow hygiene

Dated fix/recovery/observer workflows from 19 August are strong archive/removal candidates. Branch-specific test/experimental workflows must remain clearly separated from production workflows until promoted or removed.

Compiler Modules and review-only experiments are analysis/testing tools, not primary production controls.

## Agreed-target decision still required

`SYSTEM_AUDIT.md` contains the proposed target shape and recommended refactor order. No cleanup/refactor should begin until that target is reviewed and agreed.

## Documentation rule

When a persistent system-level change alters any of these five buckets, update the affected section of this file in the same change. If live/active/user-facing state changes, update `SYSTEM_OVERVIEW.md` as well.
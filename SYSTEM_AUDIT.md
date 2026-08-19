# Ontap System Audit

**Audit started:** 19 August 2026  
**Status:** First architecture audit complete; agreed cleanup 1–5 merged into `main` via PR #211.

The audit conclusion remains: **preserve the working core; remove historical scaffolding; consolidate duplicated mechanics; do not refactor for technical tidiness alone.**

## Business-priority constraint

Business priority wins over technical neatness. Website routes and public URLs are out of scope for this cleanup unless there is evidence that they materially harm indexing/discoverability, AI discoverability, user experience, reliability or inventory expansion.

## Verified core architecture

### Scheduled source refresh

- `run-full-jobg8-daily-process.yml` — primary JobG8 production entry point, twice daily.
- `run-nejobs-review.yml` — daily NEJobs review refresh.
- `run-vonne-review.yml` — daily VONNE review refresh.
- `run-teaching-vacancies-regional-review.yml` — daily Teaching Vacancies review refresh.
- `ontap-daily-review.yml` — builds/emails the master owner review.

### Reviewed publication

- `apply-publish-ontap-daily-review.yml` — owner-facing orchestration point.
- `apply-jobg8-review-decisions.yml` — exact reviewed JobG8 replay/apply path.
- source-specific approved publishers — NEJobs, VONNE and Teaching Vacancies.
- `publish-verified-pages.yml` — final shared bridge into live `app/**.json`, live-job reporting and city-page outputs.

### Indexing / monitoring

- `google-indexing-api.yml` — daily Google Indexing API submission, 200-notification cap, persistent submission state and GitHub Issue alerting.
- `build-daily-region-overview.yml` — post-publish regional operational overview.

## Agreed cleanup 1–5

### 1. Workflow hygiene — merged

Removed confirmed one-shot/delivery-specific workflows from the working tree:

- `fix-2026-08-19-review-pipeline.yml`
- `fix-2026-08-19-review-pipeline-v2.yml`
- `recover-2026-08-19-review.yml`
- `observe-2026-08-19-recovery.yml`
- `observe-nejobs-failure-2026-08-19.yml`
- `generate-teaching-vacancies-master-review-once.yml`
- `run-module2-post-expansion-now.yml`

These were explicitly dated/self-triggering/one-time mechanisms. Git history retains them if historical inspection is ever needed.

### 2. Documentation fix — merged

`pipeline/README.md` has been rewritten around the actual current operating model and now points to the canonical governance files. It no longer describes the dated May monolithic script as the current stable pipeline.

### 3. Shared current JobG8 materialisation — merged

Added:

- `pipeline/scripts/materialize_current_jobg8.py`
- `pipeline/tests/test_materialize_current_jobg8.py`

NEJobs and VONNE review/publish workflows now call that shared helper rather than each carrying a separate download + clear-input + XML-adapter block.

The main JobG8 production workflow remains the canonical production ingest owner. This cleanup deliberately reduces duplicated external-source materialisation without rewriting the working main ingest path.

### 4. Superseded standalone paths — merged

Removed after reference checks:

- `.github/workflows/run-service-admin-pipeline.yml`
- `.github/workflows/run-support-worker-pipeline.yml`
- `pipeline/jobg8_pipeline_v7_working_2026-05-06.py`

The current full/reviewed JobG8 workflows remain the canonical category-processing paths. Tests that previously asserted the old standalone service-admin workflow now assert the canonical daily workflow instead.

### 5. Report lifecycle cleanup — merged conservatively

Removed confirmed dated one-off diagnostic files from `pipeline/reports-daily/`:

- `recovery-2026-08-19-observer.txt`
- `recovery-2026-08-19-status.txt`
- `nejobs-failure-2026-08-19.txt`

Added `pipeline/reports/README.md` and updated `pipeline/README.md` to distinguish:

- recurring operational reports;
- deliberate specialist analysis;
- one-off diagnostics, which should normally live in Actions logs/artifacts or Git history.

No broad folder moves were made where a live reference could be broken merely for neatness.

## Website / UX

No website route cleanup is part of this refactor. Existing static and dynamic public routes remain untouched.

The verified scalable mechanism for future expansion remains:

- `pipeline/config/job_slice_catalog.json`
- `pipeline/registers/region_category_slice_register.csv`
- `lib/configured-job-slices.ts`
- dynamic `/job-search/[region]/...` routes
- configured data under `app/_city-pages/configured-slices/`

That does **not** create a business case for changing established routes by itself.

## Merge state

Architecture cleanup 1–5 was merged into `main` via PR #211 on 19 August 2026. The audit should therefore be read against the cleaned architecture now present on `main`, not against the former feature branch state.

## Current production repository state

The cleanup changes are now part of `main`. The merged PR was deliberately scoped away from website/public-route changes, live job JSON changes, selection-rule rewrites and Google Indexing API changes.

# Ontap System Map

**Last updated:** 19 August 2026  
**Status:** First architecture audit complete; agreed cleanup 1–5 merged into `main` via PR #211.

This is the authoritative technical map of the persistent Ontap system. It is organised into five canonical buckets. Facts not verified from the repository are marked `UNKNOWN / NEEDS AUDIT` rather than inferred from chat history.

## Recent canonical changes

- 19 August 2026 — Added publication failure isolation: up to 15 unresolved/malformed jobs per source are withheld fail-closed while clean jobs continue; larger clusters isolate that source, and source publisher failures retain the last approved state rather than blocking unrelated inventory.
- 19 August 2026 — Made NEJobs fail-soft in the owner publish orchestrator: an NEJobs publisher failure now retains the last approved NEJobs snapshot, records a warning, and allows other clean sources plus the final verified-page publish to continue.
- 19 August 2026 — Documented owner review timing: the 15:30 JobG8 refresh does not rebuild `ontap-daily-review.md`; an afternoon review requires a manual run of `Ontap daily review` after the PM refresh.
- 19 August 2026 — Clarified JobG8 feed storage: `pipeline/input/jobg8.xlsx` is a transient workflow input and is not committed to GitHub; the validated raw feed is retained durably in S3 under `jobg8/raw`.
- 19 August 2026 — Corrected Google Indexing API schedule documentation: the workflow cron is 19:30 UTC, which is 20:30 BST in summer and 19:30 GMT in winter.
- 19 August 2026 — Merged architecture cleanup 1–5 into `main` via PR #211; this cleaned architecture is now the canonical repository state.
- 19 August 2026 — Implemented the agreed architecture cleanup on `chore/architecture-cleanup-1-5`: removed proven one-off workflows, replaced stale pipeline documentation, introduced a shared current-JobG8 materializer for external-source dedupe, retired superseded standalone category workflows/old monolithic script, and removed dated one-off diagnostics.
- 19 August 2026 — Added the business-priority rule: no refactor for technical tidiness alone; website/public-route changes require a concrete business case such as discoverability, indexing, UX, reliability or expansion benefit.
- 19 August 2026 — Completed the first architecture audit and verified the main JobG8, master review/publish, external-source and indexing paths.

## 1. Pipeline

Purpose: how job data moves from source to published/indexed output.

Canonical stages:

`source → ingest → classify/select → review → approved output → compose → verified publish → app JSON → index`

### Main scheduled JobG8 path

Primary scheduled entry point: `.github/workflows/run-full-jobg8-daily-process.yml`.

It runs at 07:30 and 15:30 Europe/London and performs:

`JobG8 feed → pipeline/input/jobg8.xlsx → validation + duplicate report → LIVE slice register → service-admin/support-worker selectors → approved external-source composition → metadata enrichment → pipeline outputs/reports`

`pipeline/input/jobg8.xlsx` is created for the workflow run after the current JobG8 ZIP is downloaded and converted. It is a transient processing input and is not committed to GitHub. The validated raw feed is archived durably to S3 under `jobg8/raw`.

The main daily workflow remains the canonical production ingest owner.

### Owner review timing

`ontap-daily-review.yml` builds `pipeline/reviews/daily/ontap-daily-review.md` automatically at 08:45 Europe/London. The 15:30 JobG8 refresh updates the underlying JobG8 pipeline state but does **not** rebuild the master review file.

Operational rule:

- if the owner reviews the 08:45 file in the morning, no second review is required after the 15:30 JobG8 refresh; the next normal review is the following morning;
- if the owner chooses to review the freshest afternoon inventory, wait for the 15:30 JobG8 run and its automatic Quick View refresh to finish successfully, then manually run the workflow named `Ontap daily review` before editing `ontap-daily-review.md`.

### Shared current-feed materialization for external dedupe

External-source workflows that need a fresh JobG8 workbook for dedupe use:

- `pipeline/scripts/materialize_current_jobg8.py`
- `pipeline/tests/test_materialize_current_jobg8.py`

That helper centralises the repeated current-feed download, stale-input cleanup and `jobg8_xml_adapter.py` conversion used by NEJobs and VONNE review/publish workflows.

### Review / approved publication path

Owner-facing orchestrator: `.github/workflows/apply-publish-ontap-daily-review.yml`.

It reconciles the master review, fans valid decisions back to source-owned review files, dispatches source-specific approved publishers sequentially, and invokes `publish-verified-pages.yml` when the shared final publish is required.

Publication isolation is hierarchical:

- up to 15 unresolved or malformed review-action jobs in one source are withheld fail-closed and flagged while the clean jobs from that source continue;
- more than 15 such jobs, or a source-level integrity mismatch, isolates that source from the current run and retains its previous approved state;
- any source publisher failure is fail-soft at the owner orchestrator: the source keeps its last approved state and other clean sources continue;
- only a genuine system-level integrity failure, such as failure of the final shared verified-page publication boundary, should stop the whole owner publish.

A malformed action such as a misspelt `exclude` is therefore treated as a withheld job rather than a reason to abort publication of otherwise clean inventory. The review-hub publish plan records quarantined jobs and isolated sources in the workflow summary.

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

### Retired from the working tree in the agreed cleanup

- `pipeline/jobg8_pipeline_v7_working_2026-05-06.py`
- `.github/workflows/run-service-admin-pipeline.yml`
- `.github/workflows/run-support-worker-pipeline.yml`

Git history retains these historical implementations.

## 2. Reports / diagnostics

Purpose: persistent outputs used to reconcile, inspect or monitor Ontap.

### Operational reports

- `pipeline/reviews/daily/ontap-daily-review.md` — master owner review, generated daily and emailed.
- `pipeline/reports-daily/` — routine production/reconciliation reports and ledgers.
- `build-daily-region-overview.yml` refreshes `pipeline/reports-daily/daily-region-overview.md` after a successful verified publish.

### Specialist analysis

Compiler Modules 1, 2 and 3 are legitimate manual/analytical workflows and remain conceptually separate from day-to-day production operations.

### Report lifecycle rule

`pipeline/reports/README.md` documents three lifecycles:

- recurring operational reporting;
- deliberate specialist analysis;
- one-off diagnostics, which should normally remain in Actions logs/artifacts or Git history.

Confirmed dated recovery/failure observer reports from 19 August have been removed from the working report tree. Broad folder moves were deliberately avoided where they could break live references merely for neatness.

## 3. Website / UX

Purpose: user-facing job search, job pages, navigation and presentation.

Verified structure:

- `app/` is the primary application route/data tree.
- `components/` contains reusable UI components.
- `lib/published-jobs.ts` reads published JSON from `app/`, normalises jobs, dedupes by `job_id`, and supplies the published job/search/detail layer.
- `lib/configured-job-slices.ts` reads `pipeline/config/job_slice_catalog.json` and `pipeline/registers/region_category_slice_register.csv`.
- LIVE dynamic region/category slices are register/catalog driven.
- dynamic configured slice data lives under `app/_city-pages/configured-slices/`.
- `app/job-search/[region]/...` is the dynamic route family.

### Website refactor rule

Website routes/public URLs are not a technical-tidiness target. They stay stable unless a specific defect or evidence shows a material benefit in indexing/discoverability, AI discoverability, user experience, reliability or inventory expansion. Existing URLs/SEO behaviour must be preserved unless changing them is itself the intended business improvement.

## 4. Content / positioning

Purpose: persistent editorial, guidance and positioning structures implemented in the product/repository.

No content-architecture refactor is part of this cleanup. Persistent product content belongs here when it affects product behaviour; temporary social/campaign copy does not.

## 5. Operations / infrastructure

Purpose: workflows, scheduling, deployment, alerts, indexing integrations and persistent environment/configuration mechanisms.

### Core scheduled workflows

- `run-full-jobg8-daily-process.yml` — 07:30 and 15:30 Europe/London.
- `run-nejobs-review.yml` — 06:15 daily.
- `run-vonne-review.yml` — 06:35 daily.
- `run-teaching-vacancies-regional-review.yml` — 06:55 daily.
- `ontap-daily-review.yml` — 08:45 Europe/London daily owner review; run manually after the 15:30 refresh when an afternoon review of the freshest inventory is wanted.
- `google-indexing-api.yml` — cron 19:30 UTC daily (20:30 BST in summer; 19:30 GMT in winter).

### Owner-triggered publication

The canonical owner-facing publication entry point is `apply-publish-ontap-daily-review.yml`; source-specific publishers are implementation details behind that orchestration where possible.

The owner-facing publish gate is fail-soft by default at job and source level. Up to 15 bad/unresolved jobs in one source are withheld and flagged while clean jobs continue; larger source problems leave that source's previous approved state in place and do not abort publication of unrelated clean inventory. A final combined/publication integrity failure remains blocking.

### Google Indexing API

`google-indexing-api.yml`:

- submits eligible job URLs through Google's Indexing API;
- caps each run at 200 notifications;
- persists confirmed submission state in `pipeline/manifests/google-indexing-state.json`;
- raises/updates a GitHub Issue when backlog/safety-limit/failure conditions require attention;
- closes that alert after a healthy live run clears the condition.

### Workflow hygiene

The merged cleanup removes proven one-shot/delivery-specific workflows including dated 19 August fix/recovery/observer jobs, the self-described one-time Teaching Vacancies master-review generator and the `run-module2-post-expansion-now.yml` helper.

Branch-specific experiments and specialist compiler/review tools remain separate from the canonical production controls unless there is evidence they are obsolete.

## Validation state

Architecture cleanup 1–5 was merged into `main` via PR #211 on 19 August 2026. It is no longer isolated on `chore/architecture-cleanup-1-5`; future repository analysis should treat the cleaned architecture as the canonical current state.

## Documentation rule

When a persistent system-level change alters any of these five buckets, update the affected section of this file in the same change. If live/active/user-facing state changes, update `SYSTEM_OVERVIEW.md` as well.

# Ontap System Audit

**Audit started:** 19 August 2026  
**Status:** In progress — evidence-based classification only; no refactor or deletion yet.

This audit classifies persistent repository components as `LIVE`, `SUPPORTING`, `OLD / CANDIDATE FOR REMOVAL`, or `UNKNOWN / NEEDS AUDIT`. A component is not removed merely because it looks old; removal requires evidence that no live workflow/runtime path depends on it.

## Immediate findings

1. The repo has a real architecture-bloat problem, especially around pipeline/report/workflow areas.
2. There is already a credible live daily JobG8 entry point: `.github/workflows/run-full-jobg8-daily-process.yml`.
3. The old `pipeline/README.md` is stale enough to be unsafe as a source of truth: it still calls `jobg8_pipeline_v7_working_2026-05-06.py` the current stable version, while the live scheduled workflow uses newer modular scripts.
4. Several external-source review workflows independently redownload and rebuild the JobG8 feed for dedupe. This is duplicated operational behaviour and a consolidation candidate, not yet a deletion candidate.
5. Reports are spread across multiple folders (`reports`, `reports-audit`, `reports-daily`, `reports-discovery-audit`, `reports-module1`, `reports-module2`, etc.). Their ownership/lifecycle is not obvious from folder names alone.
6. `.github/workflows/` contains permanent-looking workflows mixed with test, fix, recovery, observer and one-off workflows. This materially increases the chance of confusion about what is live.

## 1. Pipeline

### LIVE — confirmed

- `.github/workflows/run-full-jobg8-daily-process.yml`
  - scheduled twice daily at 07:30 and 15:30 Europe/London;
  - downloads the JobG8 feed;
  - converts it to `pipeline/input/jobg8.xlsx`;
  - validates feed health;
  - reports potential duplicates;
  - archives the raw feed to S3;
  - reads live slices from the slice register;
  - runs service-admin and support-worker processing where enabled;
  - reattaches approved external-source vacancies;
  - enriches metadata;
  - refreshes review/exclusion outputs;
  - commits generated outputs/reports back to `main`.

### SUPPORTING — confirmed by live workflow references

- `pipeline/input/`
- `pipeline/scripts/`
- `pipeline/tests/`
- `pipeline/registers/`
- `pipeline/output-admin-service/`
- `pipeline/output-support-worker/`
- `pipeline/reports-daily/`
- `pipeline/reviews/`
- `pipeline/external_sources/`
- `pipeline/manifests/`

### OLD / CANDIDATE FOR REMOVAL — not yet safe to remove

- `pipeline/jobg8_pipeline_v7_working_2026-05-06.py`
  - old README still labels it current stable;
  - the confirmed live scheduled JobG8 workflow does not use it;
  - must search all remaining workflows/scripts/docs before final classification.

### STRUCTURAL CONCERN

The pipeline currently mixes source ingestion, review generation, operational reports, generated outputs, test utilities, manifests and historical/diagnostic material under one broad `pipeline/` tree. The final refactor should make active runtime paths visually obvious and move historical/one-off material out of the working path.

## 2. Reports / diagnostics

### LIVE — confirmed

- `pipeline/reviews/daily/ontap-daily-review.md`
  - generated daily by `.github/workflows/ontap-daily-review.yml` at 08:45 Europe/London;
  - emailed through configured SMTP secrets.
- `pipeline/reports-daily/`
  - receives JobG8 daily decision, validation, selection and duplicate-report outputs from the main JobG8 workflow.

### SUPPORTING / SPECIALIST — confirmed in repo, lifecycle still being classified

- `pipeline/reports-audit/`
- `pipeline/reports-discovery-audit/`
- `pipeline/reports-module1/`
- `pipeline/reports-module2/`
- `pipeline/reports/`

The existence of several parallel report directories is itself a design smell. Next audit pass must classify which are recurring products, which are temporary diagnostics, and which can be collapsed or archived.

## 3. Website / UX

### LIVE / SUPPORTING — confirmed structure

- `app/` is the main application route tree.
- `components/` contains reusable UI components.
- `app/` contains both broad product routes and many region/city-specific route directories, including `_city-pages`, `browse-jobs`, `job-search`, and region/city routes.

### STRUCTURAL CONCERN

The application tree includes generated/region-specific structure alongside core product routes. The next pass must establish which routes are templates/data-driven versus independently maintained copies before any consolidation decision.

## 4. Content / positioning

### UNKNOWN / NEEDS AUDIT

No structural conclusion yet. Persistent page copy/content will be mapped only where it affects product architecture. External social content will not be treated as repo system architecture.

## 5. Operations / infrastructure

### LIVE — scheduled workflows confirmed

- `run-full-jobg8-daily-process.yml` — 07:30 and 15:30 Europe/London.
- `run-nejobs-review.yml` — 06:15 daily.
- `run-vonne-review.yml` — 06:35 daily.
- `run-teaching-vacancies-regional-review.yml` — 06:55 daily.
- `ontap-daily-review.yml` — 08:45 Europe/London daily.
- `google-indexing-api.yml` — 19:30 daily.

### LIVE indexing behaviour — confirmed

`google-indexing-api.yml`:
- submits eligible job URLs through Google's Indexing API;
- caps notifications at 200 per run;
- persists confirmed submission state in `pipeline/manifests/google-indexing-state.json`;
- raises/updates a GitHub Issue when a backlog, safety-limit condition or failure needs attention;
- closes the alert after a healthy live run clears the condition.

### DUPLICATION / CONSOLIDATION CANDIDATE

`run-nejobs-review.yml` and `run-vonne-review.yml` each independently:
- download the JobG8 feed;
- clear/rebuild `pipeline/input/jobg8.xlsx`;
- use that temporary workbook for dedupe.

This is repeated source-ingest behaviour outside the main JobG8 pipeline and should be reviewed for consolidation into one shared mechanism.

### WORKFLOW BLOAT — confirmed

`.github/workflows/` contains permanent workflows mixed with files whose names indicate temporary purpose, including `test-*`, `fix-*`, `recover-*`, `observe-*`, proof-of-concept and one-off generation workflows. None will be deleted until trigger/reference/history checks confirm they are not required, but they should not remain mixed indefinitely with the small set of live operational workflows.

## Next audit pass

1. Build the complete workflow inventory and classify every `.github/workflows/*.yml` file.
2. Trace every workflow to the scripts/folders it calls.
3. Classify all `pipeline/` top-level folders as live/supporting/old/unknown.
4. Identify duplicate ingest, dedupe, review and publish mechanisms.
5. Trace website data consumption from pipeline outputs into `app/`/`lib/`.
6. Produce a proposed target structure before deleting or moving anything.

## Safety rule

No file/folder/workflow is to be deleted, renamed, moved or refactored during the audit phase unless a separate explicit change is approved. The audit records evidence; the refactor comes only after the target structure is agreed.

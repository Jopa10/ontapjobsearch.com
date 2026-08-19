# Ontap System Audit

**Audit started:** 19 August 2026  
**Status:** First architecture audit complete; target structure proposed; no refactor or deletion has been performed.

This audit classifies persistent repository components as `LIVE`, `SUPPORTING`, `OLD / CANDIDATE FOR REMOVAL`, or `UNKNOWN / NEEDS AUDIT`. A component is not removed merely because it looks old; removal still requires a focused dependency/history check during the refactor step.

## Executive conclusion

The core system is more coherent than the repository layout makes it appear. The main problem is not that Ontap needs a new pipeline. The problem is accumulated scaffolding around a working core: overlapping manual workflows, one-off recovery/test workflows, duplicated JobG8 ingest for external-source dedupe, several report locations, and stale documentation.

Recommended direction: **preserve the working core, make the true entry points obvious, consolidate shared mechanics, and archive/remove historical scaffolding only after focused dependency checks.**

## 1. Pipeline

### LIVE — primary production path

- `.github/workflows/run-full-jobg8-daily-process.yml`
  - scheduled twice daily at 07:30 and 15:30 Europe/London;
  - downloads the JobG8 feed;
  - converts it to `pipeline/input/jobg8.xlsx`;
  - validates feed health;
  - reports potential duplicates;
  - archives the raw feed to S3;
  - reads LIVE slices from `pipeline/registers/region_category_slice_register.csv` through shared slice-registry logic;
  - runs service-admin and support-worker processing where enabled;
  - composes approved external-source vacancies;
  - enriches metadata;
  - writes category outputs and daily reports.

### LIVE — reviewed publication path

- `.github/workflows/apply-publish-ontap-daily-review.yml` is the main reviewed-publication orchestrator.
  - reconciles the single master daily review;
  - requires complete review decisions;
  - fans decisions back to source-owned review files;
  - dispatches current source publishers sequentially;
  - dispatches `publish-verified-pages.yml` when shared publication is required.
- `.github/workflows/apply-jobg8-review-decisions.yml` restores the exact reviewed JobG8 archive by feed date, reruns the current selectors/composition and commits reviewed outputs.
- Approved external-source publisher workflows include:
  - `build-approved-nejobs-output.yml`;
  - `build-approved-vonne-output.yml`;
  - `build-approved-teaching-vacancies-regional.yml`.
- `publish-verified-pages.yml` is the final shared publisher from pipeline outputs into user-facing `app/**.json`, and also refreshes live-job reports and city-page outputs.

### LIVE — external-source review paths

- `run-nejobs-review.yml` — daily 06:15.
- `run-vonne-review.yml` — daily 06:35.
- `run-teaching-vacancies-regional-review.yml` — daily 06:55.

### SUPPORTING — confirmed

- `pipeline/config/` — includes the job-slice catalog used by dynamic website slices.
- `pipeline/geo/` — geography lookup support.
- `pipeline/input/` — current working JobG8 workbook.
- `pipeline/scripts/` — current modular processing/publishing/reporting code.
- `pipeline/tests/` — safeguards used by live/manual workflows.
- `pipeline/registers/` — category and region/category authority registers.
- `pipeline/external_sources/` — NEJobs, VONNE and Teaching Vacancies source/review/composition code.
- `pipeline/output-admin-service/`, `pipeline/output-support-worker/`, `pipeline/output-external/` — intermediate approved/composed outputs.
- `pipeline/reviews/` — source and master review surfaces.
- `pipeline/manifests/` — persistent state/evidence including Google indexing state and external-source evidence.
- `pipeline/city_pages/` — approved city-page lifecycle state.

### SPECIALIST / ANALYSIS — keep, but separate conceptually from production

- Compiler Module 1 — advertiser/campaign and role-trend reporting.
- Compiler Module 2 — category/supply validation and live-slice analysis.
- Compiler Module 3 — remote/WFH analysis.
- Their corresponding report folders are legitimate analysis outputs, but should not be visually mixed with day-to-day production reporting.

### OLD / STRONG CANDIDATES FOR ARCHIVE OR REMOVAL

- `pipeline/jobg8_pipeline_v7_working_2026-05-06.py` — stale monolithic predecessor; not used by the verified main JobG8 scheduled workflow.
- `pipeline/README.md` is currently unsafe as operational documentation because it still identifies that May script as the current stable pipeline.
- `.github/workflows/run-service-admin-pipeline.yml` — older standalone manual route overlapping the full JobG8 process.
- `.github/workflows/run-support-worker-pipeline.yml` — older standalone manual route overlapping the full JobG8 process and even calls a different support-worker entry point from the current live full process.

These are candidates, not yet deletion approvals.

### VERIFIED DUPLICATION

NEJobs and VONNE review/publish workflows independently download the current JobG8 feed, clear/rebuild `pipeline/input/jobg8.xlsx`, and use that workbook for dedupe. This shared concern should become one reusable mechanism rather than repeated workflow code.

## 2. Reports / diagnostics

### LIVE recurring reports

- `pipeline/reviews/daily/ontap-daily-review.md` — single daily owner review, built by `ontap-daily-review.yml` and emailed.
- `pipeline/reports-daily/` — production decision/validation/selection outputs, potential-duplicate report, live-job source counts/history, newly-published ledger and daily regional overview.
- `build-daily-region-overview.yml` automatically runs after a successful `Publish verified pages` workflow and writes `pipeline/reports-daily/daily-region-overview.md`.

### SPECIALIST analysis reports

- `pipeline/reports-module1/`
- `pipeline/reports-module2/`
- `pipeline/reports-module3/`

### AUDIT / TEMPORARY report areas

- `pipeline/reports-audit/`
- `pipeline/reports-discovery-audit/`
- other report folders/items not referenced by a persistent production path remain archive/consolidation candidates rather than production entry points.

### Recommended reporting shape

Do not merge every report into one undifferentiated folder. Use three clear lifecycles:

1. `daily/` — persistent operational reports used routinely;
2. `analysis/` — deliberate specialist/module analysis;
3. `archive/` or GitHub artifacts — historical/one-off diagnostics that do not belong in the working operational surface.

Exact physical moves should be decided during refactor to avoid breaking references.

## 3. Website / UX

### LIVE data model — verified

- `app/` is the Next.js application route/data tree.
- `components/` contains reusable UI.
- `lib/published-jobs.ts` reads published job JSON from `app/`, normalises/dedupes jobs by `job_id`, and supplies the job-detail/search layer.
- `lib/configured-job-slices.ts` reads:
  - `pipeline/config/job_slice_catalog.json`;
  - `pipeline/registers/region_category_slice_register.csv`.
- LIVE dynamic slices are therefore register/catalog driven rather than requiring a bespoke route per new region/category.
- Dynamic configured slice data lives under `app/_city-pages/configured-slices/`.
- `app/job-search/[region]/...` provides the dynamic job-search route family.
- `publish-verified-pages.yml` is the verified bridge from reviewed pipeline outputs into user-facing `app/**.json` and city-page data.

### Structural conclusion

The website already contains the beginnings of the right scalable architecture: dynamic configured slices alongside older/static region routes. The refactor should favour the dynamic/register-driven mechanism for future expansion, while preserving existing static routes until redirects/SEO/data behaviour are deliberately assessed.

## 4. Content / positioning

No architecture problem identified that justifies a refactor in this pass. Persistent product copy belongs in the website/content layer when it affects product behaviour; temporary campaign/social copy does not belong in the system architecture record.

## 5. Operations / infrastructure

### CORE live/supported workflow families

**Scheduled/source refresh**
- `run-full-jobg8-daily-process.yml`
- `run-nejobs-review.yml`
- `run-vonne-review.yml`
- `run-teaching-vacancies-regional-review.yml`
- `ontap-daily-review.yml`
- `google-indexing-api.yml`

**Reviewed publication / owner-triggered**
- `apply-publish-ontap-daily-review.yml`
- `apply-jobg8-review-decisions.yml`
- approved NEJobs/VONNE/Teaching Vacancies publishers
- `publish-verified-pages.yml`
- `apply-city-page-approvals.yml`

**Reporting/analysis**
- `build-daily-region-overview.yml`
- Compiler Modules 1/2/3
- `build-at-a-glance-review.yml` is review-only/experimental tooling, not a production publisher.

### STRONG ARCHIVE/REMOVAL CANDIDATES

One-shot 19 August repair/observation workflows such as:
- `fix-2026-08-19-review-pipeline.yml`;
- `fix-2026-08-19-review-pipeline-v2.yml`;
- `recover-2026-08-19-review.yml`;
- `observe-2026-08-19-recovery.yml`.

Their triggers are tied to pushes of their own workflow files and their purpose is explicitly dated recovery/observation. They should not remain mixed indefinitely with operational workflows.

Branch-specific/test workflows such as `build-customer-sales-test-slices.yml` should remain clearly isolated as experiments until promoted or removed; they are not part of the current `main` production publication path.

### Google Indexing API — LIVE

`google-indexing-api.yml`:
- runs daily at 19:30;
- caps submissions at 200 notifications per run;
- persists confirmed state in `pipeline/manifests/google-indexing-state.json`;
- raises/updates a GitHub Issue for backlog/safety-limit/failure conditions;
- closes that alert after a healthy live run clears the condition.

## Proposed target shape

This is the recommended shape to agree before refactoring. It is a **logical structure first**; exact folder moves come second.

### A. Four obvious operational entry points

1. **Refresh sources** — scheduled JobG8 + external-source review refreshes.
2. **Review** — one master Ontap daily review.
3. **Apply / publish** — one owner-facing reviewed-publication orchestrator, with source-specific publishers hidden behind it.
4. **Index / monitor** — Google indexing plus operational reporting/alerts.

The owner should not normally need to choose among a large list of source-specific workflows.

### B. One shared JobG8 materialisation mechanism

JobG8 download/archive/restore/workbook materialisation should be reusable by:
- main JobG8 refresh;
- external-source dedupe;
- reviewed replay;
- monthly analysis.

Do not let each workflow carry its own copy of that machinery.

### C. Preserve pipeline contracts

Keep the clear logical boundaries:

`source → reviewable state → reviewed/approved output → composed category output → verified publish → app JSON → website/search/indexing`

Refactor around those contracts rather than rewriting working selection logic.

### D. Separate operational from analytical workflows

Operational Actions should be easy to recognise. Compiler modules, experiments, audits and one-offs should be grouped/named/archived so they cannot be mistaken for daily production controls.

### E. Dynamic slices are the forward path

For new region/category expansion, prefer the catalog + slice register + dynamic route/data mechanism rather than adding new bespoke page/workflow structures unless a genuine exception requires it.

## Recommended refactor order

1. **Workflow hygiene first** — archive/remove proven one-shot repair workflows and clearly separate production/manual-analysis/test workflows.
2. **Documentation fix** — replace or rewrite stale `pipeline/README.md` so it points at the canonical system map and current entry points.
3. **Shared JobG8 materialisation** — remove duplicated download/adapter logic from external-source workflows behind one tested helper/action/script.
4. **Retire superseded standalone category workflows** only after confirming the reviewed orchestrator/full JobG8 workflow covers their legitimate use cases.
5. **Report lifecycle cleanup** — operational vs analysis vs archive.
6. **Website/static-route rationalisation** last, because it carries the most SEO/user-facing risk; prefer dynamic slices for future growth but do not casually delete established routes.

## What the audit does NOT recommend

- no wholesale pipeline rewrite;
- no mass deletion based on filenames alone;
- no migration of working selection rules merely for aesthetic consistency;
- no website route cleanup before SEO/data dependencies are checked;
- no brittle CI rule that forces canonical-doc edits for trivial changes.

## Decision gate

**Audit is complete enough to move to the agreement stage.** No refactor should begin until the owner agrees the target shape and refactor order above.

## Safety rule

No production behaviour has been changed by this audit. The only persistent changes during the audit are governance/audit documentation.
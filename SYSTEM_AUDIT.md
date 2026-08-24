# Ontap System Audit

**Audit started:** 19 August 2026  
**Status:** First architecture audit complete; agreed cleanup 1–5 merged into `main` via PR #211. Teaching Vacancies writeback resilience, 55-market geography reconciliation and 11-market Service Admin expansion verified 22 August 2026.

The audit conclusion remains: **preserve the working core; remove historical scaffolding; consolidate duplicated mechanics; do not refactor for technical tidiness alone.**

## Business-priority constraint

Business priority wins over technical neatness. Website routes and public URLs are out of scope for this cleanup unless there is evidence that they materially harm indexing/discoverability, AI discoverability, user experience, reliability or inventory expansion.

## Verified core architecture

### Scheduled source refresh

- `run-full-jobg8-daily-process.yml` — primary JobG8 production entry point, twice daily.
- `run-nejobs-review.yml` — daily NEJobs review refresh.
- `run-vonne-review.yml` — daily VONNE review refresh.
- `run-teaching-vacancies-regional-review.yml` — daily Teaching Vacancies review refresh; its evidence writeback now uses full-history checkout plus pull-rebase/push retry protection against concurrent `main` updates.
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

## Reliability follow-up — 22 August 2026

The scheduled Teaching Vacancies regional/master workflow successfully completed its live discovery, routing, review generation and verification on 22 August, but its final plain `git push origin main` was rejected with `fetch first` because another workflow had advanced `main` during the roughly nine-minute run. The generated 22 August TV evidence therefore never reached the repository, and the master Review Hub correctly continued to report the previous 19 August Teaching Vacancies state as stale.

This was a repository-write race, not a Teaching Vacancies discovery/classification failure. The workflow was hardened to check out full history and retry the final write up to three times using `git pull --rebase origin main` followed by `git push origin HEAD:main`, aborting a failed rebase safely before retrying. A manual post-fix rerun then green-ticked and committed fresh 22 August England-wide Teaching Vacancies evidence to `main`.

The operating implication is explicit: source refresh freshness is upstream of `apply-publish-ontap-daily-review.yml`. A stale/missing source is flagged and must not be interpreted as zero inventory, but source isolation allows the parent publication path to continue with clean sources rather than turning one stale source into a whole-system failure.

On 24 August, the live-site discovery guard was refined after an otherwise healthy run failed because one vacancy disappeared between two complete national sweeps. TV now performs one fully audited sweep: advertised page ranges, totals and vacancy-link counts must reconcile; transient page failures retain their targeted retries; inconsistent route facts retry only that route; and persistent route/page integrity failure still stops the source. This removes the false requirement that a live job board remain byte-for-byte static across two complete sweeps without weakening fail-closed source integrity.

## Geography / regional expansion follow-up — 22 August 2026

The first geography reconciliation proved that the former **33-region England footprint was a configured operational subset** and expanded England to **55 assessable markets**. A same-day scope correction then established that England alone is not the complete Ontap national geography. `pipeline/config/uk_assessable_regions.json` is now the recurring diagnostic authority with **78 UK markets: 58 England + 10 Scotland + 8 Wales + 2 Northern Ireland**. `pipeline/config/england_assessable_regions.json` remains the verified England subset/reference. `pipeline/geo/geo_lookup.xlsx` remains the factual location-routing authority; `pipeline/config/job_slice_catalog.json` remains configured/public market metadata; and `pipeline/registers/region_category_slice_register.csv` remains the LIVE-state gate.

The full JobG8 daily process now assesses Service Admin, Support Worker and Customer Sales / Sales Advisor across all 78 UK markets and targets **234 market/family rows** plus rolling 14-feed history. Exact safe lookup aliases are rolled into their canonical assessment markets; ambiguous generic geography is left unresolved rather than force-assigned. The North East remains one public/assessment roll-up over its three underlying lookup regions, including Tees Valley.

The owner set a Service Admin-specific standing launch rule on 22 August: **a governed same-feed Service Admin count over 8 is immediate approval for LIVE; 8 or below remains NOT LIVE and is tracked**. Applying that rule to the recovered geography launched 11 additional Service Admin markets: Cheshire - East, Cheshire - Warrington & Halton, Cornwall, Derbyshire, Greater Manchester - Wigan & Bolton, Leicestershire, Lincolnshire, Merseyside - Liverpool, Shropshire, Suffolk and West Midlands - Black Country.

The launch reused the existing central catalog, slice register, production selector, configured-slice routes and verified publisher. It did not remove or rename any previously live URL. After the launch, the daily regional overview reconciled to **41 / 55 LIVE Service Admin markets** and numeric live counts for all 11 newly activated markets. Support Worker and Customer Sales retain their existing explicit-approval rules unless the owner changes them separately.

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

The cleanup changes are part of `main`. Subsequent governed production changes now also include the complete 78-market UK diagnostic geography and the 11 additional Service Admin LIVE markets approved under the 22 August >8 standing rule. No previously live public URL was removed or renamed by that expansion.

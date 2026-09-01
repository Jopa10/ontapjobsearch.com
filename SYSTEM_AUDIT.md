# Ontap System Audit

**Audit started:** 19 August 2026  
**Status:** First architecture audit complete; agreed cleanup 1–5 merged into `main` via PR #211. Google Jobs eligibility remediation was audited, tested and owner-approved for production on 27 August 2026.

The audit conclusion remains: **preserve the working core; remove historical scaffolding; consolidate duplicated mechanics; do not refactor for technical tidiness alone.**

## Business-priority constraint

Business priority wins over technical neatness. Website routes and public URLs are out of scope for this cleanup unless there is evidence that they materially harm indexing/discoverability, AI discoverability, user experience, reliability or inventory expansion.

## Verified core architecture

### Scheduled source refresh

- `run-full-jobg8-daily-process.yml` — primary JobG8 production entry point, twice daily. GitHub cron is primary; cron-job.org dispatches the same workflow at 08:35 and 17:35 Europe/London as an idempotent fallback. A committed same-date morning/evening marker is written only after a successful complete run, and the workflow concurrency lock means a late duplicate exits before work starts.
- `run-nejobs-review.yml` — daily NEJobs review refresh.
- `run-vonne-review.yml` — daily VONNE review refresh.
- `run-teaching-vacancies-regional-review.yml` — daily Teaching Vacancies review refresh; its evidence writeback now uses full-history checkout plus pull-rebase/push retry protection against concurrent `main` updates.
- `ontap-daily-review.yml` — builds/emails the master owner review.

### Reviewed publication

- `apply-publish-ontap-daily-review.yml` — owner-facing orchestration point.
- The same workflow provides the 11:45 Europe/London no-edit publication safety net; it skips after a successful same-date manual run and otherwise withholds unresolved jobs without persisting exclusions while using the existing guarded publishers.
- `apply-jobg8-review-decisions.yml` — exact reviewed JobG8 replay/apply path.
- source-specific approved publishers — NEJobs, VONNE and Teaching Vacancies.
- `publish-verified-pages.yml` — final shared bridge into live `app/**.json`, live-job reporting and city-page outputs.

### Indexing / monitoring

- `google-indexing-api.yml` — daily Google Indexing API submission, 200-notification cap, persistent submission state and GitHub Issue alerting.
- `build-daily-region-overview.yml` — post-publish regional operational overview.
- `ontap-daily-status.yml` — single owner-facing Actions check for same-day source/review readiness and complete manual-or-automatic publication/deployment. It links failures back to the technical run while leaving the underlying failure-isolation architecture intact.

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

Also on 24 August, daily publication gained an 11:45 Europe/London safety net inside the existing owner-facing orchestrator. It checks for a successful manual workflow dispatch on the same local date and skips if found. If no manual publication completed, it reconciles current sources and publishes through the existing guarded chain using a distinct automatic-withhold policy: unresolved jobs are not published, not persisted as exclusions and do not isolate an otherwise healthy source merely because there are more than 15. Source staleness, changed review fingerprints, source-publisher failure isolation and the final verified-page integrity gate remain unchanged. This closes the operational dependency on the owner completing an edit session every day without weakening job-level fail-closed selection.

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

## Google Jobs eligibility follow-up — 27 August 2026

The audit evaluated all 1,187 current unique published jobs and the generated static HTML, with JobG8 treated as the primary commercial source. JobG8 contributes 1,056 unique vacancies. Before remediation, 777 JobG8 pages emitted `JobPosting` without `datePosted`, so zero JobG8 pages met all six audited schema-field requirements. The tested result is 777 complete-description JobG8 pages with valid local `JobPosting`; 279 teaser-description pages remain without job schema.

The checked 10,000-row JobG8 workbook has only `/Job/Description` for advert copy. Its 279 currently published teaser rows have no upstream full-description alternative in that upload. They therefore remain visible, indexable job pages with a working apply route but are not misrepresented as complete Google job schema. No description, employer, location, posting date or expiry has been fabricated.

For current JobG8, `datePosted` is the existing stable `ontap_first_published` date. Date precedence is: reliable original source/advert date; a populated and semantically valid JobG8 `/Job/StartDate`; otherwise stable Ontap first publication. Shared publication-date history prevents daily republication, a slice move or a reappearance from resetting that value. JobG8 supplies no current expiry value, so `validThrough` is omitted. It will be emitted only when a valid source expiry exists.

The generated-page audit verified 1,056/1,056 JobG8 pages are indexable, 1,056/1,056 expose a normal apply anchor, and exactly 777 emit `JobPosting`. All 1,056 are in static parameters and the sitemap. One JobG8 reference containing spaces and square brackets formerly generated a `noindex` 404 because the encoded route parameter did not match the raw ID; lookup now decodes the parameter while preserving the published URL.

The remediation was prepared and tested on `audit/google-jobs-eligibility`, then approved by the owner for production deployment on 27 August 2026.

## Merge state

Architecture cleanup 1–5 was merged into `main` via PR #211 on 19 August 2026. The audit should therefore be read against the cleaned architecture now present on `main`, not against the former feature branch state.

## Current production repository state

The cleanup changes are part of `main`. Subsequent governed production changes now also include the complete 78-market UK diagnostic geography and the 11 additional Service Admin LIVE markets approved under the 22 August >8 standing rule. No previously live public URL was removed or renamed by that expansion.

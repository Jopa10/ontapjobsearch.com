# Ontap System Map

**Last updated:** 20 August 2026  
**Status:** Canonical production architecture after cleanup, regional expansion, city-page expansion and deployment-path verification.

This is the authoritative technical map of the persistent Ontap system. It is organised into five canonical buckets. Facts not verified from the repository are marked `UNKNOWN / NEEDS AUDIT` rather than inferred from chat history.

## Recent canonical changes

- 20 August 2026 — Added canonical governance for discovering and activating new job families: discovery audit → family boundary → proof-region review → title register/refinement rules → national validation → 33-region diagnostic assessment → explicit LIVE-slice approval → integration into the existing daily/publish mechanisms. Family membership is non-exclusive where a job genuinely fits more than one user-facing family.
- 20 August 2026 — Confirmed the production deployment model by live test: normal Vercel Git integration is the single automatic deployment route for `main`; `Deploy Ontap production after publish` waits up to three minutes for production to reach the expected SHA and fails/alerts if it does not. `VERCEL_TOKEN`/Vercel CLI is manual recovery only. The obsolete Deploy Hook was revoked and the `VERCEL_DEPLOY_HOOK_URL` repository secret removed.
- 19 August 2026 — Homepage browse ordering now presents regional slices before city pages. Regional inventory is the primary breadth signal; city pages remain a secondary local layer, still subject to the 4-job homepage visibility floor.
- 19 August 2026 — Added a separate city homepage visibility floor: active city pages remain permanent, but homepage city cards appear only at 4+ current jobs. The launch threshold remains 6 jobs with 3 of 7 qualifying runs plus explicit approval.
- 19 August 2026 — Approved five additional Service Admin city pages: Bradford, Huddersfield, York, Barnsley and Doncaster. Initial include rules are exact-city only; the shared city-page framework owns derivation and permanence.
- 19 August 2026 — Added explicit city catchment governance: city pages represent city-anchored local employment/commuting markets, not literal exact-name-only filters. Catchment expansions require explicit include/review/exclude rules in `pipeline/city_pages/city-page-register.json`.
- 19 August 2026 — Durham Service Admin remains HOLD because the registered opportunity pattern `durham` can also match broad `County Durham` locations. Durham must be separated from County Durham and requalified before activation.
- 19 August 2026 — Activated six additional Service Admin regional slices: Buckinghamshire, Greater Manchester - South, Hertfordshire, Somerset, West Midlands - Birmingham & Solihull, and Yorkshire - East.
- 19 August 2026 — Added same-feed 33-region family coverage for Service Admin and Support Worker inside the main JobG8 daily run.
- 19 August 2026 — Added publication failure isolation and made external-source publishing fail-soft where safe.
- 19 August 2026 — Merged architecture cleanup 1–5 into `main` via PR #211.

## 1. Pipeline

Purpose: how job data moves from source to published/indexed output.

Canonical stages:

`source → ingest → classify/select → review → approved output → compose → verified publish → app JSON → city derivation → Vercel Git deployment → live SHA verification → index`

### Main scheduled JobG8 path

Primary scheduled entry point: `.github/workflows/run-full-jobg8-daily-process.yml`.

It runs at 07:30 and 15:30 Europe/London and performs:

`JobG8 feed → pipeline/input/jobg8.xlsx → validation + duplicate report → LIVE slice register → service-admin/support-worker selectors → approved external-source composition → metadata enrichment → 33-region family coverage → pipeline outputs/reports`

`pipeline/input/jobg8.xlsx` is transient workflow input and is not committed. The validated raw feed is retained durably in S3 under `jobg8/raw`.

The daily coverage pass reuses the same materialized JobG8 workbook and production rules across all 33 canonical regions. It writes diagnostic coverage only; it does not itself activate slices.

The Service Admin LIVE set includes the six 19 August evidence-led regional activations: Buckinghamshire, Greater Manchester - South, Hertfordshire, Somerset, West Midlands - Birmingham & Solihull, and Yorkshire - East.

### New job-family discovery and activation governance

A new job family must not move directly from a broad title/regex discovery result into production slices. The canonical lifecycle is:

1. **Discovery audit** — use the current feed, specialist analysis or one-off diagnostics to identify a plausible occupational seam and estimate its scale. Discovery rules are evidence gathering, not publish rules.
2. **Define the family boundary** — state the jobseeker proposition in occupational terms: what belongs, what does not, and the important ambiguous/overlap cases.
3. **Proof-region review** — inspect real jobs in a small number of representative regions before national rollout. The objective is page quality and false-positive/false-negative discovery, not simply volume.
4. **Create governed classification state** — encode recurring title decisions in the appropriate central title register and add contextual/refinement rules where title alone is insufficient. Do not leave persistent family logic as an ad-hoc regex report.
5. **National validation** — apply the candidate selector to the full current feed and review selected/rejected examples, scale, specialist contamination, salary/context effects and material false positives/negatives.
6. **33-region diagnostic assessment** — once the selector is credible, assess every canonical region using the same family logic. This produces evidence only and must not activate slices automatically.
7. **Explicit LIVE-slice approval** — activate only regions with sufficient recurring quantity and page quality. A non-zero diagnostic count is not by itself an activation decision.
8. **Integrate, do not parallel-build** — once approved, the family must use the existing shared ingest, registers/config, review, publishing, reporting and website mechanisms wherever those mechanisms can be extended safely.

Family classification is **not required to be mutually exclusive**. A single underlying job may legitimately qualify for more than one Ontap family when it genuinely serves both user intents (for example, a customer/commercial support role that fits both Service Admin and a future Sales Advisor family). Each family applies its own eligibility/refinement rules. Duplication should be suppressed only where the same job would otherwise appear redundantly in one user-facing result set; a job must not be removed from one valid family merely because it also qualifies for another.

The current Sales Advisor work is a discovery candidate under this lifecycle. It is not yet a production family and remains outside the recurring 33-region family assessment until its boundary, register/refinement rules and validation are approved.

### Owner review / approved publication

Owner-facing orchestrator: `.github/workflows/apply-publish-ontap-daily-review.yml`.

It reconciles the master review, applies valid decisions back to source-owned review files, dispatches source-specific approved publishers, and invokes `publish-verified-pages.yml` when the shared final publish is required.

Publication isolation is hierarchical:

- up to 15 unresolved/malformed jobs in one source are withheld fail-closed while clean jobs continue;
- more than 15 such jobs, or a source-level integrity mismatch, isolates that source and retains its previous approved state;
- source publisher failures are fail-soft where the prior approved state can safely be retained;
- only a genuine combined/publication integrity failure should stop the whole publish.

Confirmed source paths include JobG8, NEJobs, VONNE and Teaching Vacancies.

`publish-verified-pages.yml` is the final bridge from reviewed/composed outputs into user-facing `app/**.json`, live-job reports and city-page outputs. On successful completion, GitHub automatically starts `.github/workflows/deploy-vercel-after-publish.yml`. That guard checks out current `main`, records the expected SHA and waits for the normal Vercel Git integration deployment to reach that commit or a newer descendant. Automatic runs do not invoke Vercel CLI recovery.

### City-page derivation and launch governance

Canonical components:

- `pipeline/city_pages/opportunity-market-register.json` — monitored local employment markets beneath published regional slices;
- `pipeline/scripts/scan_city_opportunities.py` — current opportunity scan;
- `pipeline/scripts/update_city_opportunity_history.py` — rolling seven-run evidence history;
- `pipeline/reviews/city-pages/city-page-approval-review.md` — human approval surface;
- `pipeline/city_pages/city-page-register.json` — active technical catchment configurations;
- `pipeline/scripts/derive_city_pages.py` — derive/review/publish city JSON;
- `pipeline/scripts/maintain_active_city_pages.py` — keep active permanent routes refreshed even below launch threshold;
- `app/_city-pages/...` — private derived city JSON used by public city routes.

Launch gate: a candidate must have **at least 6 current jobs and at least 3 qualifying runs among the last 7 verified-publish runs**, then receive explicit human approval. READY FOR APPROVAL never publishes automatically.

Once `lifecycle_state: active`, the city route is permanent unless deliberately retired. Falling below six jobs does not delist or 404 the route; the active-city maintenance step rewrites the current output, including an empty array at zero jobs.

Homepage visibility is deliberately separate from permanence. An active city page appears as a homepage city card only at **4+ current jobs**. At 0–3 jobs the page remains live/indexable and refreshed, but its homepage card is hidden until supply returns to 4+.

Canonical city thresholds:

- **6 jobs** = launch threshold, with 3 of 7 qualifying runs plus explicit approval;
- **4 jobs** = homepage city-card visibility floor;
- **0 jobs** = valid retained state for an already-active permanent city route.

The visibility rule must never be used to justify artificially widening a catchment merely to keep a homepage card visible.

#### Catchment rule

A city page is an **approved local employment/commuting catchment anchored on the named city**. It is not defined solely by exact city-name text.

Launch catchments should be conservative. Nearby towns, suburbs or districts may be added only where they clearly belong to the same employment market and do not bleed into a separate labour market. Every addition must be encoded in `city-page-register.json` as an include/review/exclude rule with a reason.

Established examples:

- Leeds: Leeds + Pudsey;
- Newcastle: Newcastle + Gateshead + North Tyneside + Shiremoor + Wideopen;
- Brighton & Hove: Brighton + Hove + Portslade.

Broad county/region labels are not proof of city membership. **Durham is the explicit safeguard case:** a location containing `County Durham` must not count as Durham-city evidence merely because it contains the word `durham`. Durham Service Admin remains HOLD until the opportunity rule distinguishes Durham city from County Durham and its seven-run history is recalculated.

Approved on 19 August 2026 with exact-city launch catchments:

- Bradford Service Admin — `/bradford/service-administrator-jobs`;
- Huddersfield Service Admin — `/huddersfield/service-administrator-jobs`;
- York Service Admin — `/york/service-administrator-jobs`;
- Barnsley Service Admin — `/barnsley/service-administrator-jobs`;
- Doncaster Service Admin — `/doncaster/service-administrator-jobs`.

### External-source review paths

Recurring review workflows:

- NEJobs — 06:15 daily;
- VONNE — 06:35 daily;
- Teaching Vacancies regional/master review — 06:55 daily.

### Core supporting areas

- `pipeline/config/`
- `pipeline/geo/`
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

## 2. Reports / diagnostics

Purpose: persistent outputs used to reconcile, inspect or monitor Ontap.

Operational reports include:

- `pipeline/reviews/daily/ontap-daily-review.md` — daily owner review;
- `pipeline/reports-daily/daily-family-coverage.csv` — same-feed Service Admin and Support Worker coverage across all 33 canonical regions;
- `pipeline/reports-daily/daily-region-overview.md` — regional live/not-live overview;
- `pipeline/reports/city-opportunities-current.md` and `.json` — current city/local-market opportunity state;
- `pipeline/reports/city-opportunity-history.json` — rolling qualification history.

The city-opportunity scanner is diagnostic/decision support. It must not auto-activate a city page.

Compiler Modules 1, 2 and 3 remain legitimate specialist/manual analysis workflows.

Report lifecycle is recurring operational reporting / deliberate specialist analysis / one-off diagnostics in Actions artifacts or Git history.

## 3. Website / UX

Purpose: user-facing job search, job pages, navigation and presentation.

Verified structure:

- `app/` is the primary application route/data tree;
- `components/` contains reusable UI components;
- `lib/published-jobs.ts` supplies the common published job/search/detail layer;
- `lib/configured-job-slices.ts` reads the configured regional slice catalog/register;
- LIVE dynamic regional/category slices are register/catalog driven;
- `app/_city-pages/configured-slices/` holds dynamic configured-slice data;
- `app/job-search/[region]/...` is the dynamic route family;
- Browse Jobs, `/jobs/search`, job-detail backlinks and the homepage Admin grid consume published dynamic slices through shared mechanisms;
- homepage browse ordering is regional-first, then city, to make regional inventory breadth the primary visual signal;
- `lib/city-page-data.ts` reads `pipeline/city_pages/city-page-register.json` and resolves active city definitions/data;
- public city routes read private derived JSON under `app/_city-pages/...`, preventing duplicate job-detail URLs;
- homepage city cards are filtered independently at 4+ current jobs; this does not change route activation/permanence;
- `app/api/deployment-version/route.ts` exposes the deployed Vercel Git SHA for verification.

New approved city routes are Bradford, Huddersfield, York, Barnsley and Doncaster Service Admin. Durham has no approved city route.

### Website refactor rule

Public URLs remain stable unless a concrete business benefit or defect justifies change. Existing indexing/SEO behaviour should be preserved unless the change is intentionally improving it.

## 4. Content / positioning

Persistent product content belongs here when it changes product behaviour. Ontap's broad direction remains a job site for ordinary workers in an AI workplace, with sector-switching as an additional route rather than the entire identity.

## 5. Operations / infrastructure

Core scheduled workflows include:

- `run-full-jobg8-daily-process.yml` — 07:30 and 15:30 Europe/London;
- `run-nejobs-review.yml` — 06:15 daily;
- `run-vonne-review.yml` — 06:35 daily;
- `run-teaching-vacancies-regional-review.yml` — 06:55 daily;
- `ontap-daily-review.yml` — 08:45 Europe/London;
- `google-indexing-api.yml` — 19:30 UTC daily.

The owner-facing publication entry point is `apply-publish-ontap-daily-review.yml`.

### Post-publish production deployment

`.github/workflows/deploy-vercel-after-publish.yml` is the canonical production-deployment guard. It starts automatically after a successful `Publish verified pages` workflow and also supports manual dispatch for recovery/testing.

Automatic post-publish behaviour:

1. check out current `main` and record its expected SHA;
2. wait up to three minutes for normal Vercel Git integration to deploy that SHA or a newer descendant commit on `main`;
3. verify the live SHA through `/api/deployment-version`;
4. if Git deployment catches up, finish successfully and skip every CLI recovery step;
5. if production does not catch up, fail the automatic run and raise/update the GitHub Issue `Ontap production deployment is stale`;
6. do **not** invoke a second automatic deployment.

Manual recovery behaviour:

1. manually dispatch `Deploy Ontap production after publish`;
2. require the repository secret `VERCEL_TOKEN`;
3. deploy current `main` directly with the Vercel CLI to the fixed Ontap production project;
4. verify production through the same live-SHA endpoint;
5. close the stale-production issue after a healthy recovery.

The normal Git path was confirmed end-to-end in production on 20 August 2026: `Wait for normal Git deployment` succeeded, the stale flag was skipped, and all `VERCEL_TOKEN`/CLI recovery steps were skipped. The Vercel Deploy Hook used during the 19 August incident has been revoked and the `VERCEL_DEPLOY_HOOK_URL` GitHub secret removed. Deploy Hooks are no longer part of the production architecture.

This leaves one automatic route — `main` → Vercel Git integration — plus one explicit manual recovery route. The recovery route cannot create routine duplicate deployments because it does not run automatically.

### Google Indexing API

`google-indexing-api.yml` submits eligible job URLs, caps each run at 200 notifications, persists submission state in `pipeline/manifests/google-indexing-state.json`, and uses GitHub Issues for backlog/safety/failure alerts.

## Validation state

Architecture cleanup 1–5 is merged into `main` via PR #211 and is canonical. The six additional regional Service Admin slices and five additional Service Admin city pages described above are now part of the documented production state. Durham remains deliberately unapproved pending the County Durham safeguard. The Vercel production deployment route is verified as normal Git deployment with manual-only CLI recovery.

## Documentation rule

When a persistent system-level change alters any canonical bucket, update this file in the same change. If live/active/user-facing state changes, update `SYSTEM_OVERVIEW.md` as well.

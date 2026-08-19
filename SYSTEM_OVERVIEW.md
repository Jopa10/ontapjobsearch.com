# Ontap System Overview

**Last updated:** 19 August 2026  
**Status:** Canonical production state after architecture cleanup, regional expansion and city-page expansion.

This is the short owner view of how Ontap is organised. It mirrors the five canonical system buckets in `SYSTEM_MAP.md`.

## Recent canonical changes

- 19 August 2026 — Homepage browse ordering now shows regional slices before city pages, so the first impression reflects Ontap's broader job coverage while retaining city pages as a secondary local layer.
- 19 August 2026 — Replaced reliance on Vercel noticing Git pushes with an explicit post-publish deploy path: successful `Publish verified pages` completion automatically runs `Deploy Ontap production after publish`, POSTs the `VERCEL_DEPLOY_HOOK_URL` secret, then verifies the live deployment SHA. A stale/failed deployment raises or updates the GitHub Issue **Ontap production deployment is stale**; a later healthy run closes it.
- 19 August 2026 — Added a separate **4-job homepage visibility floor** for active city pages. City routes remain permanent below four jobs; only the homepage card is hidden until supply returns to 4+.
- 19 August 2026 — Approved five further Service Admin city pages: **Bradford, Huddersfield, York, Barnsley and Doncaster**. Initial catchments are exact-city only. Active city pages are permanent once launched.
- 19 August 2026 — Made the city-page geography rule explicit: a city page represents a **city-anchored local employment/commuting catchment**, not simply an exact city-name string. Nearby towns/suburbs may be added only when they genuinely belong to the same labour market and the decision is recorded in the city-page register.
- 19 August 2026 — Put **Durham Service Admin on HOLD** because the present `durham` opportunity-market pattern can also match broad `County Durham` locations. Durham must be separated from County Durham and then requalified before launch.
- 19 August 2026 — Activated six additional Service Admin regions from same-feed 33-region evidence: Buckinghamshire, Greater Manchester - South, Hertfordshire, Somerset, West Midlands - Birmingham & Solihull, and Yorkshire - East.
- 19 August 2026 — Added same-feed daily coverage for Service Admin and Support Worker across all 33 canonical regions.
- 19 August 2026 — Added fail-soft publication hierarchy: small job-level problems are withheld while clean jobs continue; larger source problems isolate that source rather than blocking the whole Ontap publish.
- 19 August 2026 — Merged architecture cleanup 1–5 into `main` via PR #211.

## 1. Pipeline

The main JobG8 process remains the production ingest/process path. NEJobs, VONNE and Teaching Vacancies retain their review paths. After review, the single **Apply and publish Ontap daily review** workflow coordinates source publishers and the final verified-page publish.

Service Admin now includes the six additional LIVE regional slices approved on 19 August. They use the same central register, production selector and verified-page publishing mechanism as the other LIVE dynamic slices.

The publish rule is deliberately fail-soft:

**up to 15 bad/unresolved jobs in one source are withheld and flagged while clean jobs continue; more than 15, or a source-integrity problem, isolates that source and keeps its last approved state; only a genuine whole-publication integrity failure should stop everything.**

The old May monolithic pipeline and older standalone service-admin/support-worker workflows have been removed because the current full/reviewed pipeline covers those operational paths.

### City-page pipeline

City pages are derived views of final approved regional pages; they are not separate feeds or classification pipelines.

The launch gate is evidence-led: **6+ current jobs and at least 3 qualifying runs in the last 7 verified-publish runs**, followed by explicit human approval. READY FOR APPROVAL does not auto-publish.

Once explicitly active, a city route is permanent even if inventory later drops below six. The daily publication path continues to rebuild its private city JSON from the approved parent regional page.

Homepage prominence is a separate rule: an active city page is shown as a homepage city card only at **4+ current jobs**. At 0–3 jobs the route remains live/indexable and continues to refresh, but its homepage card is hidden until supply returns to 4+.

The three city thresholds are therefore:

- **6 jobs** = launch qualification threshold, with 3 of 7 qualifying runs and explicit approval;
- **4 jobs** = homepage city-card visibility floor;
- **0 jobs** = permitted retained state for an already-active permanent route.

The geographic unit is an **approved local employment/commuting catchment anchored on the named city**. Launch should start conservatively. Catchments can later include nearby towns/suburbs only where they clearly belong to the same labour market and are recorded as explicit include/review/exclude rules. Low inventory is not a reason to widen a catchment artificially.

Examples: Leeds includes Pudsey; Newcastle includes Gateshead, North Tyneside, Shiremoor and Wideopen; Brighton & Hove includes Portslade.

Newly approved on 19 August 2026: **Bradford, Huddersfield, York, Barnsley and Doncaster Service Admin**. Their launch catchments are exact-city only.

**Durham is not approved.** The current opportunity rule can confuse Durham city with broad County Durham locations; it must be corrected and the history recalculated before Durham can qualify.

## 2. Reports / diagnostics

The daily regional overview is backed by same-feed Service Admin and Support Worker assessments across all 33 canonical regions. A zero in those assessed families is a real current zero rather than “not assessed”.

The city-opportunity report scans published regional/category slices against registered local markets and records seven-run qualification history. It is an expansion-control surface, not an automatic publisher.

Dated one-off recovery/failure reports are not part of the permanent working tree. The reporting rule is:

**recurring operations / specialist analysis / one-off diagnostics in Actions artifacts or Git history.**

Compiler Modules 1/2/3 remain legitimate analysis tools.

## 3. Website / UX

LIVE dynamic regional slices feed Browse Jobs, `/jobs/search`, job-detail backlinks and the homepage Admin region grid through the shared configured-slice/published-job mechanisms.

On the homepage, regional slices are deliberately listed before city pages. This gives the primary browse area a stronger sense of breadth and current inventory; city pages remain a secondary local-discovery layer beneath the regional coverage.

City pages use the common city-page framework and private `app/_city-pages/...` derived JSON, avoiding duplicate job-detail URLs. The homepage city grid independently suppresses active city cards below 4 current jobs without changing the route, sitemap/indexing status or daily refresh behaviour.

The five new approved routes are:

- `/bradford/service-administrator-jobs`
- `/huddersfield/service-administrator-jobs`
- `/york/service-administrator-jobs`
- `/barnsley/service-administrator-jobs`
- `/doncaster/service-administrator-jobs`

Existing established public routes remain stable unless there is a concrete business reason to change them.

## 4. Content / positioning

No content-architecture cleanup is included. Ontap remains positioned around useful job discovery for ordinary workers in an AI workplace, with sector-switching as an additional route rather than the whole identity.

## 5. Operations / infrastructure

Core controls are:

- scheduled source refresh/reviews;
- one master daily owner review;
- one owner-facing apply/publish orchestrator;
- final verified-page publishing including city-page derivation/maintenance;
- explicit post-publish Vercel deploy-hook execution and live SHA verification;
- Google indexing and operational monitoring.

A successful `Publish verified pages` run automatically triggers `.github/workflows/deploy-vercel-after-publish.yml`. That workflow checks out current `main`, captures the expected SHA, POSTs the repository secret `VERCEL_DEPLOY_HOOK_URL`, and polls `https://www.ontapjobsearch.com/api/deployment-version` until production contains that commit or a newer descendant on `main`.

This deploy-hook path is canonical because normal Git→Vercel automatic deployment proved intermittently unreliable. The Git integration may still deploy normally, but production publication must not depend on it noticing a push. If the hook or live-SHA verification fails, the child workflow raises/updates the GitHub Issue **Ontap production deployment is stale**; a later healthy run closes it.

The Google Indexing API retains its 200-notification safety limit and GitHub Issue alerting.

## Business rule

**Business priority wins over technical tidiness.** Cleanup is justified where it improves reliability, delivery speed, cost, UX, indexing/discoverability, AI discoverability or safe inventory growth — not simply because a cleaner-looking architecture is possible.

## Current state

Architecture cleanup 1–5 is merged into `main`. The six additional Service Admin regional slices are LIVE. Bradford, Huddersfield, York, Barnsley and Doncaster Service Admin are approved permanent city pages using the shared city-page mechanism. Active city routes remain permanent below four jobs but are hidden from the homepage until they return to 4+. Homepage browse ordering is regional-first, then city. Durham remains deliberately held pending the County Durham geography safeguard.

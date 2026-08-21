# Ontap System Overview

**Last updated:** 21 August 2026  
**Status:** Canonical production state after architecture cleanup, regional/city expansion, deployment-path verification, NHS Administrative & Clerical integration, search/UX hardening and initial Customer Sales production launch.

This is the short owner view of how Ontap is organised. It mirrors the five canonical system buckets in `SYSTEM_MAP.md`.

## Recent canonical changes

- 21 August 2026 — Customer Sales / Sales Advisor completed governed proof-region review and national/33-region validation. Explicit LIVE approval is limited to **London**, **Greater Manchester - Manchester & Salford**, and **Yorkshire - West**. The first verified production publish completed successfully on 21 August: **London 20 jobs, Manchester & Salford 6, Yorkshire - West 7**. All three public `/job-search/.../customer-sales-jobs` routes returned HTTP 200 with job-detail links and JobG8 Apply wiring present. These counts are a launch snapshot, not automatic activation/deactivation thresholds. The production family keeps genuine sales-led office/contact-centre/home/hybrid roles, allows valid Sales/Service Admin overlap, and excludes field/in-home/event/self-employed, automotive dealership, retail/property and senior/specialist contamination. North East and all other regions remain non-LIVE diagnostics.
- 21 August 2026 — NHS job-detail pages now present NHS source text as readable paragraphs/headings/bullets instead of a flattened text dump. Long descriptions show six blocks initially, with the remainder available under **Show full NHS role information**; the vacancy wording itself is not rewritten.
- 21 August 2026 — NHS jobs are now deliberately mixed into regional Service Admin pages rather than bunching near the top: non-NHS jobs keep the normal location-first order, while accepted NHS jobs retain Tier A/B → switchability → freshness order and are inserted at no more than one after every four non-NHS jobs. The hard **20% NHS ceiling** remains the upstream source cap.
- 21 August 2026 — Search now handles multi-field one-box queries across role, employer, place and curated category, protects genuine role terms from accidental location inference, and applies only high-confidence typo correction. Browser spellcheck/autocorrect is enabled; spelling vocabularies/results are cached and the search route prefers Vercel London (`lhr1`) for lower UK latency.
- 21 August 2026 — Search now uses a compact index generated once during the Vercel build rather than reconstructing published jobs from the route JSON tree on each request. The boxes are explicitly labelled; `office`/`clerical` are understood as admin intent; and weighted role-vs-location evidence can recover accidentally reversed fields. Live checks now return Great Lumley for `lumley office` and corrected `lumley offcie`, while both `admin` + `newcastle` orientations return the same 21 current matches.
- 21 August 2026 — Final search-performance optimisation now precomputes the normalised/tokenised per-job search fields at build time as `_search` metadata. The runtime search uses that metadata directly instead of repeatedly normalising full job strings, and the raw advert description/full-description payload is removed from the search-function bundle while its precomputed searchable representation is retained. Matching, typo tolerance and field interpretation are unchanged; live browser retest confirmed the previous 4–5 second perceived delay was removed.
- 21 August 2026 — Vercel was upgraded from Hobby to Pro after the Hobby build-rate limit blocked a valid production build. The deployment model is unchanged: normal Git deployment from `main` remains the sole automatic route.
- 21 August 2026 — NHS Jobs Administrative & Clerical inventory is now live inside Service Admin. NHS is a complementary source, not a separate job board: each eligible regional Service Admin page has a hard **20% NHS ceiling**, not a 20% target.
- 21 August 2026 — NHS quality/order is governed before freshness: **HC Tier A before Tier B**, then switchability preference within equivalent quality; ambiguous/unseen titles stay POSS/fail-closed unless explicitly/validly selected.
- 21 August 2026 — The normal daily workflow and the reviewed NHS publisher now use the same transactional NHS composer. It refreshes current NHS inventory, restores valid remembered decisions, preserves non-NHS jobs, enriches only accepted NHS rows and verifies the 20% cap before replacing production output.
- 21 August 2026 — The hundreds of untouched NHS POSS rows no longer have to be edited in the normal daily review. They remain excluded, but their volume does not isolate NHS or block the automatically accepted HC Tier A/B rows.
- 20 August 2026 — Added a standard new-family lifecycle: discovery audit → define family → proof-region review → governed register/refinement rules → national validation → 33-region diagnostic assessment → explicit LIVE-slice approval → integration into the existing pipeline. Jobs may legitimately belong to more than one family where both user intents are valid.
- 20 August 2026 — Confirmed the production deployment model by live test: normal pushes to `main` are deployed by Vercel Git integration; the post-publish guard waits up to three minutes for production to reach the expected SHA; `VERCEL_TOKEN`/Vercel CLI is manual recovery only and does not fire automatically. The obsolete Deploy Hook was revoked and its `VERCEL_DEPLOY_HOOK_URL` repository secret removed.
- 19 August 2026 — Homepage browse ordering now shows regional slices before city pages, so the first impression reflects Ontap's broader job coverage while retaining city pages as a secondary local layer.
- 19 August 2026 — Added a separate **4-job homepage visibility floor** for active city pages. City routes remain permanent below four jobs; only the homepage card is hidden until supply returns to 4+.
- 19 August 2026 — Approved five further Service Admin city pages: **Bradford, Huddersfield, York, Barnsley and Doncaster**. Initial catchments are exact-city only. Active city pages are permanent once launched.
- 19 August 2026 — Made the city-page geography rule explicit: a city page represents a **city-anchored local employment/commuting catchment**, not simply an exact city-name string. Nearby towns/suburbs may be added only when they genuinely belong to the same labour market and the decision is recorded in the city-page register.
- 19 August 2026 — Put **Durham Service Admin on HOLD** because the present `durham` opportunity-market pattern can also match broad `County Durham` locations. Durham must be separated from County Durham and then requalified before launch.
- 19 August 2026 — Activated six additional Service Admin regions from same-feed 33-region evidence: Buckinghamshire, Greater Manchester - South, Hertfordshire, Somerset, West Midlands - Birmingham & Solihull, and Yorkshire - East.
- 19 August 2026 — Added same-feed daily coverage for Service Admin and Support Worker across all 33 canonical regions.
- 19 August 2026 — Added fail-soft publication hierarchy: small job-level problems are withheld while clean jobs continue; larger source problems isolate that source rather than blocking the whole Ontap publish.
- 19 August 2026 — Merged architecture cleanup 1–5 into `main` via PR #211.

## 1. Pipeline

The main JobG8 process remains the primary production ingest/process path. NEJobs, VONNE, Teaching Vacancies and NHS Jobs provide additional inventory through governed source paths. After review, the single **Apply and publish Ontap daily review** workflow coordinates source publishers and the final verified-page publish.

Service Admin includes the six additional LIVE regional slices approved on 19 August. They use the same central register, production selector and verified-page publishing mechanism as the other LIVE dynamic slices.

### NHS Administrative & Clerical

NHS Jobs is now a live input to Service Admin. It is deliberately constrained so it improves supply without making Ontap feel like an NHS-only board.

The production rule is:

**fresh NHS Administrative & Clerical inventory → classify/rank → route to existing LIVE Service Admin regions → dedupe against current output → cap NHS at no more than 20% per regional page → enrich accepted NHS adverts → verify → publish through the common Service Admin page path.**

The 20% figure is a ceiling, not a quota. A region may contain less NHS inventory if there are not enough suitable jobs.

NHS ranking prefers HC Tier A over Tier B. Within equivalent quality, open/pure switch opportunities are preferred ahead of bridgeable/possible and NHS-experience-needed roles; freshness comes later.

Regional presentation applies a separate non-dominance rule after composition: non-NHS jobs keep their normal location-first ordering, the accepted NHS subset keeps the same quality/switchability/freshness priority, and no more than one NHS job is placed after each four non-NHS jobs. This does not alter the 20% composition ceiling.

Ambiguous/unseen titles are POSS by default. Untouched POSS jobs remain fail-closed and are not required in the normal daily owner edit queue. This means the large POSS population does not create hundreds of mandatory edits or isolate NHS from the wider publish.

The same transactional composer is used by both the normal full daily workflow and the reviewed NHS publisher. It refreshes NHS itself before composition, so the normal daily run does not depend on a previously refreshed review being earlier than the JobG8 schedule.

### New job-family lifecycle

New occupational families are governed before they become production slices. The standard path is:

**discovery audit → define the family boundary → review real jobs in proof regions → create central title/refinement rules → validate against the full feed → assess all 33 canonical regions diagnostically → explicitly approve suitable LIVE slices → integrate the family into the existing daily/review/publish mechanisms.**

Broad discovery regex/title buckets are evidence only; they are not publication rules. A positive regional count also does not activate a slice automatically.

Family membership is not forced to be exclusive. A job can legitimately qualify for more than one family when it serves both user intents. Each family applies its own rules, and overlap is only deduped where the same job would otherwise repeat within one user-facing result set.

Customer Sales / Sales Advisor has completed the governed lifecycle through explicit LIVE approval. The first production slices are **London**, **Greater Manchester - Manchester & Salford**, and **Yorkshire - West**. The first live verified-publish snapshot produced **20 / 6 / 7 jobs respectively**. The production selector is generated from the same current JobG8 input as the main daily process and publishes through the shared configured-slice/verified-page mechanism. The LIVE state is governed by the explicit slice register, not by those one-day counts; normal daily inventory movement may take a live page above or below its launch count without automatically changing activation state. Genuine Sales/Service Admin crossover remains valid. Direct office/contact-centre/home/hybrid sales roles qualify; customer/service titles require explicit sales/conversion evidence; generic account roles require strong sales plus office/digital evidence. Field/in-home/event/self-employed sales, automotive dealership/showroom sales, retail/property sales and senior/specialist boundary roles are excluded. **North East and every other region remain non-LIVE diagnostic candidates until separately approved.**

The general publish rule remains fail-soft:

**up to 15 bad/unresolved mandatory-review jobs in one source are withheld and flagged while clean jobs continue; more than 15, or a source-integrity problem, isolates that source and keeps its last approved state; only a genuine whole-publication integrity failure should stop everything.**

NHS untouched POSS rows are an explicit exception to the mandatory-review count: they are optional review opportunities, remain excluded if untouched, and do not by themselves isolate NHS.

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

Live source reporting now also records NHS Jobs as a provider after verified publication, alongside JobG8 and the other external sources.

The city-opportunity report scans published regional/category slices against registered local markets and records seven-run qualification history. It is an expansion-control surface, not an automatic publisher.

Dated one-off recovery/failure reports are not part of the permanent working tree. The reporting rule is:

**recurring operations / specialist analysis / one-off diagnostics in Actions artifacts or Git history.**

Compiler Modules 1/2/3 remain legitimate analysis tools.

## 3. Website / UX

LIVE dynamic regional slices feed Browse Jobs, `/jobs/search`, job-detail backlinks and the homepage Admin region grid through the shared configured-slice/published-job mechanisms.

Customer Sales uses the same dynamic configured-slice mechanism. Production launch was verified on 21 August 2026 at `/job-search/london/customer-sales-jobs`, `/job-search/west-yorkshire/customer-sales-jobs`, and `/job-search/manchester-salford/customer-sales-jobs`: all three returned HTTP 200, rendered their current job cards and `/jobs/...` detail links, and exposed the expected JobG8-backed Apply actions. The same published-job inventory feeds Browse Jobs, homepage discovery, sitemap and search indexing.

NHS jobs use those same Service Admin pages and job-detail routes. A job is identified reliably by `source: "NHS Jobs"`; the employer itself may be an NHS trust, GP surgery, healthcare provider or other organisation whose visible name does not contain “NHS”. The job-detail page links to the original NHS Jobs advert for application.

NHS detail copy is now presentation-formatted rather than shown as a single flattened block. Existing structured headings/bullets are respected; otherwise long flattened NHS text is split into readable short paragraphs without changing the wording. The first six blocks remain visible and any remainder is available under **Show full NHS role information**.

Regional Service Admin pages deliberately mix NHS into the wider result set. NHS does not take the first slots simply because its internal quality ranking is strong: the normal inventory stays location-first and NHS is interleaved at the 4 non-NHS : 1 NHS rhythm while retaining the accepted NHS priority order.

Search uses a deployment-time snapshot of current published inventory. `scripts/generate-search-index.ts` creates `generated/published-jobs-search.json` during `npm run build`; `/jobs/search` imports that index directly rather than walking/parsing the full published route-data tree for each request. Each job also carries precomputed `_search` metadata containing the normalised/tokenised title, location, region, category, company, combined fields, slice label and searchable description representation. The search bundle therefore does not carry the raw advert description/full-description text and does not redo that field preparation on each request. This removes both the original request-time inventory reconstruction and the later per-request normalisation/tokenisation bottleneck while keeping the searchable meaning tied to the deployed published supply.

Search is deliberately forgiving but guarded. One-box queries can span title, employer/advertiser, location, region and curated category, so combinations such as employer/place + role can work naturally. When the dedicated location field is empty, a token is inferred as geography only if it lacks a credible title/category role anchor; polluted source location text therefore cannot steal a real role term such as `administrator`.

Both search inputs are explicitly labelled **Role or keyword** and **Location**. If a user reverses them, Ontap compares the amount of role evidence against geography evidence and can reinterpret the fields rather than returning an avoidable zero. `office` and `clerical` are accepted internally as admin intent for matching without replacing the user's displayed wording.

High-confidence spelling correction is applied from the current published-job vocabulary, with ambiguous/tied corrections left unchanged. Both search inputs also enable browser spellcheck/autocorrect. Correction vocabularies and recent correction results are cached. Runtime matching reuses the build-time `_search` metadata and a cached corpus-level geographic vocabulary rather than repeatedly rebuilding those structures.

Production verification on 21 August includes `lumley office` → Great Lumley Surgery, `lumley offcie` → corrected `lumley office` → the same vacancy, and `admin` + `newcastle` returning 21 current matches whether the role/location values are entered in the normal or reversed boxes. After the final build-time metadata optimisation, live browser testing confirmed that the earlier roughly 4–5 second perceived search wait was removed and search felt very fast, without changing the verified result behaviour.

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

Ontap remains positioned around useful job discovery for ordinary workers in an AI workplace, with sector-switching as an additional route rather than the whole identity.

NHS/public-sector inventory is an advantage for switchers and existing sector workers, but it must remain subordinate to the overall Ontap proposition. Generic regional discovery should not be swamped by NHS: the hard 20% source ceiling and the 4+1 display rhythm both enforce that principle. Explicit NHS/public/charity interest can be surfaced more strongly through user-facing UX without changing the underlying generic-page source ceiling.

## 5. Operations / infrastructure

Core controls are:

- scheduled source refresh/reviews, including the NHS Administrative & Clerical review refresh at 10:05 UTC;
- the twice-daily full JobG8 process, which now refreshes and composes NHS transactionally inside the Service Admin path and generates every currently approved Customer Sales slice from the same feed;
- one master daily owner review;
- one owner-facing apply/publish orchestrator;
- source-specific publishers, including NHS, with the reviewed NHS publisher using the same transactional composer as the normal daily run;
- final verified-page publishing including city-page derivation/maintenance and configured Customer Sales slices;
- normal Vercel Git deployment from `main`, with explicit live-SHA verification;
- manual-only Vercel CLI recovery using `VERCEL_TOKEN` if Git deployment fails;
- Google indexing and operational monitoring.

Every `npm run build` now regenerates the published-job search index before `prisma generate` and `next build`. That generated index contains both the current result-card fields and the precomputed `_search` metadata needed for matching, while omitting the raw description/full-description payload from the runtime search bundle. Search therefore uses the exact published inventory captured by that deployment without rebuilding inventory or normalised/tokenised field structures on individual search requests.

A successful `Publish verified pages` run automatically triggers `.github/workflows/deploy-vercel-after-publish.yml`. That workflow checks out current `main`, captures the expected SHA, and waits up to three minutes for normal Vercel Git integration to deploy that commit or a newer descendant. It verifies production through `https://www.ontapjobsearch.com/api/deployment-version`.

If normal Git deployment succeeds, the workflow finishes green and all CLI recovery steps are skipped. This behaviour was confirmed in production on 20 August 2026. If production does not catch up within the wait window, the automatic workflow fails and raises/updates the GitHub Issue **Ontap production deployment is stale**; it does **not** automatically perform a second deployment.

Manual dispatch of `Deploy Ontap production after publish` is the recovery route. Only a manually dispatched run may use the `VERCEL_TOKEN` repository secret to call the Vercel CLI and deploy current `main` directly, followed by the same live-SHA verification. The old Vercel Deploy Hook has been revoked and `VERCEL_DEPLOY_HOOK_URL` removed; Deploy Hooks are no longer part of production publication.

Vercel is now on **Pro**. The upgrade was made on 21 August after the Hobby build-rate ceiling refused to start a valid deployment; once upgraded, the pending `main` search fix deployed successfully through the same Git integration. This changes capacity, not architecture.

This makes normal Git→Vercel deployment the single automatic production route, while retaining an explicit manual fallback without creating routine duplicate deployments.

The Google Indexing API retains its 200-notification safety limit and GitHub Issue alerting.

## Business rule

**Business priority wins over technical tidiness.** Cleanup is justified where it improves reliability, delivery speed, cost, UX, indexing/discoverability, AI discoverability or safe inventory growth — not simply because a cleaner-looking architecture is possible.

## Current state

Architecture cleanup 1–5 is merged into `main`. The six additional Service Admin regional slices are LIVE. Bradford, Huddersfield, York, Barnsley and Doncaster Service Admin are approved permanent city pages using the shared city-page mechanism. Active city routes remain permanent below four jobs but are hidden from the homepage until they return to 4+. Homepage browse ordering is regional-first, then city. Durham remains deliberately held pending the County Durham geography safeguard. Production deployment uses normal Vercel Git integration automatically, with CLI recovery manual-only, and Vercel is now on Pro. NHS Administrative & Clerical inventory is live inside Service Admin through the shared transactional composer, with untouched POSS rows fail-closed, a hard 20% regional source ceiling and 4+1 non-dominating display order. NHS detail formatting is live. Search now uses a deployment-time precomputed search index with `_search` metadata rather than request-time route scanning or repeated field normalisation/tokenisation; high-confidence typo correction and weighted field interpretation remain verified on the Great Lumley and Newcastle/admin cases, and the final live browser retest confirmed the earlier search delay was removed. Customer Sales / Sales Advisor is LIVE for **London, Greater Manchester - Manchester & Salford and Yorkshire - West only**. Its first production publish was verified end-to-end at **20, 6 and 7 current jobs respectively**, with all three public routes returning 200 and JobG8-backed Apply actions present. All other Customer Sales regions remain non-LIVE until separate evidence and explicit approval.
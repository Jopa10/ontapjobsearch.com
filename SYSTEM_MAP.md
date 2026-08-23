# Ontap System Map

**Last updated:** 23 August 2026  
**Status:** Canonical production architecture after cleanup, regional/city expansion, deployment-path verification, NHS Administrative & Clerical integration, search/UX hardening, Customer Sales production launch, 78-market UK geography governance and three-family live/diagnostic regional reporting with rolling history.

This is the authoritative technical map of the persistent Ontap system. It is organised into five canonical buckets. Facts not verified from the repository are marked `UNKNOWN / NEEDS AUDIT` rather than inferred from chat history.

## Recent canonical changes

- 23 August 2026 — **Legal Assistant / Paralegal boundary refinement:** owner-confirmed standalone conveyancing fee-earner roles are OUT of the family; explicit Team Leader titles are also OUT as management. Genuine paralegal roles remain eligible even where they manage files or a caseload, and mixed `Paralegal/Fee Earner` titles remain under advert-level review rather than being automatically rejected. Current content-unique evidence after the standalone fee-earner rule is 226 LIKELY_IN + 2 BORDERLINE (~227 genuine nationally); 120 active jobs are paralegal-titled, including 20 mixed Paralegal/Fee Earner titles.
- 23 August 2026 — **Shared Claims-style family content fingerprint:** reusable family discovery uses the already-proven Claims normalization for content uniqueness (normalized title + first 1,200 description characters + location), so family scale evidence is consistent rather than maintaining a separate Legal-specific fingerprint definition.
- 23 August 2026 — **Discovery geo safeguard for generic `City`:** JobG8 `Area=City` is treated as non-authoritative by reusable family discovery because current feed evidence showed named Sheffield, Leeds, Manchester, Birmingham and Belfast vacancies being falsely inherited into the lookup `City → London` route. Discovery now prefers the specific Location fallback for these rows; when no safe fallback exists it remains unresolved rather than being forced to London. The canonical `geo_lookup.xlsx` remains the factual lookup authority and is not globally rewritten by this diagnostic safeguard.
- 23 August 2026 — **Content-unique new-family evidence:** reusable family discovery now retains every source row and reference-level duplicate flag for audit, but also calculates a normalized advert-content fingerprint so the same vacancy syndicated under different JobG8 display references is counted once. National viability, 78-market recurrence, proof-region evidence and reusable boundary-review queues all use the content-unique advert set.
- 23 August 2026 — **Reusable family proof-region evidence:** the governed discovery workflow now runs `jobg8_family_proof_region_evidence.py` after national discovery and 78-market recurrence. It emits the five strongest current markets with LIKELY_IN/BORDERLINE/OUT counts, title mix and advert excerpts for human boundary inspection. This is diagnostic evidence only: it does not approve proof regions or activate public slices.
- 23 August 2026 — **Reusable family discovery and Legal boundary refinement:** `jobg8_family_discovery.py` is now family-neutral and 78-market aware; the shared discovery workflow auto-runs on governed family config, canonical UK geography and `geo_lookup.xlsx` changes. It now also runs `jobg8_family_recurrence.py`, producing a complete 78-market LIKELY_IN/BORDERLINE spread report with descriptive 3+/6+/9+ evidence that never auto-activates a slice. `jobg8_family_boundary_review.py` supports both legacy Claims diagnostics and reusable family-discovery outputs. Legal Assistant / Paralegal passed the national scale gate and its first evidence-led boundary refinement removed generic claims/caseworker/case-handler noise, legal cashier/finance contamination and qualified-lawyer/specialist titles; observed Legal PA/support, conveyancing, probate and exact `Legal Asistant` source-typo variants are covered.
- 23 August 2026 — **Claims recurrence geography correction:** `jobg8_claims_slice_viability.py` now uses the canonical 78-market `uk_assessable_regions.json` universe and its exact detail roll-ups instead of the obsolete 33-region assumption. Claims remains discovery/diagnostic evidence only and is not LIVE.
- 23 August 2026 — **LIVE regional headline geo-rollup fix:** `pipeline/scripts/build_daily_region_overview.py` now applies `uk_assessable_regions.json` detail/alias roll-ups to LIVE Service Admin and Support Worker counts before rendering canonical-market rows and headline totals. This fixes the North East case where factual JobG8 detail rows were previously omitted from the aggregate `North East` LIVE count while NEJobs/VONNE aggregate rows were counted. The 23 August corrected snapshot is **North East Service Admin 86** and **Service Admin headline 1,357**; Support Worker remains 64 and Sales Advisor 34. `pipeline/tests/test_build_daily_region_overview.py` guards direct-plus-detail roll-up behaviour, and the overview workflow runs that regression test before rebuilding the report.
- 23 August 2026 — **Reduced repeat owner editing without weakening decision persistence:** the England-wide Teaching Vacancies Markdown now generates editable blocks only for LIVE, non-hard-pass rows whose `manual_action` is still blank. Remembered `select` / `exclude` decisions remain in the complete master CSV and regional approval state, and cross-day carry-forward reads those resolved actions from the generated CSV while still accepting new edits from Markdown. The Service Admin title classifier now hard-passes Paraplanner/Paraplanning title variants before candidate/manual-review generation as specialist financial-planning work.
- 22 August 2026 — **UK geography scope correction, reconciled against the full 104-label geo lookup inventory:** the earlier 55-market result was England-only and the interim 73-market UK pass still missed five legitimate lookup markets. `pipeline/config/uk_assessable_regions.json` is now the canonical diagnostic geography authority with **78 UK markets: 58 England + 10 Scotland + 8 Wales + 2 Northern Ireland**. The five recovered markets are **Lancashire - West, Merseyside - Sefton, Merseyside - St Helens & Knowsley, Scotland - Borders and Wales - Mid**. The 55-market England file is retained as historical subset evidence, not the current national authority. `geo_lookup.xlsx` remains factual location authority; exact aliases roll up, while Channel Islands, unknown and ambiguous generic labels stay outside the governed market universe. Daily three-family diagnostics target **234 rows (78 × 3)**. LIVE/public approval remains separately controlled by the catalogue/register.
- 22 August 2026 — Following the 55-region city audit, the owner explicitly approved a one-off waiver of the city 3-of-7 history requirement for nine high-supply Service Admin localities that were present in dynamic configured-slice output but absent from the standing city scanner's history. The common city-page framework now owns permanent exact-city routes and derived output for **Bristol 38, Manchester 35, Cambridge 27, Birmingham 24, Peterborough 14, Warrington 14, Liverpool 12, Hull 11 and Oxford 10**. Each register entry records `launch_approval_date` and `launch_approval_basis`; the normal 6-current/3-of-7/explicit-approval rule remains canonical for future launches.
- 22 August 2026 — Geography reconciliation established that the former **33-region England footprint was a configured operational subset, not exhaustive geography**. `pipeline/config/england_assessable_regions.json` now governs the complete **55-market England diagnostic universe**: the previous 33 plus the exact 22 omitted non-North-East lookup markets. `geo_lookup.xlsx` remains the factual area-to-region authority; `job_slice_catalog.json` remains configured/public market metadata rather than the geography authority; and `region_category_slice_register.csv` remains the explicit LIVE activation gate. The three family diagnostics therefore produce **165 region/family rows (55 × 3)**. `North East` remains the deliberate roll-up of all three underlying lookup regions, including Tees Valley. This reconciliation changes diagnostic completeness only: it does not create LIVE slices, remove/rename public URLs or auto-publish any of the 22 additional markets.
- 22 August 2026 — **Service Admin standing launch rule:** a governed same-feed Service Admin count **over 8** is immediate owner approval for LIVE. A count of 8 or below remains NOT LIVE and stays on the normal 55-market rolling evidence. Applying that rule to the recovered geography launched 11 additional Service Admin markets: Cheshire - East, Cheshire - Warrington & Halton, Cornwall, Derbyshire, Greater Manchester - Wigan & Bolton, Leicestershire, Lincolnshire, Merseyside - Liverpool, Shropshire, Suffolk and West Midlands - Black Country. The launch used the existing catalog/register/configured-slice and verified-publish mechanisms; no previously live public URL was removed or renamed.
- 22 August 2026 — The three-family regional diagnostic now retains a rolling **14 feed-date history** in `pipeline/reports-daily/daily-family-coverage-history.json`, seeded from the current 22 August snapshot with no historical backfill. Each new or replaced 55-market snapshot stores all 165 region/family counts; the history reader remains migration-safe if an earlier 33-market snapshot is still present; a later run on the same feed date replaces that date rather than adding a duplicate; only the latest 14 feed dates are retained. `daily-region-overview.md` uses the rolling values only for NOT LIVE slices and renders each diagnostic cell as **today / 14d average / days at 6+**. The 6+ measure is decision-support/watch evidence only and never changes the explicit LIVE register.
- 22 August 2026 — Same-feed regional diagnostics now cover **Service Admin, Support Worker and Customer Sales / Sales Advisor across all 55 assessable England markets**. `pipeline/reports-daily/daily-family-coverage.csv` is now **165 rows (55 × 3)**, replacing the prior 99-row snapshot from the configured 33-market footprint. Customer Sales diagnostics reuse the governed production classifier, canonical geo, campaign dedupe and final production QA; they do not write public slices or alter the LIVE register. `daily-region-overview.md` now uses those persisted counts for NOT LIVE Sales Advisor cells, while LIVE Sales counts remain sourced from the actually published configured-slice JSON. Numeric NOT LIVE counts are current expansion evidence. They do not auto-activate Support Worker or Customer Sales; Service Admin is the standing exception, where a governed same-feed count over 8 is immediate owner approval for LIVE.
- 22 August 2026 — The 22 August production cycle itself completed correctly, including Customer Sales publication at **London 20, Greater Manchester - Manchester & Salford 6, Yorkshire - West 7**, but `pipeline/reports-daily/daily-region-overview.md` remained on the 21 August snapshot because its `workflow_run` trigger listened to the nested `Publish verified pages` workflow. PR #227 changed the completion trigger to the owner-facing **Apply and publish Ontap daily review** workflow, which is the reliable end-of-cycle signal after the guarded source publishers and shared verified publish finish. PR #231 then also added successful **Run full JobG8 daily process** completion as a direct overview trigger, so new same-feed diagnostic evidence is surfaced without relying on a `GITHUB_TOKEN`-generated push to start another workflow. Manual and relevant push triggers remain available as recovery/maintenance paths.
- 22 August 2026 — The Teaching Vacancies regional/master refresh was hardened against concurrent `main` writes after the 22 August run completed discovery, routing and review generation but its final plain `git push origin main` was rejected because `main` had advanced during the run. `.github/workflows/run-teaching-vacancies-regional-review.yml` now checks out full history and uses up to three `git pull --rebase origin main` + `git push origin HEAD:main` attempts, aborting safely if it still cannot reconcile. A post-fix rerun successfully committed fresh 22 August Teaching Vacancies evidence to `main`, removing the stale 19 August source state without overwriting concurrent work.
- 21 August 2026 — The daily regional overview now treats **Customer Sales / Sales Advisor as a first-class LIVE family** rather than test-only. The current verified snapshot is **3 / 55 LIVE markets and 33 LIVE jobs**: **London 20, Greater Manchester - Manchester & Salford 6, Yorkshire - West 7**. LIVE Sales counts are read from the current published Customer Sales configured-slice JSON; from 22 August, NOT LIVE Sales regions also receive same-feed governed diagnostic counts in the overview rather than unassessed `—` cells.
- 21 August 2026 — Customer Sales / Sales Advisor completed proof-region testing, governed national validation and the then-configured 33-market diagnostic assessment; the 22 August geography reconciliation subsequently extended recurring diagnostics to 55 assessable England markets without changing LIVE approval. Explicit LIVE approval is limited to **London**, **Greater Manchester - Manchester & Salford**, and **Yorkshire - West**. The first verified production publish completed successfully on 21 August with **20 London jobs, 6 Manchester & Salford jobs and 7 Yorkshire - West jobs**. All three public `/job-search/.../customer-sales-jobs` routes returned HTTP 200, rendered job-detail links and exposed the expected JobG8-backed Apply actions. These counts are a launch snapshot, not automatic activation/deactivation thresholds. Production generation is integrated into the existing JobG8/configured-slice/verified-publish chain; genuine Sales/Service Admin overlap remains valid. North East and all other Customer Sales regions remain non-LIVE diagnostics until separately approved.
- 21 August 2026 — NHS job-detail presentation now preserves the source vacancy text while rendering it as readable headings, paragraphs and bullets instead of a flattened text dump. Long NHS descriptions show the first six presentation blocks and place the remainder behind `Show full NHS role information`; this is presentation-only and does not rewrite/summarise the vacancy.
- 21 August 2026 — Regional Service Admin display ordering now treats NHS as a complementary stream after composition: non-NHS jobs retain the normal location-first scan, NHS jobs retain Tier A/B → switchability → freshness priority, and at most one NHS role is inserted after each four non-NHS roles. The upstream hard 20% NHS source ceiling remains unchanged and is not replaced by the display rhythm.
- 21 August 2026 — `/jobs/search` now supports multi-field one-box matching across title, employer/advertiser, location, region and curated category. Role-like terms are protected from accidental geography inference even when source location data contains job-title prose. High-confidence spelling correction, browser spellcheck/autocorrect and cached spelling vocabularies/results are live; the search route prefers Vercel London (`lhr1`) to reduce UK latency.
- 21 August 2026 — Search inventory is now generated once at build/deployment time by `scripts/generate-search-index.ts` into `generated/published-jobs-search.json`; the request path no longer recursively walks and parses the published route JSON tree. The two search fields are explicitly labelled, `office`/`clerical` are treated as admin intent internally, and weighted role-vs-geography evidence recovers accidentally swapped role/location inputs without allowing a few polluted source fields to dominate interpretation. Production verification includes `lumley office`, typo `lumley offcie`, and both orientations of `admin` + `newcastle`.
- 21 August 2026 — Final search-performance optimisation now precomputes normalised/tokenised per-job `_search` metadata during the build. Runtime search consumes that metadata directly, reuses cached corpus-level geography data, and no longer carries raw description/full-description payload in the search bundle; the precomputed searchable description representation remains available, so matching semantics are preserved. Live browser retest confirmed the previous roughly 4–5 second perceived search delay was removed.
- 21 August 2026 — Vercel was upgraded from Hobby to Pro after the Hobby build-rate limit blocked a production deployment. The deployment architecture itself is unchanged: `main` still deploys through normal Vercel Git integration, with the existing manual-only CLI recovery path.
- 21 August 2026 — NHS Jobs Administrative & Clerical inventory is now a live Service Admin source. Fresh NHS inventory is classified and routed through the existing LIVE Service Admin geography, composed transactionally with current non-NHS output, capped at a hard maximum 20% of each regional Service Admin page, and published through the common verified-page path.
- 21 August 2026 — NHS selection is governed by title classification and switchability: HC Tier A ranks before Tier B; within equivalent quality, OPEN/PURE SWITCH ranks before BRIDGEABLE/POSSIBLE and NHS-experience-needed roles; freshness is a later tie-breaker. Unreviewed POSS rows remain fail-closed and are not required in the normal daily owner edit queue.
- 21 August 2026 — The main JobG8 daily workflow and the standalone reviewed NHS publisher now use the same transactional composer, `pipeline/external_sources/compose_nhs_admin_daily.py`. It refreshes current NHS inventory, restores valid remembered decisions, enriches only rows that survive routing/dedupe/cap, verifies non-NHS preservation and required fields, then replaces NHS review/output files only after validation succeeds.
- 21 August 2026 — The Review Hub treats untouched NHS POSS rows as optional review opportunities rather than unresolved failures. Hundreds of untouched NHS POSS rows therefore do not isolate NHS; automatically accepted HC rows can continue to publish under the 20% cap.
- 20 August 2026 — Added canonical governance for discovering and activating new job families: discovery audit → family boundary → proof-region review → title register/refinement rules → national validation → diagnostic assessment across the governed assessable geography → explicit LIVE-slice approval → integration into the existing daily/publish mechanisms. The assessable geography was corrected from the configured 33-market footprint to the complete 55-market England universe on 22 August. Family membership is non-exclusive where a job genuinely fits more than one user-facing family.
- 20 August 2026 — Confirmed the production deployment model by live test: normal Vercel Git integration is the single automatic deployment route for `main`; `Deploy Ontap production after publish` waits up to three minutes for production to reach the expected SHA and fails/alerts if it does not. `VERCEL_TOKEN`/Vercel CLI is manual recovery only. The obsolete Deploy Hook was revoked and the `VERCEL_DEPLOY_HOOK_URL` repository secret removed.
- 19 August 2026 — Homepage browse ordering now presents regional slices before city pages. Regional inventory is the primary breadth signal; city pages remain a secondary local layer, still subject to the 4-job homepage visibility floor.
- 19 August 2026 — Added a separate city homepage visibility floor: active city pages remain permanent, but homepage city cards appear only at 4+ current jobs. The launch threshold remains 6 jobs with 3 of 7 qualifying runs plus explicit approval.
- 19 August 2026 — Approved five additional Service Admin city pages: Bradford, Huddersfield, York, Barnsley and Doncaster. Initial include rules are exact-city only; the shared city-page framework owns derivation and permanence.
- 19 August 2026 — Added explicit city catchment governance: city pages represent city-anchored local employment/commuting markets, not literal exact-name-only filters. Catchment expansions require explicit include/review/exclude rules in `pipeline/city_pages/city-page-register.json`.
- 19 August 2026 — Durham Service Admin remains HOLD because the original registered opportunity pattern `durham` could also match broad `County Durham` locations. The 22 August city audit added `exclude_patterns: ["county durham"]`; Durham still requires clean post-fix history before activation.
- 19 August 2026 — Activated six additional Service Admin regional slices: Buckinghamshire, Greater Manchester - South, Hertfordshire, Somerset, West Midlands - Birmingham & Solihull, and Yorkshire - East.
- 19 August 2026 — Added the first same-feed family coverage for Service Admin and Support Worker across the then-configured 33-market footprint; this was expanded to the complete 55 assessable England markets on 22 August.
- 19 August 2026 — Added publication failure isolation and made external-source publishing fail-soft where safe.
- 19 August 2026 — Merged architecture cleanup 1–5 into `main` via PR #211.

## 1. Pipeline

Purpose: how job data moves from source to published/indexed output.

Canonical stages:

`source → ingest → classify/select → review → approved output → compose → verified publish → app JSON → city derivation → Vercel Git deployment → live SHA verification → index`

### Main scheduled JobG8 path

Primary scheduled entry point: `.github/workflows/run-full-jobg8-daily-process.yml`.

It runs at 07:30 and 15:30 Europe/London and performs:

`JobG8 feed → pipeline/input/jobg8.xlsx → validation + duplicate report → LIVE slice register → service-admin/support-worker selectors → registered category selectors + Customer Sales selector → approved external-source composition → fresh transactional NHS composition → metadata enrichment → three-family 55-market diagnostic coverage → current coverage + rolling history → pipeline outputs/reports`

`pipeline/input/jobg8.xlsx` is transient workflow input and is not committed. The validated raw feed is retained durably in S3 under `jobg8/raw`.

Geography governance is layered deliberately:

- `pipeline/geo/geo_lookup.xlsx` maps factual source locations to Ontap lookup regions;
- `pipeline/config/england_assessable_regions.json` defines the complete 55-market England universe used by recurring family diagnostics and the regional overview;
- `pipeline/config/job_slice_catalog.json` supplies configured market/category route metadata and must not be treated as exhaustive geography;
- `pipeline/registers/region_category_slice_register.csv` is the explicit LIVE/CANDIDATE/other slice-state gate.

Absence from the configured/LIVE layer must never turn a successfully geo-mapped job into `unknown`. The diagnostic order is **resolve full geography → count every assessable market → apply explicit aggregate mappings → overlay configured/LIVE state**. The public/assessment `North East` market rolls up Tyneside/Wearside/Northumberland, County Durham/Darlington/Hartlepool and Tees Valley.

The daily coverage pass reuses the same materialized JobG8 workbook and governed family rules across all 55 assessable England markets. It persists the current Service Admin, Support Worker and Customer Sales diagnostic counts in `pipeline/reports-daily/daily-family-coverage.csv`. It also records the feed date in `pipeline/reports-daily/daily-family-coverage-history.json`: 55-market runs store all 165 region/family counts, same-date reruns replace the prior snapshot, and earlier pre-expansion snapshots may contain the former 99-count footprint until replaced or aged out; and only the latest 14 feed dates are retained. The history begins on 22 August 2026 with no backfill. For Customer Sales, the diagnostic path mirrors the production classifier, canonical geo, campaign dedupe and final QA without writing public slice output. Coverage and history are evidence only for Support Worker and Customer Sales. For Service Admin, a governed same-feed count over 8 is the standing owner-approved LIVE trigger; 8 or below remains on rolling evidence.

The Service Admin LIVE set is now **41 / 55 assessable England markets**. In addition to the six 19 August evidence-led activations, the 22 August >8 standing rule added 11 recovered markets: Cheshire - East, Cheshire - Warrington & Halton, Cornwall, Derbyshire, Greater Manchester - Wigan & Bolton, Leicestershire, Lincolnshire, Merseyside - Liverpool, Shropshire, Suffolk and West Midlands - Black Country.

Customer Sales production generation is owned by `pipeline/scripts/customer_sales_pipeline.py`. It reads the central LIVE slice register and therefore generates only explicitly approved Customer Sales regions. Output files use the shared `pipeline/output-admin-service/` staging area with the `customer-sales` suffix so the existing daily commit and verified-page mechanisms carry them without a parallel workflow. The first live verified-publish snapshot produced **London 20, Greater Manchester - Manchester & Salford 6, and Yorkshire - West 7**. Those numbers are normal inventory-state evidence only; LIVE status is controlled by the explicit slice register and does not switch automatically because a daily count moves above or below the launch snapshot.

### NHS Administrative & Clerical integration

NHS Jobs is a production source for Service Admin, not a separate user-facing job family.

Canonical components:

- `pipeline/external_sources/nhs_admin_inventory.py` — fetch current NHS Administrative & Clerical inventory;
- `pipeline/external_sources/nhs_admin_service.py` — classification, routing, dedupe, ranking, cap and composition rules;
- `pipeline/external_sources/nhs_review_actions.py` — remembered manual decision ledger/reapply behaviour;
- `pipeline/external_sources/compose_nhs_admin_daily.py` — transactional production composer used by both the normal daily path and reviewed NHS publisher;
- `pipeline/reviews/external/nhs-jobs-review.csv` — current detailed NHS review state;
- `pipeline/reviews/external/nhs-jobs-summary.md` — current NHS review summary;
- `pipeline/reviews/external/nhs-jobs-decisions.csv` — remembered valid manual decisions;
- `.github/workflows/refresh-nhs-admin-service-review.yml` — scheduled 10:05 UTC review refresh plus manual dispatch;
- `.github/workflows/publish-reviewed-nhs-admin-service.yml` — source-specific reviewed NHS publisher.

Classification state is fail-closed:

- HC Tier A and Tier B rows can be automatically selected when otherwise publishable;
- HARD_PASS rows are excluded;
- unseen/ambiguous titles default to POSS/BRIDGEABLE and do not publish unless a valid remembered/manual select decision exists;
- ambiguous title overrides are governed centrally rather than silently promoted.

Ranking priority is:

1. HC Tier A before Tier B;
2. within equivalent quality, OPEN/PURE SWITCH before BRIDGEABLE/POSSIBLE before NHS-experience-needed;
3. freshness after quality/switchability.

NHS is a complementary source. **20% is a hard ceiling, not a target.** Composition must never exceed 20% NHS share in an eligible regional Service Admin output.

User-facing ordering is a separate presentation rule after composition. `lib/job-display-order.ts` keeps non-NHS inventory location-first and keeps the accepted NHS subset in the same Tier A/B → switchability → freshness order, then inserts no more than one NHS job after each four non-NHS jobs. This prevents NHS bunching near the top while preserving both the source cap and NHS quality ranking.

`compose_nhs_admin_daily.py` is transactional. It works in temporary state first, preserves current non-NHS rows exactly, refreshes current NHS inventory, reapplies valid remembered decisions, pre-composes against current Service Admin output, enriches descriptions only for NHS rows that survive classification/routing/dedupe/cap, verifies required apply URLs/descriptions and the 20% ceiling, then replaces the real NHS review/output files only after all checks pass.

The normal daily JobG8 workflow invokes this composer before Service Admin metadata enrichment. The reviewed NHS publisher invokes the same composer rather than maintaining a parallel implementation, then runs the common verified Service Admin page publisher.

The unified Review Hub deliberately does **not** require the large NHS POSS population to be edited every day. Untouched NHS POSS rows are omitted from the normal mandatory owner edit queue and stay fail-closed; their volume does not isolate NHS or block automatically accepted HC rows.

### New job-family discovery and activation governance

A new job family must not move directly from a broad title/regex discovery result into production slices. The canonical lifecycle is:

1. **Discovery audit** — use the current feed, specialist analysis or one-off diagnostics to identify a plausible occupational seam and estimate its scale. Discovery rules are evidence gathering, not publish rules.
2. **Define the family boundary** — state the jobseeker proposition in occupational terms: what belongs, what does not, and the important ambiguous/overlap cases.
3. **Proof-region review** — inspect real jobs in a small number of representative regions before national rollout. The objective is page quality and false-positive/false-negative discovery, not simply volume.
4. **Create governed classification state** — encode recurring title decisions in the appropriate central title register and add contextual/refinement rules where title alone is insufficient. Do not leave persistent family logic as an ad-hoc regex report.
5. **National validation** — apply the candidate selector to the full current feed and review selected/rejected examples, scale, specialist contamination, salary/context effects and material false positives/negatives.
6. **55-market diagnostic assessment** — once the selector is credible, assess every canonical region using the same family logic. For Support Worker, Customer Sales and future families without a separate owner rule, this is decision evidence only. Service Admin has a standing owner rule: a governed same-feed count over 8 is already approval to proceed to LIVE activation.
7. **LIVE-slice activation** — for Service Admin, apply the standing >8 owner approval through the normal catalog/register/publish mechanisms; 8 or below stays NOT LIVE and tracked. Other families require separate explicit owner approval based on quantity, page quality and the family-specific evidence rule.
8. **Integrate, do not parallel-build** — once approved, the family must use the existing shared ingest, registers/config, review, publishing, reporting and website mechanisms wherever those mechanisms can be extended safely.

Family classification is **not required to be mutually exclusive**. A single underlying job may legitimately qualify for more than one Ontap family when it genuinely serves both user intents. Each family applies its own eligibility/refinement rules. Duplication should be suppressed only where the same job would otherwise appear redundantly in one user-facing result set; a job must not be removed from one valid family merely because it also qualifies for another.

Customer Sales / Sales Advisor has completed this lifecycle through explicit LIVE-slice approval. The approved production set is **London**, **Greater Manchester - Manchester & Salford**, and **Yorkshire - West** only. `pipeline/config/job_slice_catalog.json` defines the `customer_sales` category and route metadata; `pipeline/registers/region_category_slice_register.csv` is the activation gate; `pipeline/scripts/customer_sales_pipeline.py` owns production classification and campaign dedupe; and the existing config-driven verified publisher owns public materialization. Direct office/contact-centre/home/hybrid sales roles qualify; customer/service roles require explicit sales/conversion evidence; generic Account Manager/Account Executive roles require strong sales plus office/digital evidence. Field/in-home/event/self-employed, automotive dealership/showroom, retail/property and senior/specialist contamination is excluded. Legitimate Sales + Service Admin crossover remains valid. The first production publish was verified end-to-end at **20 / 6 / 7 jobs respectively**, with all three public routes returning 200 and JobG8-backed Apply actions present. **North East and every other Customer Sales region remain non-LIVE diagnostic candidates until separately approved.** Their diagnostic counts are refreshed during every full JobG8 run and surfaced in the daily regional overview; this reporting does not bypass the explicit activation gate.

### Owner review / approved publication

Owner-facing orchestrator: `.github/workflows/apply-publish-ontap-daily-review.yml`.

It reconciles the master review, applies valid decisions back to source-owned review files, dispatches source-specific approved publishers, and invokes `publish-verified-pages.yml` when the shared final publish is required.

Publication isolation is hierarchical:

- up to 15 unresolved/malformed **mandatory-review** jobs in one source are withheld fail-closed while clean jobs continue;
- more than 15 such mandatory-review jobs, or a source-level integrity mismatch, isolates that source and retains its previous approved state;
- NHS untouched POSS rows are optional review opportunities and therefore do not count toward that isolation threshold;
- source publisher failures are fail-soft where the prior approved state can safely be retained;
- only a genuine combined/publication integrity failure should stop the whole publish.

Confirmed source paths include JobG8, NEJobs, VONNE, Teaching Vacancies and NHS Jobs.

Source freshness is owned upstream of the apply/publish orchestrator. If an active source review is stale or missing, the master review flags `NOT READY TO REVIEW`, excludes that stale source from the current master-review jobs, and must not treat its absence as zero inventory. A stale source does not by itself convert a later apply/publish run into a system-level failure: clean sources can continue under the isolation model. In particular, the parent apply/publish workflow does not refresh Teaching Vacancies; fresh TV state is produced by `run-teaching-vacancies-regional-review.yml`.

The England-wide Teaching Vacancies Markdown is a pending-edit queue, not the full decision register. It shows only LIVE, non-hard-pass rows with a blank `manual_action`; previously resolved `select` / `exclude` rows remain in the master CSV and regional approval state and continue to carry forward only while their stable ID and factual fingerprint still match.

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

Recorded exception: on 22 August 2026 the owner directly approved Bristol, Manchester, Cambridge, Birmingham, Peterborough, Warrington, Liverpool, Hull and Oxford Service Admin after the 55-region audit. Their current exact-city counts materially exceeded the six-job floor, but their dynamic configured-slice parents had not been included in the city scanner's seven-run history. This was a named one-off waiver, not a change to the standing gate.

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

Broad county/region labels are not proof of city membership. **Durham is the explicit safeguard case:** `opportunity-market-register.json` now excludes `County Durham` from Durham-city evidence. Durham Service Admin remains HOLD until its seven-run history is rebuilt from clean post-fix counts.

Approved on 19 August 2026 with exact-city launch catchments:

- Bradford Service Admin — `/bradford/service-administrator-jobs`;
- Huddersfield Service Admin — `/huddersfield/service-administrator-jobs`;
- York Service Admin — `/york/service-administrator-jobs`;
- Barnsley Service Admin — `/barnsley/service-administrator-jobs`;
- Doncaster Service Admin — `/doncaster/service-administrator-jobs`.

Approved as the recorded 22 August 2026 one-off exception, also with conservative exact-city launch catchments:

- Bristol — `/bristol/service-administrator-jobs`;
- Manchester — `/manchester/service-administrator-jobs`;
- Cambridge — `/cambridge/service-administrator-jobs`;
- Birmingham — `/birmingham/service-administrator-jobs`;
- Peterborough — `/peterborough/service-administrator-jobs`;
- Warrington — `/warrington/service-administrator-jobs`;
- Liverpool — `/liverpool/service-administrator-jobs`;
- Hull — `/hull/service-administrator-jobs`;
- Oxford — `/oxford/service-administrator-jobs`.

### External-source review paths

Recurring review workflows:

- NEJobs — 06:15 daily;
- VONNE — 06:35 daily;
- Teaching Vacancies regional/master review — 06:55 daily; its review/manifests writeback uses rebase-and-retry protection against concurrent `main` updates;
- NHS Administrative & Clerical review — 10:05 UTC daily, with the production composers also refreshing NHS inventory themselves before composition.

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
- `pipeline/reports-daily/daily-family-coverage.csv` — current same-feed Service Admin, Support Worker and Customer Sales coverage across all 55 assessable England markets (165 region/family rows);
- `pipeline/reports-daily/daily-family-coverage-history.json` — rolling latest-14-feed-date history of all 165 diagnostic counts; one snapshot per feed date, with same-date reruns replacing rather than duplicating;
- `pipeline/reports-daily/daily-region-overview.md` — regional live/not-live overview; NOT LIVE family cells display `today / 14d avg / 6+ days`, while LIVE cells retain production-state reporting;
- `pipeline/reports-daily/live-job-source-count-YYYY-MM-DD.csv` — current provider/source counts, including NHS Jobs after verified publication;
- `pipeline/reports/city-opportunities-current.md` and `.json` — current city/local-market opportunity state;
- `pipeline/reports/city-opportunity-history.json` — rolling qualification history.

The rolling family history begins on **22 August 2026** with no backfill. All 165 counts are stored even though rolling metrics are displayed only for NOT LIVE slices, so evidence remains continuous if a slice later changes LIVE state. The `6+ days` metric is a simple consistency/watch signal and is not an automatic publish threshold. Service Admin's separate standing rule is based on the **current governed same-feed count over 8**, not on the 6+ history metric.

Customer Sales national/55-market assessment is recurring diagnostic evidence for non-LIVE regions. The full JobG8 run now produces it from the same current feed using the governed production classifier, canonical geo, campaign dedupe and final QA. A positive count does not activate a region; only the three explicitly approved Customer Sales slices are in production. The 21 August **20 / 6 / 7** first-live counts are a verification snapshot, not a standing publish threshold.

`pipeline/reports-daily/daily-region-overview.md` treats Sales Advisor as both a production family for LIVE reporting and a diagnostic family for NOT LIVE reporting. LIVE rows read the current published `app/_city-pages/configured-slices/**/customer-sales-jobs.json` data directly. NOT LIVE rows read the same-feed Customer Sales counts persisted in `daily-family-coverage.csv` and combine them with the observed history; a numeric `0` means assessed and none survived the governed rules. These non-LIVE values are decision support only and never switch a slice to LIVE automatically.

The city-opportunity scanner is diagnostic/decision support. It must not auto-activate a city page.

Compiler Modules 1, 2 and 3 remain legitimate specialist/manual analysis workflows.

Report lifecycle is recurring operational reporting / deliberate specialist analysis / one-off diagnostics in Actions artifacts or Git history.

## 3. Website / UX

Purpose: user-facing job search, job pages, navigation and presentation.

Verified structure:

- `app/` is the primary application route/data tree;
- `components/` contains reusable UI components;
- `lib/published-jobs.ts` supplies the common published job/detail layer and is also the build-time source for the compact search index;
- `lib/configured-job-slices.ts` reads the configured regional slice catalog/register;
- LIVE dynamic regional/category slices are register/catalog driven;
- `app/_city-pages/configured-slices/` holds dynamic configured-slice data;
- `app/job-search/[region]/...` is the dynamic route family;
- Browse Jobs, `/jobs/search`, job-detail backlinks and the homepage Admin grid consume published dynamic slices through shared mechanisms;
- the approved Customer Sales routes use that same mechanism: `/job-search/london/customer-sales-jobs`, `/job-search/west-yorkshire/customer-sales-jobs`, and `/job-search/manchester-salford/customer-sales-jobs`; production verification on 21 August confirmed all three returned HTTP 200, rendered the expected current inventory and job-detail links, and exposed JobG8-backed Apply actions;
- homepage browse ordering is regional-first, then city, to make regional inventory breadth the primary visual signal;
- `lib/city-page-data.ts` reads `pipeline/city_pages/city-page-register.json` and resolves active city definitions/data;
- public city routes read private derived JSON under `app/_city-pages/...`, preventing duplicate job-detail URLs;
- homepage city cards are filtered independently at 4+ current jobs; this does not change route activation/permanence;
- NHS-sourced jobs use the same Service Admin regional/job-detail routes as other inventory and retain `source: "NHS Jobs"` plus the original NHS apply URL; employer names do not necessarily contain the word NHS;
- `components/JobDescription.tsx` + `lib/job-description.ts` provide presentation-only readable vacancy formatting. NHS flattened source text is split into short paragraphs while structured headings/bullets are preserved; long NHS adverts expose six blocks initially and keep the rest available under `Show full NHS role information`;
- `lib/job-display-order.ts` owns page-level source mixing after composition: normal inventory stays location-first and accepted NHS inventory is interleaved at no more than one after every four non-NHS jobs while preserving NHS Tier/switchability/freshness ranking;
- `scripts/generate-search-index.ts` runs during `npm run build` and writes `generated/published-jobs-search.json` from the current published jobs. Each generated job contains the result-card fields plus precomputed `_search` metadata for title, location, region, category, company, combined structured fields, slice label and searchable description representation. Raw `description`/`full_description` are omitted from the runtime search bundle because their searchable representation has already been built;
- `lib/job-search.ts` owns the guarded matching semantics and can build search metadata for tests/builds. In production it consumes generated `_search` metadata, caches corpus-level geography vocabulary, protects role anchors before geo inference, performs weighted role-vs-location evidence checks, and preserves the existing ranking/typo behaviour without repeatedly normalising/tokenising every job field on each request;
- `/jobs/search` imports the generated index directly, labels its inputs **Role or keyword** and **Location**, applies only high-confidence typo correction, enables browser spellcheck/autocorrect, caches correction vocabularies/results, maps `office`/`clerical` to admin intent for matching, uses weighted role-vs-geo evidence to recover swapped fields, and prefers Vercel region `lhr1` for the UK search route;
- `app/api/deployment-version/route.ts` exposes the deployed Vercel Git SHA for verification.

Approved city routes include Bradford, Huddersfield, York, Barnsley and Doncaster plus the one-off 22 August set: Bristol, Manchester, Cambridge, Birmingham, Peterborough, Warrington, Liverpool, Hull and Oxford Service Admin. Durham has no approved city route.

### Search behaviour rule

Search should be forgiving of rushed user input without becoming semantically loose. Multi-word one-box queries may match across title, company/advertiser, location, region and curated category. When the dedicated location box is empty, geography may be inferred only from tokens that do not have a credible role anchor in titles/categories. If the two labelled fields appear to have been reversed, Ontap compares the weight of role evidence against geography evidence and may reinterpret them rather than returning an avoidable zero; a few polluted source strings must not outweigh the wider evidence. `office` and `clerical` are accepted as admin intent for matching while preserving what the user typed in the displayed query. Fuzzy correction should be high-confidence: short/ambiguous terms or tied candidates are left unchanged rather than guessed.

Performance is part of the governed search behaviour: expensive inventory loading and stable per-job field preparation belong at build/deployment time, not on each user request. Runtime optimisation must preserve the same searchable fields, ranking and forgiving-input semantics rather than gaining speed by narrowing valid results.

### Website refactor rule

Public URLs remain stable unless a concrete business benefit or defect justifies change. Existing indexing/SEO behaviour should be preserved unless the change is intentionally improving it.

## 4. Content / positioning

Persistent product content belongs here when it changes product behaviour. Ontap's broad direction remains a job site for ordinary workers in an AI workplace, with sector-switching as an additional route rather than the entire identity.

NHS/public-sector inventory is a complementary supply and sector-switching advantage; it must not redefine Ontap as an NHS job board. Generic job discovery should continue to mix NHS into the wider inventory under the source cap and the 4+1 display rhythm, while explicit NHS/public/charity interest can be surfaced more strongly through later UX work.

## 5. Operations / infrastructure

Core scheduled workflows include:

- `run-full-jobg8-daily-process.yml` — 07:30 and 15:30 Europe/London; includes fresh transactional NHS Service Admin composition, generation of all currently LIVE Customer Sales slices, same-feed 55-market diagnostic coverage for Service Admin, Support Worker and Customer Sales, and rolling 14-feed-date history maintenance;
- `run-nejobs-review.yml` — 06:15 daily;
- `run-vonne-review.yml` — 06:35 daily;
- `run-teaching-vacancies-regional-review.yml` — 06:55 daily; final review/manifests commit is protected by full-history checkout plus up to three pull-rebase/push attempts so concurrent `main` writes do not strand fresh TV state;
- `refresh-nhs-admin-service-review.yml` — 10:05 UTC daily;
- `ontap-daily-review.yml` — 08:45 Europe/London;
- `build-daily-region-overview.yml` — rebuilds the 55-market overview after successful **Run full JobG8 daily process** completion when new diagnostics/history are available, after successful **Apply and publish Ontap daily review** completion for end-of-cycle production reconciliation, and on relevant report/code pushes or manual dispatch. LIVE Sales counts are sourced from published configured-slice JSON; NOT LIVE family cells combine the current persisted same-feed counts with the rolling history;
- `google-indexing-api.yml` — 19:30 UTC daily.

The owner-facing publication entry point is `apply-publish-ontap-daily-review.yml`. NHS is one of its source publishers. The reviewed NHS publisher uses `compose_nhs_admin_daily.py`, the same transactional composer as the normal daily run, before the shared verified Service Admin page publish. Customer Sales requires no separate production workflow: its output is generated in the main JobG8 chain and published by the common configured-slice verified publisher.

`npm run build` regenerates the published-job search index before `prisma generate` and `next build`. The generated artifact contains the current published result-card fields plus precomputed `_search` metadata and omits the raw advert description/full-description payload from the runtime search bundle. Every Vercel deployment therefore searches the published supply represented by that deployment without reconstructing the source tree or repeatedly normalising/tokenising stable job fields on each request.

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

On 21 August 2026 the Vercel account was upgraded from Hobby to Pro after the Hobby build-rate limit prevented a valid `main` commit from starting a build. After upgrade, the same normal Git integration successfully deployed the pending search fix. This is a capacity/plan change only; it does not introduce another deployment path.

This leaves one automatic route — `main` → Vercel Git integration — plus one explicit manual recovery route. The recovery route cannot create routine duplicate deployments because it does not run automatically.

### Google Indexing API

`google-indexing-api.yml` submits eligible job URLs, caps each run at 200 notifications, persists submission state in `pipeline/manifests/google-indexing-state.json`, and uses GitHub Issues for backlog/safety/failure alerts.

## Validation state

Architecture cleanup 1–5 is merged into `main` via PR #211 and is canonical. Service Admin is now LIVE in **41 / 55 assessable England markets**: this includes the six 19 August regional activations plus the 11 recovered markets launched on 22 August under the standing governed same-feed **>8** rule. The active city-page set, including the nine documented one-off approvals described above, uses the shared production mechanism; Durham remains deliberately unapproved pending the County Durham safeguard. The Vercel production deployment route is verified as normal Git deployment with manual-only CLI recovery, now operating on Vercel Pro. NHS Administrative & Clerical inventory is part of production Service Admin through the shared transactional composer and verified publish route, with a hard 20% regional source ceiling plus non-dominating 4+1 display mixing. NHS detail formatting and forgiving search are live; production search uses a deployment-time precomputed `_search` index rather than request-time file-tree scanning or repeated per-job field normalisation/tokenisation, and remains verified for typo correction, `lumley office`, and both normal/swapped `admin` + `newcastle` inputs. Live browser retest after the final performance optimisation confirmed the earlier several-second perceived delay was removed without changing those results. Customer Sales / Sales Advisor is LIVE for **London**, **Greater Manchester - Manchester & Salford**, and **Yorkshire - West** only. Its generation is integrated into the main JobG8/configured-slice/verified-publish path; the first production publish was verified at **20, 6 and 7 jobs respectively**, with all three public routes returning 200 and JobG8-backed Apply actions present. Every other Customer Sales region remains non-LIVE until a separate explicit approval, but same-feed governed counts for those regions are now persisted and surfaced in the daily overview for expansion decisions. Rolling NOT LIVE family evidence starts on **22 August 2026**, stores all 165 daily counts for continuity, and builds to a maximum 14 observed feed dates without backfill. Teaching Vacancies review writeback resilience was verified on 22 August 2026 after a concurrent-`main` push race: the hardened workflow successfully committed fresh same-day England-wide evidence after rebase/retry protection was added.

## Documentation rule

When a persistent system-level change alters any canonical bucket, update this file in the same change. If live/active/user-facing state changes, update `SYSTEM_OVERVIEW.md` as well.

23 August 2026 — **safe geo lookup gap correction:** `pipeline/geo/geo_lookup.xlsx` remains the factual location-routing authority. Specific missing place mappings found during Legal Assistant / Paralegal discovery were added for Hook Norton, Woolston, Filey, Ware, Longfield, Milford Haven, Otley and Birmingham, plus safe county/location fallbacks where unambiguous. Broad ambiguous values such as `East of England` and bare `Merseyside` remain deliberately unresolved rather than being forced into a canonical market.

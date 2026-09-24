Warning: truncated output (original token count: 22350)
Total output lines: 372

# Ontap System Overview

**Last updated:** 24 September 2026
**Status:** Canonical production state, reconciled on 21 September against the live slice register, city-page register and scheduled workflow definitions.

This is the short owner view of how Ontap is organised. It mirrors the five canonical system buckets in `SYSTEM_MAP.md`.

## Recent canonical changes

- 24 September 2026 — First-time mobile visitors now see Quick View first; desktop visitors continue to start in Detailed View. A previously saved view choice still takes priority.

- 24 September 2026 — AI tips links now carry a checked identifier for the job page they came from. Readers can return to that exact listing; direct visits still offer `Browse current jobs`. The page's search canonical and breadcrumb remain fixed.

- 23 September 2026 — **JobG8 edge cases no longer act as blanket exclusions or whole-run failures:** practical junior/assistant finance, bookkeeping, payroll and legal-office jobs can enter the selector as candidates. Only a clear mandatory ACCA/ACA/CIMA requirement or an existing genuine hard rule excludes automatically; AAT is allowed. Unclear qualification or non-numeric salary wording goes to daily review, and an individual selector error is withheld and logged while the rest of the daily publishing process continues.

- 21 September 2026 — **Location analytics now separates permission, position, timeout and nearby-service failures:** early saved-location return events wait until GA4 is ready, manual fallback attempts are visible, and remembered-location refresh failures are measured without exposing towns or coordinates.

- 18 September 2026 — **Governance currency audit completed:** current-state sections now match the 78-market × eight-family diagnostic process, the 126 LIVE regional/category rows in the slice register, the 54 active governed city routes and the actual JobG8 schedule. Older launch counts remain only where clearly labelled as dated history. The repository README now points developers to the real production architecture rather than the superseded database-first prototype.

- 17 September 2026 — **Traffic reports can now distinguish more real return visits from unexplained Direct traffic:** explicitly identified crawler/browser-automation traffic no longer loads analytics, while ordinary browsers continue to load analytics; no standalone `navigator.webdriver` suppression is used; genuine browser interaction produces a separate qualified-visit signal, and anonymous browser timestamps identify a return after at least 30 minutes without storing identity or location. Existing saved-location return measurement remains active. A tested link generator now adds consistent campaign tags to Ontap links published through controlled channels; normal internal links remain untagged.

- 17 September 2026 — **A LIVE Marketing or HR / Recruitment market may legitimately have zero jobs today:** a properly generated empty list now clears stale vacancies for that market instead of stopping every other JobG8 update. Missing or malformed output still stops publication.

- 17 September 2026 — **NHS maintenance can no longer hold up fresh JobG8 jobs:** when the NHS feed is unavailable or returns a maintenance/malformed response, Ontap retains the last approved NHS vacancies, clearly warns that NHS was isolated, and continues the fresh JobG8 process. Normal NHS refresh resumes automatically when its feed recovers; duplicate and 20% NHS safeguards remain enforced.

- 16 September 2026 — **Live vacancy pages are served as deployment-built static pages again:** the useful personalised expired-job page is now loaded separately only when an expired URL is visited, so it no longer forces every current vacancy through uncached server rendering. Live job URLs, content, Apply behaviour, canonical tags and Google Jobs markup are unchanged; expired URLs retain their 404 status and current-job recovery options.

- 13 September 2026 — **Saved nearby locations now appear immediately on return:** mobile and laptop visitors see their saved town and last nearby-job count without a visible lookup delay; Ontap quietly refreshes the count behind the displayed panel. Older saved preferences show the town immediately and gain the stored count after that first refresh.

- 13 September 2026 — **Job pages no longer emphasise an absence of nearby matches:** if Ontap has no approved suitable job nearby, the main vacancy panel uses the full width and shows a compact all-jobs regional card at its top-right. Pages with suitable matches are unchanged.

- 13 September 2026 — **Unused Quick View duty bubbles and their daily refresh were removed:** current listing rows remain visually unchanged, including sector labels where enabled. Removing the obsolete workflow prevents unnecessary generated commits after JobG8 updates; individual job-page facts are unaffected.

- 11 September 2026 — **The onward-jobs link is shorter on phones:** individual job pages show `More [city or region] jobs` on one line at mobile widths. Desktop keeps the fuller role-and-region description, and the destination is unchanged.

- 10 September 2026 — **Visitors can save a nearby-job location on mobile or laptop:** pressing `Use my location` triggers the browser's permission prompt; Ontap uses the submitted coordinates transiently to choose the nearest approved town and find jobs within 15 straight-line miles. Only that town and region are remembered in the browser for future visits, with Change and Clear controls and a manual town fallback. The panel appears on the homepage, Browse Jobs, regional/city listings and live/expired job pages. On a job page it personalises the existing governed suitable-job recommendations without changing Apply or `Tap to search other jobs`.

- 8 September 2026 — **Google indexing notifications now share a strict daily allowance:** updates and deletions are selected against one persisted 200-notification Pacific-day ledger, with duplicate attempts suppressed and deletion cleanup retained. The 21 September policy supersedes the former fixed JobG8 reservation: JobG8 now has priority for all capacity after deletions, while non-paying sources are capped at 10%.


- 7 September 2026 — **Identical live vacancy copies now resolve to one Ontap job URL:** where a provider supplies the same advert under multiple IDs, Ontap selects one stable canonical page for listings, search and the sitemap. The other live URL remains usable but tells Google which single URL to retain. Different vacancies with similar titles remain separate. Existing expired-job sitemap removal and Google deletion notices are unchanged.

- 6 September 2026 — **Twenty-nine new Admin and office town pages are approved and active:** Exeter, Milton Keynes, Farnham, Northampton, Poole, Portsmouth, Stoke-on-Trent, Hemel Hempstead, Basingstoke, Chelmsford, Gloucester, Leicester, Maidstone, Newtownabbey, Plymouth, Sunderland, Worcester, Altrincham, Ashford, Aylesbury, Bedford, Bournemouth, Chester-le-Street, Macclesfield, Rotherham, Scarborough, Shrewsbury, Warwick and Wigston each had at least four current Service Admin jobs in the owner report, bringing the Service Admin city set to 53. Existing and new pages keep their established `/service-administrator-jobs` URLs but now use `Admin and office jobs in [Town]` for search-facing wording. They include exact-town Service Admin and suitable office-family jobs, never Support Worker; Sales Advisor is included only with explicit office/contact-centre evidence. Active pages remain permanent if their counts later fall.

- 6 September 2026 — **Job pages can now recover a precise town from a broad JobG8 location:** when JobG8 supplies only a county or region, Ontap uses a clearly stated workplace town or postcode from the advert only if it agrees with the job's existing approved region. Conflicts and casual place mentions remain unchanged. The current snapshot has 278 safe unique-job improvements, projected to raise exact-locality coverage from 886 to 1,162 after normal verified publication.
- 6 September 2026 — **Mobile pages are less crowded:** the header keeps only `Home` at the right, and vacancy pages show one onward jobs link—city when an exact live city page exists, otherwise region. Desktop navigation and the existing city-plus-region choice are unchanged.
- 6 September 2026 — **Non-London listing pages now use one consistent desktop promotion rail:** three relevant course cards are followed by Ontap's practical AI-help robot card. Mobile users do not see the promotional rail, while London's separately configured layout is unchanged.
- 6 September 2026 — **Every individual job page can now start a fresh search:** laptop users see a compact role/location search strip beneath the primary Apply area; mobile users see a small outlined magnifying-glass control that expands and can be hidden again. Apply remains the dominant action, and searches use Ontap's existing current-job search behaviour.
- 5 September 2026 — **Broad all-role town/city pages are now a permanent site layer:** Nottingham (**13**), Wakefield (**10**), Bolton (**6**), Reading (**6**), Chester (**5**), Durham (**5**), Gateshead (**5**), Northallerton (**5**), Norwich (**5**) and Salford (**5**) launch at `/[city]/jobs`. They combine every current Ontap role/provider, use exact-town supply first, link through a `Home > Jobs > Region > City` breadcrumb and regional-results call to action, and are discoverable from Browse Jobs, the homepage while at 4+ jobs, and the sitemap. Nearby vacancies remain disabled unless a specific approved mapping also passes the 15-mile safeguard.
- 5 September 2026 — **City and regional job pages now link both ways:** each permanent city page shows `Home > role > region > city` near the title and supplies the same breadcrumb hierarchy to search engines. Matching regional role pages show a prominent `Browse by city` module built from the approved permanent city-page register. Existing URLs, city-retention rules and the wider-regional-jobs button are unchanged.
- 5 September 2026 — **Approved job-page discovery recommendations are governed by published family, target-sector evidence and geography:** every vacancy shows the panel and can display up to six private-sector alternatives from the same approved family, plus any explicit cross-role relationship, within **15 straight-line miles**. Exact titles rank first, followed by explicit relationships and then other same-family work. The target's real location remains visible. An unknown landing employer no longer suppresses useful discovery because every displayed target must still be positively evidenced private; private jobs are never directed to public-sector work. Unresolved locations still fail closed to the regional slice fallback.
- 5 September 2026 — **The first discovery-panel coverage correction remains private-target fail-closed:** 20 exact direct-company identities and 159 explicit relationships support ranking, while governed same-family matching prevents title-row omissions from blanking the panel. The 1,807-job audit snapshot rises from 21 to 475 pages with targets. Agencies and generic `Company` records still remain `unknown`, but unknown landing employers may see positively evidenced private targets; four questionable identities remain inactive for review.

- 4 September 2026 — The 11:45 no-edit publication safety net can now be triggered by an authenticated external fallback using `AUTOMATIC_FALLBACK`. It behaves exactly like the scheduled safety net: it skips after a successful same-day publication and otherwise withholds untouched review items so they remain available later. Normal manual `PUBLISH` and quarantine behaviour are unchanged.

- 6 September 2026 — **The `CITY OPPORTUNITIES` tab now shows the role mix behind every locality total:** it adds one reconciled count for each of the eight governed families and an `Other / unclassified` safety column, making office-led and support-worker-led candidates directly distinguishable.

- 3 September 2026 — **The daily overview now has an all-role `CITY OPPORTUNITIES` tab:** every unique live job with a recognised town/locality is counted once across all roles and sources. Existing city pages are identified, non-London places with 4+ jobs are marked `CREATE`, lower counts are `MONITOR`, and London is held separately. The first snapshot shows **283 localities, including 23 CREATE candidates and 24 places with an existing live page**. It is a reporting structure only; it does not create pages automatically.

- 3 September 2026 — **The daily regional overview workbook now includes a `PAGES` tab:** it shows the total number of published/indexable URLs, separates individual job, regional/category, city and core pages, and lists every non-job URL with its current job count. London-wide Admin and its Central, North, East, South and West pages are listed separately rather than hidden behind one regional cell. The first snapshot totals **1,964 URLs (1,833 job + 98 regional/category + 25 city + 8 core)**.

- 3 September 2026 — **Thirteen additional regional/category slices are LIVE:** North Scotland, Tayside and South Wales Valleys Service Admin; Cambridgeshire, Cheshire West, Essex, Liverpool and North East Marketing; Warrington & Halton and London Finance / Accounts; Sussex HR / Recruitment; and Buckinghamshire and North East Customer Service / Contact Centre. They use the existing governed selectors and shared regional-page publisher. The LIVE register totals are now **51 / 16 / 10 / 7 / 6** markets for those five families respectively; no classifier or general launch-rule change is included.

- 3 September 2026 — **Belfast, Glasgow, Edinburgh and Cardiff city pages are LIVE:** the four permanent Service Admin city routes launch with **27, 21, 10 and 10** exact-city jobs respectively, drawn from Northern Ireland East, Glasgow, Edinburgh & Lothians and Cardiff & Vale. This is an owner-approved one-off waiver of missing 3-of-7 history after live-site/analytics review; the normal city launch rule remains unchanged.

- 3 September 2026 — **The JobG8 classification sheet now stays aligned after manual review:** applying owner decisions refreshes the same-feed JobG8 category counts from the final reviewed outputs before the daily overview is rebuilt. Newly selected or excluded jobs therefore appear in both the Sitewide JobG8 total and the supplier-classification breakdown for that publication.

- 2 September 2026 — **Repeated Customer Service recruitment campaigns count once:** JobG8 can send one employer campaign under many IDs and synonymous titles. Customer Service diagnostics and LIVE pages now collapse those variants and reject adverts whose opening location belongs to another region. This prevents the North East's 78 raw rows—mostly one EE campaign—from being mistaken for 78 separate opportunities.

- 2 September 2026 — **Twelve more regional slices are LIVE:** Wales South – Cardiff & Vale Service Admin; Berkshire, Hertfordshire, Kent, Glasgow, Surrey and Sussex Sales Advisor; and Bristol & Bath, Gloucestershire, Hertfordshire, Kent and Oxfordshire Marketing. Their most recent governed counts are respectively **9**; **8, 9, 9, 7, 6, 7**; and **8, 7, 9, 7, 9**. No other slice changes.

- 3 September 2026 — **Post-review category reconciliation completes end to end:** applying JobG8 review decisions refreshes the same-feed category profile, and completion of that workflow directly triggers the daily regional overview rebuild. The direct completion trigger is required because GitHub does not emit a follow-on `push` workflow from a commit made with its workflow token.
- 2 September 2026 — **All four daily regional overview sheets now use one JobG8 feed date:** the daily JobG8 run refreshes the JobG8 category sheet from its own feed and prepared published outputs, while the overview blocks any mixed-date workbook. Sitewide, JobG8 categories, LIVE and NOT LIVE therefore represent the same most recent successful JobG8 run.

- 2 September 2026 — **The homepage's four recent vacancies now show breadth:** cards come from genuine jobs in the newest 48-hour window only when they include a clear numeric salary, and the automatic choice prefers different roles, regions and titles instead of repeating one vacancy type from a source burst.

- 1 September 2026 — **The homepage makes Ontap's value clearer:** a stronger search-first hero shows the live vacancy count and the Apply direct, No signup and Updated daily promises. Four newly posted real jobs now appear before the unchanged role-and-region directory.

- 1 September 2026 — The JobG8 coverage-audit download now includes a separate CSV of published jobs absent from the latest feed, showing each job's identity, Ontap posted date, apply link and last date seen in the available JobG8 archive.

- 1 September 2026 — The downloadable daily regional overview workbook has separate Sitewide, JobG8 categories, LIVE and NOT LIVE tabs. NOT LIVE is exported only after its rolling evidence has been applied, so each compact single-line cell shows `today / 14d average / 6+ days`. JobG8 categories shows both jobs received and the number currently published by Ontap in each supplier classification, with a published total that reconciles automatically.

- 1 September 2026 — The main daily regional overview now shows how many jobs the latest JobG8 coverage audit actually received and the count in each of JobG8's own supplied classifications. This is kept distinct from Ontap categories and live-job totals.

- 1 September 2026 — **Three more regional slices are approved for LIVE:** Bedfordshire Service Admin, Bristol & Bath Sales Advisor and Buckinghamshire Marketing. Their current / rolling-average / six-plus-day evidence is **9 / 6.0 / 6-of-11, 9 / 6.6 / 9-of-11 and 13 / 4.1 / 2-of-9** respectively. They use the existing selectors and regional-page publisher; no other market changes.

- 1 September 2026 — **The twice-daily JobG8 refresh has a safe fallback:** cron-job.org can trigger the existing morning and evening JobG8 workflow at 08:35 and 17:35 UK time. The workflow records a completed UK cycle only after its normal process and commit succeed. If GitHub’s own delayed cron run then arrives, it recognises that completed cycle and ends without rerunning or making duplicate commits. If the first attempt fails, it is not marked complete, so the other trigger can still run it.

- 1 September 2026 — **NHS vacancies are eligible for Google Jobs again:** the strict 27 August posting-date check accidentally rejected NHS's fractional source timestamps and suppressed NHS `JobPosting` markup. Ontap now retains the factual NHS posting date as `YYYY-MM-DD`, keeps other malformed dates fail-closed and marks only NHS URLs for Indexing API resubmission.

- 30 August 2026 — **The fourth owner title sweep is encoded:** further agreed Admin, Payroll/Finance, Legal Support, Care/Support, People Operations and Sales Coordination titles now enter their existing governed families. Ambiguous roles, IT Support and Housing Officer remain parked; ordinary publication rules still decide what becomes live. The earlier `City` geography fix already corrects this workbook's definite false-London mappings without forcing ambiguous county conflicts.

- 30 August 2026 — **The owner-reviewed no-register sweep is encoded:** narrow exact decisions add the agreed routine Admin, Customer Service, Finance/Payroll, EA/PA, Legal Support and direct Support/Care titles without admitting the rejected optical, school-support, property/retail-sales, technical, managerial or specialist groups. Generic `City` geography now uses the job's actual location instead of defaulting to London, and the audit correctly bands SalaryAdditional-only pay. Normal LIVE-market, salary and duplicate rules still decide publication.
- 30 August 2026 — **Expired Google Jobs links are now cleaned up sooner:** whenever published job inventory changes, Ontap automatically runs its existing deletion-first Google Indexing update instead of waiting until the evening fallback run.

- 30 August 2026 — **Still-open NHS jobs are retained during JobG8 review publication:** JobG8 decisions and the refreshed NHS inventory are now composed into one commit, preventing short-lived missing job pages between the two source updates.

- 30 August 2026 — **Automatic JobG8 discovery audits now run only after relevant changes reach `main`:** a feature-branch push can no longer launch a production archive/writeback run that AWS must reject. Non-main testing remains available only through the existing safe, manual artifact-only option.
- 30 August 2026 — **The remaining owner-approved missed JobG8 titles are encoded:** named Service Admin, Finance, Customer Service, Sales, Legal and HR roles now enter their existing family selectors through exact decisions only. Personal Assistant is included for clearly executive/office PA work but not direct care, legal PA or ambiguous adverts; `Payroll , Pensions and HR Administrator (Hybrid)` remains held. Broader exclusions and all existing pay, location, duplicate and LIVE-market checks are unchanged.
- 29 August 2026 — **The agreed A–H missed-role review is encoded:** the reviewed practical Finance, Customer Service, HR, Admin, Support Worker/Housing Support, Sales, Marketing and Legal roles now enter their appropriate existing family selectors. Narrow exact-title exceptions correct the genuine false negatives without opening broad words such as `driver`, `housing`, `analyst`, `officer` or `manager` generally. The seven agreed exclusions remain out, and the six Housing Estates Officer adverts stay on hold for fuller evidence. Existing salary, location, duplicate and LIVE-market rules still decide whether an included family match is actually published.
- 29 August 2026 — **Four missed Service Admin titles are now included:** full-advert review confirmed `Admin`, `Administrative Officer`, `Admin Advertiser` and `Administration Support Assistant` as ordinary transferable office administration. They now enter the normal governed selector, while the existing pay, specialist, location, duplicate and LIVE-market checks still apply.
- 29 August 2026 — The manually run JobG8 discovery audit now supplies a downloadable Excel/CSV of every feed row, including source details, salary band, family evidence and why it is published, withheld, rejected or unmatched. It is an inspection report only and cannot change the live site.
- 29 August 2026 — **The salary-band family audit can be tested without altering production:** the normal discovery workflow now offers the named salary test branch in an artifact-only mode. That mode runs against the current JobG8 archive but cannot commit reports, merge code or push to `main`; normal main-branch audits continue unchanged.
- 28 August 2026 — **Warehouse & Logistics Operations discovery is running, with nothing activated:** the deliberately narrow seam covers warehouse/transport/logistics administration and coordination, stock or inventory control, goods-in/despatch administration and routine import/export or shipping operations. Manual warehouse work, driving, management, sales, procurement, technical systems and specialist supply-chain roles are excluded or held for review. The first local 10,000-job baseline found only **28 clear fits plus 24 borderlines**, an absolute pre-review ceiling of 52 against the ~100 national viability floor; the governed current-feed run will confirm whether it should be parked. No catalogue entry, route or LIVE market exists.
- 28 August 2026 — **The daily regional overview now accounts for everything currently live:** it shows unique JobG8 and non-JobG8 totals, every provider separately, jobs appearing on multiple slices, extra slice placements and any job left outside a governed slice. The totals reconcile unique jobs back to all regional/category placements, while a stale dated source-count CSV is clearly flagged rather than silently driving the headline. Customer Service / Contact Centre is added as the eighth LIVE/NOT LIVE family across all 78 UK markets; no existing LIVE-region decision changes. Future providers such as WhatJobs appear automatically in the provider breakdown. The six-job Customer Service measure remains evidence for launching a candidate slice; after explicit LIVE approval, any non-zero governed inventory publishes, preventing Hampshire, London or Staffordshire from being blanked merely because a daily count falls below six.
- 28 August 2026 — **One to three unavailable Teaching Vacancies regions no longer prevent clean regions publishing:** the England-wide TV publisher names each isolated region and retains its previous live page while verified regions proceed; four or more regional failures stop TV. North East's legitimate detailed NEJobs/VONNE region labels now resolve to the public North East slice, fixing the false missing-base failure. Tampered evidence, ambiguous/malformed outputs, external-only data and recomposition mismatches still stop the whole TV publish.
- 27 August 2026 — **Finance & Accounts is LIVE in eight explicitly approved markets:** North Yorkshire 13, Gloucestershire 10, North East 7, Bristol & Bath 10, Northern Ireland East 10, Shropshire 10, West Yorkshire 10 and Devon 9—**79 published jobs** in total. The selector keeps practical accounts/finance support, AP/AR, ledgers, credit control, bookkeeping, billing/invoicing and payroll operations under £45,000, while excluding senior, qualified, specialist and financial-services work. Every LIVE market must retain at least six jobs. London is CANDIDATE rather than LIVE because the current governed feed yields only four. Finance now appears as the seventh family in the 78-market daily overview. The unrelated changed NEJobs live set was held for re-review and not forced through.
- 27 August 2026 — **Four additional slices are approved for LIVE:** Berkshire Marketing, Kent Support Worker, North East Sales Advisor and Oxfordshire Support Worker. Their current / rolling-average / six-plus-day evidence is **10 / 7.0 / 2-of-4, 11 / 6.2 / 2-of-6, 4 / 5.3 / 3-of-6 and 7 / 4.8 / 3-of-6** respectively. They reuse the existing family selectors and regional-page publishing machinery; no other market is activated.
- 27 August 2026 — **A normal small change in the live NHS vacancy count no longer blocks that day's NHS update:** the fetch restarts from the beginning and tries up to three times. If NHS is still moving by 15 jobs or fewer, the final cleanly deduplicated sweep continues with a warning; a movement above 15 still holds NHS on its previous approved state. The existing transactional publication checks and 20% NHS page ceiling are unchanged.
- 27 August 2026 — **JobG8 Google Jobs coverage approved for production:** all 1,056 current JobG8 detail URLs build as indexable pages with a normal link to apply. The 777 jobs whose feed description is complete now pass the local `JobPosting` gate, up from zero with all audited required fields because every one now uses its stable Ontap first-publication date. The other 279 contain JobG8's click-apply teaser and remain deliberately without job schema; the checked workbook has no fuller description field and Ontap does not invent one. Recruiter names are not presented as the hiring employer, generic locations are not asserted as towns, and the one genuinely fully remote eligible vacancy uses Google's remote-job fields.
- 27 August 2026 — **`datePosted` is set once, not refreshed:** current JobG8 uses `ontap_first_published` because no dependable source posting date is supplied. A future source date, or a semantically valid future JobG8 `StartDate`, takes precedence when first available. The verified publisher retains the earliest stable date across daily republishes, slice moves and reappearances.
- 26 August 2026 — **One conflicting duplicate JobG8 ID no longer stops every clean output:** if the same JobG8 display reference arrives with different factual metadata, that ambiguous job is left out and named while the clean jobs continue. Up to 15 conflicting IDs are isolated this way; 16 or more still stop JobG8 as a likely feed-wide problem. This uses the existing publication-isolation rule and does not affect external-source jobs.
- 26 August 2026 — **Five further Service Admin markets are approved for LIVE:** Cheshire - West, Northern Ireland - East, Scotland Central - Edinburgh & Lothians, Scotland West - Glasgow and Worcestershire. Their current / rolling-average / six-plus-day evidence is **8 / 8.0 / 5-of-5, 8 / 8.5 / 4-of-4, 6 / 12.8 / 4-of-4, 10 / 14.5 / 4-of-4 and 10 / 8.8 / 5-of-5** respectively. This is a named owner approval for all five and does not change the general Service Admin rule that automatic approval requires more than 8 current jobs. The Service Admin LIVE footprint is now **43 / 55 England markets and 46 / 78 UK markets**; the established regional-page, homepage, Browse Jobs, search and verified-publish mechanisms are reused.
- 26 August 2026 — **One bad Teaching Vacancies advert no longer stops the other clean TV jobs:** after normal retries, up to 15 unavailable or malformed individual adverts are left out and named in the run evidence. Sixteen or more still stop TV, as does a broken/incomplete listing or a run producing no usable jobs.
- 26 August 2026 — **NEJobs no longer mistakes two genuine vacancies for one merely because their title, employer and location match:** separate source IDs remain separate jobs. True duplicates already supplied by another source are still withheld, and the final check stops only for an approved job that is genuinely unaccounted for. The same correction protects VONNE because both use the shared North East composer.
- 26 August 2026 — **VONNE connection interruptions now retry safely:** temporary resets or timeouts between GitHub and VONNE receive up to four bounded attempts instead of immediately ending the workflow. Invalid pages and exhausted retries still fail safely.
- 26 August 2026 — **VONNE no longer loses its whole approved batch because of a small edit queue:** up to 10 undecided or changed vacancies are withheld individually while unchanged, previously selected VONNE jobs continue. Eleven or more stop VONNE for review, and genuine source/detail/factual integrity failures still block it.
- 26 August 2026 — **Teaching Vacancies no longer retains obsolete regional review files:** when a vacancy moves into its corrected region, the old generated regional pair is removed before the master review is rebuilt. The existing identical Diss/Norfolk duplicate can pass through the recovery run safely, while conflicting duplicates still stop.
- 26 August 2026 — **Teaching Vacancies now handles a search returning exactly one job:** TV writes `result` rather than `results` in that case. The page audit accepts both forms while keeping all existing page-count and vacancy-link completeness checks.
- 24 August 2026 — **HR / Recruitment is LIVE in six explicitly approved markets:** London, West Yorkshire, Berkshire, Manchester & Salford, Nottinghamshire, and Birmingham & Solihull. The three exact-five proof markets—Sussex, Bristol & Bath and Essex—remain reserves and are not public. Daily selection now uses the reviewed advert-level HR / Recruitment boundary instead of the older exact-title HR mechanism, rechecking the £50k ceiling, senior/advisory/specialist and agency-sales exclusions, content duplicates and geographic conflicts before the shared verified-page publisher runs. The proof-reviewed Ashton-under-Lyne/Tameside advert remains in Manchester through a narrow explicit exception; unrelated location conflicts are still withheld.
- 24 August 2026 — **HR / Recruitment proof-…6350 tokens truncated…ly when they genuinely belong to the same labour market and the decision is recorded in the city-page register.
- 19 August 2026 — Put **Durham Service Admin on HOLD** because the original `durham` opportunity-market pattern could also match broad `County Durham` locations. The 22 August city audit added an explicit County Durham exclusion, but Durham remains HOLD until clean post-fix history requalifies it.
- 19 August 2026 — Activated six additional Service Admin regions from same-feed evidence against the then-configured 33-market footprint: Buckinghamshire, Greater Manchester - South, Hertfordshire, Somerset, West Midlands - Birmingham & Solihull, and Yorkshire - East.
- 19 August 2026 — Added the first same-feed daily coverage for Service Admin and Support Worker across the then-configured 33-market footprint; this was expanded to all 55 assessable England markets on 22 August.
- 19 August 2026 — Added fail-soft publication hierarchy: small job-level problems are withheld while clean jobs continue; larger source problems isolate that source rather than blocking the whole Ontap publish.
- 19 August 2026 — Merged architecture cleanup 1–5 into `main` via PR #211.

## 1. Pipeline

The main JobG8 process remains the primary production ingest/process path. NEJobs, VONNE, Teaching Vacancies and NHS Jobs provide additional inventory through governed source paths. After review, the single **Apply and publish Ontap daily review** workflow coordinates source publishers and the final verified-page publish.

A source shown as `STALE` or `MISSING` in the unified review must not be interpreted as zero inventory. Repair/rerun that source, then rerun `Ontap daily review` to regenerate the master edit file before reviewing. The 22 August Teaching Vacancies recovery verified this operating sequence and the fail-soft source-isolation behaviour.

At the 18 September audit, Service Admin is LIVE in **51 / 78 UK markets**. All use the same central catalog, slice register, production selector and verified-page publishing mechanism. `pipeline/registers/region_category_slice_register.csv` is authoritative if that count later changes.

Regional geography has two deliberately separate layers. `pipeline/config/uk_assessable_regions.json` defines the **78 assessable UK markets** used for daily diagnostics and coverage reporting; `england_assessable_regions.json` remains a subset/reference. `pipeline/config/job_slice_catalog.json` is the configured/public market layer and is not the national geography authority; `region_category_slice_register.csv` decides what is LIVE. A mapped job can therefore be assessed even when its market has no LIVE slice. `North East` remains the deliberate roll-up of all three underlying North East lookup areas, including Tees Valley.

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

**discovery audit → define the family boundary → review real jobs in proof regions → create central title/refinement rules → validate against the full feed → assess all 78 canonical UK markets diagnostically → explicitly approve suitable LIVE slices → integrate the family into the existing daily/review/publish mechanisms.**

Broad discovery regex/title buckets are evidence only; they are not publication rules. Positive counts do not generally activate a slice automatically. **Service Admin is the standing exception from 22 August 2026: a governed same-feed count over 8 is immediate owner approval for LIVE; 8 or below stays NOT LIVE and remains on rolling evidence.** Other families still require separate explicit approval unless the owner changes their rule.

Family membership is not forced to be exclusive. A job can legitimately qualify for more than one family when it serves both user intents. Each family applies its own rules, and overlap is only deduped where the same job would otherwise repeat within one user-facing result set.

Customer Sales / Sales Advisor has completed the governed lifecycle through explicit LIVE approval. Its original launch set was London, Greater Manchester - Manchester & Salford and Yorkshire - West; the register has since expanded to **14 LIVE markets as at 18 September**. The production selector is generated from the same current JobG8 input as the main daily process and publishes through the shared configured-slice/verified-page mechanism. LIVE state is governed by the explicit slice register, not by a one-day job count. Genuine Sales/Service Admin crossover remains valid. Direct office/contact-centre/home/hybrid sales roles qualify; customer/service titles require explicit sales/conversion evidence; generic account roles require strong sales plus office/digital evidence. Field/in-home/event/self-employed sales, automotive dealership/showroom sales, retail/property sales and senior/specialist boundary roles are excluded. Every non-LIVE region remains diagnostic only until explicitly approved; its governed count is refreshed in the 78-market daily family coverage.

The general publish rule remains fail-soft:

**up to 15 bad/unresolved mandatory-review jobs in one source are withheld and flagged while clean jobs continue; more than 15, or a source-integrity problem, isolates that source and keeps its last approved state; only a genuine whole-publication integrity failure should stop everything.**

NHS untouched POSS rows are an explicit exception to the mandatory-review count: they are optional review opportunities, remain excluded if untouched, and do not by themselves isolate NHS.

The old May monolithic pipeline and older standalone service-admin/support-worker workflows have been removed because the current full/reviewed pipeline covers those operational paths.

### City-page pipeline

City pages are derived views of final approved regional pages; they are not separate feeds or classification pipelines.

For Service Admin, a non-London exact town with **at least four current governed Service Admin jobs** may be activated after explicit human approval. Supplementary office-family jobs can enrich a page but cannot qualify the town. READY FOR APPROVAL does not auto-publish.

Once explicitly active, a city route is permanent even if inventory later drops below four. The daily publication path continues to rebuild its private city JSON from the approved parent regional page, including an empty list when necessary.

Homepage prominence is a separate rule: an active city page is shown as a homepage city card only at **4+ current jobs**. At 0–3 jobs the route remains live/indexable and continues to refresh, but its homepage card is hidden until supply returns to 4+.

The Service Admin city thresholds are therefore:

- **4 current Service Admin jobs** = launch qualification threshold with explicit approval;
- **4 jobs** = homepage city-card visibility floor;
- **0 jobs** = permitted retained state for an already-active permanent route.

The geographic unit is an **approved local employment/commuting catchment anchored on the named city**. Launch should start conservatively. Catchments can later include nearby towns/suburbs only where they clearly belong to the same labour market and are recorded as explicit include/review/exclude rules. Low inventory is not a reason to widen a catchment artificially.

Examples: Leeds includes Pudsey; Newcastle includes Gateshead, North Tyneside, Shiremoor and Wideopen; Brighton & Hove includes Portslade.

Newly approved on 19 August 2026: **Bradford, Huddersfield, York, Barnsley and Doncaster Service Admin**. Their launch catchments are exact-city only.

One-off owner approval on 22 August 2026: **Bristol, Manchester, Cambridge, Birmingham, Peterborough, Warrington, Liverpool, Hull and Oxford Service Admin**. Each launched from a conservative exact-city catchment using current published regional inventory, with the one-off waiver of the missing 3-of-7 history explicitly recorded in `city-page-register.json`. This exception does not replace the standing launch gate.

**Durham is not approved.** The opportunity rule now excludes broad County Durham locations, but Durham must accumulate clean post-fix history before it can qualify.

## 2. Reports / diagnostics

The daily regional overview is backed by same-feed **Service Admin, Support Worker, Customer Sales / Sales Advisor, Paralegal, Marketing, Finance / Accounts, HR / Recruitment and Customer Service / Contact Centre** assessments across all 78 canonical UK markets. For NOT LIVE cells, a numeric zero means the current feed was assessed and no jobs survived that family's governed selector; `—` means that family was not present in the persisted transitional snapshot.

`pipeline/reports-daily/daily-family-coverage.csv` contains 624 rows (78 markets × eight families). `pipeline/reports-daily/daily-family-coverage-history.json` is the rolling evidence store: one snapshot per feed date, same-date reruns replace the existing date, all current counts are retained within each snapshot, and only the latest 14 feed dates are kept. Older snapshots contribute only to families present in them; later families are not backfilled artificially. In `daily-region-overview.md`, rolling metrics are shown only for NOT LIVE slices as **today / 14d average / days at 6+**. The 6+ count is deliberately a watch signal rather than an activation rule.

The overview's sitewide section reads the current published job JSON directly using the same canonical identity rules as the live-source counter. It distinguishes unique jobs from slice placements, reports jobs appearing on multiple slices and extra placements, and verifies that every unique live job belongs to a governed regional/category slice. Provider rows are dynamic, so a new source such as WhatJobs is included automatically. The latest dated live-source CSV remains visible as a cross-check and is marked stale if it no longer matches the current published site.

Its `CITY OPPORTUNITIES` section uses that same unique live inventory across all roles and providers. Exact recognised town/locality evidence is grouped through the canonical geo lookup, existing permanent city routes are identified from the city-page register, non-London places at 4+ current **Service Admin** jobs are marked `CREATE`, and lower counts remain `MONITOR`. Each locality also has reconciled columns for all eight governed role families plus `Other / unclassified`, so the owner can distinguish office-led candidates from support-worker-led candidates. London rows are retained as `HOLD – LONDON`; broader or unrecognised locations are counted in the reconciliation summary rather than forced into a city. The table is decision support and never publishes a page by itself.

LIVE family counts come directly from current published configured-slice JSON rather than diagnostic output. For every NOT LIVE region, the overview shows the same-feed governed diagnostic count generated with the relevant classifier, canonical geography, dedupe and final QA. These counts are expansion evidence only: a positive count never activates a region without separate explicit approval, except for the separately documented Service Admin >8 rule.

Live source reporting records NHS Jobs and Teaching Vacancies as providers after verified publication, alongside JobG8 and the other external sources. The verified 22 August post-recovery snapshot was **1,592 total live jobs**, of which **116 were Teaching Vacancies and 270 NHS Jobs**.

The city-opportunity report scans published regional/category slices against registered local markets and records seven-run qualification history. It is an expansion-control surface, not an automatic publisher.

Dated one-off recovery/failure reports are not part of the permanent working tree. The reporting rule is:

**recurring operations / specialist analysis / one-off diagnostics in Actions artifacts or Git history.**

Compiler Modules 1/2/3 remain legitimate analysis tools.

## 3. Website / UX

Saved-location discovery is a progressive enhancement across mobile and desktop. It does not change canonical URLs, server-rendered inventory, sitemap membership or indexing. The browser asks for geolocation only after a user presses the control. Coordinates are used in a JSON POST only long enough to resolve the nearest approved canonical town and are not saved or included in analytics; `localStorage` retains the resulting town, region and last displayed nearby-job count. Returning visitors see those saved details immediately while Ontap refreshes the count silently, and Change, Clear and manual-town controls keep it user-controlled. The separate `Suitable jobs nearby` panel on a vacancy remains anchored on that vacancy's governed role, sector, locality and 15-mile rules; a saved visitor location never replaces it.

The saved-location panel's count and `View nearby jobs` button use the same 15-mile search. An exact location search with no matching vacancies continues to display zero. Its onward action widens first to genuine current jobs within 15 straight-line miles of the approved canonical town, then to the corresponding Ontap region; it does not silently substitute unrelated national vacancies into the original results.


Non-London job-listing pages show three relevant course cards followed by Ontap's practical AI-help robot card in the desktop left rail. The full promotional rail is hidden on mobile, keeping the vacancies central. London retains its separately configured layout. First-time mobile visitors start with Quick View; desktop visitors start with Detailed View, while a saved choice is remembered. The robot links to `/ai-tips` with a checked source value, so readers can return to the same listing. Direct visits show `Browse current jobs`; the page's canonical URL and breadcrumb remain fixed. GA4 records the AI-tip and return-link clicks.

LIVE dynamic regional slices feed Browse Jobs, `/jobs/search`, job-detail backlinks and the homepage Admin region grid through the shared configured-slice/published-job mechanisms.

Customer Sales uses the same dynamic configured-slice mechanism. Production launch was verified on 21 August 2026 at `/job-search/london/customer-sales-jobs`, `/job-search/west-yorkshire/customer-sales-jobs`, and `/job-search/manchester-salford/customer-sales-jobs`: all three returned HTTP 200, rendered their current job cards and `/jobs/...` detail links, and exposed the expected JobG8-backed Apply actions. The same published-job inventory feeds Browse Jobs, homepage discovery, sitemap and search indexing.

NHS jobs use those same Service Admin pages and job-detail routes. A job is identified reliably by `source: "NHS Jobs"`; the employer itself may be an NHS trust, GP surgery, healthcare provider or other organisation whose visible name does not contain “NHS”. The job-detail page links to the original NHS Jobs advert for application.

Individual job pages use the governed published category as their family for the **Suitable jobs nearby** panel. A target must be in that same family or have an explicit registered relationship, must be positively evidenced private-sector, and must resolve within 15 straight-line miles. Results retain their true location and distance. Exact titles rank first, explicit relationships next and other same-family jobs after them; active locality exclusions still block a pair. When no approved match qualifies, the sidebar disappears, the main vacancy panel expands to full width, and a top-right card links to all current jobs in that region rather than claiming more jobs in the unavailable family.

`pipeline/scripts/audit_discovery_recommendation_coverage.py` applies those gates to the complete current published inventory and records whether each page receives ranked jobs or the slice fallback. Its CSV and Markdown reports are diagnostic only; they cannot classify an employer, activate a relationship or change a page.

NHS detail copy is now presentation-formatted rather than shown as a single flattened block. Existing structured headings/bullets are respected; otherwise long flattened NHS text is split into readable short paragraphs without changing the wording. The first six blocks remain visible and any remainder is available under **Show full NHS role information**.

Regional Service Admin pages deliberately mix NHS into the wider result set. NHS does not take the first slots simply because its internal quality ranking is strong: the normal inventory stays location-first and NHS is interleaved at the 4 non-NHS : 1 NHS rhythm while retaining the accepted NHS priority order.

The London-wide Service Admin page is the first sector-view trial. It keeps one canonical all-jobs URL and includes the complete Quick and Detailed result sets in server-rendered HTML. The client-visible controls switch among `All jobs`, `Business & agency`, and `Public service & charity`; they do not request or create separate sector result pages. Source-aware badges and `/sector-switching` explain the grouping. Authoritative NHS Jobs and Teaching Vacancies records are grouped directly, while JobG8 moves only on explicit public/charity evidence and otherwise remains under Business & agency. London area pages do not yet enable the trial.

Search uses a deployment-time snapshot of current published inventory. `scripts/generate-search-index.ts` creates `generated/published-jobs-search.json` during `npm run build`; `/jobs/search` imports that index directly rather than walking/parsing the full published route-data tree for each request. Each job also carries precomputed `_search` metadata containing the normalised/tokenised title, location, region, category, company, combined fields, slice label and searchable description representation. The search bundle therefore does not carry the raw advert description/full-description text and does not redo that field preparation on each request. This removes both the original request-time inventory reconstruction and the later per-request normalisation/tokenisation bottleneck while keeping the searchable meaning tied to the deployed published supply.

Search is deliberately forgiving but guarded. One-box queries can span title, employer/advertiser, location, region and curated category, so combinations such as employer/place + role can work naturally. When the dedicated location field is empty, a token is inferred as geography only if it lacks a credible title/category role anchor; polluted source location text therefore cannot steal a real role term such as `administrator`.

Both search inputs are explicitly labelled **Role or keyword** and **Location**. If a user reverses them, Ontap compares the amount of role evidence against geography evidence and can reinterpret the fields rather than returning an avoidable zero. `office` and `clerical` are accepted internally as admin intent for matching without replacing the user's displayed wording.

High-confidence spelling correction is applied from the current published-job vocabulary, with ambiguous/tied corrections left unchanged. Both search inputs also enable browser spellcheck/autocorrect. Correction vocabularies and recent correction results are cached. Runtime matching reuses the build-time `_search` metadata and a cached corpus-level geographic vocabulary rather than repeatedly rebuilding those structures.

Production verification on 21 August includes `lumley office` → Great Lumley Surgery, `lumley offcie` → corrected `lumley office` → the same vacancy, and `admin` + `newcastle` returning 21 current matches whether the role/location values are entered in the normal or reversed boxes. After the final build-time metadata optimisation, live browser testing confirmed that the earlier roughly 4–5 second perceived search wait was removed and search felt very fast, without changing the verified result behaviour.

On the homepage, the four recently added cards are selected from genuine vacancies in the newest 48-hour window with clear numeric salary information, while preferring different role families, regions and titles. Regional slices are deliberately listed before city pages. This gives the primary browse area a stronger sense of breadth and current inventory; city pages remain a secondary local-discovery layer beneath the regional coverage.

City pages use the common city-page framework and private `app/_city-pages/...` derived JSON, avoiding duplicate job-detail URLs. The homepage city grid independently suppresses active city cards below 4 current jobs without changing the route, sitemap/indexing status or daily refresh behaviour.

At the 18 September audit, `city-page-register.json` contains **54 active permanent routes: 53 Admin and office routes and one Support Worker route**. That register, rather than a copied route list here, is the authority for the active set.

Existing established public routes remain stable unless there is a concrete business reason to change them.

## 4. Content / positioning

Ontap remains positioned around useful job discovery for ordinary workers in an AI workplace, with sector-switching as an additional route rather than the whole identity.

NHS/public-sector inventory is an advantage for switchers and existing sector workers, but it must remain subordinate to the overall Ontap proposition. Generic regional discovery should not be swamped by NHS: the hard 20% source ceiling and the 4+1 display rhythm both enforce that principle. The London sector-view trial surfaces explicit NHS/public/charity interest without changing the underlying generic-page source ceiling, canonical URL or server-rendered inventory.

## 5. Operations / infrastructure

Core controls are:

- scheduled source refresh/reviews, including NEJobs, VONNE, Teaching Vacancies regional/master review and the NHS Administrative & Clerical review refresh at 10:05 UTC;
- the twice-daily full JobG8 process, which refreshes and composes NHS transactionally, generates every approved registered family slice, persists the current **78-market × eight-family (624-row)** diagnostic snapshot, and records/replaces that feed date in the rolling 14-date family coverage history;
- one master daily owner review;
- one owner-facing apply/publish orchestrator, with manual `PUBLISH` control and an 11:45 Europe/London no-edit safety net;
- one owner-facing **Ontap daily status** workflow on the Actions page, combining morning source/review readiness with the final manual-or-automatic publication and deployment receipt;
- source-specific publishers, including NHS, with the reviewed NHS publisher using the same transactional composer as the normal daily run;
- final verified-page publishing including city-page derivation/maintenance and configured Customer Sales slices;
- normal Vercel Git deployment from `main`, with explicit live-SHA verification;
- manual-only Vercel CLI recovery using `VERCEL_TOKEN` if Git deployment fails;
- Google indexing and operational monitoring.

The JobG8 discovery coverage audit now uses the exact current Europe/London feed date rather than a fixed monthly archive. If that day’s raw feed is unavailable, or the selected feed date differs from the audit date, it stops without publishing a report. This keeps the published JobG8 total, JobG8-supplied category breakdown and genuine published-but-absent exceptions on one same-day basis.

After every successful coverage-audit run, the daily regional overview workflow is triggered directly and rebuilds both the Markdown report and Excel download. This direct workflow-completion link avoids GitHub's restriction that prevents a workflow-token commit from triggering another workflow through a normal `push` event.

The 11:45 safety net checks for a successful Apply and publish dispatch on the current London date. If found, it exits without a second publication. Otherwise it uses the same publisher chain in automatic-withhold mode: unresolved review jobs are omitted without becoming remembered exclusions, regardless of queue size, while valid existing decisions and automatically eligible jobs continue. An authenticated external fallback can invoke this same path with `AUTOMATIC_FALLBACK`; it cannot enter manual quarantine mode. Freshness, fingerprint, source-publisher and combined-publication integrity controls are unchanged.

`Ontap daily status` is the normal owner check. It runs when the daily master review finishes and when the production deployment guard finishes, plus 09:15 and 12:15 UK-time fallback snapshots. Before publication, a green result means every named source has same-day review state and the master edit file is current. After publication, green means every source publisher, verified-page build, same-day live-source report and Vercel deployment completed; the summary explicitly says **MANUAL** or **AUTOMATIC**. If a source was retained fail-soft, the site may still have updated, but the status check fails visibly and names that source rather than presenting the day as wholly green.

Teaching Vacancies regional/master review uses one complete audited discovery pass with targeted retries for a failed listing page or internally inconsistent route; it does not require an identical second national sweep. After detail-request retries, up to 15 failed or malformed individual vacancy pages are quarantined and reported while clean jobs continue; 16+ detail failures or a source-level listing/integrity failure stops TV. Its writeback is protected against concurrent `main` movement by full-history checkout plus up to three pull-rebase/push attempts. The 22 August recovery proved the generated source evidence, rebuilt master review, reviewed publication and final deployment chain end-to-end.

Every `npm run build` now regenerates the published-job search index before `prisma generate` and `next build`. That generated index contains both the current result-card fields and the precomputed `_search` metadata needed for matching, while omitting the raw description/full-description payload from the runtime search bundle. Search therefore uses the exact published inventory captured by that deployment without rebuilding inventory or normalised/tokenised field structures on individual search requests.

A successful `Publish verified pages` run automatically triggers `.github/workflows/deploy-vercel-after-publish.yml`. That workflow checks out current `main`, captures the expected SHA, and waits up to three minutes for normal Vercel Git integration to deploy that commit or a newer descendant. It verifies production through `https://www.ontapjobsearch.com/api/deployment-version`.

If normal Git deployment succeeds, the workflow finishes green and all CLI recovery steps are skipped. This behaviour was confirmed in production on 20 August 2026 and again after the recovered 22 August reviewed publication. If production does not catch up within the wait window, the automatic workflow fails and raises/updates the GitHub Issue **Ontap production deployment is stale**; it does **not** automatically perform a second deployment.

Manual dispatch of `Deploy Ontap production after publish` is the recovery route. Only a manually dispatched run may use the `VERCEL_TOKEN` repository secret to call the Vercel CLI and deploy current `main` directly, followed by the same live-SHA verification. The old Vercel Deploy Hook has been revoked and `VERCEL_DEPLOY_HOOK_URL` removed; Deploy Hooks are no longer part of production publication.

Vercel is now on **Pro**. The upgrade was made on 21 August after the Hobby build-rate ceiling refused to start a valid deployment; once upgraded, the pending `main` search fix deployed successfully through the same Git integration. This changes capacity, not architecture.

This makes normal Git→Vercel deployment the single automatic production route, while retaining an explicit manual fallback without creating routine duplicate deployments.

The Google Indexing API retains its 200-notification safety limit and GitHub Issue alerting. The selection policy is JobG8-first: after the 20-notification deletion allowance, eligible JobG8 URLs use available capacity before non-JobG8 URLs. Non-paying sources have a hard ceiling of 20 submissions per Pacific day (10% of quota), and unused JobG8 capacity is not released to them. Each run reports live inventory, candidate and selected counts by source so feed-to-publication-to-indexing gaps are visible.

## Business rule

**Business priority wins over technical tidiness.** Cleanup is justified where it improves reliability, delivery speed, cost, UX, indexing/discoverability, AI discoverability or safe inventory growth — not simply because a cleaner-looking architecture is possible.

## Current state

As reconciled from `pipeline/registers/region_category_slice_register.csv` on 18 September 2026, the register contains **126 LIVE rows**: Service Admin 51, Marketing 19, Customer Sales 14, Finance / Accounts 12, Support Worker 11, HR / Recruitment 9, Customer Service / Contact Centre 6 and Legal Assistant / Paralegal 4. Another 15 rows are CANDIDATE. The live register remains authoritative after this dated snapshot.

The full JobG8 workflow assesses all eight families across all 78 UK markets (624 rows) and retains up to 14 feed-date snapshots. The shared city mechanism owns 54 active permanent routes (53 Admin and office, one Support Worker). Production deployment uses normal Vercel Git integration automatically, with CLI recovery manual-only. NHS Administrative & Clerical inventory is isolated safely on feed failure, remains capped at 20% per Service Admin page and uses the 4+1 display order. Live vacancy pages and search use deployment-built static/current inventory; expired-job recovery remains separate. Teaching Vacancies retains the source-isolation and concurrent-write safeguards described above.
- 21 September 2026 — **Google indexing now gives JobG8 first claim on the daily allowance:** after the fixed deletion allowance, every available eligible JobG8 URL is selected before any non-JobG8 URL. Non-paying sources are capped at **20 of 200 submissions (10%)**; unused JobG8 capacity is never released to them. Workflow summaries now show live inventory, indexing candidates and selected submissions by source.

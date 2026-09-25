Warning: truncated output (original token count: 30474)
Total output lines: 522

# Ontap System Map

**Last updated:** 24 September 2026
**Status:** Canonical production architecture, reconciled on 24 September against the active workflows, slice register, city-page register and current diagnostic contract.

- 21 September 2026 — **Nearby-location analytics now explains incomplete location attempts and reliably measures restored preferences:** client events that occur before GA4 initialises wait for the shared analytics-ready signal instead of being dropped. Unsuccessful geolocation attempts now distinguish unsupported browsers, permission denial, unavailable positions, timeouts and nearby-API failures; manual-town attempts and saved-location refresh failures are measured separately. Existing `saved_location_return` and `saved_location_results_loaded` events remain the proof of remembered-location reuse.

This is the authoritative technical map of the persistent Ontap system. It is organised into five canonical buckets. Facts not verified from the repository are marked `UNKNOWN / NEEDS AUDIT` rather than inferred from chat history.

## Recent canonical changes

- 24 September 2026 — **Four approved regional slices were activated:** Greater Manchester - North Finance / Accounts, Scotland Central - Fife Service Admin, Bristol & Bath Legal Assistant / Paralegal, and Staffordshire Marketing. The configured catalog supplies route metadata, the explicit LIVE register controls activation, and existing family generation plus verified publication workflows handle the pages.

- 24 September 2026 — **Quick View is the initial view on mobile listing pages:** on first visit without a saved choice, screens up to 700 px start in Quick View and wider screens start in Detailed View. A stored explicit choice still takes priority on later visits.

- 24 September 2026 — **AI tips now return visitors to their originating job listing:** listing cards pass a validated source key, and `/ai-tips` resolves it only through the known regional/category route registry. Admin listing links retain their existing region key; other categories use a region-and-category key. Direct or invalid visits keep the `Browse current jobs` fallback. The fixed canonical URL and breadcrumb schema are unchanged, and the return-link click retains GA4 measurement.

- 23 September 2026, corrected 25 September — **JobG8 practical-role selection is three-way and failure-isolated:** clearly junior/assistant/practical finance, bookkeeping, payroll and legal-office titles are eligible candidates despite broad words such as `legal` or `accountant`. ACCA/ACA/CIMA qualification checks apply only to Assistant Accountant and Assistant Management Accountant titles; a clear mandatory requirement excludes, AAT is allowed, and missing/preferred/unclear wording goes to review. These qualification checks do not apply to ordinary Bookkeeper, payroll, credit-control or legal-office titles. Salary ceilings remain hard, while non-numeric salary wording is reviewed rather than excluded. A malformed or undecidable individual row is withheld and logged as `DAILY_REVIEW` while the remaining JobG8 rows continue. The daily review view labels salary as coming from JobG8 fields, extracted from the description, or no supported amount being found in either source.

- 18 September 2026 — **Governance currency audit:** corrected stale current-state references to the former 55-market/three- or five-family diagnostic phases. The production contract is now explicitly 78 UK markets × eight governed families (624 rows); the 18 September documentation reported 126 LIVE rows; a 24 September register recount found 159 before four further activations and the city register contains 54 active permanent routes. Dated rollout figures remain historical evidence only.

- 17 September 2026 — **Traffic reporting now separates explicit automation, human-qualified visits and anonymous returning browsers:** the shared client analytics bootstrap suppresses GA4 only for explicitly identified crawler/automation user agents. It does not use `navigator.webdriver` as a standalone suppression signal, and ordinary browsers continue to load GA4 and emit events; public-page access and indexing are unaffected. Real browsers emit `qualified_visit` after the first trusted interaction in a browser session. Anonymous local first/last-seen timestamps emit `returning_browser` only after a gap of at least 30 minutes, with no identity, town or coordinates; the existing `saved_location_return` and `saved_location_results_loaded` events remain the narrower proof of restored location use. `scripts/build-campaign-url.ts` is the single tested helper for links published on channels Ontap controls; internal navigation deliberately remains untagged so it cannot overwrite acquisition attribution.

- 17 September 2026 — **A valid zero-job LIVE family slice no longer stops the JobG8 day:** recurring Marketing and HR / Recruitment verification still requires every registered LIVE output file to exist and contain a JSON array, but an empty array is accepted as the publisher's already-governed `validated zero` state. The verified publisher clears any stale destination jobs for that slice while the rest of the fresh inventory continues. Missing files, malformed JSON and non-array content remain blocking integrity failures.

- 17 September 2026 — **An unavailable NHS feed no longer blocks fresh JobG8 publication:** the NHS inventory client now identifies maintenance redirects, empty responses and malformed/non-vacancy XML as an upstream source outage. The normal JobG8 rebuild snapshots the last approved combined Service Admin outputs before replacing its base; if NHS discovery or accepted-advert enrichment is unavailable, the composer safely recomposes that approved NHS subset against the fresh non-NHS rows, reapplies duplicate and 20% source-cap protection, emits an explicit workflow warning and lets the remaining JobG8 process continue. NHS review evidence is left unchanged until a successful refresh. Integrity failures outside the recognised NHS transport/content failure remain fail-closed.

- 16 September 2026 — **Current vacancy pages are statically generated again for faster users and crawlers:** expired-job personalisation no longer reads request headers inside the shared `/jobs/[id]` route, and public job requests no longer pass through admin authentication middleware. All current job IDs remain generated at deployment and keep the same canonical URL, metadata and `JobPosting` output. Expired URLs still return the useful 404 shell immediately, then progressively load their former-job context and governed recommendations from `/api/jobs/expired-recovery/[id]`; failure of that optional lookup leaves the generic current-jobs recovery intact.

- 13 September 2026 — **Returning visitors no longer see a location-loading blank state:** the shared saved-location component restores the saved town and last known nearby count immediately on both mobile and desktop, then refreshes the count silently. Existing preferences without a stored count still show the saved town immediately with neutral supporting text until the first background refresh completes.

- 13 September 2026 — **Empty job-detail recommendation panels no longer advertise missing matches:** when no approved nearby vacancy qualifies, Ontap suppresses the sidebar and negative message, expands the main vacancy panel to full width, and places a compact pale-blue all-jobs regional link at its top-right. Populated panels and all governed matching rules are unchanged.

- 13 September 2026 — **The obsolete Quick View duty-bubble system was removed:** Quick View retains its compact location-first job rows and sector badges, but no longer reads or renders generated duty tags. The separate daily `Refresh Quick View duties` workflow, its fallback preview data, dedicated generation scripts and tests were removed, eliminating redundant post-JobG8 commits without changing the live listing presentation or the job-detail facts panel.

- 11 September 2026 — **Mobile job-page onward links use concise place wording:** below 640 px the primary link now displays `More [city or region] jobs` on one line, while desktop retains the full role-and-region wording. The link destination and full accessible label are unchanged, and the secondary regional link remains desktop-only.

- 10 September 2026 — **Saved-location job discovery is available across core landing, city, regional and individual job pages:** the user must explicitly press `Use my location` before the browser asks for geolocation permission. Exact coordinates are sent only in a JSON POST to `/api/jobs/nearby` to resolve the nearest approved canonical town and current jobs within 15 straight-line miles; coordinates are not placed in URLs, analytics or browser storage. Only the matched town and region are retained in `localStorage`, restored on later visits, and removable with `Clear`. A manual town fallback is offered after refusal or failure. The saved-location strip remains separate from each vacancy's governed `Suitable jobs nearby` panel, which always stays anchored on the vacancy itself. Apply and the existing `Tap to search other jobs` control remain unchanged. Zero-result location searches remain explicitly at zero, but replace the generic national fallback with a governed 15-mile nearby search where current jobs exist, followed by the matched Ontap region if the user needs to widen again.

- 8 September 2026 — **Google Indexing API selection now enforces one explicit 200-notification Pacific-day allowance:** URL updates and deletions share the same persisted attempt ledger and already-attempted type/URL pairs are deduplicated. The former protected-lane/released-reservation policy was superseded on 21 September by JobG8-first selection, a 20-notification deletion allowance and a hard 10% non-JobG8 cap. Workflow reporting exposes quota usage and source-level live, candidate and selected counts.


- 7 September 2026 — **Exact duplicate live vacancy URLs are consolidated before discovery:** the shared published-job inventory now groups only adverts with the same source, normalised title, employer/recruiter, location and complete description, choosing the earliest factual posting date then stable job ID as the canonical Ontap vacancy. Listings retain the vacancy in each legitimate slice but link to the canonical ID; search, recommendations, static generation and the sitemap expose only that canonical URL. A duplicate ID remains resolvable while its source row is live and declares the selected canonical, avoiding an abrupt user-facing loss while Google consolidates it. Similar titles or materially different descriptions are never merged. Expired jobs continue to leave the live sitemap and internal inventory through the existing publisher, with Google deletion notifications already handled by the established Indexing API workflow.

- 6 September 2026 — **Service Admin city expansion is now office-intent led:** 29 owner-approved exact-town routes launch at four or more current Service Admin jobs, taking active Service Admin city pages from 24 to 53. All retain `/[town]/service-administrator-jobs`, while their title, H1, description, breadcrumbs and internal labels use `Admin and office jobs in [Town]`. The same governed town page may supplement Service Admin with exact-town Paralegal, Marketing, Finance / Accounts, HR / Recruitment and Customer Service / Contact Centre jobs. Support Worker is always excluded; Customer Sales is admitted only with explicit office/contact-centre evidence. Existing active routes receive the same office-family composition and wording without URL changes. Broad `/[town]/jobs` routes remain separate and are not duplicated where they already cover the same town.

- 6 September 2026 — **Broad JobG8 locations are refined from explicit advert evidence before publication:** the shared verified publisher now preserves regional selection but promotes a county/region-only displayed location to a specific town when the advert supplies a mapped postcode or an explicit workplace cue such as `Location:` or `based in`. The town must map back to the already-approved Ontap region; conflicting, uncued and non-JobG8 evidence remains unchanged. The current 1,526-job JobG8 snapshot contains 278 unique live-job refinements, raising projected exact-locality coverage from 886 to 1,162. This improves job-page location accuracy, city-opportunity counts and downstream city derivation without guessing that a broad county belongs to any particular town.
- 6 September 2026 — **Mobile navigation and job-detail onward links are simplified without changing desktop:** below 640 px the site header hides `Browse Jobs` and keeps `Home` aligned at the right edge. Individual job pages show only their primary onward link on mobile: the active exact-city page when the vacancy belongs to one, otherwise the governed regional slice. The secondary regional link remains available alongside the city link on desktop.
- 6 September 2026 — **Non-London job-listing promotion rails are consistent and desktop-only:** every `JobSlicePage` route now resolves to three role-appropriate course cards and the existing practical AI-help card beneath them. Office-based dynamic and generated city pages no longer fall back to a single or care-specific course set; support-worker pages retain three care courses. At mobile widths up to 700 px the entire promotional rail is hidden, leaving the job content uninterrupted. London keeps its existing explicitly configured three-card and AI layout.
- 6 September 2026 — **Individual job pages now provide direct search without weakening Apply:** desktop shows a shallow always-open `Search other jobs` strip with separate role/keyword and town/region fields; mobile starts with a compact outlined Ontap magnifying-glass control and expands the same fields only when requested. Both submit to the existing governed `/jobs/search` route, so its current matching, typo, field-reversal and published-index behaviour is reused unchanged. No discovery register, recommendation rule, public URL or publication mechanism changes.
- 5 September 2026 — **Ten permanent broad town/city pages launched across all live job families and providers:** Nottingham, Wakefield, Bolton, Reading, Chester, Durham, Gateshead, Northallerton, Norwich and Salford use shared `/[city]/jobs` rendering and a governed broad-city register. Exact-city vacancies appear first; up to six nearby vacancies may appear only from fully approved locality rules with approved coordinates inside a 15-mile straight-line ceiling, while retaining their true locations. Each route renders `Home > Jobs > Region > City`, CollectionPage, BreadcrumbList and ItemList markup, a wider-region results link, and remains live below its launch count. Homepage visibility retains the 4-job floor; Browse Jobs and the sitemap retain every active route permanently.
- 5 September 2026 — **Permanent city pages now expose their full role/region hierarchy in both directions:** every active registered city page renders a visible `Home > role > region > city` breadcrumb and an identical `BreadcrumbList` JSON-LD structure while retaining its existing regional-jobs call to action. Every matching regional role page automatically renders a high-page `Browse by city` module sourced from active entries in `city-page-register.json`; zero-current-job permanent city routes remain linked. Static regional routes and configured `/job-search/...` regional routes are resolved to their real public URLs, with no canonical, sitemap, inventory or publication-rule changes.
- 5 September 2026 — **Owner-approved job-detail discovery recommendations are now register-driven:** every individual `/jobs/[id]` page can show a discovery panel. It can show up to six suitable private-sector alternatives where the target shares the landing job's governed published family or has an explicit `role_relationships.csv` relationship, has an evidence-based `employer_sector_rules.csv` private classification, and is no more than **15 straight-line miles** away using canonical coordinates. Same-title jobs rank first, explicit relationships next, then other same-family jobs. The panel preserves each target's true job location and distance. Where no job qualifies, the panel and negative empty-state copy are suppressed and only the relevant regional slice link is shown. An unknown landing-employer sector does not block discovery because every displayed target must still be positively classified private; no private job can be directed to public-sector work. `city_nearby_rules.csv` remains the approved exclusion surface and `canonical_location_coordinates.csv` the locality source of truth.
- 5 September 2026 — **Discovery coverage was corrected after the first production audit:** 20 exact direct-company identities and 159 explicit recurring-title relationships remain available for ranking, but exact title rows no longer gate the whole panel. Same-family matching and unknown-source-to-private routing increase the 1,807-job audit snapshot from 21 to 475 pages with governed targets. Four ambiguous employer identities remain inactive `REVIEW`. `pipeline/scripts/audit_discovery_recommendation_coverage.py` reproduces the resolver gates and writes the per-job CSV plus concise Markdown report.

- 4 September 2026 — **The no-edit publication safety net accepts an external fallback dispatch:** `Apply and publish Ontap daily review` now accepts exact `AUTOMATIC_FALLBACK` as well as the owner-only `PUBLISH` approval. `AUTOMATIC_FALLBACK` follows the existing scheduled automatic-withhold path, including the same-date successful-dispatch check; it never enters manual quarantine mode. This allows cron-job.org to recover a delayed GitHub 11:45 schedule without turning untouched review items into exclusions or publishing twice. Manual `PUBLISH` behaviour is unchanged.

- 6 September 2026 — **City opportunities now expose their role-family mix:** each locality row retains its deduplicated all-job total and adds mutually exclusive counts for the eight governed Ontap families, plus an explicit `Other / unclassified` fail-safe. Canonical published-family assignment prevents jobs placed on multiple slices from inflating the breakdown; every row therefore reconciles to `All live jobs`.

- 3 September 2026 — **Daily overview adds all-role city opportunities:** `build_daily_region_overview.py` now deduplicates the complete live Ontap inventory and groups every job with an exact recognised town/locality from the canonical geo lookup, regardless of role family or provider. The Markdown report and Excel workbook add a filterable `CITY OPPORTUNITIES` table showing all-role live-job counts, existing permanent city routes, `CREATE` at 4+ jobs, `MONITOR` below four and a separate London hold. The first snapshot contains **283 mapped localities: 23 CREATE, 24 with an existing live page, 33 London holds and 203 monitors**. This is decision support only and does not publish pages automatically.

- 3 September 2026 — **Daily overview now reports every published/indexable page:** `build_daily_region_overview.py` mirrors the sitemap gates for core, regional/category, permanent city and individual live-job routes, then emits a reconciled `PAGES` section with one row per non-job URL. The Excel exporter adds a filterable `PAGES` tab with summary totals, live-job counts and explicit London sub-area routes. The first generated snapshot is **1,964 URLs: 1,833 individual jobs, 98 regional/category pages, 25 city pages and 8 core pages**.

- 3 September 2026 — **Thirteen additional regional/category slices approved for LIVE:** Service Admin adds North Scotland, Scotland Central - Tayside and Wales South - Valleys; Marketing adds Cambridgeshire, Cheshire - West, Essex, Merseyside - Liverpool and North East; Finance / Accounts adds Cheshire - Warrington & Halton and London; HR / Recruitment adds Sussex; Customer Service / Contact Centre adds Buckinghamshire and North East. The central register now contains **51 Service Admin, 16 Marketing, 10 Finance / Accounts, 7 HR / Recruitment and 6 Customer Service / Contact Centre LIVE markets**. The three newly configured UK markets reuse the canonical UK geography slugs and anchors; no family boundary or automatic activation rule changes.

- 3 September 2026 — **Four owner-approved Service Admin city pages launched:** Belfast (**27** exact-city jobs), Glasgow (**21**), Edinburgh (**10**) and Cardiff (**10**) are active permanent city routes derived from their existing LIVE regional slices. The owner explicitly approved a one-off waiver of the normal 3-of-7 history requirement after live-site/analytics review; the normal 6-current/3-of-7/explicit-approval rule remains canonical for later launches. All four use conservative exact-city catchments and are now registered in the recurring city-opportunity scanner.

- 3 September 2026 — **Post-review JobG8 category counts now reconcile to live inventory:** `Apply JobG8 review decisions` rebuilds `jobg8-feed-category-profile.csv` after applying owner decisions and before committing the reviewed outputs. `Build daily regional overview` listens directly for completion of that workflow because GitHub suppresses `push` events created with the workflow token; it therefore rebuilds the Markdown and Excel reports from the corrected profile rather than retaining the pre-review snapshot.

- 2 September 2026 — **Customer Service coverage and publication now deduplicate employer campaigns:** exact-title matches sharing the same region, employer and normalised advert campaign count once even when JobG8 supplies many IDs and synonymous titles. The same opening-location conflict guard used by Customer Sales rejects adverts whose stated location belongs to another region. This corrects the North East diagnostic spike from 78 raw rows—73 from EE, including 71 variants of one campaign—to distinct regional opportunities, and the rule is shared by diagnostics and LIVE publication.

- 2 September 2026 — **Twelve owner-approved regional slices activated:** Wales South – Cardiff & Vale Service Admin (**9** current jobs); Berkshire **8**, Hertfordshire **9**, Kent **9**, Scotland West – Glasgow **7**, Surrey **6** and Sussex **7** Customer Sales / Sales Advisor; and Bristol & Bath **8**, Gloucestershire **7**, Hertfordshire **9**, Kent **7** and Oxfordshire **9** Marketing are now `LIVE` through the existing central register and configured-slice publisher. The governed footprints become **Service Admin 48 / 78, Customer Sales 11 / 78 and Marketing 11 / 78**; no other slice changes.

- 2 September 2026 — **Daily overview enforces one JobG8 feed date across all four sheets:** the full JobG8 daily process now writes the supplier-category and published-category profile from the same materialised feed and prepared JobG8 outputs used for that run. The overview refuses to build if that profile date differs from the 78-market family-coverage date, preventing a current Sitewide/LIVE/NOT LIVE workbook from silently carrying a previous day's JobG8 categories.

- 2 September 2026 — **Homepage recent jobs diversified automatically:** the four-card homepage block uses genuine published vacancies from the newest 48-hour window with a clear numeric salary, then prefers distinct role families, regions and normalised titles before filling any remaining spaces. This prevents blank-pay cards and one same-source burst, such as several receptionist vacancies, from visually narrowing Ontap's range; no carousel, manual curation or publishing change is introduced.

- 1 September 2026 — **Homepage discovery hierarchy strengthened:** the homepage now leads with a branded search hero, dynamic live-job count and direct-apply/no-signup trust signals, followed by four of the newest real published vacancies before the existing role-and-region directory. Search behaviour, job destinations, routes and publishing pipelines are unchanged.

- 1 September 2026 — **Coverage audit exposes retained JobG8 evidence:** the complete selection-audit artifact includes `jobg8-published-absent-current-feed.csv`, listing every currently published JobG8 ID absent from the latest feed with title, employer, Ontap posted date, apply URL and its last date seen across the available raw JobG8 archive.

- 1 September 2026 — **Daily regional overview Excel is owner-ready:** the existing overview workflow exports and commits `pipeline/reports-daily/daily-region-overview.xlsx` alongside the Markdown report. Its four tabs are Sitewide, JobG8 categories, LIVE and NOT LIVE. The workbook export deliberately runs after the same-feed coverage/history patch so NOT LIVE contains the final `today / 14d avg / 6+ days` evidence in single-line, non-wrapped cells. The JobG8 category tab adds the published Ontap JobG8 count beside each supplier classification and a reconciled published total; these counts are generated by joining the current published JobG8 IDs to the exact raw feed used by the coverage audit.

- 1 September 2026 — **Daily overview now records the factual JobG8 feed profile:** each non-artifact JobG8 coverage audit writes the exact row count and `/Job/Category` distribution from its latest archived raw feed into `pipeline/reports-daily/jobg8-feed-category-profile.csv`. The existing daily regional overview displays that JobG8-supplied total and classification table immediately after the provider breakdown. Counts reconcile exactly to the audit workbook rows and are deliberately separate from Ontap's governed families and published inventory.

- 1 September 2026 — **Three owner-approved regional slices activated:** Bedfordshire Service Admin, Bristol & Bath Customer Sales / Sales Advisor and Buckinghamshire Marketing are now `LIVE` through the existing central slice register, governed selectors, configured dynamic routes and verified publisher. The approval evidence is respectively **9 / 6.0 / 6-of-11, 9 / 6.6 / 9-of-11 and 13 / 4.1 / 2-of-9**. The current governed footprints become **Service Admin 47 / 78, Customer Sales 5 / 78 and Marketing 6 / 78**; no other market is activated.

- 1 September 2026 — **JobG8 has a safe external scheduling fallback:** `Run full JobG8 daily process` accepts an authenticated `workflow_dispatch` for an explicit UK `morning` or `evening` cycle. A small committed state file records a cycle only after its full pipeline succeeds and is included in the existing guarded output commit. The workflow-wide `jobg8-daily` concurrency lock serialises GitHub cron and external requests; any later request for a completed same-date/cycle exits successfully without downloading, archiving, composing or committing a second time. A failed or unpushed run leaves no completion marker, so the fallback remains able to recover it. cron-job.org is configuration only, not a second pipeline or repository secret.

- 1 September 2026 — **NHS Google Jobs eligibility restored after strict-date regression:** NHS Jobs source timestamps containing fractional seconds without a timezone are now emitted as their factual `YYYY-MM-DD` source date in `JobPosting`, without inventing timezone precision. Strict fail-closed behaviour remains unchanged for every other source and malformed date. NHS-only Indexing API fingerprints are versioned once so restored NHS pages are resubmitted without consuming the daily quota on unchanged JobG8 or other-provider URLs.

- 30 August 2026 — **Fourth owner sweep extends governed title coverage:** exact reviewed titles add further routine Admin/Business Support, operational Payroll/Finance, Legal Support, direct Care/Support, People Operations and Sales Coordination roles to their existing governed families. Context-dependent PA variants retain advert checks; Housing Officer remains parked for its proper future family, IT Support remains parked, and the agreed managerial, training-advert, specialist and ambiguous titles remain outside automatic matching. The earlier generic `Area=City` geography correction already resolves the definite Belfast/Leeds/Birmingham/Nottinghamshire/Surrey misroutes in this workbook; ambiguous county/area conflicts remain unresolved rather than being force-mapped. Existing LIVE-market, salary, dedupe and specialist gates remain unchanged.

- 30 August 2026 — **Owner-reviewed no-register sweep encoded narrowly:** exact reviewed titles add routine Admin/Business Support, Customer Service, transactional Finance/Payroll, corporate EA/PA, Legal Support and direct Support/Care roles to their existing governed families. Optical, school behaviour/PMLD support, property/retail sales, technical, managerial and specialist roles remain excluded; apprenticeships and Supported Housing Officer remain parked. Generic JobG8 `Area=City` now falls back to the precise location rather than being misrouted to London, and SalaryAdditional-only pay is annualised in the coverage artifact. Existing LIVE-market, salary, dedupe and specialist checks remain in force.
- 30 August 2026 — **Google deletion notifications now follow live inventory changes:** changes to published `app/**/*.json` job inventory on `main` immediately trigger the existing Google Indexing API workflow, whose deletion-first plan sends `URL_DELETED` for previously submitted job URLs no longer live. The 19:30 UTC schedule remains as a fallback; the existing 200-notification cap, persistent state, concurrency guard and operational alerts are unchanged.

- 30 August 2026 — **JobG8 review application no longer creates temporary NHS 404s:** the JobG8 service-admin rebuild now runs the transactional NHS composer before committing its combined outputs, and includes the NHS review/decision surfaces in the same guarded commit. This prevents an intermediate `main` revision from deleting still-open NHS vacancies before the later NHS publisher restores them; NHS fetch, enrichment, source-cap and fail-closed controls remain unchanged.

- 30 August 2026 — **JobG8 coverage evidence and salary reporting made factual:** the artifact retains the raw JobG8 salary columns but labels the effective source as `structured`, `description_fallback` or `missing`, displays the effective salary text and calculates annualised values/bands from that evidence. The shared description parser also no longer attaches the words `Hourly rate` to a preceding annual salary amount; it selects the explicit hourly figure that follows. The former inferred `Selection status` is replaced by `Publication / coverage status`: exact current publication, governed-family register match in a LIVE or non-LIVE market, governed-register rejection, or no governed-register match. The artifact explicitly does not claim an actual selector decision when it has not executed that family selector.
- 30 August 2026 — **Automatic JobG8 discovery audits are main-only:** the path-filtered `push` trigger now runs only for changes already on `main`, matching the workflow's main checkout, AWS OIDC trust and diagnostic writeback target. Feature-branch pushes no longer start a doomed production audit; the existing manually dispatched, artifact-only route remains the sole non-main audit path.
- 30 August 2026 — **Owner-approved remainder of the missed JobG8 family-title review applied through exact refinements:** the existing Service Admin, Finance / Accounts, Customer Service, Customer Sales, Legal and HR / Recruitment selectors now admit only the named reviewed titles. `Personal Assistant` enters Service Admin only when advert text explicitly establishes executive/corporate-office PA work; direct-care, legal and ambiguous PA adverts fail closed. `Payroll , Pensions and HR Administrator (Hybrid)` remains an explicit Service Admin `HARD_PASS`. Generic title patterns, specialist exclusions, salary ceilings, geography, dedupe and LIVE-market gates are unchanged; focused regressions protect all additions and nearby exclusions.
- 29 August 2026 — **Owner-reviewed A–H false negatives added to existing governed families:** persistent exact-title decisions now cover the agreed accessible Finance / Accounts, Customer Service, HR / Recruitment, Service Admin and Support Worker adverts found in the owner audit. Narrow production exceptions admit Accounts Payable Analyst, Assistant Accountant, Finance Administration Officer, HR and Payroll Administrator, Customer Engagement Executive, driver-qualified Support Worker/Practitioner and direct Housing Support variants without weakening the existing salary, source-integrity, geography, duplicate, seniority or LIVE-slice gates. Customer Service production now consum…14474 tokens truncated…permanent review decisions. Source freshness and factual-fingerprint checks remain authoritative.

Publication isolation is hierarchical:

- up to 15 unresolved/malformed **mandatory-review** jobs in one source are withheld fail-closed while clean jobs continue;
- more than 15 such mandatory-review jobs, or a source-level integrity mismatch, isolates that source and retains its previous approved state;
- after TV regional composition, up to three named regions missing a usable base output or approved snapshot/evidence retain their previous live page while verified TV regions publish; four or more stop TV, and any composition/evidence integrity failure stops regardless of count;
- NHS untouched POSS rows are optional review opportunities and therefore do not count toward that isolation threshold;
- source publisher failures are fail-soft where the prior approved state can safely be retained;
- only a genuine combined/publication integrity failure should stop the whole publish.

Confirmed source paths include JobG8, NEJobs, VONNE, Teaching Vacancies and NHS Jobs.

Source freshness is owned upstream of the apply/publish orchestrator. If an active source review is stale or missing, the master review flags `NOT READY TO REVIEW`, excludes that stale source from the current master-review jobs, and must not treat its absence as zero inventory. A stale source does not by itself convert a later apply/publish run into a system-level failure: clean sources can continue under the isolation model. In particular, the parent apply/publish workflow does not refresh Teaching Vacancies; fresh TV state is produced by `run-teaching-vacancies-regional-review.yml`. TV discovery uses one complete audited national sweep: page audit failures retry that page, inconsistent route-level totals/ranges retry only that route, and persistent integrity failures stop the source. Exact equality with a second full sweep is not required because live vacancies can legitimately appear or close during the run.

The England-wide Teaching Vacancies Markdown is a pending-edit queue, not the full decision register. It shows only LIVE, non-hard-pass rows with a blank `manual_action`; previously resolved `select` / `exclude` rows remain in the master CSV and regional approval state and continue to carry forward only while their stable ID and factual fingerprint still match. During cross-day regeneration, obsolete Markdown blocks that are already resolved in the CSV or no longer reviewable are ignored; strict block/fact validation still applies when owner edits are applied.

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

Service Admin city launch gate: a non-London exact town with **at least 4 current governed Service Admin jobs** may be activated after explicit human approval. The four-job test is based only on Service Admin; supplementary office-family jobs cannot qualify a town. Other family-specific city pages retain their separately governed thresholds. READY FOR APPROVAL never publishes automatically.

Recorded exception: on 22 August 2026 the owner directly approved Bristol, Manchester, Cambridge, Birmingham, Peterborough, Warrington, Liverpool, Hull and Oxford Service Admin after the 55-region audit. Their current exact-city counts materially exceeded the six-job floor, but their dynamic configured-slice parents had not been included in the city scanner's seven-run history. This was a named one-off waiver, not a change to the standing gate.

Once `lifecycle_state: active`, the city route is permanent unless deliberately retired. Falling below its launch count does not delist or 404 the route; the active-city maintenance step rewrites the current output, including an empty array at zero jobs.

Homepage visibility is deliberately separate from permanence. An active city page appears as a homepage city card only at **4+ current jobs**. At 0–3 jobs the page remains live/indexable and refreshed, but its homepage card is hidden until supply returns to 4+.

Canonical Service Admin city thresholds:

- **4 current Service Admin jobs** = launch threshold with explicit approval;
- **4 total current page jobs** = homepage city-card visibility floor;
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
- `pipeline/reports-daily/daily-family-coverage.csv` — current same-feed eight-family assessment across all 78 UK markets (624 region/family rows);
- `pipeline/reports-daily/daily-family-coverage-history.json` — rolling latest-14-feed-date history for every family present in each snapshot; one snapshot per feed date, with same-date reruns replacing rather than duplicating;
- `pipeline/reports-daily/daily-region-overview.md` — sitewide unique/provider/duplicate reconciliation, all-role city/locality opportunities, page inventory and regional LIVE/NOT LIVE overview; NOT LIVE family cells display `today / 14d avg / 6+ days`, while LIVE cells count current published slice placements;
- `pipeline/reports-daily/live-job-source-count-YYYY-MM-DD.csv` — current provider/source counts, including NHS Jobs after verified publication;
- `pipeline/reports/city-opportunities-current.md` and `.json` — current city/local-market opportunity state;
- `pipeline/reports/city-opportunity-history.json` — rolling qualification history.

The rolling family history begins on **22 August 2026** with no backfill. Current snapshots store all 624 counts even though rolling metrics are displayed only for NOT LIVE slices; older snapshots may contain the smaller family set that existed at the time. The `6+ days` metric is a consistency/watch signal and is not an automatic publish threshold. Service Admin's separate standing rule is based on the **current governed same-feed count over 8**, not on the 6+ history metric.

Customer Sales national 78-market assessment is recurring diagnostic evidence for non-LIVE regions. The full JobG8 run produces it from the same current feed using the governed production classifier, canonical geography, campaign dedupe and final QA. A positive count does not activate a region; the slice register is authoritative. The 21 August **20 / 6 / 7** figures are a launch verification snapshot, not the current footprint or a standing publish threshold.

`pipeline/reports-daily/daily-region-overview.md` treats Sales Advisor as both a production family for LIVE reporting and a diagnostic family for NOT LIVE reporting. LIVE rows read the current published `app/_city-pages/configured-slices/**/customer-sales-jobs.json` data directly. NOT LIVE rows read the same-feed Customer Sales counts persisted in `daily-family-coverage.csv` and combine them with the observed history; a numeric `0` means assessed and none survived the governed rules. These non-LIVE values are decision support only and never switch a slice to LIVE automatically.

The city-opportunity scanner is diagnostic/decision support. It must not auto-activate a city page.

The daily overview's `CITY OPPORTUNITIES` section is the owner-facing all-role view. It counts each canonical live job once, matches only exact recognised town/locality evidence from `geo_lookup.xlsx`, shows existing routes from `city-page-register.json`, flags non-London localities at four or more current **Service Admin** jobs as `CREATE`, and keeps London as `HOLD – LONDON`. Each row also shows mutually exclusive counts for all eight governed role families and `Other / unclassified`; family assignment uses the job's published category before its file placement so office-family city duplication cannot relabel a Marketing or Finance job as Service Admin. Broader and unrecognised job locations remain visible in the summary count but are not guessed into a city. It never activates a route automatically.

Compiler Modules 1, 2 and 3 remain legitimate specialist/manual analysis workflows.

Report lifecycle is recurring operational reporting / deliberate specialist analysis / one-off diagnostics in Actions artifacts or Git history.

## 3. Website / UX

Every non-London `JobSlicePage` listing uses a consistent desktop promotion rail with three role-appropriate course cards and the practical AI-help card beneath them. Office-based dynamic and generated city pages resolve to the shared office set; support-worker pages resolve to three care courses; explicitly configured legacy pages keep their established three-card set. At mobile widths up to 700 px the whole rail is hidden. London retains its separately configured layout. The job-view switcher defaults first-time mobile visitors to Quick View and desktop visitors to Detailed View; a visitor's saved choice takes priority on later visits. The AI card links to `/ai-tips` with a validated regional/category source key; the page returns visitors to that exact approved listing, while direct or invalid visits see `Browse current jobs`. The canonical URL and breadcrumb schema stay fixed, and GA4 records AI-tip visits and return-link clicks.

Purpose: user-facing job search, job pages, navigation and presentation.

Saved-location discovery is progressive enhancement and does not alter server-rendered inventory, canonical URLs, sitemap inclusion or indexing. `components/SavedLocationJobs.tsx` owns browser permission, manual fallback and the town/region preference with its last displayed count; it restores that display immediately and refreshes the count in the background. `app/api/jobs/nearby/route.ts` resolves a submitted coordinate or town against the approved canonical location register; and `lib/discovery-recommendations.ts` remains the governed role/sector matcher. Exact device coordinates are transient request data only.

`components/Analytics.tsx` owns the GA4 bootstrap. It suppresses analytics collection only when the browser explicitly exposes recognised crawler/automation signals; it never blocks the underlying page. The same component emits `qualified_visit` on the first trusted pointer, keyboard, touch or scroll interaction in a browser session and uses anonymous first/last-seen timestamps in local storage to emit `returning_browser` after a 30-minute absence. No persistent visitor ID, town or coordinates are recorded by this mechanism. Saved-location return measurement remains separately owned by `SavedLocationJobs.tsx`. Externally distributed Ontap links should be generated with `npm run campaign:url -- ...`; internal links must not carry UTM parameters.

Zero-result searches do not inject unrelated vacancies into the result count. The saved-location panel's `View nearby jobs` action and its displayed count both use the same `near` search. When a searched location resolves through the approved canonical register, `/jobs/search` offers that separate search containing current jobs within 15 straight-line miles; the next fallback is that canonical location's Ontap region. If neither resolution is available, the existing role-and-region Browse Jobs route remains the safe fallback.


Verified structure:

- `app/` is the primary application route/data tree;
- `components/` contains reusable UI components;
- `components/SavedLocationJobs.tsx` is the shared client-side location panel used on the homepage, Browse Jobs, regional/city listing pages, live job pages and expired-job recovery pages. It restores only the approved town/region from `localStorage`, provides Change/Clear controls and never requests location until a user action;
- `app/api/jobs/nearby/route.ts` accepts JSON POST requests, maps coordinates or a submitted town to the nearest approved canonical location, and returns only the matched town/region, current 15-mile count and minimal governed recommendation fields;
- `lib/published-jobs.ts` supplies the common published job/detail layer and is also the build-time source for the compact search index;
- `lib/discovery-recommendations.ts` is the sole resolver for the job-detail **Suitable jobs nearby** panel: it accepts a target from the same governed published family or an explicit registered role relation, requires a positive private-sector target classification and a resolvable canonical locality within 15 Haversine miles, applies active locality exclusions, and ranks exact title before explicit relationship priority, then other same-family jobs, distance and posting date; unknown landing-employer sectors are permitted because targets still fail closed unless evidenced private;
- `pipeline/scripts/audit_discovery_recommendation_coverage.py` audits every currently published job through those same fail-closed sector, exact-role, canonical-location and 15-mile gates, producing `pipeline/reports/discovery-recommendation-coverage.csv` and `.md`; it is diagnostic and never activates or widens a rule;
- `lib/configured-job-slices.ts` reads the configured regional slice catalog/register;
- LIVE dynamic regional/category slices are register/catalog driven;
- `app/_city-pages/configured-slices/` holds dynamic configured-slice data;
- `app/job-search/[region]/...` is the dynamic route family;
- Browse Jobs, `/jobs/search`, job-detail backlinks and the homepage Admin grid consume published dynamic slices through shared mechanisms;
- all approved Customer Sales routes use that same mechanism; the three original launch routes at London, West Yorkshire and Manchester & Salford remain dated end-to-end verification examples rather than a complete current route list;
- homepage browse ordering is regional-first, then city, to make regional inventory breadth the primary visual signal;
- `lib/city-page-data.ts` reads `pipeline/city_pages/city-page-register.json` and resolves active city definitions/data;
- public city routes read private derived JSON under `app/_city-pages/...`, preventing duplicate job-detail URLs;
- homepage city cards are filtered independently at 4+ current jobs; this does not change route activation/permanence;
- NHS-sourced jobs use the same Service Admin regional/job-detail routes as other inventory and retain `source: "NHS Jobs"` plus the original NHS apply URL; employer names do not necessarily contain the word NHS;
- `components/JobDescription.tsx` + `lib/job-description.ts` provide presentation-only readable vacancy formatting. NHS flattened source text is split into short paragraphs while structured headings/bullets are preserved; long NHS adverts expose six blocks initially and keep the rest available under `Show full NHS role information`;
- `lib/job-display-order.ts` owns page-level source mixing after composition: normal inventory stays location-first and accepted NHS inventory is interleaved at no more than one after every four non-NHS jobs while preserving NHS Tier/switchability/freshness ranking;
- the London-wide `/london/service-administrator-jobs` route enables the sector-view trial through `JobSlicePage`; `lib/job-sector.ts` classifies known public/charity feeds and only explicit JobG8 evidence, while `JobViewSwitcher`, `QuickJobList` and `DetailedJobList` retain every result in initial server HTML and apply the selected view in the client. The canonical page URL, job-detail links and source inventory remain unchanged;
- public/charity badges and the reusable sector-switch banner make the grouping interpretable, while `/sector-switching` provides the linked transfer guide. All and Business views place the banner after five jobs visible in that selected view; Public service & charity uses an overview above its results;
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

NHS/public-sector inventory is a complementary supply and sector-switching advantage; it must not redefine Ontap as an NHS job board. Generic job discovery continues to mix NHS into the wider inventory under the source cap and the 4+1 display rhythm. The London-wide Service Admin trial now surfaces explicit NHS/public/charity interest through a client-visible sector view while preserving the single server-rendered all-jobs page.

## 5. Operations / infrastructure

Core scheduled workflows include:

- `run-full-jobg8-daily-process.yml` — GitHub cron remains primary; cron-job.org dispatches the existing workflow at 08:35 and 17:35 Europe/London as a fallback. A persisted same-date `morning`/`evening` completion marker plus the workflow-wide concurrency lock makes either trigger idempotent: a late duplicate exits before feed download, while a failed/unpushed attempt is not marked complete and can retry. The workflow includes fresh transactional NHS Service Admin composition, generation of all currently LIVE Customer Sales slices, same-feed 78-market diagnostic coverage and rolling 14-feed-date history maintenance;
- `run-nejobs-review.yml` — 06:15 daily;
- `run-vonne-review.yml` — 06:35 daily;
- `run-teaching-vacancies-regional-review.yml` — 06:55 daily; final review/manifests commit is protected by full-history checkout plus up to three pull-rebase/push attempts so concurrent `main` writes do not strand fresh TV state;
- `refresh-nhs-admin-service-review.yml` — 10:05 UTC daily;
- `ontap-daily-review.yml` — 08:45 Europe/London;
- `ontap-daily-status.yml` — the single owner-facing daily health check. It runs after `Ontap daily review`, after `Deploy Ontap production after publish`, and at 09:15/12:15 Europe/London as fallback snapshots. The morning result proves whether every source and the master file are ready to edit; the post-publish result proves whether the cycle was manual or automatic and whether every source publisher, verified-page build, live-source report and production deployment completed;
- `build-daily-region-overview.yml` — rebuilds the 78-market overview after successful **Run full JobG8 daily process**, **Apply and publish Ontap daily review**, or **Run JobG8 discovery coverage audit** completion, on any published `app/**/*.json` change, on relevant report/code pushes or manual dispatch. The direct coverage-audit completion trigger is required because commits made with GitHub's workflow token do not start downstream push-triggered workflows. Concurrent obsolete rebuilds are cancelled. LIVE counts and the sitewide reconciliation come directly from current published JSON; NOT LIVE family cells combine the current persisted same-feed counts with rolling history;
- `google-indexing-api.yml` — 19:30 UTC daily.

The manually run JobG8 discovery coverage audit is date-locked to the current Europe/London day. It derives the month dynamically, requires that exact daily raw feed to exist, and passes the expected date into the final selection-audit export. A missing or mismatched feed fails the workflow before any report commit. Consequently, the sitewide published JobG8 total, the JobG8-category published counts, and any “published ID absent from current feed” exception are all interpreted against the same dated feed; the category counts must reconcile to the published JobG8 total.

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

As reconciled from `pipeline/registers/region_category_slice_register.csv` on 24 September 2026, the register contains **163 LIVE rows**: Service Admin 52, Marketing 22, Customer Sales 14, Finance / Accounts 36, Support Worker 11, HR / Recruitment 9, Customer Service / Contact Centre 6 and Legal Assistant / Paralegal 13. A further 12 rows are CANDIDATE. The register is authoritative for current activation state.

The full JobG8 workflow enforces the current **78 markets × eight families = 624 rows** diagnostic contract and up to 14 feed-date snapshots. `city-page-register.json` contains **54 active permanent routes (53 Admin and office, one Support Worker)**. NHS feed isolation, the 20% Service Admin ceiling, the 4+1 display rhythm, Teaching Vacancies source isolation, deployment-built search/static live vacancy pages and normal Git-to-Vercel deployment with manual-only CLI recovery remain the verified production architecture.

## Documentation rule

When a persistent system-level change alters any canonical bucket, update this file in the same change. If live/active/user-facing state changes, update `SYSTEM_OVERVIEW.md` as well.

23 August 2026 — **safe geo lookup gap correction:** `pipeline/geo/geo_lookup.xlsx` remains the factual location-routing authority. Specific missing place mappings found during Legal Assistant / Paralegal discovery were added for Hook Norton, Woolston, Filey, Ware, Longfield, Milford Haven, Otley and Birmingham, plus safe county/location fallbacks where unambiguous. Broad ambiguous values such as `East of England` and bare `Merseyside` remain deliberately unresolved rather than being forced into a canonical market.
- 21 September 2026 — **Google indexing is now JobG8-first with a hard non-paying cap:** after the fixed deletion allowance, every eligible JobG8 candidate is selected before non-JobG8 candidates. Non-paying sources cannot exceed 20 of the 200 daily notifications (10%), and unused JobG8 capacity is never released to them. The workflow summary now reports live, eligible-candidate and selected-submission counts by source.

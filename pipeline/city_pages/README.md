# City-page derivation

City pages are derived geographic views of final approved regional pages. They are not separate feeds or classification pipelines.

The flow is:

`source feeds -> regional selection/composition -> verified regional app JSON -> city opportunity history -> human approval review -> active city page`

The common derivation engine is `pipeline/scripts/derive_city_pages.py`. Each approved city has its own technical configuration in `city-page-register.json`, including:

- the parent regional page;
- city-specific include, review and exclude location rules;
- a reason for every rule;
- the route and private derived-data output path;
- the six-job launch threshold;
- explicit `lifecycle_state: active` approval; and
- review-output paths.

The technical register is generated for new approvals and is not the normal human editing surface.

## City-page catchment principle

A city page represents an **approved local employment/commuting catchment anchored on that city**, not necessarily only vacancies whose location text is the exact city name.

The default launch rule is deliberately conservative: begin with the exact city/locality patterns that clearly belong to the market. The catchment may later be expanded to nearby towns, suburbs or districts only where there is a clear real-world employment/commuting relationship and the expansion does not bleed into a separate labour market.

Examples already approved in production:

- Leeds includes Leeds and Pudsey;
- Newcastle includes Newcastle, Gateshead, North Tyneside, Shiremoor and Wideopen;
- Brighton & Hove includes Brighton, Hove and Portslade.

New city pages should therefore be thought of as **city-anchored labour-market pages**, not literal string filters. Catchment additions are a governance decision and must be recorded in `city-page-register.json` with include/review/exclude rules.

Broad county or regional labels must never be treated as proof that a vacancy belongs to the anchor city. In particular, `Durham` must not match broad `County Durham` locations for city-page launch purposes unless the stated workplace is actually Durham city or an explicitly approved Durham-city catchment location. The market register now enforces that exclusion; the August 2026 Durham candidate remains on hold until its qualifying history is rebuilt from clean post-fix counts.

## Regional opportunity markets

`opportunity-market-register.json` defines the local employment markets to monitor underneath each broad regional slice. A region can have several independent markets: for example North East can monitor Newcastle, Sunderland, Durham and Darlington at the same time; Sussex can monitor Brighton & Hove, Crawley, Horsham, Eastbourne and other local markets independently.

The same regional market definitions are applied to every published category slice in that region. This means a Sunderland admin/service opportunity and a Sunderland support-worker opportunity build separate counts and histories from the same local-market definition.

A market may combine location labels only where they genuinely belong to the same employment market. For example Brighton and Hove are one monitored market, while Crawley and Horsham remain separate. Active city-page rules in `city-page-register.json` take precedence for an already launched page such as Newcastle.

Registered markets with one to three current jobs appear as **BUILDING**. Four or five jobs are **NEAR**. Six or more jobs enter the qualification-history process. Exact locations not yet in the register are still surfaced when they reach four jobs, so the monitor can reveal a market we forgot to define.

## Candidate and approval lifecycle

`pipeline/scripts/scan_city_opportunities.py` discovers possible city/locality splits across all published regional/category slices. `pipeline/scripts/update_city_opportunity_history.py` records the last seven verified-publish pipeline runs. A candidate becomes **READY FOR APPROVAL** only when it has at least six qualifying live jobs on at least three of those seven runs and still has at least six jobs now.

READY FOR APPROVAL never publishes automatically. READY cities are written to:

`pipeline/reviews/city-pages/city-page-approval-review.md`

For the human approval step, edit only the `action:` line in the relevant city block:

- `action: approve` = launch the city page;
- blank `action:` = hold it.

When that approval file is committed, `pipeline/scripts/manage_city_page_approvals.py` validates the candidate against the current registered market, generates the technical city configuration and route, and the city derivation pipeline writes the live city JSON. Future approved cities use the same generic process; they do not require city-specific classification logic.

As of 19 August 2026 the newly approved Service Admin city pages are Bradford, Huddersfield, York, Barnsley and Doncaster. Their initial launch catchments are exact-city only. Durham is explicitly held pending the County Durham safeguard and a fresh qualifying-history check.

On 22 August 2026 the owner approved a named one-off exception for Bristol, Manchester, Cambridge, Birmingham, Peterborough, Warrington, Liverpool, Hull and Oxford Service Admin. The 55-region audit found current exact-city counts of 38, 35, 27, 24, 14, 14, 12, 11 and 10 respectively, but their dynamic configured-slice parents had not accumulated city-opportunity history. Each page therefore uses the normal active/permanent city mechanism and a conservative exact-city catchment, while its register entry records the explicit waiver of the 3-of-7 evidence requirement. The standing launch rule is unchanged for later candidates.

## Permanent-page and homepage-visibility rules

Once a city page is explicitly active, the route is permanent unless it is deliberately retired. Falling below six jobs does not remove the page, delist the URL from the site architecture/sitemap, or return 404.

Homepage prominence is a separate UX decision from route permanence. An active city page is shown in the homepage city grid only while it has **at least 4 current jobs**. If it falls to 0–3 jobs, the route remains live/indexable and continues to refresh normally, but the homepage card is temporarily hidden. It automatically reappears when current inventory returns to 4+ jobs.

The three canonical thresholds are therefore:

- **6 jobs** = launch qualification threshold, subject to 3 of the last 7 verified-publish runs and explicit approval;
- **4 jobs** = minimum current supply for homepage city-card visibility;
- **0 jobs** = allowed for an already-active permanent city route; an empty active page is retained rather than removed.

This presentation rule must not be used as a reason to widen a city catchment artificially. Catchments remain evidence-led labour markets; low current supply is allowed to hide a city from the homepage rather than pull unrelated nearby markets into the page.

The ordinary derivation step may apply the launch threshold internally. `pipeline/scripts/maintain_active_city_pages.py` then rewrites every explicitly active city JSON from the current approved parent jobs even when the count is below six. At zero jobs it writes an empty JSON array rather than removing the output, so the page remains available and displays the site's empty-jobs state without stale vacancies.

The route reads from `app/_city-pages/...`. The private underscore directory is deliberately excluded from the published-job catalogue, preventing duplicate job-detail records or duplicate job URLs. Individual job pages continue to use the parent regional source data.

Only effective `include` jobs are written to city JSON; `review` and `exclude` jobs are omitted. The first left-hand CSV column is `decision`. It is pre-filled with the current automatic `include`, `review` or `exclude` result and may be changed to `include` or `exclude`. In Markdown, edit only the `action:` line: use `select` or `exclude`, or leave it blank to accept the automatic result. Genuine changes are retained by `job_id`.

Automatic inclusion must be supported by the stated job location. Employer or summary context may identify an obvious exclusion or ambiguity, but cannot by itself auto-include a job. JobG8 IDs are displayed with a `jobg8-` prefix in review files only so their source is obvious; the underlying live job IDs are not changed.

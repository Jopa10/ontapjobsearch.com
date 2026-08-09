# City-page derivation

City pages are derived geographic views of final approved regional pages. They are not separate feeds or classification pipelines.

The flow is:

`source feeds -> regional selection/composition -> verified regional app JSON -> city opportunity history -> explicit approval -> active city page`

The common derivation engine is `pipeline/scripts/derive_city_pages.py`. Each approved city has its own configuration in `city-page-register.json`, including:

- the parent regional page;
- city-specific include, review and exclude location rules;
- a reason for every rule;
- the route and private derived-data output path;
- the six-job launch threshold;
- explicit `lifecycle_state: active` approval; and
- review-output paths.

## Regional opportunity markets

`opportunity-market-register.json` defines the local employment markets to monitor underneath each broad regional slice. A region can have several independent markets: for example North East can monitor Newcastle, Sunderland, Durham and Darlington at the same time; Sussex can monitor Brighton & Hove, Crawley, Horsham, Eastbourne and other local markets independently.

The same regional market definitions are applied to every published category slice in that region. This means a Sunderland admin/service opportunity and a Sunderland support-worker opportunity build separate counts and histories from the same local-market definition.

A market may combine location labels only where they genuinely belong to the same employment market. For example Brighton and Hove are one monitored market, while Crawley and Horsham remain separate. Active city-page rules in `city-page-register.json` take precedence for an already launched page such as Newcastle.

Registered markets with one to three current jobs appear as **BUILDING**. Four or five jobs are **NEAR**. Six or more jobs enter the qualification-history process. Exact locations not yet in the register are still surfaced when they reach four jobs, so the monitor can reveal a market we forgot to define.

## Candidate and approval lifecycle

`pipeline/scripts/scan_city_opportunities.py` discovers possible city/locality splits across all published regional/category slices. `pipeline/scripts/update_city_opportunity_history.py` records the last seven verified-publish pipeline runs. A candidate becomes **READY FOR APPROVAL** only when it has at least six qualifying live jobs on at least three of those seven runs and still has at least six jobs now.

READY FOR APPROVAL never publishes automatically. A city becomes live only after an explicit human decision to promote it: add the approved configuration/route and mark the register entry `lifecycle_state: active`.

Newcastle admin and customer-service jobs is the first active city page. Its launch threshold is six jobs.

## Permanent-page rule

Once a city page is explicitly active, the route is permanent unless it is deliberately retired. Falling below six jobs does not remove the page, take it out of navigation/sitemap, or return 404.

The ordinary derivation step may apply the launch threshold internally. `pipeline/scripts/maintain_active_city_pages.py` then rewrites every explicitly active city JSON from the current approved parent jobs even when the count is below six. At zero jobs it writes an empty JSON array rather than removing the output, so the page remains available and displays the site's empty-jobs state without stale vacancies.

The route reads from `app/_city-pages/...`. The private underscore directory is deliberately excluded from the published-job catalogue, preventing duplicate job-detail records or duplicate job URLs. Individual job pages continue to use the parent regional source data.

Only effective `include` jobs are written to city JSON; `review` and `exclude` jobs are omitted. The first left-hand CSV column is `decision`. It is pre-filled with the current automatic `include`, `review` or `exclude` result and may be changed to `include` or `exclude`. In Markdown, edit only the `action:` line: use `select` or `exclude`, or leave it blank to accept the automatic result. Genuine changes are retained by `job_id`.

Automatic inclusion must be supported by the stated job location. Employer or summary context may identify an obvious exclusion or ambiguity, but cannot by itself auto-include a job. JobG8 IDs are displayed with a `jobg8-` prefix in review files only so their source is obvious; the underlying live job IDs are not changed.

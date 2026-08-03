# City-page derivation

City pages are derived geographic views of final approved regional pages. They are not separate feeds or classification pipelines.

The flow is:

`source feeds -> regional selection/composition -> verified regional app JSON -> city derivation -> gated city JSON`

The common engine is `pipeline/scripts/derive_city_pages.py`. Each city has its own configuration in `city-page-register.json`, including:

- the parent regional page;
- city-specific include, review and exclude location rules;
- a reason for every rule;
- the route and private derived-data output path;
- the minimum live-job threshold; and
- review-output paths.

Newcastle admin and customer-service jobs is the first configured live city page. It derives only from the final approved North East JSON. Only effective `include` jobs are written to the city JSON; `review` and `exclude` jobs are omitted. If fewer than eight jobs remain included, the derived JSON is removed and the route returns 404 until supply recovers.

The route reads from `app/_city-pages/...`. The private underscore directory is deliberately excluded from the published-job catalogue, preventing duplicate job-detail records or duplicate job URLs. The individual job pages continue to use the parent regional source data.

The first left-hand CSV column is `decision`. It is pre-filled with the current automatic `include`, `review` or `exclude` result and may be changed to `include` or `exclude`. In Markdown, edit only the `action:` line: use `select` or `exclude`, or leave it blank to accept the automatic result. Genuine changes are retained by `job_id`.

Automatic inclusion must be supported by the stated job location. Employer or summary context may identify an obvious exclusion or ambiguity, but cannot by itself auto-include a job. JobG8 IDs are displayed with a `jobg8-` prefix in review files only so their source is obvious; the underlying live job IDs are not changed.

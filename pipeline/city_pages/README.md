# City-page derivation

City pages are derived geographic views of final approved regional pages. They are not separate feeds or classification pipelines.

The flow is:

`source feeds -> regional selection/composition -> verified regional app JSON -> city derivation`

The common engine is `pipeline/scripts/derive_city_pages.py`. Each city has its own configuration in `city-page-register.json`, including:

- the parent regional page;
- city-specific include, review and exclude location rules;
- a reason for every rule;
- the minimum live-job threshold; and
- review-output paths.

The first configured page is Newcastle service-administrator jobs. Its initial mode is deliberately `review_only`: the process writes a CSV and Markdown summary, but no live Newcastle JSON or route. This allows the catchment rules and borderline decisions to be checked before publication is enabled.

Automatic inclusion must be supported by the stated job location. Employer or summary context may identify an obvious exclusion or ambiguity, but cannot by itself auto-include a job.

The first left-hand CSV column is the editable `decision` column. Enter `include` or `exclude` only where a reviewer wants to override the automatic decision; otherwise leave it blank. Saved decisions are retained by `job_id` across later review runs.

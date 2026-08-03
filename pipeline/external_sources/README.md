# External-source proofs of concept

## North East Jobs

`northeast_jobs_poc.py` is a controlled review-and-approval ETL. It:

1. reads the official North East Jobs all-vacancies RSS feed;
2. applies a broad provisional title/teaser screen;
3. fetches detail pages only for screened candidates;
4. standardises factual vacancy fields;
5. keeps only Ontap's two agreed North East geographies and excludes Tees Valley;
6. compares candidates with the current JobG8 workbook;
7. labels target candidates `HC`, `POSS`, or `HARD_PASS`; and
8. applies same-day manual `select`/`exclude` actions from the Markdown review;
9. writes CSV and Markdown review reports by default; and
10. writes a separate approved JSON only after an exact same-day review-set
    check and explicit `PUBLISH` confirmation.

A normal review run does not write to `output-admin-service`, `app`, or any
other live publishing location. The ETL never retains full North East Jobs
descriptions.

The reviewer CSV puts the North East Jobs vacancy first, suppresses weak
nearest-neighbour JobG8 candidates, and shows JobG8 candidate details only for
a credible confirmed or possible duplicate. Default `23:59` closing times are
omitted; earlier closing times remain visible. The first four text columns are
capped only in the reviewer output so GitHub's automatic CSV column sizing does
not make the sheet unnecessarily wide; the ETL record retains the full values.

### Stage 1: review

Run the **Run NEJobs review** workflow. It updates only:

- `pipeline/reviews/external/northeast-jobs-review.csv`
- `pipeline/reviews/external/northeast-jobs-summary.md`

It cannot create external JSON or change a live page.

The equivalent local command, run from `pipeline/`, is:


```bash
python -m external_sources.northeast_jobs_poc \
  --fetch-live \
  --acknowledge-source-terms
```

The acknowledgement confirms that the source terms have been reviewed. It is
not a claim that public availability grants permission to copy descriptions.

### Reproducible snapshot run

```bash
python -m external_sources.northeast_jobs_poc \
  --rss-file /path/to/rss.xml \
  --details-dir /path/to/detail-snapshots
```

Detail snapshots are named `<vacancy-id>.html`, `.txt`, or `.md`. Raw snapshots
are intentionally not committed; generated reports retain factual fields only.

The POC uses the repository's current:

- `input/jobg8.xlsx`
- `geo/geo_lookup.xlsx`
- North East salary review point of £30,000

External-source review outputs are kept under `pipeline/reviews/external/`;
the existing JobG8 review files are kept separately under
`pipeline/reviews/jobg8/`.

### Manual review

The Markdown report uses the same review pattern as the JobG8 pipeline. Edit
only the `action:` line in a vacancy block:

- `action: select` promotes a `POSS` vacancy into the selected set;
- `action: exclude` removes a selected vacancy or rejects a `POSS` vacancy;
- a blank `action:` leaves the automated decision unchanged.

Commit the edit and rerun the NEJobs process for the same `review_date`.
Decisions are matched by the stable North East Jobs `source_job_id`. Actions
from an older review date are ignored so stale decisions cannot carry into a
new vacancy run.

### Stage 2: approved output

After checking the Markdown review, run **Build approved NEJobs output** and
enter `PUBLISH` exactly. The workflow:

1. fetches the source again;
2. blocks if any detail page fails;
3. blocks if the current reviewable vacancy IDs or factual/classification
   fingerprint differ from the same-day review;
4. applies the reviewed `select`/`exclude` actions;
5. omits vacancies whose closing deadline has passed;
6. writes factual fields plus short original Ontap summaries to
   `pipeline/output-external/northeast-jobs-admin-service.json`; and
7. replaces the previous NEJobs subset in
   `pipeline/output-admin-service/north-east-admin-service.json`, preserving
   the current JobG8 jobs.

This stage still does not change `app/`. Review the combined count and then run
the existing **Publish verified pages** workflow as the final live-site gate.

The JobG8 daily and standalone service-admin workflows run
`compose_northeast_admin.py` after regenerating the JobG8 JSON. This reattaches
the most recently approved, still-open NEJobs subset without duplicating it.

### Reuse boundary

Approved records contain factual vacancy fields, source attribution, a stable
NEJobs-prefixed ID, Ontap referral parameters and original Ontap wording. They
do not contain copied source descriptions. This is a cautious practical
position, not a legal guarantee or a substitute for permission.

The screening rules are provisional and do not amend Ontap's permanent
selection rules.

## VONNE

`vonne_poc.py` is a separate, bounded review-only proof of concept. It reuses
the established NEJobs geography and review conventions where appropriate, but
has its own VONNE listing/detail parsers and makes no assumption that the two
source sites behave alike.

It:

1. reads the public VONNE Job Finder listing page;
2. extracts the stable `cid`, title, employer, salary, location, closing date
   and source URL from each listing;
3. fetches detail pages for plausible office/service candidates and retains
   only factual fields such as contract type, role type, hours, based location
   and VONNE role-description label;
4. excludes explicit Tees Valley roles using Ontap's existing North East rules;
5. retains explicit target-geography roles and forces generic `Hybrid`,
   `Home-based` or `Regionwide` roles to `POSS` for manual geography review;
6. compares retained vacancies with both the current JobG8 workbook and the
   currently approved NEJobs JSON;
7. flags same-source factual duplicates rather than silently discarding them;
8. classifies retained vacancies as `HC`, `POSS` or `HARD_PASS`; and
9. writes only CSV and Markdown review outputs.

There is deliberately no VONNE approved-JSON option, composition step, live
page path or publishing workflow in this first implementation.

### Run the review

Run the **Run VONNE review** workflow. It is manually dispatched and updates
only:

- `pipeline/reviews/external/vonne-review.csv`
- `pipeline/reviews/external/vonne-summary.md`

The equivalent local command, run from `pipeline/`, is:

```bash
python -m external_sources.vonne_poc \
  --fetch-live \
  --acknowledge-source-terms
```

A reproducible snapshot run can use:

```bash
python -m external_sources.vonne_poc \
  --listing-file /path/to/vonne-listing.html \
  --details-dir /path/to/detail-snapshots
```

Detail snapshots are named `<cid>.html`, `.txt`, or `.md`. Raw pages are not
committed. The standardised vacancy and reports do not contain the full source
description.

The Markdown report supports same-day `action: select` and `action: exclude`
edits for review continuity, but those actions cannot publish anything.

Source identity remains explicit in every review row through:

- `source: VONNE`
- stable `tracking_key: vonne-<cid>`
- the original VONNE source URL

A Monday/Thursday operating routine would align cleanly with NEJobs and
LinkedIn, but this POC intentionally creates no schedule. Frequency should be
agreed only after the first live review demonstrates that parsing, geography,
deduplication and closing-date quality are reliable.

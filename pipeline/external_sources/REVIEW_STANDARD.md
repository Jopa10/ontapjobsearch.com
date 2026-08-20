# External-source review standard

This is the required presentation and operating format for every new Ontap
external vacancy source. Before implementing a new source, inspect the current
NEJobs and VONNE review files and copy their established pattern. Do not invent
a source-specific review interface.

## Mandatory pre-POC intake gates

Before any POC, scraper, API integration, feed parser or other ETL work begins,
every proposed external source must pass both of these gates:

1. **Legal/commercial permission gate** — confirm that Ontap's intended use is
   permitted by the source's terms, licence, API/feed terms or explicit written
   permission. If permission is unclear, treat the source as HOLD and do not
   code around access controls, anti-bot measures or contractual restrictions.
2. **Application-route / two-click gate** — confirm that the source can provide
   an application destination that preserves Ontap's straight-to-employer / two-click
   principle wherever practical. A route that normally becomes
   `Ontap → source/aggregator advert → employer/application portal` is a material
   negative and must be explicitly approved before ETL development. Prefer a
   direct employer/application URL when the source lawfully exposes one.

A source that fails either gate is **rejected or parked before coding**, even if
its apparent vacancy volume is attractive. These gates come before volume,
additionality, field extraction and classification checks.

The canonical intake order is therefore:

`legal/commercial permission → application route → volume/additionality → POC → field audit → review → approval → live`

## Initial sweep to ETL acceptance gate

A source does not pass merely because vacancies were discovered and classified.
Before an initial sweep is accepted as an ETL source:

- compare the generated review with several live source adverts;
- verify title, employer, location, salary, posted date and closing date;
- include examples where a field is populated visibly but absent from structured
  metadata;
- add a source-specific visible-page fallback and automated fixture test for any
  such discrepancy;
- block the live review when a required core field is visible on the source but
  blank in Ontap's output; and
- record clearly whether a blank means `not stated by source` or `extraction
  failure`.

The source must not move to routine review or approved-output development until
this field audit passes. A successful fetch, geography filter or HC/POSS split
alone is not sufficient.

## Required repository outputs

Each source review writes exactly two files under `pipeline/reviews/external/`:

- `<region>-<source>-review.csv`
- `<region>-<source>-summary.md`

The regional slice must come first so reviews remain identifiable when the same
source is later used in more than one region. For example:

- `west-yorkshire-teaching-vacancies-review.csv`
- `west-yorkshire-teaching-vacancies-summary.md`

A normal review run must not write approved JSON, combined output, `app/`
content, or any live-site file.

## CSV presentation

- `final_decision` is the first, left-hand column.
- Rows are ordered `SELECTED`, `POSS`, `EXCLUDED`, then `HARD_PASS`.
- Source vacancy facts appear before duplicate diagnostics and internal fields.
- Weak nearest-neighbour duplicate candidates are hidden; candidate details are
  shown only for a credible confirmed or possible duplicate.
- The CSV and Markdown must represent the same decisions and row ordering.

## Markdown presentation

The summary follows the NEJobs/VONNE structure:

1. title;
2. `review_date`;
3. `review_fingerprint`;
4. the instruction `Edit only the action: line`;
5. run metadata, funnel and review outcomes;
6. `## SELECTED`;
7. `## POSS — choose SELECT or EXCLUDE`;
8. `## EXCLUDED BY REVIEW`;
9. `## HARD_PASS`;
10. safety boundary.

Every reviewable vacancy is an editable block delimited by `---` and contains:

```text
---
action:
SELECTED or POSS | geography | location | salary | title
employer: ...
closing_date: ...
reason: ...
source: ...
source_job_id: ...
source_url: ...
---
```

The reviewer changes only `action:`:

- `action: select` promotes a `POSS` vacancy;
- `action: exclude` removes a selected vacancy or rejects a `POSS` vacancy;
- a blank action leaves the automated decision unchanged.

Checkboxes, separate decision documents and source-specific review layouts are
not permitted.

## Decision safety

- Decisions are matched by stable `source_job_id`.
- Actions apply only to the same `review_date`.
- The review fingerprint covers every factual/classification field shown to the
  reviewer.
- Any later approved-output stage must refetch the source and require an exact
  same-day ID and fingerprint match.
- Review workflows commit only the two review files and verify that live output
  paths remain unchanged.

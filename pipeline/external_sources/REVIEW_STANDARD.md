# External-source review standard

This is the required presentation and operating format for every new Ontap
external vacancy source. Before implementing a new source, inspect the current
NEJobs and VONNE review files and copy their established pattern. Do not invent
a source-specific review interface.

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

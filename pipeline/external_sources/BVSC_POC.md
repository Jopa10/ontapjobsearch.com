# BVSC review-only proof of concept

This proof of concept is deliberately bounded to:

- source: BVSC Charity Jobs West Midlands;
- geography: Birmingham & Solihull only;
- category: Ontap admin/service only.

It reuses the shared Ontap title, salary, deduplication and review conventions from the existing North East Jobs and VONNE work, while keeping a source-specific BVSC parser because BVSC vacancies are article-style pages rather than an RSS/API feed.

## Behaviour

The module:

1. reads the current BVSC vacancies listing;
2. follows vacancy detail pages;
3. extracts title, employer, location, salary, closing date, a bounded description excerpt and the direct application link or email where available;
4. retains explicit Birmingham or Solihull vacancies, hard-passes explicit out-of-area vacancies, and sends generic hybrid/remote/West Midlands locations to `POSS`;
5. compares candidates with the current JobG8 workbook and configured approved external-source JSON files;
6. classifies each vacancy as `HC`, `POSS` or `HARD_PASS`;
7. writes only:
   - `pipeline/reviews/external/bvsc-review.csv`
   - `pipeline/reviews/external/bvsc-summary.md`

There is no approved JSON option, composition function, live-page path or publishing option.

## Source-specific limitations

BVSC adverts are manually supplied article pages. Labels and formatting vary, some closing dates are open-ended, direct application may be an email address rather than a URL, and the listing can retain old adverts. The POC therefore preserves uncertain facts for review rather than inventing values or treating an ambiguous vacancy as publishable.

## Run

From `pipeline/`:

```bash
python -m external_sources.bvsc_poc --fetch-live
```

For reproducible snapshots:

```bash
python -m external_sources.bvsc_poc \
  --listing-file /path/to/bvsc-listing.html \
  --details-dir /path/to/detail-pages
```

The manual **Run BVSC review** workflow tests the parser, refreshes the two review files and refuses to commit changes under `app/`, `pipeline/output-external/` or `pipeline/output-admin-service/`.

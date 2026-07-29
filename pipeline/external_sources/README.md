# External-source proofs of concept

## North East Jobs

`northeast_jobs_poc.py` is a review-only ETL proof of concept. It:

1. reads the official North East Jobs all-vacancies RSS feed;
2. applies a broad provisional title/teaser screen;
3. fetches detail pages only for screened candidates;
4. standardises factual vacancy fields;
5. keeps only Ontap's two agreed North East geographies and excludes Tees Valley;
6. compares candidates with the current JobG8 workbook;
7. labels target candidates `HC`, `POSS`, or `HARD_PASS`; and
8. writes CSV and Markdown review reports only.

It does not write to `output-admin-service`, `app`, or any other live publishing
location. It does not retain full North East Jobs descriptions.

The reviewer CSV puts the North East Jobs vacancy first, suppresses weak
nearest-neighbour JobG8 candidates, and shows JobG8 candidate details only for
a credible confirmed or possible duplicate. Default `23:59` closing times are
omitted; earlier closing times remain visible. The first four text columns are
capped only in the reviewer output so GitHub's automatic CSV column sizing does
not make the sheet unnecessarily wide; the ETL record retains the full values.

### Live research run

Run from `pipeline/`:

```bash
python -m external_sources.northeast_jobs_poc \
  --fetch-live \
  --acknowledge-research-only
```

The acknowledgement is required because North East Jobs' terms require written
permission for commercial reuse of site material. A live run is for internal
comparison research only.

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

The screening rules are provisional and do not amend Ontap's permanent
selection rules.

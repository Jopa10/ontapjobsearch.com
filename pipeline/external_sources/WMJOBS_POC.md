# WMJobs review-only proof of concept

Scope is deliberately limited to:

- source: WMJobs public RSS feed;
- geography: Birmingham & Solihull;
- category: Ontap admin/service only.

## Source design

The normal WMJobs search and job-detail pages return access-denied responses to automated clients. The public RSS feed at `https://www.wmjobs.co.uk/jobsrss/` is accessible and intended for syndication, so the POC uses that feed only. It does not use a proxy, renderer, browser challenge bypass, login, form submission or record-ID enumeration.

RSS provides title, employer, salary text, a short description/location hint, publication date and the original WMJobs job URL. It does not provide a dependable closing-date field. Missing closing dates therefore remain explicit in review output and no job can be published from this POC.

## Behaviour

The module:

1. fetches or reads a WMJobs RSS snapshot;
2. parses stable job IDs and factual RSS fields;
3. filters explicit Birmingham and Solihull roles, retains genuinely ambiguous hybrid geography as `POSS`, and records out-of-area admin/service rows as hard-pass diagnostics;
4. classifies `HC`, `POSS` and `HARD_PASS` using the existing Ontap admin/service patterns;
5. compares retained rows with current JobG8 and configured approved external-source JSON;
6. writes only:
   - `pipeline/reviews/external/wmjobs-review.csv`
   - `pipeline/reviews/external/wmjobs-summary.md`

There is no approved JSON, composition, live-page or publishing option.

## Local review command

From `pipeline/`:

```bash
python -m external_sources.wmjobs_poc --fetch-live
```

A reproducible run can use:

```bash
python -m external_sources.wmjobs_poc \
  --rss-file /path/to/wmjobs.xml
```

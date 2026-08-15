# NHS Jobs source audit — Ontap inventory

Date: 2026-08-15

## Decision

Proceed with a review-only NHS Jobs proof of concept for Administrative & Clerical vacancies. Do not publish NHS Jobs inventory on Ontap until NHS Jobs confirms the appropriate external-job-board access/reuse route and attribution/content boundary.

## 1. Source / API route

The current NHSBSA integration page says NHS Jobs supports third-party integration and that vacancies posted on NHS Jobs can be shared across national job boards. It currently links a Self-Serve API (XML/RSS) whose filters mirror NHS Jobs search.

A separate NHSBSA-published document is also indexed as **NHS Jobs External Job Board Vacancy API specification**. Because that title is a closer match for Ontap than the employer-oriented Self-Serve description, Ontap should ask NHS Jobs whether an external job board should be onboarded to that interface instead of relying on the Self-Serve feed for production redistribution.

For the technical POC only, use the public XML endpoint:

`https://www.jobs.nhs.uk/api/v1/search_xml`

with:

`staffGroup=ADMINISTRATIVE_AND_CLERICAL`

and page through the response using `page` plus the returned `totalPages` / `totalResults` values.

## 2. ETL and Ontap field map

The XML response exposes `vacancyDetails` records with these useful factual fields:

| NHS XML | Ontap review field | Production intent |
|---|---|---|
| `id` | `source_job_id` | Stable NHS source identity; future job id prefix `nhs-` |
| `title` | `title` | Title / selection logic |
| `employer` | `employer` | Future `company` / `advertiser_name` |
| `locations/location` | `locations` | Raw location evidence; region routing still to be added |
| `salary` | `salary_text` | Preserve source wording initially |
| `reference` | `job_reference` | Secondary source identity / audit field |
| `type` | `employment_type` | Contract label |
| `postDate` | `posted_date` | Freshness |
| `closeDate` | `closing_date` | Expiry / removal |
| `url` | `source_url` | Original NHS vacancy/application route |

The POC intentionally does not fetch or copy NHS detail-page descriptions.

## 3. Dedupe

Use two layers:

1. Exact NHS source identity (`id`) to prevent same-source duplicates across pages/runs.
2. Cross-source JobG8 comparison using Ontap's existing title/employer similarity convention: 65% title + 35% employer; `>=0.86` duplicate, `>=0.68` possible duplicate.

The POC loads current selected JobG8 rows from `pipeline/output-admin-service/*.json`, ignoring rows explicitly labelled as another external source. Confirmed JobG8 duplicates become `HARD_PASS`; possible duplicates become `POSS` for review.

Before production composition, extend cross-source dedupe to all implemented external sources so NHS cannot duplicate NEJobs, VONNE, Teaching Vacancies or future feeds.

## 4. Legal / reuse gate

Current evidence supports technical integration but does not yet remove the need for an explicit job-board reuse confirmation:

- NHSBSA says NHS Jobs integrates with third-party services and NHS Jobs vacancies can be shared across national job boards.
- NHSBSA's general website terms permit reuse of NHSBSA website information under the Open Government Licence with the stated attribution requirements.
- The current Self-Serve API wording is narrower: it describes employers displaying NHS Jobs listings on their own websites or intranets.
- NHSBSA also publishes/has published a document specifically titled `NHS Jobs External Job Board Vacancy API specification`.

Therefore Ontap should ask NHS Jobs to confirm:

1. Which API/feed they want an independent UK job board such as Ontap to use.
2. Whether commercial third-party display of externally advertised NHS vacancies is permitted.
3. Which returned fields/content may be republished, including any summary/overview text.
4. Exact attribution requirements.
5. Whether applications should link to NHS Jobs or another supplied external application URL.
6. Whether there are rate limits, update-frequency rules, takedown requirements, or onboarding credentials.

Until that answer arrives, this implementation remains review-only and retains factual fields only.

## 5. Technical implementation and production gate

Branch: `agent/nhs-inventory-poc`

Implemented:

- `pipeline/external_sources/nhs_jobs_poc.py`
- parser/classification/dedupe tests
- guarded GitHub Actions inventory review
- output restricted to `pipeline/reviews/external/nhs-jobs-admin-clerical-review.csv` and `...summary.md`
- explicit check that `pipeline/output-external`, `pipeline/output-admin-service` and `app` are unchanged

After NHS confirmation, the production implementation should add:

1. regional routing through Ontap's existing geography layer;
2. agreed source attribution and application URL handling;
3. approved-output JSON with stable `nhs-<source_job_id>` identity;
4. all-source dedupe before composition;
5. an NHS concentration cap/selection rule if needed so one employer ecosystem does not swamp a regional slice;
6. scheduled refresh and expiry reconciliation; and
7. only then inclusion in the existing verified-page publishing path.

There is deliberately no live-page publishing path in the POC.

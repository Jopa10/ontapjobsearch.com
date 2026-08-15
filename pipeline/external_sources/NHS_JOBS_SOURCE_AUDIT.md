# NHS Jobs source audit — Ontap inventory

Date: 2026-08-15

## Decision

Proceed with the review-only NHS Jobs proof of concept for Administrative & Clerical vacancies. The legal basis for an external job-board feed is substantially stronger than the initial source sweep suggested: the current NHS Jobs Employer Terms explicitly state that external recruitment platforms may take a feed of live vacancies displayed on NHS Jobs and advertise them on their own platforms.

Do not publish NHS Jobs inventory on Ontap yet. The remaining production gate is to confirm the correct NHS Jobs External Job Board API/feed route, onboarding requirements, attribution/content boundary, refresh expectations and any rate limits. Ontap will handle that communication separately.

## 1. Source / API route

The current NHSBSA integration page says NHS Jobs supports third-party integration and that vacancies posted on NHS Jobs can be shared across national job boards. It separately describes the Self-Serve API (XML/RSS) as allowing employers to display NHS Jobs listings on their own sites or intranets.

NHSBSA also currently indexes a document titled **NHS Jobs External Job Board Vacancy API specification**. That title is a closer match for Ontap's production use case than the employer-oriented Self-Serve wording, so Ontap should ask NHS Jobs which external-job-board interface/feed it wants Ontap to use in production.

For the technical POC only, use the public XML endpoint:

`https://www.jobs.nhs.uk/api/v1/search_xml`

with:

`staffGroup=ADMINISTRATIVE_AND_CLERICAL`

For efficient listing retrieval request `limit=100`, sort newest first, and page using `page` plus the returned `totalPages` / `totalResults` values.

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

## 3. Selection and dedupe

The NHS `Administrative & Clerical` staff group is a useful source filter, not a sufficient Ontap selection rule. Live sampling includes clear admin/service roles but also out-of-scope managers and other roles, so Ontap's title/salary/geography selection layer remains essential.

Use two dedupe layers:

1. Exact NHS source identity (`id`) to prevent same-source duplicates across pages/runs.
2. Cross-source JobG8 comparison using Ontap's existing title/employer similarity convention: 65% title + 35% employer; `>=0.86` duplicate, `>=0.68` possible duplicate.

The POC loads current selected JobG8 rows from `pipeline/output-admin-service/*.json`, ignoring rows explicitly labelled as another external source. Confirmed JobG8 duplicates become `HARD_PASS`; possible duplicates become `POSS` for review.

Before production composition, extend cross-source dedupe to all implemented external sources so NHS cannot duplicate NEJobs, VONNE, Teaching Vacancies or future feeds.

## 4. Legal / reuse position

Current official evidence supports external-job-board redistribution in principle:

- NHSBSA says NHS Jobs integrates with third-party services and that vacancies posted on NHS Jobs can be shared across other national job boards.
- The current NHS Jobs Employer Terms section 10 says NHSBSA is the owner or licensee of NHS Jobs material, that most NHS Jobs website content is published under the Open Government Licence and may be reused subject to the licence conditions, and that reused content must reference the NHS Jobs source using links to the website.
- Most importantly, Employer Terms clause 10.3 explicitly says external recruitment platforms may take a feed of live vacancies displayed on NHS Jobs and advertise them on their own platforms.
- NHSBSA currently indexes a separate document titled `NHS Jobs External Job Board Vacancy API specification`.
- The Self-Serve API page is worded for employers displaying their own listings. It should therefore be treated as a useful technical proof route, not assumed to be Ontap's final production contract/interface.

This changes the remaining question from "is a job board allowed to redistribute NHS vacancies at all?" to "which official external-job-board feed/API and operating rules should Ontap use?"

Ontap should confirm:

1. Which External Job Board API/feed an independent UK job board such as Ontap should use.
2. Whether any onboarding, credentials or commercial agreement is required despite the general permission in clause 10.3.
3. Which returned fields/content may be republished, including any summary/overview text.
4. Exact attribution/link requirements in addition to the Employer Terms/OGL wording.
5. Whether applications should link to NHS Jobs or another supplied external application URL.
6. Any rate limits, refresh-frequency rules, closure/takedown requirements or service expectations.

Until those operational points are confirmed, the implementation remains review-only and retains factual feed fields only.

## 5. Technical implementation and production gate

Branch: `agent/nhs-inventory-poc`

Implemented:

- `pipeline/external_sources/nhs_jobs_poc.py`
- `pipeline/external_sources/nhs_jobs_etl.py` with `limit=100` listing retrieval
- parser/classification/dedupe tests
- guarded GitHub Actions inventory review
- output restricted to `pipeline/reviews/external/nhs-jobs-admin-clerical-review.csv` and `...summary.md`
- explicit check that `pipeline/output-external`, `pipeline/output-admin-service` and `app` are unchanged

After the external-job-board feed details are confirmed, the production implementation should add:

1. regional routing through Ontap's existing geography layer;
2. agreed source attribution and application URL handling;
3. approved-output JSON with stable `nhs-<source_job_id>` identity;
4. all-source dedupe before composition;
5. an NHS concentration cap/selection rule if needed so one employer ecosystem does not swamp a regional slice;
6. scheduled refresh and expiry reconciliation; and
7. only then inclusion in the existing verified-page publishing path.

There is deliberately no live-page publishing path in the POC.

# NHS Jobs source audit — Ontap inventory

Date: 2026-08-16

## Decision

Proceed now on the assumption that the **NHS Jobs External Job Board Vacancy API** is Ontap's intended production interface. Do not wait for the NHS Jobs reply before building the downstream Ontap mechanics.

NHSBSA publicly says NHS Jobs integrates with third-party services, that vacancies posted on NHS Jobs can be shared across national job boards, and separately indexes a document titled **NHS Jobs External Job Board Vacancy API specification**. The Self-Serve XML/RSS feed is described for employers displaying their own listings, so it remains a useful review/discovery source but is no longer the production architecture assumption.

This does **not** mean guessing an unpublished endpoint, authentication method or payload schema. Ontap now isolates that first transport/decoder step behind an adapter boundary. Once the exact external-job-board endpoint/credentials/specification are available, that adapter can be filled in without rebuilding selection, switchability, slice composition or publishing logic.

Production pages remain untouched on this branch.

## 1. Source / API route

Production assumption:

`NHS Jobs External Job Board Vacancy API -> Ontap NHS adapter -> canonical NHS vacancy -> selection/switchability -> regional routing -> all-source dedupe -> source-mix guard -> verified page publishing`

The exact External Job Board endpoint/auth/schema is deliberately not hard-coded until it is known from the specification/onboarding details.

For inventory review only, the existing public XML endpoint remains usable:

`https://www.jobs.nhs.uk/api/v1/search_xml`

with:

`staffGroup=ADMINISTRATIVE_AND_CLERICAL`

The review runner requests `limit=100`, sorts newest first and pages using returned `totalPages` / `totalResults` values.

## 2. Stable Ontap adapter boundary

`pipeline/external_sources/nhs_external_job_board.py` defines Ontap's side of the production contract now.

Whatever the official NHS transport ultimately returns is decoded into a canonical `NHSExternalVacancy` with:

- stable NHS source identity;
- title and employer;
- one or more locations;
- salary / reference / employment type;
- posted and closing dates;
- source URL and application URL;
- optional description only where the official production feed permits it.

The canonical Ontap row uses stable identity `nhs-<source_job_id>`, source `NHS Jobs`, employer as company/advertiser, and preserves an external application route. The adapter deduplicates repeated records by official source identity before downstream processing.

No production HTTP transport or decoder schema is invented in this branch.

## 3. Selection, switchability and dedupe

The NHS `Administrative & Clerical` staff group is a useful source filter, not a sufficient Ontap selection rule. Ontap still applies its own role selection and person-specification/switchability layer.

Current review logic already checks likely JobG8 duplication. Before live NHS composition, dedupe must cover **all** sources so an NHS vacancy cannot duplicate JobG8, NEJobs, VONNE, Teaching Vacancies or later feeds.

NHS switchability is a separate Ontap value-add. When NHS capacity has to be throttled, `OPEN_SWITCH` jobs are given capacity before more restrictive NHS jobs; the source-mix code does not itself decide switchability.

## 4. Source-mix guard

`pipeline/external_sources/source_mix_policy.py` now owns a source-agnostic composition rule:

- all non-JobG8 inventory combined: **maximum 30%** of a normal slice;
- any one external source: **maximum 25%** of a normal slice;
- existing rows are never deleted merely to force the percentage down;
- if a slice is already at/above a cap, further external additions are deferred;
- JobG8 additions remain allowed because they reduce the external share;
- missing-source rows are deferred rather than silently accepted;
- deferred rows keep explicit reason codes; they are not silently discarded;
- NHS batches can be stably ordered so `OPEN_SWITCH` rows receive available capacity first.

The policy returns a concise workflow-summary line such as `CAP APPLIED — accepted X, deferred Y; non-JobG8 ...`. This is intended for routine visibility without creating another noisy email warning stream.

## 5. Refresh frequency

The live JobG8 workflow currently runs at 07:30 and 15:30 Europe/London. Initial NHS production cadence should be **once daily after the 07:30 JobG8 run**, rather than hourly polling.

Do not add the NHS production schedule until the official External Job Board transport is configured. At that point, schedule one morning NHS run after JobG8, then compose against the freshly built JobG8/external slice state. A second afternoon NHS refresh can be added later only if measured freshness/application value justifies it.

Expiry/takedown reconciliation runs as part of that same daily NHS cycle.

## 6. Legal / operating details still to confirm

Current official evidence supports external-job-board redistribution in principle, but Ontap should still obtain/confirm the operating details for the External Job Board interface:

1. exact endpoint/feed and authentication/onboarding requirements;
2. which returned content fields may be republished;
3. exact attribution/link requirements;
4. supplied application-route behaviour;
5. rate limits or refresh expectations;
6. closure/takedown/service rules.

Those details should change the thin adapter/configuration layer, not the rest of the Ontap pipeline.

## 7. Implementation state

Integration branch: `agent/nhs-external-api-integration`

Built/tested on the branch:

- existing review-only Self-Serve XML inventory runner;
- `nhs_external_job_board.py` production adapter boundary;
- stable `nhs-<source_job_id>` Ontap identity contract;
- `source_mix_policy.py` with 30% total-external / 25% single-source caps;
- explicit deferred-job reasons and workflow-summary text;
- NHS `OPEN_SWITCH` priority helper;
- tests for adapter identity/dedupe and source-mix boundary arithmetic;
- existing guard that review workflow cannot alter live app/output files.

Still to build before live publishing:

1. fill in the real External Job Board transport/decoder when endpoint/auth/schema are available;
2. regional routing through Ontap's existing geography layer;
3. connect the reviewed NHS selection/switchability classification into canonical rows;
4. central all-source dedupe before composition;
5. connect the source-mix guard to the final regional composer and persist deferred-job reporting;
6. expiry/deletion reconciliation and verified internal Ontap job pages with external NHS apply route;
7. morning scheduled run and exception-only alerting;
8. only then merge into the production publishing path.

There is deliberately no NHS live-page publishing path on this branch yet.

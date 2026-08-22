# Ontap Review Hub

The Review Hub is the single human-review layer above Ontap's source-specific pipelines.

## Operator contract

The operator normally touches one file only:

`pipeline/reviews/daily/ontap-daily-review.md`

Each morning the hub reads current source review outputs and includes only vacancies that still need a human decision. Automatic selections, hard passes and unchanged remembered decisions are omitted. A source that did not refresh for the current date is shown as `STALE` or `MISSING` and contributes no review items; it must never be interpreted as zero inventory.

Edit only `action:` in each review block (`select`, `exclude`, or blank). The apply workflow validates the stored fingerprint against the current source facts before copying a non-blank action back to the owning review surface.

If a source refresh is stale, fix/rerun that source first and then rerun `Ontap daily review` to rebuild the master edit file before reviewing. The publication layer is fail-soft where safe: a stale or failed source can be isolated while clean sources continue, but that does not make stale inventory equivalent to zero.

## Enabled sources

- JobG8 — service/admin and support-worker review queues.
- North East Jobs (NEJobs).
- VONNE.
- Teaching Vacancies — England-wide master review surface.
- NHS Jobs — live Administrative & Clerical Service Admin source. HC Tier A/B rows can publish automatically when otherwise eligible; untouched NHS POSS rows are optional review opportunities, remain fail-closed and are omitted from the normal mandatory owner queue.

## Adding future sources

To add another source, add one adapter to `adapters.py` that returns a `SourceResult` and `ReviewItem` records using the shared fields below. Add the source-specific action-routing branch only when the source becomes reviewable. Existing master-file, email and publishing orchestration should be extended rather than redesigned.

Required review item fields:

- `source`
- `source_job_id` (stable within the source)
- `title`
- `category`

Strongly recommended factual fields:

- `employer`
- `location`
- `region`
- `salary`
- `closing_date`
- `reason`
- `source_url`

The hub fingerprints the factual review record. A remembered decision is valid only while the fingerprint is unchanged.

## Workflows

`Ontap daily review` runs after the morning source refreshes, writes the one master review file and sends the review email when SMTP secrets are configured. It is the workflow to rerun after repairing a stale source when the operator needs a fresh edit surface.

`Apply and publish Ontap daily review` requires explicit `PUBLISH` after the master review has been completed, reconciles the current source state, fans decisions back to their owning source review files, then dispatches current source publishers sequentially. Existing source-specific approval and publication guards remain authoritative underneath the hub.

## Email secrets

The email sender is standard SMTP and requires repository secrets:

- `ONTAP_REVIEW_EMAIL_TO`
- `ONTAP_REVIEW_EMAIL_FROM` (optional if username is also the sender)
- `ONTAP_SMTP_HOST`
- `ONTAP_SMTP_PORT` (optional; defaults to 587)
- `ONTAP_SMTP_USERNAME` (optional for unauthenticated relay)
- `ONTAP_SMTP_PASSWORD`
- `ONTAP_SMTP_SSL` (optional; use `true` for implicit TLS/port 465)

# Neon shadow database: first checkpoint

Status: owner created the 12 tables in `ontap-db-test` on 2 November 2026 and supplied the resulting table list. Neon Free, London, Auth/Realtime off. The connection is verified as Preview-only under `ONTAP_SHADOW_`. Production remains file-based.

## Boundaries

The existing live file pipeline, selection rules, URLs, Brevo private tests,
Prisma models and publisher remain untouched. The repository already contains
legacy PostgreSQL `Job`, `Admin` and `Application` models; those are not the new
vacancy/alert design. In particular, the legacy `Application` means an Apply
click, not proof of a completed external application.

`001_initial.sql` defines exactly 12 tables under `ontap_shadow`, separate from
legacy `public` tables. No schedule, automatic cleanup, production switch or full test website is installed. The sample harness below is a deliberately invoked, build-only database check. Running the
SQL twice deliberately fails instead of silently accepting a mismatched schema.

## Table responsibilities

| Table | One record represents |
|---|---|
| suppliers | A supplier such as JobG8 |
| jobs | One Ontap vacancy with a permanent public ID |
| supplier_adverts | One supplier's representation of that vacancy |
| feed_runs | One identified feed snapshot and its acceptance outcome |
| advert_appearances | An advert's appearance on one supplier feed date |
| selection_decisions | A selector outcome for an advert/run/scope, with evidence and revision |
| subscribers | A subscriber, linked to an existing Brevo contact if relevant |
| subscriber_preferences | One saved preference and its signup job |
| consent_history | One grant or withdrawal, with exact wording/version |
| emails_sent | One attempted message, including queued/uncertain/failed states |
| job_recommendations | One job included in a message, with origin and matching evidence |
| activity_events | One measured action, keeping Apply clicks and confirmed applications distinct |

Supplier-specific wording lives in `supplier_adverts.raw_payload`. Job records
hold compact canonical details, with `preferred_advert_id` choosing an advert.
The full advert is not copied into each day's appearance record. The
`(advert_id, seen_on)` primary key prevents a same-day rerun doubling history;
its feed-run reference identifies the accepted snapshot most recently recording
that appearance. Per-run multiple intraday appearance history is not retained.
Only successful accepted snapshots may affect availability; failed imports must
not mark jobs missing. Disappearance/expiry policy still needs supplier evidence.

The supplier's ID remains the initial public ID, preserving `/jobs/[job_id]`.
Initial UUIDs are deterministic for replay safety. On later imports, the stored
advert-to-job relationship wins; do not reset a manually reconciled cross-feed
link to the initial generated UUID. Cross-feed matching is deliberately not
implemented yet. Different supplier IDs are not assumed to identify different
vacancies, and matching apply URLs alone is not conclusive.

Never treat unpublished as synonymous with excluded. Coverage audits do not
execute all production selectors. Record unknown when actual selector evidence
is absent, and later reuse production outcomes without reimplementing policy.

Sector and role-level fields support future recommendations but default to
unknown; they do not enable broader consent, step-up publishing or sending.
A recommended job stores its signup job, preference and sector snapshots so
later classification changes do not rewrite the history of a sent message.
`application_confirmed` requires external conversion evidence; an Apply click
must never be promoted to a completed application. Automated email-scanner clicks
need filtering before reporting engagement.

## Offline preflight

Use the XLSX produced by the existing `jobg8_xml_adapter.py`:

```bash
python pipeline/scripts/plan_shadow_jobg8_import.py \
  --feed-xlsx /path/to/current-jobg8.xlsx \
  --feed-date 2026-11-02 \
  --output /tmp/ontap-shadow-plan.json
python -m unittest discover -s pipeline/tests -p 'test_plan_shadow_jobg8_import.py'
```

Optional `--published-json` takes an array exported from the SAME completed
feed/publication snapshot. The preflight does not verify that snapshot's date;
its provenance must be verified before interpreting the comparison. It flags
published-but-absent IDs rather than inventing an expiry decision. It checks
identity, content hashes, daily appearance keys and raw/published counts. It does
not connect to a database, execute selections or write public inventories.

## Retention agreed with owner

Keep full adverts for **90 days after inactivity**, resetting the inactivity
clock on return. Later cleanup will clear raw descriptions/payloads while
retaining compact identity, relationships and daily appearance history. This
policy concerns job adverts; subscriber and click retention needs a separate
purpose-based decision. Cleanup is not implemented or scheduled here.

## Provisioning and cost controls: pending

Vercel team: `ontap1` / `team_xjm8VOa1951ZXxawa7UFF2gd`.
Existing production project: `ontapjobsearch.com` /
`prj_sLI0SohbF03NrRFj6yZyuN8mOOZB`.

The Vercel connector can list projects but returned 403 for integration
configuration access. No authenticated Vercel CLI exists in this workspace.
The owner has created and connected the test database through the dashboard. Vercel environment metadata confirms `ONTAP_SHADOW_DATABASE_URL` and related keys are sensitive and Preview-only. Their secret values cannot be retrieved through this connector; the verification build consumes them inside Vercel. Never put connection strings in chat,
Git, workflow output or a `NEXT_PUBLIC_` variable.

Suggested first setup: Free plan while a sample fits its limits; isolated test
resource; no production connection. Confirm current Marketplace pricing before
accepting a plan. For paid testing, begin at the smallest compute size, enable
scale-to-zero for test endpoints and set a spend notification at $20/month
(alerts at 80% and 100% where supported). This is a warning, not a hard total
bill cap. Confirm charges for restore history, backups and test branches too.
Keep an initial $25–40 monthly planning allowance, not a guarantee or approved
unlimited spend. Record daily accumulated usage and projected month-end spend
during early testing. Billing integration/API access remains unverified; no
notification or limit has actually been set.

## Following checkpoints

1. Provision an isolated Neon test resource; verify pricing, region, permissions,
   cost controls and credentials before executing this SQL. Confirm the database
   is not the legacy/live target. Keep subscriber data out of generic previews.
2. Execute SQL once, test constraints/rollback and inspect real storage usage.
3. Add an idempotent transactional shadow importer to the existing pipeline,
   with acceptance gates and real selection evidence, using the same raw feed.
   A shadow failure must not delay live publication. Test gaps, returns, changed
   content, failed feeds and replay before enabling routine shadow runs.
4. Reconcile whole-feed counts and representative published jobs; then build a
   protected test website using the shared read mechanisms, preserving URLs.
5. Migrate alert history/preferences/consent only with verifiable provenance.
   Brevo sender retry safety must treat ambiguous sends separately from success.
6. Prove the complete test flow and rollback before the production switch.
7. Add supplier two only after the JobG8 database route is proven.

## Sample importer checkpoint

`harness/importer.mjs` imports 1–20 normalized **published JobG8 adverts**, with
transactional upserts, stable IDs, content hashes, daily appearance keys and
accepted-snapshot replay protection. It preserves an existing advert-to-job link.
All imported jobs remain `withheld` inside the test schema. It records inclusion
as published-snapshot evidence, not a newly evaluated selector decision.

`harness/sample.json` pins 20 existing adverts from London published inventory
at source revision `a828536b62928d5c287fa9e18aa7924769851e29`. The observation
date is 2 November, not a claimed supplier feed timestamp or job-posting date.
It is not a complete raw feed, so no missing advert is expired. The full raw-feed
importer and actual per-selector exclusion reasons remain subsequent work.

Run `npm ci` and `npm test` in `database/shadow/harness` for PostgreSQL-backed
PGlite tests. They cover replay, updates, gaps/returns, rollback, invalid IDs, old
snapshots, same-day appearances, partial-feed isolation, referential integrity
and the distinction between Apply clicks and confirmed applications.

For the deliberate remote check, upload the harness files (excluding tests and
node_modules) as one Preview deployment in the existing `.com` project. The
harness `vercel.json` applies only to this uploaded source bundle. Do not edit
project-wide build settings or use the production target. `verify-neon.mjs`
requires Preview, the exact Neon project `noisy-fire-97386602`, and TLS. It uses
only `ONTAP_SHADOW_DATABASE_URL`, never the legacy `DATABASE_URL`. It persists
the 20 real samples, verifies repeat import, and rolls back simulated future
dates/title changes. It exposes no database-write HTTP handler; static output
contains only a sanitized verification summary. Existing Vercel Preview SSO
protection applies. No Brevo messages are sent.

Credentials are not copied to Git, logs, artifacts, chat or local environment
files. Free limits remain the initial spending boundary; no paid plan upgrade
or paid-plan spend notification has been configured.

## Verified Neon result — 2 November 2026

Preview deployment `dpl_ByCsyjqCviLDoQPyo4z8BB24vTwc` ran source revision
`bb08111dda3b11ce5c8978c43124b7e0af98eeb4` and reached READY. The build ran
in 44 seconds, exposing no runtime functions. It verified the live Neon schema
and imported the pinned 20 real adverts. Before: all six importer-owned tables
empty. After: 1 supplier, 20 jobs, 20 supplier adverts, 1 accepted sample run,
20 daily appearances, 20 published-snapshot decisions.

Replay, unchanged content, updated content, stable public IDs, gaps, return from
inactivity, rollback and conflicting replay rejection all passed against Neon.
Simulated future days/title changes were rolled back. Subscribers, consent,
emails, recommendations and activity tables were not populated. Database size
was 8,912,896 bytes (8.5 MiB), including normal PostgreSQL database overhead.
This is not an extrapolated full-feed storage measurement.

Project metadata checked after the preview retained framework `nextjs`, Node
24, unchanged project update timestamp and existing Preview SSO protection.
No production deployment, project-wide build edit, paid upgrade, scheduled job
or Brevo send was performed. Whole-feed import and the test website remain
subsequent checkpoints.

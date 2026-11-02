# Neon shadow database: first checkpoint

Status: foundation prepared on `feat/neon-shadow-database`; NOT migrated, connected or live.

## Boundaries

The existing live file pipeline, selection rules, URLs, Brevo private tests,
Prisma models and publisher remain untouched. The repository already contains
legacy PostgreSQL `Job`, `Admin` and `Application` models; those are not the new
vacancy/alert design. In particular, the legacy `Application` means an Apply
click, not proof of a completed external application.

`001_initial.sql` defines exactly 12 tables under `ontap_shadow`, separate from
legacy `public` tables. No migration runner, schedule, automatic cleanup,
production switch or test website is installed in this checkpoint. Running the
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
The owner must create/connect the Neon test database through the dashboard, or
provide a supported authorized connection. Never put connection strings in chat,
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

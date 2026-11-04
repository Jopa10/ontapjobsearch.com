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

The owner-approved general policy is to keep full adverts for **90 days after
inactivity**, resetting the inactivity clock on return. A narrower exception
applies to adverts whose verified selector outcome is EXCLUDE in every
production family: retain their full payload for three calendar days from the
first fully excluded run, then clear only `raw_payload`. Keep supplier identity,
content hash, compact selection history and all linked job/run records. Repeated
identical excluded snapshots do not restart the window; changed content starts
a new review window, while an advert no longer excluded clears the exclusion
marker. Payload deletion is transactional and must follow successful selector
readback. This is an explicit shadow retention operation, not scheduled cleanup
or an expiry decision. `002_exclude_review_window.sql` adds the marker to an
already-created test schema without deleting data. Subscriber and click
retention needs a separate purpose-based decision.

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

## Guarded staged raw-feed test

`stage-request.json` requests the archived 2 November feed at 20%, 50%, then
100%. `.github/workflows/test-neon-jobg8-staged.yml` runs only on pushes to
`feat/neon-shadow-database` that change that request file. There is no schedule
or production trigger. A separate concurrency lock serializes database tests.
It reads the existing S3 archive using the established archive role and downloads
one ZIP once; its SHA-256 is fixed for all stages. It does not request a new
JobG8 feed, write the archive or invoke publication. Role access from the test
branch must be verified by the actual run; do not change AWS trust to bypass
a denial.

`prepare_raw_stage.py` validates IDs and creates deterministic nested subsets
using hash order, preserving original raw JobG8 fields. This exercises supplied
adverts across the feed, including unsuitable and unpublished roles. Normalized
job records retain stable IDs; existing advert-to-job links are preserved.
Original descriptions and all supplier pay wording are retained in raw payloads.
Full normalized salary fallback/geography/selection integration is pending.

`harness/staged-importer.mjs` writes batched transactions, one accepted run per
archive fingerprint and stage, one advert per supplier ID, and one appearance
per advert/day. An identical stage replay changes no row counts. Earlier-day
raw content cannot overwrite later advert content. Selection outcomes are
explicitly unknown pending same-snapshot production evidence. No job is marked
missing/expired from a partial stage, and no test job is publicly published.

`verify-stage-neon.mjs` executes only within the specific Neon test resource and
Preview environment. It measures actual whole-database and per-table storage
before/after, counts, elapsed import/replay time and duplicate protection. Before
writing, a conservative payload-based estimate must fit under **800 MiB**; the
limit cannot be raised through the request beyond that ceiling. After writing,
measured growth and average schema bytes per advert project full-feed size with
50% headroom. If that or actual database size reaches the ceiling, later stages
stop. This is a test threshold, not a provider billing cap. Neon remains Free;
no plan upgrade is authorized. It does not estimate 90-day turnover retention.

The workflow uses the existing Vercel token only during Preview deployment.
Neon credentials stay inside Vercel. It emits sanitized measurement JSON, with
no raw adverts, environment files or tokens in the uploaded report artifact.
Each Vercel deployment contains a build-only importer and static summary; no
database-write endpoint or persistent worker remains. Existing project-wide
build settings and production domains are not changed.

Validation before running: seven PostgreSQL-backed importer tests, two archive
preparation tests, parsed workflow YAML/shell and syntax/diff checks. The new
checks exercise all three nested fractions, replay conflicts and preflight
storage rejection before any records are written. Results must distinguish
source receipt total, fraction imported, total stored adverts (including the
previous 20 samples) and unknown selection evidence.

### Source fallback after archive permission check

Run `41499293820` stopped before downloading or writing data: the AWS role
refused `sts:AssumeRoleWithWebIdentity` from the feature branch. AWS trust was
not changed. The next attempt instead uses the existing `JOBG8_FEED_URL`
repository secret to save **one direct supplier snapshot** into runner scratch,
then uses the identical ZIP/hash for all three fractions. This is an isolated
data fetch, not a production pipeline run or publisher dispatch. `archiveDate`
in the request denotes the observation/snapshot date for this fallback; the
source mode is explicit. No S3 archive is read, modified or pruned. The workflow
no longer requests AWS/OIDC permission. No database records were added by the
failed archive-access attempt.

### Duplicate supplier IDs in the received snapshot

Direct-fetch attempt `41499849031` detected repeated supplier IDs before any
database writes. The test preparation now distinguishes identical repeats
(collapsed to one advert, with counts retained) from differing payloads sharing
an ID (quarantined by ID, up to the repository's 15-record integrity boundary).
More conflicting IDs stop this isolated source test for assessment; clean live
publication is not involved. Reports distinguish total received rows, unique IDs,
exact repeats, conflicting IDs held and clean unique records. Stage fractions
apply to clean unique records. The source ZIP is retained for two days as a
GitHub Actions artifact for reproducible retries, without any credentials.

### Connector-driven staged execution

Run `41500434597` saved source artifact `13168067903`, inner ZIP SHA-256
`046881410cda7588c5589af808449b6e3f41c8b889955de8b57c23be426ab5bd`.
It contains 43,798 source rows, 43,797 unique supplier IDs, zero identical repeats
and one conflicting ID `1401786160` (two rows held), leaving 43,796 clean IDs.
The repository Vercel CLI authentication returned User not found before database
access. Its token was neither retrieved nor modified.

The supported Vercel connector creates the test Preview builds instead.
`harness/bootstrap-stage.mjs` downloads the preserved source artifact via a
short-lived file URL, verifies the inner ZIP hash, prepares the requested slice
and invokes the same staged importer. Temporary URLs are supplied only in the
deployment source, never committed or logged; refresh them between stages.
Only sanitized report output is deployed. No persistent database-write endpoint.

The GitHub branch workflow is now **source preparation only**: it no longer
installs a deployment CLI or receives the Vercel token. Its earlier failed runs
added no raw-feed database records. The source workflow remains unscheduled and
request-file-triggered; documentation/code updates alone do not rerun it.

## Verified staged result — 2 November 2026

All three connector-driven Preview builds reached READY using the same source
ZIP/hash and tested commit `8abd9c7a8e24db33de55448f39ff6f5dec40545b`.

| Stage | Clean adverts in snapshot fraction | Whole database bytes | Import time | Repeat time |
|---|---:|---:|---:|---:|
| 20% | 8,759 | 47,865,856 | 16.2 seconds | 0.389 seconds |
| 50% | 21,898 | 119,357,440 | 38.9 seconds | 0.382 seconds |
| 100% | 43,796 | 242,335,744 | 74.9 seconds | 0.389 seconds |

Each repeat added no jobs, adverts, daily appearances or decisions. The final
counts are 1 supplier, 43,796 jobs, 43,796 supplier adverts, 4 accepted test runs,
43,796 daily appearance records and 74,473 selection-evidence records. Decisions
include each stage's explicit unknowns plus the original 20 published-snapshot
observations; they are not a count of published jobs. The 20 original sample
adverts are all represented in the final clean feed.

One conflicting ID `1401786160` accounts for two held source rows; its raw
variants remain in the two-day source ZIP artifact. These are not falsely
merged or published. Current total is about 242 MB decimal (231 MiB), including
PostgreSQL overhead, indexes and staged test history. The 800 MiB safety gate
passed at each stage. This does not measure daily turnover or 90-day retained
storage. No paid plan upgrade or spend setting was changed.

The live production alias was checked after completion and still points to
`dpl_DFvFXPE9uCPaDzZWuCDsSS1gRQEc`. Project framework, Node version, update
timestamp and SSO protection were unchanged. No production database, publisher,
selection rule, schedule, expiry process or email sender was modified.

See `staged-verification-2026-11-02.json` for per-stage receipts and deployment
IDs/URLs. Next attach same-snapshot existing selector evidence and normalize
existing display fields through shared code before connecting a test website.

## Same-snapshot selector parity harness (prepared; verification pending)

`run_selector_parity.py` checks the pinned archive hash and receipt, uses the
existing XML adapter, withholds the already identified conflicting ID, and
preserves supplier row order. It creates two isolated scratch copies of the
pipeline's scripts, geography, registers, configuration and current owner review
stores. Both execute the existing Service Admin and Support Worker entry points,
including the seven family generators reached through the Service Admin chain.
It does not execute the daily workflow, fetch a feed, compose external sources,
enrich outputs, derive cities, publish, deploy production or send email.

The first replay is unchanged file processing. The second observes actual
executed rejection gates with Python 3.12 per-code monitoring; it does not evaluate or
copy policy expressions. Existing selector decision CSVs take precedence, and
actual selected output rows take precedence over intermediate states. Unobserved
rows stay **unknown** and block database attachment. Exact equality of all LIVE
family output arrays (including ordering and display fields) is required. The
observer is confined to the test harness; no production selector is edited.

Decision scopes are `production:<family>` and describe that family's generated
inventory, **not global job suitability**. An exclude can mean an actual policy
rejection, non-LIVE geography, duplicate suppression or a final output gate.
Eligible candidates withheld by a final threshold/campaign gate are explicitly
identified; they are not invented human review decisions. Review outcomes come
from actual production reports. Original raw-import unknown records remain as
historical evidence in their original scope.

```bash
python database/shadow/test_selector_capture.py
python database/shadow/run_selector_parity.py \
  --archive /path/to/ontap-shadow-feed.zip --work /tmp/new-parity-work
# logs, report.json and compact selection.json.gz are written only in scratch
```

`harness/selection-importer.mjs` verifies all stored advert content hashes against
the pinned raw input, then attaches eight scoped decisions per clean advert to
the existing accepted 100% run in one transaction. It compares every stored ID,
outcome, reason and gate, verifies exact replay, and preserves withheld jobs,
raw payloads, public IDs and availability. It refuses incomplete evidence,
conflicting replay and projected/measured growth above 800 MiB. The deliberate
`verify-selection-neon.mjs` Preview build uses the same fixed Neon resource and
saved `ONTAP_SHADOW_` connection; it exposes only a sanitized static receipt.
No runtime write handler, recurring import or cleanup is installed.

Scope limitation: this proves the JobG8 family-generation boundary, not full
publisher/city/composed-inventory parity. Those later boundaries and the protected
database-backed website remain pending. No full-feed storage import is repeated.
The exact original ZIP has additionally been preserved as `ontap-shadow-feed.zip`
for continuation after the short-lived GitHub artifact expires.

Fresh saved-source mode was prepared on 4 November 2026. Pass
`--source-request database/shadow/fresh-integration-prep-checkpoint-2026-11-03.json`
with the archived ZIP to validate the pinned 3 November S3 object metadata and
counts before selector execution. The request fixes the archive key, bucket,
region, 35,800,056-byte length, SHA-256, 44,432 source rows, 44,430 clean
records and quarantined ID 1401786160. It sets `ONTAP_FEED_DATE=2026-11-03`
for both isolated selector copies and captures that value in runtime provenance.
The original command without this option still uses the historical 2 November
pin. The existing isolated workflow now offers a `fresh_selection_parity`
request mode that downloads the saved ZIP through a short-lived
`ONTAP_SAVED_FEED_URL` Actions secret, then runs this exact checkpoint-backed
validation. Create the presigned GET URL only in owner CloudShell; never put it
in code or chat. No new workflow or AWS role is added. The mode is not triggered
until `stage-request.json` is deliberately updated. No fresh replay has run.

### Durable selector replay execution

Request mode `selection_parity` extends the existing branch-only shadow test
workflow. It downloads artifact `13168067903` from run `41500434597`, verifies
the fixed inner ZIP fingerprint in the harness, and runs the two independent
scratch replays concurrently. This mode never reads the supplier URL secret,
prepares storage fractions, connects to Neon, publishes or sends emails. It
retains the compact selection fixture, sanitized count/hash receipt and replay
logs as `neon-shadow-selection-parity` for seven days. Includes retain exact
region membership. The original source is also preserved in ChatGPT as
`ontap-shadow-feed.zip`; no new supplier fetch is a substitute for a lost pin.

The initial local replay attempt was interrupted by a scratch-workspace reset
before its full comparison/receipt could be retained. No database decisions
were attached. Existing completed storage measurements remain authoritative;
this durable run repeats selection verification only. A success must still be
followed by the guarded Preview attachment and its database readback check.

The existing `harness/bootstrap-stage.mjs` also accepts deliberate build-source
mode `selection_parity`: download the completed compact artifact through the
supported temporary file URL, verify its separately supplied SHA-256, and run
`verify-selection-neon.mjs`. This URL is never committed or printed. Only this
later Preview build can attach decisions; the GitHub replay has no database
credentials. Selection artifact extraction and decompression are bounded.

A no-write replay verifies the existing full evidence before reserving storage;
it does not project another copy of rows already stored. New attachments still
pass both projected and measured storage checks. A PostgreSQL-backed regression
test exercises replay when the reported database size is near the ceiling.

### Recording overhead correction

The first durable run completed unchanged file generation, but its global
`sys.settrace` dispatcher also received calls from helpers that did not need
recording. The observed Finance pass was still advancing after an hour. No
Neon decisions were attached. The replacement recorder uses Python 3.12
`sys.monitoring` local events on the explicit selector main/QA code objects
only. No global events or global trace hook are installed, and helper functions
are not monitored. Actual gates, report precedence and output-equality checks
are unchanged; monitoring is removed even when a selector raises.

Three recorder tests and five PostgreSQL-backed attachment tests pass. A focused
1,000-advert helper-heavy comparison produced identical output and all 1,000
identical evidence records under old/new observers; this is a recorder check,
not a replacement for whole-feed parity. The full private comparison still
reuses the exact original ZIP. Completed raw-storage stages are not rerun.
The workflow additionally retains available replay output/evidence files for
two days in a separate recovery artifact, so an interrupted comparison need
not discard a completed file pass.

## Verified selector attachment — 2 November 2026

2 November 2026 — **Selector parity and Neon attachment verified:** run `41530087079` passed exact output equality across 239 region/family outputs with zero unknowns and 4,884 unique selected jobs. Preview `dpl_FBiZhrK7ogdwbtmtSK7cqZtQJWeF` attached 350,368 scoped decisions, compared every stored outcome/reason/gate/region and verified replay adds nothing. Whole database measured 390,012,928 bytes under the 800 MiB ceiling; all 43,796 jobs remain withheld. Receipt: `database/shadow/selection-verification-2026-11-02.json`. No raw-feed import, production publish, email or paid-plan change. Next: shared display-field normalization and protected database-backed test website; full composition/city parity, expiry and turnover retention remain unproved.

Stop checkpoint: no replay or raw import is needed. Resume by inspecting current branch and the saved receipt. Build the protected read-only test website using existing display normalization; preserve public IDs and production isolation. Do not infer full publisher/city parity from this family-generation test. The historical raw-import unknowns remain in their original scope; current production-family decisions are complete. Retention/turnover sizing must be resolved before enabling recurring ingestion.

## Recoverable display checkpoint — 3 November 2026

3 November 2026 — **Protected display preview in preparation (not deployed):** `harness/display-snapshot.mjs` projects exact verified selector display rows into existing selection-decision evidence, checks membership/apply URLs, reconstructs every ordered region/family output and enforces the 800 MiB ceiling. Two focused display roundtrip/rejection tests pass. No display data has yet been attached to Neon and no preview website has been built. Resume from this checkpoint; reuse recovery artifact `13183730978` from run `41530087079`, compare plain/observed outputs and require the existing receipt hash before attaching display data. Existing completed storage/selection tests must not be repeated. City/final-publisher parity remains pending.

- 3 November 2026 — **Protected display preview execution started:** deployment `dpl_CrdoMGjyLYY7i3gszcJVrJiyghZm` (`ontapjobsearch-ot0bj3nlo-ontap1.vercel.app`) runs the saved `build-display-preview.mjs` builder using recovery artifact `13183730978`. It verifies matching plain/observed outputs and the attached selection receipt, materializes selected display fields inside existing decision evidence, reads them back exactly, verifies replay and renders static test pages. Completion/receipt NOT YET VERIFIED at this checkpoint. No production changes. Resume by inspecting this deployment, not starting a duplicate.

## Verified display checkpoint

3 November 2026 — **Protected database display preview verified:** deployment `dpl_CrdoMGjyLYY7i3gszcJVrJiyghZm` reached READY. Database readback exactly reproduced the saved 239 ordered family/region arrays (hash `c2b1c7710151669e4592b0954ec6023ddd250638ebbf9eb00aeda6959b02ae83`); 5,821 selected scoped display records produced 4,884 unique static job pages. Replay changed no display records. Database measured 407,306,240 bytes, under 800 MiB. Sample deployed page returned HTTP 200 with expected title/salary and noindex. Production alias remains on `dpl_EYL6UPXQyg8BHAZpcZHGTWe7MDwb`; no publication/email/plan change. Receipt: `database/shadow/display-verification-2026-11-03.json`. This is a simplified build-time database preview, not the production Next.js UI or continuous ingestion. City derivation, composition/enrichment, production title/facts rendering, turnover retention and final publisher parity remain pending. Stop/resume here; do not rerun completed storage or selector tests.

## Full-site verification recovery checkpoint

3 November 2026 — **Full Next.js/city verification prepared, not yet verified:** `build-full-preview.mjs` exports only the accepted pinned display snapshot in a read-only Neon transaction, checks its exact output hash, runs `prepare-full-preview.py` using existing `publish_one`, city derivation and active-city persistence functions, then builds the actual Next.js site. All writes are confined to the Preview build checkout. Job inventory from the pinned checkout is cleared to prevent stale/other-source mixing. Scope is saved JobG8 only, not external composition or current live inventory. The local isolated publisher preparation is in progress; two active-city persistence tests pass. No remote full-site deployment has been started. Resume from this checkpoint and inspect existing activity before launching anything; do not repeat storage/selector tests or touch production.

- 3 November 2026 — **Full-site preview running:** pinned commit `2dc121e664822ccae9a51f6c8425ef0ec90d6737`, deployment `dpl_2TntDxthA37CKoEhtzhGxiX6bDs7`, URL `https://ontapjobsearch-cqpbodnnm-ontap1.vercel.app`. Local existing-publisher preparation passed all 239 regions/families and 66 active family-city pages (1,131 entries). Remote Next.js build/HTTP/rendering remain UNVERIFIED. Inspect this exact deployment before any retry; no duplicate run. Local receipt and resume details: `database/shadow/full-preview-checkpoint-2026-11-03.json`. This is read-only Neon and isolated Preview, not production publication.

Full-site attempt `dpl_2TntDxthA37CKoEhtzhGxiX6bDs7` failed before publisher preparation: Vercel lacked openpyxl. Builder now pins openpyxl 3.1.5. Local city suite: 19 derivation + 2 persistence tests pass. No database writes. Retry only after saving this fix.

## Verified full-site checkpoint — resume here

3 November 2026 — **Full-site saved-snapshot verification passed:** protected Next.js Preview `dpl_7PjH6yDhdu2esqKB6B8w3BkE2hJV` reached READY at pinned code `2ef581c170f2592bda022909dd88bdae5cbca58a`. Read-only Neon export matched the exact saved output hash. Existing publisher/city code produced 239 regional outputs and 66 active family-city pages (1,131 entries); Next.js compiled, type-checked and generated 5,238 static routes. Homepage, North East, Newcastle, Leeds, Nottingham broad-city and job detail returned 200 with normal headings/CSS/noindex. Newcastle desktop layout and Quick view were checked in-browser. Sample counts: Newcastle 18, Leeds 93, North East 78, Nottingham broad 36. Existing website code reconciles 4,884 selected advert IDs to 4,849 displayed jobs: 33 duplicate aliases and two existing London-guard exclusions. No database writes, production alias/settings change, email or paid-plan change. Receipt: `database/shadow/full-site-verification-2026-11-03.json`. This is build-time DB export using pinned website code, not live database querying or current-feed/external-composition parity. Mobile/exhaustive UI, current-feed ingestion, retention/turnover and eventual cutover remain pending. All attempts and recovery details are retained; no build remains running.

## Read-only retention audit — prepared 3 November 2026

`harness/measure-retention.mjs` uses a repeatable-read READ ONLY transaction in the existing verified Preview-only Neon project. It measures relation/index/TOAST allocation, logical raw payload and scoped decision/display evidence sizes, daily appearance counts and accepted run dates. PostgreSQL statistics are estimates where labelled; logical field sizes are not reclaimable disk space. No feed fetch, import, cleanup, schema change, selector replay or production operation is performed. Sanitized aggregate receipt is the only output. Save implementation before deliberate remote execution and record deployment ID immediately. Daily raw turnover cannot be established from the single accepted full snapshot.

The read-only audit also reports payload rows/bytes by fully-excluded, other complete-selector, and incomplete-selector groups for the latest accepted run with persisted full-family decisions. An absent selector baseline is reported with zero in those groups and must be treated as insufficient evidence, not as zero excluded adverts. Capture this baseline before applying migration 002 or importing the fresh feed.

## Exclusion review baseline — 4 November 2026

The Preview audit `dpl_2cc1SchxPFFGdQ8xUhE1oGm2hgJo` completed from a repeatable-read `READ ONLY` transaction. The database measured **407,363,584 bytes**, the same as the last saved post-probe allocation. It contains 43,796 adverts and all 43,796 still have a full raw payload (101,655,870 `pg_column_size` bytes; 164,477,431 bytes as JSON text). Against the latest complete 2 November selector run, 38,633 are EXCLUDE in all eight families (89,251,788 payload bytes); 5,163 have another complete outcome (12,404,082 bytes); there are no adverts without complete selector coverage. All 43,796 jobs remain withheld. No 3 November feed was imported, migration or cleanup ran, and production is unchanged. Receipt: `exclude-review-baseline-2026-11-04.json`.

The 800 MiB code ceiling leaves 431,497,216 bytes at this baseline. This is not fresh-import approval: the saved 3 November raw-only forecast, even with its reserve, excludes the new selector/display history allocation. The fully-excluded payload count is an upper bound for eventual logical raw payload removal; clearing JSON does not guarantee the Neon database's physical size shrinks by the same amount. The new review marker migration is not applied.

## Retention measurement completed — 3 November 2026

READ ONLY audit `dpl_CpW9YzU2p8Y2foqopoVBKbLtowAV` reached READY. Whole database: 407,347,200 bytes; decisions: 207,028,224; supplier adverts: 158,597,120; stable jobs: 24,428,544; appearances: 8,708,096. Exact counts distinguish 350,368 production decisions from 74,473 historical test observations. Daily append-everything is unsuitable: 90 days of appearances alone plus today's other data projects to about 1.18 GB, before new adverts/decisions. Current raw turnover is UNKNOWN (one full date only). No records were deleted or imported. See `retention-measurement-2026-11-03.json` and `retention-assessment-2026-11-03.md` for measurements, assumptions and proposed hot-state/archive approach. The agreed 90 days after inactivity is not shortened; archival/compaction remains proposed and unimplemented. Next compare a pinned completed snapshot offline and budget before any fresh DB import. No audit remains running.

## Offline turnover and admission budget — 3 November 2026

The existing `pipeline/scripts/plan_shadow_jobg8_import.py` now accepts `--previous-feed-xlsx`, `--previous-feed-date` and `--storage-receipt`; optional `--quarantine-duplicates` collapses exact repeats and holds up to 15 conflicting IDs for offline comparison only. Default strict duplicate rejection is preserved. Both inputs must be complete raw snapshots with the same adapter field representation; mixed formats/schema changes must be normalized before interpreting changed hashes. No source fetch, lifecycle mutation or importer is invoked.

Two saved August full spreadsheets validate exact ID/hash comparison: 9,998 clean IDs each, 682 added/absent, 357 changed and 8,959 unchanged. One conflicting ID is held in each input. This historical fixture does not establish current 50k turnover. Returns remain unknown without earlier complete ID history. Source file checksums and exact counts are retained in `turnover-budget-verification-2026-11-03.json`. Ten preflight/comparison/budget checks pass.

Today’s completed source profile records 44,432 received rows. The existing importer appends raw unknowns plus eight family scopes (nine decisions per clean advert), not only eight family rows. At this received-row upper bound, the conservative allocation model requires 842,141,387 bytes including 50% growth headroom and a 64 MiB reserve, EVEN with hypothetical zero new/changed adverts. That is above the unchanged 838,860,800-byte ceiling. This is a forecast rejection, not measured future usage or an enforced importer gate: the CLI reports the result and never authorizes/imports data. Current full raw turnover remains unmeasured because recent full feeds are in private S3; no access/trust policy was changed.

Resume: reduce repeated decision evidence with verified current-state reuse and recoverable historical archives before any fresh full database import. Do not spend a full selector replay or fresh import to confirm this rejected budget. Implementing reuse requires complete dependency keys, exact readback and protection for pinned verification evidence; archive/lifecycle changes remain separately controlled. No remote run was started for this offline checkpoint.

## Compact decision history checkpoint — prepared 3 November 2026

`selection-history.mjs` encodes immutable compressed baselines and daily deltas in existing feed-run diagnostics; no table/schema change. `attachCompactSelection` in the existing selector attachment entry point validates complete fresh eight-family evidence, exact raw-run membership/hash, dependency metadata, ancestry, replay and full readback. It never skips selector execution. At most six delta links precede a fresh baseline. Existing pinned selection/display rows are untouched. The staged importer has an explicit full-snapshot-only compact mode: per-advert raw unknown rows are replaced by a single run-level pending marker until verified compact evidence is attached; default legacy mode is unchanged. Nothing is connected to production or a recurring workflow.

Five new local codec/PostgreSQL tests pass. Full existing regression suite and local compression/readback of the saved 350,368-decision artifact are in progress. No Neon write or remote build has been started. Dependency hashes in the full-fixture storage experiment are explicitly synthetic, not certified historical provenance. Display-row storage/export and appearance-history compaction remain separate pending work. Resume by checking local execution results or rerunning only this offline storage check; do not repeat selectors or fetch/import a feed.

## Compact decision history verified locally — 3 November 2026

All 19 harness checks passed (including five new codec/PostgreSQL checks); additional provenance/older-snapshot safeguards passed the five-test compact suite afterwards. The saved real fixture (artifact 13184005546, SHA-256 `7eb9b15fe9bbeb0334d179d282af5431cb41c93125d909c4209d73aacaf9c58a`) round-trips all 350,368 decisions / 43,796 source hashes exactly in canonical evidence order. Compressed baseline: 3,367,165 bytes; JSON/base64 payload: 4,489,915 bytes. A synthetic unchanged subsequent snapshot produces 3,497 encoded bytes and zero new decision/source-hash entries. This is local encoded-size evidence, not measured PostgreSQL/Neon allocation or a current turnover estimate. The experiment explicitly uses synthetic dependency hashes; real manifest provenance is still required before a real run.

The existing raw importer’s opt-in compact mode reserves only demonstrably new/changed raw payloads, plus touch/index allowance for every row and a fixed 64 MiB reserve. It measures under the supplier transaction lock and checks actual allocation before commit. Default legacy budget/unknown decision representation is unchanged. Compact pending runs cannot claim verified selection; attachment requires complete freshly verified outcomes and exact raw-run provenance. Replays compare full evidence and add nothing. Historical readback has a maximum of six delta links; periodic complete baselines intentionally repeat state to bound read time. No runs may be deleted while a child delta still depends on them.

No schema changes, new tables, Neon writes, cleanup, full-feed imports, selectors, publication or emails were executed. Current Neon remains at its last measured ~407 MB; no storage was reclaimed. Full daily website display reconstruction from this compact format is NOT yet implemented: existing pinned `selection_decisions`/display evidence and preview builders remain intact. Appearance histories still grow daily, so this does NOT establish 90-day Free-plan viability. See `compact-selection-verification-2026-11-03.json`.

Recovery: implementation checkpoint `5a5b15fc5d986b96b17603d5b0df52e8fcd44921`; final implementation/receipt saved in the same branch. Local full-fixture verification is reproducible with `node database/shadow/harness/verify-selection-history-offline.mjs /path/to/selection.json.gz /tmp/receipt.json`. No remote run remains active. Next: compact exact appearance history and integrate verified display state before the fresh-feed/retention test; preserve the agreed 90-day inactive-advert history and stable URLs.

## Compact appearance and display checkpoint — 3 November 2026

Opt-in compact raw imports now store a checksummed compressed exact supplier-ID manifest in existing feed-run diagnostics rather than daily appearance rows. Dates remain on runs; missing/returning IDs reconstruct exactly. Attachment checks this manifest against current stored adverts and complete verified selection. Legacy raw/import/display representations are unchanged. These JSON references do not create foreign keys: future cleanup must retain referenced advert identities and parent selection runs, validate archives first and preserve stable URLs. No cleanup is implemented.

Compact display attachment validates exact output hash, selected IDs/regions, row ordering and raw Apply URLs; database readback/replay is exact. The existing full-preview builder can read verified compact display or its existing legacy representation and still requires the pinned accepted output hash. It was syntax-checked; no remote build was started.

The saved full artifacts reconstruct 43,796 IDs from a 170,998-byte encoded manifest and all 239 regional arrays (5,821 entries) from a 6,185,669-byte display payload. Complete outputs hash remains `c2b1c7710151669e4592b0954ec6023ddd250638ebbf9eb00aeda6959b02ae83`. Local PostgreSQL tests cover three dates with gaps/returns, zero daily appearance rows, stable identities, display attachment/readback/replay and corrupt manifest/display rejection. Saved full-fixture tests use synthetic dependency metadata solely for storage verification. Receipt: `compact-snapshot-verification-2026-11-03.json`.

IMPORTANT: daily full display snapshots still require bounded verified historical archival. Keeping 90 full displays plus appearances and periodic decision baselines would exceed the unchanged 800 MiB ceiling, even without turnover. This change does not certify 90-day Free viability. No Neon write, import, deletion, supplier fetch, selector replay, email, paid upgrade or production publication occurred. Last Neon measurement remains about 407 MB, not reduced by these local tests. Next implement verified historical display archive/retention and real dependency provenance before fresh-feed/remote verification. Do not enable daily ingestion yet.

Reproduction: `node database/shadow/harness/verify-compact-snapshot-offline.mjs selection.json.gz outputs.json /tmp/receipt.json`. Both inputs must match the saved accepted artifacts; no new feed is needed.

## Display archive and bounded retention plan — 3 November 2026

`harness/display-archive.mjs` creates a self-contained compressed packet containing full canonical selection state (no parent-run dependency), exact compact display and exact appearance IDs. Immutable content-addressed keys include run ID and byte checksum. Recovery verifies checksum/size, run/date, selection state, display hash and ID membership. `archiveCompactDisplay` exports under a read-only snapshot, verifies immutable store readback, then rechecks current state under the existing supplier lock before recording an archive pointer. It removes nothing. Store adapters must implement immutable put-if-absent and read; no provider/credentials were configured.

`planDisplayRetention` is DRY RUN ONLY: minimum seven calendar days of display stay hot, the latest snapshot is retained even after a gap, and a 64 MiB hot-display budget is reported. Older data without a matching verified archive receipt remains blocked. Before any future cleanup, re-fetch and revalidate archive bytes, preserve identity links/decision ancestors, and recheck the source transactionally. No clearing function or schedule is installed; receipt flags alone are not authorization to delete. Days with multiple snapshots or larger payloads can exceed budget, in which case report/stop rather than shorten retention. Display policy does not shorten the owner's 90-day full-advert-after-inactivity policy; raw adverts are NOT included in this display archive and require their own retained source guarantee.

All 23 harness checks passed, including three new archive/retention checks. Additional local PostgreSQL archival-pointer checks passed without deleting hot data. The accepted full fixture restored all 350,368 decisions, 43,796 source identities and 239 regional outputs exactly from an 8,147,866-byte archive via a local immutable-file adapter. The test uses a synthetic run ID/dependency context, explicitly NOT a claim of real historical provenance. Seven full hot displays at the measured fixture size total 43,299,683 encoded bytes, excluding PostgreSQL overhead. Evidence: `display-archive-verification-2026-11-03.json`. Reproduction extends the existing offline verifier with a final local archive-directory argument.

No remote execution, Neon write, deletion, import, publication, email, upgrade or permission change occurred. Current production and all pinned legacy evidence remain unchanged. No running test remains. Next verify the existing persistent archive provider's immutable write/read permissions and retention guarantees, implement its adapter, and capture real dependency provenance. Do not enable cleanup/daily ingestion or certify 90-day Free suitability until that and current turnover/live allocation checks pass.

## Archive access audit checkpoint — 3 November 2026

Repository confirms private bucket `ontap-jobg8-archive-179402568934-eu-west-2-an` in eu-west-2, existing GitHub OIDC role `OntapJobG8ArchiveGitHubRole`, raw prefix `jobg8/raw`, and production `--skip-prune` (bucket lifecycle owns expiry). Live lifecycle, bucket policy, new-prefix immutable writes and retention guarantees remain UNVERIFIED. This session has no AWS credential environment or connected ordinary S3/IAM administration capability; plugin search found an analytics integration, not the required bucket-control capability. No live AWS probe or policy change was made. Do not rerun the previously denied feature-branch role assumption or change trust merely to work around access.

`audit_archive_access.py` is a read-only metadata audit for an already authenticated AWS environment. It reads bucket lifecycle/location/versioning/encryption/lock, role trust, optional role permission simulation, and one byte from each specified existing raw ZIP to check GetObject without logging payload. It never uploads/deletes, fetches credentials or changes permissions. Denials are reported as unverified; simulation is NOT proof of effective immutable writes. Two mocked API-boundary checks pass. `archive-access-checkpoint-2026-11-03.json` preserves the verified facts and blocker.

Next run this saved audit in AWS CloudShell and review the resulting metadata. Object-age expiration must not be confused with 90 days after advert inactivity. Account/role ARNs in output are identifiers, not secrets; no credential values are requested. No adapter activation, cleanup, import, publishing or paid upgrade is enabled.

## Owner AWS audit and prepared lifecycle separation — 3 November 2026

Owner-provided CloudShell output confirms eu-west-2; bucket-wide enabled Expiration Days=93; versioning not enabled; Object Lock absent; AES256 encryption. Both 2/3 November raw ZIPs are readable. GitHub OIDC trust grants only main (duplicated subject entries do not add another branch). New archive-prefix GetObject/PutObject simulation is allowed, but effective conditional writes remain untested.

Prepared `prepare_archive_lifecycle.py`: default read-only plan, explicit `--apply` changes ONLY the audited rule filter from global to `jobg8/raw/`. Raw-feed expiry stays 93 days. It verifies the exact audited configuration, refuses unrelated top-level/jobg8 content, backs up the previous config locally before applying, and reads back the changed rule. No IAM, objects, encryption, versioning or lock settings change. Three tests pass. AWS has NOT yet been changed; owner must run the saved script in CloudShell and return readback. The expiry of existing ontap-shadow content is removed by this proposal, so future archive storage must be monitored and later bounded; no indefinite-cost claim is made. No source/archive cleanup is enabled.

This is intentionally no automatic expiry for database archives until verified inactivity-based retention and reference tracking exist, rather than inventing a fixed object age that could delete still-required evidence. Raw JobG8 ZIPs remain on their existing 93-day policy; this alone does NOT meet the 90-days-after-inactivity full-advert guarantee. A retained raw-advert history path is still required. No production cutover, imports, emails or upgrade. Resume from `archive-policy-checkpoint-2026-11-03.json`.

## Lifecycle separation applied — 3 November 2026, 11:17 UTC

Owner CloudShell screenshot confirms `applied: true`, `readback_verified: true`; the enabled 93-day rule now filters `jobg8/raw/`. Database archive prefix `ontap-shadow/` is excluded from automatic expiration. Backup: `ontap-lifecycle-before-20261103T111731621152Z.json` in owner CloudShell. No objects deleted, IAM trust changed or production/Neon import performed. Do not rerun the apply script: its old-configuration guard should now refuse. Actual immutable provider write/read, production runtime integration and raw advert 90-days-after-inactivity guarantee remain pending. Archive accumulation requires monitoring and later reference-aware cleanup. Resume from updated `archive-policy-checkpoint-2026-11-03.json`.


## Persistent archive transport probe — prepared 3 November 2026

`verify_archive_transport.py` is an explicitly invoked CloudShell probe. It embeds a
922-byte synthetic archive made and restored by the existing JavaScript display
archive codec. The exact key is allowlisted. It checks account, region and the
already-applied raw-only lifecycle before any write, sends AES256 and SHA-256 with
`IfNoneMatch=*`, requires HTTP 412 on repeat, and reads back exact bytes and the
complete decoded packet. Same-script reruns reuse the existing object after exact
validation. Unexpected API errors, checksum mismatch, expiring content or changed
lifecycle fail closed. No unconditional put/delete, IAM/lifecycle mutation,
Neon connection, feed fetch, publication or email exists in this executable.

Four mocked API-boundary tests pass. Saved fixture was generated and semantically
restored locally with `makeDisplayArchive` / `restoreDisplayArchive`; Python verifies
the complete packet hash during recovery. The probe reports explicitly that this
is synthetic transport evidence, not real selectors/provenance, full 8.15 MB S3
recovery, Object Lock, GitHub-role access or 90-day raw retention. There is no
production adapter integration yet. Conditional client writes prevent this client
overwriting an existing object; privileged unconditional writes remain possible.

Save the executable and checkpoint in GitHub before providing the pinned CloudShell
command. The owner runs it in the existing authenticated CloudShell; a successful
receipt is saved as `ontap-archive-transport-result.json` before it is printed.
Only after owner output is received may remote transport be recorded as passed.
Keep the object; no cleanup is authorized. Recover from
`archive-transport-checkpoint-2026-11-03.json`.


## Full archive S3 recovery — prepared 3 November 2026

`verify_full_archive.py` reuses the conditional S3 transport entry point with an
explicit 8,147,866-byte saved archive. Its immutable key/byte count/SHA-256 are
pinned to `display-archive-verification-2026-11-03.json`. Full archive regeneration
from the two saved artifacts matched the previous checksum exactly; the existing
JavaScript restorer validated every decision/appearance/output locally. CloudShell
then verifies identical full compressed bytes and bounded gzip recovery after
actual S3 upload and conditional-repeat rejection. It does not run selectors or
query Neon. Local full-size mocked provider roundtrip and corrupt-input rejection
passed; the original four transport checks remain green.

The archive is supplied as `ontap-full-display-2026-11-02.json.gz`. Upload that file
to owner CloudShell, download this executable, the shared transport module and
the pinned display receipt from the same committed revision, then run
`python3 verify_full_archive.py`. A successful result is saved to
`ontap-full-archive-result.json` before printing. No automatic cleanup or deletion
is installed. Record actual owner output before claiming full S3 recovery.

This remains the real saved selector/display fixture packaged with synthetic
dependency metadata/run ID, not certified fresh-run provenance. It does not
contain full raw adverts or establish inactive-advert retention, main-only GitHub
role write access, Object Lock, current turnover or 90-day Neon Free viability.
Current Neon remains at the last measured 407,347,200 bytes. Production remains
file-based. Resume from `full-archive-checkpoint-2026-11-03.json`.


## Dependency provenance checkpoint — prepared 3 November 2026

Full S3 recovery is now owner-verified (see `full-archive-checkpoint-2026-11-03.json`);
do not repeat that upload. Its synthetic run/dependency metadata remain labelled.

`dependency_provenance.py` reconstructs an exact Git inventory at the historical
selector revision: 946 candidate files, SHA-256 list saved in
`dependency-source-2026-11-02.json`. This is explicitly NOT an execution context: it
cannot recover the historical sparse checkout, untracked files, packages or env.
It must not retroactively certify the existing synthetic archive.

The existing `run_selector_parity.py` now captures the actual retained source set
before replay, including all copied pipeline inputs outside the same existing
input/output/report/cache exclusions and adapter/observer/capture code. It refuses
uncommitted dependency bytes, verifies both scratch copies, and checks source
immutability afterwards. Allowlisted `ONTAP_FEED_DATE`, timezone/locale/hash seed,
Python/pandas/openpyxl versions, workbook SHA/created time, raw archive SHA, output
scopes/hash and actual start/end times are recorded. No arbitrary environment or
credential values are logged. The source inventory is conservative: it includes
possibly unused files rather than claiming an exact dynamic dependency trace.

Start/final manifests are retained by the same isolated workflow alongside the
existing report/selection artifact. The report provides `compactContext`; when
a captured manifest is present, the existing history codec checks its hash and
recomputes group/runtime/scope bindings, rejecting a substituted context or a
historical reconstruction. Existing legacy/synthetic fixture readback remains
unchanged and is not runtime evidence. No selector execution is skipped.

No replay request has been changed or remote run launched. Capture has local
boundary/cross-language tests; actual emission during a complete replay remains
unexecuted. Do not run the two full selectors solely to backfill historical
metadata. Capture it on the next separately justified saved/current-feed replay.
The extra file manifest is retained in report metadata, so previous tiny synthetic
delta-size measurements do not include this provenance overhead; measure actual
compact allocation before declaring Free-plan viability.

Resume from `dependency-provenance-checkpoint-2026-11-03.json`. Next current
saved-feed turnover and measured compact database growth; no cleanup, daily
ingestion, paid upgrade or production cutover is authorized.


## Current saved-feed turnover — prepared 3 November 2026

`compare_saved_archives.py --s3` reads exactly `jobg8/raw/2026-11-02.zip` and
`jobg8/raw/2026-11-03.zip` from the already-audited owner account/bucket/region.
Only STS identity, bucket-location, HeadObject and conditional GetObject calls
exist. No S3 write/delete, supplier URL, database, selector, publisher or email
operation is present. Head ETag pins each download; size guards and exact pin/
quarantine counts validate the accepted 2 November input. Raw ZIP SHA-256 and
S3 metadata identify both snapshots. Caller permissions remain CloudShell-specific.

`fingerprint_archive` reuses the existing raw flattener, streams XML and retains
only IDs, raw hashes and compact byte counts. Conflicting IDs are quarantined
(up to the existing 15-ID source boundary), exact duplicates collapse. Existing
`compare_plans` computes actual raw additions/changes/absence. Returns require
earlier complete history and remain unknown; absence never expires a job.
Changed/new canonical payload bytes support the existing compact raw gate
formula. Selection/display growth is EXTRA and unknown; the old measured
407,347,200 bytes is a dated baseline, not a fresh Neon measurement. The legacy
append forecast remains separately labelled. No result authorizes an import or
proves 90-day Free viability. No full adverts are printed or written to receipts.

Fourteen local checks pass: five comparison/provider-boundary tests, three
existing archive-stage tests, six existing preflight tests. Streamed hashes
match the original raw loader on the same mixed duplicate/quarantine fixture.

Owner CloudShell needs the wrapper, `prepare_raw_stage.py`, the existing
`plan_shadow_jobg8_import.py` and saved `retention-measurement-2026-11-03.json`
from one committed revision in the same directory. Run
`python3 compare_saved_archives.py --s3`. It saves a detailed local
`ontap-current-turnover-result.json` before printing an aggregate summary.
Actual S3 execution/results remain pending until owner output is received.
No new supplier feed is fetched. No cleanup/import/cutover is authorized.
Resume from `current-turnover-checkpoint-2026-11-03.json`.


### Daily archive is not automatically the Neon test source

The first owner execution stopped at the ZIP pin guard: daily S3 2 November ZIP
is byte-different from the separately captured test ZIP. This proves neither
content corruption nor semantic difference; raw job hashes must decide.

Corrected comparison reads the existing full archive
`ontap-full-display-2026-11-02.json.gz` if present in CloudShell, verifying its
exact 8,147,866-byte length and pinned SHA-256 before recovering source hashes.
If absent locally, S3 mode READS the already-verified content-addressed archive
object, never uploads or replaces it. Its source raw-archive SHA/counts are checked.
Synthetic run/dependency metadata are not used to certify fresh runtime evidence.

The result separates daily S3 2-to-3 November turnover from pinned-Neon-to-current
turnover. A packaging-only difference is reported only if every clean ID/hash
matches; otherwise the snapshots remain distinct. Budget forecasts use exact
pinned source hashes, not the different daily archive. Unlinked comparisons may
report raw daily turnover but have no storage estimate. No baseline guard is
bypassed. Source-object metadata/checksums are checkpointed locally before the
comparison, retaining evidence if a later stage fails. The detailed result stays
in `ontap-current-turnover-result.json`; terminal output is a compact summary.

Sixteen checks pass (seven comparison/provider/baseline, three raw preparation,
six existing preflight). Actual corrected S3 comparison is pending owner output.


## Compact Neon allocation calibration — prepared 3 November 2026

Current raw turnover is now verified; see `current-turnover-checkpoint-2026-11-03.json`.
Do not repeat that comparison or the S3 archive upload. Fresh compact import is
not yet authorized by its raw-only storage forecast.

`harness/measure-compact-allocation.mjs` runs only in protected Preview on the
existing Neon test project. It SELECTs the saved raw hashes, complete production
decisions and selected display rows, reconstructs original fixture ordering,
and requires the original selector fixture checksum and 239-output hash.
No supplier/archive download or selector replay is needed. Code/register hashes
are reconstructed historical evidence; actual historical runtime remains unknown.

The existing codecs produce a real saved-snapshot baseline/display/appearance
payload plus a synthetic unchanged subsequent-day delta/display payload. A
seven-display scenario stores one baseline payload and six copies of that
synthetic delta/display payload; these are NOT seven actual feed dates.

`compact-allocation.mjs` holds the existing supplier advisory lock, checks
prewrite headroom (encoded bytes times three plus 64 MiB reserve), creates only
`ontap_shadow.compact_allocation_probe`, verifies each JSONB readback and measures
normal heap/TOAST/index/database allocation. All probe writes always ROLLBACK,
including on error. A pre-existing probe table is refused, never replaced.
Existing importer-owned row counts and probe-table absence are checked after
rollback. No existing row UPDATE/DELETE, feed import, cleanup or plan change
exists. Catalog/WAL allocation may grow despite rollback; before/during/after
measurements must be reported without a reclaimed-space claim.

Four local PGlite checks pass (readback/rollback, preflight stop before writes,
failed-readback rollback, pre-existing-table preservation). This calibrates
compact JSONB in a separate normal table, not a current-feed end-to-end import
or exact incremental allocation inside existing feed_runs. It does not prove
90-day Free viability, raw inactivity retention or fresh-run provenance.

Save source before one deliberate Preview execution. Upload only the harness
modules/package/lock and pinned receipt/inventory listed in the checkpoint;
rename `compact-allocation-vercel.json` to `vercel.json` in that isolated bundle.
Never change project-wide settings or use a production target. Static output
contains aggregate measurements only, under existing Preview protection.
Record deployment ID immediately and resume that exact deployment after an
interruption. Checkpoint: `compact-allocation-checkpoint-2026-11-03.json`.


## Compact allocation verified — 3 November 2026

Protected Preview `dpl_3okrcLVU6dVw9vSuotkUKe62Lzf4` reached READY from saved
source `aa568b41412ffbdd38f3a417d99e00312f063fdd` in 55 seconds. Original
350,368-decision fixture checksum and all 239 output arrays matched exactly
from existing Neon evidence before probing. The existing codecs verified
complete baseline/delta/display/appearance reconstruction and exact JSONB
readback. No selectors, raw imports or source/archive downloads ran.

Normal probe heap/TOAST/index allocation: first snapshot 11,329,536 bytes; seven
payloads 51,003,392 bytes. This includes selection/display/appearances, with six
copies of a synthetic unchanged-day payload, not seven actual feeds. Probe
rolled back, its table is absent and existing importer-owned row counts are
unchanged. Database before: 407,347,200; after: 407,363,584 bytes (16 KiB
bookkeeping allocation). Existing data was not compacted or deleted, and no
space reclamation is claimed. All 12 existing relation allocations are unchanged.

Illustrative forecast adds after-rollback database allocation, the independently
verified current raw step estimate 114,296,315 bytes, seven-payload calibration
51,003,392, and 64 MiB reserve: 639,772,155 < 838,860,800. This is NOT import
approval, seven days of changing adverts, exact feed_runs marginal allocation,
a fresh complete-feed test or 90-day Free-plan viability. Full source receipt/
checksums, actual captured runtime provenance, raw inactivity retention, and
fresh compact update/expiry/duplicate integration still need verification.

Protected aggregate receipt returned HTTP 200/noindex. Project remains Next.js,
Node 24, same project update timestamp/protection and production alias. No
function, public alias, email, plan or schedule changed; no build remains running.
Receipt: `compact-allocation-verification-2026-11-03.json`; recovery/state:
`compact-allocation-checkpoint-2026-11-03.json`. Do not repeat this completed probe.


## Fresh selector integration preparation — 4 November 2026

The exact saved 3 November S3 object metadata is pinned in
`fresh-integration-prep-checkpoint-2026-11-03.json`; no new supplier feed is
needed. The existing selector runner now has an explicit option that checks the
ZIP's SHA-256, byte length, source row count, clean count and quarantined ID,
sets the pinned feed date, and captures it in runtime provenance. Its original
2 November default remains unchanged.

The existing isolated branch workflow now supports
`fresh_selection_parity`. It downloads the saved ZIP through the
short-lived `ONTAP_SAVED_FEED_URL` Actions secret, then validates it against
the pinned checkpoint. The secret must be created from owner CloudShell's
existing S3 access and kept out of chat and source code. No new IAM role or
workflow was added. The request file remains unchanged; no fresh selector run
or Preview integration has started. The current daily JobG8 workflow was still
running when this checkpoint was prepared.

The wrapper `harness/compact-integration.mjs` remains prepared and its local
tests passed on 3 November. It requires real selector evidence and runtime
provenance before accessing Neon. Raw, selection and display stages commit
separately, so failures remain recoverable rather than globally atomic. Jobs
remain withheld and expiry remains disabled.

Next: finish the daily feed process; create the short-lived URL/secret; then
deliberately update `stage-request.json` to run fresh selector parity. Save the
complete evidence and outputs before preparing the guarded Preview runner and
combined headroom check. Do not repeat completed sizing, archive transport or
turnover checks. Production remains file-based; no cutover, cleanup, emails,
schedule or paid plan change is authorized.

Execution order and remaining expiry/90-day/runtime/publisher gates:
`NEXT_INTEGRATION_TEST.md`.

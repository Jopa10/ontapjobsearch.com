# Next compact integration checkpoint

Updated 5 November 2026 after the second full pinned-feed Preview integration.
Production remains file-based; PR 336 remains unmerged. The isolated Preview Neon
database contains the 5 November snapshot, with every job withheld. No production
publish, email, expiry or purge occurred.

**5 November source and selector:** S3 object `jobg8/raw/2026-11-05.zip`,
35,093,994 bytes, SHA-256
`866570e8e23c38863292dc3f1fedc1518a18d750012c4449b7a208e7c51d019d`.
The selector replay passed on workflow run 42023032553: 43,391 source rows,
43,387 clean records, 239 scopes, 4,946 selected unique jobs, zero unknowns.
Output SHA-256:
`b4f3950d3cc1f1ea1fdbaa100b8fdf47a39703a2fc83043b40022d677777a6a2`.

**5 November Preview integration:** run ID
`714c55e3-0e3c-56b2-9d9f-83ddb62d1b8f`, deployment
`dpl_6cmnV7csw5GdiatNVaWmHqSHBXNq`. Raw, compact selection and display phases,
readback, and complete replay passed. Database size grew from 485,834,752 to
518,569,984 bytes: net 32,735,232 bytes. Measured headroom above the protected
64 MiB reserve is 253,181,952 bytes. Final counts: 50,252 adverts and jobs,
6 feed runs, zero published jobs. Purge was explicitly disabled; 38,138 excluded
records were marked for review, zero were due, and zero were purged.

The temporary Preview artifact URL variables were cleared after the run, and
`harness/vercel.json` is restored to the read-only retention audit command.
Checkpoint with full IDs and metrics:
`fresh-integration-prep-checkpoint-2026-11-05.json`.

**Next gate:** when the saved 6 November feed is available, pin its exact archive
metadata and checksum, run selector validation, then do the read-only Neon
storage/count preflight. Only after those pass should a separate Preview
integration be prepared. Do not repeat the 5 November selector or integration.
Forecasts give no credit for future purges. The earliest useful three-day
retention check remains 7 November; do not artificially age rows.

## Starting evidence (do not repeat)

- `current-turnover-checkpoint-2026-11-03.json`: exact Neon baseline to saved
  3 November feed: 1,394 added, 952 changed, 760 absent, 42,084 unchanged;
  44,430 clean records from 44,432 supplied rows. Conflicting ID 1401786160
  remains quarantined. Daily 2 November S3 ZIP is NOT the Neon test ZIP.
- `compact-allocation-verification-2026-11-03.json`: actual database after
  rolled-back probe 407,363,584 bytes; one payload 11,329,536 bytes; synthetic
  seven-payload calibration 51,003,392 bytes. No storage reclaimed.
- `full-archive-checkpoint-2026-11-03.json`: S3 full saved-fixture transport
  passed. Do not repeat upload or lifecycle apply. Historical metadata remains
  reconstructed/synthetic rather than captured historical execution.

## Preparation now available

`harness/compact-integration.mjs` calls the EXISTING raw, compact selection and
compact display entry points. Before DB access it requires a captured dependency
manifest, exact raw/selector hashes and revision/date, complete scoped evidence,
output checksum/membership and matching Apply URLs. It reads back the full
selection/display/appearance state, replays all three stages and verifies counts
and the reserved allocation ceiling. Jobs remain withheld; expiry is disabled.
After exact selector readback, the integration records the first run where an
advert is excluded in every production family. Its full payload remains
available for three calendar days, then `raw_payload` alone is cleared; compact
decision history, stable identity, hashes and run/job links remain. Repeated
identical exclusions do not restart the clock; changed content does. The cleanup
is an explicit transaction with no schedule. Preview Neon has the additive `002_exclude_review_window.sql` migration applied and verified. The 4 November integration used it with jobs withheld and expiry disabled; no purge was attempted.

The three existing stages commit independently. The optional `onCheckpoint`
callback receives only phase/run ID/archive SHA/feed date after each stage.
Caller must persist these events durably. If a later phase fails, inspect the
actual saved diagnostics and rerun the same pinned input; do not start another
feed. A complete import is not globally rolled back by this wrapper.

Five focused local PostgreSQL checks cover:

1. Complete input/output comparisons across initial/update/gap/return
   behavior (three synthetic feed dates), stable public/job IDs, exact replay,
   historical display readback and no per-advert daily decision/appearance rows.
2. Mismatched dependency context and raw hashes rejected before DB access.
3. Display failure after committed raw/selection resumes without duplicate jobs.
4. Fully excluded payload remains through day three and is purged after it,
   while its compact decisions and stable identity remain.
5. The read-only Neon baseline query separates fully excluded payloads from
   other or incomplete selector evidence.

These are synthetic local fixtures, not production selector/provenance evidence.
Absence does not imply expiry: the missing advert's prior last-seen/availability
are preserved. Actual expiry policy and 90-day raw retention remain UNPROVEN.
The three-day fully-excluded window is tested only with a synthetic local date;
the pinned 3 November feed is not yet old enough to cause a purge on a current
Neon run. The fresh integration must report current payload rows/bytes and
eligible EXCLUDE payload rows/bytes before and after the run; it must not advance
the review date artificially to force a purge in Neon.

## Historical execution notes (4 November; superseded by the current checkpoint)

1. Read AGENTS/canonical maps/README/checkpoints. Inspect GitHub/Vercel activity
   first. Keep deployment/run IDs and checkpoints durable before every execution.
2. Use the owner-pinned source metadata in
   `fresh-integration-prep-checkpoint-2026-11-03.json`; it supersedes the old
   missing-checksum note above. The exact source is
   `jobg8/raw/2026-11-03.zip`, 35,800,056 bytes, SHA-256
   `e6dcb08ea537bcb34dffd2ad9da089d443b5f0b1f875018c53aac0357fecc892`.
   Its S3 ETag is multipart metadata, not SHA-256. Do not mix it with the
   separate original Neon fixture or fetch another supplier feed.
3. `run_selector_parity.py` now accepts the explicit
   `--source-request database/shadow/fresh-integration-prep-checkpoint-2026-11-03.json`
   option. The historical no-option command remains pinned to the original
   2 November fixture. Fresh mode verifies the exact checkpoint path, source
   key/bucket/region, byte count, SHA-256, row counts and quarantined ID before
   running; it sets and captures the pinned `ONTAP_FEED_DATE`.
4. The existing isolated workflow now supports `fresh_selection_parity` using
   the same request file and runner. It downloads the exact S3 object through the
   short-lived `ONTAP_SAVED_FEED_URL` Actions secret, then verifies all pinned
   metadata locally. The owner must create that URL from the existing CloudShell
   S3 access and set it as the secret without pasting it into chat. This uses no
   new AWS role, IAM trust or workflow. The URL must still be valid when the run
   starts.
5. After the live JobG8 process is clear and the short-lived secret is ready,
   update `stage-request.json` to `fresh_selection_parity` and trigger its
   existing workflow. That file has not been changed yet. Do not fetch a new
   supplier feed or repeat the old replay.
6. Save the full selector report, complete decisions, source hashes, exact
   output arrays and dependency manifests immediately. Confirm actual source,
   register, geography, configuration, environment and runtime capture, workbook
   hash/time, exact output parity and zero unknowns. No selector run may be skipped.
7. Run the existing Preview-only read-only retention audit before changing the
   schema. Confirm its Neon project guard, whole-database size, advert payload
   counts/bytes, and fully-excluded payload counts/bytes from the latest complete
   selector run. Save the receipt. If the latest selector evidence is absent or
   the result is over budget, stop and report it.
8. After the baseline is saved and headroom passes, apply
   `002_exclude_review_window.sql` only to the verified `ontap-db-test` Preview
   database; it only adds the review-date column and index. Read-only verify the
   column, measure the database again, and save a checkpoint before import.
9. Perform all input validation and combined raw/selection/display headroom checks
   before any deliberate Preview import. The illustrative forecast is not import
   approval or a live allocation check. Keep the 800 MiB ceiling and 64 MiB
   reserve. No cleanup, plan upgrade or production connection.
10. Prepare the build-only Preview runner with the existing Neon project, TLS and
   Preview guards; call `verifyCompactIntegration` with those exact artifacts.
   The runner has not been installed or started. Save its source commit and run
   ID before execution. Inspect activity before retries and preserve the original
   pinned legacy evidence.
11. Compare IDs, hashes, outputs and actual allocation after raw/selection/display;
   verify full replay is idempotent. Persist failure-phase diagnostics. Continue
   with existing publisher/city rendering checks using the same snapshot only
   after raw/scoped display integration passes. Raw/family parity does not itself
   prove current production composition, alerts, website or cross-feed dedupe.

## Remaining separate gates

- Verified supplier expiry/disappearance policy, failed-feed isolation and return
  handling before any availability mutation. Local absence tests are not expiry
  implementation or authorization.
- Full adverts for 90 days AFTER inactivity, resetting on return, for records
  outside the fully-excluded three-day exception. Current raw ZIP age=93 days
  and display archive WITHOUT raw adverts do not meet this alone.
- Effective permissions for the eventual runtime; CloudShell root proof is not
  main-only GitHub-role write proof. No IAM trust expansion to bypass this.
- Sustained storage/turnover and retained-history bounds, real publisher/city
  parity, rollback rehearsal, then separately agreed production cutover.

No request file, schedule, sender or production setting changed for this prep.

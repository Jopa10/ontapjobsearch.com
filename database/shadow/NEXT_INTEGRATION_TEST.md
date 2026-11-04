# Next compact integration checkpoint

Prepared 3 November 2026 as the local baseline; execution sequence updated 4 November.
Production remains file-based; draft PR 336 remains unmerged. Fresh-source replay
and Neon import remain gated by the steps below.

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
is an explicit transaction with no schedule. Existing Neon needs the additive
`002_exclude_review_window.sql` migration before this code can run; applying it
and running the fresh-feed test are separate remote actions and are not included
in local verification.

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

## Tomorrow: execution order and unresolved inputs

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

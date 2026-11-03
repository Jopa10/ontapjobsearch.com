# Next compact integration checkpoint

Prepared 3 November 2026. LOCAL PREPARATION ONLY. No full feed replay, remote
build or Neon import is authorized for today by this preparation request.
Production remains file-based; draft PR 336 remains unmerged.

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

The three existing stages commit independently. The optional `onCheckpoint`
callback receives only phase/run ID/archive SHA/feed date after each stage.
Caller must persist these events durably. If a later phase fails, inspect the
actual saved diagnostics and rerun the same pinned input; do not start another
feed. A complete import is not globally rolled back by this wrapper.

Three focused local PostgreSQL checks cover:

1. Complete input/output comparisons across initial/update/gap/return
   behavior (three synthetic feed dates), stable public/job IDs, exact replay,
   historical display readback and no per-advert daily decision/appearance rows.
2. Mismatched dependency context and raw hashes rejected before DB access.
3. Display failure after committed raw/selection resumes without duplicate jobs.

These are synthetic local fixtures, not production selector/provenance evidence.
Absence does not imply expiry: the missing advert's prior last-seen/availability
are preserved. Actual expiry policy and 90-day raw retention remain UNPROVEN.

## Tomorrow: execution order and unresolved inputs

1. Read AGENTS/canonical maps/README/checkpoints. Inspect GitHub/Vercel activity
   first. Keep deployment/run IDs and checkpoints durable before every execution.
2. Recover the FULL existing CloudShell `ontap-current-turnover-result.json`
   (not only the pasted terminal summary). It contains current ZIP SHA-256 and
   S3 ETag/metadata required to pin the exact source. This full receipt has not
   yet been copied into GitHub. Do not infer its missing checksum.
3. Prefer that complete saved 3 November archive: it is fresh relative to Neon,
   reproducible and unaffected by tomorrow's publication. If selecting another
   date, establish a NEW exact receipt/count/turnover identity first. Never silently
   substitute tomorrow's supplier feed or mix dates/archives.
4. The existing `run_selector_parity.py` is still hard-pinned to the original
   2 November ZIP/43,796 records. It is NOT yet a general fresh-source runner.
   Adapt its existing entry point to an explicit validated source request before
   launching the complete fresh replay; preserve its default historical pin.
   Do not introduce another workflow or rerun old selectors just for sizing.
5. Pin code plus raw archive/date/quarantine/counts. Run unchanged actual family
   selectors through the adapted existing isolated path with dependency capture.
   Capture the actual materialized source/register/geography/config/env/runtime,
   workbook hash/time, full exact file parity and zero unknowns. Save both output
   and decision artifacts immediately. No selector execution may be skipped.
6. Do all input validation and combined raw/selection/display headroom checks
   before any deliberate Preview import. Today's 640 MB illustrative scenario
   is not admission approval or a live allocation check. Keep the 800 MiB ceiling
   and 64 MiB reserve. No cleanup, plan upgrade or production connection.
7. A separately prepared build-only Preview runner must enforce existing Neon
   project/TLS/Preview guards and call `verifyCompactIntegration` with those exact
   artifacts. That runner/remote bundle is NOT installed or started today.
   Save its source commit and execution ID before continuing. Inspect exact
   activity before retries. Preserve original pinned legacy evidence.
8. Compare IDs, hashes, outputs and actual allocation after raw/selection/display;
   verify full replay is idempotent. Persist failure-phase diagnostics. Continue
   with existing publisher/city rendering checks using the same snapshot only
   after raw/scoped display integration passes. Raw/family parity does not itself
   prove current production composition, alerts, website or cross-feed dedupe.

## Remaining separate gates

- Verified supplier expiry/disappearance policy, failed-feed isolation and return
  handling before any availability mutation. Local absence tests are not expiry
  implementation or authorization.
- Full adverts for 90 days AFTER inactivity, resetting on return. Current raw
  ZIP age=93 days and display archive WITHOUT raw adverts do not meet this alone.
- Effective permissions for the eventual runtime; CloudShell root proof is not
  main-only GitHub-role write proof. No IAM trust expansion to bypass this.
- Sustained storage/turnover and retained-history bounds, real publisher/city
  parity, rollback rehearsal, then separately agreed production cutover.

No request file, schedule, sender or production setting changed for this prep.

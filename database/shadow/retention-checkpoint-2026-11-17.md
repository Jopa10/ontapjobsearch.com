# Ontap expiry and retention verification — 17 November 2026

Status: **Four Preview simulations and recoverable archive upload/download checks passed. No new saved-feed secret was needed.**

## Scope and evidence

- Workflow **44091016620**.
- Neon temporary-lifecycle job **134065799639**; evidence artifact **14331098017**.
- Fresh uploaded-archive recovery job **134066346797**; receipt artifact **14330084992**.
- Actual current Neon publication was read through `current-publication.mjs`: **5,372 SELECTED IDs / 256 scopes**, current feed **2026-11-17**.
- Payload copies from real source IDs **107939734, 108019280, 108026901** seeded clearly labelled synthetic fixtures. No individual real-job decisions were changed.
- All lifecycle mutations were restricted to PostgreSQL **pg_temp** tables and rolled back. Real current-publication fingerprint was identical before/after; temporary test tables were gone after rollback. **0 actual advert payloads purged.**
- No supplier refetch, production publication, PR merge or production expiry activation occurred.

## Test 1 — missing jobs do not leak from retained history

**PASS.** The fixture moved from two SELECTED jobs to one, with the missing advert's previous payload still stored. The shared latest-publication reader returned only the one current SELECTED job; REVIEW was not published. An incomplete later feed with no completion receipt was also ignored.

The reusable reader chooses the latest **completed daily refresh receipt**, then loads only that date's SELECTED records and scope arrays. It verifies that the selected IDs and scope memberships agree. This reader is now wired into the automatic daily verifier and latest Preview publisher. Previous 316-file website parity remains valid; no unchanged page build was repeated.

## Test 2 — ninety-day retention, return and reset

**PASS** using a simulated clock:
- The inactivity timer began on the first accepted day the fixture advert was absent.
- Full payload remained at day **89**.
- Day **90** cleanup without a verified recoverable archive was rejected, leaving the payload intact.
- A return retained the same identity and cleared inactivity.
- A later absence started a fresh timer; the old timer could not remove the returned advert's payload.
- Duplicate identities: **0**.

These are boundary simulations. The actual master-advert inactivity/90-day archive/purge path is still not enabled by this test.

## Test 3 — current EXCLUDE policy

**PASS.**
- Fixture stored **1 SELECTED + 1 REVIEW** full payload and **0 EXCLUDE** payloads.
- The EXCLUDE marker/identity was absent from stored fixture payloads.
- The actual daily selected/review table contained **0 EXCLUDE records**.
- **No three-day EXCLUDE storage is enabled for the current daily process.** The owner confirmed that excluded adverts should remain in supplier archives rather than be saved in Neon.
- Older three-day EXCLUDE tests concern legacy test paths only. Do not treat them as the current ingestion policy or enable new EXCLUDE storage.

## Test 4 — preserve identity/history and recover exactly what was clicked

**PASS.**
- A synthetic click linked to immutable version 1 of a copied advert.
- A later advert revision created a distinct version 2; the click remained linked to version 1.
- Both versions were compressed and SHA-256 checked on archive readback.
- Deliberately corrupted archive data blocked cleanup; both temporary full payloads remained intact.
- With valid archives, day-90 cleanup cleared **2 fixture payloads**, preserving **1 job identity**, the click and its version references.
- Attempted deletion of the referenced identity was blocked by PostgreSQL foreign keys.
- The click recovered the original full advert exactly, not the later revision.
- Both compressed versions were exported, uploaded as a GitHub evidence artifact, freshly downloaded in another job, decompressed and verified again: **2/2 exact archive versions**.

The archive roundtrip used fixture evidence files in GitHub Actions, not a newly enabled production S3 cleanup path. Real historical payload removal still requires the approved durable version-archive integration and its operational receipts.

## Changes on the isolated testing branch

- `harness/current-publication.mjs`: shared reader for the latest completed publication only.
- `harness/retention-fixture.mjs`: mutation-restricted temporary-table lifecycle verification implementation.
- `harness/verify-retention-neon.mjs`: four real-PostgreSQL fixture scenarios plus unchanged-current-publication check.
- `verify-retention-archive-roundtrip.py`: fresh artifact-download recovery/hash verification.
- `.github/workflows/test-neon-retention.yml`: Preview deployment and archive roundtrip test.
- Automatic daily verifier and latest Preview publisher now use the shared completed-publication reader.

## Remaining operational gates

1. Wednesday's actual next-day publication: current-day automatic discovery, added/changed/absent/returning IDs and latest-set publishing with retained previous-day data.
2. A storage-bounded recurring master/version model and the real inactivity/90-day durable archive-before-purge integration. Today's fixture proof must not be presented as enabled cleanup of the real master tables.
3. Cutover-specific production safeguards and deployment rollback preparation, followed by explicit production-switch approval.

Keep PR #336 draft/unmerged, the normal publishing schedule and SEO behavior unchanged. Do not repeat the passed selector, 316-file website, daily same-day refresh/idempotency or four retention simulations without a relevant change.

## Subsequent actual cleanup implementation

The actual master-table cleanup routine has now been built and tested at 89/90/91 days against marked records in the real Preview tables, with archives uploaded/downloaded before apply mode. It is connected to the automatic daily refresh in dry-run mode. Read `master-cleanup-checkpoint-2026-11-17.md` for exact receipts and remaining permanent-S3/master-ingestion gates. Do not repeat the older temporary-table simulations. No production change or real-advert purge occurred.

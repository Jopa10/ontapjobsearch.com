# Preview master cleanup routine

Implementation: `database/shadow/harness/master-cleanup.mjs`.
Metadata migration: `004_master_cleanup_versions.sql` (applied to the isolated Neon Preview database).
Verification: `.github/workflows/test-neon-master-cleanup.yml`.

## What the routine does

The actual cleanup code reads `ontap_shadow.supplier_adverts` and `jobs`. It considers full payloads only when the advert has been inactive for at least 90 days, availability is missing/expired, the master job is not published, and neither public/supplier ID is in the latest completed daily SELECTED set.

Before clearing any candidate payload it:
1. Locks the affected master rows and daily/master coordination locks.
2. Archives each exact content version through an immutable durable store.
3. Reads and verifies compressed byte size/SHA-256, advert/job IDs, content version and full payload hash.
4. Stores the verified archive pointer in `advert_payload_versions`.
5. Revalidates archive bytes immediately before clearing `supplier_adverts.raw_payload`.

All candidate archives must pass before the first hot payload is cleared. `runMasterCleanup` owns a transaction and rolls back on any error. No identity, advert, activity, recommendation or consent row is deleted. The supplier advert retains its ID, version hash, archive pointer and purge timestamp. An identical repeat has no remaining candidate payloads.

`activity_events.advert_content_hash` can link future clicks to an exact version; its FK protects the version metadata. Existing events without a recorded version remain unknown: do not guess or relink them to today's version.

## Daily connection

The automatic daily Preview refresh now calls:
```js
await runMasterCleanup(client, { asOfDate: snapshot.feedDate, mode: 'dry-run' });
```

This is a real master-table eligibility check after each successful refresh. Real payload removal remains blocked until the approved permanent archive store is connected. Current master inactivity data and the bounded recurring master/version ingestion model remain separate migration gates.

Apply entry point, once the durable store is configured:
```js
await runMasterCleanup(client, { mode: 'apply', store: approvedImmutableS3Store });
```

Both entry points enforce the isolated Preview environment/project. A production switch remains separately unauthorised.

## Archive adapter contract and remaining connection

For actual non-test adverts, the adapter must have `provider: 's3-immutable'`:
- `putIfAbsent(key, bytes)` must enforce immutable conditional creation, or verify already stored identical bytes. It returns durable delivery metadata such as bucket/key/object version; never credentials or signed URLs.
- `get(key)` must read the saved durable bytes for checksum and content verification.
- The archive prefix is `ontap-shadow/advert-versions/`. Its retention must preserve job versions for the approved inactive-history period, including older clicked versions; do not assume raw-feed calendar expiry is sufficient.
- AWS access, existing bucket lifecycle and read/write roundtrip must be verified before enabling real-data apply mode. The saved-feed presigned GET secret is not an archive-write credential.

The test backend `github-actions-test` accepts only records explicitly marked with the current test-run ID. It cannot clear unmarked real records. Its archive artifact is uploaded and freshly downloaded before the apply test begins. This backend is test evidence, not the permanent S3 connection.

## Proven tests

The exact cleanup implementation was run on marked records in the actual master tables (not the earlier pg_temp simulation). Ages 89/90/91, return protection, published/current SELECTED protection, missing/corrupt archive rollback, exact clicked-version recovery, preserved FKs and repeat idempotency all passed. Synthetic data changes were finally rolled back; the additive metadata schema remains available.

## Prepared permanent-store connection files

The S3 adapter implementation is `harness/s3-master-archive-store.mjs`; its four transport guard checks passed. `prepare_preview_archive_role.py` prepares a separate prefix-limited Preview role (plan-only unless `--apply` is given). `test-preview-permanent-archive.yml` is ready for live immutable write/read verification after owner-authenticated AWS access is configured. None of those live AWS changes has been executed. See `master-cleanup-checkpoint-2026-11-17.md` for receipts.

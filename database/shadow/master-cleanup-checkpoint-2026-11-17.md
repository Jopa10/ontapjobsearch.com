# Actual master-table cleanup — 17 November 2026

Status: **Actual cleanup routine built, tested against marked records in the real Preview master tables, and connected to the daily refresh in dry-run mode. Permanent S3 access remains unconnected; real-data apply mode is not enabled.**

## Code and schema

- `harness/master-cleanup.mjs`: actual transactional cleanup and exact-version recovery, using `ontap_shadow.supplier_adverts`, `jobs`, `activity_events` and `advert_payload_versions`.
- `004_master_cleanup_versions.sql`: additive version/archive metadata and nullable exact-version click reference; applied to the isolated Preview database. Existing identities/payloads/history were not removed.
- `harness/s3-master-archive-store.mjs`: prepared AWS SDK v3 adapter with conditional create-only writes, expected bucket owner, AES256, checksum/readback verification and strict advert-version prefix.
- `harness/verify-daily-refresh-neon.mjs`: calls the actual master cleanup planner after a successful current-day refresh, defaulting to dry-run.

## Actual master cleanup test — passed

Workflow **44097948401**:
- Archive preparation job **134089973322** passed.
- **3 exact version archives** were uploaded as durable artifact **14335051336**, then downloaded and verified in a separate job **before any apply-mode cleanup**.
- Apply-test job **134090515037** passed; evidence artifact **14335745161**.

Six clearly marked synthetic records were inserted in the actual master tables inside an enclosing transaction, using these IDs:
- `cleanup-44097948401-age89`
- `cleanup-44097948401-age90`
- `cleanup-44097948401-age91`
- `cleanup-44097948401-returned`
- `cleanup-44097948401-published`
- `cleanup-44097948401-current-selected`

As-of date **2026-11-17**, results:
- **89 days inactive: full payload retained.**
- **90 days inactive: archived, verified and full hot payload cleared.**
- **91 days inactive: archived, verified and full hot payload cleared.**
- Returned advert retained.
- Master-published advert protected.
- ID in the latest actual daily SELECTED set protected even if stale master fields claimed inactivity.
- Missing archive blocked the entire batch before clearing any payload.
- Corrupt archive blocked the entire batch before clearing any payload.
- **2 synthetic full payloads cleared; all 6 identities and 1 synthetic click event preserved.**
- Exact original clicked version recovered after a newer version existed and the current hot payload was cleared.
- Foreign keys blocked deletion of the referenced advert identity.
- Identical second cleanup cleared **0** payloads.
- At the end, the enclosing test transaction was rolled back, leaving **0 test adverts**. **0 real adverts were purged.** Current publication remained **5,372 SELECTED IDs / 256 scopes**, fingerprint unchanged.

This uses the actual cleanup implementation and master tables; it supersedes the earlier policy-only pg_temp simulations as the cleanup-code verification. The durable test backend is restricted to matching synthetic test markers and cannot clear unmarked real adverts.

## Daily integration — passed

Workflow **44098257351**, job **134091076222**, artifact **14335216179**:
- Automatic current-day refresh passed unchanged.
- **5,372 SELECTED + 189 REVIEW-only = 5,561 records**.
- Exact IDs, decisions, full payload hashes, source positions and all **256** scope orders passed.
- **0 inserts, 0 payload updates, 0 metadata updates, 0 duplicates**.
- Actual master cleanup planner ran after the refresh: **0 real eligible candidates, 0 payloads cleared**, mode **dry-run**.
- Database **681,426,944 → 681,426,944 bytes**.

The planner reads existing master inactivity state. The dated daily-copy path does not yet maintain the complete recurring master/version state for every current advert; that bounded master-ingestion/timer integration remains a separate operational gate. Do not present a zero-candidate plan as proof that all real inactivity timers are populated.

## S3 adapter guard checks — passed

Workflow **44099156353**, job **134094169417**, **4/4** checks passed:
1. Conditional write sends expected owner, encryption and checksum and requires a fresh readback.
2. Existing identical object is reused without overwrite.
3. Existing different/corrupt object blocks reuse without a second write.
4. Keys outside `ontap-shadow/advert-versions/` are rejected.

These are transport contract checks, not a live AWS write test. No live S3 role/policy or bucket lifecycle was changed by this work.

## Remaining permanent archive connection

The last verified AWS trust allowed main only; the isolated branch's earlier OIDC attempts were denied. A saved-feed presigned GET URL is not an archive write credential.

Concrete setup and verification are prepared:
- `prepare_preview_archive_role.py`: read-only plan by default; `--apply` creates a separate **OntapNeonPreviewArchiveRole**, trusting only this testing branch, with Get/GetVersion and conditional encrypted Put only under the advert-version archive prefix. It does not modify the production role, raw-feed prefix or bucket lifecycle.
- `.github/workflows/test-preview-permanent-archive.yml`: ready to verify live conditional write/duplicate rejection/readback once that role is available. No trigger request was created before access exists.
- `MASTER_CLEANUP.md`: runtime entry points and store connection details.

**Real-data apply stays blocked until the approved permanent S3 connection and its live read/write/lifecycle receipts are verified.** The actual routine, metadata and test evidence are ready; no fresh feed secret is required for this connection. Real production cleanup, publication and PR merge remain unauthorised.

## Next checks

- Wednesday's actual current-day rollover and ID changes, using the existing automatic workflow.
- Permanent archive access and live immutable roundtrip.
- Complete recurring master/version ingestion and inactivity updates with bounded storage.
- Then verify actual Preview apply mode on eligible real master data, with recoverable archive receipts and rollback safeguards, before any production cutover approval.

PR **#336** remains **open, draft and unmerged**.

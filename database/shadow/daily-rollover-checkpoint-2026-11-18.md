# Wednesday Neon daily rollover — 18 November 2026

Status: **Blocked before Neon write.** Automatic discovery found Wednesday's completed production publication, but the saved-feed URL still identifies Tuesday's ZIP and failed the date check. No database changes were made.

## Discovery and failed attempt

- Request mode: `today`; only `attempt` was incremented from 3 to 4.
- Workflow: **44275136700** (run number 6), failed at “Discover today's completed publication and restore matching saved feed”.
- Automatically discovered feed date: **2026-11-18**. No date, run ID, or artifact ID was supplied in the request.
- Production deploy receipt run: **44270557665**.
- Completed JobG8 output run: **44259504159**.
- Matching saved output artifacts: service-admin **14410666153**; support-worker **14410755977**.
- The existing `ONTAP_SAVED_FEED_URL` value identified the **2026-11-17** archive, so the workflow stopped with “Saved URL does not identify automatically discovered current feed”.
- No Wednesday feed ZIP was restored; saved selector output was not downloaded; selector was not rerun; Neon was not written; no repeat was run; no Tuesday/Wednesday advert comparison was possible.
- PR #336 remains draft and unmerged. No production action or cleanup apply occurred.

## Next step to resume

Renew the short-lived signed GET URL for S3 object `jobg8/raw/2026-11-18.zip`, replace the GitHub Actions repository secret `ONTAP_SAVED_FEED_URL`, then increment only the request attempt and rerun the same `today` workflow. Do not enter a date or production identifiers.

## Baseline and cleanup note

Tuesday's completed set was **5,372 SELECTED + 189 REVIEW-only = 5,561 records across 256 scopes**. Wednesday results and the Tuesday-to-Wednesday added/absent/returning/changed IDs are pending the successful rerun.

The latest prior cleanup dry-run found **0 eligible candidates / 0 payloads cleared**. The real master inactivity state is not yet fully maintained by bounded recurring master/version ingestion, so zero candidates does not prove that all real inactivity timers are populated. Cleanup remains dry-run only.


## Retry after archive URL renewal

- The owner renewed `ONTAP_SAVED_FEED_URL`; no credential was exposed in chat.
- Request mode remained `today`; only attempt changed from 4 to **5**.
- Workflow **44276835562** automatically rediscovered the 18 November publication, restored matching saved feed `jobg8/raw/2026-11-18.zip`, and verified archive SHA-256 `7c5a2943b7a12246dda635ab301fb263f1f07dec14a1889dcaf7929837070606`.
- Reused saved production artifacts **14410666153** (service admin) and **14410755977** (support worker). No supplier refetch and no selector rerun.
- Confirmed **256 scopes** and exact published JobG8 scope inputs/order before Neon deployment.
- Prepared **5,431 SELECTED**, **206 review-list IDs**, **18 overlaps**, **188 REVIEW-only**, **5,619 distinct rows** total; 40,302 raw feed nodes. Tuesday had 5,372 SELECTED and 189 REVIEW-only.
- The Preview build then failed closed at the existing storage admission check: **“Storage estimate exceeds protected Preview ceiling.”** This happened before the first insert/update, so Wednesday's payloads, receipts and scopes were **not written**. No capacity threshold or reserve was bypassed.
- Therefore exact Neon readback, Tuesday/Wednesday ID-level differences, changed payloads, repeat/idempotency and Wednesday cleanup dry-run remain untested. The 256-scope source comparison passed, but not the Neon comparison.

## Cleanup status

No Wednesday cleanup dry-run ran because the refresh failed before commit. The last successful daily dry-run (17 November) found **0 eligible candidates / 0 payloads cleared**. The known gap remains: bounded recurring master/version ingestion does not yet maintain complete real advert inactivity tracking; zero candidates is not proof that all timers are populated. Real cleanup remains disabled.

## Next safe step

Capture the exact Neon byte count and admission estimate on the rejection path, then review a storage-bounded way to retain Tuesday history while storing Wednesday's current payloads within the **800 MiB ceiling and 64 MiB reserve**. Do not retry by weakening the guard, deleting history or applying cleanup. PR #336 remains draft and unmerged.

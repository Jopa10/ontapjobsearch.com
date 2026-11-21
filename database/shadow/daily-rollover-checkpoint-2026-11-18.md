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


## Exact guarded admission diagnostic — attempt 6

- Added a log-only admission report immediately before the existing assertion; no threshold or write behavior changed.
- Workflow **44277554479** again found Wednesday's publication and archive, reused the saved outputs, and confirmed **256 scopes**.
- Database before: **681,426,944 bytes**.
- Protected maximum: **838,860,800 bytes** (800 MiB); required reserve: **67,108,864 bytes** (64 MiB).
- Available projected growth while preserving the reserve: **90,324,992 bytes**.
- Wednesday's conservative estimated growth: **129,547,100 bytes**; it exceeds the available amount by **39,222,108 bytes** (~37.4 MiB).
- Estimate components: **23,291,643 payload bytes**, **1,566,759 metadata bytes**, **5,619 new date-specific rows**; no changed payload rows and no metadata-only updates.
- The same guard rejected the update before the first write. Neon remains unchanged; no threshold or reserve was bypassed.

The exact refusal is explained by the current table design budgeting a full selected/review payload row for each advert on this new feed date. A storage-bounded design must retain Tuesday's historical identity/decision evidence while avoiding this projected full-payload growth. Do not retry the update until that design fits the existing ceiling and reserve without weakening the guard.

The optional log-only instrumentation is committed on `feat/neon-shadow-database`; PR #336 remains draft/unmerged. No production code, data, publishing, or cleanup-apply mode changed.


## Scheduled daily-check follow-up — 18 November

Reviewed the three 17 November daily/cleanup/failure-recovery checkpoints, this rollover evidence and PR #336 (draft/unmerged). Request remains `mode: today`, attempt **6**. No duplicate refresh was triggered: the confirmed capacity rejection remains unresolved.

Independent read-only audit workflow **44281384493**, job **134722663120**, passed:
- Database **681,426,944 bytes**, unchanged from the rejected daily admission.
- Daily selected/review table: **0 EXCLUDE rows / 0 EXCLUDE payload rows**.
- Legacy master audit found **3,716 confirmed all-family excluded payload candidates**, **0 hash mismatches**, using date-matched complete eight-family evidence. Candidate JSON bytes **15,014,362**; stored bytes **9,340,530**. This is an audit, not a purge receipt or evidence that disk capacity has been recovered.
- **39,691** master payloads had decision evidence for a different payload date; **16,764** had no selector evidence; **389** were not excluded in every family. These classifications must not be treated as confirmed exclusions.
- Legacy exclude-review markers numbered **37,631**, but overlapped **68 current selected/review rows** and **69 published rows**; markers alone cannot safely identify deletable payloads.
- Subsequent broader audit **44281949209**, job **134724655190**, failed with PostgreSQL `Query read timeout` at `audit-exclude-payloads.mjs:60`; no successful broader report or cleanup is established.

Wednesday Neon write/readback, rollover ID-level additions/changes/absences/returns, active Wednesday receipt, Wednesday idempotency and fresh `report.failureResidue` verification remain pending. Tuesday's successful zero-residue result is historical evidence only. Wednesday master-cleanup dry-run did not execute; the last successful plan remains **0 candidates / 0 cleared**, with incomplete recurring master/version and inactivity coverage.

Resume only after a storage-bounded implementation or independently verified capacity recovery fits the unchanged **800 MiB ceiling / 64 MiB reserve**. No further secret renewal is shown necessary by the successful Wednesday archive restoration; access may expire later. Permanent immutable archive access and live read/write/lifecycle receipts remain gates; real cleanup apply stays disabled. No supplier refetch, selector rerun, failure injection, 316-file website rerun, real purge, AWS change, production action or PR merge occurred in this follow-up.


## Completed Wednesday selected-only rollover — attempts 8 and 9

Status: **Passed in isolated Neon Preview.** Mode remained `today`; only the request attempt changed. Wednesday was discovered automatically, the matching saved feed and production artifacts were reused, and Python remained the selection authority. No supplier refetch, selector rerun, production publish or PR merge occurred.

- Attempt 8 / workflow [44314516472](https://github.com/Jopa10/ontapjobsearch.com/actions/runs/44314516472) found feed date **2026-11-18**, deployment receipt **44270557665**, and saved selector output **44259504159**. It reused service-admin artifact **14410666153** and support-worker artifact **14410755977**.
- Prepared **5,431 SELECTED** payloads from the saved feed. The selector evidence contained 206 review-list IDs: 18 overlapped SELECTED and 188 were REVIEW-only. Neon stored **0 REVIEW-only and 0 EXCLUDE payloads**.
- Before saving Wednesday, the guarded reset cleared **619,929 rows across 18 `ontap_shadow` tables**. All subscriber, preference, consent, email, recommendation and activity-event tables were empty. The schema and supplier lookup were preserved.
- Neon size: **681,713,664 bytes** before reset; **9,191,424 bytes** after reset and before insert; **27,426,816 bytes** after Wednesday's write. The existing **800 MiB ceiling / 64 MiB reserve** was unchanged.
- Readback matched all **5,431 IDs, SELECTED decisions, payload hashes and original feed-row positions**. The **256 scope lists** matched exact membership and order. The current-publication reader returned exactly the Wednesday selected set.
- Tuesday-to-Wednesday comparison: Tuesday **5,372 SELECTED**; Wednesday **5,431**; **564 added**, **505 absent** from Wednesday, **44 returning** IDs (a subset of added), and **53 changed payload hashes** among IDs selected on both days. Net selected count change: **+59**. The exact ID lists are in [daily-rollover-diff-2026-11-18.json](daily-rollover-diff-2026-11-18.json). Tuesday-only IDs are absent from Wednesday's current set.
- Attempt 9 / workflow [44315328708](https://github.com/Jopa10/ontapjobsearch.com/actions/runs/44315328708) repeated the same `today` update after the one-time reset was disabled. It passed with **0 inserts, 0 payload updates, 5,431 unchanged rows, 0 duplicate IDs**; full payload/hash, feed-position and 256-scope readback passed again. The database measured **27,443,200 bytes** after replay.
- Master cleanup dry-run: **0 candidates, 0 cleared**. This is expected after the reset removed prior master-advert and inactivity records; it does **not** prove 90-day inactivity tracking. Recurring master/version ingestion and complete inactivity coverage remain gaps. The 90-day policy remains under owner review; real cleanup stays disabled.
- No subscriber or click-history rows were lost; the pre-reset guard confirmed all six related tables had zero rows. PR #336 remains draft and unmerged.

The selected-only daily table now contains Wednesday's current payloads. Future daily snapshots still need storage monitoring under the same hard ceiling and reserve.

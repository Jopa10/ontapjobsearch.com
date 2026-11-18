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

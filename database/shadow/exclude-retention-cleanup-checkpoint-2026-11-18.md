# EXCLUDE payload cleanup checkpoint — 18 November 2026

Status: **Confirmed EXCLUDE raw payload cleanup completed and independently verified in isolated Neon Preview.** Production was not changed. PR #336 remains draft/unmerged.

## Plain-English result

- Neon no longer has any full raw payloads that the available selector evidence confirms were EXCLUDE-only.
- The current daily SELECTED/REVIEW table has **0 EXCLUDE rows**.
- The cleanup removed raw advert payloads but kept the permanent IDs and the decision/history records needed to explain the advert's treatment.
- Some old rows remain because they are published, appeared in saved SELECTED/REVIEW history, or lack enough matching selector evidence to call them excludes.

## Audit and cleanup evidence

- First optimized read-only audit: workflow **44292376469**, run 4. It found **41,257** hash-matching EXCLUDE payload candidates, **0 hash mismatches**, and **0** current daily EXCLUDE payload rows.
- The first cleanup attempt was cancelled after its repeated history scan proved too slow. It may have committed some small batches before cancellation; the follow-up cleanup safely reselected only rows whose raw payload was still present.
- Guarded Preview cleanup: workflow **44293810549**, run 2. The Neon operation completed and reported **39,507** payload fields cleared in that run, **0** hash mismatches, **0** remaining confirmed candidates, and **0** decision/identity rows deleted. The GitHub run was marked failed only because its report parser rejected trailing Vercel CLI output; the returned Preview report confirmed the database operation completed. The parser was then fixed.
- Independent read-only verification: workflow **44294357037**, run 5. It confirmed **0** confirmed EXCLUDE payload candidates and **0** daily EXCLUDE rows. **90** legacy-marker payloads remain, all protected by saved SELECTED/REVIEW history and/or published status (88 with saved SELECTED/REVIEW history; 69 published, with overlap).
- Final measured database size: **681,713,664 bytes**. This is below the 800 MiB limit and leaves the 64 MiB reserve. The reported size did not shrink immediately after setting JSON payloads to null; no manual vacuum or physical shrink was run.
- No production publication, S3 write, archive copy, real cleanup activation, or PR merge occurred.

## Records left untouched

The read-only audit found raw payloads without enough matching evidence to safely classify them as EXCLUDE-only: **3,666** had selector decisions for a different payload date, **9,720** had no selector evidence, and **389** had at least one non-EXCLUDE family decision. Published and any-date saved SELECTED/REVIEW records were also protected. Do not describe those unknown/date-mismatched rows as confirmed excludes.

## Current retention rule

Never store full EXCLUDE payloads in Neon, even temporarily. The old three-day EXCLUDE window is superseded. Keep permanent IDs, hashes, decisions/reasons, rule versions, feed and appearance history, and linked user history. Current daily payload writes contain SELECTED and REVIEW only.

The general 90-day inactivity policy remains under owner review, not an active cleanup timer. See the current retention section in `database/shadow/README.md`.

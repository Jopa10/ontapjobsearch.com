# Thursday Neon master refresh — 19 November 2026

Status: **Passed in isolated Neon Preview**. PR #336 remains open, draft and unmerged. Request mode stayed `today`; attempts 24 and 25 changed only the attempt number. No date, run ID, artifact ID or commit was supplied by the request.

## Source

- The resolver automatically identified the 19 November AM publication and passed its before-noon/single-publication guard.
- Production deployment receipt: **44497271752**.
- Completed JobG8 output run: **44480225892**.
- Matching saved output artifacts: service-admin **14511837094**, support-worker **14512046722**.
- Saved feed key: `jobg8/raw/2026-11-19.zip`; SHA-256: `cdc3258fe625c377ef3908fe7624940258e1107afe07908d59dc30907c74ddd0`.
- No supplier feed fetch or selector rerun occurred. The selector evidence yielded **5,586 SELECTED**, **227 review-list IDs** (19 overlaps, 208 REVIEW-only); Neon saved **0 REVIEW-only and 0 EXCLUDE payloads**.
- Attempt 23 had failed before any Neon write because the URL secret did not identify Thursday's dated ZIP. Attempt 24 succeeded after the URL was updated.

## Thursday data and Wednesday comparison

Attempt 24 / [workflow 44505695023](https://github.com/Jopa10/ontapjobsearch.com/actions/runs/44505695023):

- Exact readback passed for **5,586 selected IDs, full payloads, hashes, decisions and feed positions**.
- Stored **5,586 Thursday appearances**, **5,586 decisions**, **256 exact ordered scopes**, and **1 matching refresh receipt**.
- Master now holds **6,189 full payloads**: 5,586 selected Thursday and **603 retained adverts absent from Thursday**. These 603 remain in Neon but were not exposed by the current-publication reader. No master payload lacked appearance tracking.
- Against Wednesday's saved master baseline (**5,431 selected**): **758 added**, **603 absent**, **76 shared adverts with changed payload hashes**, net **+155**. The 76 changed payloads were updated in place and received brief changed-field notes; all notes passed the label-only/length checks. **4,752** shared payloads were unchanged.
- Current-publication reader returned exactly Thursday's selected set. The storage ceiling and reserve were unchanged: **838,860,800-byte maximum / 67,108,864-byte reserve**.
- Database size: **48,029,696 → 53,837,824 bytes**.
- Exact added, absent and changed ID arrays are in the workflow report/logs.

## Identical repeat

Attempt 25 / [workflow 44506190635](https://github.com/Jopa10/ontapjobsearch.com/actions/runs/44506190635):

- **0 inserts, 0 payload updates, 5,586 unchanged selected payloads, 0 duplicates**; master remained at **6,189 full payloads** and the reader still returned exactly Thursday's set.
- **0 legacy Thursday payload rows** were removed; **0** remain.
- Database size increased **3,235,840 bytes** during the identical repeat (**53,837,824 → 57,073,664**) despite no payload updates or duplicate rows. The repeat is payload-idempotent but not database-size-neutral; inspect unchanged metadata upserts before treating it as zero-write.
- Cleanup was dry-run only: **0 candidates / 0 cleared**. Full payload cleanup uses the 30-day rule. Appearance metadata currently has **no automatic expiry**. No 30-day expiry or return-after-absence reset was exercised.

## Remaining

- Test 30-day cleanup eligibility and reappearance resetting the full-payload retention period.
- Review the repeat's database-size increase and avoid unnecessary same-day metadata upserts if appropriate.
- The automatic test still needs a fresh date-matched saved-feed URL. A true post-publication event trigger and AWS OIDC access have not been tested.
- One-day GitHub report retention for excluded/review-only items was not tested. Click tracking remains out of scope.
- No production publish, selector change, real cleanup, paid upgrade, S3 publishing-blocker change, or PR merge occurred.

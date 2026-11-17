# Ontap automatic daily Neon refresh — 17 November 2026

Status: **Automatic current-day discovery, Neon refresh and identical real workflow repeat all passed. No manually pinned feed date or production run/commit IDs were supplied.**

## Owner's scope and decisions

- Use `today` / latest completed publication discovery rather than a manually pinned Tuesday date.
- After this passes, expiry/retention is the next work item. Do not change expiry or purge records as part of this refresh test.
- The owner dropped the optional before/after selector-rule replay: matching the revised production outputs is sufficient for this migration check. Do not restart that optional audit.
- The refreshed saved-feed access worked in source job of workflow **44080130595**. That optional selector workflow was subsequently cancelled. Its already verified archive artifact **14327160793** was reused; no supplier feed was refetched.

## Executable automatic workflow

- `.github/workflows/test-neon-daily-refresh.yml`
- Trigger request `database/shadow/daily-refresh-request.json` has only mode `today`, attempt and purpose. It has **no feed date, production commit, publication run ID or artifact IDs**.
- `database/shadow/resolve-daily-source.py` discovers the latest successful main-branch production deployment workflow, reads its verified live production commit artifact, then reads that commit's completed JobG8 cycle state and matching successful feed run/artifacts.
- It derives `jobg8/raw/<discovered date>.zip` and refuses a stale publication when its feed date differs from today's Europe/London date.
- Archive access is distinct from date discovery: a matching already verified cached archive is reused; otherwise the configured signed URL must identify the discovered date and remain valid. A future day may require renewed archive access, but does not require editing the date/run IDs in the workflow.
- No production workflow, selector rule or publishing schedule changed.

## First real automatic daily-refresh run — passed

Workflow **44082162809**, job **134035219967**, evidence artifact **14326224729**.

Automatically discovered:
- Feed date **2026-11-17**, not supplied by request.
- Verified production deployment workflow **44053774414**.
- Completed JobG8 feed workflow **44039319889**.
- Published production commit **dc31cdb5ca846cc29f712700a59f80d807cf4912**.
- Selector source revision **6e001e11000854fd211f984c7d4db9f8b40e51e1**.
- Exact source archive SHA-256 `8638a31e4baca46665fed119fc2ddb227e48959a5da3b055189ae41d6ed55486`.
- Matching production artifacts **14311541647** and **14311691542**, with their GitHub SHA-256 digests verified during download.

Neon result:
- **5,372 SELECTED** IDs.
- **206** review-list IDs, including **17** overlaps with SELECTED; **189 REVIEW-only**.
- **5,561** distinct saved records.
- Exact IDs, decisions, full payload/hash readback and original feed positions all matched.
- All **256** publication scopes matched exact JobG8 ordering.
- The same scopes matched the existing verified Neon-backed website snapshot, so the passed 316-file website build did not need repeating.
- **0 inserted records, 0 payload updates, 5,561 metadata-only updates** to record the automatically discovered final production publication provenance.
- The change detector immediately returned **0** records for an identical replay; duplicate count **0**.
- Latest active daily-refresh receipt date **2026-11-17**.
- EXCLUDE payloads written **0**; expiry changed **false**; production changed **false**.
- Database **680,837,120 → 681,254,912 bytes**; unchanged 800 MiB ceiling and 64 MiB reserve retained.
- Admission estimates use actual new/changed full payloads and metadata changes. Unchanged full payloads are not rewritten merely because the workflow runs again.

Three resolver tests passed: unchanged logic discovers Tuesday then Wednesday using simulated dates; yesterday's completed publication cannot be used as today's; a missing verified live production receipt stops discovery. These are fixture checks, not actual Wednesday feed evidence.

## Identical real workflow repeat

Workflow **44082575857**, job **134036640911**, evidence artifact **14328635017**, repeated the same `today` request with only the attempt incremented and **passed**.

- Automatically rediscovered the same current publication/feed and verified the same 5,372 SELECTED + 189 REVIEW-only records.
- **5,561 unchanged rows**; **0 inserts, 0 payload updates, 0 metadata updates, 0 duplicates**.
- All IDs/decisions, full payload hashes, feed positions and all 256 scope orders matched again; existing verified website scope inputs matched.
- Active receipt date remained **2026-11-17**.
- Database bytes **681,279,488 → 681,279,488**, exactly no growth during the repeat.
- No production or expiry change.

Step 1 is complete. The real next-day rollover test still requires Wednesday's actual completed publication; the resolver's simulated Wednesday fixture is not a substitute.

## What remains

1. Actual Wednesday and later publication-day rollover, added/updated/absent/returning adverts and capacity behavior. Follow-up automation for 18–20 November has been updated to use this same automatic workflow and increment only its attempt, with no manually set dates/run IDs.
2. Preview master-advert inactivity/expiry and archive-before-purge for the agreed **90 days after inactivity**. This remains distinct from the dated selected/review snapshot table. Older master imports still have expiry disabled. The three-day EXCLUDE fixture boundary and actual Preview transaction rollback have already passed.
3. Cutover-specific production safeguards and deployment rollback preparation before any production switch approval.

PR #336 stays draft/unmerged; existing production publishing and SEO requirements remain in force.

## Subsequent expiry/retention checkpoint

All four agreed Preview simulations and a separate durable artifact recovery roundtrip passed. Read `retention-checkpoint-2026-11-17.md` for exact scope and receipts. The current daily process saves **zero EXCLUDE payloads**; the old three-day EXCLUDE helper is a legacy test path, not current policy. The shared current-publication reader now uses the latest completed daily receipt. Real 90-day master-table cleanup remains disabled; these tests changed only temporary fixture records and preserved the actual current publication.

## Subsequent actual cleanup implementation

The actual master-table cleanup routine has now been built and tested at 89/90/91 days against marked records in the real Preview tables, with archives uploaded/downloaded before apply mode. It is connected to the automatic daily refresh in dry-run mode. Read `master-cleanup-checkpoint-2026-11-17.md` for exact receipts and remaining permanent-S3/master-ingestion gates. Do not repeat the older temporary-table simulations. No production change or real-advert purge occurred.

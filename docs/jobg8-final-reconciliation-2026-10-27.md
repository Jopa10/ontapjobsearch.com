# Expanded-feed final combined reconciliation

Test feed: 50,000 rows. Production unchanged; no feed switch or deployment.

## Inventory
Owner screenshot baseline: 4144 total / 3615 JobG8 / 529 external. Checked-out HEAD aa60be7f13aa3f323e3d9c998e2bd0d82e136a4e JSON-counter baseline is newer: 4196 total / 3662 JobG8 / 534 external. Do not present these as identical snapshots.

Final maintained app JSON counter: 5855 total / 5322 JobG8 / 533 external (323 NHS, 210 Teaching Vacancies). Against same-method HEAD baseline, JobG8 IDs: 3245 retained, 2077 added, 417 absent; net +1660. Different feed snapshots, not a controlled size-only uplift.

Website canonical generator: 5786 total / 5253 JobG8 / 533 external. Difference from JSON counter: 45 content-duplicate alias IDs and 24 configured-file rows not admitted by canonical route collection (static-page precedence). Earlier blanket attribution of 69 rows to duplicates was too broad.

Teaching Vacancies baseline-to-test loss of one job: School Administrator - SLT Support, St Thomas Becket Catholic School, Northampton. Manifest closing datetime 2026-10-27T12:00:00+00:00; expired during testing.

## Composition and reviews
All four existing external composition commands passed. NHS refresh HTTP 403 triggered approved-state fallback retaining 323 NHS jobs. Final page composition: 54 changed, 169 unchanged, zero skipped/failed. City derivation and active-page maintenance both exit 0.
Compact Service Admin CSV: baseline 2532 rows (2328 selected, 186 dropped, 18 possible); test 3316 rows (2967 selected, 135 dropped, 214 possible). These are compact source rows, not final unanswered owner-review counts; persistent-review finalization/owner projection still needs verification.

## Final build
Search-index generation and production Next build both exit 0 after final external composition and city maintenance; 6145 static pages generated. Same workspace-only TLS and localhost DATABASE_URL setup as earlier build. Largest final NFT dependency sum 253686693 bytes (253.7 decimal MB), jobs/all; browse-jobs 253686586; job detail 253636382. This is NOT actual Vercel function package size. Platform packaging must pass before live-switch recommendation.

## Remaining release checks
1. Actual Vercel packaging/preview on the expanded output; assess size margin and adjust tracing only if evidence requires it.
2. Confirm persistent review finalization and owner queue behavior at increased possible volume.
3. Smaller staged feed-size comparisons have not been performed; no full-chain timing claim because runtime interruptions prevented uninterrupted full measurement.

No production clearance yet. Successful local build proves local compilation/generation capacity, not platform package acceptance.

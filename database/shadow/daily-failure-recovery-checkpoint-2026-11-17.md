# Daily update interruption and recovery — 17 November 2026

Status: **PASS — two deliberate failures in the actual daily Preview workflow, followed by a normal successful retry.**

## Evidence

- Workflow **44102521633**, job **134106457433**.
- Artifact **14337116998** contains both expected-failure deployment logs, the failure-recovery report, normal retry deployment log/report, source discovery receipt and exact scope ID arrays.
- Expected failed Preview deployments:
  - After partial payload write: **dpl_84G9VQbWpmQWjkZPzofNXn6mo3TY**.
  - Immediately before commit: **dpl_Gd9AXP9mjTWAfthtJs8tjjES3MyS**.
- Successful normal retry Preview: **dpl_vYe3aTDW3fA9sGz5Z3sQGPdbWGhi**.
- No production publishing, selector-rule change, real payload cleanup or PR merge.

## Exact test and result

The test reused today's automatically resolved publication, matching archived feed and production artifacts. The supplier was not refetched.

The actual `verify-daily-refresh-neon.mjs` transaction was interrupted at:
1. After a partial payload write.
2. After its ordinary validation and just before COMMIT.

A clearly marked synthetic next-day record/scope was staged inside each transaction. In the pre-commit case, a synthetic next-day completion receipt was also staged. This intentionally made the writer capable of seeing the fictional new set while testing whether a separate reader could see it.

A second PostgreSQL connection, verified to use a different backend, read the shared `current-publication.mjs` publication API while the writer transaction was open.

At both points it saw:
- Current feed **2026-11-17**.
- **5,372 SELECTED IDs**.
- **5,561 total saved records**.
- **256 scopes** with the unchanged ordering.
- Exact publication digest `1bdb25802115d86a2e56c0dfced51de9be76ea7aa963e781667d823d0c74681a`.
- **0 visible probe rows / no partial new set**.

Both deliberate exceptions caused the real updater's transaction rollback and failed the corresponding Preview deployment as expected.

The next failed attempt's baseline and final normal retry both matched the original digest exactly. The normal retry:
- Passed source discovery, exact IDs/decisions, full payload hashes, feed positions and all scope orders.
- Retained **5,372 SELECTED + 189 REVIEW-only = 5,561 records**.
- Wrote **0 inserts, 0 payload updates, 0 metadata updates**.
- Found **0 duplicates, 0 leftover probe rows, 0 uncommitted future completion receipts**.
- Database **681,426,944 → 681,426,944 bytes**, no growth on normal retry.
- Ran the existing master cleanup dry-run with **0 candidates / 0 cleared**.

The fictional next-day date **2026-11-18** was generated only for failure injection and never committed. This does **not** substitute for Wednesday's actual feed/publication rollover test.

## Code and one-off mode

- `harness/daily-failure-probe.mjs`: explicit Preview-only fault injection, independent reader checks and post-retry residue verification.
- `run-daily-failure-recovery.py`: expects both interrupted deployments to fail, verifies visibility/rollback and performs a normal retry with the fault configuration removed.
- Existing `test-neon-daily-refresh.yml` runs the same automatic source preparation and updater. It detects the explicit test trigger from the immutable triggering commit.
- `daily-failure-test-request.json` is the one-off trigger. **Do not increment it for normal daily tests.**
- Normal `daily-refresh-request.json` changes and workflow_dispatch do not enable fault injection. Generated fault files are removed before retry and in the runner's finally block.
- Checkout now uses the exact triggering SHA with its parent, preventing branch movement from changing the code used during a run.
- The initial mode-selection diagnostic run **44102358987** completed as an ordinary no-change refresh (artifact **14336443139**). It is not counted as failure-test evidence; explicit commit-based test selection was used for successful workflow **44102521633**.

## Next useful work

Wednesday's actual daily rollover, changing membership and payloads, and retained-history filtering. Do not repeat this passed failure test or other passed same-day simulations without a relevant change.

Other operational gates remain as recorded in `master-cleanup-checkpoint-2026-11-17.md`: permanent immutable S3 archive access, bounded recurring master/version ingestion and inactivity updates, and production cutover safeguards/rollback. Real-data cleanup remains off. PR #336 remains **open, draft and unmerged**.

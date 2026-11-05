# Ontap storage and retention assessment — 3 November 2026

Status: read-only measurement complete; retention changes PROPOSED, not implemented.
Receipt: `retention-measurement-2026-11-03.json`.
Audit Preview: `dpl_CpW9YzU2p8Y2foqopoVBKbLtowAV` READY.
Implementation: `d471eff9b0e939909062eea8f68a6ec6cbc66409`.
No new feed fetched/imported, database records changed, emails sent, paid upgrade or production switch.

## Measured storage

Decimal MB throughout this table. Allocated sizes include indexes/TOAST.

| Component | Bytes | MB |
| --- | ---: | ---: |
| Selection decisions, including display evidence and staged test history | 207,028,224 | 207.03 |
| Supplier adverts, including raw payload | 158,597,120 | 158.60 |
| Stable jobs | 24,428,544 | 24.43 |
| Daily advert appearances | 8,708,096 | 8.71 |
| Other shadow tables | 344,064 | 0.34 |
| Database overhead/outside shadow relations | 8,241,152 | 8.24 |
| Whole database | 407,347,200 | 407.35 |

The small increase from the earlier 407,306,240-byte receipt is 40,960 bytes; no application writes occurred in this audit. Provider/PostgreSQL maintenance can affect allocation. The audit transaction confirmed READ ONLY.

Exact decision counts: 350,368 production family decisions, 74,453 historical raw-stage unknowns and 20 original published-snapshot observations. Those 74,473 historical records occupy 29,788,312 logical row bytes before indexes/page overhead. They are test history, not extra jobs. Current production evidence is complete.

Selected displayRows occupy 19,589,278 bytes as JSON text, embedded in 5,821 selected scoped decisions; they are not a separate table. This logical text size is NOT an additional 19.59 MB on top of the 207.03 MB decision allocation. Raw payloads occupy 101,655,870 stored field bytes (164,477,431 as JSON text), already inside the supplier-advert allocation. Logical field sizes cannot establish precisely reclaimable disk space without rewriting/measuring, which this audit did not do. Estimated dead tuples are not certified reclaimable bytes.

## Growth finding

Only one full current raw-feed date exists in Neon: 2 November, 43,796 clean adverts. Current new/changed/missing/returning rates are UNKNOWN. Do not infer raw turnover from published first-seen jobs.

Even with zero new adverts, retaining one appearance per current advert per day at today's measured allocation gives:
407,347,200 + 89 × 8,708,096 = **1,182,367,744 bytes** at day 90, before any new decisions, changed data, or new adverts. This is an allocation-based scenario, not an exact future measurement. It exceeds both the 838,860,800-byte code ceiling and the currently advertised 1 GB Free storage allowance.

Appending another full set of eight decisions daily is substantially worse: simple proportional allocation suggests roughly 171 MB/day for production decisions at current mix, excluding future variation and extra appearance/raw growth. Therefore copying all current test records daily is rejected as the recurring-ingestion design.

Raw adverts plus stable job allocation currently average about 4,179 bytes per advert. Illustrative additional raw/job identity allocation for 90 days of net new IDs, assuming comparable payloads and no cleanup:
- 500/day: approximately 188 MB extra.
- 1,000/day: approximately 376 MB extra.
- 2,000/day: approximately 752 MB extra.
These exclude additional decision/history/index churn; they do not certify a retention window. The agreed 90 days starts AFTER inactivity, so active lifespan adds to residency.

Existing committed August archives were read locally, without fetching or importing. August 2–10 introduced 59–476 new-to-window IDs/day in feeds of 1,910–2,426 IDs (2.6–21.4% per day); August 11 was a volume expansion and is not comparable. August 12 introduced 674 new-to-window IDs in 9,999. These historical lower-volume observations demonstrate variability, not current 50k-feed turnover.
Published JobG8 first-seen history separately shows 61–478 new published IDs/day on recent non-expansion days, with 2,152 on 30 October's feed expansion; it is NOT an estimate of all received adverts.

## Proposed bounded hot-storage design

1. Preserve permanent jobs/public IDs and supplier identity links. Never recycle URLs or delete linked recommendation/activity/consent history as part of advert cleanup. Compact expired URL records must not serve an active Apply link. Permanent identity growth itself needs monitoring; finite capacity cannot be guaranteed forever.
2. Keep current raw advert state once per supplier identity. Update only changed fields; unchanged payloads must not be rewritten. Preserve full historical advert evidence for the owner's agreed 90 days after inactivity in a verified compressed archive, using the existing archive mechanism where practical. Store archive location, checksum, count and schema/version receipt; confirm readable archive before any later payload purge. Reappearance resets inactivity. Moving evidence out of PostgreSQL is a proposed policy/implementation change, not permission to purge now.
3. Keep latest effective family decisions and selected display state in the hot database. Record decision changes and rules/input revisions, with daily run totals/checksums referencing that state. Do not append eight identical decisions per advert every day. A reuse key must include every relevant dependency: payload, selector code, owner review/register/config/geography revisions and date-sensitive gates. Matching only a raw advert hash is insufficient.
4. Preserve exact daily appearance history through compressed per-run ID manifests outside the hot database plus compact in-database contiguous presence intervals; retain gaps and returns exactly. Keep a short configurable hot daily-row window (initial candidate seven days) only after archive/interval round-trip checks pass. This requires a migration; the current schema/importer does not yet implement intervals. Existing foreign keys prevent casual deletion of runs or adverts.
5. Keep compact run receipts/totals and archive pointers. Archive verbose historical test evidence only after retaining verification receipts and a recoverable archive. Do not infer that removing 29.79 MB logical rows shrinks the physical database by the same amount. Ordinary vacuum normally makes freed space reusable; it does not guarantee immediate file shrink. No VACUUM FULL/reindex/table rewrite is authorized.
6. Retain the unchanged 800 MiB code ceiling. Proposed admission budget: forecast post-import peak, indexes, temporary overlap and at least 64 MiB reserve below the ceiling; warn early. If budget is insufficient, stop the shadow import before writes and report it. Never silently shorten 90-day retention or upgrade. A hard cap is the backstop; actual turnover and tested compaction must justify the chosen hot window.
7. Subscriber consent, email history and engagement retention remain separate, undecided policies. The empty tables add almost no current storage.

This bounds bulky hot evidence while preserving required history elsewhere. It does NOT yet prove Free suitability: raw turnover, identity growth, archive cost/permissions, compute, egress, compaction and update bloat need validation. Reusing existing S3 archives is a candidate, not a claim that their current lifecycle/access policy already satisfies the 90-day guarantee.

## Next executable checkpoint

Before importing a fresh feed, extend the existing offline preflight to compare the pinned source with an ALREADY completed production snapshot/archive: exact ID overlap, new IDs, changed hashes, missing and returned IDs, plus projected raw/decision/appearance bytes. Pin source/checksum and save checkpoint before execution. Do not fetch another supplier feed just for sizing.

Then implement and validate decision-state reuse and archival/dry-run retention separately on the shadow branch, including exact historical readback, URL/reference preservation and rollback. Keep production file-based. Any fresh-feed database test must pass the measured admission budget first. No recurring ingestion/cutover until these gates pass.

## Provider reference

Checked 3 November 2026:
- https://neon.com/blog/neon-free-plan-1-gb-per-project — 2 October announcement: Free storage increased to 1 GB/project, existing projects included.
- https://github.com/neondatabase/website/blob/main/content/faqs/free-plan-limits-and-quotas.md — Free quotas, no billed overages; storage-increasing operations fail at limit.
These public documents are not account-specific billing inspection. The code ceiling is unchanged and is neither a billing cap nor the provider limit.

## Recovery

First attempt `dpl_BTvUGduq8qNYcXHruf6r237bfkcr` completed the READ ONLY audit but static publication failed due to inherited Next.js routes-manifest expectations; one large log line was truncated. Retry used only the saved audit script, existing harness package/lock and an explicit static vercel.json. It reached READY and report.json was retrieved/parsed successfully. No audit remains running.

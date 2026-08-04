# Ontap external-source register

This is the canonical record of external job websites assessed for Ontap.

It records the approximate number of potentially suitable roles found at the time of review, whether those roles appear additional to JobG8/approved sources, the access method, and the decision taken.

## Operating rule

Do not build a new ETL until a manual source check identifies at least **3–4 genuinely suitable, likely additional roles** for the intended region and category.

Counts are snapshots from the stated review date, not guaranteed daily volumes. Where deduplication has not yet been performed, the additional-role count must remain marked as preliminary.

## Source assessments

| Source | Region / slice | Review date | Potentially suitable before dedupe | Likely additional after dedupe | Access route | Status / decision | Evidence | Notes |
|---|---|---:|---:|---:|---|---|---|---|
| North East Jobs | North East — service administrator | 2026-07 pilot | Historical pilot completed; exact snapshot count not yet backfilled here | Implemented source | Public feed/pages | **Implemented** | Repository external-source pipeline | Approved vacancies are combined with JobG8; latest approved snapshot is retained on JobG8-only days. |
| VONNE | North East — service administrator | 2026-08 implementation | Historical review completed; exact snapshot count not yet backfilled here | Implemented source | Public listings/detail pages | **Implemented** | Repository VONNE POC and approved-source files | Review, dedupe and approval process completed before implementation. |
| BVSC Charity Jobs West Midlands | Birmingham & Solihull — service administrator | 2026-08-04 | 2 total review rows: 0 HC, 1 POSS, 1 hard pass | 1 plausible additional role | Public article listing/detail pages | **Park — insufficient volume** | Draft PR #164 | Technically working review-only POC. Do not schedule or publish unless later checks show materially higher volume. |
| WMJobs | Birmingham & Solihull — service administrator | 2026-08-04 | 2 plausible roles: 1 HC, 1 POSS; plus 4 diagnostic hard passes | 2 likely additional roles | Public RSS feed only | **Park — insufficient volume** | Draft PR #165 | Search/detail pages block automated access. RSS omits reliable closing dates. No bypass attempted. |
| jobs.ac.uk | Birmingham & Solihull — service administrator | 2026-08-04 preliminary screen | At least 4 plausible admin/support roles visible | **Not yet deduplicated** | Public Birmingham listings | **Investigate manually before ETL** | Preliminary chat review; repository assessment still required | Meets the initial visible-volume threshold, but must be manually classified and checked against JobG8 before any coding. |

## Required update after every source check

Each completed source assessment must add or update one row with:

1. the date and exact regional/category slice checked;
2. potentially suitable roles before deduplication;
3. likely additional roles after comparison with JobG8 and approved sources;
4. the public access route and any material limitations;
5. the decision: investigate, build POC, implemented, parked or rejected;
6. a repository PR/file reference where one exists.

## Backfill note

The exact historical NEJobs and VONNE review counts are not currently consolidated in this register. They should be backfilled from their retained review outputs when those files are next inspected; no count should be guessed.

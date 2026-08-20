# Ontap external-source register

This is the canonical record of external job websites assessed for Ontap.

It records the approximate number of potentially suitable roles found at the time of review, whether those roles appear additional to JobG8/approved sources, the access method, the legal/commercial position, the application route, and the decision taken.

## Operating rule

Do not build a new ETL until the source has first passed both mandatory intake gates:

1. **Legal/commercial permission** — Ontap's intended ingestion/republication/linking use must be permitted by terms, licence, API/feed terms or explicit permission. If unclear, HOLD before coding.
2. **Application route / two-click fit** — establish whether Ontap can send the candidate directly enough to the employer/application destination. A normal route of `Ontap → source/aggregator advert → employer/application portal` is a material negative and requires explicit approval before ETL.

Only after those gates pass should a manual source check test whether there are at least **3–4 genuinely suitable, likely additional roles** for the intended region and category.

Canonical intake order:

`legal/commercial permission → application route → volume/additionality → POC → field audit → review → approval → live`

Counts are snapshots from the stated review date, not guaranteed daily volumes. The **Possible additional roles** field is numeric so the CSV can be sorted correctly. Where a historical count is not known, that field remains blank rather than being guessed.

## Source assessments

| Source | Region / slice | Review date | Potentially suitable before dedupe | Possible additional roles | Possible-role explanation | Access route | Status / decision | Evidence | Notes |
|---|---|---:|---:|---:|---|---|---|---|---|
| North East Jobs | North East — service administrator | 2026-07 pilot | Historical pilot completed; exact snapshot count not yet backfilled here |  | Implemented source; historical additional-role count not yet backfilled. | Public feed/pages | **Implemented** | Repository external-source pipeline | Approved vacancies are combined with JobG8; latest approved snapshot is retained on JobG8-only days. |
| VONNE | North East — service administrator | 2026-08 implementation | Historical review completed; exact snapshot count not yet backfilled here |  | Implemented source; historical additional-role count not yet backfilled. | Public listings/detail pages | **Implemented** | Repository VONNE POC and approved-source files | Review, dedupe and approval process completed before implementation. |
| BVSC Charity Jobs West Midlands | Birmingham & Solihull — service administrator | 2026-08-04 | 2 total review rows: 0 HC, 1 POSS, 1 hard pass | 1 | One plausible additional role after review. | Public article listing/detail pages | **Park — insufficient volume** | Draft PR #164 | Technically working review-only POC. Do not schedule or publish unless later checks show materially higher volume. |
| WMJobs | Birmingham & Solihull — service administrator | 2026-08-04 | 2 plausible roles: 1 HC, 1 POSS; plus 4 diagnostic hard passes | 2 | Two likely additional roles after comparison. | Public RSS feed only | **Park — insufficient volume** | Draft PR #165 | Search/detail pages block automated access. RSS omits reliable closing dates. No bypass attempted. |
| jobs.ac.uk | Birmingham & Solihull — service administrator | 2026-08-04 preliminary screen | At least 4 plausible admin/support roles visible | 4 | Preliminary possible count only; not yet deduplicated against JobG8. | Public Birmingham listings | **Investigate manually before ETL** | Preliminary chat review; repository assessment still required | Meets the initial visible-volume threshold, but must pass the legal/commercial and application-route gates before any coding. |

## Required update after every source check

Each completed source assessment must add or update one row with:

1. the date and exact regional/category slice checked;
2. the legal/commercial permission basis, or an explicit HOLD/REJECT if unresolved;
3. the application route and whether it preserves the two-click/straight-to-employer principle;
4. potentially suitable roles before deduplication;
5. a numeric possible-additional-role count;
6. a separate explanation stating whether that count is confirmed, preliminary or historical;
7. the public access route and any material limitations;
8. the decision: investigate, build POC, implemented, parked or rejected;
9. a repository PR/file reference where one exists.

## Backfill note

The exact historical NEJobs and VONNE review counts are not currently consolidated in this register. They should be backfilled from their retained review outputs when those files are next inspected; no count should be guessed.

# Ontap external-source register

This is the canonical record of external job websites assessed for Ontap.

It records the approximate number of potentially suitable roles found at the time of review, whether those roles appear additional to JobG8/approved sources, the access method, and the decision taken.

## Operating rule

Do not build a new ETL until a manual source check identifies at least **3–4 genuinely suitable, likely additional roles** for the intended region and category.

Counts are snapshots from the stated review date, not guaranteed daily volumes. The **Possible additional roles** field is numeric so the CSV can be sorted correctly. Where a historical count is not known, that field remains blank rather than being guessed.

## Source assessments

| Source | Region / slice | Review date | Potentially suitable before dedupe | Possible additional roles | Possible-role explanation | Access route | Status / decision | Evidence | Notes |
|---|---|---:|---:|---:|---|---|---|---|---|
| North East Jobs | North East — service administrator | 2026-07 pilot | Historical pilot completed; exact snapshot count not yet backfilled here |  | Implemented source; historical additional-role count not yet backfilled. | Public feed/pages | **Implemented** | Repository external-source pipeline | Approved vacancies are combined with JobG8; latest approved snapshot is retained on JobG8-only days. |
| VONNE | North East — service administrator | 2026-08 implementation | Historical review completed; exact snapshot count not yet backfilled here |  | Implemented source; historical additional-role count not yet backfilled. | Public listings/detail pages | **Implemented** | Repository VONNE POC and approved-source files | Review, dedupe and approval process completed before implementation. |
| BVSC Charity Jobs West Midlands | Birmingham & Solihull — service administrator | 2026-08-04 | 2 total review rows: 0 HC, 1 POSS, 1 hard pass | 1 | One plausible additional role after review. | Public article listing/detail pages | **Park — insufficient volume** | Draft PR #164 | Technically working review-only POC. Do not schedule or publish unless later checks show materially higher volume. |
| WMJobs | Birmingham & Solihull — service administrator | 2026-08-04 | 2 plausible roles: 1 HC, 1 POSS; plus 4 diagnostic hard passes | 2 | Two likely additional roles after comparison. | Public RSS feed only | **Park — insufficient volume** | Draft PR #165 | Search/detail pages block automated access. RSS omits reliable closing dates. No bypass attempted. |
| jobs.ac.uk | Birmingham & Solihull — service administrator | 2026-08-04 preliminary screen | At least 4 plausible admin/support roles visible | 4 | Preliminary possible count only; not yet deduplicated against JobG8. | Public Birmingham listings | **Investigate manually before ETL** | Preliminary chat review; repository assessment still required | Meets the initial visible-volume threshold, but must be manually classified and checked against JobG8 before any coding. |
| Lever direct-employer network | London — existing Ontap office/service families | 2026-08-20 preliminary source sweep | At least 10 plausible London office/admin/customer/people/operations roles across multiple direct employers | 10 | Preliminary floor from current published Lever job boards; multiple checked employers did not appear in current Ontap repository outputs. Exact additional count must come from the review-only POC dedupe. | Public Lever Postings API / employer job boards | **Build review-only POC** | Lever Postings API documentation plus current Splend, MOO, Duffel, WisdomTree, Sofar Sounds, Mulberry, Palantir, Getty Images and e.l.f. Beauty job boards | Lever states published postings are public and may be scraped by third parties. One shared adapter can serve allowlisted direct employers. London is the proof region only; no schedule or publishing until field audit and review pass. |
| Workable global XML feed | London — existing Ontap office/service families | 2026-08-20 field audit | 11 classification-reviewable salary-bearing London roles before the expiry gate; one had a visible past closing date | 10 | Confirmed current POC result after Ontap classification, current-source dedupe and visible-closing-date expiry blocking: 7 SELECTED + 3 POSS remain likely additional. | Official Workable global XML feed + direct Workable application URLs | **Field audit passed — proceed to approved-output development** | `pipeline/reviews/external/london-workable-review.csv`; `pipeline/reviews/external/london-workable-summary.md`; Workable XML feed documentation | Audit saw 2,512 London feed rows, 338 salary-bearing rows, extracted 52 explicit closing dates and blocked 11 expired adverts. Core title/employer/location/salary/posted/closing/application fields were checked against live adverts. Global XML does not reliably distinguish hybrid from on-site when `remote=false`; this is recorded as a structured-feed limitation. Review-only: no schedule or publishing path yet. |

## Required update after every source check

Each completed source assessment must add or update one row with:

1. the date and exact regional/category slice checked;
2. potentially suitable roles before deduplication;
3. a numeric possible-additional-role count;
4. a separate explanation stating whether that count is confirmed, preliminary or historical;
5. the public access route and any material limitations;
6. the decision: investigate, build POC, implemented, parked or rejected;
7. a repository PR/file reference where one exists.

## Backfill note

The exact historical NEJobs and VONNE review counts are not currently consolidated in this register. They should be backfilled from their retained review outputs when those files are next inspected; no count should be guessed.

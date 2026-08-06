# Teaching Vacancies source-wide design decisions

This record captures decisions made while converting the completed West Yorkshire Teaching Vacancies implementation into a reusable Ontap external-source process. The operating instructions are in `TEACHING_VACANCIES_REGIONAL_PLAYBOOK.md`.

## 2026-08-06 — source scope

Teaching Vacancies is a national service for state-funded school and college vacancies in England. Ontap discovery must therefore be source-wide and region-neutral, but it must not claim coverage outside England that the source does not provide.

A discovered vacancy may route to any Ontap region represented by `pipeline/geo/geo_lookup.xlsx`. Yorkshire is not a discovery boundary. No search request may use an Ontap region, regional radius or Yorkshire-only place list.

## 2026-08-06 — discovery routes

The primary discovery route is the public national `Administration, HR, data and finance` listing:

`https://teaching-vacancies.service.gov.uk/administration-hr-data-finance-jobs`

This route exposes a reported total, ten results per page and explicit pagination. A complete sweep must fetch every advertised page and reconcile every page range against the reported total.

The existing occupational keywords are retained as supplemental national coverage routes without a location or radius. They are not treated as separate vacancies: overlapping results are deduplicated by canonical detail URL before detail fetching and by stable source ID after factual extraction.

## 2026-08-06 — completeness evidence

A live discovery run is blocked unless:

1. every configured route exposes a parseable result-range audit;
2. every advertised page is fetched;
3. page ranges and totals reconcile throughout the sweep;
4. two complete sweeps return the same vacancy URL and provenance set;
5. all discovered detail pages parse successfully.

The process does not use a production page cap. Source instability or incomplete detail fetching prevents a new manifest from replacing good evidence.

## 2026-08-06 — manifest boundary

The source-wide manifest is written before geography and occupational classification. It contains factual extracted fields, a bounded description excerpt, a factual fingerprint and all query/page provenance. It does not contain copied HTML or full source descriptions.

## 2026-08-06 — existing authorities

No replacement central registry is introduced.

- `pipeline/geo/geo_lookup.xlsx` remains the geographic source of truth.
- `pipeline/registers/region_category_slice_register.csv` remains the LIVE/CANDIDATE authority.

Unresolved geography remains visible and unpublished. A missing slice-register entry never implies LIVE.

## 2026-08-06 — review and migration

The factual manifest is routed before classification. Separate reviews are generated for every encountered Ontap region and compare vacancies only with current JobG8 rows from that region.

The completed West Yorkshire decisions are migrated only when stable source ID and all material review facts match. A selected legacy ID must also exist in the legacy approved snapshot. Blank legacy POSS decisions remain blank; changed records require a new review.

## 2026-08-06 — approval and composition

Approved snapshots are separate by region and may be created only for an explicitly LIVE admin/service slice. The approved CSV/Markdown set, actions, fingerprints, deadlines and evidence hashes must reconcile.

The generic composer is region-neutral and identifies regions from current output rows. It replaces only Teaching Vacancies rows, preserves JobG8 and other external sources, blocks empty or external-only overwrites, and supports a one-region filter for approval runs.

The established North East and West Yorkshire compositors remain first in the daily workflow. The generic composer runs afterwards and is dormant unless a verified regional snapshot exists. This preserves an immediate rollback path.

## 2026-08-06 — operator workflows

Two new controlled workflows implement the operating process:

- **Run Teaching Vacancies regional review** performs complete England-wide discovery, routing and separate regional reviews, and commits review evidence only.
- **Build approved Teaching Vacancies regional snapshot** approves one exact LIVE region after `PUBLISH` confirmation, writes its snapshot/evidence, and composes only that region.

The legacy West Yorkshire review and approval workflows remain available during the compatibility period.

## 2026-08-06 — validation outcome

GitHub Actions validate:

- complete source-wide discovery and live national-route parsing;
- 1,230 factual mappings from the real geographic workbook, including LocationFallback;
- routing, unresolved handling and LIVE/CANDIDATE controls;
- strict West Yorkshire decision migration and blank-POSS preservation;
- separate regional approval snapshots and tamper evidence;
- generic multi-region composition, one-region isolation and expiry/deduplication;
- exact West Yorkshire old/new output equivalence and rollback;
- coexistence with NEJobs and VONNE;
- compatibility with the existing verified publisher;
- workflow ordering, fallback retention and dormant behavior without snapshots;
- the existing live West Yorkshire review preview and live-site isolation; and
- the complete slice-register suite, including Yorkshire East as CANDIDATE.

The final CI run passed 80 tests. The live-route test initially exposed HTML markup around the result-range text. The parser was corrected to validate visible page text rather than brittle raw markup. CI also exposed and fixed a blank-action parser that could otherwise absorb the next review line. Both cases now have regression coverage.

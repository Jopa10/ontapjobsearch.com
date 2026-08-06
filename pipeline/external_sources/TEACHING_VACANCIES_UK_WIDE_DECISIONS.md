# Teaching Vacancies source-wide design decisions

This record captures decisions made while converting the completed West Yorkshire Teaching Vacancies implementation into a reusable Ontap external-source process. It is a development record for the eventual cradle-to-grave playbook.

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

## 2026-08-06 — publication safety

The source-wide discovery module is non-publishing. It does not alter reviews, approved snapshots, JobG8 outputs, external-source composition or application JSON. Regional review, approval migration and generic daily composition remain later controlled stages on the same draft branch.

## 2026-08-06 — validation outcome

GitHub Actions passed:

- 35 Teaching Vacancies discovery, review, approval, contract and retention tests;
- a live smoke test of the national administration route, including its reported total and stable detail links;
- the existing live West Yorkshire review-only preview and live-site isolation checks;
- the complete slice-register test suite, including the new East Yorkshire CANDIDATE row.

The live-route test initially exposed HTML markup around the result-range text. The parser was corrected to validate visible page text rather than brittle raw markup, and the full checks then passed.

# Ontap England geography market reconciliation — 22 August 2026

## Scope

Geography audit and diagnostic-governance change. This file does **not** activate production slices, remove or rename public routes, or change LIVE status.

Purpose: reconcile the former operational 33-market footprint against the fuller geography already present in `pipeline/geo/geo_lookup.xlsx`, establish a complete England assessment universe, and keep public search naming/grouping as a separate layer.

## Finding

The former 33-market England diagnostic footprint was a configured operational subset, not the full geography authority.

The August Module 2 profiler explicitly reads `geo/geo_lookup.xlsx`. Its 2026-08 run log records **1,198 geo areas loaded**, and its daily-count output preserves the underlying lookup regions while adding `North East` separately as a published aggregate made from three lookup regions.

Reconciling the operational 33 against those lookup-region labels produces **exactly 22 additional non-North-East England markets**.

The governed England assessment universe is therefore:

- **33 former operational markets** (including the deliberate `North East` roll-up)
- **22 omitted non-North-East markets**
- **55 assessable England markets in total**

This 55 is an Ontap diagnostic/routing geography, not an official government geography count and not an instruction to create 55 public pages.

## Existing 33 retained in the assessable set

1. Berkshire
2. Bristol & Bath
3. Buckinghamshire
4. Cambridgeshire
5. Cumbria - North
6. Cumbria - South
7. Devon
8. Dorset
9. Essex
10. Gloucestershire
11. Greater Manchester - Manchester & Salford
12. Greater Manchester - South
13. Hampshire
14. Hertfordshire
15. Kent
16. Lancashire - North
17. London
18. Norfolk
19. North East
20. Northamptonshire
21. Nottinghamshire
22. Oxfordshire
23. Somerset
24. Staffordshire
25. Surrey
26. Sussex
27. West Midlands - Birmingham & Solihull
28. West Midlands - Coventry & Warwickshire
29. Wiltshire
30. Yorkshire - East
31. Yorkshire - North
32. Yorkshire - South
33. Yorkshire - West

## Exact 22 recovered non-North-East markets

1. Bedfordshire
2. Cheshire - East
3. Cheshire - Warrington & Halton
4. Cheshire - West
5. Cornwall
6. Cumbria - West
7. Derbyshire
8. Greater Manchester - North
9. Greater Manchester - Wigan & Bolton
10. Herefordshire
11. Lancashire - Blackpool & Fylde
12. Lancashire - Central
13. Lancashire - East
14. Leicestershire
15. Lincolnshire
16. Merseyside - Liverpool
17. Merseyside - Wirral
18. Rutland
19. Shropshire
20. Suffolk
21. West Midlands - Black Country
22. Worcestershire

## North East special case

`North East` is intentionally not a peer lookup region. The underlying lookup retains:

- North East - Tyneside, Wearside & Northumberland
- North East - County Durham & Darlington/Hartlepool
- North East - Tees Valley

The 55-market assessment layer explicitly rolls all three into `North East`. This is separate from the missing-22 reconciliation.

## Current-feed validation — PASS

A same-repository PR validation run on **22 August 2026** downloaded the current JobG8 feed using the normal feed secret, converted and health-checked **10,000 jobs**, then ran the governed Service Admin, Support Worker and Customer Sales / Sales Advisor selectors against the new assessable geography.

Verified result:

- JobG8 feed date: **2026-08-22**
- assessable England markets: **55**
- governed families: **3**
- unique market/family rows: **165**
- former operational footprint: **33 markets**
- recovered markets outside that footprint: **exactly 22**
- JobG8 health guard: **PASS**
- selector/55×3 validation: **PASS**

Selected jobs in the 22 recovered markets on that feed totalled:

- **Service Admin: 194**
- **Support Worker: 17**
- **Customer Sales / Sales Advisor: 36**

These are diagnostic candidate counts, not new LIVE jobs and not automatic slice approvals.

| Recovered market | Service Admin | Support Worker | Customer Sales |
|---|---:|---:|---:|
| Bedfordshire | 4 | 1 | 3 |
| Cheshire - East | 13 | 1 | 2 |
| Cheshire - Warrington & Halton | 20 | 1 | 3 |
| Cheshire - West | 7 | 1 | 3 |
| Cornwall | 17 | 0 | 2 |
| Cumbria - West | 2 | 1 | 0 |
| Derbyshire | 14 | 0 | 4 |
| Greater Manchester - North | 4 | 0 | 1 |
| Greater Manchester - Wigan & Bolton | 9 | 0 | 2 |
| Herefordshire | 2 | 0 | 0 |
| Lancashire - Blackpool & Fylde | 0 | 0 | 0 |
| Lancashire - Central | 3 | 1 | 0 |
| Lancashire - East | 5 | 0 | 0 |
| Leicestershire | 27 | 0 | 2 |
| Lincolnshire | 11 | 1 | 2 |
| Merseyside - Liverpool | 10 | 2 | 2 |
| Merseyside - Wirral | 2 | 0 | 1 |
| Rutland | 0 | 0 | 0 |
| Shropshire | 10 | 2 | 2 |
| Suffolk | 17 | 2 | 3 |
| West Midlands - Black Country | 9 | 2 | 1 |
| Worcestershire | 8 | 2 | 3 |

## External benchmark

The Ontap market count is custom and must not be presented as an ONS/GOV.UK standard.

External geography is used as the **coverage backstop**:

- ONS describes England's exhaustive administrative structure through regions, counties, unitary authorities, metropolitan counties/districts and London boroughs: https://www.ons.gov.uk/methodology/geography/ukgeographies/administrativegeography/england
- GOV.UK confirms the six metropolitan county areas, including Greater Manchester, Merseyside, South Yorkshire, Tyne and Wear, West Midlands and West Yorkshire: https://www.gov.uk/guidance/local-government-structure-and-elections
- ONS Travel to Work Areas are labour-market areas based on commuting patterns and cover the whole UK, but at 228 UK-wide they are a validation layer rather than the intended Ontap public-market granularity: https://www.ons.gov.uk/methodology/geography/ukgeographies/othergeographies

The recovered set contains externally recognisable geographic holes that the old 33 could not plausibly claim to cover, including Merseyside/Liverpool, Cheshire, Derbyshire, Leicestershire, Lincolnshire, Suffolk, Worcestershire, Cornwall, Herefordshire and Shropshire.

## Governance after this audit

The geography and public search layers must remain separate:

1. `geo_lookup.xlsx` resolves factual source location.
2. `england_assessable_regions.json` defines the complete **55-market England diagnostic universe**.
3. Explicit roll-ups are applied after factual geography resolution; currently all three North East detail regions roll into `North East` for the assessment/public regional layer.
4. `job_slice_catalog.json` provides configured/public route metadata; absence from it is not geography failure.
5. `region_category_slice_register.csv` remains the explicit LIVE activation gate.

A mapped job must never be labelled `unknown` merely because its market has no configured/LIVE page.

## Public naming / aggregate search layer still to refine

The 55 assessment markets are now fixed for complete diagnostic coverage. Public-facing search wording can still use broader or alternative aggregates where that better matches jobseeker behaviour, without changing the underlying routing geography.

Priority naming/aggregate groups:

- Cheshire: East / West / Warrington & Halton, with broader `Cheshire jobs` search behaviour above them where useful
- Greater Manchester: Manchester & Salford / North / South / Wigan & Bolton, with a broader `Greater Manchester jobs` aggregate where useful
- Lancashire: North / Central / East / Blackpool & Fylde
- Cumbria: North / South / West
- Merseyside: Liverpool / Wirral, with broader Merseyside search behaviour where useful
- Leicestershire / Rutland
- West Midlands - Black Country

The governing rule is:

> official geography/commuting evidence guarantees complete coverage; jobseeker search behaviour determines the public-facing market name and grouping.

City pages remain a subordinate local/SEO layer and must not define regional coverage.

## Production safety

No existing regional URL is removed or redirected by this audit. The change is additive at the assessment layer. Any later public rename/restructure must be evidence-led and preserve existing indexing through appropriate redirects where necessary.

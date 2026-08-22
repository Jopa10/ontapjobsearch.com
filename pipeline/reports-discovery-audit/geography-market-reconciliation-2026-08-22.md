# Ontap England geography market reconciliation — 22 August 2026

## Scope

One-off audit only. This file does **not** change production geography, public routes, LIVE slice status or publishing.

Purpose: reconcile the current operational 33-market footprint against the fuller geography already present in `pipeline/geo/geo_lookup.xlsx`, then identify the candidate public England market set that must be validated against external geography and jobseeker search terminology before it is made canonical.

## What is now established internally

The current 33-market England diagnostic footprint is a configured operational subset, not the full geography authority.

The August Module 2 profiler explicitly reads `geo/geo_lookup.xlsx`. Its 2026-08 run log records **1,198 geo areas loaded**, and its daily-count output preserves the underlying lookup regions while adding `North East` separately as a published aggregate made from three lookup regions.

Reconciling the operational 33 against those lookup-region labels produces **exactly 22 additional non-North-East England markets**.

Therefore the current candidate public set is:

- **33 existing operational markets** (including the deliberate `North East` roll-up)
- **22 omitted non-North-East markets**
- **55 candidate public England markets in total**

This 55 is a candidate Ontap market count, not an official government geography count.

## Existing 33 — retain as candidates

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

## Exact 22 omitted non-North-East lookup markets

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

`North East` is intentionally not a peer lookup region. The Module 2 profiler preserves these three underlying regions:

- North East - Tyneside, Wearside & Northumberland
- North East - County Durham & Darlington/Hartlepool
- North East - Tees Valley

and separately creates the public/published `North East` aggregate. This was already a known special case and is not part of the missing-22 problem.

## External benchmark

The Ontap market count is custom and must not be presented as an ONS/GOV.UK standard.

External geography is used as the **coverage backstop**:

- ONS describes England's exhaustive administrative structure through regions, counties, unitary authorities, metropolitan counties/districts and London boroughs: https://www.ons.gov.uk/methodology/geography/ukgeographies/administrativegeography/england
- GOV.UK confirms the six metropolitan county areas, including Greater Manchester, Merseyside, South Yorkshire, Tyne and Wear, West Midlands and West Yorkshire: https://www.gov.uk/guidance/local-government-structure-and-elections
- ONS Travel to Work Areas are labour-market areas based on commuting patterns and cover the whole UK, but at 228 UK-wide they are a validation layer rather than the intended Ontap public-market granularity: https://www.ons.gov.uk/methodology/geography/ukgeographies/othergeographies

The missing-22 list includes externally recognisable geographic holes that the old 33 could not plausibly claim to cover, including Merseyside/Liverpool, Cheshire, Derbyshire, Leicestershire, Lincolnshire, Suffolk, Worcestershire, Cornwall, Herefordshire and Shropshire.

## What remains before `55` can become canonical public geography

The geography membership is now reconciled enough to make 55 the working candidate set. The **public market naming/grouping** still needs evidence-led sign-off in the areas below:

- Cheshire: East / West / Warrington & Halton versus broader jobseeker-facing Cheshire wording
- Greater Manchester: Manchester & Salford / North / South / Wigan & Bolton
- Lancashire: North / Central / East / Blackpool & Fylde
- Cumbria: North / South / West
- Merseyside: Liverpool / Wirral versus broader Merseyside wording
- Leicestershire / Rutland: whether Rutland warrants its own public market or should sit within a broader neighbouring search market
- West Midlands - Black Country: retain as a distinct market if search behaviour supports the recognised Black Country term

The governing rule is:

> official geography/commuting evidence guarantees complete coverage; jobseeker search behaviour determines the public-facing market name and grouping.

City pages remain a subordinate local/SEO layer and must not define the regional catchment.

## Production safety

No existing regional URL should be removed or redirected as part of this audit. The working assumption is additive. Any later rename/restructure must be evidence-led and preserve existing indexing through appropriate redirects where necessary.

## Next evidence step

Compare the ambiguous public market names in Google Keyword Planner (and, where useful, Search Console / established job-board search terminology), then freeze the public market names. After that, update diagnostics so a job mapped to any legitimate geography can never disappear merely because its region is absent from the configured LIVE-market subset.

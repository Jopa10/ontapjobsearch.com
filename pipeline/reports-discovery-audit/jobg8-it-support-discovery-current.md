# JobG8 IT Support family discovery

Feed: **2026-08-27.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **105**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **105**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **105**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **52**
Provisional BORDERLINE: **36**
Provisional OUT (specialist/salary): **17**
Estimated genuine inventory before deep advert review: **~70** (working range **52–88**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 52 |
| BORDERLINE | 36 |
| OUT_SALARY | 14 |
| OUT_SPECIALIST | 3 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 37 |
| £30k–£40k | 28 |
| £25k–£30k | 16 |
| >£50,000 OUT | 14 |
| £40k–£50,000 | 9 |
| <£25k | 1 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| I.T. & Communications | 79 |
| Administration | 14 |
| Consulting & Corporate Strategy | 3 |
| Real Estate & Property | 3 |
| Call Centre / CustomerService | 3 |
| Sales & Marketing | 1 |
| Accounting | 1 |
| Executive Positions | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **102**.
Content-unique candidates outside it or unresolved: **3**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 13 | YES |
| Kent | 9 | YES |
| Essex | 8 | YES |
| Greater Manchester - Manchester & Salford | 6 | YES |
| Hampshire | 6 | YES |
| Surrey | 6 | YES |
| Yorkshire - West | 5 | YES |
| Northern Ireland - East | 4 | YES |
| Hertfordshire | 3 | YES |
| Norfolk | 3 | YES |
| Wiltshire | 3 | YES |
| Worcestershire | 2 | YES |
| Northamptonshire | 2 | YES |
| Wales South - Swansea Bay | 2 | YES |
| Berkshire | 2 | YES |
| Other / Unknown | 2 | NO |
| West Midlands - Coventry & Warwickshire | 2 | YES |
| Oxfordshire | 2 | YES |
| Cambridgeshire | 2 | YES |
| West Midlands - Birmingham & Solihull | 2 | YES |
| Sussex | 2 | YES |
| Leicestershire | 1 | YES |
| Derbyshire | 1 | YES |
| Gloucestershire | 1 | YES |
| South West | 1 | NO |
| North East | 1 | YES |
| Dorset | 1 | YES |
| Staffordshire | 1 | YES |
| Bristol & Bath | 1 | YES |
| Cheshire - West | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

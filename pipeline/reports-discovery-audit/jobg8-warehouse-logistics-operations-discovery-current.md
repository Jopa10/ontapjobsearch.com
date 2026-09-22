# JobG8 Warehouse & Logistics Operations family discovery

Feed: **2026-09-22.xlsx**
Jobs in feed: **17,340**
Raw broad possible universe before exclusions/dedupe: **176**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **176**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **176**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **32**
Provisional BORDERLINE: **28**
Provisional OUT (specialist/salary): **116**
Estimated genuine inventory before deep advert review: **~46** (working range **32–60**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 94 |
| LIKELY_IN | 32 |
| BORDERLINE | 28 |
| OUT_SALARY | 22 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 71 |
| £25k–£30k | 41 |
| £30k–£40k | 25 |
| >£45,000 OUT | 22 |
| £40k–£45,000 | 9 |
| <£25k | 8 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Transport & Logistics | 148 |
| I.T. & Communications | 11 |
| Accounting | 6 |
| Real Estate & Property | 2 |
| Call Centre / CustomerService | 2 |
| Executive Positions | 2 |
| Administration | 1 |
| HR / Recruitment | 1 |
| Science & Technology | 1 |
| Sales & Marketing | 1 |
| Banking & Financial Services | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **166**.
Content-unique candidates outside it or unresolved: **10**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 13 | YES |
| North East | 8 | YES |
| Northamptonshire | 8 | YES |
| Bristol & Bath | 7 | YES |
| Gloucestershire | 7 | YES |
| Other / Unknown | 7 | NO |
| Northern Ireland - East | 6 | YES |
| Lincolnshire | 5 | YES |
| Hertfordshire | 5 | YES |
| Essex | 5 | YES |
| Greater Manchester - Manchester & Salford | 5 | YES |
| Suffolk | 4 | YES |
| West Midlands - Birmingham & Solihull | 4 | YES |
| Oxfordshire | 4 | YES |
| Somerset | 4 | YES |
| Sussex | 4 | YES |
| Kent | 4 | YES |
| Surrey | 3 | YES |
| Cheshire - West | 3 | YES |
| Derbyshire | 3 | YES |
| Greater Manchester - South | 3 | YES |
| Dorset | 3 | YES |
| Yorkshire - East | 3 | YES |
| Staffordshire | 3 | YES |
| Hampshire | 3 | YES |
| Worcestershire | 3 | YES |
| Nottinghamshire | 3 | YES |
| Leicestershire | 3 | YES |
| Cambridgeshire | 3 | YES |
| Wales - West | 2 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

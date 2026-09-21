# JobG8 Warehouse & Logistics Operations family discovery

Feed: **2026-09-21.xlsx**
Jobs in feed: **17,785**
Raw broad possible universe before exclusions/dedupe: **184**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **184**
Additional cross-reference content duplicates: **1**
Content-unique broad universe: **183**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **33**
Provisional BORDERLINE: **31**
Provisional OUT (specialist/salary): **119**
Estimated genuine inventory before deep advert review: **~49** (working range **33–64**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 97 |
| LIKELY_IN | 33 |
| BORDERLINE | 31 |
| OUT_SALARY | 22 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 75 |
| £25k–£30k | 43 |
| £30k–£40k | 26 |
| >£45,000 OUT | 22 |
| £40k–£45,000 | 9 |
| <£25k | 8 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Transport & Logistics | 153 |
| I.T. & Communications | 12 |
| Accounting | 6 |
| HR / Recruitment | 3 |
| Real Estate & Property | 2 |
| Call Centre / CustomerService | 2 |
| Executive Positions | 2 |
| Banking & Financial Services | 1 |
| Administration | 1 |
| Science & Technology | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **171**.
Content-unique candidates outside it or unresolved: **12**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 13 | YES |
| Other / Unknown | 9 | NO |
| Northamptonshire | 9 | YES |
| Bristol & Bath | 8 | YES |
| Gloucestershire | 7 | YES |
| North East | 7 | YES |
| Lincolnshire | 6 | YES |
| Essex | 6 | YES |
| Northern Ireland - East | 6 | YES |
| Hertfordshire | 5 | YES |
| Greater Manchester - Manchester & Salford | 5 | YES |
| Somerset | 4 | YES |
| Suffolk | 4 | YES |
| Cheshire - West | 4 | YES |
| Oxfordshire | 4 | YES |
| Sussex | 4 | YES |
| Worcestershire | 4 | YES |
| Nottinghamshire | 4 | YES |
| Surrey | 3 | YES |
| Derbyshire | 3 | YES |
| Devon | 3 | YES |
| Yorkshire - West | 3 | YES |
| Dorset | 3 | YES |
| Yorkshire - East | 3 | YES |
| West Midlands - Birmingham & Solihull | 3 | YES |
| Staffordshire | 3 | YES |
| Hampshire | 3 | YES |
| Leicestershire | 3 | YES |
| Cambridgeshire | 3 | YES |
| Kent | 3 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

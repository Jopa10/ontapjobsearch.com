# JobG8 HR / Recruitment family discovery

Feed: **2026-09-12.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **814**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **814**
Additional cross-reference content duplicates: **58**
Content-unique broad universe: **756**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **111**
Provisional BORDERLINE: **141**
Provisional OUT (specialist/salary): **504**
Estimated genuine inventory before deep advert review: **~181** (working range **111–252**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 415 |
| BORDERLINE | 141 |
| LIKELY_IN | 111 |
| OUT_SALARY | 89 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 320 |
| £30k–£40k | 151 |
| £25k–£30k | 95 |
| £40k–£50,000 | 95 |
| >£50,000 OUT | 89 |
| <£25k | 6 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| HR / Recruitment | 649 |
| Administration | 41 |
| Sales & Marketing | 25 |
| Legal | 19 |
| Consulting & Corporate Strategy | 8 |
| I.T. & Communications | 5 |
| Accounting | 2 |
| Executive Positions | 2 |
| Banking & Financial Services | 2 |
| Real Estate & Property | 1 |
| Healthcare & Medical | 1 |
| Retail & Consumer Products | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **705**.
Content-unique candidates outside it or unresolved: **51**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 119 | YES |
| Northern Ireland - East | 41 | YES |
| Other / Unknown | 40 | NO |
| West Midlands - Birmingham & Solihull | 38 | YES |
| Bristol & Bath | 26 | YES |
| Hampshire | 25 | YES |
| West Midlands - Coventry & Warwickshire | 22 | YES |
| Yorkshire - West | 20 | YES |
| Greater Manchester - Manchester & Salford | 20 | YES |
| Essex | 19 | YES |
| Surrey | 19 | YES |
| North East | 18 | YES |
| Nottinghamshire | 17 | YES |
| Kent | 15 | YES |
| Northamptonshire | 15 | YES |
| Devon | 15 | YES |
| Gloucestershire | 12 | YES |
| Oxfordshire | 12 | YES |
| Berkshire | 12 | YES |
| Hertfordshire | 11 | YES |
| Yorkshire - North | 11 | YES |
| Sussex | 10 | YES |
| Wiltshire | 10 | YES |
| Suffolk | 10 | YES |
| Buckinghamshire | 10 | YES |
| Worcestershire | 9 | YES |
| Dorset | 9 | YES |
| Somerset | 9 | YES |
| Norfolk | 8 | YES |
| Yorkshire - South | 8 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

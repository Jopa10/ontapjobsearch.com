# JobG8 HR / Recruitment family discovery

Feed: **2026-08-24.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **529**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **529**
Additional cross-reference content duplicates: **7**
Content-unique broad universe: **522**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **102**
Provisional BORDERLINE: **99**
Provisional OUT (specialist/salary): **321**
Estimated genuine inventory before deep advert review: **~152** (working range **102–201**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 240 |
| LIKELY_IN | 102 |
| BORDERLINE | 99 |
| OUT_SALARY | 81 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £30k–£40k | 170 |
| £25k–£30k | 120 |
| missing/unknown | 83 |
| >£50,000 OUT | 80 |
| £40k–£50,000 | 60 |
| <£25k | 9 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| HR / Recruitment | 370 |
| Administration | 104 |
| Sales & Marketing | 25 |
| Accounting | 6 |
| I.T. & Communications | 4 |
| Executive Positions | 3 |
| Consulting & Corporate Strategy | 3 |
| Retail & Consumer Products | 2 |
| Banking & Financial Services | 2 |
| Advert / Media / Entertainment | 1 |
| Healthcare & Medical | 1 |
| Legal | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **488**.
Content-unique candidates outside it or unresolved: **34**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 67 | YES |
| Bristol & Bath | 28 | YES |
| Other / Unknown | 27 | NO |
| Hampshire | 25 | YES |
| Yorkshire - West | 23 | YES |
| West Midlands - Birmingham & Solihull | 18 | YES |
| Nottinghamshire | 18 | YES |
| Greater Manchester - Manchester & Salford | 17 | YES |
| North East | 17 | YES |
| Berkshire | 15 | YES |
| Surrey | 15 | YES |
| Buckinghamshire | 14 | YES |
| Hertfordshire | 13 | YES |
| Devon | 13 | YES |
| Sussex | 12 | YES |
| Essex | 12 | YES |
| Kent | 11 | YES |
| Northamptonshire | 11 | YES |
| Lincolnshire | 10 | YES |
| Suffolk | 9 | YES |
| Yorkshire - East | 8 | YES |
| Leicestershire | 8 | YES |
| East Midlands | 7 | NO |
| Oxfordshire | 7 | YES |
| Yorkshire - North | 7 | YES |
| West Midlands - Coventry & Warwickshire | 7 | YES |
| Lancashire - Central | 7 | YES |
| Cambridgeshire | 7 | YES |
| Staffordshire | 6 | YES |
| Gloucestershire | 6 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

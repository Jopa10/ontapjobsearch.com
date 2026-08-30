# JobG8 Accounts & Finance Operations family discovery

Feed: **2026-08-30.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **821**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **821**
Additional cross-reference content duplicates: **1**
Content-unique broad universe: **820**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **171**
Provisional BORDERLINE: **0**
Provisional OUT (specialist/salary): **649**
Estimated genuine inventory before deep advert review: **~171** (working range **171–171**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 394 |
| OUT_SALARY | 240 |
| LIKELY_IN | 171 |
| OUT_BOUNDARY | 15 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| >£45,000 OUT | 239 |
| missing/unknown | 220 |
| £25k–£30k | 157 |
| £30k–£40k | 136 |
| £40k–£45,000 | 50 |
| <£25k | 18 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Accounting | 279 |
| Banking & Financial Services | 212 |
| Sales & Marketing | 204 |
| Administration | 43 |
| I.T. & Communications | 22 |
| HR / Recruitment | 14 |
| Executive Positions | 12 |
| Advert / Media / Entertainment | 7 |
| Consulting & Corporate Strategy | 7 |
| Real Estate & Property | 5 |
| Legal | 4 |
| Call Centre / CustomerService | 4 |
| Insurance & Superannuation | 4 |
| Retail & Consumer Products | 2 |
| Healthcare & Medical | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **751**.
Content-unique candidates outside it or unresolved: **69**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 81 | YES |
| Other / Unknown | 57 | NO |
| Yorkshire - West | 40 | YES |
| Greater Manchester - Manchester & Salford | 31 | YES |
| Bristol & Bath | 28 | YES |
| Devon | 28 | YES |
| Hampshire | 23 | YES |
| Northern Ireland - East | 22 | YES |
| West Midlands - Birmingham & Solihull | 21 | YES |
| Yorkshire - North | 20 | YES |
| Gloucestershire | 18 | YES |
| Oxfordshire | 17 | YES |
| Cambridgeshire | 16 | YES |
| Leicestershire | 16 | YES |
| Yorkshire - South | 16 | YES |
| Surrey | 15 | YES |
| Hertfordshire | 15 | YES |
| Berkshire | 15 | YES |
| Buckinghamshire | 15 | YES |
| Sussex | 14 | YES |
| North East | 14 | YES |
| Wiltshire | 14 | YES |
| Northamptonshire | 13 | YES |
| Cheshire - Warrington & Halton | 13 | YES |
| Nottinghamshire | 13 | YES |
| Essex | 12 | YES |
| Derbyshire | 11 | YES |
| Suffolk | 11 | YES |
| Merseyside - Liverpool | 11 | YES |
| Shropshire | 11 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

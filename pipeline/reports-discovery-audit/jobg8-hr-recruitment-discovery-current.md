# JobG8 HR / Recruitment family discovery

Feed: **2026-08-30.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **255**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **255**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **255**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **45**
Provisional BORDERLINE: **53**
Provisional OUT (specialist/salary): **157**
Estimated genuine inventory before deep advert review: **~71** (working range **45–98**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 136 |
| BORDERLINE | 53 |
| LIKELY_IN | 45 |
| OUT_SALARY | 21 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £25k–£30k | 88 |
| £30k–£40k | 78 |
| missing/unknown | 47 |
| >£50,000 OUT | 21 |
| £40k–£50,000 | 14 |
| <£25k | 7 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| HR / Recruitment | 141 |
| Administration | 49 |
| Sales & Marketing | 36 |
| I.T. & Communications | 10 |
| Consulting & Corporate Strategy | 5 |
| Accounting | 5 |
| Retail & Consumer Products | 2 |
| Real Estate & Property | 2 |
| Executive Positions | 2 |
| Healthcare & Medical | 1 |
| Banking & Financial Services | 1 |
| Legal | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **233**.
Content-unique candidates outside it or unresolved: **22**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 26 | YES |
| Bristol & Bath | 25 | YES |
| Other / Unknown | 22 | NO |
| Hampshire | 15 | YES |
| Greater Manchester - Manchester & Salford | 12 | YES |
| Yorkshire - West | 11 | YES |
| North East | 10 | YES |
| West Midlands - Birmingham & Solihull | 8 | YES |
| Essex | 7 | YES |
| Devon | 7 | YES |
| Sussex | 6 | YES |
| Kent | 6 | YES |
| Nottinghamshire | 6 | YES |
| Gloucestershire | 6 | YES |
| Yorkshire - North | 6 | YES |
| Suffolk | 5 | YES |
| Northamptonshire | 5 | YES |
| Lincolnshire | 5 | YES |
| Leicestershire | 5 | YES |
| Buckinghamshire | 5 | YES |
| Worcestershire | 5 | YES |
| Surrey | 4 | YES |
| Oxfordshire | 4 | YES |
| Berkshire | 3 | YES |
| West Midlands - Coventry & Warwickshire | 3 | YES |
| Shropshire | 3 | YES |
| Lancashire - Central | 3 | YES |
| Merseyside - Liverpool | 3 | YES |
| Somerset | 3 | YES |
| Bedfordshire | 2 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

# JobG8 HR / Recruitment family discovery

Feed: **2026-08-28.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **280**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **280**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **280**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **48**
Provisional BORDERLINE: **61**
Provisional OUT (specialist/salary): **171**
Estimated genuine inventory before deep advert review: **~78** (working range **48–109**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **CAUTION / LIKELY BELOW GATE**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 141 |
| BORDERLINE | 61 |
| LIKELY_IN | 48 |
| OUT_SALARY | 30 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £25k–£30k | 85 |
| £30k–£40k | 84 |
| missing/unknown | 61 |
| >£50,000 OUT | 29 |
| £40k–£50,000 | 13 |
| <£25k | 8 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| HR / Recruitment | 150 |
| Administration | 50 |
| Sales & Marketing | 39 |
| Accounting | 10 |
| Consulting & Corporate Strategy | 8 |
| I.T. & Communications | 7 |
| Executive Positions | 7 |
| Retail & Consumer Products | 2 |
| Legal | 2 |
| Banking & Financial Services | 2 |
| Real Estate & Property | 2 |
| Healthcare & Medical | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **258**.
Content-unique candidates outside it or unresolved: **22**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 37 | YES |
| Bristol & Bath | 24 | YES |
| Other / Unknown | 21 | NO |
| Hampshire | 17 | YES |
| Greater Manchester - Manchester & Salford | 13 | YES |
| Yorkshire - West | 10 | YES |
| North East | 10 | YES |
| West Midlands - Birmingham & Solihull | 9 | YES |
| Devon | 8 | YES |
| Buckinghamshire | 8 | YES |
| Nottinghamshire | 7 | YES |
| Sussex | 7 | YES |
| Essex | 7 | YES |
| Kent | 7 | YES |
| Lincolnshire | 6 | YES |
| Suffolk | 5 | YES |
| Northamptonshire | 5 | YES |
| Leicestershire | 5 | YES |
| Gloucestershire | 5 | YES |
| Oxfordshire | 4 | YES |
| West Midlands - Coventry & Warwickshire | 4 | YES |
| Lancashire - Central | 4 | YES |
| Somerset | 4 | YES |
| Worcestershire | 4 | YES |
| Yorkshire - North | 4 | YES |
| Surrey | 3 | YES |
| Berkshire | 3 | YES |
| Hertfordshire | 3 | YES |
| Scotland West - Glasgow | 3 | YES |
| Shropshire | 3 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

# JobG8 Warehouse & Logistics Operations family discovery

Feed: **2026-08-28.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **96**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **96**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **96**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **18**
Provisional BORDERLINE: **24**
Provisional OUT (specialist/salary): **54**
Estimated genuine inventory before deep advert review: **~30** (working range **18–42**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 36 |
| BORDERLINE | 24 |
| LIKELY_IN | 18 |
| OUT_SALARY | 18 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 27 |
| £25k–£30k | 25 |
| >£45,000 OUT | 18 |
| £30k–£40k | 16 |
| £40k–£45,000 | 6 |
| <£25k | 4 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Administration | 31 |
| Banking & Financial Services | 14 |
| Sales & Marketing | 13 |
| Executive Positions | 9 |
| I.T. & Communications | 6 |
| Call Centre / CustomerService | 5 |
| Healthcare & Medical | 3 |
| Consulting & Corporate Strategy | 3 |
| HR / Recruitment | 3 |
| Advert / Media / Entertainment | 2 |
| Real Estate & Property | 2 |
| Accounting | 2 |
| Science & Technology | 1 |
| Retail & Consumer Products | 1 |
| Legal | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **85**.
Content-unique candidates outside it or unresolved: **11**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 11 | YES |
| Other / Unknown | 9 | NO |
| Berkshire | 5 | YES |
| West Midlands - Birmingham & Solihull | 4 | YES |
| Scotland West - Glasgow | 4 | YES |
| Northamptonshire | 4 | YES |
| Essex | 3 | YES |
| West Midlands - Black Country | 3 | YES |
| Buckinghamshire | 3 | YES |
| Leicestershire | 3 | YES |
| Kent | 3 | YES |
| Staffordshire | 3 | YES |
| Derbyshire | 2 | YES |
| Lincolnshire | 2 | YES |
| West Midlands - Coventry & Warwickshire | 2 | YES |
| Yorkshire - West | 2 | YES |
| Greater Manchester - Manchester & Salford | 2 | YES |
| Oxfordshire | 2 | YES |
| Cambridgeshire | 2 | YES |
| Surrey | 2 | YES |
| Bristol & Bath | 2 | YES |
| Northern Ireland - East | 2 | YES |
| East Midlands | 2 | NO |
| Somerset | 2 | YES |
| Nottinghamshire | 2 | YES |
| Yorkshire - North | 2 | YES |
| Norfolk | 2 | YES |
| Cumbria - South | 1 | YES |
| Lancashire - East | 1 | YES |
| Dorset | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

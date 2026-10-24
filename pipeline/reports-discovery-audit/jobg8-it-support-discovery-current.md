# JobG8 IT Support family discovery

Feed: **2026-10-24.xlsx**
Jobs in feed: **20,000**
Raw broad possible universe before exclusions/dedupe: **189**
Reference-key duplicates within broad universe: **1**
Reference-deduped broad universe: **188**
Additional cross-reference content duplicates: **4**
Content-unique broad universe: **184**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **97**
Provisional BORDERLINE: **63**
Provisional OUT (specialist/salary): **24**
Estimated genuine inventory before deep advert review: **~129** (working range **97–160**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO TO BOUNDARY SAMPLE / SCALE PLAUSIBLE**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 97 |
| BORDERLINE | 63 |
| OUT_SALARY | 14 |
| OUT_SPECIALIST | 10 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 81 |
| £30k–£40k | 50 |
| £25k–£30k | 20 |
| >£50,000 OUT | 14 |
| £40k–£50,000 | 11 |
| <£25k | 8 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| I.T. & Communications | 142 |
| Call Centre / CustomerService | 13 |
| Administration | 12 |
| Real Estate & Property | 4 |
| Sales & Marketing | 3 |
| Accounting | 3 |
| Government & Defence | 2 |
| Healthcare & Medical | 2 |
| Transport & Logistics | 1 |
| Legal | 1 |
| HR / Recruitment | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **172**.
Content-unique candidates outside it or unresolved: **12**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 24 | YES |
| Other / Unknown | 10 | NO |
| Essex | 9 | YES |
| Oxfordshire | 9 | YES |
| Berkshire | 8 | YES |
| Hertfordshire | 7 | YES |
| Bristol & Bath | 7 | YES |
| Greater Manchester - Manchester & Salford | 7 | YES |
| Surrey | 7 | YES |
| Hampshire | 7 | YES |
| Gloucestershire | 5 | YES |
| Buckinghamshire | 5 | YES |
| Nottinghamshire | 4 | YES |
| Yorkshire - West | 4 | YES |
| Kent | 4 | YES |
| Lincolnshire | 4 | YES |
| North East | 4 | YES |
| West Midlands - Birmingham & Solihull | 4 | YES |
| Sussex | 4 | YES |
| Dorset | 4 | YES |
| Worcestershire | 3 | YES |
| West Midlands - Coventry & Warwickshire | 3 | YES |
| Norfolk | 3 | YES |
| Northamptonshire | 3 | YES |
| Merseyside - Liverpool | 3 | YES |
| Greater Manchester - Wigan & Bolton | 2 | YES |
| Suffolk | 2 | YES |
| Bedfordshire | 2 | YES |
| Scotland Central - Edinburgh & Lothians | 2 | YES |
| Devon | 2 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

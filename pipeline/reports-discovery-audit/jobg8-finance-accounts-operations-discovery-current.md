# JobG8 Accounts & Finance Operations family discovery

Feed: **2026-09-12.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **889**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **889**
Additional cross-reference content duplicates: **6**
Content-unique broad universe: **883**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **162**
Provisional BORDERLINE: **0**
Provisional OUT (specialist/salary): **721**
Estimated genuine inventory before deep advert review: **~162** (working range **162–162**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 468 |
| OUT_SALARY | 228 |
| LIKELY_IN | 162 |
| OUT_BOUNDARY | 25 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 359 |
| >£45,000 OUT | 228 |
| £30k–£40k | 124 |
| £25k–£30k | 112 |
| £40k–£45,000 | 46 |
| <£25k | 14 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Accounting | 266 |
| Sales & Marketing | 217 |
| Banking & Financial Services | 141 |
| Insurance & Superannuation | 111 |
| Administration | 54 |
| HR / Recruitment | 32 |
| I.T. & Communications | 17 |
| Call Centre / CustomerService | 13 |
| Legal | 11 |
| Advert / Media / Entertainment | 7 |
| Real Estate & Property | 6 |
| Consulting & Corporate Strategy | 4 |
| Retail & Consumer Products | 2 |
| Executive Positions | 2 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **822**.
Content-unique candidates outside it or unresolved: **61**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 144 | YES |
| Northern Ireland - East | 50 | YES |
| Other / Unknown | 49 | NO |
| Greater Manchester - Manchester & Salford | 47 | YES |
| Yorkshire - West | 32 | YES |
| Sussex | 29 | YES |
| Bristol & Bath | 27 | YES |
| Hampshire | 26 | YES |
| West Midlands - Birmingham & Solihull | 22 | YES |
| Surrey | 21 | YES |
| Northamptonshire | 20 | YES |
| Essex | 19 | YES |
| Buckinghamshire | 18 | YES |
| Hertfordshire | 18 | YES |
| Gloucestershire | 17 | YES |
| North East | 16 | YES |
| Devon | 16 | YES |
| Kent | 15 | YES |
| Berkshire | 15 | YES |
| Cambridgeshire | 15 | YES |
| West Midlands - Coventry & Warwickshire | 15 | YES |
| Wiltshire | 14 | YES |
| Yorkshire - North | 14 | YES |
| Merseyside - Liverpool | 12 | YES |
| Dorset | 12 | YES |
| Suffolk | 10 | YES |
| Leicestershire | 10 | YES |
| Yorkshire - South | 10 | YES |
| Staffordshire | 9 | YES |
| Cheshire - West | 9 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

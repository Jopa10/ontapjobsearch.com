# JobG8 Accounts & Finance Operations family discovery

Feed: **2026-08-29.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **838**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **838**
Additional cross-reference content duplicates: **1**
Content-unique broad universe: **837**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **182**
Provisional BORDERLINE: **0**
Provisional OUT (specialist/salary): **655**
Estimated genuine inventory before deep advert review: **~182** (working range **182–182**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 394 |
| OUT_SALARY | 244 |
| LIKELY_IN | 182 |
| OUT_BOUNDARY | 17 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| >£45,000 OUT | 243 |
| missing/unknown | 222 |
| £25k–£30k | 163 |
| £30k–£40k | 139 |
| £40k–£45,000 | 51 |
| <£25k | 19 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Accounting | 291 |
| Banking & Financial Services | 222 |
| Sales & Marketing | 200 |
| Administration | 42 |
| I.T. & Communications | 21 |
| HR / Recruitment | 16 |
| Executive Positions | 11 |
| Advert / Media / Entertainment | 7 |
| Consulting & Corporate Strategy | 6 |
| Real Estate & Property | 5 |
| Insurance & Superannuation | 5 |
| Legal | 4 |
| Call Centre / CustomerService | 4 |
| Retail & Consumer Products | 2 |
| Healthcare & Medical | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **767**.
Content-unique candidates outside it or unresolved: **70**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 87 | YES |
| Other / Unknown | 58 | NO |
| Yorkshire - West | 40 | YES |
| Greater Manchester - Manchester & Salford | 31 | YES |
| Bristol & Bath | 28 | YES |
| Devon | 27 | YES |
| Hampshire | 24 | YES |
| Northern Ireland - East | 23 | YES |
| Yorkshire - North | 21 | YES |
| West Midlands - Birmingham & Solihull | 20 | YES |
| Leicestershire | 19 | YES |
| Gloucestershire | 17 | YES |
| Yorkshire - South | 17 | YES |
| North East | 16 | YES |
| Buckinghamshire | 16 | YES |
| Cambridgeshire | 16 | YES |
| Oxfordshire | 16 | YES |
| Hertfordshire | 15 | YES |
| Berkshire | 15 | YES |
| Surrey | 14 | YES |
| Sussex | 14 | YES |
| Wiltshire | 14 | YES |
| Northamptonshire | 13 | YES |
| Essex | 13 | YES |
| Cheshire - Warrington & Halton | 13 | YES |
| Suffolk | 13 | YES |
| Nottinghamshire | 13 | YES |
| Somerset | 12 | YES |
| Yorkshire - East | 11 | YES |
| Derbyshire | 10 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

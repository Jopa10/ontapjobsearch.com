# JobG8 Accounts & Finance Operations family discovery

Feed: **2026-08-28.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **1,057**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **1,057**
Additional cross-reference content duplicates: **1**
Content-unique broad universe: **1,056**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **277**
Provisional BORDERLINE: **0**
Provisional OUT (specialist/salary): **779**
Estimated genuine inventory before deep advert review: **~277** (working range **277–277**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 410 |
| OUT_SALARY | 352 |
| LIKELY_IN | 277 |
| OUT_BOUNDARY | 17 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| >£45,000 OUT | 351 |
| missing/unknown | 251 |
| £25k–£30k | 218 |
| £30k–£40k | 165 |
| £40k–£45,000 | 47 |
| <£25k | 24 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Accounting | 409 |
| Banking & Financial Services | 305 |
| Sales & Marketing | 205 |
| Administration | 48 |
| HR / Recruitment | 16 |
| I.T. & Communications | 16 |
| Executive Positions | 13 |
| Consulting & Corporate Strategy | 10 |
| Advert / Media / Entertainment | 7 |
| Legal | 6 |
| Call Centre / CustomerService | 6 |
| Real Estate & Property | 5 |
| Insurance & Superannuation | 5 |
| Healthcare & Medical | 3 |
| Retail & Consumer Products | 2 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **974**.
Content-unique candidates outside it or unresolved: **82**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 128 | YES |
| Other / Unknown | 58 | NO |
| Greater Manchester - Manchester & Salford | 57 | YES |
| Yorkshire - West | 52 | YES |
| Bristol & Bath | 36 | YES |
| Leicestershire | 31 | YES |
| West Midlands - Birmingham & Solihull | 30 | YES |
| Hampshire | 25 | YES |
| Devon | 24 | YES |
| Yorkshire - South | 22 | YES |
| Oxfordshire | 22 | YES |
| Yorkshire - North | 22 | YES |
| Buckinghamshire | 22 | YES |
| Northamptonshire | 21 | YES |
| Cambridgeshire | 21 | YES |
| Northern Ireland - East | 20 | YES |
| Nottinghamshire | 20 | YES |
| North East | 19 | YES |
| Cheshire - Warrington & Halton | 18 | YES |
| Gloucestershire | 18 | YES |
| Hertfordshire | 18 | YES |
| Berkshire | 17 | YES |
| Surrey | 16 | YES |
| Essex | 16 | YES |
| Merseyside - Liverpool | 16 | YES |
| Shropshire | 15 | YES |
| East Midlands | 14 | NO |
| Lincolnshire | 14 | YES |
| Scotland West - Glasgow | 13 | YES |
| Sussex | 13 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

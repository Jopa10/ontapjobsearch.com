# JobG8 IT Support family discovery

Feed: **2026-08-31.xlsx**
Jobs in feed: **5,354**
Raw broad possible universe before exclusions/dedupe: **402**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **402**
Additional cross-reference content duplicates: **1**
Content-unique broad universe: **401**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **229**
Provisional BORDERLINE: **116**
Provisional OUT (specialist/salary): **56**
Estimated genuine inventory before deep advert review: **~287** (working range **229–345**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 229 |
| BORDERLINE | 116 |
| OUT_SALARY | 34 |
| OUT_SPECIALIST | 22 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 213 |
| £30k–£40k | 88 |
| £25k–£30k | 36 |
| >£50,000 OUT | 34 |
| £40k–£50,000 | 26 |
| <£25k | 4 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| I.T. & Communications | 383 |
| Administration | 13 |
| Call Centre / CustomerService | 3 |
| Real Estate & Property | 1 |
| Accounting | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **381**.
Content-unique candidates outside it or unresolved: **20**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 92 | YES |
| Hampshire | 18 | YES |
| West Midlands - Birmingham & Solihull | 17 | YES |
| Surrey | 15 | YES |
| Kent | 14 | YES |
| Hertfordshire | 13 | YES |
| Berkshire | 13 | YES |
| North East | 13 | YES |
| Bristol & Bath | 12 | YES |
| Oxfordshire | 11 | YES |
| Essex | 9 | YES |
| Other / Unknown | 9 | NO |
| Greater Manchester - Manchester & Salford | 9 | YES |
| Yorkshire - West | 8 | YES |
| Merseyside - Liverpool | 8 | YES |
| Norfolk | 8 | YES |
| East Midlands | 8 | NO |
| Sussex | 7 | YES |
| Yorkshire - South | 7 | YES |
| Gloucestershire | 6 | YES |
| Scotland West - Glasgow | 6 | YES |
| Buckinghamshire | 6 | YES |
| Staffordshire | 5 | YES |
| Cambridgeshire | 5 | YES |
| Scotland Central - Edinburgh & Lothians | 5 | YES |
| Lincolnshire | 5 | YES |
| Worcestershire | 4 | YES |
| Northamptonshire | 4 | YES |
| Northern Ireland - East | 3 | YES |
| West Midlands - Black Country | 3 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

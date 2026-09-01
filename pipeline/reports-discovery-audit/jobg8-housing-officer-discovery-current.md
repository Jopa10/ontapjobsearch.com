# JobG8 Housing Officer family discovery

Feed: **2026-09-01.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **75**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **75**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **75**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **18**
Provisional BORDERLINE: **30**
Provisional OUT (specialist/salary): **27**
Estimated genuine inventory before deep advert review: **~33** (working range **18–48**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| BORDERLINE | 30 |
| LIKELY_IN | 18 |
| OUT_SALARY | 16 |
| OUT_SPECIALIST | 11 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 24 |
| >£50,000 OUT | 16 |
| £30k–£40k | 15 |
| £25k–£30k | 9 |
| <£25k | 8 |
| £40k–£50,000 | 3 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Real Estate & Property | 28 |
| Healthcare & Medical | 17 |
| Administration | 9 |
| Banking & Financial Services | 6 |
| Call Centre / CustomerService | 4 |
| Legal | 4 |
| Executive Positions | 3 |
| I.T. & Communications | 3 |
| Insurance & Superannuation | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **67**.
Content-unique candidates outside it or unresolved: **8**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 13 | YES |
| Other / Unknown | 7 | NO |
| Greater Manchester - Manchester & Salford | 5 | YES |
| Oxfordshire | 5 | YES |
| Dorset | 4 | YES |
| Devon | 3 | YES |
| Kent | 3 | YES |
| Sussex | 3 | YES |
| Hampshire | 3 | YES |
| Cambridgeshire | 3 | YES |
| Northamptonshire | 2 | YES |
| Wiltshire | 2 | YES |
| Nottinghamshire | 2 | YES |
| Surrey | 2 | YES |
| Berkshire | 2 | YES |
| Essex | 1 | YES |
| Norfolk | 1 | YES |
| Yorkshire - North | 1 | YES |
| North East | 1 | YES |
| Cheshire - Warrington & Halton | 1 | YES |
| Staffordshire | 1 | YES |
| Hertfordshire | 1 | YES |
| Yorkshire - West | 1 | YES |
| Suffolk | 1 | YES |
| Buckinghamshire | 1 | YES |
| Cheshire - East | 1 | YES |
| Shropshire | 1 | YES |
| Bristol & Bath | 1 | YES |
| Scotland West - Ayrshire | 1 | YES |
| Gloucestershire | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

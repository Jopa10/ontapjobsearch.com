# JobG8 Housing Officer family discovery

Feed: **2026-08-28.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **100**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **100**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **100**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **29**
Provisional BORDERLINE: **38**
Provisional OUT (specialist/salary): **33**
Estimated genuine inventory before deep advert review: **~48** (working range **29–67**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| BORDERLINE | 38 |
| LIKELY_IN | 29 |
| OUT_SALARY | 22 |
| OUT_SPECIALIST | 11 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £25k–£30k | 26 |
| >£50,000 OUT | 22 |
| missing/unknown | 22 |
| £30k–£40k | 20 |
| <£25k | 6 |
| £40k–£50,000 | 4 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Real Estate & Property | 29 |
| Healthcare & Medical | 26 |
| Executive Positions | 10 |
| Accounting | 9 |
| Administration | 8 |
| Banking & Financial Services | 6 |
| Legal | 6 |
| Call Centre / CustomerService | 4 |
| Insurance & Superannuation | 1 |
| Consulting & Corporate Strategy | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **92**.
Content-unique candidates outside it or unresolved: **8**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 12 | YES |
| Other / Unknown | 8 | NO |
| Greater Manchester - Manchester & Salford | 7 | YES |
| Oxfordshire | 6 | YES |
| Devon | 4 | YES |
| Cambridgeshire | 4 | YES |
| Dorset | 4 | YES |
| Hampshire | 4 | YES |
| Surrey | 4 | YES |
| Wiltshire | 3 | YES |
| Kent | 3 | YES |
| Sussex | 3 | YES |
| West Midlands - Birmingham & Solihull | 2 | YES |
| Essex | 2 | YES |
| Cheshire - Warrington & Halton | 2 | YES |
| Northamptonshire | 2 | YES |
| North East | 2 | YES |
| West Midlands - Coventry & Warwickshire | 2 | YES |
| Nottinghamshire | 2 | YES |
| Bedfordshire | 2 | YES |
| Hertfordshire | 2 | YES |
| Suffolk | 2 | YES |
| Scotland West - Glasgow | 2 | YES |
| Merseyside - Liverpool | 2 | YES |
| Leicestershire | 2 | YES |
| North Scotland | 1 | YES |
| Norfolk | 1 | YES |
| Yorkshire - North | 1 | YES |
| Somerset | 1 | YES |
| Staffordshire | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

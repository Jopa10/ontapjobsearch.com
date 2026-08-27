# JobG8 Housing Officer family discovery

Feed: **2026-08-27.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **98**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **98**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **98**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **28**
Provisional BORDERLINE: **37**
Provisional OUT (specialist/salary): **33**
Estimated genuine inventory before deep advert review: **~46** (working range **28–65**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| BORDERLINE | 37 |
| LIKELY_IN | 28 |
| OUT_SALARY | 22 |
| OUT_SPECIALIST | 11 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 24 |
| >£50,000 OUT | 22 |
| £30k–£40k | 21 |
| £25k–£30k | 21 |
| <£25k | 6 |
| £40k–£50,000 | 4 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Real Estate & Property | 30 |
| Healthcare & Medical | 25 |
| Administration | 9 |
| Accounting | 9 |
| Executive Positions | 7 |
| Legal | 6 |
| Banking & Financial Services | 5 |
| Call Centre / CustomerService | 4 |
| Retail & Consumer Products | 1 |
| Consulting & Corporate Strategy | 1 |
| Insurance & Superannuation | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **92**.
Content-unique candidates outside it or unresolved: **6**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 14 | YES |
| Other / Unknown | 6 | NO |
| Greater Manchester - Manchester & Salford | 6 | YES |
| Oxfordshire | 6 | YES |
| Hampshire | 5 | YES |
| Cambridgeshire | 4 | YES |
| Dorset | 4 | YES |
| Sussex | 4 | YES |
| Devon | 3 | YES |
| Essex | 3 | YES |
| Wiltshire | 3 | YES |
| Hertfordshire | 3 | YES |
| Kent | 3 | YES |
| Bedfordshire | 2 | YES |
| West Midlands - Birmingham & Solihull | 2 | YES |
| Cheshire - Warrington & Halton | 2 | YES |
| Northamptonshire | 2 | YES |
| North East | 2 | YES |
| West Midlands - Coventry & Warwickshire | 2 | YES |
| Nottinghamshire | 2 | YES |
| Suffolk | 2 | YES |
| Scotland West - Glasgow | 2 | YES |
| Merseyside - Liverpool | 2 | YES |
| North Scotland | 1 | YES |
| Norfolk | 1 | YES |
| Yorkshire - North | 1 | YES |
| Somerset | 1 | YES |
| Staffordshire | 1 | YES |
| Cornwall | 1 | YES |
| Berkshire | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

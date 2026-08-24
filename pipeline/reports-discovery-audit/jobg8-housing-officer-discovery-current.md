# JobG8 Housing Officer family discovery

Feed: **2026-08-24.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **129**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **129**
Additional cross-reference content duplicates: **2**
Content-unique broad universe: **127**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **40**
Provisional BORDERLINE: **34**
Provisional OUT (specialist/salary): **53**
Estimated genuine inventory before deep advert review: **~57** (working range **40–74**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 40 |
| OUT_SALARY | 36 |
| BORDERLINE | 34 |
| OUT_SPECIALIST | 17 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| >£50,000 OUT | 36 |
| £30k–£40k | 28 |
| missing/unknown | 27 |
| £25k–£30k | 20 |
| <£25k | 8 |
| £40k–£50,000 | 8 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Real Estate & Property | 53 |
| Healthcare & Medical | 22 |
| Legal | 16 |
| Executive Positions | 12 |
| Administration | 10 |
| Banking & Financial Services | 6 |
| Call Centre / CustomerService | 5 |
| Consulting & Corporate Strategy | 2 |
| Insurance & Superannuation | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **121**.
Content-unique candidates outside it or unresolved: **6**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 23 | YES |
| Greater Manchester - Manchester & Salford | 12 | YES |
| Essex | 8 | YES |
| Other / Unknown | 5 | NO |
| Cambridgeshire | 5 | YES |
| Yorkshire - West | 5 | YES |
| Sussex | 5 | YES |
| Berkshire | 4 | YES |
| West Midlands - Birmingham & Solihull | 4 | YES |
| Bedfordshire | 4 | YES |
| Dorset | 4 | YES |
| Devon | 3 | YES |
| Cheshire - Warrington & Halton | 3 | YES |
| Hertfordshire | 3 | YES |
| Oxfordshire | 3 | YES |
| Cumbria - North | 2 | YES |
| Norfolk | 2 | YES |
| North East | 2 | YES |
| West Midlands - Coventry & Warwickshire | 2 | YES |
| Suffolk | 2 | YES |
| Yorkshire - South | 2 | YES |
| Wiltshire | 2 | YES |
| Kent | 2 | YES |
| Worcestershire | 1 | YES |
| Wales South - Valleys | 1 | YES |
| North Scotland | 1 | YES |
| Yorkshire - North | 1 | YES |
| Northamptonshire | 1 | YES |
| Cumbria - West | 1 | YES |
| Buckinghamshire | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

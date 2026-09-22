# JobG8 Housing Officer family discovery

Feed: **2026-09-22.xlsx**
Jobs in feed: **17,340**
Raw broad possible universe before exclusions/dedupe: **55**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **55**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **55**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **8**
Provisional BORDERLINE: **20**
Provisional OUT (specialist/salary): **27**
Estimated genuine inventory before deep advert review: **~18** (working range **8–28**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| BORDERLINE | 20 |
| OUT_SPECIALIST | 19 |
| LIKELY_IN | 8 |
| OUT_SALARY | 8 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 26 |
| £30k–£40k | 11 |
| £25k–£30k | 7 |
| >£50,000 OUT | 6 |
| £40k–£50,000 | 4 |
| <£25k | 1 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Healthcare & Medical | 17 |
| Legal | 15 |
| Community & Sport | 8 |
| Real Estate & Property | 7 |
| Accounting | 3 |
| I.T. & Communications | 1 |
| Executive Positions | 1 |
| Administration | 1 |
| Insurance & Superannuation | 1 |
| Call Centre / CustomerService | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **52**.
Content-unique candidates outside it or unresolved: **3**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 8 | YES |
| Greater Manchester - Manchester & Salford | 5 | YES |
| Sussex | 4 | YES |
| Merseyside - Liverpool | 4 | YES |
| Kent | 3 | YES |
| Other / Unknown | 3 | NO |
| North East | 2 | YES |
| West Midlands - Birmingham & Solihull | 2 | YES |
| Norfolk | 2 | YES |
| Devon | 2 | YES |
| Scotland West - Ayrshire | 1 | YES |
| Bristol & Bath | 1 | YES |
| Buckinghamshire | 1 | YES |
| Hampshire | 1 | YES |
| Northamptonshire | 1 | YES |
| Cambridgeshire | 1 | YES |
| Berkshire | 1 | YES |
| West Midlands - Coventry & Warwickshire | 1 | YES |
| Greater Manchester - Wigan & Bolton | 1 | YES |
| Dorset | 1 | YES |
| Surrey | 1 | YES |
| Cheshire - West | 1 | YES |
| Hertfordshire | 1 | YES |
| Oxfordshire | 1 | YES |
| Greater Manchester - South | 1 | YES |
| Bedfordshire | 1 | YES |
| Suffolk | 1 | YES |
| Worcestershire | 1 | YES |
| Leicestershire | 1 | YES |
| Shropshire | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

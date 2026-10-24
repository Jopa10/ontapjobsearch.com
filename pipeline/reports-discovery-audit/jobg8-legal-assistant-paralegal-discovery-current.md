# JobG8 Legal Assistant / Paralegal family discovery

Feed: **2026-10-24.xlsx**
Jobs in feed: **20,000**
Raw broad possible universe before exclusions/dedupe: **507**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **507**
Additional cross-reference content duplicates: **19**
Content-unique broad universe: **488**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **381**
Provisional BORDERLINE: **19**
Provisional OUT (specialist/salary): **88**
Estimated genuine inventory before deep advert review: **~391** (working range **381–400**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 381 |
| OUT_SPECIALIST | 51 |
| OUT_SALARY | 37 |
| BORDERLINE | 19 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 261 |
| £25k–£30k | 104 |
| £30k–£40k | 70 |
| >£50,000 OUT | 37 |
| £40k–£50,000 | 11 |
| <£25k | 5 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Legal | 470 |
| Administration | 15 |
| Real Estate & Property | 3 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **463**.
Content-unique candidates outside it or unresolved: **25**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 85 | YES |
| Essex | 37 | YES |
| Suffolk | 33 | YES |
| Surrey | 24 | YES |
| Yorkshire - North | 20 | YES |
| Other / Unknown | 19 | NO |
| Yorkshire - West | 17 | YES |
| Norfolk | 16 | YES |
| Hertfordshire | 15 | YES |
| Hampshire | 14 | YES |
| Sussex | 12 | YES |
| Greater Manchester - Manchester & Salford | 12 | YES |
| Northamptonshire | 11 | YES |
| Berkshire | 10 | YES |
| Kent | 9 | YES |
| Nottinghamshire | 9 | YES |
| West Midlands - Coventry & Warwickshire | 9 | YES |
| Buckinghamshire | 9 | YES |
| Yorkshire - South | 8 | YES |
| Cambridgeshire | 8 | YES |
| Bristol & Bath | 8 | YES |
| North East | 7 | YES |
| Dorset | 7 | YES |
| Gloucestershire | 6 | YES |
| Scotland West - Glasgow | 6 | YES |
| Devon | 6 | YES |
| Bedfordshire | 5 | YES |
| Oxfordshire | 5 | YES |
| West Midlands - Birmingham & Solihull | 5 | YES |
| Leicestershire | 4 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

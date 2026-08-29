# JobG8 IT Support family discovery

Feed: **2026-08-29.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **158**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **158**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **158**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **86**
Provisional BORDERLINE: **54**
Provisional OUT (specialist/salary): **18**
Estimated genuine inventory before deep advert review: **~113** (working range **86–140**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO TO BOUNDARY SAMPLE / SCALE PLAUSIBLE**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 86 |
| BORDERLINE | 54 |
| OUT_SALARY | 12 |
| OUT_SPECIALIST | 6 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 64 |
| £30k–£40k | 41 |
| £25k–£30k | 28 |
| £40k–£50,000 | 12 |
| >£50,000 OUT | 12 |
| <£25k | 1 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| I.T. & Communications | 139 |
| Administration | 13 |
| Call Centre / CustomerService | 3 |
| Real Estate & Property | 1 |
| Sales & Marketing | 1 |
| Accounting | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **141**.
Content-unique candidates outside it or unresolved: **17**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 25 | YES |
| Other / Unknown | 15 | NO |
| Kent | 10 | YES |
| Essex | 8 | YES |
| Hampshire | 7 | YES |
| Berkshire | 7 | YES |
| West Midlands - Birmingham & Solihull | 6 | YES |
| Yorkshire - West | 5 | YES |
| Gloucestershire | 5 | YES |
| Surrey | 5 | YES |
| Northern Ireland - East | 4 | YES |
| Hertfordshire | 4 | YES |
| Northamptonshire | 4 | YES |
| Staffordshire | 3 | YES |
| Leicestershire | 3 | YES |
| West Midlands - Black Country | 3 | YES |
| Wiltshire | 3 | YES |
| Bristol & Bath | 3 | YES |
| Greater Manchester - Manchester & Salford | 3 | YES |
| Norfolk | 3 | YES |
| Worcestershire | 2 | YES |
| Derbyshire | 2 | YES |
| North East | 2 | YES |
| Sussex | 2 | YES |
| Yorkshire - South | 2 | YES |
| West Midlands - Coventry & Warwickshire | 2 | YES |
| Oxfordshire | 2 | YES |
| Cambridgeshire | 2 | YES |
| Lincolnshire | 1 | YES |
| South West | 1 | NO |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

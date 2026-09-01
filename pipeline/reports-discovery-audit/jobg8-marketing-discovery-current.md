# JobG8 Marketing family discovery

Feed: **2026-08-31.xlsx**
Jobs in feed: **5,354**
Raw broad possible universe before exclusions/dedupe: **97**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **97**
Additional cross-reference content duplicates: **8**
Content-unique broad universe: **89**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **38**
Provisional BORDERLINE: **20**
Provisional OUT (specialist/salary): **31**
Estimated genuine inventory before deep advert review: **~48** (working range **38–58**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 38 |
| BORDERLINE | 20 |
| OUT_SPECIALIST | 18 |
| OUT_SALARY | 13 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 42 |
| £30k–£40k | 15 |
| £40k–£50,000 | 12 |
| >£50,000 OUT | 12 |
| £25k–£30k | 5 |
| <£25k | 3 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Sales & Marketing | 49 |
| I.T. & Communications | 19 |
| Advert / Media / Entertainment | 11 |
| Administration | 4 |
| Retail & Consumer Products | 3 |
| Consulting & Corporate Strategy | 1 |
| Legal | 1 |
| Call Centre / CustomerService | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **80**.
Content-unique candidates outside it or unresolved: **9**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 29 | YES |
| Other / Unknown | 9 | NO |
| West Midlands - Birmingham & Solihull | 5 | YES |
| Greater Manchester - Manchester & Salford | 4 | YES |
| Berkshire | 4 | YES |
| Hampshire | 4 | YES |
| Kent | 3 | YES |
| Surrey | 3 | YES |
| Dorset | 2 | YES |
| Northern Ireland - East | 2 | YES |
| Wales South - Swansea Bay | 2 | YES |
| Wales - West | 2 | YES |
| Sussex | 2 | YES |
| Lincolnshire | 2 | YES |
| North East | 2 | YES |
| Oxfordshire | 2 | YES |
| Nottinghamshire | 1 | YES |
| Buckinghamshire | 1 | YES |
| Essex | 1 | YES |
| Scotland Central - Tayside | 1 | YES |
| Devon | 1 | YES |
| Scotland Central - Edinburgh & Lothians | 1 | YES |
| Bedfordshire | 1 | YES |
| West Midlands - Coventry & Warwickshire | 1 | YES |
| Gloucestershire | 1 | YES |
| Norfolk | 1 | YES |
| Worcestershire | 1 | YES |
| Suffolk | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

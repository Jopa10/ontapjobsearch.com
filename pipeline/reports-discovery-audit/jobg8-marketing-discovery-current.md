# JobG8 Marketing family discovery

Feed: **2026-08-24.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **207**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **207**
Additional cross-reference content duplicates: **10**
Content-unique broad universe: **197**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **97**
Provisional BORDERLINE: **39**
Provisional OUT (specialist/salary): **61**
Estimated genuine inventory before deep advert review: **~117** (working range **97–136**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO TO BOUNDARY SAMPLE / SCALE PLAUSIBLE**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 97 |
| BORDERLINE | 39 |
| OUT_SPECIALIST | 33 |
| OUT_SALARY | 28 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 54 |
| £30k–£40k | 52 |
| £40k–£50,000 | 29 |
| £25k–£30k | 29 |
| >£50,000 OUT | 28 |
| <£25k | 5 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Sales & Marketing | 104 |
| Advert / Media / Entertainment | 50 |
| I.T. & Communications | 20 |
| Administration | 10 |
| Executive Positions | 6 |
| Retail & Consumer Products | 2 |
| Banking & Financial Services | 2 |
| Consulting & Corporate Strategy | 1 |
| Legal | 1 |
| Healthcare & Medical | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **185**.
Content-unique candidates outside it or unresolved: **12**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 55 | YES |
| Other / Unknown | 11 | NO |
| Surrey | 8 | YES |
| Greater Manchester - Manchester & Salford | 8 | YES |
| West Midlands - Birmingham & Solihull | 8 | YES |
| Berkshire | 7 | YES |
| Kent | 7 | YES |
| Yorkshire - South | 5 | YES |
| Hampshire | 5 | YES |
| Yorkshire - North | 5 | YES |
| Yorkshire - West | 5 | YES |
| Norfolk | 5 | YES |
| Oxfordshire | 4 | YES |
| Sussex | 4 | YES |
| Nottinghamshire | 4 | YES |
| Lincolnshire | 4 | YES |
| Buckinghamshire | 3 | YES |
| Bristol & Bath | 3 | YES |
| Merseyside - Liverpool | 3 | YES |
| Hertfordshire | 3 | YES |
| Northamptonshire | 3 | YES |
| Cambridgeshire | 3 | YES |
| Scotland West - Glasgow | 2 | YES |
| Dorset | 2 | YES |
| Northern Ireland - East | 2 | YES |
| Wales South - Swansea Bay | 2 | YES |
| Wales - West | 2 | YES |
| Essex | 2 | YES |
| North East | 2 | YES |
| Devon | 2 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

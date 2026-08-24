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

Provisional LIKELY_IN: **101**
Provisional BORDERLINE: **49**
Provisional OUT (specialist/salary): **47**
Estimated genuine inventory before deep advert review: **~125** (working range **101–150**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 101 |
| BORDERLINE | 49 |
| OUT_SALARY | 25 |
| OUT_SPECIALIST | 22 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 63 |
| £30k–£40k | 51 |
| £25k–£30k | 29 |
| >£50,000 OUT | 25 |
| £40k–£50,000 | 25 |
| <£25k | 4 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Sales & Marketing | 103 |
| Advert / Media / Entertainment | 53 |
| I.T. & Communications | 20 |
| Administration | 10 |
| Executive Positions | 5 |
| Retail & Consumer Products | 2 |
| Banking & Financial Services | 2 |
| Consulting & Corporate Strategy | 1 |
| Legal | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **176**.
Content-unique candidates outside it or unresolved: **21**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 54 | YES |
| Other / Unknown | 21 | NO |
| Surrey | 9 | YES |
| Greater Manchester - Manchester & Salford | 8 | YES |
| West Midlands - Birmingham & Solihull | 8 | YES |
| Berkshire | 6 | YES |
| Kent | 6 | YES |
| Yorkshire - West | 6 | YES |
| Yorkshire - South | 5 | YES |
| Yorkshire - North | 5 | YES |
| Norfolk | 5 | YES |
| Oxfordshire | 4 | YES |
| Hampshire | 4 | YES |
| Nottinghamshire | 4 | YES |
| Lincolnshire | 4 | YES |
| Sussex | 3 | YES |
| Bristol & Bath | 3 | YES |
| Merseyside - Liverpool | 3 | YES |
| Hertfordshire | 3 | YES |
| Northamptonshire | 3 | YES |
| Cambridgeshire | 3 | YES |
| Dorset | 2 | YES |
| Northern Ireland - East | 2 | YES |
| Wales South - Swansea Bay | 2 | YES |
| Wales - West | 2 | YES |
| Buckinghamshire | 2 | YES |
| Staffordshire | 2 | YES |
| Scotland West - Glasgow | 2 | YES |
| West Midlands - Coventry & Warwickshire | 2 | YES |
| Derbyshire | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

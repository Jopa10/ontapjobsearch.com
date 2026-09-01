# JobG8 Marketing family discovery

Feed: **2026-09-01.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **471**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **471**
Additional cross-reference content duplicates: **11**
Content-unique broad universe: **460**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **225**
Provisional BORDERLINE: **110**
Provisional OUT (specialist/salary): **125**
Estimated genuine inventory before deep advert review: **~280** (working range **225–335**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 225 |
| BORDERLINE | 110 |
| OUT_SALARY | 91 |
| OUT_SPECIALIST | 34 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 150 |
| £30k–£40k | 92 |
| >£50,000 OUT | 89 |
| £25k–£30k | 61 |
| £40k–£50,000 | 57 |
| <£25k | 11 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Sales & Marketing | 407 |
| Advert / Media / Entertainment | 25 |
| I.T. & Communications | 13 |
| Administration | 5 |
| Retail & Consumer Products | 3 |
| Banking & Financial Services | 2 |
| Consulting & Corporate Strategy | 1 |
| Legal | 1 |
| Call Centre / CustomerService | 1 |
| Science & Technology | 1 |
| Executive Positions | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **431**.
Content-unique candidates outside it or unresolved: **29**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 107 | YES |
| Greater Manchester - Manchester & Salford | 32 | YES |
| Other / Unknown | 26 | NO |
| Yorkshire - West | 20 | YES |
| Buckinghamshire | 15 | YES |
| Berkshire | 15 | YES |
| Yorkshire - North | 14 | YES |
| Oxfordshire | 11 | YES |
| Hampshire | 11 | YES |
| Hertfordshire | 11 | YES |
| Surrey | 10 | YES |
| Gloucestershire | 10 | YES |
| Kent | 9 | YES |
| Yorkshire - South | 9 | YES |
| North East | 9 | YES |
| Cambridgeshire | 8 | YES |
| Bristol & Bath | 8 | YES |
| Dorset | 7 | YES |
| Devon | 7 | YES |
| Cheshire - West | 6 | YES |
| Nottinghamshire | 6 | YES |
| Sussex | 6 | YES |
| Essex | 6 | YES |
| West Midlands - Birmingham & Solihull | 5 | YES |
| Cheshire - East | 5 | YES |
| Northamptonshire | 5 | YES |
| Leicestershire | 5 | YES |
| West Midlands - Coventry & Warwickshire | 5 | YES |
| Scotland Central - Edinburgh & Lothians | 4 | YES |
| Lincolnshire | 4 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

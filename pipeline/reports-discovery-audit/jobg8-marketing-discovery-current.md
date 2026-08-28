# JobG8 Marketing family discovery

Feed: **2026-08-28.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **260**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **260**
Additional cross-reference content duplicates: **8**
Content-unique broad universe: **252**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **124**
Provisional BORDERLINE: **55**
Provisional OUT (specialist/salary): **73**
Estimated genuine inventory before deep advert review: **~152** (working range **124–179**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 124 |
| BORDERLINE | 55 |
| OUT_SALARY | 48 |
| OUT_SPECIALIST | 25 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 76 |
| >£50,000 OUT | 47 |
| £30k–£40k | 45 |
| £25k–£30k | 38 |
| £40k–£50,000 | 36 |
| <£25k | 10 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Sales & Marketing | 200 |
| Advert / Media / Entertainment | 26 |
| I.T. & Communications | 8 |
| Administration | 5 |
| Retail & Consumer Products | 5 |
| Consulting & Corporate Strategy | 2 |
| Call Centre / CustomerService | 2 |
| Executive Positions | 1 |
| HR / Recruitment | 1 |
| Legal | 1 |
| Science & Technology | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **232**.
Content-unique candidates outside it or unresolved: **20**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 62 | YES |
| Other / Unknown | 19 | NO |
| Greater Manchester - Manchester & Salford | 18 | YES |
| Berkshire | 9 | YES |
| Yorkshire - West | 9 | YES |
| Hampshire | 8 | YES |
| Oxfordshire | 7 | YES |
| Surrey | 6 | YES |
| Buckinghamshire | 6 | YES |
| North East | 6 | YES |
| Gloucestershire | 6 | YES |
| West Midlands - Birmingham & Solihull | 5 | YES |
| Bristol & Bath | 5 | YES |
| Northern Ireland - East | 4 | YES |
| Sussex | 4 | YES |
| Cambridgeshire | 4 | YES |
| Northamptonshire | 4 | YES |
| Yorkshire - South | 4 | YES |
| Dorset | 3 | YES |
| Wales South - Swansea Bay | 3 | YES |
| Kent | 3 | YES |
| Essex | 3 | YES |
| Lincolnshire | 3 | YES |
| Leicestershire | 3 | YES |
| Cheshire - East | 3 | YES |
| Derbyshire | 3 | YES |
| Lancashire - East | 3 | YES |
| Worcestershire | 3 | YES |
| West Midlands - Coventry & Warwickshire | 3 | YES |
| Hertfordshire | 3 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

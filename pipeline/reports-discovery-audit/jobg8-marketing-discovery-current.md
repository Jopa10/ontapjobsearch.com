# JobG8 Marketing family discovery

Feed: **2026-08-27.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **226**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **226**
Additional cross-reference content duplicates: **8**
Content-unique broad universe: **218**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **108**
Provisional BORDERLINE: **44**
Provisional OUT (specialist/salary): **66**
Estimated genuine inventory before deep advert review: **~130** (working range **108–152**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 108 |
| BORDERLINE | 44 |
| OUT_SALARY | 42 |
| OUT_SPECIALIST | 24 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 67 |
| £30k–£40k | 45 |
| >£50,000 OUT | 42 |
| £40k–£50,000 | 29 |
| £25k–£30k | 27 |
| <£25k | 8 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Sales & Marketing | 163 |
| Advert / Media / Entertainment | 29 |
| I.T. & Communications | 8 |
| Administration | 6 |
| Retail & Consumer Products | 5 |
| Consulting & Corporate Strategy | 1 |
| Banking & Financial Services | 1 |
| Executive Positions | 1 |
| HR / Recruitment | 1 |
| Legal | 1 |
| Science & Technology | 1 |
| Call Centre / CustomerService | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **200**.
Content-unique candidates outside it or unresolved: **18**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 59 | YES |
| Other / Unknown | 17 | NO |
| Greater Manchester - Manchester & Salford | 15 | YES |
| Berkshire | 12 | YES |
| Yorkshire - West | 8 | YES |
| Oxfordshire | 7 | YES |
| West Midlands - Birmingham & Solihull | 6 | YES |
| Surrey | 5 | YES |
| Buckinghamshire | 5 | YES |
| North East | 5 | YES |
| Leicestershire | 5 | YES |
| Northern Ireland - East | 4 | YES |
| Hampshire | 4 | YES |
| West Midlands - Coventry & Warwickshire | 4 | YES |
| Yorkshire - South | 3 | YES |
| Wales South - Swansea Bay | 3 | YES |
| Dorset | 3 | YES |
| Sussex | 3 | YES |
| Kent | 3 | YES |
| Lincolnshire | 3 | YES |
| Cambridgeshire | 3 | YES |
| Yorkshire - North | 3 | YES |
| Cheshire - East | 3 | YES |
| Lancashire - East | 3 | YES |
| Wales - West | 2 | YES |
| Essex | 2 | YES |
| Norfolk | 2 | YES |
| Northamptonshire | 2 | YES |
| Gloucestershire | 2 | YES |
| Worcestershire | 2 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

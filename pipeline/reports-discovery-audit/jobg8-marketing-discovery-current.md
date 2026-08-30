# JobG8 Marketing family discovery

Feed: **2026-08-30.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **213**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **213**
Additional cross-reference content duplicates: **8**
Content-unique broad universe: **205**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **101**
Provisional BORDERLINE: **49**
Provisional OUT (specialist/salary): **55**
Estimated genuine inventory before deep advert review: **~125** (working range **101–150**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 101 |
| BORDERLINE | 49 |
| OUT_SALARY | 35 |
| OUT_SPECIALIST | 20 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 69 |
| £30k–£40k | 43 |
| >£50,000 OUT | 34 |
| £40k–£50,000 | 28 |
| £25k–£30k | 28 |
| <£25k | 3 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Sales & Marketing | 167 |
| Advert / Media / Entertainment | 17 |
| I.T. & Communications | 8 |
| Administration | 4 |
| Retail & Consumer Products | 4 |
| Consulting & Corporate Strategy | 1 |
| Executive Positions | 1 |
| Legal | 1 |
| Call Centre / CustomerService | 1 |
| Science & Technology | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **191**.
Content-unique candidates outside it or unresolved: **14**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 45 | YES |
| Greater Manchester - Manchester & Salford | 13 | YES |
| Other / Unknown | 13 | NO |
| Yorkshire - West | 9 | YES |
| Oxfordshire | 8 | YES |
| Berkshire | 7 | YES |
| Hampshire | 6 | YES |
| Buckinghamshire | 6 | YES |
| North East | 5 | YES |
| Cambridgeshire | 5 | YES |
| West Midlands - Birmingham & Solihull | 5 | YES |
| Gloucestershire | 5 | YES |
| Bristol & Bath | 5 | YES |
| Northern Ireland - East | 4 | YES |
| Cheshire - West | 4 | YES |
| Surrey | 4 | YES |
| Yorkshire - North | 4 | YES |
| Leicestershire | 4 | YES |
| Nottinghamshire | 3 | YES |
| Sussex | 3 | YES |
| Kent | 3 | YES |
| Essex | 3 | YES |
| Lincolnshire | 3 | YES |
| Yorkshire - South | 3 | YES |
| West Midlands - Coventry & Warwickshire | 3 | YES |
| Dorset | 2 | YES |
| Wales South - Swansea Bay | 2 | YES |
| Wales - West | 2 | YES |
| Staffordshire | 2 | YES |
| Hertfordshire | 2 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

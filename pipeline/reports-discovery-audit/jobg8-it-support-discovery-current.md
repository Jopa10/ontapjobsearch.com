# JobG8 IT Support family discovery

Feed: **2026-09-22.xlsx**
Jobs in feed: **17,340**
Raw broad possible universe before exclusions/dedupe: **58**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **58**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **58**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **27**
Provisional BORDERLINE: **20**
Provisional OUT (specialist/salary): **11**
Estimated genuine inventory before deep advert review: **~37** (working range **27–47**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 27 |
| BORDERLINE | 20 |
| OUT_SPECIALIST | 6 |
| OUT_SALARY | 5 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 28 |
| £25k–£30k | 12 |
| £30k–£40k | 7 |
| £40k–£50,000 | 7 |
| >£50,000 OUT | 4 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| I.T. & Communications | 54 |
| Legal | 1 |
| Transport & Logistics | 1 |
| HR / Recruitment | 1 |
| Healthcare & Medical | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **57**.
Content-unique candidates outside it or unresolved: **1**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 11 | YES |
| Surrey | 5 | YES |
| Scotland Central - Edinburgh & Lothians | 3 | YES |
| Greater Manchester - Manchester & Salford | 3 | YES |
| Merseyside - Liverpool | 2 | YES |
| West Midlands - Birmingham & Solihull | 2 | YES |
| Hampshire | 2 | YES |
| Buckinghamshire | 2 | YES |
| Hertfordshire | 2 | YES |
| Sussex | 2 | YES |
| Northern Ireland - East | 2 | YES |
| Yorkshire - West | 2 | YES |
| Bedfordshire | 2 | YES |
| Worcestershire | 1 | YES |
| Other / Unknown | 1 | NO |
| Northamptonshire | 1 | YES |
| Cheshire - West | 1 | YES |
| Berkshire | 1 | YES |
| North East | 1 | YES |
| Gloucestershire | 1 | YES |
| Essex | 1 | YES |
| Derbyshire | 1 | YES |
| Shropshire | 1 | YES |
| Scotland Central - Falkirk & Stirling | 1 | YES |
| Yorkshire - North | 1 | YES |
| Yorkshire - South | 1 | YES |
| Oxfordshire | 1 | YES |
| Yorkshire - East | 1 | YES |
| Bristol & Bath | 1 | YES |
| Wales South - Cardiff & Vale | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

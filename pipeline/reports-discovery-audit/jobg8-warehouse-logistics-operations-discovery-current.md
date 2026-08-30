# JobG8 Warehouse & Logistics Operations family discovery

Feed: **2026-08-30.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **82**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **82**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **82**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **17**
Provisional BORDERLINE: **19**
Provisional OUT (specialist/salary): **46**
Estimated genuine inventory before deep advert review: **~27** (working range **17–36**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 28 |
| BORDERLINE | 19 |
| OUT_SALARY | 18 |
| LIKELY_IN | 17 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £25k–£30k | 23 |
| missing/unknown | 20 |
| >£45,000 OUT | 18 |
| £30k–£40k | 13 |
| <£25k | 4 |
| £40k–£45,000 | 4 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Administration | 29 |
| Sales & Marketing | 13 |
| Banking & Financial Services | 10 |
| I.T. & Communications | 10 |
| Executive Positions | 7 |
| Call Centre / CustomerService | 3 |
| Advert / Media / Entertainment | 2 |
| Accounting | 2 |
| Real Estate & Property | 1 |
| Healthcare & Medical | 1 |
| Retail & Consumer Products | 1 |
| Consulting & Corporate Strategy | 1 |
| Legal | 1 |
| HR / Recruitment | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **74**.
Content-unique candidates outside it or unresolved: **8**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 7 | YES |
| Other / Unknown | 6 | NO |
| Berkshire | 5 | YES |
| Kent | 4 | YES |
| Staffordshire | 4 | YES |
| Essex | 3 | YES |
| West Midlands - Black Country | 3 | YES |
| Derbyshire | 3 | YES |
| Leicestershire | 3 | YES |
| Scotland West - Glasgow | 3 | YES |
| Yorkshire - West | 3 | YES |
| Buckinghamshire | 3 | YES |
| Somerset | 2 | YES |
| Lincolnshire | 2 | YES |
| West Midlands - Coventry & Warwickshire | 2 | YES |
| Hampshire | 2 | YES |
| East Midlands | 2 | NO |
| Northamptonshire | 2 | YES |
| Cambridgeshire | 2 | YES |
| Bristol & Bath | 2 | YES |
| Yorkshire - North | 2 | YES |
| Cumbria - South | 1 | YES |
| Lancashire - East | 1 | YES |
| Scotland West - Lanarkshire | 1 | YES |
| North East | 1 | YES |
| Shropshire | 1 | YES |
| Oxfordshire | 1 | YES |
| Scotland Central - Tayside | 1 | YES |
| Gloucestershire | 1 | YES |
| Worcestershire | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

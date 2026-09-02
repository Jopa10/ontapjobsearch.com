# JobG8 Warehouse & Logistics Operations family discovery

Feed: **2026-09-02.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **83**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **83**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **83**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **20**
Provisional BORDERLINE: **22**
Provisional OUT (specialist/salary): **41**
Estimated genuine inventory before deep advert review: **~31** (working range **20–42**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 28 |
| BORDERLINE | 22 |
| LIKELY_IN | 20 |
| OUT_SALARY | 13 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 29 |
| £25k–£30k | 22 |
| >£45,000 OUT | 13 |
| £30k–£40k | 11 |
| £40k–£45,000 | 6 |
| <£25k | 2 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Administration | 33 |
| Sales & Marketing | 21 |
| I.T. & Communications | 8 |
| Call Centre / CustomerService | 5 |
| Retail & Consumer Products | 3 |
| Banking & Financial Services | 3 |
| HR / Recruitment | 2 |
| Executive Positions | 2 |
| Real Estate & Property | 1 |
| Science & Technology | 1 |
| Legal | 1 |
| Insurance & Superannuation | 1 |
| Accounting | 1 |
| Advert / Media / Entertainment | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **74**.
Content-unique candidates outside it or unresolved: **9**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 9 | YES |
| Other / Unknown | 7 | NO |
| Staffordshire | 5 | YES |
| Kent | 5 | YES |
| Leicestershire | 4 | YES |
| West Midlands - Coventry & Warwickshire | 3 | YES |
| Berkshire | 3 | YES |
| Northamptonshire | 3 | YES |
| Cambridgeshire | 3 | YES |
| Yorkshire - North | 3 | YES |
| West Midlands - Black Country | 2 | YES |
| West Midlands - Birmingham & Solihull | 2 | YES |
| Greater Manchester - Manchester & Salford | 2 | YES |
| East Midlands | 2 | NO |
| Oxfordshire | 2 | YES |
| Essex | 2 | YES |
| Surrey | 2 | YES |
| Yorkshire - West | 2 | YES |
| Yorkshire - South | 2 | YES |
| Nottinghamshire | 2 | YES |
| Merseyside - Liverpool | 2 | YES |
| Lincolnshire | 1 | YES |
| Scotland West - Glasgow | 1 | YES |
| Buckinghamshire | 1 | YES |
| Scotland Central - Tayside | 1 | YES |
| Gloucestershire | 1 | YES |
| Bristol & Bath | 1 | YES |
| Wales South - Swansea Bay | 1 | YES |
| Devon | 1 | YES |
| Northern Ireland - East | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

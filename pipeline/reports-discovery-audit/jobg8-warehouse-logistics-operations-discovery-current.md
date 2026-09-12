# JobG8 Warehouse & Logistics Operations family discovery

Feed: **2026-09-12.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **69**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **69**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **69**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **19**
Provisional BORDERLINE: **20**
Provisional OUT (specialist/salary): **30**
Estimated genuine inventory before deep advert review: **~29** (working range **19–39**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| BORDERLINE | 20 |
| LIKELY_IN | 19 |
| OUT_SPECIALIST | 17 |
| OUT_SALARY | 13 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £25k–£30k | 23 |
| missing/unknown | 17 |
| >£45,000 OUT | 13 |
| £30k–£40k | 12 |
| <£25k | 2 |
| £40k–£45,000 | 2 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Administration | 26 |
| I.T. & Communications | 11 |
| Call Centre / CustomerService | 9 |
| Sales & Marketing | 6 |
| Retail & Consumer Products | 4 |
| Banking & Financial Services | 3 |
| Real Estate & Property | 3 |
| Executive Positions | 2 |
| Accounting | 2 |
| Legal | 1 |
| Advert / Media / Entertainment | 1 |
| HR / Recruitment | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **60**.
Content-unique candidates outside it or unresolved: **9**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 9 | YES |
| Other / Unknown | 8 | NO |
| Yorkshire - West | 4 | YES |
| Oxfordshire | 3 | YES |
| Surrey | 3 | YES |
| Staffordshire | 3 | YES |
| Kent | 3 | YES |
| West Midlands - Birmingham & Solihull | 3 | YES |
| Northamptonshire | 2 | YES |
| Cambridgeshire | 2 | YES |
| Merseyside - Liverpool | 2 | YES |
| Yorkshire - North | 2 | YES |
| Bristol & Bath | 2 | YES |
| Buckinghamshire | 2 | YES |
| Yorkshire - South | 2 | YES |
| Greater Manchester - Manchester & Salford | 2 | YES |
| North East | 2 | YES |
| Essex | 1 | YES |
| Nottinghamshire | 1 | YES |
| Somerset | 1 | YES |
| Scotland Central - Fife | 1 | YES |
| Wiltshire | 1 | YES |
| West Midlands - Coventry & Warwickshire | 1 | YES |
| Berkshire | 1 | YES |
| Scotland West - Lanarkshire | 1 | YES |
| Hampshire | 1 | YES |
| Lincolnshire | 1 | YES |
| Scotland Central - Tayside | 1 | YES |
| East Midlands | 1 | NO |
| Scotland Central - Edinburgh & Lothians | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

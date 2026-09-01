# JobG8 IT Support family discovery

Feed: **2026-09-01.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **215**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **215**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **215**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **117**
Provisional BORDERLINE: **69**
Provisional OUT (specialist/salary): **29**
Estimated genuine inventory before deep advert review: **~151** (working range **117–186**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 117 |
| BORDERLINE | 69 |
| OUT_SALARY | 18 |
| OUT_SPECIALIST | 11 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 101 |
| £30k–£40k | 52 |
| £25k–£30k | 29 |
| >£50,000 OUT | 18 |
| £40k–£50,000 | 13 |
| <£25k | 2 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| I.T. & Communications | 188 |
| Administration | 17 |
| Call Centre / CustomerService | 5 |
| Real Estate & Property | 3 |
| Sales & Marketing | 1 |
| Accounting | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **206**.
Content-unique candidates outside it or unresolved: **9**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 44 | YES |
| Surrey | 13 | YES |
| West Midlands - Birmingham & Solihull | 11 | YES |
| Hampshire | 10 | YES |
| Essex | 10 | YES |
| Berkshire | 9 | YES |
| North East | 9 | YES |
| Hertfordshire | 8 | YES |
| Merseyside - Liverpool | 8 | YES |
| Bristol & Bath | 8 | YES |
| Yorkshire - West | 6 | YES |
| Kent | 6 | YES |
| Other / Unknown | 6 | NO |
| Greater Manchester - Manchester & Salford | 6 | YES |
| Gloucestershire | 4 | YES |
| Sussex | 4 | YES |
| Lincolnshire | 4 | YES |
| Worcestershire | 3 | YES |
| Buckinghamshire | 3 | YES |
| Cumbria - West | 3 | YES |
| Northamptonshire | 3 | YES |
| Yorkshire - South | 3 | YES |
| Northern Ireland - East | 3 | YES |
| Dorset | 2 | YES |
| Scotland West - Glasgow | 2 | YES |
| Nottinghamshire | 2 | YES |
| Leicestershire | 2 | YES |
| Scotland Central - Edinburgh & Lothians | 2 | YES |
| Oxfordshire | 2 | YES |
| Suffolk | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

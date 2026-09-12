# JobG8 IT Support family discovery

Feed: **2026-09-12.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **81**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **81**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **81**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **41**
Provisional BORDERLINE: **28**
Provisional OUT (specialist/salary): **12**
Estimated genuine inventory before deep advert review: **~55** (working range **41–69**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 41 |
| BORDERLINE | 28 |
| OUT_SPECIALIST | 7 |
| OUT_SALARY | 5 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 36 |
| £30k–£40k | 18 |
| £25k–£30k | 12 |
| £40k–£50,000 | 8 |
| >£50,000 OUT | 5 |
| <£25k | 2 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| I.T. & Communications | 59 |
| Administration | 11 |
| Call Centre / CustomerService | 5 |
| Real Estate & Property | 2 |
| Sales & Marketing | 1 |
| Accounting | 1 |
| Executive Positions | 1 |
| Legal | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **75**.
Content-unique candidates outside it or unresolved: **6**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 15 | YES |
| Northern Ireland - East | 11 | YES |
| Surrey | 6 | YES |
| Yorkshire - West | 6 | YES |
| Other / Unknown | 6 | NO |
| Essex | 4 | YES |
| Greater Manchester - Manchester & Salford | 4 | YES |
| Hampshire | 3 | YES |
| Berkshire | 3 | YES |
| Kent | 2 | YES |
| Merseyside - Liverpool | 2 | YES |
| West Midlands - Birmingham & Solihull | 2 | YES |
| Northern Ireland - West | 2 | YES |
| Buckinghamshire | 2 | YES |
| West Midlands - Black Country | 1 | YES |
| Scotland Central - Edinburgh & Lothians | 1 | YES |
| Worcestershire | 1 | YES |
| North East | 1 | YES |
| Northamptonshire | 1 | YES |
| Cheshire - West | 1 | YES |
| Bedfordshire | 1 | YES |
| Gloucestershire | 1 | YES |
| Derbyshire | 1 | YES |
| Bristol & Bath | 1 | YES |
| Shropshire | 1 | YES |
| Cumbria - West | 1 | YES |
| Sussex | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

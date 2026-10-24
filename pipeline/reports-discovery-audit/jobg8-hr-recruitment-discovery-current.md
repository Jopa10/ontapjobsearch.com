# JobG8 HR / Recruitment family discovery

Feed: **2026-10-24.xlsx**
Jobs in feed: **20,000**
Raw broad possible universe before exclusions/dedupe: **1,181**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **1,181**
Additional cross-reference content duplicates: **14**
Content-unique broad universe: **1,167**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **135**
Provisional BORDERLINE: **226**
Provisional OUT (specialist/salary): **806**
Estimated genuine inventory before deep advert review: **~248** (working range **135–361**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 667 |
| BORDERLINE | 226 |
| OUT_SALARY | 139 |
| LIKELY_IN | 135 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £30k–£40k | 373 |
| £25k–£30k | 300 |
| missing/unknown | 203 |
| >£50,000 OUT | 138 |
| £40k–£50,000 | 124 |
| <£25k | 29 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| HR / Recruitment | 1,055 |
| Administration | 44 |
| Accounting | 24 |
| Sales & Marketing | 23 |
| Banking & Financial Services | 5 |
| Real Estate & Property | 3 |
| Government & Defence | 3 |
| Community & Sport | 3 |
| I.T. & Communications | 2 |
| Call Centre / CustomerService | 2 |
| Advert / Media / Entertainment | 1 |
| Education | 1 |
| Insurance & Superannuation | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **1,012**.
Content-unique candidates outside it or unresolved: **155**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 163 | YES |
| Other / Unknown | 134 | NO |
| Greater Manchester - Manchester & Salford | 52 | YES |
| Hampshire | 51 | YES |
| West Midlands - Birmingham & Solihull | 42 | YES |
| Devon | 40 | YES |
| Yorkshire - West | 33 | YES |
| Surrey | 32 | YES |
| Bristol & Bath | 32 | YES |
| Nottinghamshire | 31 | YES |
| Berkshire | 30 | YES |
| Essex | 26 | YES |
| Sussex | 25 | YES |
| Kent | 24 | YES |
| North East | 21 | YES |
| Leicestershire | 21 | YES |
| Buckinghamshire | 21 | YES |
| Suffolk | 20 | YES |
| Hertfordshire | 20 | YES |
| Gloucestershire | 20 | YES |
| West Midlands - Coventry & Warwickshire | 18 | YES |
| Oxfordshire | 18 | YES |
| West Midlands | 18 | NO |
| West Midlands - Black Country | 17 | YES |
| Derbyshire | 17 | YES |
| Staffordshire | 16 | YES |
| Yorkshire - South | 16 | YES |
| Northamptonshire | 15 | YES |
| Scotland West - Glasgow | 13 | YES |
| Dorset | 12 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

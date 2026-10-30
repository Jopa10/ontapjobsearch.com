# JobG8 HR / Recruitment family discovery

Feed: **2026-10-30.xlsx**
Jobs in feed: **20,000**
Raw broad possible universe before exclusions/dedupe: **1,223**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **1,223**
Additional cross-reference content duplicates: **14**
Content-unique broad universe: **1,209**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **132**
Provisional BORDERLINE: **223**
Provisional OUT (specialist/salary): **854**
Estimated genuine inventory before deep advert review: **~244** (working range **132–355**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 703 |
| BORDERLINE | 223 |
| OUT_SALARY | 151 |
| LIKELY_IN | 132 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £30k–£40k | 401 |
| £25k–£30k | 300 |
| missing/unknown | 213 |
| >£50,000 OUT | 150 |
| £40k–£50,000 | 121 |
| <£25k | 24 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| HR / Recruitment | 1,112 |
| Administration | 34 |
| Sales & Marketing | 21 |
| Accounting | 19 |
| Banking & Financial Services | 5 |
| Real Estate & Property | 5 |
| I.T. & Communications | 3 |
| Government & Defence | 2 |
| Community & Sport | 2 |
| Call Centre / CustomerService | 2 |
| Advert / Media / Entertainment | 1 |
| Insurance & Superannuation | 1 |
| Healthcare & Medical | 1 |
| Education | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **1,032**.
Content-unique candidates outside it or unresolved: **177**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 158 | YES |
| Other / Unknown | 153 | NO |
| Greater Manchester - Manchester & Salford | 54 | YES |
| Hampshire | 53 | YES |
| West Midlands - Birmingham & Solihull | 42 | YES |
| Yorkshire - West | 40 | YES |
| Devon | 39 | YES |
| Leicestershire | 29 | YES |
| Bristol & Bath | 28 | YES |
| Surrey | 27 | YES |
| Nottinghamshire | 27 | YES |
| Buckinghamshire | 26 | YES |
| Essex | 25 | YES |
| Berkshire | 25 | YES |
| North East | 25 | YES |
| Sussex | 24 | YES |
| Staffordshire | 21 | YES |
| Gloucestershire | 21 | YES |
| Kent | 19 | YES |
| West Midlands | 19 | NO |
| Suffolk | 18 | YES |
| Hertfordshire | 18 | YES |
| Northamptonshire | 17 | YES |
| Yorkshire - South | 17 | YES |
| Oxfordshire | 17 | YES |
| West Midlands - Black Country | 16 | YES |
| West Midlands - Coventry & Warwickshire | 16 | YES |
| Derbyshire | 15 | YES |
| Northern Ireland - East | 13 | YES |
| Bedfordshire | 13 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

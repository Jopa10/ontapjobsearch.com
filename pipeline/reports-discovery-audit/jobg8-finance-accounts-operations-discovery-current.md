# JobG8 Accounts & Finance Operations family discovery

Feed: **2026-10-30.xlsx**
Jobs in feed: **20,000**
Raw broad possible universe before exclusions/dedupe: **2,640**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **2,640**
Additional cross-reference content duplicates: **72**
Content-unique broad universe: **2,568**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **756**
Provisional BORDERLINE: **0**
Provisional OUT (specialist/salary): **1,812**
Estimated genuine inventory before deep advert review: **~756** (working range **756–756**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 1,022 |
| LIKELY_IN | 756 |
| OUT_SALARY | 699 |
| OUT_BOUNDARY | 91 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 761 |
| >£45,000 OUT | 699 |
| £30k–£40k | 580 |
| £25k–£30k | 400 |
| £40k–£45,000 | 94 |
| <£25k | 34 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Accounting | 1,752 |
| Sales & Marketing | 411 |
| Insurance & Superannuation | 158 |
| Banking & Financial Services | 71 |
| Administration | 68 |
| HR / Recruitment | 35 |
| I.T. & Communications | 19 |
| Legal | 17 |
| Call Centre / CustomerService | 15 |
| Government & Defence | 5 |
| Real Estate & Property | 4 |
| Transport & Logistics | 4 |
| Advert / Media / Entertainment | 4 |
| Community & Sport | 3 |
| Healthcare & Medical | 1 |
| Education | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **2,313**.
Content-unique candidates outside it or unresolved: **255**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 355 | YES |
| Other / Unknown | 224 | NO |
| Greater Manchester - Manchester & Salford | 99 | YES |
| Hampshire | 96 | YES |
| Surrey | 82 | YES |
| Yorkshire - West | 75 | YES |
| Kent | 74 | YES |
| West Midlands - Birmingham & Solihull | 73 | YES |
| Hertfordshire | 71 | YES |
| West Midlands - Coventry & Warwickshire | 71 | YES |
| Leicestershire | 62 | YES |
| Berkshire | 60 | YES |
| North East | 58 | YES |
| Sussex | 56 | YES |
| Oxfordshire | 53 | YES |
| Buckinghamshire | 50 | YES |
| Bristol & Bath | 49 | YES |
| Essex | 46 | YES |
| Dorset | 45 | YES |
| Gloucestershire | 44 | YES |
| Norfolk | 42 | YES |
| Yorkshire - South | 42 | YES |
| Nottinghamshire | 41 | YES |
| Northamptonshire | 39 | YES |
| Merseyside - Liverpool | 37 | YES |
| Suffolk | 37 | YES |
| Worcestershire | 36 | YES |
| Devon | 35 | YES |
| Cambridgeshire | 33 | YES |
| Staffordshire | 31 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

# JobG8 Accounts & Finance Operations family discovery

Feed: **2026-09-22.xlsx**
Jobs in feed: **17,340**
Raw broad possible universe before exclusions/dedupe: **2,457**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **2,457**
Additional cross-reference content duplicates: **27**
Content-unique broad universe: **2,430**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **727**
Provisional BORDERLINE: **0**
Provisional OUT (specialist/salary): **1,703**
Estimated genuine inventory before deep advert review: **~727** (working range **727–727**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 1,013 |
| LIKELY_IN | 727 |
| OUT_SALARY | 611 |
| OUT_BOUNDARY | 79 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 1,308 |
| >£45,000 OUT | 610 |
| £30k–£40k | 301 |
| £25k–£30k | 138 |
| £40k–£45,000 | 59 |
| <£25k | 14 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Accounting | 1,879 |
| Banking & Financial Services | 305 |
| Insurance & Superannuation | 98 |
| Sales & Marketing | 66 |
| I.T. & Communications | 25 |
| Legal | 22 |
| HR / Recruitment | 20 |
| Education | 5 |
| Transport & Logistics | 2 |
| Consulting & Corporate Strategy | 2 |
| Healthcare & Medical | 2 |
| Call Centre / CustomerService | 1 |
| Administration | 1 |
| Real Estate & Property | 1 |
| Community & Sport | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **2,337**.
Content-unique candidates outside it or unresolved: **93**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 434 | YES |
| Yorkshire - West | 104 | YES |
| Kent | 86 | YES |
| Greater Manchester - Manchester & Salford | 82 | YES |
| Surrey | 71 | YES |
| Sussex | 69 | YES |
| Essex | 66 | YES |
| Hampshire | 59 | YES |
| Bristol & Bath | 57 | YES |
| West Midlands - Birmingham & Solihull | 56 | YES |
| Devon | 53 | YES |
| Hertfordshire | 51 | YES |
| Berkshire | 51 | YES |
| Other / Unknown | 50 | NO |
| North East | 47 | YES |
| Yorkshire - North | 46 | YES |
| Cambridgeshire | 46 | YES |
| West Midlands - Coventry & Warwickshire | 44 | YES |
| Merseyside - Liverpool | 41 | YES |
| Buckinghamshire | 41 | YES |
| Leicestershire | 41 | YES |
| Oxfordshire | 40 | YES |
| Wiltshire | 39 | YES |
| Yorkshire - South | 39 | YES |
| Dorset | 38 | YES |
| Suffolk | 38 | YES |
| Gloucestershire | 34 | YES |
| Nottinghamshire | 34 | YES |
| Northamptonshire | 32 | YES |
| Cheshire - Warrington & Halton | 30 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

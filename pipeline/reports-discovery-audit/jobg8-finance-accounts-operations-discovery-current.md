# JobG8 Accounts & Finance Operations family discovery

Feed: **2026-10-24.xlsx**
Jobs in feed: **20,000**
Raw broad possible universe before exclusions/dedupe: **3,036**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **3,036**
Additional cross-reference content duplicates: **96**
Content-unique broad universe: **2,940**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **930**
Provisional BORDERLINE: **0**
Provisional OUT (specialist/salary): **2,010**
Estimated genuine inventory before deep advert review: **~930** (working range **930–930**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 1,157 |
| LIKELY_IN | 930 |
| OUT_SALARY | 744 |
| OUT_BOUNDARY | 109 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 962 |
| >£45,000 OUT | 743 |
| £30k–£40k | 655 |
| £25k–£30k | 444 |
| £40k–£45,000 | 97 |
| <£25k | 39 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Accounting | 2,179 |
| Sales & Marketing | 421 |
| Insurance & Superannuation | 105 |
| Administration | 73 |
| Banking & Financial Services | 62 |
| HR / Recruitment | 31 |
| I.T. & Communications | 19 |
| Call Centre / CustomerService | 17 |
| Legal | 12 |
| Government & Defence | 6 |
| Real Estate & Property | 5 |
| Advert / Media / Entertainment | 4 |
| Transport & Logistics | 4 |
| Community & Sport | 2 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **2,649**.
Content-unique candidates outside it or unresolved: **291**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 440 | YES |
| Other / Unknown | 251 | NO |
| Hampshire | 113 | YES |
| Greater Manchester - Manchester & Salford | 94 | YES |
| Surrey | 89 | YES |
| West Midlands - Birmingham & Solihull | 87 | YES |
| Kent | 83 | YES |
| Hertfordshire | 82 | YES |
| West Midlands - Coventry & Warwickshire | 81 | YES |
| Yorkshire - West | 78 | YES |
| Sussex | 73 | YES |
| Berkshire | 73 | YES |
| Leicestershire | 68 | YES |
| Oxfordshire | 65 | YES |
| North East | 62 | YES |
| Essex | 58 | YES |
| Buckinghamshire | 55 | YES |
| Nottinghamshire | 53 | YES |
| Bristol & Bath | 51 | YES |
| Gloucestershire | 50 | YES |
| Norfolk | 47 | YES |
| Dorset | 46 | YES |
| Worcestershire | 46 | YES |
| Yorkshire - South | 45 | YES |
| Merseyside - Liverpool | 38 | YES |
| Cambridgeshire | 38 | YES |
| Devon | 38 | YES |
| Northamptonshire | 38 | YES |
| Suffolk | 35 | YES |
| Cheshire - Warrington & Halton | 33 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

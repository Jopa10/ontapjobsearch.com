# JobG8 Accounts & Finance Operations family discovery

Feed: **2026-09-21.xlsx**
Jobs in feed: **17,785**
Raw broad possible universe before exclusions/dedupe: **2,467**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **2,467**
Additional cross-reference content duplicates: **27**
Content-unique broad universe: **2,440**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **738**
Provisional BORDERLINE: **0**
Provisional OUT (specialist/salary): **1,702**
Estimated genuine inventory before deep advert review: **~738** (working range **738–738**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 1,019 |
| LIKELY_IN | 738 |
| OUT_SALARY | 606 |
| OUT_BOUNDARY | 77 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 1,315 |
| >£45,000 OUT | 605 |
| £30k–£40k | 304 |
| £25k–£30k | 142 |
| £40k–£45,000 | 60 |
| <£25k | 14 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Accounting | 1,882 |
| Banking & Financial Services | 311 |
| Insurance & Superannuation | 91 |
| Sales & Marketing | 64 |
| I.T. & Communications | 33 |
| Legal | 22 |
| HR / Recruitment | 20 |
| Education | 5 |
| Transport & Logistics | 2 |
| Consulting & Corporate Strategy | 2 |
| Healthcare & Medical | 2 |
| Executive Positions | 2 |
| Call Centre / CustomerService | 1 |
| Administration | 1 |
| Real Estate & Property | 1 |
| Community & Sport | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **2,345**.
Content-unique candidates outside it or unresolved: **95**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 450 | YES |
| Yorkshire - West | 101 | YES |
| Kent | 87 | YES |
| Greater Manchester - Manchester & Salford | 78 | YES |
| Surrey | 72 | YES |
| Sussex | 70 | YES |
| Essex | 66 | YES |
| Bristol & Bath | 59 | YES |
| Hampshire | 57 | YES |
| West Midlands - Birmingham & Solihull | 56 | YES |
| Berkshire | 54 | YES |
| Other / Unknown | 53 | NO |
| Hertfordshire | 52 | YES |
| Devon | 49 | YES |
| North East | 48 | YES |
| Yorkshire - North | 47 | YES |
| Cambridgeshire | 45 | YES |
| West Midlands - Coventry & Warwickshire | 45 | YES |
| Buckinghamshire | 43 | YES |
| Merseyside - Liverpool | 41 | YES |
| Leicestershire | 41 | YES |
| Oxfordshire | 40 | YES |
| Dorset | 38 | YES |
| Wiltshire | 38 | YES |
| Yorkshire - South | 38 | YES |
| Suffolk | 37 | YES |
| Gloucestershire | 35 | YES |
| Nottinghamshire | 34 | YES |
| Northamptonshire | 31 | YES |
| Cheshire - Warrington & Halton | 30 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

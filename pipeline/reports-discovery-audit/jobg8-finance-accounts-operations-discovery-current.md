# JobG8 Accounts & Finance Operations family discovery

Feed: **2026-08-31.xlsx**
Jobs in feed: **5,354**
Raw broad possible universe before exclusions/dedupe: **197**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **197**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **197**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **54**
Provisional BORDERLINE: **0**
Provisional OUT (specialist/salary): **143**
Estimated genuine inventory before deep advert review: **~54** (working range **54–54**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 86 |
| LIKELY_IN | 54 |
| OUT_SALARY | 46 |
| OUT_BOUNDARY | 11 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 55 |
| >£45,000 OUT | 46 |
| £30k–£40k | 46 |
| £25k–£30k | 36 |
| £40k–£45,000 | 8 |
| <£25k | 6 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Accounting | 49 |
| I.T. & Communications | 41 |
| Administration | 40 |
| Banking & Financial Services | 21 |
| Sales & Marketing | 20 |
| Advert / Media / Entertainment | 7 |
| HR / Recruitment | 7 |
| Legal | 4 |
| Consulting & Corporate Strategy | 2 |
| Real Estate & Property | 2 |
| Retail & Consumer Products | 2 |
| Executive Positions | 1 |
| Healthcare & Medical | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **168**.
Content-unique candidates outside it or unresolved: **29**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 43 | YES |
| Other / Unknown | 28 | NO |
| Sussex | 9 | YES |
| Greater Manchester - Manchester & Salford | 8 | YES |
| Bristol & Bath | 7 | YES |
| West Midlands - Birmingham & Solihull | 6 | YES |
| Surrey | 5 | YES |
| Derbyshire | 5 | YES |
| Berkshire | 5 | YES |
| Staffordshire | 5 | YES |
| Somerset | 4 | YES |
| Yorkshire - West | 4 | YES |
| Hampshire | 4 | YES |
| Buckinghamshire | 4 | YES |
| Hertfordshire | 4 | YES |
| Northern Ireland - East | 3 | YES |
| Northamptonshire | 3 | YES |
| Cambridgeshire | 3 | YES |
| Kent | 3 | YES |
| Oxfordshire | 3 | YES |
| Yorkshire - East | 3 | YES |
| Devon | 3 | YES |
| Essex | 2 | YES |
| Cheshire - Warrington & Halton | 2 | YES |
| Gloucestershire | 2 | YES |
| Nottinghamshire | 2 | YES |
| Leicestershire | 2 | YES |
| Scotland West - Glasgow | 2 | YES |
| West Midlands - Black Country | 2 | YES |
| Shropshire | 2 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

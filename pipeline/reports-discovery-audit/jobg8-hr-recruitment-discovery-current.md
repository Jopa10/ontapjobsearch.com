# JobG8 HR / Recruitment family discovery

Feed: **2026-08-31.xlsx**
Jobs in feed: **5,354**
Raw broad possible universe before exclusions/dedupe: **142**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **142**
Additional cross-reference content duplicates: **1**
Content-unique broad universe: **141**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **34**
Provisional BORDERLINE: **26**
Provisional OUT (specialist/salary): **81**
Estimated genuine inventory before deep advert review: **~47** (working range **34–60**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 69 |
| LIKELY_IN | 34 |
| BORDERLINE | 26 |
| OUT_SALARY | 12 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £30k–£40k | 48 |
| £25k–£30k | 44 |
| missing/unknown | 25 |
| >£50,000 OUT | 12 |
| £40k–£50,000 | 8 |
| <£25k | 4 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| HR / Recruitment | 74 |
| Administration | 48 |
| Consulting & Corporate Strategy | 5 |
| I.T. & Communications | 5 |
| Retail & Consumer Products | 2 |
| Real Estate & Property | 2 |
| Accounting | 2 |
| Healthcare & Medical | 1 |
| Legal | 1 |
| Sales & Marketing | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **125**.
Content-unique candidates outside it or unresolved: **16**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 20 | YES |
| Other / Unknown | 16 | NO |
| West Midlands - Birmingham & Solihull | 8 | YES |
| Hampshire | 8 | YES |
| Nottinghamshire | 6 | YES |
| Greater Manchester - Manchester & Salford | 6 | YES |
| Yorkshire - West | 5 | YES |
| North East | 5 | YES |
| Sussex | 5 | YES |
| Essex | 5 | YES |
| Kent | 5 | YES |
| Lincolnshire | 4 | YES |
| Northamptonshire | 3 | YES |
| Bristol & Bath | 3 | YES |
| Leicestershire | 3 | YES |
| Shropshire | 3 | YES |
| Worcestershire | 3 | YES |
| Surrey | 2 | YES |
| Berkshire | 2 | YES |
| Suffolk | 2 | YES |
| Hertfordshire | 2 | YES |
| Scotland West - Glasgow | 2 | YES |
| Devon | 2 | YES |
| West Midlands - Coventry & Warwickshire | 2 | YES |
| Merseyside - Liverpool | 2 | YES |
| Buckinghamshire | 2 | YES |
| Staffordshire | 2 | YES |
| Gloucestershire | 2 | YES |
| Bedfordshire | 1 | YES |
| Greater Manchester - South | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

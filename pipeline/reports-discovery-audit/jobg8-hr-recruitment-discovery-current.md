# JobG8 HR / Recruitment family discovery

Feed: **2026-08-27.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **288**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **288**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **288**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **45**
Provisional BORDERLINE: **63**
Provisional OUT (specialist/salary): **180**
Estimated genuine inventory before deep advert review: **~77** (working range **45–108**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **CAUTION / LIKELY BELOW GATE**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 152 |
| BORDERLINE | 63 |
| LIKELY_IN | 45 |
| OUT_SALARY | 28 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £25k–£30k | 96 |
| £30k–£40k | 89 |
| missing/unknown | 53 |
| >£50,000 OUT | 27 |
| £40k–£50,000 | 14 |
| <£25k | 9 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| HR / Recruitment | 155 |
| Administration | 54 |
| Sales & Marketing | 43 |
| Accounting | 10 |
| Consulting & Corporate Strategy | 8 |
| Executive Positions | 5 |
| I.T. & Communications | 4 |
| Banking & Financial Services | 3 |
| Retail & Consumer Products | 2 |
| Legal | 2 |
| Healthcare & Medical | 1 |
| Real Estate & Property | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **267**.
Content-unique candidates outside it or unresolved: **21**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 31 | YES |
| Bristol & Bath | 26 | YES |
| Other / Unknown | 19 | NO |
| Hampshire | 18 | YES |
| Yorkshire - West | 12 | YES |
| Greater Manchester - Manchester & Salford | 12 | YES |
| Kent | 9 | YES |
| West Midlands - Birmingham & Solihull | 9 | YES |
| North East | 9 | YES |
| Buckinghamshire | 9 | YES |
| Sussex | 8 | YES |
| Devon | 7 | YES |
| Nottinghamshire | 7 | YES |
| Surrey | 6 | YES |
| Lincolnshire | 6 | YES |
| Essex | 6 | YES |
| Oxfordshire | 5 | YES |
| Yorkshire - North | 5 | YES |
| Suffolk | 5 | YES |
| Northamptonshire | 5 | YES |
| Lancashire - Central | 5 | YES |
| Worcestershire | 5 | YES |
| Somerset | 5 | YES |
| Berkshire | 4 | YES |
| Leicestershire | 4 | YES |
| Gloucestershire | 4 | YES |
| Hertfordshire | 3 | YES |
| Scotland West - Glasgow | 3 | YES |
| West Midlands - Coventry & Warwickshire | 3 | YES |
| Shropshire | 3 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

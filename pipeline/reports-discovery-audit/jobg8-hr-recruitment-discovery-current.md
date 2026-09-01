# JobG8 HR / Recruitment family discovery

Feed: **2026-09-01.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **367**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **367**
Additional cross-reference content duplicates: **8**
Content-unique broad universe: **359**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **54**
Provisional BORDERLINE: **79**
Provisional OUT (specialist/salary): **226**
Estimated genuine inventory before deep advert review: **~94** (working range **54–133**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **CAUTION / LIKELY BELOW GATE**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 190 |
| BORDERLINE | 79 |
| LIKELY_IN | 54 |
| OUT_SALARY | 36 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £30k–£40k | 101 |
| £25k–£30k | 92 |
| missing/unknown | 91 |
| >£50,000 OUT | 36 |
| £40k–£50,000 | 31 |
| <£25k | 8 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| HR / Recruitment | 233 |
| Administration | 56 |
| Sales & Marketing | 48 |
| Consulting & Corporate Strategy | 6 |
| I.T. & Communications | 4 |
| Accounting | 4 |
| Real Estate & Property | 3 |
| Retail & Consumer Products | 2 |
| Call Centre / CustomerService | 1 |
| Legal | 1 |
| Banking & Financial Services | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **336**.
Content-unique candidates outside it or unresolved: **23**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 50 | YES |
| Bristol & Bath | 21 | YES |
| Other / Unknown | 20 | NO |
| Greater Manchester - Manchester & Salford | 18 | YES |
| Yorkshire - West | 17 | YES |
| Hampshire | 17 | YES |
| Devon | 13 | YES |
| Berkshire | 11 | YES |
| West Midlands - Birmingham & Solihull | 10 | YES |
| Essex | 9 | YES |
| Kent | 9 | YES |
| Nottinghamshire | 9 | YES |
| Buckinghamshire | 9 | YES |
| North East | 8 | YES |
| Sussex | 8 | YES |
| Yorkshire - North | 8 | YES |
| Northamptonshire | 7 | YES |
| Lincolnshire | 7 | YES |
| Gloucestershire | 7 | YES |
| Surrey | 7 | YES |
| Worcestershire | 6 | YES |
| Somerset | 6 | YES |
| Suffolk | 5 | YES |
| Hertfordshire | 5 | YES |
| West Midlands - Coventry & Warwickshire | 5 | YES |
| Leicestershire | 5 | YES |
| Lancashire - Central | 5 | YES |
| Cheshire - West | 5 | YES |
| Scotland West - Glasgow | 4 | YES |
| Shropshire | 4 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

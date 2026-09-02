# JobG8 HR / Recruitment family discovery

Feed: **2026-09-02.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **357**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **357**
Additional cross-reference content duplicates: **8**
Content-unique broad universe: **349**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **52**
Provisional BORDERLINE: **77**
Provisional OUT (specialist/salary): **220**
Estimated genuine inventory before deep advert review: **~90** (working range **52–129**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **CAUTION / LIKELY BELOW GATE**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 183 |
| BORDERLINE | 77 |
| LIKELY_IN | 52 |
| OUT_SALARY | 37 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £30k–£40k | 96 |
| £25k–£30k | 89 |
| missing/unknown | 86 |
| >£50,000 OUT | 37 |
| £40k–£50,000 | 31 |
| <£25k | 10 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| HR / Recruitment | 227 |
| Administration | 54 |
| Sales & Marketing | 46 |
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
Content-unique candidates mapping into that UK market universe: **325**.
Content-unique candidates outside it or unresolved: **24**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 51 | YES |
| Bristol & Bath | 24 | YES |
| Other / Unknown | 21 | NO |
| Greater Manchester - Manchester & Salford | 18 | YES |
| Hampshire | 16 | YES |
| Yorkshire - West | 14 | YES |
| Berkshire | 12 | YES |
| Devon | 12 | YES |
| Kent | 9 | YES |
| West Midlands - Birmingham & Solihull | 9 | YES |
| Nottinghamshire | 9 | YES |
| Essex | 8 | YES |
| Yorkshire - North | 8 | YES |
| Sussex | 7 | YES |
| North East | 7 | YES |
| Buckinghamshire | 7 | YES |
| Surrey | 7 | YES |
| Northamptonshire | 6 | YES |
| Lincolnshire | 6 | YES |
| West Midlands - Coventry & Warwickshire | 6 | YES |
| Leicestershire | 6 | YES |
| Somerset | 6 | YES |
| Gloucestershire | 6 | YES |
| Suffolk | 5 | YES |
| Hertfordshire | 5 | YES |
| Worcestershire | 5 | YES |
| Shropshire | 4 | YES |
| Lancashire - Central | 4 | YES |
| Cheshire - West | 4 | YES |
| Oxfordshire | 4 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

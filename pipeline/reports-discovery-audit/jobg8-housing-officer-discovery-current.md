# JobG8 Housing Officer family discovery

Feed: **2026-10-30.xlsx**
Jobs in feed: **20,000**
Raw broad possible universe before exclusions/dedupe: **248**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **248**
Additional cross-reference content duplicates: **1**
Content-unique broad universe: **247**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **34**
Provisional BORDERLINE: **88**
Provisional OUT (specialist/salary): **125**
Estimated genuine inventory before deep advert review: **~78** (working range **34–122**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **CAUTION / LIKELY BELOW GATE**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| BORDERLINE | 88 |
| OUT_SALARY | 88 |
| OUT_SPECIALIST | 37 |
| LIKELY_IN | 34 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| >£50,000 OUT | 88 |
| £30k–£40k | 73 |
| missing/unknown | 37 |
| £40k–£50,000 | 25 |
| £25k–£30k | 19 |
| <£25k | 5 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Real Estate & Property | 142 |
| Community & Sport | 36 |
| Legal | 23 |
| Call Centre / CustomerService | 19 |
| Healthcare & Medical | 10 |
| Administration | 8 |
| Accounting | 3 |
| Banking & Financial Services | 3 |
| Sales & Marketing | 2 |
| I.T. & Communications | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **224**.
Content-unique candidates outside it or unresolved: **23**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 72 | YES |
| Other / Unknown | 23 | NO |
| Greater Manchester - Manchester & Salford | 16 | YES |
| West Midlands - Birmingham & Solihull | 10 | YES |
| Sussex | 9 | YES |
| Berkshire | 8 | YES |
| West Midlands - Coventry & Warwickshire | 7 | YES |
| Yorkshire - West | 7 | YES |
| Kent | 6 | YES |
| Essex | 5 | YES |
| Surrey | 5 | YES |
| Devon | 4 | YES |
| Cambridgeshire | 4 | YES |
| Northamptonshire | 4 | YES |
| Bristol & Bath | 4 | YES |
| North East | 4 | YES |
| Wales South - Gwent | 4 | YES |
| Merseyside - Liverpool | 3 | YES |
| Dorset | 3 | YES |
| West Midlands - Black Country | 3 | YES |
| Hampshire | 3 | YES |
| Leicestershire | 3 | YES |
| Norfolk | 3 | YES |
| Nottinghamshire | 3 | YES |
| Bedfordshire | 2 | YES |
| Merseyside - St Helens & Knowsley | 2 | YES |
| Worcestershire | 2 | YES |
| Hertfordshire | 2 | YES |
| Cornwall | 2 | YES |
| Scotland - Borders | 2 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

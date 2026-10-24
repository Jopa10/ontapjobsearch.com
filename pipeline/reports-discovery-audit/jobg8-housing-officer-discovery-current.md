# JobG8 Housing Officer family discovery

Feed: **2026-10-24.xlsx**
Jobs in feed: **20,000**
Raw broad possible universe before exclusions/dedupe: **245**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **245**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **245**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **44**
Provisional BORDERLINE: **88**
Provisional OUT (specialist/salary): **113**
Estimated genuine inventory before deep advert review: **~88** (working range **44–132**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **CAUTION / LIKELY BELOW GATE**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| BORDERLINE | 88 |
| OUT_SALARY | 85 |
| LIKELY_IN | 44 |
| OUT_SPECIALIST | 28 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| >£50,000 OUT | 85 |
| £30k–£40k | 80 |
| missing/unknown | 33 |
| £40k–£50,000 | 27 |
| £25k–£30k | 13 |
| <£25k | 7 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Real Estate & Property | 155 |
| Community & Sport | 35 |
| Call Centre / CustomerService | 14 |
| Legal | 13 |
| Administration | 10 |
| Healthcare & Medical | 7 |
| Banking & Financial Services | 5 |
| Accounting | 4 |
| I.T. & Communications | 1 |
| Sales & Marketing | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **218**.
Content-unique candidates outside it or unresolved: **27**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 72 | YES |
| Other / Unknown | 26 | NO |
| Greater Manchester - Manchester & Salford | 12 | YES |
| Sussex | 12 | YES |
| West Midlands - Birmingham & Solihull | 10 | YES |
| Kent | 8 | YES |
| West Midlands - Coventry & Warwickshire | 7 | YES |
| Berkshire | 6 | YES |
| Surrey | 6 | YES |
| Yorkshire - West | 6 | YES |
| Northamptonshire | 5 | YES |
| Bristol & Bath | 5 | YES |
| Essex | 4 | YES |
| Cambridgeshire | 4 | YES |
| Hampshire | 4 | YES |
| North East | 3 | YES |
| Merseyside - Liverpool | 3 | YES |
| Leicestershire | 3 | YES |
| Norfolk | 3 | YES |
| Bedfordshire | 3 | YES |
| Merseyside - St Helens & Knowsley | 3 | YES |
| Staffordshire | 2 | YES |
| Suffolk | 2 | YES |
| Devon | 2 | YES |
| Dorset | 2 | YES |
| West Midlands - Black Country | 2 | YES |
| Hertfordshire | 2 | YES |
| Shropshire | 2 | YES |
| Cornwall | 2 | YES |
| Scotland - Borders | 2 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

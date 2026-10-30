# JobG8 Marketing family discovery

Feed: **2026-10-30.xlsx**
Jobs in feed: **20,000**
Raw broad possible universe before exclusions/dedupe: **495**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **495**
Additional cross-reference content duplicates: **25**
Content-unique broad universe: **470**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **248**
Provisional BORDERLINE: **118**
Provisional OUT (specialist/salary): **104**
Estimated genuine inventory before deep advert review: **~307** (working range **248–366**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 248 |
| BORDERLINE | 118 |
| OUT_SALARY | 86 |
| OUT_SPECIALIST | 18 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 170 |
| £30k–£40k | 98 |
| >£50,000 OUT | 86 |
| £25k–£30k | 60 |
| £40k–£50,000 | 53 |
| <£25k | 3 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Sales & Marketing | 417 |
| Advert / Media / Entertainment | 21 |
| Community & Sport | 9 |
| Administration | 6 |
| Accounting | 5 |
| I.T. & Communications | 5 |
| Healthcare & Medical | 3 |
| Call Centre / CustomerService | 2 |
| Legal | 1 |
| HR / Recruitment | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **425**.
Content-unique candidates outside it or unresolved: **45**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 94 | YES |
| Other / Unknown | 44 | NO |
| Greater Manchester - Manchester & Salford | 29 | YES |
| Surrey | 19 | YES |
| West Midlands - Birmingham & Solihull | 19 | YES |
| Nottinghamshire | 18 | YES |
| Kent | 15 | YES |
| Yorkshire - West | 14 | YES |
| Buckinghamshire | 14 | YES |
| Berkshire | 14 | YES |
| Hampshire | 14 | YES |
| Sussex | 14 | YES |
| Cambridgeshire | 12 | YES |
| West Midlands - Coventry & Warwickshire | 9 | YES |
| Hertfordshire | 9 | YES |
| Essex | 9 | YES |
| Scotland West - Glasgow | 9 | YES |
| Leicestershire | 8 | YES |
| Bristol & Bath | 8 | YES |
| North East | 7 | YES |
| Oxfordshire | 7 | YES |
| Dorset | 6 | YES |
| Gloucestershire | 6 | YES |
| West Midlands - Black Country | 5 | YES |
| Bedfordshire | 4 | YES |
| Devon | 4 | YES |
| Lincolnshire | 3 | YES |
| Derbyshire | 3 | YES |
| Staffordshire | 3 | YES |
| Yorkshire - South | 3 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

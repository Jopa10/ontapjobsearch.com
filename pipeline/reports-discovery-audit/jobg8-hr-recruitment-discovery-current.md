# JobG8 HR / Recruitment family discovery

Feed: **2026-09-22.xlsx**
Jobs in feed: **17,340**
Raw broad possible universe before exclusions/dedupe: **598**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **598**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **598**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **89**
Provisional BORDERLINE: **95**
Provisional OUT (specialist/salary): **414**
Estimated genuine inventory before deep advert review: **~137** (working range **89–184**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO TO BOUNDARY SAMPLE / SCALE PLAUSIBLE**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 339 |
| BORDERLINE | 95 |
| LIKELY_IN | 89 |
| OUT_SALARY | 75 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 283 |
| £30k–£40k | 98 |
| £40k–£50,000 | 78 |
| >£50,000 OUT | 75 |
| £25k–£30k | 57 |
| <£25k | 7 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| HR / Recruitment | 527 |
| Sales & Marketing | 26 |
| Accounting | 11 |
| I.T. & Communications | 8 |
| Banking & Financial Services | 8 |
| Education | 4 |
| Administration | 4 |
| Healthcare & Medical | 3 |
| Legal | 2 |
| Community & Sport | 1 |
| Insurance & Superannuation | 1 |
| Transport & Logistics | 1 |
| Consulting & Corporate Strategy | 1 |
| Call Centre / CustomerService | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **577**.
Content-unique candidates outside it or unresolved: **21**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 112 | YES |
| West Midlands - Birmingham & Solihull | 28 | YES |
| Bristol & Bath | 27 | YES |
| Greater Manchester - Manchester & Salford | 26 | YES |
| Hampshire | 23 | YES |
| Yorkshire - West | 17 | YES |
| Essex | 14 | YES |
| Kent | 13 | YES |
| Northamptonshire | 13 | YES |
| West Midlands - Coventry & Warwickshire | 13 | YES |
| Surrey | 13 | YES |
| Yorkshire - South | 13 | YES |
| Worcestershire | 12 | YES |
| Cambridgeshire | 12 | YES |
| Gloucestershire | 12 | YES |
| Other / Unknown | 11 | NO |
| North East | 11 | YES |
| Oxfordshire | 11 | YES |
| Devon | 11 | YES |
| Staffordshire | 11 | YES |
| Berkshire | 10 | YES |
| Hertfordshire | 10 | YES |
| Sussex | 10 | YES |
| Buckinghamshire | 9 | YES |
| Cheshire - Warrington & Halton | 9 | YES |
| Suffolk | 9 | YES |
| Dorset | 8 | YES |
| Scotland West - Glasgow | 8 | YES |
| East Midlands | 8 | NO |
| Scotland Central - Edinburgh & Lothians | 8 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

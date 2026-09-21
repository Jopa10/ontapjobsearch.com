# JobG8 HR / Recruitment family discovery

Feed: **2026-09-21.xlsx**
Jobs in feed: **17,785**
Raw broad possible universe before exclusions/dedupe: **606**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **606**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **606**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **89**
Provisional BORDERLINE: **96**
Provisional OUT (specialist/salary): **421**
Estimated genuine inventory before deep advert review: **~137** (working range **89–185**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO TO BOUNDARY SAMPLE / SCALE PLAUSIBLE**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 345 |
| BORDERLINE | 96 |
| LIKELY_IN | 89 |
| OUT_SALARY | 76 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 289 |
| £30k–£40k | 101 |
| £40k–£50,000 | 77 |
| >£50,000 OUT | 76 |
| £25k–£30k | 57 |
| <£25k | 6 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| HR / Recruitment | 532 |
| Sales & Marketing | 28 |
| Accounting | 12 |
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
Content-unique candidates mapping into that UK market universe: **583**.
Content-unique candidates outside it or unresolved: **23**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 114 | YES |
| West Midlands - Birmingham & Solihull | 30 | YES |
| Bristol & Bath | 26 | YES |
| Greater Manchester - Manchester & Salford | 26 | YES |
| Hampshire | 23 | YES |
| Yorkshire - West | 17 | YES |
| Essex | 14 | YES |
| Other / Unknown | 13 | NO |
| Kent | 13 | YES |
| Northamptonshire | 13 | YES |
| Surrey | 13 | YES |
| Yorkshire - South | 13 | YES |
| Staffordshire | 13 | YES |
| Gloucestershire | 13 | YES |
| Cambridgeshire | 12 | YES |
| West Midlands - Coventry & Warwickshire | 12 | YES |
| Devon | 12 | YES |
| Berkshire | 11 | YES |
| Worcestershire | 11 | YES |
| Hertfordshire | 11 | YES |
| North East | 11 | YES |
| Oxfordshire | 11 | YES |
| Sussex | 10 | YES |
| Scotland West - Glasgow | 9 | YES |
| Suffolk | 9 | YES |
| Dorset | 8 | YES |
| Buckinghamshire | 8 | YES |
| East Midlands | 8 | NO |
| Cheshire - Warrington & Halton | 8 | YES |
| Scotland Central - Edinburgh & Lothians | 8 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

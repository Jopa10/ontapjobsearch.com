# JobG8 Legal Assistant / Paralegal family discovery

Feed: **2026-10-30.xlsx**
Jobs in feed: **20,000**
Raw broad possible universe before exclusions/dedupe: **462**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **462**
Additional cross-reference content duplicates: **17**
Content-unique broad universe: **445**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **349**
Provisional BORDERLINE: **20**
Provisional OUT (specialist/salary): **76**
Estimated genuine inventory before deep advert review: **~359** (working range **349–369**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 349 |
| OUT_SPECIALIST | 44 |
| OUT_SALARY | 32 |
| BORDERLINE | 20 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 238 |
| £25k–£30k | 94 |
| £30k–£40k | 63 |
| >£50,000 OUT | 32 |
| £40k–£50,000 | 14 |
| <£25k | 4 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Legal | 432 |
| Administration | 12 |
| Real Estate & Property | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **423**.
Content-unique candidates outside it or unresolved: **22**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 97 | YES |
| Surrey | 24 | YES |
| Greater Manchester - Manchester & Salford | 21 | YES |
| Sussex | 20 | YES |
| Other / Unknown | 18 | NO |
| Yorkshire - North | 17 | YES |
| Yorkshire - West | 16 | YES |
| Hampshire | 14 | YES |
| Essex | 11 | YES |
| Bristol & Bath | 10 | YES |
| Northamptonshire | 10 | YES |
| Hertfordshire | 10 | YES |
| West Midlands - Coventry & Warwickshire | 9 | YES |
| West Midlands - Birmingham & Solihull | 9 | YES |
| Nottinghamshire | 8 | YES |
| Yorkshire - South | 8 | YES |
| Cambridgeshire | 8 | YES |
| Kent | 8 | YES |
| Norfolk | 7 | YES |
| Buckinghamshire | 7 | YES |
| Dorset | 6 | YES |
| Merseyside - Liverpool | 6 | YES |
| Berkshire | 6 | YES |
| North East | 6 | YES |
| Cheshire - West | 6 | YES |
| Bedfordshire | 6 | YES |
| Oxfordshire | 5 | YES |
| Gloucestershire | 5 | YES |
| Scotland West - Glasgow | 5 | YES |
| Scotland Central - Edinburgh & Lothians | 5 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

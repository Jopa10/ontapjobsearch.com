# JobG8 Accounts & Finance Operations family discovery

Feed: **2026-09-01.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **907**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **907**
Additional cross-reference content duplicates: **5**
Content-unique broad universe: **902**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **114**
Provisional BORDERLINE: **0**
Provisional OUT (specialist/salary): **788**
Estimated genuine inventory before deep advert review: **~114** (working range **114–114**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 508 |
| OUT_SALARY | 259 |
| LIKELY_IN | 114 |
| OUT_BOUNDARY | 21 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 309 |
| >£45,000 OUT | 259 |
| £30k–£40k | 150 |
| £25k–£30k | 124 |
| £40k–£45,000 | 46 |
| <£25k | 14 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Sales & Marketing | 421 |
| Accounting | 173 |
| Banking & Financial Services | 123 |
| Administration | 56 |
| I.T. & Communications | 36 |
| Insurance & Superannuation | 30 |
| HR / Recruitment | 21 |
| Call Centre / CustomerService | 13 |
| Advert / Media / Entertainment | 8 |
| Legal | 7 |
| Consulting & Corporate Strategy | 4 |
| Real Estate & Property | 4 |
| Retail & Consumer Products | 4 |
| Executive Positions | 2 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **815**.
Content-unique candidates outside it or unresolved: **87**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 170 | YES |
| Other / Unknown | 67 | NO |
| Greater Manchester - Manchester & Salford | 36 | YES |
| Bristol & Bath | 33 | YES |
| Yorkshire - West | 33 | YES |
| West Midlands - Birmingham & Solihull | 28 | YES |
| Surrey | 22 | YES |
| Hertfordshire | 21 | YES |
| Northamptonshire | 20 | YES |
| Hampshire | 20 | YES |
| Oxfordshire | 20 | YES |
| Devon | 19 | YES |
| Buckinghamshire | 19 | YES |
| Essex | 18 | YES |
| Berkshire | 17 | YES |
| Sussex | 16 | YES |
| Cambridgeshire | 16 | YES |
| Suffolk | 14 | YES |
| North East | 14 | YES |
| Yorkshire - North | 14 | YES |
| Northern Ireland - East | 13 | YES |
| Gloucestershire | 13 | YES |
| West Midlands - Coventry & Warwickshire | 12 | YES |
| Kent | 11 | YES |
| Cheshire - Warrington & Halton | 10 | YES |
| Nottinghamshire | 10 | YES |
| Leicestershire | 10 | YES |
| Staffordshire | 10 | YES |
| Somerset | 9 | YES |
| Scotland Central - Edinburgh & Lothians | 9 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

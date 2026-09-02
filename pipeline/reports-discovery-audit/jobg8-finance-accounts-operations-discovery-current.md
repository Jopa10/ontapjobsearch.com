# JobG8 Accounts & Finance Operations family discovery

Feed: **2026-09-02.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **893**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **893**
Additional cross-reference content duplicates: **12**
Content-unique broad universe: **881**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **113**
Provisional BORDERLINE: **0**
Provisional OUT (specialist/salary): **768**
Estimated genuine inventory before deep advert review: **~113** (working range **113–113**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 497 |
| OUT_SALARY | 252 |
| LIKELY_IN | 113 |
| OUT_BOUNDARY | 19 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 299 |
| >£45,000 OUT | 252 |
| £30k–£40k | 145 |
| £25k–£30k | 123 |
| £40k–£45,000 | 47 |
| <£25k | 15 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Sales & Marketing | 394 |
| Accounting | 177 |
| Banking & Financial Services | 127 |
| Administration | 56 |
| I.T. & Communications | 36 |
| Insurance & Superannuation | 30 |
| HR / Recruitment | 18 |
| Call Centre / CustomerService | 13 |
| Advert / Media / Entertainment | 8 |
| Legal | 7 |
| Consulting & Corporate Strategy | 5 |
| Real Estate & Property | 4 |
| Retail & Consumer Products | 4 |
| Executive Positions | 2 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **799**.
Content-unique candidates outside it or unresolved: **82**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 173 | YES |
| Other / Unknown | 66 | NO |
| Greater Manchester - Manchester & Salford | 33 | YES |
| Bristol & Bath | 31 | YES |
| Yorkshire - West | 29 | YES |
| West Midlands - Birmingham & Solihull | 27 | YES |
| Surrey | 22 | YES |
| Hertfordshire | 21 | YES |
| Hampshire | 20 | YES |
| Oxfordshire | 19 | YES |
| Devon | 19 | YES |
| Essex | 18 | YES |
| Northamptonshire | 18 | YES |
| Buckinghamshire | 18 | YES |
| Sussex | 16 | YES |
| Berkshire | 16 | YES |
| Cambridgeshire | 15 | YES |
| Northern Ireland - East | 14 | YES |
| Gloucestershire | 14 | YES |
| North East | 14 | YES |
| Suffolk | 13 | YES |
| Yorkshire - North | 12 | YES |
| West Midlands - Coventry & Warwickshire | 12 | YES |
| Kent | 11 | YES |
| Cheshire - Warrington & Halton | 10 | YES |
| Nottinghamshire | 10 | YES |
| Staffordshire | 10 | YES |
| Somerset | 9 | YES |
| Scotland Central - Edinburgh & Lothians | 9 | YES |
| Leicestershire | 9 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

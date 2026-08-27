# JobG8 Accounts & Finance Operations family discovery

Feed: **2026-08-27.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **1,073**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **1,073**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **1,073**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **298**
Provisional BORDERLINE: **0**
Provisional OUT (specialist/salary): **775**
Estimated genuine inventory before deep advert review: **~298** (working range **298–298**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 408 |
| OUT_SALARY | 351 |
| LIKELY_IN | 298 |
| OUT_BOUNDARY | 16 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| >£45,000 OUT | 351 |
| missing/unknown | 256 |
| £25k–£30k | 238 |
| £30k–£40k | 158 |
| £40k–£45,000 | 44 |
| <£25k | 26 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Accounting | 431 |
| Banking & Financial Services | 338 |
| Sales & Marketing | 157 |
| Administration | 50 |
| HR / Recruitment | 21 |
| Executive Positions | 14 |
| I.T. & Communications | 14 |
| Consulting & Corporate Strategy | 10 |
| Call Centre / CustomerService | 8 |
| Insurance & Superannuation | 7 |
| Advert / Media / Entertainment | 7 |
| Legal | 6 |
| Real Estate & Property | 5 |
| Healthcare & Medical | 3 |
| Retail & Consumer Products | 2 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **991**.
Content-unique candidates outside it or unresolved: **82**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 119 | YES |
| Other / Unknown | 60 | NO |
| Greater Manchester - Manchester & Salford | 52 | YES |
| Yorkshire - West | 48 | YES |
| Leicestershire | 31 | YES |
| Bristol & Bath | 30 | YES |
| West Midlands - Birmingham & Solihull | 30 | YES |
| Devon | 28 | YES |
| Yorkshire - North | 26 | YES |
| Hampshire | 25 | YES |
| Oxfordshire | 24 | YES |
| Buckinghamshire | 24 | YES |
| Cambridgeshire | 23 | YES |
| Yorkshire - South | 21 | YES |
| Northern Ireland - East | 21 | YES |
| Nottinghamshire | 21 | YES |
| North East | 21 | YES |
| Surrey | 20 | YES |
| Gloucestershire | 19 | YES |
| Northamptonshire | 19 | YES |
| Merseyside - Liverpool | 19 | YES |
| Hertfordshire | 18 | YES |
| Berkshire | 17 | YES |
| Sussex | 16 | YES |
| Essex | 16 | YES |
| Cheshire - Warrington & Halton | 16 | YES |
| Somerset | 15 | YES |
| East Midlands | 15 | NO |
| Scotland West - Glasgow | 14 | YES |
| Lincolnshire | 14 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

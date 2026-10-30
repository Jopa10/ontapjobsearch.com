# JobG8 Warehouse & Logistics Operations family discovery

Feed: **2026-10-30.xlsx**
Jobs in feed: **20,000**
Raw broad possible universe before exclusions/dedupe: **387**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **387**
Additional cross-reference content duplicates: **2**
Content-unique broad universe: **385**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **65**
Provisional BORDERLINE: **87**
Provisional OUT (specialist/salary): **233**
Estimated genuine inventory before deep advert review: **~109** (working range **65–152**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO TO BOUNDARY SAMPLE / SCALE PLAUSIBLE**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 185 |
| BORDERLINE | 87 |
| LIKELY_IN | 65 |
| OUT_SALARY | 48 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £25k–£30k | 116 |
| £30k–£40k | 100 |
| missing/unknown | 79 |
| >£45,000 OUT | 48 |
| <£25k | 32 |
| £40k–£45,000 | 10 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Transport & Logistics | 247 |
| Administration | 66 |
| Sales & Marketing | 35 |
| Call Centre / CustomerService | 7 |
| Banking & Financial Services | 6 |
| I.T. & Communications | 6 |
| HR / Recruitment | 4 |
| Advert / Media / Entertainment | 3 |
| Accounting | 3 |
| Real Estate & Property | 3 |
| Government & Defence | 2 |
| Legal | 2 |
| Healthcare & Medical | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **343**.
Content-unique candidates outside it or unresolved: **42**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| Other / Unknown | 32 | NO |
| London | 30 | YES |
| Oxfordshire | 21 | YES |
| Greater Manchester - Manchester & Salford | 18 | YES |
| Hampshire | 16 | YES |
| Yorkshire - West | 16 | YES |
| Kent | 15 | YES |
| Essex | 14 | YES |
| North East | 12 | YES |
| Leicestershire | 10 | YES |
| West Midlands - Birmingham & Solihull | 10 | YES |
| West Midlands | 9 | NO |
| Berkshire | 9 | YES |
| Bristol & Bath | 9 | YES |
| Northamptonshire | 9 | YES |
| Bedfordshire | 8 | YES |
| Hertfordshire | 8 | YES |
| Nottinghamshire | 7 | YES |
| West Midlands - Black Country | 7 | YES |
| Worcestershire | 7 | YES |
| Gloucestershire | 7 | YES |
| Yorkshire - South | 6 | YES |
| Somerset | 6 | YES |
| Cambridgeshire | 6 | YES |
| Surrey | 6 | YES |
| West Midlands - Coventry & Warwickshire | 6 | YES |
| Sussex | 5 | YES |
| Buckinghamshire | 5 | YES |
| Derbyshire | 5 | YES |
| Wiltshire | 4 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

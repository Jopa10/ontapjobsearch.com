# JobG8 Warehouse & Logistics Operations family discovery

Feed: **2026-10-24.xlsx**
Jobs in feed: **20,000**
Raw broad possible universe before exclusions/dedupe: **332**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **332**
Additional cross-reference content duplicates: **2**
Content-unique broad universe: **330**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **68**
Provisional BORDERLINE: **66**
Provisional OUT (specialist/salary): **196**
Estimated genuine inventory before deep advert review: **~101** (working range **68–134**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO TO BOUNDARY SAMPLE / SCALE PLAUSIBLE**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SPECIALIST | 149 |
| LIKELY_IN | 68 |
| BORDERLINE | 66 |
| OUT_SALARY | 47 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £25k–£30k | 103 |
| £30k–£40k | 89 |
| missing/unknown | 61 |
| >£45,000 OUT | 47 |
| <£25k | 20 |
| £40k–£45,000 | 10 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Transport & Logistics | 193 |
| Administration | 69 |
| Sales & Marketing | 36 |
| Call Centre / CustomerService | 6 |
| HR / Recruitment | 5 |
| Government & Defence | 4 |
| Accounting | 4 |
| Banking & Financial Services | 4 |
| I.T. & Communications | 4 |
| Advert / Media / Entertainment | 2 |
| Real Estate & Property | 1 |
| Healthcare & Medical | 1 |
| Legal | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **288**.
Content-unique candidates outside it or unresolved: **42**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| Other / Unknown | 31 | NO |
| London | 25 | YES |
| Greater Manchester - Manchester & Salford | 16 | YES |
| Hampshire | 16 | YES |
| Oxfordshire | 15 | YES |
| Yorkshire - West | 14 | YES |
| Kent | 13 | YES |
| Nottinghamshire | 9 | YES |
| Essex | 9 | YES |
| West Midlands | 8 | NO |
| Hertfordshire | 8 | YES |
| Yorkshire - South | 8 | YES |
| Berkshire | 8 | YES |
| Leicestershire | 8 | YES |
| Worcestershire | 8 | YES |
| West Midlands - Birmingham & Solihull | 7 | YES |
| Northamptonshire | 7 | YES |
| North East | 7 | YES |
| Gloucestershire | 6 | YES |
| Bedfordshire | 6 | YES |
| Buckinghamshire | 6 | YES |
| West Midlands - Black Country | 6 | YES |
| Surrey | 6 | YES |
| West Midlands - Coventry & Warwickshire | 6 | YES |
| Bristol & Bath | 5 | YES |
| Suffolk | 5 | YES |
| Dorset | 4 | YES |
| Sussex | 4 | YES |
| Somerset | 4 | YES |
| Cambridgeshire | 4 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

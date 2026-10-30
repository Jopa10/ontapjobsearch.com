# JobG8 IT Support family discovery

Feed: **2026-10-30.xlsx**
Jobs in feed: **20,000**
Raw broad possible universe before exclusions/dedupe: **248**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **248**
Additional cross-reference content duplicates: **26**
Content-unique broad universe: **222**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **130**
Provisional BORDERLINE: **67**
Provisional OUT (specialist/salary): **25**
Estimated genuine inventory before deep advert review: **~164** (working range **130–197**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 130 |
| BORDERLINE | 67 |
| OUT_SALARY | 17 |
| OUT_SPECIALIST | 8 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 74 |
| £30k–£40k | 49 |
| <£25k | 45 |
| £25k–£30k | 24 |
| >£50,000 OUT | 17 |
| £40k–£50,000 | 13 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| I.T. & Communications | 172 |
| Call Centre / CustomerService | 17 |
| Administration | 16 |
| Real Estate & Property | 3 |
| Government & Defence | 2 |
| Healthcare & Medical | 2 |
| HR / Recruitment | 2 |
| Sales & Marketing | 2 |
| Transport & Logistics | 1 |
| Legal | 1 |
| Accounting | 1 |
| Advert / Media / Entertainment | 1 |
| Education | 1 |
| Banking & Financial Services | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **209**.
Content-unique candidates outside it or unresolved: **13**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 28 | YES |
| Other / Unknown | 11 | NO |
| Berkshire | 11 | YES |
| Essex | 11 | YES |
| Surrey | 9 | YES |
| Sussex | 9 | YES |
| Hampshire | 9 | YES |
| Oxfordshire | 8 | YES |
| North East | 7 | YES |
| Buckinghamshire | 7 | YES |
| Nottinghamshire | 6 | YES |
| Greater Manchester - Manchester & Salford | 6 | YES |
| Northamptonshire | 5 | YES |
| Merseyside - Liverpool | 5 | YES |
| Devon | 5 | YES |
| Cambridgeshire | 5 | YES |
| West Midlands - Birmingham & Solihull | 4 | YES |
| Gloucestershire | 4 | YES |
| Hertfordshire | 4 | YES |
| Kent | 4 | YES |
| Scotland West - Glasgow | 4 | YES |
| Norfolk | 4 | YES |
| Yorkshire - West | 3 | YES |
| Bristol & Bath | 3 | YES |
| Dorset | 3 | YES |
| Lincolnshire | 3 | YES |
| Wales South - Swansea Bay | 3 | YES |
| Northern Ireland - East | 3 | YES |
| Leicestershire | 3 | YES |
| Yorkshire - North | 3 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

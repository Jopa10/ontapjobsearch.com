# JobG8 Warehouse & Logistics Operations family discovery

Feed: **2026-08-31.xlsx**
Jobs in feed: **5,354**
Raw broad possible universe before exclusions/dedupe: **42**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **42**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **42**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £45,000 = OUT; exactly £45,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **14**
Provisional BORDERLINE: **12**
Provisional OUT (specialist/salary): **16**
Estimated genuine inventory before deep advert review: **~20** (working range **14–26**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 14 |
| BORDERLINE | 12 |
| OUT_SPECIALIST | 9 |
| OUT_SALARY | 7 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £25k–£30k | 19 |
| missing/unknown | 8 |
| >£45,000 OUT | 7 |
| £30k–£40k | 5 |
| <£25k | 2 |
| £40k–£45,000 | 1 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Administration | 27 |
| I.T. & Communications | 4 |
| Banking & Financial Services | 2 |
| Advert / Media / Entertainment | 2 |
| Call Centre / CustomerService | 2 |
| HR / Recruitment | 2 |
| Real Estate & Property | 1 |
| Retail & Consumer Products | 1 |
| Executive Positions | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **37**.
Content-unique candidates outside it or unresolved: **5**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| Other / Unknown | 5 | NO |
| Staffordshire | 4 | YES |
| West Midlands - Black Country | 3 | YES |
| Leicestershire | 3 | YES |
| London | 3 | YES |
| Essex | 2 | YES |
| Derbyshire | 2 | YES |
| Lancashire - East | 2 | YES |
| West Midlands - Coventry & Warwickshire | 2 | YES |
| Northamptonshire | 2 | YES |
| Oxfordshire | 2 | YES |
| Berkshire | 1 | YES |
| Somerset | 1 | YES |
| Lincolnshire | 1 | YES |
| Scotland West - Glasgow | 1 | YES |
| Buckinghamshire | 1 | YES |
| Cambridgeshire | 1 | YES |
| Scotland Central - Tayside | 1 | YES |
| Gloucestershire | 1 | YES |
| Nottinghamshire | 1 | YES |
| Yorkshire - West | 1 | YES |
| Merseyside - Liverpool | 1 | YES |
| Hampshire | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

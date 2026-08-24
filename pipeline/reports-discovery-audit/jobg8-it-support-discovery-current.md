# JobG8 IT Support family discovery

Feed: **2026-08-24.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **80**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **80**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **80**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **44**
Provisional BORDERLINE: **30**
Provisional OUT (specialist/salary): **6**
Estimated genuine inventory before deep advert review: **~59** (working range **44–74**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 44 |
| BORDERLINE | 30 |
| OUT_SPECIALIST | 3 |
| OUT_SALARY | 3 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £30k–£40k | 27 |
| £25k–£30k | 26 |
| missing/unknown | 17 |
| £40k–£50,000 | 6 |
| >£50,000 OUT | 3 |
| <£25k | 1 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| I.T. & Communications | 51 |
| Administration | 23 |
| Call Centre / CustomerService | 4 |
| Legal | 1 |
| Real Estate & Property | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **75**.
Content-unique candidates outside it or unresolved: **5**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| Essex | 7 | YES |
| London | 7 | YES |
| Hertfordshire | 6 | YES |
| Surrey | 5 | YES |
| Berkshire | 4 | YES |
| Other / Unknown | 4 | NO |
| Hampshire | 4 | YES |
| Kent | 4 | YES |
| Yorkshire - West | 3 | YES |
| Worcestershire | 2 | YES |
| Greater Manchester - Manchester & Salford | 2 | YES |
| Northern Ireland - East | 2 | YES |
| Sussex | 2 | YES |
| West Midlands - Birmingham & Solihull | 2 | YES |
| North East | 2 | YES |
| Scotland West - Glasgow | 2 | YES |
| Yorkshire - North | 2 | YES |
| Devon | 2 | YES |
| West Midlands - Black Country | 2 | YES |
| Staffordshire | 2 | YES |
| Cheshire - East | 1 | YES |
| West Midlands - Coventry & Warwickshire | 1 | YES |
| Leicestershire | 1 | YES |
| Norfolk | 1 | YES |
| South West | 1 | NO |
| Derbyshire | 1 | YES |
| Gloucestershire | 1 | YES |
| Northamptonshire | 1 | YES |
| Wales South - Cardiff & Vale | 1 | YES |
| Oxfordshire | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

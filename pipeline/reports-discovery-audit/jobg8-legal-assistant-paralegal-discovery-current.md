# JobG8 Legal Assistant / Paralegal family discovery

Feed: **2026-08-28.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **98**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **98**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **98**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **82**
Provisional BORDERLINE: **3**
Provisional OUT (specialist/salary): **13**
Estimated genuine inventory before deep advert review: **~84** (working range **82–85**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 82 |
| OUT_SPECIALIST | 9 |
| OUT_SALARY | 4 |
| BORDERLINE | 3 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £25k–£30k | 53 |
| missing/unknown | 17 |
| £30k–£40k | 15 |
| <£25k | 6 |
| >£50,000 OUT | 4 |
| £40k–£50,000 | 3 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Legal | 82 |
| Administration | 15 |
| Call Centre / CustomerService | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **95**.
Content-unique candidates outside it or unresolved: **3**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 13 | YES |
| Yorkshire - West | 6 | YES |
| Yorkshire - South | 5 | YES |
| Bedfordshire | 4 | YES |
| Greater Manchester - Manchester & Salford | 4 | YES |
| Kent | 4 | YES |
| Bristol & Bath | 4 | YES |
| Surrey | 4 | YES |
| Wales South - Valleys | 4 | YES |
| Nottinghamshire | 3 | YES |
| West Midlands - Birmingham & Solihull | 3 | YES |
| Wiltshire | 3 | YES |
| Other / Unknown | 3 | NO |
| Cambridgeshire | 2 | YES |
| Leicestershire | 2 | YES |
| Hertfordshire | 2 | YES |
| Shropshire | 2 | YES |
| Essex | 2 | YES |
| Hampshire | 2 | YES |
| North East | 2 | YES |
| Scotland Central - Edinburgh & Lothians | 2 | YES |
| Oxfordshire | 2 | YES |
| Wales South - Gwent | 2 | YES |
| Wales South - Cardiff & Vale | 2 | YES |
| Scotland Central - Tayside | 1 | YES |
| Northern Ireland - East | 1 | YES |
| Devon | 1 | YES |
| Lincolnshire | 1 | YES |
| Cheshire - Warrington & Halton | 1 | YES |
| Northamptonshire | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

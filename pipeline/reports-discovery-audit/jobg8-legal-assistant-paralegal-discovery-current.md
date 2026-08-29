# JobG8 Legal Assistant / Paralegal family discovery

Feed: **2026-08-29.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **81**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **81**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **81**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **68**
Provisional BORDERLINE: **2**
Provisional OUT (specialist/salary): **11**
Estimated genuine inventory before deep advert review: **~69** (working range **68–70**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 68 |
| OUT_SPECIALIST | 7 |
| OUT_SALARY | 4 |
| BORDERLINE | 2 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| £25k–£30k | 44 |
| £30k–£40k | 14 |
| missing/unknown | 13 |
| >£50,000 OUT | 4 |
| £40k–£50,000 | 3 |
| <£25k | 3 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Legal | 66 |
| Administration | 14 |
| Call Centre / CustomerService | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **79**.
Content-unique candidates outside it or unresolved: **2**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 12 | YES |
| Yorkshire - South | 5 | YES |
| Yorkshire - West | 5 | YES |
| Greater Manchester - Manchester & Salford | 4 | YES |
| Shropshire | 3 | YES |
| Bedfordshire | 3 | YES |
| West Midlands - Birmingham & Solihull | 3 | YES |
| Kent | 3 | YES |
| Wiltshire | 3 | YES |
| Surrey | 3 | YES |
| Wales South - Valleys | 3 | YES |
| Northern Ireland - East | 2 | YES |
| Leicestershire | 2 | YES |
| Lincolnshire | 2 | YES |
| Nottinghamshire | 2 | YES |
| Essex | 2 | YES |
| Oxfordshire | 2 | YES |
| Other / Unknown | 2 | NO |
| West Midlands - Black Country | 2 | YES |
| Scotland Central - Tayside | 1 | YES |
| Devon | 1 | YES |
| Hertfordshire | 1 | YES |
| Cheshire - Warrington & Halton | 1 | YES |
| Northamptonshire | 1 | YES |
| North East | 1 | YES |
| Suffolk | 1 | YES |
| Sussex | 1 | YES |
| Hampshire | 1 | YES |
| Cambridgeshire | 1 | YES |
| Scotland Central - Edinburgh & Lothians | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

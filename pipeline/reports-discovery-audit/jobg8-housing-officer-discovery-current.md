# JobG8 Housing Officer family discovery

Feed: **2026-08-29.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **94**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **94**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **94**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **26**
Provisional BORDERLINE: **37**
Provisional OUT (specialist/salary): **31**
Estimated genuine inventory before deep advert review: **~44** (working range **26–63**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| BORDERLINE | 37 |
| LIKELY_IN | 26 |
| OUT_SALARY | 19 |
| OUT_SPECIALIST | 12 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 24 |
| £25k–£30k | 21 |
| £30k–£40k | 19 |
| >£50,000 OUT | 19 |
| <£25k | 7 |
| £40k–£50,000 | 4 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Real Estate & Property | 29 |
| Healthcare & Medical | 26 |
| Administration | 8 |
| Executive Positions | 8 |
| Accounting | 7 |
| Banking & Financial Services | 5 |
| Legal | 5 |
| Call Centre / CustomerService | 4 |
| Insurance & Superannuation | 1 |
| I.T. & Communications | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **86**.
Content-unique candidates outside it or unresolved: **8**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 12 | YES |
| Other / Unknown | 8 | NO |
| Greater Manchester - Manchester & Salford | 7 | YES |
| Oxfordshire | 6 | YES |
| Surrey | 5 | YES |
| Devon | 4 | YES |
| Dorset | 4 | YES |
| Hampshire | 4 | YES |
| Bristol & Bath | 4 | YES |
| Essex | 3 | YES |
| Wiltshire | 3 | YES |
| Sussex | 3 | YES |
| Cheshire - Warrington & Halton | 2 | YES |
| Northamptonshire | 2 | YES |
| Cambridgeshire | 2 | YES |
| Kent | 2 | YES |
| Bedfordshire | 2 | YES |
| Hertfordshire | 2 | YES |
| Scotland West - Glasgow | 2 | YES |
| Merseyside - Liverpool | 2 | YES |
| North Scotland | 1 | YES |
| Norfolk | 1 | YES |
| Yorkshire - North | 1 | YES |
| North East | 1 | YES |
| Somerset | 1 | YES |
| Nottinghamshire | 1 | YES |
| Staffordshire | 1 | YES |
| Cornwall | 1 | YES |
| Berkshire | 1 | YES |
| Yorkshire - West | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

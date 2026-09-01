# JobG8 Housing Officer family discovery

Feed: **2026-08-31.xlsx**
Jobs in feed: **5,354**
Raw broad possible universe before exclusions/dedupe: **37**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **37**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **37**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **7**
Provisional BORDERLINE: **8**
Provisional OUT (specialist/salary): **22**
Estimated genuine inventory before deep advert review: **~11** (working range **7–15**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| OUT_SALARY | 14 |
| BORDERLINE | 8 |
| OUT_SPECIALIST | 8 |
| LIKELY_IN | 7 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| >£50,000 OUT | 14 |
| missing/unknown | 12 |
| <£25k | 4 |
| £25k–£30k | 3 |
| £30k–£40k | 2 |
| £40k–£50,000 | 2 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Real Estate & Property | 9 |
| Administration | 7 |
| Banking & Financial Services | 4 |
| Healthcare & Medical | 4 |
| I.T. & Communications | 4 |
| Call Centre / CustomerService | 3 |
| Executive Positions | 3 |
| Legal | 2 |
| Insurance & Superannuation | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **31**.
Content-unique candidates outside it or unresolved: **6**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 8 | YES |
| Other / Unknown | 6 | NO |
| Surrey | 3 | YES |
| Northamptonshire | 2 | YES |
| Greater Manchester - Manchester & Salford | 2 | YES |
| Kent | 2 | YES |
| Oxfordshire | 2 | YES |
| Devon | 1 | YES |
| Essex | 1 | YES |
| Norfolk | 1 | YES |
| Yorkshire - North | 1 | YES |
| North East | 1 | YES |
| Cheshire - Warrington & Halton | 1 | YES |
| Dorset | 1 | YES |
| Yorkshire - West | 1 | YES |
| Suffolk | 1 | YES |
| Sussex | 1 | YES |
| Shropshire | 1 | YES |
| Bristol & Bath | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

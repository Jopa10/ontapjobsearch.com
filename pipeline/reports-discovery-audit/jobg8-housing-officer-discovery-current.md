# JobG8 Housing Officer family discovery

Feed: **2026-09-12.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **87**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **87**
Additional cross-reference content duplicates: **0**
Content-unique broad universe: **87**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **18**
Provisional BORDERLINE: **29**
Provisional OUT (specialist/salary): **40**
Estimated genuine inventory before deep advert review: **~32** (working range **18–47**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **STOP / VERY THIN**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| BORDERLINE | 29 |
| OUT_SPECIALIST | 27 |
| LIKELY_IN | 18 |
| OUT_SALARY | 13 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 30 |
| £25k–£30k | 21 |
| £30k–£40k | 18 |
| >£50,000 OUT | 12 |
| £40k–£50,000 | 4 |
| <£25k | 2 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Real Estate & Property | 31 |
| Healthcare & Medical | 19 |
| Legal | 14 |
| Administration | 10 |
| Banking & Financial Services | 5 |
| Insurance & Superannuation | 2 |
| Executive Positions | 2 |
| I.T. & Communications | 1 |
| Accounting | 1 |
| Sales & Marketing | 1 |
| Call Centre / CustomerService | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **78**.
Content-unique candidates outside it or unresolved: **9**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 10 | YES |
| Sussex | 9 | YES |
| Other / Unknown | 9 | NO |
| Greater Manchester - Manchester & Salford | 7 | YES |
| Merseyside - Liverpool | 6 | YES |
| Northern Ireland - East | 5 | YES |
| Kent | 4 | YES |
| Northamptonshire | 4 | YES |
| Surrey | 3 | YES |
| Hampshire | 3 | YES |
| Greater Manchester - Wigan & Bolton | 3 | YES |
| Oxfordshire | 2 | YES |
| North East | 2 | YES |
| West Midlands - Birmingham & Solihull | 2 | YES |
| Norfolk | 2 | YES |
| Buckinghamshire | 2 | YES |
| Dorset | 1 | YES |
| Nottinghamshire | 1 | YES |
| Staffordshire | 1 | YES |
| Yorkshire - West | 1 | YES |
| Cheshire - East | 1 | YES |
| Scotland West - Ayrshire | 1 | YES |
| Devon | 1 | YES |
| Hertfordshire | 1 | YES |
| Bristol & Bath | 1 | YES |
| Greater Manchester - North | 1 | YES |
| Cheshire - West | 1 | YES |
| Lincolnshire | 1 | YES |
| Wiltshire | 1 | YES |
| Essex | 1 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

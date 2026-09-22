# JobG8 Marketing family discovery

Feed: **2026-09-22.xlsx**
Jobs in feed: **17,340**
Raw broad possible universe before exclusions/dedupe: **291**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **291**
Additional cross-reference content duplicates: **18**
Content-unique broad universe: **273**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **157**
Provisional BORDERLINE: **68**
Provisional OUT (specialist/salary): **48**
Estimated genuine inventory before deep advert review: **~191** (working range **157–225**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 157 |
| BORDERLINE | 68 |
| OUT_SALARY | 35 |
| OUT_SPECIALIST | 13 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 153 |
| £30k–£40k | 52 |
| >£50,000 OUT | 34 |
| £40k–£50,000 | 22 |
| £25k–£30k | 9 |
| <£25k | 3 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Sales & Marketing | 250 |
| I.T. & Communications | 9 |
| Advert / Media / Entertainment | 9 |
| Transport & Logistics | 2 |
| Community & Sport | 1 |
| Call Centre / CustomerService | 1 |
| Retail & Consumer Products | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **256**.
Content-unique candidates outside it or unresolved: **17**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 73 | YES |
| Surrey | 13 | YES |
| Other / Unknown | 12 | NO |
| Berkshire | 12 | YES |
| Oxfordshire | 9 | YES |
| Yorkshire - West | 9 | YES |
| Merseyside - Liverpool | 8 | YES |
| West Midlands - Birmingham & Solihull | 8 | YES |
| Greater Manchester - Manchester & Salford | 7 | YES |
| Kent | 7 | YES |
| Essex | 7 | YES |
| Staffordshire | 7 | YES |
| Norfolk | 7 | YES |
| Hertfordshire | 6 | YES |
| Bristol & Bath | 6 | YES |
| North East | 5 | YES |
| Gloucestershire | 5 | YES |
| Somerset | 4 | YES |
| West Midlands - Coventry & Warwickshire | 4 | YES |
| Cheshire - Warrington & Halton | 4 | YES |
| Buckinghamshire | 4 | YES |
| Devon | 3 | YES |
| Leicestershire | 3 | YES |
| Lincolnshire | 3 | YES |
| Nottinghamshire | 3 | YES |
| Yorkshire - South | 3 | YES |
| Sussex | 3 | YES |
| Yorkshire - North | 3 | YES |
| East Midlands | 3 | NO |
| Greater Manchester - Wigan & Bolton | 3 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

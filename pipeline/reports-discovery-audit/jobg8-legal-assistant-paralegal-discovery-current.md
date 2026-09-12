# JobG8 Legal Assistant / Paralegal family discovery

Feed: **2026-09-12.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **302**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **302**
Additional cross-reference content duplicates: **5**
Content-unique broad universe: **297**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **248**
Provisional BORDERLINE: **8**
Provisional OUT (specialist/salary): **41**
Estimated genuine inventory before deep advert review: **~252** (working range **248–256**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 248 |
| OUT_SPECIALIST | 31 |
| OUT_SALARY | 10 |
| BORDERLINE | 8 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 178 |
| £25k–£30k | 59 |
| £30k–£40k | 30 |
| <£25k | 13 |
| >£50,000 OUT | 10 |
| £40k–£50,000 | 7 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Legal | 288 |
| Administration | 6 |
| Call Centre / CustomerService | 1 |
| Banking & Financial Services | 1 |
| Real Estate & Property | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **291**.
Content-unique candidates outside it or unresolved: **6**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 62 | YES |
| Greater Manchester - Manchester & Salford | 17 | YES |
| Kent | 15 | YES |
| Northern Ireland - East | 15 | YES |
| Yorkshire - West | 13 | YES |
| West Midlands - Birmingham & Solihull | 12 | YES |
| Surrey | 11 | YES |
| Nottinghamshire | 9 | YES |
| Yorkshire - North | 9 | YES |
| Sussex | 8 | YES |
| Bristol & Bath | 7 | YES |
| Merseyside - Liverpool | 6 | YES |
| Essex | 6 | YES |
| Dorset | 6 | YES |
| Leicestershire | 5 | YES |
| Yorkshire - South | 5 | YES |
| Other / Unknown | 5 | NO |
| Derbyshire | 4 | YES |
| Worcestershire | 4 | YES |
| West Midlands - Black Country | 4 | YES |
| North East | 4 | YES |
| Wiltshire | 4 | YES |
| Suffolk | 3 | YES |
| West Midlands - Coventry & Warwickshire | 3 | YES |
| Cheshire - West | 3 | YES |
| Lincolnshire | 3 | YES |
| Wales South - Cardiff & Vale | 3 | YES |
| Cheshire - Warrington & Halton | 3 | YES |
| Bedfordshire | 3 | YES |
| Shropshire | 3 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

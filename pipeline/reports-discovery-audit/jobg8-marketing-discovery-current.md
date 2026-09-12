# JobG8 Marketing family discovery

Feed: **2026-09-12.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **456**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **456**
Additional cross-reference content duplicates: **8**
Content-unique broad universe: **448**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **241**
Provisional BORDERLINE: **111**
Provisional OUT (specialist/salary): **96**
Estimated genuine inventory before deep advert review: **~297** (working range **241–352**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 241 |
| BORDERLINE | 111 |
| OUT_SALARY | 72 |
| OUT_SPECIALIST | 24 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 197 |
| £30k–£40k | 96 |
| >£50,000 OUT | 71 |
| £40k–£50,000 | 37 |
| £25k–£30k | 35 |
| <£25k | 12 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Sales & Marketing | 401 |
| Advert / Media / Entertainment | 18 |
| I.T. & Communications | 11 |
| Administration | 6 |
| Retail & Consumer Products | 5 |
| Call Centre / CustomerService | 3 |
| HR / Recruitment | 2 |
| Legal | 1 |
| Consulting & Corporate Strategy | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **422**.
Content-unique candidates outside it or unresolved: **26**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 127 | YES |
| Other / Unknown | 22 | NO |
| Surrey | 21 | YES |
| Greater Manchester - Manchester & Salford | 15 | YES |
| Berkshire | 15 | YES |
| Yorkshire - West | 13 | YES |
| Kent | 12 | YES |
| Greater Manchester - South | 12 | YES |
| Yorkshire - North | 12 | YES |
| Gloucestershire | 11 | YES |
| Oxfordshire | 10 | YES |
| Bristol & Bath | 10 | YES |
| West Midlands - Birmingham & Solihull | 10 | YES |
| Hertfordshire | 9 | YES |
| Merseyside - Liverpool | 8 | YES |
| Northern Ireland - East | 8 | YES |
| Wiltshire | 8 | YES |
| Devon | 7 | YES |
| Hampshire | 7 | YES |
| Buckinghamshire | 7 | YES |
| Sussex | 7 | YES |
| Essex | 7 | YES |
| North East | 6 | YES |
| Cheshire - Warrington & Halton | 6 | YES |
| West Midlands - Coventry & Warwickshire | 6 | YES |
| Cambridgeshire | 6 | YES |
| Norfolk | 6 | YES |
| Yorkshire - South | 5 | YES |
| Somerset | 5 | YES |
| Cheshire - West | 4 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

# JobG8 Marketing family discovery

Feed: **2026-09-21.xlsx**
Jobs in feed: **17,785**
Raw broad possible universe before exclusions/dedupe: **321**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **321**
Additional cross-reference content duplicates: **18**
Content-unique broad universe: **303**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **168**
Provisional BORDERLINE: **78**
Provisional OUT (specialist/salary): **57**
Estimated genuine inventory before deep advert review: **~207** (working range **168–246**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 168 |
| BORDERLINE | 78 |
| OUT_SALARY | 42 |
| OUT_SPECIALIST | 15 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 165 |
| £30k–£40k | 57 |
| >£50,000 OUT | 41 |
| £40k–£50,000 | 27 |
| £25k–£30k | 9 |
| <£25k | 4 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Sales & Marketing | 265 |
| I.T. & Communications | 25 |
| Advert / Media / Entertainment | 7 |
| Transport & Logistics | 2 |
| Community & Sport | 1 |
| Education | 1 |
| Call Centre / CustomerService | 1 |
| Retail & Consumer Products | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **271**.
Content-unique candidates outside it or unresolved: **32**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 83 | YES |
| Other / Unknown | 27 | NO |
| Surrey | 15 | YES |
| Berkshire | 12 | YES |
| West Midlands - Birmingham & Solihull | 11 | YES |
| Oxfordshire | 9 | YES |
| Yorkshire - West | 9 | YES |
| Merseyside - Liverpool | 8 | YES |
| Kent | 7 | YES |
| Essex | 7 | YES |
| Staffordshire | 7 | YES |
| Norfolk | 7 | YES |
| Greater Manchester - Manchester & Salford | 6 | YES |
| Hertfordshire | 6 | YES |
| Bristol & Bath | 6 | YES |
| Gloucestershire | 6 | YES |
| Cheshire - Warrington & Halton | 5 | YES |
| North East | 5 | YES |
| Somerset | 4 | YES |
| West Midlands - Coventry & Warwickshire | 4 | YES |
| Sussex | 4 | YES |
| Buckinghamshire | 4 | YES |
| Devon | 3 | YES |
| Leicestershire | 3 | YES |
| Hampshire | 3 | YES |
| Lincolnshire | 3 | YES |
| Yorkshire - North | 3 | YES |
| East Midlands | 3 | NO |
| Greater Manchester - Wigan & Bolton | 3 | YES |
| Northern Ireland - East | 3 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

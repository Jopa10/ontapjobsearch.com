# JobG8 Marketing family discovery

Feed: **2026-09-02.xlsx**
Jobs in feed: **10,000**
Raw broad possible universe before exclusions/dedupe: **457**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **457**
Additional cross-reference content duplicates: **11**
Content-unique broad universe: **446**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **219**
Provisional BORDERLINE: **105**
Provisional OUT (specialist/salary): **122**
Estimated genuine inventory before deep advert review: **~271** (working range **219–324**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 219 |
| BORDERLINE | 105 |
| OUT_SALARY | 89 |
| OUT_SPECIALIST | 33 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 147 |
| £30k–£40k | 91 |
| >£50,000 OUT | 87 |
| £25k–£30k | 60 |
| £40k–£50,000 | 51 |
| <£25k | 10 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Sales & Marketing | 393 |
| Advert / Media / Entertainment | 25 |
| I.T. & Communications | 12 |
| Administration | 5 |
| Retail & Consumer Products | 3 |
| Executive Positions | 2 |
| Banking & Financial Services | 2 |
| Consulting & Corporate Strategy | 1 |
| Legal | 1 |
| Call Centre / CustomerService | 1 |
| Science & Technology | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **419**.
Content-unique candidates outside it or unresolved: **27**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 109 | YES |
| Greater Manchester - Manchester & Salford | 31 | YES |
| Other / Unknown | 24 | NO |
| Yorkshire - West | 20 | YES |
| Berkshire | 16 | YES |
| Buckinghamshire | 14 | YES |
| Yorkshire - North | 13 | YES |
| Hampshire | 11 | YES |
| Hertfordshire | 11 | YES |
| Surrey | 10 | YES |
| Oxfordshire | 10 | YES |
| Kent | 9 | YES |
| North East | 9 | YES |
| Devon | 8 | YES |
| Yorkshire - South | 8 | YES |
| Bristol & Bath | 8 | YES |
| Gloucestershire | 8 | YES |
| Cambridgeshire | 8 | YES |
| Dorset | 6 | YES |
| Cheshire - West | 6 | YES |
| Nottinghamshire | 6 | YES |
| Sussex | 5 | YES |
| Essex | 5 | YES |
| West Midlands - Birmingham & Solihull | 5 | YES |
| Merseyside - Liverpool | 5 | YES |
| Leicestershire | 5 | YES |
| Lincolnshire | 4 | YES |
| Greater Manchester - South | 4 | YES |
| Lancashire - East | 4 | YES |
| Derbyshire | 4 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

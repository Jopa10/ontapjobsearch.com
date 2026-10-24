# JobG8 Marketing family discovery

Feed: **2026-10-24.xlsx**
Jobs in feed: **20,000**
Raw broad possible universe before exclusions/dedupe: **520**
Reference-key duplicates within broad universe: **0**
Reference-deduped broad universe: **520**
Additional cross-reference content duplicates: **25**
Content-unique broad universe: **495**

This is discovery evidence only. JobG8 classification is reported but never used as a candidate gate.
All source rows remain in the CSV with duplicate flags; viability, geography and recurrence use content-unique adverts.
Salary rule applied diagnostically: **over £50,000 = OUT; exactly £50,000 is not excluded; missing salary is retained.**

## Early volume viability gate

Provisional LIKELY_IN: **278**
Provisional BORDERLINE: **115**
Provisional OUT (specialist/salary): **102**
Estimated genuine inventory before deep advert review: **~336** (working range **278–393**).
Viability floor: **~100 genuine jobs nationally**.
Early verdict: **GO / SCALE CLEAR**.

## Provisional decision breakdown

| Decision | Content-unique jobs |
|---|---:|
| LIKELY_IN | 278 |
| BORDERLINE | 115 |
| OUT_SALARY | 88 |
| OUT_SPECIALIST | 14 |

## Salary distribution — content-unique broad universe

| Salary bucket | Jobs |
|---|---:|
| missing/unknown | 175 |
| £30k–£40k | 112 |
| >£50,000 OUT | 88 |
| £40k–£50,000 | 59 |
| £25k–£30k | 56 |
| <£25k | 5 |

## JobG8 classifications feeding the seam

Classification column: **/Job/Classification**

| JobG8 classification | Jobs |
|---|---:|
| Sales & Marketing | 446 |
| Advert / Media / Entertainment | 18 |
| Community & Sport | 9 |
| Accounting | 6 |
| Administration | 6 |
| HR / Recruitment | 3 |
| Legal | 2 |
| Healthcare & Medical | 2 |
| I.T. & Communications | 2 |
| Call Centre / CustomerService | 1 |

## Geography — evidence only, not an occupational gate

Canonical UK assessment universe: **78 markets**.
Content-unique candidates mapping into that UK market universe: **448**.
Content-unique candidates outside it or unresolved: **47**.
The national occupational discovery count above is not reduced by geography. Geography is used only to describe spread after occupational candidate discovery.
Exact detail aliases are rolled up to their canonical UK assessment market; ambiguous generic geo values remain unresolved rather than being forced into the wrong market.

| Assessable market / geo result | Jobs | In UK market universe? |
|---|---:|---|
| London | 97 | YES |
| Other / Unknown | 46 | NO |
| Greater Manchester - Manchester & Salford | 34 | YES |
| Nottinghamshire | 24 | YES |
| Yorkshire - West | 20 | YES |
| Surrey | 17 | YES |
| Hertfordshire | 15 | YES |
| Kent | 15 | YES |
| Berkshire | 15 | YES |
| Sussex | 13 | YES |
| West Midlands - Coventry & Warwickshire | 13 | YES |
| Buckinghamshire | 12 | YES |
| Cambridgeshire | 11 | YES |
| West Midlands - Birmingham & Solihull | 11 | YES |
| Hampshire | 10 | YES |
| Northamptonshire | 9 | YES |
| North East | 9 | YES |
| Oxfordshire | 9 | YES |
| Scotland West - Glasgow | 8 | YES |
| Bristol & Bath | 7 | YES |
| Essex | 6 | YES |
| Yorkshire - South | 6 | YES |
| Leicestershire | 6 | YES |
| Dorset | 6 | YES |
| Somerset | 5 | YES |
| Cheshire - East | 4 | YES |
| Yorkshire - North | 4 | YES |
| Devon | 4 | YES |
| Norfolk | 4 | YES |
| Bedfordshire | 4 | YES |

## Next gate

If the early verdict is STOP / VERY THIN or CAUTION / LIKELY BELOW GATE, do not spend time on full advert-level boundary work yet.
If scale is plausible, use the candidate CSV for advert-level IN / BORDERLINE / OUT review, freeze reusable family rules, then validate the frozen selector against the whole feed before any 78-market UK recurrence/slice assessment.

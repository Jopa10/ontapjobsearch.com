# Ontap daily regional overview

Generated: 2026-08-22T15:00:30+00:00

> LIVE Service Admin and Support Worker counts reconcile to `pipeline/reports-daily/live-job-source-count-2026-08-22.csv` on `main`. LIVE Sales Advisor counts come from the current published Customer Sales configured-slice JSON on `main`. NOT LIVE Service Admin and Support Worker were assessed from the same JobG8 daily feed (2026-08-22) used by the production family run, across all 33 canonical regions with the config-driven production wrappers, persistent review decisions and canonical geo. NOT LIVE Sales Advisor was assessed from that same feed across all 33 regions using the governed Customer Sales classifier, canonical geo, campaign dedupe and final production QA. Sales diagnostic counts are evidence only and never activate a slice automatically; LIVE Sales Advisor counts continue to come from the current published Customer Sales configured-slice JSON. Rolling family history stores one snapshot per feed date, replaces same-date reruns, retains the latest 14 feed dates and is used only as decision evidence for NOT LIVE slices.

## LIVE

| Region | Service admin | Support worker | Sales advisor |
|---|---:|---:|---:|
| Berkshire | 39 |  |  |
| Bristol & Bath | 35 |  |  |
| Buckinghamshire | 18 |  |  |
| Cambridgeshire | 41 |  |  |
| Cumbria - North |  |  |  |
| Cumbria - South |  | 2 |  |
| Devon | 45 |  |  |
| Dorset | 23 |  |  |
| Essex | 46 |  |  |
| Gloucestershire | 23 |  |  |
| Greater Manchester - Manchester & Salford | 35 |  | 6 |
| Greater Manchester - South | 13 |  |  |
| Hampshire | 57 | 13 |  |
| Hertfordshire | 22 |  |  |
| Kent | 57 |  |  |
| Lancashire - North |  |  |  |
| London | 161 | 14 | 20 |
| Norfolk | 19 |  |  |
| North East | 30 | 6 |  |
| Northamptonshire | 30 |  |  |
| Nottinghamshire | 24 |  |  |
| Oxfordshire | 50 |  |  |
| Somerset | 16 |  |  |
| Staffordshire | 18 |  |  |
| Surrey | 71 | 12 |  |
| Sussex | 34 | 13 |  |
| West Midlands - Birmingham & Solihull | 26 |  |  |
| West Midlands - Coventry & Warwickshire | 31 |  |  |
| Wiltshire | 29 | 4 |  |
| Yorkshire - East | 14 |  |  |
| Yorkshire - North | 21 |  |  |
| Yorkshire - South | 29 | 2 |  |
| Yorkshire - West | 61 | 2 | 7 |

## NOT LIVE

> Cells show `today / 14d avg / 6+ days` over observed feed dates (maximum 14). The 6+ measure is a watch signal only, not an automatic activation threshold.

| Region | Service admin | Support worker | Sales advisor |
|---|---:|---:|---:|
| Berkshire |  | 1 / 1.0 / 0/1 | 1 / 1.0 / 0/1 |
| Bristol & Bath |  | 1 / 1.0 / 0/1 | 5 / 5.0 / 0/1 |
| Buckinghamshire |  | 2 / 2.0 / 0/1 | 2 / 2.0 / 0/1 |
| Cambridgeshire |  | 0 / 0.0 / 0/1 | 5 / 5.0 / 0/1 |
| Cumbria - North | 3 / 3.0 / 0/1 | 6 / 6.0 / 1/1 | 0 / 0.0 / 0/1 |
| Cumbria - South | 2 / 2.0 / 0/1 |  | 1 / 1.0 / 0/1 |
| Devon |  | 0 / 0.0 / 0/1 | 2 / 2.0 / 0/1 |
| Dorset |  | 1 / 1.0 / 0/1 | 4 / 4.0 / 0/1 |
| Essex |  | 1 / 1.0 / 0/1 | 4 / 4.0 / 0/1 |
| Gloucestershire |  | 1 / 1.0 / 0/1 | 3 / 3.0 / 0/1 |
| Greater Manchester - Manchester & Salford |  | 0 / 0.0 / 0/1 |  |
| Greater Manchester - South |  | 1 / 1.0 / 0/1 | 1 / 1.0 / 0/1 |
| Hampshire |  |  | 4 / 4.0 / 0/1 |
| Hertfordshire |  | 3 / 3.0 / 0/1 | 4 / 4.0 / 0/1 |
| Kent |  | 4 / 4.0 / 0/1 | 5 / 5.0 / 0/1 |
| Lancashire - North | 1 / 1.0 / 0/1 | 1 / 1.0 / 0/1 | 0 / 0.0 / 0/1 |
| London |  |  |  |
| Norfolk |  | 1 / 1.0 / 0/1 | 4 / 4.0 / 0/1 |
| North East |  |  | 6 / 6.0 / 1/1 |
| Northamptonshire |  | 0 / 0.0 / 0/1 | 4 / 4.0 / 0/1 |
| Nottinghamshire |  | 2 / 2.0 / 0/1 | 3 / 3.0 / 0/1 |
| Oxfordshire |  | 3 / 3.0 / 0/1 | 1 / 1.0 / 0/1 |
| Somerset |  | 3 / 3.0 / 0/1 | 0 / 0.0 / 0/1 |
| Staffordshire |  | 0 / 0.0 / 0/1 | 0 / 0.0 / 0/1 |
| Surrey |  |  | 5 / 5.0 / 0/1 |
| Sussex |  |  | 3 / 3.0 / 0/1 |
| West Midlands - Birmingham & Solihull |  | 1 / 1.0 / 0/1 | 5 / 5.0 / 0/1 |
| West Midlands - Coventry & Warwickshire |  | 0 / 0.0 / 0/1 | 1 / 1.0 / 0/1 |
| Wiltshire |  |  | 3 / 3.0 / 0/1 |
| Yorkshire - East |  | 1 / 1.0 / 0/1 | 3 / 3.0 / 0/1 |
| Yorkshire - North |  | 5 / 5.0 / 0/1 | 0 / 0.0 / 0/1 |
| Yorkshire - South |  |  | 5 / 5.0 / 0/1 |
| Yorkshire - West |  |  |  |

## HEADLINE

| Measure | Service admin | Support worker | Sales advisor |
|---|---:|---:|---:|
| Live regions | 30 / 33 | 9 / 33 | 3 / 33 |
| Live jobs | 1118 | 68 | 33 |

**Live slices: 42 / 99.**

# Ontap daily regional overview

Production source commit: `bbd0f37a060131727042827513277b2bc116c2fa`

Generated: 2026-11-12T09:09:46+00:00

[Download this overview as Excel](./daily-region-overview.xlsx)

## SITEWIDE RECONCILIATION

| Measure | Count |
|---|---:|
| Unique live jobs | 5,750 |
| Unique JobG8 jobs | 5,392 |
| Unique non-JobG8 jobs | 358 |
| Regional/category slice placements | 7,165 |
| Jobs appearing on multiple slices | 1,400 |
| Extra slice placements | 1,415 |
| Unique jobs outside governed slices | 0 |
| Jobs found in non-LIVE slices | 0 |

**Reconciliation: 5,750 unique jobs + 1,415 extra slice placements = 7,165 regional/category slice placements.**

Latest source-count CSV: `pipeline/reports-daily/live-job-source-count-2026-11-12.csv` — **STALE — CSV says 5,896 for 2026-11-12**.

### Provider breakdown

| Provider | Unique live jobs | Jobs on 2+ slices | Extra slice placements |
|---|---:|---:|---:|
| JobG8 | 5,392 | 1,400 | 1,415 |
| NHS Jobs | 291 | 0 | 0 |
| Teaching Vacancies | 67 | 0 | 0 |

## JOBG8 FEED RECEIVED

**JobG8 jobs received: 43,462** (feed date: 2026-11-12)

| JobG8 classification | Jobs received | Ontap jobs classified/published |
|---|---:|---:|
| Education | 9,994 | 67 |
| Transport & Logistics | 7,135 | 151 |
| Accounting | 6,722 | 1,430 |
| Healthcare & Medical | 4,148 | 385 |
| Sales & Marketing | 4,061 | 1,045 |
| Legal | 2,693 | 448 |
| Administration | 1,746 | 1,159 |
| Real Estate & Property | 1,445 | 90 |
| HR / Recruitment | 1,350 | 180 |
| I.T. & Communications | 1,243 | 3 |
| Call Centre / CustomerService | 818 | 368 |
| Insurance & Superannuation | 652 | 22 |
| Community & Sport | 581 | 59 |
| Banking & Financial Services | 477 | 12 |
| Government & Defence | 257 | 7 |
| Advert / Media / Entertainment | 140 | 21 |
| Total across classifications | 43,462 | 5,447 |

## JOBG8 XML RECONCILIATION

| Check | XML feed total | Sum of ‘Jobs received’ | Difference (sum − XML) | Result |
|---|---:|---:|---:|---|
| JobG8 feed categories | 43,462 | 43,462 | 0 | **PASS** |

**JobG8 feed reconciliation: PASS.** Difference is 0 jobs (summed categories minus XML total).

## JOBG8 LAST 10 FEED DATES — TOTALS ONLY

Saved history contains 10 of the latest 10 feed dates. Older feed totals were not saved and are not backfilled.

| Feed date | JobG8 jobs received | Ontap jobs classified/published |
|---|---:|---:|
| 2026-11-12 | 43,462 | 5,447 |
| 2026-11-11 | 44,280 | 5,491 |
| 2026-11-10 | 46,440 | 5,541 |
| 2026-11-09 | 45,751 | 5,414 |
| 2026-11-08 | 45,971 | 5,412 |
| 2026-11-07 | 46,633 | 5,494 |
| 2026-11-06 | 43,409 | 4,904 |
| 2026-11-05 | 43,391 | 4,946 |
| 2026-11-04 | 41,409 | 4,684 |
| 2026-11-03 | 44,432 | 4,974 |

## JOBG8 LAST 10 FEED DATES — SELECTED JOBS BY CLASSIFICATION

Each dated column shows Ontap jobs classified/published in that JobG8 classification.

| JobG8 classification | 2026-11-12 | 2026-11-11 | 2026-11-10 | 2026-11-09 | 2026-11-08 | 2026-11-07 | 2026-11-06 | 2026-11-05 | 2026-11-04 | 2026-11-03 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Accounting | 1430 | 1452 | 1462 | 1435 | 1433 | 1450 | 1167 | 1180 | 1125 | 1200 |
| Administration | 1159 | 1154 | 1177 | 1138 | 1139 | 1167 | 1130 | 1148 | 1057 | 1151 |
| Advert / Media / Entertainment | 21 | 19 | 18 | 19 | 19 | 21 | 23 | 24 | 24 | 26 |
| Banking & Financial Services | 12 | 12 | 13 | 12 | 13 | 12 | 13 | 14 | 13 | 15 |
| Call Centre / CustomerService | 368 | 358 | 426 | 409 | 411 | 425 | 418 | 422 | 395 | 414 |
| Community & Sport | 59 | 58 | 59 | 54 | 57 | 55 | 56 | 58 | 57 | 53 |
| Education | 67 | 70 | 70 | 65 | 65 | 69 | 66 | 68 | 62 | 66 |
| Government & Defence | 7 | 7 | 6 | 5 | 5 | 5 | 6 | 4 | 4 | 4 |
| Healthcare & Medical | 385 | 407 | 409 | 406 | 408 | 410 | 412 | 406 | 388 | 386 |
| HR / Recruitment | 180 | 182 | 183 | 184 | 186 | 190 | 192 | 198 | 186 | 203 |
| I.T. & Communications | 3 | 7 | 36 | 37 | 37 | 37 | 34 | 35 | 33 | 39 |
| Insurance & Superannuation | 22 | 23 | 20 | 19 | 19 | 20 | 17 | 17 | 17 | 19 |
| Legal | 448 | 435 | 402 | 397 | 396 | 397 | 294 | 296 | 287 | 294 |
| Real Estate & Property | 90 | 93 | 88 | 91 | 91 | 89 | 75 | 73 | 70 | 80 |
| Sales & Marketing | 1045 | 1059 | 1013 | 988 | 980 | 990 | 855 | 857 | 828 | 871 |
| Transport & Logistics | 151 | 155 | 159 | 155 | 153 | 157 | 146 | 146 | 138 | 153 |

## PAGES

**Published/indexable URLs: 6,128** — 5,750 individual job pages, 258 regional/category pages, 112 city pages and 8 core pages.

| Level | Page type | Area | Family | URL | Page count | Live jobs | In sitemap |
|---|---|---|---|---|---:|---:|---|
| Summary | All published/indexable URLs | Sitewide |  |  | 6,128 |  | Yes |
| Summary | Individual job | Sitewide |  | /jobs/[id] | 5,750 | 5,750 | Yes |
| Summary | Regional/category | Sitewide |  | Multiple | 258 |  | Yes |
| Summary | City | Sitewide |  | Multiple | 112 |  | Yes |
| Summary | Core | Sitewide |  | Multiple | 8 |  | Yes |
| Detail | Core | Sitewide |  | / | 1 |  | Yes |
| Detail | Core | Sitewide |  | /browse-jobs | 1 |  | Yes |
| Detail | Core | Sitewide |  | /about | 1 |  | Yes |
| Detail | Regional/category | Ai At Work | Ai At Work | /ai-at-work | 1 |  | Yes |
| Detail | Regional/category | Ai At Work | Reception And Office Admin | /ai-at-work/reception-and-office-admin | 1 |  | Yes |
| Detail | Regional/category | Ai At Work | Accounts And Finance Admin | /ai-at-work/accounts-and-finance-admin | 1 |  | Yes |
| Detail | Regional/category | Ai At Work | Ai Job Advert Watch | /ai-at-work/ai-job-advert-watch | 1 |  | Yes |
| Detail | Regional/category | Ai At Work | October 2026 | /ai-at-work/ai-job-advert-watch/october-2026 | 1 |  | Yes |
| Detail | Core | Sitewide |  | /ai-tips | 1 |  | Yes |
| Detail | Regional/category | Ai Course Reviews | Ai Course Reviews | /ai-course-reviews | 1 |  | Yes |
| Detail | Core | Sitewide |  | /contact | 1 |  | Yes |
| Detail | Core | Sitewide |  | /privacy-policy | 1 |  | Yes |
| Detail | Core | Sitewide |  | /terms-of-service | 1 |  | Yes |
| Detail | Core | Sitewide |  | /sector-switching | 1 |  | Yes |
| Detail | Regional/category | West Yorkshire | Support Worker | /west-yorkshire/support-worker | 1 | 7 | Yes |
| Detail | Regional/category | South Yorkshire | Support Worker | /south-yorkshire/support-worker | 1 | 3 | Yes |
| Detail | Regional/category | North East | Support Worker | /north-east/support-worker | 1 | 21 | Yes |
| Detail | Regional/category | Sussex | Support Worker | /sussex/support-worker | 1 | 37 | Yes |
| Detail | Regional/category | Cumbria South | Support Worker | /cumbria-south/support-worker | 1 | 4 | Yes |
| Detail | Regional/category | Hampshire | Support Worker | /hampshire/support-worker | 1 | 27 | Yes |
| Detail | Regional/category | West Yorkshire | Service Administrator Jobs | /west-yorkshire/service-administrator-jobs | 1 | 157 | Yes |
| Detail | Regional/category | South Yorkshire | Service Administrator Jobs | /south-yorkshire/service-administrator-jobs | 1 | 65 | Yes |
| Detail | Regional/category | North Yorkshire | Service Administrator Jobs | /north-yorkshire/service-administrator-jobs | 1 | 42 | Yes |
| Detail | Regional/category | North East | Service Administrator Jobs | /north-east/service-administrator-jobs | 1 | 94 | Yes |
| Detail | Regional/category | London | Service Administrator Jobs | /london/service-administrator-jobs | 1 | 427 | Yes |
| Detail | Regional/category | London | Central Service Administrator Jobs | /london/central-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | North Service Administrator Jobs | /london/north-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | East Service Administrator Jobs | /london/east-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | South Service Administrator Jobs | /london/south-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | West Service Administrator Jobs | /london/west-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | Hampshire | Service Administrator Jobs | /hampshire/service-administrator-jobs | 1 | 148 | Yes |
| Detail | Regional/category | Coventry Warwickshire | Service Administrator Jobs | /coventry-warwickshire/service-administrator-jobs | 1 | 84 | Yes |
| Detail | Regional/category | Surrey | Service Administrator Jobs | /surrey/service-administrator-jobs | 1 | 137 | Yes |
| Detail | Regional/category | Kent | Service Administrator Jobs | /kent/service-administrator-jobs | 1 | 137 | Yes |
| Detail | Regional/category | Sussex | Service Administrator Jobs | /sussex/service-administrator-jobs | 1 | 104 | Yes |
| Detail | City | Newcastle | admin and office jobs | /newcastle/service-administrator-jobs | 1 | 20 | Yes |
| Detail | City | Southampton | support worker jobs | /southampton/support-worker | 1 | 4 | Yes |
| Detail | City | Sheffield | admin and office jobs | /sheffield/service-administrator-jobs | 1 | 39 | Yes |
| Detail | City | Leeds | admin and office jobs | /leeds/service-administrator-jobs | 1 | 95 | Yes |
| Detail | City | Coventry | admin and office jobs | /coventry/service-administrator-jobs | 1 | 18 | Yes |
| Detail | City | Southampton | admin and office jobs | /southampton/service-administrator-jobs | 1 | 16 | Yes |
| Detail | City | Brighton & Hove | admin and office jobs | /brighton-hove/service-administrator-jobs | 1 | 14 | Yes |
| Detail | City | Bradford | admin and office jobs | /bradford/service-administrator-jobs | 1 | 33 | Yes |
| Detail | City | Huddersfield | admin and office jobs | /huddersfield/service-administrator-jobs | 1 | 22 | Yes |
| Detail | City | York | admin and office jobs | /york/service-administrator-jobs | 1 | 12 | Yes |
| Detail | City | Barnsley | admin and office jobs | /barnsley/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Doncaster | admin and office jobs | /doncaster/service-administrator-jobs | 1 | 20 | Yes |
| Detail | City | Bristol | admin and office jobs | /bristol/service-administrator-jobs | 1 | 66 | Yes |
| Detail | City | Manchester | admin and office jobs | /manchester/service-administrator-jobs | 1 | 141 | Yes |
| Detail | City | Cambridge | admin and office jobs | /cambridge/service-administrator-jobs | 1 | 50 | Yes |
| Detail | City | Birmingham | admin and office jobs | /birmingham/service-administrator-jobs | 1 | 133 | Yes |
| Detail | City | Peterborough | admin and office jobs | /peterborough/service-administrator-jobs | 1 | 26 | Yes |
| Detail | City | Warrington | admin and office jobs | /warrington/service-administrator-jobs | 1 | 29 | Yes |
| Detail | City | Liverpool | admin and office jobs | /liverpool/service-administrator-jobs | 1 | 52 | Yes |
| Detail | City | Hull | admin and office jobs | /hull/service-administrator-jobs | 1 | 23 | Yes |
| Detail | City | Oxford | admin and office jobs | /oxford/service-administrator-jobs | 1 | 12 | Yes |
| Detail | City | Belfast | admin and office jobs | /belfast/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Glasgow | admin and office jobs | /glasgow/service-administrator-jobs | 1 | 27 | Yes |
| Detail | City | Edinburgh | admin and office jobs | /edinburgh/service-administrator-jobs | 1 | 29 | Yes |
| Detail | City | Cardiff | admin and office jobs | /cardiff/service-administrator-jobs | 1 | 19 | Yes |
| Detail | City | Exeter | admin and office jobs | /exeter/service-administrator-jobs | 1 | 28 | Yes |
| Detail | City | Milton Keynes | admin and office jobs | /milton-keynes/service-administrator-jobs | 1 | 23 | Yes |
| Detail | City | Farnham | admin and office jobs | /farnham/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Northampton | admin and office jobs | /northampton/service-administrator-jobs | 1 | 15 | Yes |
| Detail | City | Poole | admin and office jobs | /poole/service-administrator-jobs | 1 | 15 | Yes |
| Detail | City | Portsmouth | admin and office jobs | /portsmouth/service-administrator-jobs | 1 | 11 | Yes |
| Detail | City | Stoke-on-trent | admin and office jobs | /stoke-on-trent/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Hemel Hempstead | admin and office jobs | /hemel-hempstead/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Basingstoke | admin and office jobs | /basingstoke/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Chelmsford | admin and office jobs | /chelmsford/service-administrator-jobs | 1 | 16 | Yes |
| Detail | City | Gloucester | admin and office jobs | /gloucester/service-administrator-jobs | 1 | 18 | Yes |
| Detail | City | Leicester | admin and office jobs | /leicester/service-administrator-jobs | 1 | 26 | Yes |
| Detail | City | Maidstone | admin and office jobs | /maidstone/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Newtownabbey | admin and office jobs | /newtownabbey/service-administrator-jobs | 1 | 0 | Yes |
| Detail | City | Plymouth | admin and office jobs | /plymouth/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Sunderland | admin and office jobs | /sunderland/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Worcester | admin and office jobs | /worcester/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Altrincham | admin and office jobs | /altrincham/service-administrator-jobs | 1 | 18 | Yes |
| Detail | City | Ashford | admin and office jobs | /ashford/service-administrator-jobs | 1 | 10 | Yes |
| Detail | City | Aylesbury | admin and office jobs | /aylesbury/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Bedford | admin and office jobs | /bedford/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Bournemouth | admin and office jobs | /bournemouth/service-administrator-jobs | 1 | 10 | Yes |
| Detail | City | Chester Le Street | admin and office jobs | /chester-le-street/service-administrator-jobs | 1 | 0 | Yes |
| Detail | City | Macclesfield | admin and office jobs | /macclesfield/service-administrator-jobs | 1 | 15 | Yes |
| Detail | City | Rotherham | admin and office jobs | /rotherham/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Scarborough | admin and office jobs | /scarborough/service-administrator-jobs | 1 | 3 | Yes |
| Detail | City | Shrewsbury | admin and office jobs | /shrewsbury/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Warwick | admin and office jobs | /warwick/service-administrator-jobs | 1 | 18 | Yes |
| Detail | City | Wigston | admin and office jobs | /wigston/service-administrator-jobs | 1 | 0 | Yes |
| Detail | City | Dartford | admin and office jobs | /dartford/service-administrator-jobs | 1 | 12 | Yes |
| Detail | City | Stockport | admin and office jobs | /stockport/service-administrator-jobs | 1 | 18 | Yes |
| Detail | City | Swansea | admin and office jobs | /swansea/service-administrator-jobs | 1 | 10 | Yes |
| Detail | City | Walsall | admin and office jobs | /walsall/service-administrator-jobs | 1 | 10 | Yes |
| Detail | City | Bath | admin and office jobs | /bath/service-administrator-jobs | 1 | 10 | Yes |
| Detail | City | Eastleigh | admin and office jobs | /eastleigh/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Harrogate | admin and office jobs | /harrogate/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Watford | admin and office jobs | /watford/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Crawley | admin and office jobs | /crawley/service-administrator-jobs | 1 | 11 | Yes |
| Detail | City | Swindon | admin and office jobs | /swindon/service-administrator-jobs | 1 | 20 | Yes |
| Detail | City | Horsham | admin and office jobs | /horsham/service-administrator-jobs | 1 | 3 | Yes |
| Detail | City | Lincoln | admin and office jobs | /lincoln/service-administrator-jobs | 1 | 38 | Yes |
| Detail | City | Nottingham | All roles | /nottingham/jobs | 1 |  | Yes |
| Detail | City | Wakefield | All roles | /wakefield/jobs | 1 |  | Yes |
| Detail | City | Bolton | All roles | /bolton/jobs | 1 |  | Yes |
| Detail | City | Reading | All roles | /reading/jobs | 1 |  | Yes |
| Detail | City | Chester | All roles | /chester/jobs | 1 |  | Yes |
| Detail | City | Durham | All roles | /durham/jobs | 1 |  | Yes |
| Detail | City | Gateshead | All roles | /gateshead/jobs | 1 |  | Yes |
| Detail | City | Northallerton | All roles | /northallerton/jobs | 1 |  | Yes |
| Detail | City | Norwich | All roles | /norwich/jobs | 1 |  | Yes |
| Detail | City | Salford | All roles | /salford/jobs | 1 |  | Yes |
| Detail | City | Redditch | All roles | /redditch/jobs | 1 |  | Yes |
| Detail | City | Guildford | All roles | /guildford/jobs | 1 |  | Yes |
| Detail | City | Carlisle | All roles | /carlisle/jobs | 1 |  | Yes |
| Detail | City | Preston | All roles | /preston/jobs | 1 |  | Yes |
| Detail | City | Witney | All roles | /witney/jobs | 1 |  | Yes |
| Detail | City | Yeovil | All roles | /yeovil/jobs | 1 |  | Yes |
| Detail | City | Hertford | All roles | /hertford/jobs | 1 |  | Yes |
| Detail | City | Leatherhead | All roles | /leatherhead/jobs | 1 |  | Yes |
| Detail | City | Rugby | All roles | /rugby/jobs | 1 |  | Yes |
| Detail | City | Colchester | All roles | /colchester/jobs | 1 |  | Yes |
| Detail | City | Hereford | All roles | /hereford/jobs | 1 |  | Yes |
| Detail | City | Stafford | All roles | /stafford/jobs | 1 |  | Yes |
| Detail | City | Ipswich | All roles | /ipswich/jobs | 1 |  | Yes |
| Detail | City | Solihull | All roles | /solihull/jobs | 1 |  | Yes |
| Detail | City | Derby | All roles | /derby/jobs | 1 |  | Yes |
| Detail | City | Cheltenham | All roles | /cheltenham/jobs | 1 |  | Yes |
| Detail | City | Bracknell | All roles | /bracknell/jobs | 1 |  | Yes |
| Detail | City | Canterbury | All roles | /canterbury/jobs | 1 |  | Yes |
| Detail | City | Blackburn | All roles | /blackburn/jobs | 1 |  | Yes |
| Detail | City | Corby | All roles | /corby/jobs | 1 |  | Yes |
| Detail | City | Crewe | All roles | /crewe/jobs | 1 |  | Yes |
| Detail | City | Stevenage | All roles | /stevenage/jobs | 1 |  | Yes |
| Detail | City | Chesterfield | All roles | /chesterfield/jobs | 1 |  | Yes |
| Detail | City | Woking | All roles | /woking/jobs | 1 |  | Yes |
| Detail | City | Abingdon | All roles | /abingdon/jobs | 1 |  | Yes |
| Detail | City | King's Lynn | All roles | /kings-lynn/jobs | 1 |  | Yes |
| Detail | City | Newport | All roles | /newport/jobs | 1 |  | Yes |
| Detail | City | Oldham | All roles | /oldham/jobs | 1 |  | Yes |
| Detail | City | Redhill | All roles | /redhill/jobs | 1 |  | Yes |
| Detail | City | Sittingbourne | All roles | /sittingbourne/jobs | 1 |  | Yes |
| Detail | City | Wrexham | All roles | /wrexham/jobs | 1 |  | Yes |
| Detail | City | Kettering | All roles | /kettering/jobs | 1 |  | Yes |
| Detail | City | High Wycombe | All roles | /high-wycombe/jobs | 1 |  | Yes |
| Detail | City | Dudley | All roles | /dudley/jobs | 1 |  | Yes |
| Detail | City | Dundee | All roles | /dundee/jobs | 1 |  | Yes |
| Detail | City | Wirral | All roles | /wirral/jobs | 1 |  | Yes |
| Detail | Regional/category | Yorkshire - East | Admin & Customer Service | /job-search/east-yorkshire/service-administrator-jobs | 1 | 42 | Yes |
| Detail | Regional/category | Northern Ireland - East | Admin & Customer Service | /job-search/northern-ireland-east/service-administrator-jobs | 1 | 10 | Yes |
| Detail | Regional/category | London | Customer Service & Contact Centre | /job-search/london/customer-service-jobs | 1 | 12 | Yes |
| Detail | Regional/category | London | HR & Recruitment | /job-search/london/hr-recruitment-jobs | 1 | 33 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Admin & Customer Service | /job-search/manchester-salford/service-administrator-jobs | 1 | 121 | Yes |
| Detail | Regional/category | London | Finance & Accounts | /job-search/london/finance-accounts-jobs | 1 | 170 | Yes |
| Detail | Regional/category | Oxfordshire | Admin & Customer Service | /job-search/oxfordshire/service-administrator-jobs | 1 | 69 | Yes |
| Detail | Regional/category | Bristol & Bath | Admin & Customer Service | /job-search/bristol-bath/service-administrator-jobs | 1 | 66 | Yes |
| Detail | Regional/category | Essex | Admin & Customer Service | /job-search/essex/service-administrator-jobs | 1 | 129 | Yes |
| Detail | Regional/category | Hampshire | Customer Service & Contact Centre | /job-search/hampshire/customer-service-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Cambridgeshire | Admin & Customer Service | /job-search/cambridgeshire/service-administrator-jobs | 1 | 54 | Yes |
| Detail | Regional/category | Gloucestershire | Admin & Customer Service | /job-search/gloucestershire/service-administrator-jobs | 1 | 69 | Yes |
| Detail | Regional/category | London | Support Worker | /job-search/london/support-worker | 1 | 115 | Yes |
| Detail | Regional/category | Devon | Finance & Accounts | /job-search/devon/finance-accounts-jobs | 1 | 26 | Yes |
| Detail | Regional/category | Dorset | Admin & Customer Service | /job-search/dorset/service-administrator-jobs | 1 | 52 | Yes |
| Detail | Regional/category | Staffordshire | Customer Service & Contact Centre | /job-search/staffordshire/customer-service-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Devon | Admin & Customer Service | /job-search/devon/service-administrator-jobs | 1 | 81 | Yes |
| Detail | Regional/category | Surrey | Customer Service & Contact Centre | /job-search/surrey/customer-service-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Wiltshire | Admin & Customer Service | /job-search/wiltshire/service-administrator-jobs | 1 | 51 | Yes |
| Detail | Regional/category | Northamptonshire | Admin & Customer Service | /job-search/northamptonshire/service-administrator-jobs | 1 | 77 | Yes |
| Detail | Regional/category | Berkshire | Admin & Customer Service | /job-search/berkshire/service-administrator-jobs | 1 | 71 | Yes |
| Detail | Regional/category | Nottinghamshire | Admin & Customer Service | /job-search/nottinghamshire/service-administrator-jobs | 1 | 73 | Yes |
| Detail | Regional/category | Buckinghamshire | Admin & Customer Service | /job-search/buckinghamshire/service-administrator-jobs | 1 | 72 | Yes |
| Detail | Regional/category | Surrey | Support Worker | /job-search/surrey/support-worker | 1 | 14 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Customer Service & Contact Centre | /job-search/manchester-salford/customer-service-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Hampshire | HR & Recruitment | /job-search/hampshire/hr-recruitment-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Hertfordshire | Admin & Customer Service | /job-search/hertfordshire/service-administrator-jobs | 1 | 95 | Yes |
| Detail | Regional/category | Staffordshire | Admin & Customer Service | /job-search/staffordshire/service-administrator-jobs | 1 | 76 | Yes |
| Detail | Regional/category | Norfolk | Admin & Customer Service | /job-search/norfolk/service-administrator-jobs | 1 | 55 | Yes |
| Detail | Regional/category | Sussex | Finance & Accounts | /job-search/sussex/finance-accounts-jobs | 1 | 32 | Yes |
| Detail | Regional/category | Yorkshire - West | Finance & Accounts | /job-search/west-yorkshire/finance-accounts-jobs | 1 | 64 | Yes |
| Detail | Regional/category | Gloucestershire | Finance & Accounts | /job-search/gloucestershire/finance-accounts-jobs | 1 | 29 | Yes |
| Detail | Regional/category | Bristol & Bath | Finance & Accounts | /job-search/bristol-bath/finance-accounts-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Sussex | Customer Service & Contact Centre | /job-search/sussex/customer-service-jobs | 1 | 5 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Admin & Customer Service | /job-search/birmingham-solihull/service-administrator-jobs | 1 | 110 | Yes |
| Detail | Regional/category | Yorkshire - West | HR & Recruitment | /job-search/west-yorkshire/hr-recruitment-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Greater Manchester - South | Admin & Customer Service | /job-search/greater-manchester-south/service-administrator-jobs | 1 | 49 | Yes |
| Detail | Regional/category | Hampshire | Finance & Accounts | /job-search/hampshire/finance-accounts-jobs | 1 | 45 | Yes |
| Detail | Regional/category | North East | Finance & Accounts | /job-search/north-east/finance-accounts-jobs | 1 | 31 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Finance & Accounts | /job-search/birmingham-solihull/finance-accounts-jobs | 1 | 26 | Yes |
| Detail | Regional/category | Wiltshire | Support Worker | /job-search/wiltshire/support-worker | 1 | 10 | Yes |
| Detail | Regional/category | Somerset | Admin & Customer Service | /job-search/somerset/service-administrator-jobs | 1 | 41 | Yes |
| Detail | Regional/category | London | Customer Sales & Sales Advisor | /job-search/london/customer-sales-jobs | 1 | 117 | Yes |
| Detail | Regional/category | Yorkshire - West | Customer Sales & Sales Advisor | /job-search/west-yorkshire/customer-sales-jobs | 1 | 20 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Customer Sales & Sales Advisor | /job-search/manchester-salford/customer-sales-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Leicestershire | Admin & Customer Service | /job-search/leicestershire/service-administrator-jobs | 1 | 86 | Yes |
| Detail | Regional/category | Cheshire - Warrington & Halton | Admin & Customer Service | /job-search/warrington-halton/service-administrator-jobs | 1 | 36 | Yes |
| Detail | Regional/category | Cornwall | Admin & Customer Service | /job-search/cornwall/service-administrator-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Suffolk | Admin & Customer Service | /job-search/suffolk/service-administrator-jobs | 1 | 55 | Yes |
| Detail | Regional/category | Derbyshire | Admin & Customer Service | /job-search/derbyshire/service-administrator-jobs | 1 | 52 | Yes |
| Detail | Regional/category | Cheshire - East | Admin & Customer Service | /job-search/cheshire-east/service-administrator-jobs | 1 | 30 | Yes |
| Detail | Regional/category | Lincolnshire | Admin & Customer Service | /job-search/lincolnshire/service-administrator-jobs | 1 | 40 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Admin & Customer Service | /job-search/merseyside-liverpool/service-administrator-jobs | 1 | 44 | Yes |
| Detail | Regional/category | Shropshire | Admin & Customer Service | /job-search/shropshire/service-administrator-jobs | 1 | 34 | Yes |
| Detail | Regional/category | Greater Manchester - Wigan & Bolton | Admin & Customer Service | /job-search/wigan-bolton/service-administrator-jobs | 1 | 34 | Yes |
| Detail | Regional/category | West Midlands - Black Country | Admin & Customer Service | /job-search/black-country/service-administrator-jobs | 1 | 60 | Yes |
| Detail | Regional/category | London | Legal Assistant & Paralegal | /job-search/london/paralegal-jobs | 1 | 103 | Yes |
| Detail | Regional/category | Suffolk | Legal Assistant & Paralegal | /job-search/suffolk/paralegal-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Essex | Legal Assistant & Paralegal | /job-search/essex/paralegal-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Norfolk | Legal Assistant & Paralegal | /job-search/norfolk/paralegal-jobs | 1 | 18 | Yes |
| Detail | Regional/category | London | Marketing | /job-search/london/marketing-jobs | 1 | 156 | Yes |
| Detail | Regional/category | Surrey | Marketing | /job-search/surrey/marketing-jobs | 1 | 28 | Yes |
| Detail | Regional/category | Greater Manchester - North | Finance & Accounts | /job-search/greater-manchester-north/finance-accounts-jobs | 1 | 17 | Yes |
| Detail | Regional/category | Scotland Central - Fife | Admin & Customer Service | /job-search/fife/service-administrator-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Bristol & Bath | Legal Assistant & Paralegal | /job-search/bristol-bath/paralegal-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Staffordshire | Marketing | /job-search/staffordshire/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Marketing | /job-search/manchester-salford/marketing-jobs | 1 | 33 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Marketing | /job-search/birmingham-solihull/marketing-jobs | 1 | 32 | Yes |
| Detail | Regional/category | Berkshire | HR & Recruitment | /job-search/berkshire/hr-recruitment-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | HR & Recruitment | /job-search/manchester-salford/hr-recruitment-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Nottinghamshire | HR & Recruitment | /job-search/nottinghamshire/hr-recruitment-jobs | 1 | 5 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | HR & Recruitment | /job-search/birmingham-solihull/hr-recruitment-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Sussex | HR & Recruitment | /job-search/sussex/hr-recruitment-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Essex | HR & Recruitment | /job-search/essex/hr-recruitment-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Cheshire - West | Admin & Customer Service | /job-search/cheshire-west/service-administrator-jobs | 1 | 25 | Yes |
| Detail | Regional/category | Scotland Central - Edinburgh & Lothians | Admin & Customer Service | /job-search/edinburgh-lothians/service-administrator-jobs | 1 | 35 | Yes |
| Detail | Regional/category | Worcestershire | Admin & Customer Service | /job-search/worcestershire/service-administrator-jobs | 1 | 30 | Yes |
| Detail | Regional/category | Berkshire | Marketing | /job-search/berkshire/marketing-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Kent | Support Worker | /job-search/kent/support-worker | 1 | 20 | Yes |
| Detail | Regional/category | North East | Customer Sales & Sales Advisor | /job-search/north-east/customer-sales-jobs | 1 | 26 | Yes |
| Detail | Regional/category | Oxfordshire | Support Worker | /job-search/oxfordshire/support-worker | 1 | 10 | Yes |
| Detail | Regional/category | Yorkshire - North | Finance & Accounts | /job-search/north-yorkshire/finance-accounts-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Northern Ireland - East | Finance & Accounts | /job-search/northern-ireland-east/finance-accounts-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Shropshire | Finance & Accounts | /job-search/shropshire/finance-accounts-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Bedfordshire | Admin & Customer Service | /job-search/bedfordshire/service-administrator-jobs | 1 | 31 | Yes |
| Detail | Regional/category | Bristol & Bath | Customer Sales & Sales Advisor | /job-search/bristol-bath/customer-sales-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Buckinghamshire | Marketing | /job-search/buckinghamshire/marketing-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Wales South - Cardiff & Vale | Admin & Customer Service | /job-search/cardiff-vale/service-administrator-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Berkshire | Customer Sales & Sales Advisor | /job-search/berkshire/customer-sales-jobs | 1 | 17 | Yes |
| Detail | Regional/category | Hertfordshire | Customer Sales & Sales Advisor | /job-search/hertfordshire/customer-sales-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Kent | Customer Sales & Sales Advisor | /job-search/kent/customer-sales-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Scotland West - Glasgow | Customer Sales & Sales Advisor | /job-search/glasgow/customer-sales-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Surrey | Customer Sales & Sales Advisor | /job-search/surrey/customer-sales-jobs | 1 | 24 | Yes |
| Detail | Regional/category | Sussex | Customer Sales & Sales Advisor | /job-search/sussex/customer-sales-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Bristol & Bath | Marketing | /job-search/bristol-bath/marketing-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Gloucestershire | Marketing | /job-search/gloucestershire/marketing-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Hertfordshire | Marketing | /job-search/hertfordshire/marketing-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Kent | Marketing | /job-search/kent/marketing-jobs | 1 | 24 | Yes |
| Detail | Regional/category | Oxfordshire | Marketing | /job-search/oxfordshire/marketing-jobs | 1 | 10 | Yes |
| Detail | Regional/category | North Scotland | Admin & Customer Service | /job-search/north-scotland/service-administrator-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Scotland Central - Tayside | Admin & Customer Service | /job-search/tayside/service-administrator-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Wales South - Valleys | Admin & Customer Service | /job-search/south-wales-valleys/service-administrator-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Cambridgeshire | Marketing | /job-search/cambridgeshire/marketing-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Cheshire - West | Marketing | /job-search/cheshire-west/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Essex | Marketing | /job-search/essex/marketing-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Marketing | /job-search/merseyside-liverpool/marketing-jobs | 1 | 6 | Yes |
| Detail | Regional/category | North East | Marketing | /job-search/north-east/marketing-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Cheshire - Warrington & Halton | Finance & Accounts | /job-search/warrington-halton/finance-accounts-jobs | 1 | 17 | Yes |
| Detail | Regional/category | Buckinghamshire | Customer Service & Contact Centre | /job-search/buckinghamshire/customer-service-jobs | 1 | 1 | Yes |
| Detail | Regional/category | North East | Customer Service & Contact Centre | /job-search/north-east/customer-service-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Devon | Customer Sales & Sales Advisor | /job-search/devon/customer-sales-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Hampshire | Customer Sales & Sales Advisor | /job-search/hampshire/customer-sales-jobs | 1 | 29 | Yes |
| Detail | Regional/category | North Scotland | Customer Sales & Sales Advisor | /job-search/north-scotland/customer-sales-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Greater Manchester - South | Marketing | /job-search/greater-manchester-south/marketing-jobs | 1 | 1 | Yes |
| Detail | Regional/category | Northern Ireland - East | Marketing | /job-search/northern-ireland-east/marketing-jobs | 1 | 1 | Yes |
| Detail | Regional/category | Yorkshire - North | Marketing | /job-search/north-yorkshire/marketing-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Essex | Finance & Accounts | /job-search/essex/finance-accounts-jobs | 1 | 40 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Finance & Accounts | /job-search/manchester-salford/finance-accounts-jobs | 1 | 53 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | HR & Recruitment | /job-search/coventry-warwickshire/hr-recruitment-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Berkshire | Finance & Accounts | /job-search/berkshire/finance-accounts-jobs | 1 | 23 | Yes |
| Detail | Regional/category | Buckinghamshire | Finance & Accounts | /job-search/buckinghamshire/finance-accounts-jobs | 1 | 31 | Yes |
| Detail | Regional/category | Cambridgeshire | Finance & Accounts | /job-search/cambridgeshire/finance-accounts-jobs | 1 | 21 | Yes |
| Detail | Regional/category | Cheshire - East | Finance & Accounts | /job-search/cheshire-east/finance-accounts-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Cheshire - West | Finance & Accounts | /job-search/cheshire-west/finance-accounts-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Dorset | Finance & Accounts | /job-search/dorset/finance-accounts-jobs | 1 | 22 | Yes |
| Detail | Regional/category | Hertfordshire | Finance & Accounts | /job-search/hertfordshire/finance-accounts-jobs | 1 | 33 | Yes |
| Detail | Regional/category | Kent | Finance & Accounts | /job-search/kent/finance-accounts-jobs | 1 | 57 | Yes |
| Detail | Regional/category | Lancashire - East | Finance & Accounts | /job-search/lancashire-east/finance-accounts-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Leicestershire | Finance & Accounts | /job-search/leicestershire/finance-accounts-jobs | 1 | 33 | Yes |
| Detail | Regional/category | Norfolk | Finance & Accounts | /job-search/norfolk/finance-accounts-jobs | 1 | 26 | Yes |
| Detail | Regional/category | Northamptonshire | Finance & Accounts | /job-search/northamptonshire/finance-accounts-jobs | 1 | 32 | Yes |
| Detail | Regional/category | Nottinghamshire | Finance & Accounts | /job-search/nottinghamshire/finance-accounts-jobs | 1 | 22 | Yes |
| Detail | Regional/category | Oxfordshire | Finance & Accounts | /job-search/oxfordshire/finance-accounts-jobs | 1 | 18 | Yes |
| Detail | Regional/category | Suffolk | Finance & Accounts | /job-search/suffolk/finance-accounts-jobs | 1 | 20 | Yes |
| Detail | Regional/category | Surrey | Finance & Accounts | /job-search/surrey/finance-accounts-jobs | 1 | 52 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Finance & Accounts | /job-search/coventry-warwickshire/finance-accounts-jobs | 1 | 40 | Yes |
| Detail | Regional/category | Wiltshire | Finance & Accounts | /job-search/wiltshire/finance-accounts-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Yorkshire - South | Finance & Accounts | /job-search/south-yorkshire/finance-accounts-jobs | 1 | 23 | Yes |
| Detail | Regional/category | Norfolk | Marketing | /job-search/norfolk/marketing-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Yorkshire - West | Marketing | /job-search/west-yorkshire/marketing-jobs | 1 | 19 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Legal Assistant & Paralegal | /job-search/birmingham-solihull/paralegal-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Yorkshire - North | Legal Assistant & Paralegal | /job-search/north-yorkshire/paralegal-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Yorkshire - West | Legal Assistant & Paralegal | /job-search/west-yorkshire/paralegal-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Berkshire | Legal Assistant & Paralegal | /job-search/berkshire/paralegal-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Legal Assistant & Paralegal | /job-search/manchester-salford/paralegal-jobs | 1 | 28 | Yes |
| Detail | Regional/category | Kent | Legal Assistant & Paralegal | /job-search/kent/paralegal-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Legal Assistant & Paralegal | /job-search/merseyside-liverpool/paralegal-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Surrey | Legal Assistant & Paralegal | /job-search/surrey/paralegal-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Buckinghamshire | Legal Assistant & Paralegal | /job-search/buckinghamshire/paralegal-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Cheshire - Warrington & Halton | Marketing | /job-search/warrington-halton/marketing-jobs | 1 | 2 | Yes |
| Detail | Regional/category | Essex | Customer Sales & Sales Advisor | /job-search/essex/customer-sales-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Gloucestershire | HR & Recruitment | /job-search/gloucestershire/hr-recruitment-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Greater Manchester - North | Admin & Customer Service | /job-search/greater-manchester-north/service-administrator-jobs | 1 | 30 | Yes |
| Detail | Regional/category | Hampshire | Legal Assistant & Paralegal | /job-search/hampshire/paralegal-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Herefordshire | Admin & Customer Service | /job-search/herefordshire/service-administrator-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Lancashire - East | Admin & Customer Service | /job-search/lancashire-east/service-administrator-jobs | 1 | 26 | Yes |
| Detail | Regional/category | Lincolnshire | Finance & Accounts | /job-search/lincolnshire/finance-accounts-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Finance & Accounts | /job-search/merseyside-liverpool/finance-accounts-jobs | 1 | 24 | Yes |
| Detail | Regional/category | Nottinghamshire | Marketing | /job-search/nottinghamshire/marketing-jobs | 1 | 21 | Yes |
| Detail | Regional/category | Oxfordshire | Legal Assistant & Paralegal | /job-search/oxfordshire/paralegal-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Somerset | Finance & Accounts | /job-search/somerset/finance-accounts-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Staffordshire | Finance & Accounts | /job-search/staffordshire/finance-accounts-jobs | 1 | 18 | Yes |
| Detail | Regional/category | Sussex | Marketing | /job-search/sussex/marketing-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Wales South - Swansea Bay | Admin & Customer Service | /job-search/swansea-bay/service-administrator-jobs | 1 | 11 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Marketing | /job-search/coventry-warwickshire/marketing-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Worcestershire | Finance & Accounts | /job-search/worcestershire/finance-accounts-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Yorkshire - East | Finance & Accounts | /job-search/east-yorkshire/finance-accounts-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Cumbria - North | Admin & Customer Service | /job-search/cumbria-north/service-administrator-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Dorset | Customer Sales & Sales Advisor | /job-search/dorset/customer-sales-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Hertfordshire | Legal Assistant & Paralegal | /job-search/hertfordshire/paralegal-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Lancashire - Central | Admin & Customer Service | /job-search/lancashire-central/service-administrator-jobs | 1 | 17 | Yes |
| Detail | Regional/category | North Wales - East | Admin & Customer Service | /job-search/north-wales-east/service-administrator-jobs | 1 | 26 | Yes |
| Detail | Regional/category | Northamptonshire | Customer Sales & Sales Advisor | /job-search/northamptonshire/customer-sales-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Nottinghamshire | Legal Assistant & Paralegal | /job-search/nottinghamshire/paralegal-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Oxfordshire | Customer Sales & Sales Advisor | /job-search/oxfordshire/customer-sales-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Scotland Central - Falkirk & Stirling | Admin & Customer Service | /job-search/falkirk-stirling/service-administrator-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Suffolk | Customer Sales & Sales Advisor | /job-search/suffolk/customer-sales-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Wales South - Gwent | Admin & Customer Service | /job-search/gwent/service-administrator-jobs | 1 | 19 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Legal Assistant & Paralegal | /job-search/coventry-warwickshire/paralegal-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Yorkshire - West | Customer Service & Contact Centre | /job-search/west-yorkshire/customer-service-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Cambridgeshire | Customer Sales & Sales Advisor | /job-search/cambridgeshire/customer-sales-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Nottinghamshire | Customer Sales & Sales Advisor | /job-search/nottinghamshire/customer-sales-jobs | 1 | 10 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Customer Sales & Sales Advisor | /job-search/coventry-warwickshire/customer-sales-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Worcestershire | Customer Sales & Sales Advisor | /job-search/worcestershire/customer-sales-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Northamptonshire | Marketing | /job-search/northamptonshire/marketing-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Scotland West - Glasgow | Marketing | /job-search/glasgow/marketing-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Cornwall | Finance & Accounts | /job-search/cornwall/finance-accounts-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Derbyshire | Finance & Accounts | /job-search/derbyshire/finance-accounts-jobs | 1 | 15 | Yes |
| Detail | Regional/category | Herefordshire | Finance & Accounts | /job-search/herefordshire/finance-accounts-jobs | 1 | 8 | Yes |
| Detail | Regional/category | North East | HR & Recruitment | /job-search/north-east/hr-recruitment-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Staffordshire | HR & Recruitment | /job-search/staffordshire/hr-recruitment-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Surrey | HR & Recruitment | /job-search/surrey/hr-recruitment-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Hertfordshire | Customer Service & Contact Centre | /job-search/hertfordshire/customer-service-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Kent | Customer Service & Contact Centre | /job-search/kent/customer-service-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Merseyside - St Helens & Knowsley | Admin & Customer Service | /job-search/st-helens-knowsley/service-administrator-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Cheshire - East | Customer Sales & Sales Advisor | /job-search/cheshire-east/customer-sales-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Gloucestershire | Customer Sales & Sales Advisor | /job-search/gloucestershire/customer-sales-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Leicestershire | Customer Sales & Sales Advisor | /job-search/leicestershire/customer-sales-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Norfolk | Customer Sales & Sales Advisor | /job-search/norfolk/customer-sales-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Scotland West - Glasgow | Legal Assistant & Paralegal | /job-search/glasgow/paralegal-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Yorkshire - South | Marketing | /job-search/south-yorkshire/marketing-jobs | 1 | 8 | Yes |
| Detail | Regional/category | West Midlands - Black Country | Finance & Accounts | /job-search/black-country/finance-accounts-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Leicestershire | HR & Recruitment | /job-search/leicestershire/hr-recruitment-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Suffolk | HR & Recruitment | /job-search/suffolk/hr-recruitment-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Merseyside - Wirral | Admin & Customer Service | /job-search/merseyside-wirral/service-administrator-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Scotland West - Lanarkshire | Admin & Customer Service | /job-search/lanarkshire/service-administrator-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Berkshire | Support Worker | /job-search/berkshire/support-worker | 1 | 15 | Yes |
| Detail | Regional/category | Dorset | Support Worker | /job-search/dorset/support-worker | 1 | 17 | Yes |
| Detail | Regional/category | Essex | Support Worker | /job-search/essex/support-worker | 1 | 15 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Support Worker | /job-search/manchester-salford/support-worker | 1 | 6 | Yes |
| Detail | Regional/category | Nottinghamshire | Support Worker | /job-search/nottinghamshire/support-worker | 1 | 21 | Yes |
| Detail | Regional/category | Derbyshire | Customer Sales & Sales Advisor | /job-search/derbyshire/customer-sales-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Lincolnshire | Legal Assistant & Paralegal | /job-search/lincolnshire/paralegal-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Sussex | Legal Assistant & Paralegal | /job-search/sussex/paralegal-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Yorkshire - South | Legal Assistant & Paralegal | /job-search/south-yorkshire/paralegal-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Dorset | Marketing | /job-search/dorset/marketing-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Leicestershire | Marketing | /job-search/leicestershire/marketing-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Bedfordshire | Finance & Accounts | /job-search/bedfordshire/finance-accounts-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Buckinghamshire | HR & Recruitment | /job-search/buckinghamshire/hr-recruitment-jobs | 1 | 9 | Yes |
| Detail | Regional/category | West Midlands - Black Country | HR & Recruitment | /job-search/black-country/hr-recruitment-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Lancashire - Blackpool & Fylde | Admin & Customer Service | /job-search/blackpool-fylde/service-administrator-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Bedfordshire | Customer Sales & Sales Advisor | /job-search/bedfordshire/customer-sales-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Cambridgeshire | Legal Assistant & Paralegal | /job-search/cambridgeshire/paralegal-jobs | 1 | 26 | Yes |
| Detail | Regional/category | North East | Legal Assistant & Paralegal | /job-search/north-east/paralegal-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Scotland Central - Edinburgh & Lothians | Legal Assistant & Paralegal | /job-search/edinburgh-lothians/paralegal-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Hampshire | Marketing | /job-search/hampshire/marketing-jobs | 1 | 15 | Yes |
| Detail | Regional/category | Shropshire | Marketing | /job-search/shropshire/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Greater Manchester - South | Finance & Accounts | /job-search/greater-manchester-south/finance-accounts-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Lancashire - Central | Finance & Accounts | /job-search/lancashire-central/finance-accounts-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Merseyside - Wirral | Finance & Accounts | /job-search/merseyside-wirral/finance-accounts-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Scotland Central - Edinburgh & Lothians | Finance & Accounts | /job-search/edinburgh-lothians/finance-accounts-jobs | 1 | 10 | Yes |

## CITY OPPORTUNITIES

**583 mapped towns/localities with live jobs or an existing city page.** Counts use all 5,750 unique live Ontap jobs across every role and provider: 3,187 have an exact recognised town/locality and 2,563 have only broader or unrecognised location evidence. CREATE means 4+ current Service Admin jobs and no existing city page; London is held separately.

| Status | Town/city/locality | Region | All live jobs | Existing pages | Current routes | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre | Other / unclassified |
|---|---|---|---:|---:|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CREATE | St. Ives | Cambridgeshire | 11 | 0 |  | 6 | 0 | 4 | 0 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Tamworth | Staffordshire | 11 | 0 |  | 9 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| CREATE | Mansfield | Nottinghamshire | 10 | 0 |  | 4 | 4 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Luton | Bedfordshire | 9 | 0 |  | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Tunbridge Wells | Kent | 9 | 0 |  | 4 | 2 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Washington | North East - Tyneside, Wearside & Northumberland | 9 | 0 |  | 5 | 3 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| CREATE | Winchester | Hampshire | 9 | 0 |  | 7 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Loughborough | Leicestershire | 8 | 0 |  | 7 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| CREATE | Maidenhead | Berkshire | 8 | 0 |  | 5 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Blackpool | Lancashire - Blackpool & Fylde | 7 | 0 |  | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Cullompton | Devon | 7 | 0 |  | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Fareham | Hampshire | 7 | 0 |  | 5 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Halifax | Yorkshire - West | 7 | 0 |  | 4 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Hessle | Yorkshire - East | 7 | 0 |  | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Hove | Sussex | 7 | 0 |  | 6 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Sevenoaks | Kent | 7 | 0 |  | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Stirling | Scotland Central - Falkirk & Stirling | 7 | 0 |  | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Trafford | Greater Manchester - South | 7 | 0 |  | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Aberdeen | North Scotland | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Batley | Yorkshire - West | 6 | 0 |  | 4 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Bury | Greater Manchester - North | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Daventry | Northamptonshire | 6 | 0 |  | 4 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Epsom | Surrey | 6 | 0 |  | 5 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Grays | Essex | 6 | 0 |  | 5 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Richmond | Yorkshire - North | 6 | 0 |  | 5 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Rochdale | Greater Manchester - North | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Shirley | West Midlands - Birmingham & Solihull | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Wellingborough | Northamptonshire | 6 | 0 |  | 5 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | West Bromwich | West Midlands - Black Country | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Widnes | Cheshire - Warrington & Halton | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Banbury | Oxfordshire | 5 | 0 |  | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Brinsworth | Yorkshire - South | 5 | 0 |  | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Chorley | Lancashire - Central | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Darlington | North East - County Durham & Darlington/Hartlepool | 5 | 0 |  | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Grantham | Lincolnshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Havant | Hampshire | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Leyland | Lancashire - Central | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Livingston | Scotland Central - Edinburgh & Lothians | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Malton | Yorkshire - North | 5 | 0 |  | 4 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Ramsbottom | Greater Manchester - North | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Rogerstone | Wales South -gwent | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Selby | Yorkshire - North | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Southend-on-sea | Essex | 5 | 0 |  | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Staines | Surrey | 5 | 0 |  | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Telford | Shropshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Wigan | Greater Manchester - Wigan & Bolton | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Wilmslow | Cheshire - East | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Birkenhead | Merseyside - Wirral | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Chelmsley Wood | West Midlands - Birmingham & Solihull | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Chippenham | Wiltshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Colwyn Bay | North Wales - East | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Ellesmere Port | Cheshire - West | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Ely | Cambridgeshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Goole | Yorkshire - East | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Knowsley | Merseyside - St Helens & Knowsley | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Leigh | Greater Manchester - Wigan & Bolton | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Normanton | Yorkshire - West | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Oldbury | West Midlands - Black Country | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Ross-on-wye | Herefordshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Rugeley | Staffordshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Shepperton | Surrey | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Westbury | Wiltshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Witham | Essex | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Manchester | Greater Manchester - Manchester & Salford | 149 | 1 | /manchester/service-administrator-jobs | 113 | 4 | 3 | 10 | 8 | 9 | 0 | 2 | 0 |
| LIVE PAGE | Birmingham | West Midlands - Birmingham & Solihull | 133 | 1 | /birmingham/service-administrator-jobs | 88 | 0 | 0 | 10 | 24 | 8 | 3 | 0 | 0 |
| LIVE PAGE | Leeds | Yorkshire - West | 94 | 1 | /leeds/service-administrator-jobs | 70 | 0 | 3 | 7 | 7 | 3 | 2 | 2 | 0 |
| LIVE PAGE | Bristol | Bristol & Bath | 73 | 1 | /bristol/service-administrator-jobs | 53 | 0 | 11 | 6 | 2 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Liverpool | Merseyside - Liverpool | 51 | 1 | /liverpool/service-administrator-jobs | 43 | 0 | 0 | 2 | 3 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Nottingham | Nottinghamshire | 47 | 1 | /nottingham/jobs | 25 | 9 | 6 | 1 | 4 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Sheffield | Yorkshire - South | 39 | 1 | /sheffield/service-administrator-jobs | 34 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Bradford | Yorkshire - West | 34 | 1 | /bradford/service-administrator-jobs | 26 | 1 | 4 | 0 | 1 | 1 | 0 | 1 | 0 |
| LIVE PAGE | Exeter | Devon | 31 | 1 | /exeter/service-administrator-jobs | 27 | 0 | 3 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Leicester | Leicestershire | 30 | 1 | /leicester/service-administrator-jobs | 20 | 0 | 7 | 0 | 2 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Edinburgh | Scotland Central - Edinburgh & Lothians | 29 | 1 | /edinburgh/service-administrator-jobs | 27 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Warrington | Cheshire - Warrington & Halton | 29 | 1 | /warrington/service-administrator-jobs | 26 | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Peterborough | Cambridgeshire | 28 | 1 | /peterborough/service-administrator-jobs | 20 | 0 | 6 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Glasgow | Scotland West - Glasgow | 27 | 1 | /glasgow/service-administrator-jobs | 19 | 0 | 2 | 3 | 3 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Huddersfield | Yorkshire - West | 27 | 1 | /huddersfield/service-administrator-jobs | 19 | 1 | 5 | 1 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Bolton | Greater Manchester - Wigan & Bolton | 25 | 1 | /bolton/jobs | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Newcastle | North East - Tyneside, Wearside & Northumberland | 25 | 1 | /newcastle/service-administrator-jobs | 13 | 1 | 10 | 0 | 0 | 0 | 0 | 1 | 0 |
| LIVE PAGE | Reading | Berkshire | 25 | 1 | /reading/jobs | 13 | 4 | 7 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Hull | Yorkshire - East | 23 | 1 | /hull/service-administrator-jobs | 23 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Milton Keynes | Buckinghamshire | 23 | 1 | /milton-keynes/service-administrator-jobs | 21 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| LIVE PAGE | Oxford | Oxfordshire | 23 | 1 | /oxford/service-administrator-jobs | 10 | 6 | 5 | 1 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Doncaster | Yorkshire - South | 22 | 1 | /doncaster/service-administrator-jobs | 17 | 2 | 0 | 1 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Southampton | Hampshire | 22 | 2 | /southampton/service-administrator-jobs, /southampton/support-worker | 14 | 4 | 3 | 0 | 0 | 0 | 1 | 0 | 0 |
| LIVE PAGE | Norwich | Norfolk | 21 | 1 | /norwich/jobs | 10 | 0 | 9 | 0 | 2 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Cambridge | Cambridgeshire | 20 | 1 | /cambridge/service-administrator-jobs | 16 | 0 | 3 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Swindon | Wiltshire | 20 | 1 | /swindon/service-administrator-jobs | 19 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Cardiff | Wales South - Cardiff & Vale | 19 | 1 | /cardiff/service-administrator-jobs | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Chelmsford | Essex | 19 | 1 | /chelmsford/service-administrator-jobs | 13 | 2 | 3 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Gloucester | Gloucestershire | 19 | 1 | /gloucester/service-administrator-jobs | 17 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Northampton | Northamptonshire | 19 | 1 | /northampton/service-administrator-jobs | 12 | 0 | 6 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Altrincham | Greater Manchester - South | 18 | 1 | /altrincham/service-administrator-jobs | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Coventry | West Midlands - Coventry & Warwickshire | 18 | 1 | /coventry/service-administrator-jobs | 10 | 0 | 2 | 2 | 0 | 4 | 0 | 0 | 0 |
| LIVE PAGE | Derby | Derbyshire | 18 | 1 | /derby/jobs | 16 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Ipswich | Suffolk | 18 | 1 | /ipswich/jobs | 9 | 0 | 7 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Stockport | Greater Manchester - South | 18 | 1 | /stockport/service-administrator-jobs | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Wakefield | Yorkshire - West | 18 | 1 | /wakefield/jobs | 12 | 1 | 2 | 1 | 0 | 1 | 1 | 0 | 0 |
| LIVE PAGE | Warwick | West Midlands - Coventry & Warwickshire | 18 | 1 | /warwick/service-administrator-jobs | 13 | 0 | 2 | 1 | 0 | 1 | 1 | 0 | 0 |
| LIVE PAGE | Bracknell | Berkshire | 16 | 1 | /bracknell/jobs | 10 | 1 | 2 | 0 | 2 | 0 | 1 | 0 | 0 |
| LIVE PAGE | Macclesfield | Cheshire - East | 16 | 1 | /macclesfield/service-administrator-jobs | 14 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Blackburn | Lancashire - East | 15 | 1 | /blackburn/jobs | 14 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Poole | Dorset | 15 | 1 | /poole/service-administrator-jobs | 13 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Cheltenham | Gloucestershire | 14 | 1 | /cheltenham/jobs | 6 | 0 | 3 | 0 | 1 | 4 | 0 | 0 | 0 |
| LIVE PAGE | Chester | Cheshire - West | 14 | 1 | /chester/jobs | 12 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Dartford | Kent | 14 | 1 | /dartford/service-administrator-jobs | 11 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Basingstoke | Hampshire | 13 | 1 | /basingstoke/service-administrator-jobs | 6 | 2 | 4 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Brighton & Hove | Sussex | 13 | 1 | /brighton-hove/service-administrator-jobs | 6 | 4 | 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Crawley | Sussex | 13 | 1 | /crawley/service-administrator-jobs | 11 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Guildford | Surrey | 13 | 1 | /guildford/jobs | 6 | 1 | 5 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Wrexham | North Wales - East | 13 | 1 | /wrexham/jobs | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Ashford | Kent | 12 | 1 | /ashford/service-administrator-jobs | 6 | 0 | 4 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Bournemouth | Dorset | 12 | 1 | /bournemouth/service-administrator-jobs | 8 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | High Wycombe | Buckinghamshire | 12 | 1 | /high-wycombe/jobs | 10 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Portsmouth | Hampshire | 12 | 1 | /portsmouth/service-administrator-jobs | 9 | 1 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | York | Yorkshire - North | 12 | 1 | /york/service-administrator-jobs | 11 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Bath | Bristol & Bath | 11 | 1 | /bath/service-administrator-jobs | 8 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Bedford | Bedfordshire | 11 | 1 | /bedford/service-administrator-jobs | 5 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Chesterfield | Derbyshire | 11 | 1 | /chesterfield/jobs | 8 | 0 | 1 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Dudley | West Midlands - Black Country | 11 | 1 | /dudley/jobs | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Rugby | West Midlands - Coventry & Warwickshire | 11 | 1 | /rugby/jobs | 5 | 0 | 4 | 0 | 1 | 0 | 1 | 0 | 0 |
| LIVE PAGE | Salford | Greater Manchester - Manchester & Salford | 11 | 1 | /salford/jobs | 6 | 2 | 1 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Colchester | Essex | 10 | 1 | /colchester/jobs | 4 | 1 | 3 | 0 | 2 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Corby | Northamptonshire | 10 | 1 | /corby/jobs | 8 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Kettering | Northamptonshire | 10 | 1 | /kettering/jobs | 9 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Newport | Wales South -gwent | 10 | 1 | /newport/jobs | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Plymouth | Devon | 10 | 1 | /plymouth/service-administrator-jobs | 8 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Swansea | Wales South - Swansea Bay | 10 | 1 | /swansea/service-administrator-jobs | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Walsall | West Midlands - Black Country | 10 | 1 | /walsall/service-administrator-jobs | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Belfast | Northern Ireland - East | 9 | 1 | /belfast/service-administrator-jobs | 7 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Canterbury | Kent | 9 | 1 | /canterbury/jobs | 4 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Redhill | Surrey | 9 | 1 | /redhill/jobs | 8 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Shrewsbury | Shropshire | 9 | 1 | /shrewsbury/service-administrator-jobs | 7 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Sittingbourne | Kent | 9 | 1 | /sittingbourne/jobs | 6 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| LIVE PAGE | Solihull | West Midlands - Birmingham & Solihull | 9 | 1 | /solihull/jobs | 8 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Stoke-on-trent | Staffordshire | 9 | 1 | /stoke-on-trent/service-administrator-jobs | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Watford | Hertfordshire | 9 | 1 | /watford/service-administrator-jobs | 7 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Wirral | Merseyside - Wirral | 9 | 1 | /wirral/jobs | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Worcester | Worcestershire | 9 | 1 | /worcester/service-administrator-jobs | 4 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Barnsley | Yorkshire - South | 8 | 1 | /barnsley/service-administrator-jobs | 4 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Dundee | Scotland Central - Tayside | 8 | 1 | /dundee/jobs | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Preston | Lancashire - Central | 8 | 1 | /preston/jobs | 6 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Abingdon | Oxfordshire | 7 | 1 | /abingdon/jobs | 5 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Durham | North East - County Durham & Darlington/Hartlepool | 7 | 1 | /durham/jobs | 5 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Eastleigh | Hampshire | 7 | 1 | /eastleigh/service-administrator-jobs | 5 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Harrogate | Yorkshire - North | 7 | 1 | /harrogate/service-administrator-jobs | 5 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Hemel Hempstead | Hertfordshire | 7 | 1 | /hemel-hempstead/service-administrator-jobs | 6 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Leatherhead | Surrey | 7 | 1 | /leatherhead/jobs | 5 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Maidstone | Kent | 7 | 1 | /maidstone/service-administrator-jobs | 5 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Oldham | Greater Manchester - North | 7 | 1 | /oldham/jobs | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Stevenage | Hertfordshire | 7 | 1 | /stevenage/jobs | 2 | 0 | 3 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Sunderland | North East - Tyneside, Wearside & Northumberland | 7 | 1 | /sunderland/service-administrator-jobs | 4 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Aylesbury | Buckinghamshire | 6 | 1 | /aylesbury/service-administrator-jobs | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Crewe | Cheshire - East | 6 | 1 | /crewe/jobs | 5 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Farnham | Surrey | 6 | 1 | /farnham/service-administrator-jobs | 5 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| LIVE PAGE | Hertford | Hertfordshire | 6 | 1 | /hertford/jobs | 5 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Lincoln | Lincolnshire | 6 | 1 | /lincoln/service-administrator-jobs | 5 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Redditch | Worcestershire | 6 | 1 | /redditch/jobs | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Woking | Surrey | 6 | 1 | /woking/jobs | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Gateshead | North East - Tyneside, Wearside & Northumberland | 5 | 1 | /gateshead/jobs | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 1 | 0 |
| LIVE PAGE | Hereford | Herefordshire | 5 | 1 | /hereford/jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Horsham | Sussex | 5 | 1 | /horsham/service-administrator-jobs | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Rotherham | Yorkshire - South | 5 | 1 | /rotherham/service-administrator-jobs | 4 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Stafford | Staffordshire | 5 | 1 | /stafford/jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Yeovil | Somerset | 5 | 1 | /yeovil/jobs | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | King's Lynn | Norfolk | 4 | 1 | /kings-lynn/jobs | 3 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Witney | Oxfordshire | 4 | 1 | /witney/jobs | 2 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Northallerton | Yorkshire - North | 3 | 1 | /northallerton/jobs | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Scarborough | Yorkshire - North | 3 | 1 | /scarborough/service-administrator-jobs | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Carlisle | Cumbria - North | 2 | 1 | /carlisle/jobs | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Chester Le Street |  | 0 | 1 | /chester-le-street/service-administrator-jobs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Newtownabbey |  | 0 | 1 | /newtownabbey/service-administrator-jobs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Wigston |  | 0 | 1 | /wigston/service-administrator-jobs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Uxbridge | London | 19 | 0 |  | 16 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 0 |
| HOLD – LONDON | Croydon | London | 10 | 0 |  | 6 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Surbiton | London | 9 | 0 |  | 3 | 1 | 2 | 2 | 0 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Bromley | London | 7 | 0 |  | 4 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hounslow | London | 7 | 0 |  | 1 | 3 | 0 | 0 | 2 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Kingston Upon Thames | London | 7 | 0 |  | 5 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Bexley | London | 6 | 0 |  | 4 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Greenford | London | 6 | 0 |  | 2 | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Ruislip | London | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Barking | London | 5 | 0 |  | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Borehamwood | London | 5 | 0 |  | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Enfield | London | 5 | 0 |  | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hayes | London | 5 | 0 |  | 2 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Sutton | London | 5 | 0 |  | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| HOLD – LONDON | Edgware | London | 4 | 0 |  | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Harrow | London | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | South Croydon | London | 4 | 0 |  | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Twickenham | London | 4 | 0 |  | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Beckenham | London | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Brentford | London | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Erith | London | 3 | 0 |  | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Feltham | London | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hillingdon | London | 3 | 0 |  | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Islington | London | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Lambeth | London | 3 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| HOLD – LONDON | Loughton | London | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Newham | London | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Orpington | London | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Romford | London | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Sidcup | London | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Southwark | London | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Bexleyheath | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Dagenham | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hammersmith And Fulham | London | 2 | 0 |  | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Ilford | London | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Mitcham | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | New Malden | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Purley | London | 2 | 0 |  | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Southall | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Wandsworth | London | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Wembley | London | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Barnet | London | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Brimsdown | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Brixton | London | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Broxbourne | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Chessington | London | 1 | 0 |  | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hackney | London | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hornchurch | London | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Isleworth | London | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Northolt | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Northwood | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Pinner | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Rainham | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Teddington | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Wallington | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | West Drayton | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | West Wickham | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Eastbourne | Sussex | 10 | 0 |  | 2 | 4 | 1 | 2 | 0 | 0 | 1 | 0 | 0 |
| MONITOR | Castleford | Yorkshire - West | 8 | 0 |  | 3 | 1 | 1 | 0 | 3 | 0 | 0 | 0 | 0 |
| MONITOR | Ferndown | Dorset | 8 | 0 |  | 2 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Heanor | Derbyshire | 7 | 0 |  | 3 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Basildon | Essex | 6 | 0 |  | 3 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Godalming | Surrey | 6 | 0 |  | 2 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 |
| MONITOR | Winsford | Cheshire - West | 6 | 0 |  | 3 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| MONITOR | Andover | Hampshire | 5 | 0 |  | 2 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Braintree | Essex | 5 | 0 |  | 2 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Coalville | Leicestershire | 5 | 0 |  | 3 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| MONITOR | Farnborough | Hampshire | 5 | 0 |  | 2 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Fleet | Hampshire | 5 | 0 |  | 1 | 0 | 2 | 0 | 2 | 0 | 0 | 0 | 0 |
| MONITOR | Hook Norton | Oxfordshire | 5 | 0 |  | 0 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Horley | Surrey | 5 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| MONITOR | Knaphill | Surrey | 5 | 0 |  | 0 | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knutsford | Cheshire - East | 5 | 0 |  | 3 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Leamington Spa | West Midlands - Coventry & Warwickshire | 5 | 0 |  | 3 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Middlewich | Cheshire - East | 5 | 0 |  | 3 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Newbury | Berkshire | 5 | 0 |  | 1 | 2 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Salisbury | Wiltshire | 5 | 0 |  | 1 | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Slough | Berkshire | 5 | 0 |  | 2 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wokingham | Berkshire | 5 | 0 |  | 2 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Worksop | Nottinghamshire | 5 | 0 |  | 2 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Worthing | Sussex | 5 | 0 |  | 1 | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bicester | Oxfordshire | 4 | 0 |  | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Clitheroe | Lancashire - East | 4 | 0 |  | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Dorking | Surrey | 4 | 0 |  | 2 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Haywards Heath | Sussex | 4 | 0 |  | 2 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Herne Bay | Kent | 4 | 0 |  | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Heywood | Greater Manchester - North | 4 | 0 |  | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Huntingdon | Cambridgeshire | 4 | 0 |  | 3 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Lichfield | Staffordshire | 4 | 0 |  | 1 | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 0 |
| MONITOR | New Milton | Hampshire | 4 | 0 |  | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newark | Nottinghamshire | 4 | 0 |  | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | North Shields | North East - Tyneside, Wearside & Northumberland | 4 | 0 |  | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Nuneaton | West Midlands - Coventry & Warwickshire | 4 | 0 |  | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Runcorn | Cheshire - Warrington & Halton | 4 | 0 |  | 3 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Stratford-upon-avon | West Midlands - Coventry & Warwickshire | 4 | 0 |  | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tonbridge | Kent | 4 | 0 |  | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Trowbridge | Wiltshire | 4 | 0 |  | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Weybridge | Surrey | 4 | 0 |  | 2 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Windsor | Berkshire | 4 | 0 |  | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Alton | Hampshire | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Aylesford | Kent | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Barrow-in-furness | Cumbria - South | 3 | 0 |  | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bognor Regis | Sussex | 3 | 0 |  | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bordon | Hampshire | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brentwood | Essex | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bridlington | Yorkshire - East | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bury St Edmunds | Suffolk | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chatham | Kent | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Christchurch | Dorset | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cirencester | Gloucestershire | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Corsham | Wiltshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cramlington | North East - Tyneside, Wearside & Northumberland | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cranleigh | Surrey | 3 | 0 |  | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Crowthorne | Berkshire | 3 | 0 |  | 0 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Darwen | Lancashire - East | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dereham | Norfolk | 3 | 0 |  | 1 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dorchester | Dorset | 3 | 0 |  | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | East Grinstead | Sussex | 3 | 0 |  | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Emsworth | Hampshire | 3 | 0 |  | 1 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Falkirk | Scotland Central - Falkirk & Stirling | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Falmouth | Cornwall | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Felixstowe | Suffolk | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Flint | North Wales - East | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fordingbridge | Hampshire | 3 | 0 |  | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Gosport | Hampshire | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Gravesend | Kent | 3 | 0 |  | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Great Yarmouth | Norfolk | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Grimsby | Lincolnshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hailsham | Sussex | 3 | 0 |  | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hastings | Sussex | 3 | 0 |  | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Heathfield | Sussex | 3 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Inverness | North Scotland | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kingswinford | West Midlands - Black Country | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lewes | Sussex | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Melksham | Wiltshire | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Motherwell | Scotland West - Lanarkshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newton-le-willows | Merseyside - St Helens & Knowsley | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Northfleet | Kent | 3 | 0 |  | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Northwich | Cheshire - West | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Penwortham | Lancashire - Central | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Perth | Scotland Central - Tayside | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Prenton | Merseyside - Wirral | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Reigate | Surrey | 3 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Rochester | Kent | 3 | 0 |  | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Royston | Hertfordshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Helens | Merseyside - St Helens & Knowsley | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Leonards-on-sea | Sussex | 3 | 0 |  | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stone | Staffordshire | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Sutton Coldfield | West Midlands - Birmingham & Solihull | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sutton-in-ashfield | Nottinghamshire | 3 | 0 |  | 1 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| MONITOR | Tarporley | Cheshire - West | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Taunton | Somerset | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tewkesbury | Gloucestershire | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Thame | Oxfordshire | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Totton | Hampshire | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Waltham Abbey | Essex | 3 | 0 |  | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Waterlooville | Hampshire | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Welwyn Garden City | Hertfordshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wymondham | Norfolk | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Yate | Bristol & Bath | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Accrington | Lancashire - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Addlestone | Surrey | 2 | 0 |  | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| MONITOR | Aldershot | Hampshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ashington | North East - Tyneside, Wearside & Northumberland | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bedale | Yorkshire - North | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bedlington | North East - Tyneside, Wearside & Northumberland | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bentley | Yorkshire - South | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Beverley | Yorkshire - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bexhill-on-sea | Sussex | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bishop Auckland | North East - County Durham & Darlington/Hartlepool | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Boston | Lincolnshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bridgwater | Somerset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brierley Hill | West Midlands - Black Country | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brighouse | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Burnley | Lancashire - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Camberley | Surrey | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cannock | Staffordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chepstow | Wales South - Gwent | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cleckheaton | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cosham | Hampshire | 2 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Cottingham | Yorkshire - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dewsbury | Yorkshire - West | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Didcot | Oxfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dunstable | Bedfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Elgin | North Scotland | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fakenham | Norfolk | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fetcham | Surrey | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Gainsborough | Lincolnshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Gillingham | Kent | 2 | 0 |  | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Halesowen | West Midlands - Black Country | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Harlow | Essex | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Harpenden | Hertfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hatfield | Hertfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hedge End | Hampshire | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Henley-on-thames | Oxfordshire | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hook | Hampshire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Irchester | Northamptonshire | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kidlington | Oxfordshire | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knaresborough | Yorkshire - North | 2 | 0 |  | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Lancing | Sussex | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Larne | Northern Ireland - East | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Ledbury | Herefordshire | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Liskeard | Cornwall | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lowestoft | Suffolk | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lydney | Gloucestershire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Maldon | Essex | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Marlborough | Wiltshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Marlow | Buckinghamshire | 2 | 0 |  | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Morpeth | North East - Tyneside, Wearside & Northumberland | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newquay | Cornwall | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ossett | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Peterlee | North East - County Durham & Darlington/Hartlepool | 2 | 0 |  | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Potters Bar | Hertfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Radstock | Somerset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ramsgate | Kent | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rushden | Northamptonshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sedgefield | North East - County Durham & Darlington/Hartlepool | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shaftesbury | Dorset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shefford | Bedfordshire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sherborne | Dorset | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Silsden | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Smethwick | West Midlands - Black Country | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Southwick | Sussex | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stanley | North East - County Durham & Darlington/Hartlepool | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stretford | Greater Manchester - Manchester & Salford | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Takeley | Essex | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tonypandy | Wales South - Valleys | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Uckfield | Sussex | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Uttoxeter | Staffordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wallsend | North East - Tyneside, Wearside & Northumberland | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Waltham Cross | Hertfordshire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Warminster | Wiltshire | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Wednesbury | West Midlands - Black Country | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | West Malling | Kent | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Weymouth | Dorset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wickford | Essex | 2 | 0 |  | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wimborne | Dorset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Aberdare | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Abergavenny | Wales South - Gwent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Alcester | West Midlands - Coventry & Warwickshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Alderley Edge | Cheshire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Antrim | Northern Ireland - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Astwood Bank | Worcestershire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bacup | Lancashire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bagshot | Surrey | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| MONITOR | Bakewell | Derbyshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ballymena | Northern Ireland - East | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Battle | Sussex | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Beccles | Suffolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Belper | Derbyshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Benfleet | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Berkhamsted | Hertfordshire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Biggleswade | Bedfordshire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Blandford Forum | Dorset | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Blantyre | Scotland West - Lanarkshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Blaydon-on-Tyne | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brampton | Cumbria - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bridgend | Wales South - Swansea Bay | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bridgnorth | Shropshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bridport | Dorset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Broadstairs | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Broadstone | Dorset | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bromsgrove | Worcestershire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Buckingham | Buckinghamshire | 1 | 0 |  | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Burford | Oxfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Burgess Hill | Sussex | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bury St. Edmunds | Suffolk | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Caerphilly | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Calne | Wiltshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Camborne | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Caterham | Surrey | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chapelhall | Scotland West - Lanarkshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cheadle | Greater Manchester - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chesham | Buckinghamshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chichester | Sussex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Clacton-on-sea | Essex | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Coatbridge | Scotland West - Lanarkshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cobham | Surrey | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Colden Common | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Conwy | North Wales - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Corwen | North Wales - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dalkeith | Scotland Central - Edinburgh & Lothians | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Deal | Kent | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Denton | Greater Manchester - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Devizes | Wiltshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Diss | Norfolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dover | Kent | 1 | 0 |  | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Downham Market | Norfolk | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Droitwich | Worcestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dukinfield | Greater Manchester - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Durkar | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Duxford | Cambridgeshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Easby | Yorkshire - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Eccles | Greater Manchester - Manchester & Salford | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Esher | Surrey | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fairford | Gloucestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Featherstone | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Folkestone | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Frinton-on-sea | Essex | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Full Sutton | Yorkshire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Grangemouth | Scotland Central - Falkirk & Stirling | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Haslemere | Surrey | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Haverhill | Suffolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hindhead | Surrey | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hitchin | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hoddesdon | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Holmfirth | Yorkshire - West | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Ilminster | Somerset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ivybridge | Devon | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kenilworth | West Midlands - Coventry & Warwickshire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kirkby | Merseyside - St Helens & Knowsley | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kirkcaldy | Scotland Central - Fife | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kirriemuir | Scotland Central - Tayside | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knowle | West Midlands - Birmingham & Solihull | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Leek | Staffordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Leigh-on-sea | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lingfield | Surrey | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| MONITOR | Little Paxton | Cambridgeshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Littlehampton | Sussex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Liversedge | Yorkshire - West | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lutterworth | Leicestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lymm | Cheshire - Warrington & Halton | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lyndhurst | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | March | Cambridgeshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Market Harborough | Leicestershire | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Midhurst | Sussex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Mold | North Wales - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Montrose | North Scotland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Mountain Ash | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Nelson | Lancashire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newmarket | Suffolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newport Pagnell | Buckinghamshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newton Aycliffe | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newtownards | Northern Ireland - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Olney | Buckinghamshire | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Oswestry | Shropshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Oxted | Surrey | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Penicuik | Scotland Central - Edinburgh & Lothians | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pershore | Worcestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Peterhead | North Scotland | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pontefract | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pontyclun | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pontypridd | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Portgordon | North Scotland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Portishead | Bristol & Bath | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Potton | Bedfordshire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Poulton-le-Fylde | Lancashire - Blackpool & Fylde | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Prescot | Merseyside - St Helens & Knowsley | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Prestatyn | North Wales - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Prestonpans | Scotland Central - Edinburgh & Lothians | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pudsey | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Radcliffe | Greater Manchester - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Redruth | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Retford | Nottinghamshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rickmansworth | Hertfordshire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ringwood | Hampshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Romsey | Hampshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rossendale | Lancashire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rossett | North Wales - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Royton | Greater Manchester - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Saltash | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sandwich | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Scunthorpe | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Seaham | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shap | Cumbria - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sherburn In Elmet | Yorkshire - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shildon | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shipley | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Skipton | Yorkshire - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sleaford | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Snodland | Kent | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | South Shields | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Southam | West Midlands - Coventry & Warwickshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Southsea | Hampshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sowerby Bridge | Yorkshire - West | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Spalding | Lincolnshire | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Albans | Hertfordshire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Asaph | North Wales - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Neots | Cambridgeshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stanford-le-hope | Essex | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Studley | West Midlands - Coventry & Warwickshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sudbury | Suffolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sunbury-on-thames | Surrey | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Swanley | Kent | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tadley | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tadworth | Surrey | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Tavistock | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Thornaby | North East - Tees Valley | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Thurso | North Scotland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tipton | West Midlands - Black Country | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tiverton | Devon | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Torquay | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Totnes | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tredegar | Wales South - Gwent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tring | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Truro | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ulverston | Cumbria - South | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Verwood | Dorset | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wallingford | Oxfordshire | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Waltham | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wareham | Dorset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wellington | Shropshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Welwyn | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Westerham | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Weston-super-mare | Somerset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Whyteleafe | Surrey | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Willand | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Woodhall Spa | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Worsley | Greater Manchester - Manchester & Salford | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

> LIVE counts come directly from the current published `app/` JSON, deduplicated within each canonical region/family slice while preserving legitimate appearances in more than one family. This is the live-site authority for the reconciliation above; the dated source-count CSV is shown only as a freshness cross-check. The overview covers all 78 assessable UK markets; LIVE status remains controlled only by the slice register. Before same-feed 78-market coverage has run, NOT LIVE Admin/Support and Customer Service may fall back to the latest all-region Module 2 profile (2026-08-17), and Service Admin may also add current Teaching Vacancies regional candidate output. `—` means not assessed / no current source; it does NOT mean zero. NOT LIVE Service Admin and Support Worker were assessed from the same JobG8 daily feed (2026-11-12) used by the production family run, across 78 UK markets with the config-driven production wrappers, persistent review decisions and canonical geo. NOT LIVE Sales Advisor was assessed from that same feed across 78 UK markets using the governed Customer Sales classifier, canonical geo, campaign dedupe and final production QA. Sales diagnostic counts are evidence only and never activate a slice automatically; LIVE Sales Advisor counts continue to come from the current published Customer Sales configured-slice JSON. NOT LIVE Paralegal, Marketing, Finance / Accounts and HR / Recruitment were assessed from that same feed across 78, 78, 78 and 78 UK markets respectively, using their governed production boundaries and canonical geo. NOT LIVE Customer Service / Contact Centre was assessed from that same feed across 78 UK markets using its governed exact-title, salary and geography rules. All diagnostic counts are evidence only and never activate a slice automatically. Rolling family history stores one snapshot per feed date, replaces same-date reruns, retains the latest 14 feed dates and is used only as decision evidence for NOT LIVE slices.

## LIVE

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire | 35 |  | 9 |  |  | 7 |  |  |
| Berkshire | 70 | 15 | 17 | 16 | 19 | 23 | 6 |  |
| Bristol & Bath | 78 |  | 13 | 12 | 7 | 16 |  |  |
| Buckinghamshire | 74 |  |  | 8 | 11 | 31 | 9 | 1 |
| Cambridgeshire | 89 |  | 13 | 21 | 9 | 21 |  |  |
| Cheshire - East | 31 |  | 5 |  |  | 19 |  |  |
| Cheshire - Warrington & Halton | 39 |  |  |  | 2 | 17 |  |  |
| Cheshire - West | 25 |  |  |  | 5 | 11 |  |  |
| Cornwall | 11 |  |  |  |  | 7 |  |  |
| Cumbria - North | 4 |  |  |  |  |  |  |  |
| Cumbria - South |  | 4 |  |  |  |  |  |  |
| Cumbria - West |  |  |  |  |  |  |  |  |
| Derbyshire | 52 |  | 6 |  |  | 15 |  |  |
| Devon | 82 |  | 5 |  |  | 25 |  |  |
| Dorset | 54 | 17 | 9 |  | 3 | 21 |  |  |
| Essex | 130 | 15 | 14 | 16 | 12 | 39 | 5 |  |
| Gloucestershire | 70 |  | 8 |  | 8 | 29 | 3 |  |
| Greater Manchester - Manchester & Salford | 150 | 6 | 11 | 28 | 33 | 53 | 7 | 12 |
| Greater Manchester - North | 30 |  |  |  |  | 17 |  |  |
| Greater Manchester - South | 49 |  |  |  | 1 | 10 |  |  |
| Greater Manchester - Wigan & Bolton | 34 |  |  |  |  |  |  |  |
| Hampshire | 154 | 27 | 29 | 11 | 15 | 45 | 7 | 9 |
| Herefordshire | 10 |  |  |  |  | 8 |  |  |
| Hertfordshire | 96 |  | 12 | 10 | 7 | 33 |  | 3 |
| Kent | 137 | 20 | 19 | 13 | 24 | 57 |  | 4 |
| Lancashire - Blackpool & Fylde | 8 |  |  |  |  |  |  |  |
| Lancashire - Central | 17 |  |  |  |  | 11 |  |  |
| Lancashire - East | 26 |  |  |  |  | 12 |  |  |
| Lancashire - North |  |  |  |  |  |  |  |  |
| Lancashire - West |  |  |  |  |  |  |  |  |
| Leicestershire | 88 |  | 9 |  | 8 | 30 | 5 |  |
| Lincolnshire | 51 |  |  | 9 |  | 12 |  |  |
| London | 424 | 114 | 116 | 103 | 156 | 170 | 33 | 12 |
| Merseyside - Liverpool | 52 |  |  | 7 | 6 | 24 |  |  |
| Merseyside - Sefton |  |  |  |  |  |  |  |  |
| Merseyside - St Helens & Knowsley | 12 |  |  |  |  |  |  |  |
| Merseyside - Wirral | 16 |  |  |  |  | 8 |  |  |
| Norfolk | 53 |  | 11 | 17 | 9 | 25 |  |  |
| North East | 101 | 21 | 26 | 12 | 16 | 31 | 6 | 7 |
| North Scotland | 11 |  | 4 |  |  |  |  |  |
| North Wales - East | 26 |  |  |  |  |  |  |  |
| North Wales - West |  |  |  |  |  |  |  |  |
| Northamptonshire | 79 |  | 13 |  | 9 | 31 |  |  |
| Northern Ireland - East | 12 |  |  |  | 1 | 7 | CHECK |  |
| Northern Ireland - West |  |  |  |  |  |  |  |  |
| Nottinghamshire | 73 | 21 | 10 | 6 | 20 | 22 | 5 |  |
| Oxfordshire | 70 | 10 | 13 | 10 | 10 | 18 |  |  |
| Rutland |  |  |  |  |  |  |  |  |
| Scotland - Borders |  |  |  |  |  |  |  |  |
| Scotland Central - Edinburgh & Lothians | 37 |  |  | 7 |  | 10 |  |  |
| Scotland Central - Falkirk & Stirling | 11 |  |  |  |  |  |  |  |
| Scotland Central - Fife | 5 |  |  |  |  |  |  |  |
| Scotland Central - Tayside | 12 |  |  |  |  |  |  |  |
| Scotland West - Ayrshire |  |  |  |  |  |  |  |  |
| Scotland West - Glasgow | 27 |  | 10 | 5 | 10 |  |  |  |
| Scotland West - Lanarkshire | 6 |  |  |  |  |  |  |  |
| Scotland West - Renfrewshire & Inverclyde |  |  |  |  |  |  |  |  |
| Shropshire | 36 |  |  |  | 5 | 6 |  |  |
| Somerset | 41 |  |  |  |  | 7 |  |  |
| Staffordshire | 69 |  |  |  | 5 | 18 | 7 | 3 |
| Suffolk | 55 |  | 11 | 4 |  | 20 | 3 |  |
| Surrey | 136 | 14 | 24 | 12 | 26 | 52 | 9 | 12 |
| Sussex | 106 | 36 | 11 | 18 | 11 | 32 | 6 | 5 |
| Wales - Mid |  |  |  |  |  |  |  |  |
| Wales - West |  |  |  |  |  |  |  |  |
| Wales South - Cardiff & Vale | 19 |  |  |  |  | CHECK |  |  |
| Wales South - Gwent | 19 |  |  |  |  |  |  |  |
| Wales South - Swansea Bay | 11 |  |  |  |  |  |  |  |
| Wales South - Valleys | 7 |  |  |  |  |  |  |  |
| West Midlands - Birmingham & Solihull | 155 |  |  | 14 | 32 | 26 | 7 |  |
| West Midlands - Black Country | 59 |  |  |  |  | 16 | 4 |  |
| West Midlands - Coventry & Warwickshire | 91 |  | 13 | 7 | 7 | 38 | 4 |  |
| Wiltshire | 52 | 10 |  |  |  | 14 |  |  |
| Worcestershire | 31 |  | 9 |  |  | 8 |  |  |
| Yorkshire - East | 42 |  |  |  |  | 9 |  |  |
| Yorkshire - North | 45 |  |  | 14 | 6 | 11 |  |  |
| Yorkshire - South | 78 | 3 |  | 8 | 8 | 23 |  |  |
| Yorkshire - West | 189 | 7 | 20 | 16 | 19 | 64 | 6 | 10 |

## NOT LIVE

> Cells show `today / 14d avg / 6+ days` over observed feed dates (maximum 14). The 6+ measure is a watch signal only, not an automatic activation threshold.

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire |  | 4 / 3.8 / 0/14 |  | 6 / 5.1 / 8/14 | 3 / 3.0 / 0/14 |  | 0 / 1.0 / 0/14 | 4 / 3.0 / 0/14 |
| Berkshire |  |  |  |  |  |  |  | 1 / 0.9 / 0/14 |
| Bristol & Bath |  | 9 / 6.9 / 12/14 |  |  |  |  | 5 / 3.0 / 0/14 | 4 / 3.3 / 0/14 |
| Buckinghamshire |  | 2 / 2.1 / 0/14 | 7 / 5.4 / 7/14 |  |  |  |  |  |
| Cambridgeshire |  | 1 / 1.2 / 0/14 |  |  |  |  | 1 / 0.9 / 0/14 | 1 / 1.6 / 0/14 |
| Cheshire - East |  | 5 / 3.2 / 0/14 |  | 1 / 0.9 / 0/14 | 2 / 1.8 / 0/14 |  | 0 / 0.4 / 0/14 | 2 / 2.4 / 0/14 |
| Cheshire - Warrington & Halton |  | 6 / 4.7 / 7/14 | 3 / 2.9 / 0/14 | 0 / 0.7 / 0/14 |  |  | 1 / 1.0 / 0/14 | 2 / 1.4 / 0/14 |
| Cheshire - West |  | 3 / 1.6 / 0/14 | 3 / 2.4 / 0/14 | 5 / 4.7 / 1/14 |  |  | 1 / 0.9 / 0/14 | 0 / 0.1 / 0/14 |
| Cornwall |  | 3 / 5.6 / 11/14 | 0 / 0.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |  | 0 / 0.0 / 0/14 | 1 / 0.9 / 0/14 |
| Cumbria - North |  | 8 / 6.5 / 9/14 | 5 / 3.1 / 1/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 2.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Cumbria - South | 5 / 2.8 / 0/14 |  | 0 / 0.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Cumbria - West | 6 / 4.9 / 5/14 | 4 / 3.7 / 4/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Derbyshire |  | 6 / 4.2 / 3/14 |  | 3 / 2.6 / 0/14 | 8 / 4.1 / 2/14 |  | 2 / 0.9 / 0/14 | 3 / 2.9 / 0/14 |
| Devon |  | 14 / 15.4 / 12/14 |  | 8 / 5.8 / 7/14 | 4 / 3.1 / 1/14 |  | 2 / 3.6 / 0/14 | 6 / 4.6 / 5/14 |
| Dorset |  |  |  | 6 / 4.8 / 4/14 |  |  | 2 / 1.8 / 0/14 | 4 / 3.2 / 0/14 |
| Essex |  |  |  |  |  |  |  | 7 / 4.2 / 3/14 |
| Gloucestershire |  | 8 / 5.0 / 7/14 |  | 4 / 3.9 / 3/14 |  |  |  | 2 / 1.7 / 0/14 |
| Greater Manchester - Manchester & Salford |  |  |  |  |  |  |  |  |
| Greater Manchester - North |  | 2 / 1.3 / 0/14 | 2 / 0.9 / 0/14 | 3 / 2.4 / 0/14 | 3 / 1.6 / 0/14 |  | 1 / 1.6 / 0/14 | 2 / 1.7 / 0/14 |
| Greater Manchester - South |  | 0 / 2.4 / 0/14 | 2 / 2.4 / 0/14 | 4 / 3.1 / 0/14 |  |  | 2 / 1.7 / 0/14 | 0 / 0.3 / 0/14 |
| Greater Manchester - Wigan & Bolton |  | 3 / 1.5 / 0/14 | 2 / 1.6 / 0/14 | 1 / 1.9 / 0/14 | 1 / 0.7 / 0/14 | 6 / 4.9 / 5/14 | 0 / 1.0 / 0/14 | 4 / 2.6 / 0/14 |
| Hampshire |  |  |  |  |  |  |  |  |
| Herefordshire |  | 2 / 1.5 / 0/14 | 1 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.1 / 0/14 |  | 2 / 1.4 / 0/14 | 0 / 0.0 / 0/14 |
| Hertfordshire |  | 7 / 5.4 / 12/14 |  |  |  |  | 3 / 2.6 / 0/14 |  |
| Kent |  |  |  |  |  |  | 5 / 3.4 / 0/14 |  |
| Lancashire - Blackpool & Fylde |  | 1 / 1.7 / 0/14 | 0 / 0.6 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.9 / 0/14 | 3 / 2.3 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Lancashire - Central |  | 3 / 2.3 / 0/14 | 4 / 1.8 / 0/14 | 0 / 0.0 / 0/14 | 4 / 3.6 / 0/14 |  | 1 / 0.9 / 0/14 | 0 / 0.0 / 0/14 |
| Lancashire - East |  | 2 / 1.6 / 0/14 | 1 / 0.9 / 0/14 | 4 / 3.7 / 0/14 | 0 / 0.6 / 0/14 |  | 1 / 1.6 / 0/14 | 2 / 1.7 / 0/14 |
| Lancashire - North | 2 / 1.4 / 0/14 | 1 / 0.7 / 0/14 | 2 / 0.3 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.9 / 0/14 | 0 / 0.2 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Lancashire - West | 4 / 3.5 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.4 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.5 / 0/14 | 2 / 1.6 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.9 / 0/14 |
| Leicestershire |  | 7 / 6.0 / 12/14 |  | 3 / 1.6 / 0/14 |  |  |  | 2 / 1.8 / 0/14 |
| Lincolnshire |  | 5 / 4.1 / 2/14 | 5 / 5.3 / 9/14 |  | 0 / 0.0 / 0/14 |  | 0 / 1.1 / 0/14 | 1 / 0.3 / 0/14 |
| London |  |  |  |  |  |  |  |  |
| Merseyside - Liverpool |  | 0 / 0.0 / 0/14 | 2 / 1.9 / 0/14 |  |  |  | 1 / 2.4 / 0/14 | 1 / 0.4 / 0/14 |
| Merseyside - Sefton | 2 / 2.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Merseyside - St Helens & Knowsley |  | 0 / 0.9 / 0/14 | 0 / 0.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 5 / 3.6 / 2/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Merseyside - Wirral |  | 2 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.4 / 0/14 | 4 / 3.9 / 0/14 |  | 0 / 0.4 / 0/14 | 0 / 0.0 / 0/14 |
| Norfolk |  | 7 / 3.8 / 2/14 |  |  |  |  | 3 / 3.0 / 0/14 | 3 / 1.6 / 0/14 |
| North East |  |  |  |  |  |  |  |  |
| North Scotland |  | 3 / 1.5 / 0/14 |  | 2 / 1.4 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.2 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.9 / 0/14 |
| North Wales - East |  | 7 / 2.8 / 3/14 | 2 / 1.8 / 0/14 | 1 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 3 / 2.0 / 0/14 | 4 / 1.7 / 0/14 | 2 / 1.1 / 0/14 |
| North Wales - West | 3 / 1.6 / 0/14 | 2 / 1.7 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Northamptonshire |  | 4 / 2.8 / 1/14 |  | 6 / 5.7 / 9/14 |  |  | 2 / 2.4 / 0/14 | 3 / 1.9 / 0/14 |
| Northern Ireland - East |  | 0 / 0.0 / 0/14 | 2 / 1.1 / 0/14 | 0 / 0.0 / 0/14 |  |  |  | 0 / 0.0 / 0/14 |
| Northern Ireland - West | 7 / 4.6 / 3/14 | 0 / 0.0 / 0/14 | 5 / 4.2 / 1/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 3 / 2.8 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.5 / 0/14 |
| Nottinghamshire |  |  |  |  |  |  |  | 0 / 0.7 / 0/14 |
| Oxfordshire |  |  |  |  |  |  | 4 / 3.6 / 0/14 | 3 / 1.1 / 0/14 |
| Rutland | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland - Borders | 1 / 0.4 / 0/14 | 0 / 0.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Edinburgh & Lothians |  | 1 / 0.4 / 0/14 | 2 / 1.6 / 0/14 |  | 3 / 1.5 / 0/14 |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Falkirk & Stirling |  | 0 / 0.0 / 0/14 | 2 / 1.0 / 0/14 | 3 / 2.1 / 0/14 | 0 / 0.0 / 0/14 | 3 / 2.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Fife |  | 0 / 0.7 / 0/14 | 3 / 1.5 / 0/14 | 1 / 1.1 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.9 / 0/14 | 2 / 1.7 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Tayside |  | 0 / 0.1 / 0/14 | 3 / 2.6 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.1 / 0/14 | 0 / 0.4 / 0/14 | 2 / 1.1 / 0/14 |
| Scotland West - Ayrshire | 6 / 3.6 / 2/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 3 / 1.4 / 0/14 | 1 / 0.6 / 0/14 | 0 / 0.3 / 0/14 |
| Scotland West - Glasgow |  | 0 / 0.0 / 0/14 |  |  |  | 5 / 5.4 / 5/14 | 1 / 1.6 / 0/14 | 0 / 2.4 / 0/14 |
| Scotland West - Lanarkshire |  | 1 / 1.6 / 0/14 | 3 / 2.1 / 0/14 | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 2 / 2.1 / 0/14 | 1 / 0.9 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland West - Renfrewshire & Inverclyde | 4 / 3.8 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Shropshire |  | 5 / 5.0 / 7/14 | 5 / 4.5 / 2/14 | 2 / 1.4 / 0/14 |  |  | 3 / 2.9 / 0/14 | 3 / 2.9 / 0/14 |
| Somerset |  | 8 / 6.9 / 12/14 | 7 / 5.2 / 9/14 | 3 / 2.8 / 0/14 | 0 / 0.4 / 0/14 |  | 2 / 1.8 / 0/14 | 2 / 2.3 / 0/14 |
| Staffordshire |  | 5 / 2.9 / 0/14 | 5 / 5.0 / 7/14 | 6 / 4.5 / 3/14 |  |  |  |  |
| Suffolk |  | 8 / 3.1 / 1/14 |  |  | 3 / 2.4 / 0/14 |  |  | 3 / 2.1 / 0/14 |
| Surrey |  |  |  |  |  |  |  |  |
| Sussex |  |  |  |  |  |  |  |  |
| Wales - Mid | 0 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.4 / 0/14 | 0 / 0.6 / 0/14 | 0 / 0.0 / 0/14 |
| Wales - West | 1 / 1.1 / 0/14 | 2 / 1.7 / 0/14 | 1 / 0.6 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.7 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.2 / 0/14 |
| Wales South - Cardiff & Vale |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 4 / 2.6 / 0/14 | 1 / 0.6 / 0/14 |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Wales South - Gwent |  | 1 / 0.9 / 0/14 | 3 / 1.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 3 / 1.8 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Wales South - Swansea Bay |  | 3 / 2.6 / 0/14 | 0 / 0.5 / 0/14 | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 4 / 3.3 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Wales South - Valleys |  | 0 / 0.2 / 0/14 | 1 / 0.9 / 0/14 | 0 / 0.5 / 0/14 | 0 / 0.0 / 0/14 | 4 / 4.1 / 1/14 | 1 / 0.9 / 0/14 | 0 / 0.2 / 0/14 |
| West Midlands - Birmingham & Solihull |  | 0 / 0.4 / 0/14 | 4 / 2.6 / 0/14 |  |  |  |  | 4 / 4.9 / 9/14 |
| West Midlands - Black Country |  | 3 / 2.7 / 0/14 | 7 / 5.1 / 7/14 | 1 / 0.9 / 0/14 | 2 / 4.1 / 0/14 |  |  | 4 / 3.7 / 0/14 |
| West Midlands - Coventry & Warwickshire |  | 5 / 6.1 / 10/14 |  |  |  |  |  | 7 / 5.6 / 10/14 |
| Wiltshire |  |  | 4 / 3.9 / 0/14 | 7 / 2.4 / 1/14 | 5 / 3.9 / 0/14 |  | 2 / 1.1 / 0/14 | 1 / 0.9 / 0/14 |
| Worcestershire |  | 5 / 4.4 / 1/14 |  | 5 / 3.6 / 0/14 | 1 / 1.1 / 0/14 |  | 2 / 0.9 / 0/14 | 1 / 0.1 / 0/14 |
| Yorkshire - East |  | 1 / 1.2 / 0/14 | 4 / 2.5 / 0/14 | 2 / 3.6 / 0/14 | 2 / 2.4 / 0/14 |  | 1 / 1.2 / 0/14 | 0 / 0.4 / 0/14 |
| Yorkshire - North |  | 11 / 10.1 / 12/14 | 5 / 3.6 / 1/14 |  |  |  | 0 / 0.0 / 0/14 | 0 / 0.9 / 0/14 |
| Yorkshire - South |  |  | 3 / 1.9 / 0/14 |  |  |  | 3 / 2.6 / 0/14 | 3 / 2.4 / 0/14 |
| Yorkshire - West |  |  |  |  |  |  |  |  |

## HEADLINE

| Measure | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Live regions | 65 / 78 | 16 / 78 | 29 / 78 | 26 / 78 | 33 / 78 | 51 / 78 | 19 / 78 | 11 / 78 |
| Live slice placements | 3962 | 340 | 470 | 404 | 520 | 1259 + 1 CHECK | 132 + 1 CHECK | 78 |

**Live slices: 250 / 624.**

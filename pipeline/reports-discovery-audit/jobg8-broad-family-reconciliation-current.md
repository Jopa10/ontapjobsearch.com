# JobG8 register-first broad-family reconciliation

Jobs reconciled: **17,785**
Jobs assigned first from an existing selected Ontap register: **911**
Original title-rule Other / Unclassified: **4,375**
Jobs resolved by description-majority pass: **240**
Remaining Other / Unclassified after register-first + title + description passes: **2,376**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Professional Finance / Accountancy | 3,275 | 18.4% |
| Driving / Warehouse / Logistics | 2,735 | 15.4% |
| Other / Unclassified | 2,376 | 13.4% |
| Legal / Conveyancing | 1,136 | 6.4% |
| Healthcare / Clinical | 1,074 | 6.0% |
| Education / Teaching | 1,049 | 5.9% |
| Sales / Business Development | 913 | 5.1% |
| IT / Data / Software | 727 | 4.1% |
| HR / Recruitment | 574 | 3.2% |
| Engineering / Technical | 547 | 3.1% |
| Admin / Customer Service | 508 | 2.9% |
| Financial Advice / Mortgages | 495 | 2.8% |
| Care / Support Work | 433 | 2.4% |
| Construction / Trades / Property | 366 | 2.1% |
| Marketing / Digital / Creative | 345 | 1.9% |
| Management / Team Leadership | 321 | 1.8% |
| Insurance / Claims | 284 | 1.6% |
| Operations / General Management | 112 | 0.6% |
| Charity / Fundraising / Community | 104 | 0.6% |
| Market Research / Field Interviewing | 80 | 0.4% |
| Retail / Store | 70 | 0.4% |
| Compliance / Risk / Quality | 70 | 0.4% |
| Procurement / Buying / Supply Chain | 47 | 0.3% |
| Security / Emergency Services | 44 | 0.2% |
| Manufacturing / Production | 28 | 0.2% |
| Property / Housing / Planning | 26 | 0.1% |
| Science / Laboratory | 19 | 0.1% |
| Hospitality / Catering | 10 | 0.1% |
| Cleaning / Domestic / Facilities | 7 | 0.0% |
| Employment Support / Careers | 7 | 0.0% |
| Agriculture / Environment | 3 | 0.0% |
| **TOTAL** | **17,785** | **100.0%** |

## Refined family totals by salary band

Salary uses the midpoint of the available structured minimum/maximum after annualising hourly, daily, weekly or monthly amounts. Five-figure values are treated as annual even when the source period is inconsistent. The first column combines genuinely sub-£20k jobs with missing or unusable salary so every family reconciles exactly to its total.

| Broad family | Below £20k / unknown | £20k–<£35k | £35k–£45k | Over £45k | Total |
|---|---:|---:|---:|---:|---:|
| Professional Finance / Accountancy | 1,898 | 253 | 418 | 706 | 3,275 |
| Driving / Warehouse / Logistics | 899 | 670 | 908 | 258 | 2,735 |
| Other / Unclassified | 1,568 | 180 | 246 | 382 | 2,376 |
| Legal / Conveyancing | 828 | 35 | 60 | 213 | 1,136 |
| Healthcare / Clinical | 671 | 28 | 170 | 205 | 1,074 |
| Education / Teaching | 833 | 52 | 69 | 95 | 1,049 |
| Sales / Business Development | 488 | 115 | 117 | 193 | 913 |
| IT / Data / Software | 452 | 8 | 59 | 208 | 727 |
| HR / Recruitment | 319 | 58 | 110 | 87 | 574 |
| Engineering / Technical | 294 | 36 | 93 | 124 | 547 |
| Admin / Customer Service | 352 | 109 | 39 | 8 | 508 |
| Financial Advice / Mortgages | 184 | 32 | 93 | 186 | 495 |
| Care / Support Work | 276 | 79 | 29 | 49 | 433 |
| Construction / Trades / Property | 193 | 62 | 52 | 59 | 366 |
| Marketing / Digital / Creative | 217 | 34 | 37 | 57 | 345 |
| Management / Team Leadership | 123 | 32 | 69 | 97 | 321 |
| Insurance / Claims | 177 | 11 | 38 | 58 | 284 |
| Operations / General Management | 78 | 5 | 9 | 20 | 112 |
| Charity / Fundraising / Community | 97 | 3 | 3 | 1 | 104 |
| Market Research / Field Interviewing | 61 | 19 | 0 | 0 | 80 |
| Retail / Store | 67 | 2 | 1 | 0 | 70 |
| Compliance / Risk / Quality | 43 | 1 | 3 | 23 | 70 |
| Procurement / Buying / Supply Chain | 23 | 4 | 9 | 11 | 47 |
| Security / Emergency Services | 31 | 1 | 0 | 12 | 44 |
| Manufacturing / Production | 26 | 1 | 0 | 1 | 28 |
| Property / Housing / Planning | 11 | 6 | 1 | 8 | 26 |
| Science / Laboratory | 1 | 0 | 11 | 7 | 19 |
| Hospitality / Catering | 6 | 3 | 0 | 1 | 10 |
| Cleaning / Domestic / Facilities | 6 | 1 | 0 | 0 | 7 |
| Employment Support / Careers | 2 | 4 | 1 | 0 | 7 |
| Agriculture / Environment | 1 | 0 | 0 | 2 | 3 |
| **TOTAL** | **10,225** | **1,844** | **2,645** | **3,071** | **17,785** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Professional Finance / Accountancy | 3,275 | 541 | 2,734 | 86 | 22.0 | 71 | 57 | 104 | London (576); Yorkshire - West (145); Kent (122); Sussex (102); Surrey (101) |
| Driving / Warehouse / Logistics | 2,735 | 6 | 2,729 | 92 | 14.5 | 71 | 57 | 171 | Northamptonshire (146); Yorkshire - West (131); East Midlands (96); Hampshire (88); London (85) |
| Legal / Conveyancing | 1,136 | 0 | 1,136 | 73 | 7 | 46 | 29 | 28 | London (185); Greater Manchester - Manchester & Salford (72); Essex (55); Suffolk (52); Berkshire (50) |
| Healthcare / Clinical | 1,074 | 0 | 1,074 | 88 | 7.0 | 60 | 34 | 76 | London (129); Surrey (50); Sussex (43); Hampshire (42); Kent (31) |
| Education / Teaching | 1,049 | 0 | 1,049 | 72 | 6.0 | 44 | 30 | 73 | London (186); West Midlands - Birmingham & Solihull (61); Greater Manchester - Manchester & Salford (44); Sussex (43); Hertfordshire (40) |
| Sales / Business Development | 913 | 0 | 913 | 79 | 6 | 45 | 32 | 75 | London (106); Sussex (31); Kent (30); Scotland Central - Tayside (30); Hertfordshire (28) |
| IT / Data / Software | 727 | 0 | 727 | 59 | 5 | 30 | 19 | 112 | London (139); Hampshire (46); Gloucestershire (40); Kent (34); Greater Manchester - Manchester & Salford (32) |
| HR / Recruitment | 574 | 78 | 496 | 67 | 4 | 33 | 19 | 18 | London (113); West Midlands - Birmingham & Solihull (32); Bristol & Bath (24); Greater Manchester - Manchester & Salford (24); Hampshire (23) |
| Engineering / Technical | 547 | 0 | 547 | 69 | 5 | 36 | 16 | 39 | London (85); Kent (29); Gloucestershire (28); Greater Manchester - Manchester & Salford (26); Northamptonshire (19) |
| Admin / Customer Service | 508 | 114 | 394 | 70 | 4.0 | 34 | 15 | 41 | London (79); Scotland Central - Tayside (26); Cheshire - Warrington & Halton (21); Greater Manchester - Manchester & Salford (17); Surrey (15) |
| Financial Advice / Mortgages | 495 | 0 | 495 | 60 | 5.0 | 31 | 15 | 19 | London (63); Essex (30); Surrey (28); Sussex (24); Kent (21) |
| Care / Support Work | 433 | 172 | 261 | 66 | 4.0 | 28 | 9 | 42 | Hampshire (37); London (29); Kent (24); Surrey (22); Sussex (15) |
| Construction / Trades / Property | 366 | 0 | 366 | 54 | 3.0 | 20 | 7 | 18 | London (98); Kent (26); Essex (20); Surrey (12); Hertfordshire (11) |
| Marketing / Digital / Creative | 345 | 0 | 345 | 53 | 3 | 19 | 7 | 33 | London (98); Surrey (12); Berkshire (11); Yorkshire - West (11); West Midlands - Birmingham & Solihull (11) |
| Management / Team Leadership | 321 | 0 | 321 | 68 | 3.0 | 22 | 6 | 14 | London (38); Sussex (19); Devon (16); Greater Manchester - Manchester & Salford (10); Yorkshire - West (10) |
| Insurance / Claims | 284 | 0 | 284 | 47 | 2 | 16 | 6 | 29 | London (64); Greater Manchester - Manchester & Salford (18); Yorkshire - West (16); Essex (14); Bristol & Bath (13) |
| Operations / General Management | 112 | 0 | 112 | 40 | 1.0 | 2 | 1 | 13 | London (25); Yorkshire - West (6); Kent (4); Hampshire (4); Lincolnshire (4) |
| Charity / Fundraising / Community | 104 | 0 | 104 | 31 | 1 | 2 | 1 | 17 | London (33); Hampshire (6); Oxfordshire (4); Surrey (4); Norfolk (3) |
| Market Research / Field Interviewing | 80 | 0 | 80 | 20 | 1.5 | 3 | 0 | 30 | Lancashire - East (7); Suffolk (5); Cornwall (5); Dorset (4); Greater Manchester - North (4) |
| Retail / Store | 70 | 0 | 70 | 37 | 1 | 1 | 1 | 10 | London (13); Essex (4); Scotland Central - Edinburgh & Lothians (3); North East - Tyneside, Wearside & Northumberland (2); Cheshire - Warrington & Halton (2) |
| Compliance / Risk / Quality | 70 | 0 | 70 | 19 | 1 | 1 | 1 | 5 | London (37); West Midlands - Birmingham & Solihull (4); Hertfordshire (3); Yorkshire - West (3); Bristol & Bath (2) |
| Procurement / Buying / Supply Chain | 47 | 0 | 47 | 29 | 1 | 1 | 1 | 1 | London (10); Essex (3); Gloucestershire (3); Devon (2); Wales South - Gwent (2) |
| Security / Emergency Services | 44 | 0 | 44 | 14 | 1.0 | 2 | 1 | 5 | London (17); Gloucestershire (6); Berkshire (2); Wiltshire (2); Bristol & Bath (2) |
| Manufacturing / Production | 28 | 0 | 28 | 10 | 1.0 | 2 | 0 | 4 | Northern Ireland - East (9); London (6); Northern Ireland - West (2); Greater Manchester - Manchester & Salford (1); Staffordshire (1) |
| Property / Housing / Planning | 26 | 0 | 26 | 15 | 1 | 1 | 0 | 1 | London (6); Surrey (4); Devon (2); Greater Manchester - Manchester & Salford (2); Scotland West - Ayrshire (1) |
| Science / Laboratory | 19 | 0 | 19 | 8 | 2.0 | 0 | 0 | 1 | London (4); Scotland West - Glasgow (4); Dorset (3); North East - Tees Valley (2); Greater Manchester - Manchester & Salford (2) |
| Hospitality / Catering | 10 | 0 | 10 | 8 | 1.0 | 0 | 0 | 0 | Sussex (2); Leicestershire (2); Cheshire - East (1); Lincolnshire (1); Cambridgeshire (1) |
| Cleaning / Domestic / Facilities | 7 | 0 | 7 | 5 | 1 | 0 | 0 | 1 | Yorkshire - West (2); Cheshire - East (1); Berkshire (1); North East - Tees Valley (1); Northamptonshire (1) |
| Employment Support / Careers | 7 | 0 | 7 | 5 | 1 | 0 | 0 | 0 | Hampshire (2); Nottinghamshire (2); Yorkshire - North (1); Greater Manchester - Manchester & Salford (1); London (1) |
| Agriculture / Environment | 3 | 0 | 3 | 3 | 1 | 0 | 0 | 0 | Devon (1); devon (1); Yorkshire - North (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 12,623 |
| still_unclassified | 2,376 |
| title_rule_pass2 | 1,635 |
| existing_register:finance_accounts | 541 |
| description_majority | 240 |
| existing_register:support_worker | 172 |
| existing_register:hr_recruitment | 78 |
| existing_register:admin_service | 61 |
| existing_register:customer_service_contact_centre | 53 |
| existing_register:warehouse_logistics | 6 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 56 | Nursery Practitioner Level 3 |
| 31 | Nursery Practitioner Level 2 |
| 27 | Nursery Room Leader |
| 26 | Nursery Manager |
| 19 | Wellbeing and Activities Assistant |
| 18 | Service Delivery Partner |
| 14 | Senior Working Capital Assistant |
| 14 | End User Technology Lead |
| 13 | Estate Planning Consultant |
| 12 | Conflicts analyst |
| 11 | Occupational Health Advisor |
| 11 | Working Capital Assistant |
| 10 | Bid Manager |
| 10 | MOT Tester |
| 10 | Property Lister |
| 9 | Account Handler |
| 9 | Toddler Room Leader (Level 3) - Cyprus Flights, Accommodation & Car Hire Included - Cyprus |
| 9 | Wellbeing and Activities Assistant - Bank |
| 8 | Nursery Practitioner |
| 8 | Client Liaison Manager |
| 8 | Senior QA Tester |
| 7 | Customer Representative Field Based |
| 7 | Senior Nursery Room Leader |
| 7 | Block Manager |
| 7 | Senior Mission System Architect - Platform Interface |
| 7 | Senior Mission System Architect - Payload |
| 7 | Combat Systems Architect - Exports |
| 6 | Data Architect |
| 6 | Class 1 Tramper |
| 6 | Class 1 Drivers |
| 6 | VAT Manager |
| 6 | Protection Advisor |
| 6 | Senior Credit Controller |
| 6 | Senior Data Governance Manager |
| 6 | Paint Sprayer |
| 6 | Business Services Senior |
| 6 | Lifeguard |
| 6 | PMO Analyst |
| 5 | Executive Search Consultant |
| 5 | Customer consultant |
| 5 | Behaviour Mentor |
| 5 | Financial Accounting Manager |
| 5 | Dementia Adviser |
| 5 | Technical Consultant - Financial Planning |
| 5 | Financial Reporting Manager |
| 5 | Speech and Language Practitioner for Children |
| 5 | Tennis Coach |
| 5 | Occupational Therapy Professional |
| 5 | Paediatric Occupational Therapy Specialist |
| 4 | Fire Stopper |
| 4 | LSA |
| 4 | Service Delivery Manager |
| 4 | Chair of the Board of Trustees |
| 4 | Chair of Trustees |
| 4 | Deputy Ward Manager |
| 4 | Aftersales Manager |
| 4 | Commercial Analyst |
| 4 | Psychology Graduate |
| 4 | Development Executive |
| 4 | Aftersales Advisor |
| 4 | Corporate Account Handler |
| 4 | Employee Benefits Consultant |
| 4 | Vinyl Vehicle Wrapper |
| 4 | Group Reporting Manager |
| 4 | Head of Corporate Solutions |
| 4 | D365 Senior SCM Consultant |
| 4 | Senior Pricing Analyst |
| 4 | Occupational Therapy Assistant |
| 4 | Relationship Manager |
| 3 | Land Agent |
| 3 | Technical Lead, Full Stack Java |
| 3 | Class 1 |
| 3 | Freelance DSA Specialist Mentor |
| 3 | Early Years Practitioner |
| 3 | Supply Teachers |

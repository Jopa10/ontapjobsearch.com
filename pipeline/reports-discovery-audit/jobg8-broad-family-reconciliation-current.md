# JobG8 register-first broad-family reconciliation

Jobs reconciled: **17,340**
Jobs assigned first from an existing selected Ontap register: **908**
Original title-rule Other / Unclassified: **4,262**
Jobs resolved by description-majority pass: **220**
Remaining Other / Unclassified after register-first + title + description passes: **2,332**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Professional Finance / Accountancy | 3,236 | 18.7% |
| Driving / Warehouse / Logistics | 2,821 | 16.3% |
| Other / Unclassified | 2,332 | 13.4% |
| Legal / Conveyancing | 1,164 | 6.7% |
| Healthcare / Clinical | 1,051 | 6.1% |
| Education / Teaching | 1,033 | 6.0% |
| Sales / Business Development | 890 | 5.1% |
| HR / Recruitment | 572 | 3.3% |
| Engineering / Technical | 500 | 2.9% |
| Admin / Customer Service | 496 | 2.9% |
| Financial Advice / Mortgages | 493 | 2.8% |
| IT / Data / Software | 466 | 2.7% |
| Care / Support Work | 426 | 2.5% |
| Construction / Trades / Property | 359 | 2.1% |
| Marketing / Digital / Creative | 328 | 1.9% |
| Management / Team Leadership | 314 | 1.8% |
| Insurance / Claims | 289 | 1.7% |
| Operations / General Management | 106 | 0.6% |
| Charity / Fundraising / Community | 103 | 0.6% |
| Market Research / Field Interviewing | 75 | 0.4% |
| Retail / Store | 70 | 0.4% |
| Compliance / Risk / Quality | 54 | 0.3% |
| Procurement / Buying / Supply Chain | 43 | 0.2% |
| Manufacturing / Production | 27 | 0.2% |
| Property / Housing / Planning | 25 | 0.1% |
| Security / Emergency Services | 21 | 0.1% |
| Science / Laboratory | 19 | 0.1% |
| Hospitality / Catering | 10 | 0.1% |
| Cleaning / Domestic / Facilities | 7 | 0.0% |
| Employment Support / Careers | 7 | 0.0% |
| Agriculture / Environment | 3 | 0.0% |
| **TOTAL** | **17,340** | **100.0%** |

## Refined family totals by salary band

Salary uses the midpoint of the available structured minimum/maximum after annualising hourly, daily, weekly or monthly amounts. Five-figure values are treated as annual even when the source period is inconsistent. The first column combines genuinely sub-£20k jobs with missing or unusable salary so every family reconciles exactly to its total.

| Broad family | Below £20k / unknown | £20k–<£35k | £35k–£45k | Over £45k | Total |
|---|---:|---:|---:|---:|---:|
| Professional Finance / Accountancy | 1,868 | 245 | 407 | 716 | 3,236 |
| Driving / Warehouse / Logistics | 1,013 | 657 | 892 | 259 | 2,821 |
| Other / Unclassified | 1,554 | 175 | 237 | 366 | 2,332 |
| Legal / Conveyancing | 855 | 35 | 60 | 214 | 1,164 |
| Healthcare / Clinical | 665 | 25 | 168 | 193 | 1,051 |
| Education / Teaching | 835 | 52 | 55 | 91 | 1,033 |
| Sales / Business Development | 472 | 119 | 114 | 185 | 890 |
| HR / Recruitment | 312 | 61 | 108 | 91 | 572 |
| Engineering / Technical | 265 | 37 | 89 | 109 | 500 |
| Admin / Customer Service | 349 | 102 | 37 | 8 | 496 |
| Financial Advice / Mortgages | 184 | 31 | 92 | 186 | 493 |
| IT / Data / Software | 292 | 6 | 39 | 129 | 466 |
| Care / Support Work | 273 | 77 | 27 | 49 | 426 |
| Construction / Trades / Property | 190 | 61 | 50 | 58 | 359 |
| Marketing / Digital / Creative | 213 | 27 | 36 | 52 | 328 |
| Management / Team Leadership | 120 | 31 | 70 | 93 | 314 |
| Insurance / Claims | 182 | 11 | 39 | 57 | 289 |
| Operations / General Management | 72 | 5 | 9 | 20 | 106 |
| Charity / Fundraising / Community | 97 | 3 | 2 | 1 | 103 |
| Market Research / Field Interviewing | 61 | 14 | 0 | 0 | 75 |
| Retail / Store | 67 | 2 | 1 | 0 | 70 |
| Compliance / Risk / Quality | 31 | 1 | 4 | 18 | 54 |
| Procurement / Buying / Supply Chain | 20 | 4 | 9 | 10 | 43 |
| Manufacturing / Production | 25 | 1 | 0 | 1 | 27 |
| Property / Housing / Planning | 11 | 5 | 1 | 8 | 25 |
| Security / Emergency Services | 12 | 1 | 0 | 8 | 21 |
| Science / Laboratory | 1 | 0 | 11 | 7 | 19 |
| Hospitality / Catering | 5 | 3 | 0 | 2 | 10 |
| Cleaning / Domestic / Facilities | 6 | 1 | 0 | 0 | 7 |
| Employment Support / Careers | 2 | 4 | 1 | 0 | 7 |
| Agriculture / Environment | 1 | 0 | 0 | 2 | 3 |
| **TOTAL** | **10,053** | **1,796** | **2,558** | **2,933** | **17,340** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Professional Finance / Accountancy | 3,236 | 537 | 2,699 | 86 | 21.5 | 70 | 56 | 101 | London (543); Yorkshire - West (146); Kent (121); Greater Manchester - Manchester & Salford (107); Sussex (105) |
| Driving / Warehouse / Logistics | 2,821 | 4 | 2,817 | 92 | 14.0 | 71 | 58 | 187 | Northamptonshire (142); Yorkshire - West (124); Hampshire (107); East Midlands (95); London (93) |
| Legal / Conveyancing | 1,164 | 0 | 1,164 | 73 | 7 | 46 | 30 | 29 | London (183); Greater Manchester - Manchester & Salford (77); Essex (54); Berkshire (52); Suffolk (52) |
| Healthcare / Clinical | 1,051 | 0 | 1,051 | 88 | 7.0 | 59 | 34 | 76 | London (124); Surrey (51); Sussex (42); Hampshire (39); Kent (31) |
| Education / Teaching | 1,033 | 0 | 1,033 | 71 | 6 | 43 | 29 | 70 | London (185); West Midlands - Birmingham & Solihull (61); Greater Manchester - Manchester & Salford (45); Sussex (41); Hertfordshire (40) |
| Sales / Business Development | 890 | 0 | 890 | 79 | 6 | 45 | 33 | 69 | London (100); Scotland Central - Tayside (30); Hampshire (28); Kent (28); Sussex (28) |
| HR / Recruitment | 572 | 80 | 492 | 67 | 4 | 33 | 19 | 16 | London (111); West Midlands - Birmingham & Solihull (30); Bristol & Bath (25); Greater Manchester - Manchester & Salford (25); Hampshire (23) |
| Engineering / Technical | 500 | 0 | 500 | 68 | 4.5 | 34 | 15 | 31 | London (71); Kent (29); Gloucestershire (23); Northamptonshire (20); Greater Manchester - Manchester & Salford (18) |
| Admin / Customer Service | 496 | 117 | 379 | 70 | 4.0 | 32 | 13 | 41 | London (75); Scotland Central - Tayside (26); Cheshire - Warrington & Halton (21); Greater Manchester - Manchester & Salford (17); Surrey (15) |
| Financial Advice / Mortgages | 493 | 0 | 493 | 60 | 5.0 | 31 | 15 | 19 | London (63); Essex (30); Surrey (26); Sussex (23); Yorkshire - West (21) |
| IT / Data / Software | 466 | 0 | 466 | 61 | 3 | 24 | 14 | 37 | London (76); Hampshire (39); Kent (35); Bristol & Bath (17); Greater Manchester - Manchester & Salford (17) |
| Care / Support Work | 426 | 170 | 256 | 67 | 4 | 26 | 9 | 40 | Hampshire (38); London (30); Kent (24); Surrey (20); Sussex (16) |
| Construction / Trades / Property | 359 | 0 | 359 | 54 | 3.0 | 19 | 6 | 18 | London (94); Kent (26); Essex (20); Surrey (12); Hertfordshire (11) |
| Marketing / Digital / Creative | 328 | 0 | 328 | 53 | 3 | 18 | 6 | 25 | London (91); Hampshire (14); Surrey (12); Berkshire (11); Northern Ireland - East (11) |
| Management / Team Leadership | 314 | 0 | 314 | 67 | 3 | 23 | 4 | 14 | London (36); Sussex (18); Devon (16); Hampshire (10); Gloucestershire (9) |
| Insurance / Claims | 289 | 0 | 289 | 47 | 3 | 16 | 7 | 29 | London (63); Greater Manchester - Manchester & Salford (19); Yorkshire - West (16); Bristol & Bath (14); Essex (14) |
| Operations / General Management | 106 | 0 | 106 | 39 | 1 | 2 | 1 | 12 | London (24); Yorkshire - West (6); Kent (4); Hampshire (4); Devon (3) |
| Charity / Fundraising / Community | 103 | 0 | 103 | 32 | 1.0 | 3 | 1 | 17 | London (29); Hampshire (6); Surrey (5); Oxfordshire (4); Sussex (4) |
| Market Research / Field Interviewing | 75 | 0 | 75 | 19 | 1 | 3 | 0 | 27 | Lancashire - East (7); Suffolk (5); Cornwall (5); Dorset (4); Greater Manchester - North (4) |
| Retail / Store | 70 | 0 | 70 | 37 | 1 | 1 | 1 | 10 | London (13); Essex (4); Scotland Central - Edinburgh & Lothians (3); North East - Tyneside, Wearside & Northumberland (2); Cheshire - Warrington & Halton (2) |
| Compliance / Risk / Quality | 54 | 0 | 54 | 18 | 1.0 | 1 | 1 | 3 | London (29); Hertfordshire (3); Bristol & Bath (2); West Midlands - Birmingham & Solihull (2); Kent (2) |
| Procurement / Buying / Supply Chain | 43 | 0 | 43 | 28 | 1.0 | 1 | 0 | 1 | London (8); Essex (3); Gloucestershire (3); Devon (2); Wales South - Gwent (2) |
| Manufacturing / Production | 27 | 0 | 27 | 10 | 1.0 | 2 | 0 | 4 | Northern Ireland - East (9); London (5); Northern Ireland - West (2); Greater Manchester - Manchester & Salford (1); Staffordshire (1) |
| Property / Housing / Planning | 25 | 0 | 25 | 15 | 1 | 1 | 0 | 1 | London (6); Surrey (4); Devon (2); Scotland West - Ayrshire (1); Northern Ireland - East (1) |
| Security / Emergency Services | 21 | 0 | 21 | 10 | 1.0 | 1 | 0 | 1 | London (9); Bristol & Bath (2); Kent (2); Berkshire (1); West Midlands - Coventry & Warwickshire (1) |
| Science / Laboratory | 19 | 0 | 19 | 8 | 2.0 | 0 | 0 | 1 | London (4); Scotland West - Glasgow (4); Dorset (3); North East - Tees Valley (2); Greater Manchester - Manchester & Salford (2) |
| Hospitality / Catering | 10 | 0 | 10 | 7 | 1 | 0 | 0 | 0 | Leicestershire (2); Lincolnshire (2); Sussex (2); Cheshire - East (1); Nottinghamshire (1) |
| Cleaning / Domestic / Facilities | 7 | 0 | 7 | 5 | 1 | 0 | 0 | 1 | Yorkshire - West (2); Cheshire - East (1); Berkshire (1); North East - Tees Valley (1); Northamptonshire (1) |
| Employment Support / Careers | 7 | 0 | 7 | 5 | 1 | 0 | 0 | 0 | Hampshire (2); Nottinghamshire (2); Yorkshire - North (1); Greater Manchester - Manchester & Salford (1); London (1) |
| Agriculture / Environment | 3 | 0 | 3 | 3 | 1 | 0 | 0 | 0 | Devon (1); devon (1); Yorkshire - North (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 12,296 |
| still_unclassified | 2,332 |
| title_rule_pass2 | 1,584 |
| existing_register:finance_accounts | 537 |
| description_majority | 220 |
| existing_register:support_worker | 170 |
| existing_register:hr_recruitment | 80 |
| existing_register:admin_service | 64 |
| existing_register:customer_service_contact_centre | 53 |
| existing_register:warehouse_logistics | 4 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 63 | Deliveroo Rider |
| 55 | Nursery Practitioner Level 3 |
| 30 | Nursery Practitioner Level 2 |
| 28 | Nursery Manager |
| 28 | Nursery Room Leader |
| 17 | Service Delivery Partner |
| 15 | Wellbeing and Activities Assistant |
| 14 | Senior Working Capital Assistant |
| 14 | End User Technology Lead |
| 13 | Estate Planning Consultant |
| 12 | Conflicts analyst |
| 11 | Occupational Health Advisor |
| 11 | Working Capital Assistant |
| 10 | Account Handler |
| 10 | MOT Tester |
| 9 | Property Lister |
| 9 | Toddler Room Leader (Level 3) - Cyprus Flights, Accommodation & Car Hire Included - Cyprus |
| 9 | Wellbeing and Activities Assistant - Bank |
| 8 | Bid Manager |
| 8 | Nursery Practitioner |
| 8 | Senior Nursery Room Leader |
| 7 | Customer Representative Field Based |
| 7 | Block Manager |
| 7 | Senior Mission System Architect - Platform Interface |
| 7 | Senior Mission System Architect - Payload |
| 7 | Combat Systems Architect - Exports |
| 6 | Class 1 Tramper |
| 6 | Class 1 Drivers |
| 6 | Protection Advisor |
| 6 | Senior Credit Controller |
| 6 | Paint Sprayer |
| 6 | Business Services Senior |
| 6 | PMO Analyst |
| 6 | Client Liaison Manager |
| 5 | Executive Search Consultant |
| 5 | Deputy Ward Manager |
| 5 | Customer consultant |
| 5 | Behaviour Mentor |
| 5 | Financial Accounting Manager |
| 5 | VAT Manager |
| 5 | Technical Consultant - Financial Planning |
| 5 | Financial Reporting Manager |
| 5 | Speech and Language Practitioner for Children |
| 4 | Fire Stopper |
| 4 | LSA |
| 4 | Chair of the Board of Trustees |
| 4 | Chair of Trustees |
| 4 | Functional Specialist |
| 4 | Aftersales Manager |
| 4 | Head of Business |
| 4 | Psychology Graduate |
| 4 | Development Executive |
| 4 | Dementia Adviser |
| 4 | Aftersales Advisor |
| 4 | Corporate Account Handler |
| 4 | Employee Benefits Consultant |
| 4 | Vinyl Vehicle Wrapper |
| 4 | Group Reporting Manager |
| 4 | Head of Corporate Solutions |
| 4 | D365 Senior SCM Consultant |
| 4 | Philanthropy Manager |
| 4 | Senior Pricing Analyst |
| 4 | Occupational Therapy Assistant |
| 4 | Occupational Therapy Professional |
| 4 | Paediatric Occupational Therapy Specialist |
| 3 | Land Agent |
| 3 | Class 1 |
| 3 | Early Years Practitioner |
| 3 | Supply Teachers |
| 3 | Nursery Assistant |
| 3 | EHCP Assistant |
| 3 | F5 SME |
| 3 | Data Architect |
| 3 | IT Manager |
| 3 | Paraplanning Manager |

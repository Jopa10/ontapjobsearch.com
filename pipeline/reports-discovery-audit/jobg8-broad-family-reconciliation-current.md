# JobG8 register-first broad-family reconciliation

Jobs reconciled: **20,000**
Jobs assigned first from an existing selected Ontap register: **2,007**
Original title-rule Other / Unclassified: **5,280**
Jobs resolved by description-majority pass: **328**
Remaining Other / Unclassified after register-first + title + description passes: **3,007**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Professional Finance / Accountancy | 3,490 | 17.4% |
| Other / Unclassified | 3,007 | 15.0% |
| Sales / Business Development | 2,302 | 11.5% |
| Admin / Customer Service | 2,300 | 11.5% |
| Legal / Conveyancing | 1,656 | 8.3% |
| HR / Recruitment | 1,062 | 5.3% |
| IT / Data / Software | 769 | 3.8% |
| Engineering / Technical | 689 | 3.4% |
| Marketing / Digital / Creative | 587 | 2.9% |
| Driving / Warehouse / Logistics | 517 | 2.6% |
| Construction / Trades / Property | 511 | 2.6% |
| Care / Support Work | 507 | 2.5% |
| Education / Teaching | 472 | 2.4% |
| Insurance / Claims | 351 | 1.8% |
| Healthcare / Clinical | 280 | 1.4% |
| Management / Team Leadership | 279 | 1.4% |
| Property / Housing / Planning | 249 | 1.2% |
| Operations / General Management | 195 | 1.0% |
| Compliance / Risk / Quality | 164 | 0.8% |
| Market Research / Field Interviewing | 122 | 0.6% |
| Procurement / Buying / Supply Chain | 107 | 0.5% |
| Financial Advice / Mortgages | 102 | 0.5% |
| Charity / Fundraising / Community | 102 | 0.5% |
| Security / Emergency Services | 48 | 0.2% |
| Employment Support / Careers | 43 | 0.2% |
| Retail / Store | 31 | 0.2% |
| Cleaning / Domestic / Facilities | 28 | 0.1% |
| Hospitality / Catering | 16 | 0.1% |
| Manufacturing / Production | 12 | 0.1% |
| Agriculture / Environment | 1 | 0.0% |
| Science / Laboratory | 1 | 0.0% |
| **TOTAL** | **20,000** | **100.0%** |

## Refined family totals by salary band

Salary uses the midpoint of the available structured minimum/maximum after annualising hourly, daily, weekly or monthly amounts. Five-figure values are treated as annual even when the source period is inconsistent. The first column combines genuinely sub-£20k jobs with missing or unusable salary so every family reconciles exactly to its total.

| Broad family | Below £20k / unknown | £20k–<£35k | £35k–£45k | Over £45k | Total |
|---|---:|---:|---:|---:|---:|
| Professional Finance / Accountancy | 1,392 | 727 | 531 | 840 | 3,490 |
| Other / Unclassified | 1,508 | 574 | 313 | 612 | 3,007 |
| Sales / Business Development | 536 | 592 | 486 | 688 | 2,302 |
| Admin / Customer Service | 487 | 1,425 | 303 | 85 | 2,300 |
| Legal / Conveyancing | 1,015 | 166 | 105 | 370 | 1,656 |
| HR / Recruitment | 223 | 413 | 266 | 160 | 1,062 |
| IT / Data / Software | 394 | 35 | 79 | 261 | 769 |
| Engineering / Technical | 292 | 89 | 114 | 194 | 689 |
| Marketing / Digital / Creative | 216 | 119 | 125 | 127 | 587 |
| Driving / Warehouse / Logistics | 141 | 234 | 100 | 42 | 517 |
| Construction / Trades / Property | 108 | 109 | 130 | 164 | 511 |
| Care / Support Work | 129 | 279 | 52 | 47 | 507 |
| Education / Teaching | 285 | 64 | 53 | 70 | 472 |
| Insurance / Claims | 183 | 35 | 57 | 76 | 351 |
| Healthcare / Clinical | 58 | 50 | 59 | 113 | 280 |
| Management / Team Leadership | 77 | 52 | 64 | 86 | 279 |
| Property / Housing / Planning | 40 | 38 | 89 | 82 | 249 |
| Operations / General Management | 90 | 9 | 29 | 67 | 195 |
| Compliance / Risk / Quality | 54 | 21 | 22 | 67 | 164 |
| Market Research / Field Interviewing | 82 | 39 | 0 | 1 | 122 |
| Procurement / Buying / Supply Chain | 35 | 44 | 10 | 18 | 107 |
| Financial Advice / Mortgages | 11 | 25 | 35 | 31 | 102 |
| Charity / Fundraising / Community | 72 | 14 | 12 | 4 | 102 |
| Security / Emergency Services | 19 | 9 | 9 | 11 | 48 |
| Employment Support / Careers | 5 | 33 | 5 | 0 | 43 |
| Retail / Store | 22 | 7 | 0 | 2 | 31 |
| Cleaning / Domestic / Facilities | 6 | 20 | 2 | 0 | 28 |
| Hospitality / Catering | 6 | 8 | 2 | 0 | 16 |
| Manufacturing / Production | 4 | 2 | 3 | 3 | 12 |
| Agriculture / Environment | 0 | 1 | 0 | 0 | 1 |
| Science / Laboratory | 1 | 0 | 0 | 0 | 1 |
| **TOTAL** | **7,491** | **5,233** | **3,055** | **4,221** | **20,000** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Professional Finance / Accountancy | 3,490 | 732 | 2,758 | 91 | 16 | 67 | 56 | 449 | London (698); Hampshire (145); Surrey (98); Berkshire (97); Sussex (91) |
| Sales / Business Development | 2,302 | 0 | 2,302 | 86 | 8.0 | 52 | 40 | 497 | London (597); Berkshire (81); Hampshire (69); Bristol & Bath (54); Kent (51) |
| Admin / Customer Service | 2,300 | 916 | 1,384 | 87 | 10 | 54 | 45 | 509 | London (519); Surrey (78); Hampshire (67); Hertfordshire (59); Kent (58) |
| Legal / Conveyancing | 1,656 | 0 | 1,656 | 77 | 10 | 51 | 39 | 93 | London (265); Essex (99); Greater Manchester - Manchester & Salford (71); Surrey (65); Suffolk (63) |
| HR / Recruitment | 1,062 | 146 | 916 | 72 | 6.0 | 38 | 24 | 233 | London (286); Hampshire (38); Devon (29); Bristol & Bath (27); Nottinghamshire (25) |
| IT / Data / Software | 769 | 0 | 769 | 63 | 5 | 34 | 17 | 93 | London (227); Hampshire (36); Bristol & Bath (35); Berkshire (29); Greater Manchester - Manchester & Salford (19) |
| Engineering / Technical | 689 | 0 | 689 | 69 | 4 | 32 | 19 | 112 | London (155); Hampshire (28); Bristol & Bath (26); North East - Tyneside, Wearside & Northumberland (18); Berkshire (17) |
| Marketing / Digital / Creative | 587 | 0 | 587 | 56 | 3.0 | 25 | 14 | 79 | London (171); Nottinghamshire (24); Greater Manchester - Manchester & Salford (23); Kent (18); Berkshire (18) |
| Driving / Warehouse / Logistics | 517 | 11 | 506 | 67 | 3 | 28 | 10 | 156 | London (45); Kent (21); Hampshire (19); Staffordshire (15); Essex (13) |
| Construction / Trades / Property | 511 | 0 | 511 | 56 | 4.0 | 24 | 9 | 65 | London (165); Essex (27); Hampshire (22); Sussex (19); Kent (15) |
| Care / Support Work | 507 | 202 | 305 | 66 | 3.0 | 24 | 9 | 143 | London (62); Sussex (31); Hampshire (18); Kent (15); Surrey (15) |
| Education / Teaching | 472 | 0 | 472 | 54 | 3.0 | 23 | 8 | 134 | London (80); Gloucestershire (30); Bristol & Bath (17); Essex (14); Sussex (13) |
| Insurance / Claims | 351 | 0 | 351 | 51 | 2 | 21 | 7 | 42 | London (89); Yorkshire - West (17); Essex (17); Greater Manchester - Manchester & Salford (16); Kent (14) |
| Healthcare / Clinical | 280 | 0 | 280 | 47 | 2 | 12 | 5 | 73 | London (50); Essex (16); Bristol & Bath (16); Surrey (13); Berkshire (10) |
| Management / Team Leadership | 279 | 0 | 279 | 57 | 2 | 13 | 3 | 37 | London (60); Hampshire (14); Sussex (13); Greater Manchester - Manchester & Salford (8); Kent (7) |
| Property / Housing / Planning | 249 | 0 | 249 | 46 | 2.0 | 11 | 3 | 31 | London (70); Kent (17); Essex (15); Gloucestershire (8); Bristol & Bath (8) |
| Operations / General Management | 195 | 0 | 195 | 41 | 2 | 7 | 2 | 34 | London (61); Hampshire (12); Berkshire (9); Bristol & Bath (6); Hertfordshire (5) |
| Compliance / Risk / Quality | 164 | 0 | 164 | 40 | 2.0 | 5 | 1 | 29 | London (52); West Midlands - Coventry & Warwickshire (5); North East - Tyneside, Wearside & Northumberland (5); Hampshire (5); Essex (5) |
| Market Research / Field Interviewing | 122 | 0 | 122 | 31 | 3 | 6 | 1 | 18 | London (16); Kent (9); Lancashire - East (7); Lincolnshire (6); Dorset (6) |
| Procurement / Buying / Supply Chain | 107 | 0 | 107 | 27 | 2 | 4 | 1 | 25 | London (21); Hertfordshire (6); Greater Manchester - Manchester & Salford (5); Essex (5); Kent (4) |
| Financial Advice / Mortgages | 102 | 0 | 102 | 36 | 1.0 | 3 | 1 | 16 | London (21); Kent (7); Surrey (7); Leicestershire (4); Lincolnshire (3) |
| Charity / Fundraising / Community | 102 | 0 | 102 | 31 | 2 | 1 | 1 | 19 | London (25); Hampshire (4); Essex (3); Surrey (3); Shropshire (3) |
| Security / Emergency Services | 48 | 0 | 48 | 17 | 1 | 1 | 1 | 11 | London (16); West Midlands - Coventry & Warwickshire (2); Sussex (2); Wiltshire (2); Nottinghamshire (2) |
| Employment Support / Careers | 43 | 0 | 43 | 17 | 1 | 0 | 0 | 16 | London (4); Bristol & Bath (2); Kent (2); Surrey (2); Yorkshire - North (2) |
| Retail / Store | 31 | 0 | 31 | 17 | 1 | 1 | 0 | 3 | London (7); Essex (2); Surrey (2); Hertfordshire (2); Yorkshire - North (2) |
| Cleaning / Domestic / Facilities | 28 | 0 | 28 | 15 | 1 | 1 | 0 | 3 | London (9); Hampshire (2); Essex (2); West Midlands (1); Merseyside - Wirral (1) |
| Hospitality / Catering | 16 | 0 | 16 | 6 | 1.5 | 1 | 0 | 1 | London (8); Northamptonshire (2); Cambridgeshire (2); Hertfordshire (1); Hampshire (1) |
| Manufacturing / Production | 12 | 0 | 12 | 11 | 1 | 0 | 0 | 0 | Nottinghamshire (2); Greater Manchester - Manchester & Salford (1); Suffolk (1); Shropshire (1); London (1) |
| Agriculture / Environment | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | Shropshire (1) |
| Science / Laboratory | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | Hertfordshire (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 12,958 |
| still_unclassified | 3,007 |
| title_rule_pass2 | 1,700 |
| existing_register:finance_accounts | 732 |
| existing_register:admin_service | 635 |
| description_majority | 328 |
| existing_register:customer_service_contact_centre | 281 |
| existing_register:support_worker | 202 |
| existing_register:hr_recruitment | 146 |
| existing_register:warehouse_logistics | 11 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 22 | External Examiner- BTEC - HN 4-7 - Higher Technical ... |
| 17 | Corporate Associate |
| 15 | Disability Assessor |
| 15 | Pitch Executive |
| 15 | Pitch Executive (5.00pm - 1:30am) |
| 14 | Associate - Corporate |
| 14 | Associate - disputes |
| 13 | Disputes Associate |
| 10 | Sports Coach |
| 10 | SOC Analyst Programme |
| 9 | Neighbourhood Officer |
| 9 | Estates Manager |
| 9 | Repairs Planner |
| 9 | Account Handler |
| 7 | CRM Manager |
| 7 | Change Manager |
| 7 | Partnership Executive |
| 6 | Facilities Officer |
| 6 | ER Specialist |
| 6 | Territory Representative |
| 6 | Lead Identity Manager |
| 6 | Examiner - International Advanced Level - History (2016 ... |
| 5 | National Account Director |
| 5 | Block Manager |
| 5 | Data Protection Officer |
| 5 | Tenancy Sustainment Officer |
| 5 | Senior Manager |
| 5 | Immigration Partner |
| 5 | Account Director |
| 5 | Team Assistant |
| 5 | HSE Advisor |
| 5 | Occupational Health Advisor |
| 5 | Regional Customer Relationship Manager |
| 5 | Behaviour Mentor |
| 5 | Estate Planning Consultant |
| 5 | Planner - Transportation |
| 4 | Multiskilled Host |
| 4 | Bid Manager |
| 4 | Employment Partner |
| 4 | Housing Standards Officer |
| 4 | Project Support Officer |
| 4 | Contract Support |
| 4 | Group Reporting Manager |
| 4 | Transaction Manager |
| 4 | New Store Opening Training Manager |
| 4 | Business Change Manager |
| 4 | Nursery Manager |
| 4 | Chair of Trustees |
| 4 | Paid Media Manager |
| 4 | Customer Consultant |
| 4 | Learning & Development Manager |
| 4 | Customer Relations Manager |
| 4 | Graduate Commercial Business Trainee |
| 4 | Data Architect |
| 4 | Head of Property and Facilities |
| 4 | Operations Assistant |
| 4 | Early Years Educator |
| 4 | Nursery Practitioner |
| 4 | Customer Services Executive |
| 4 | Mentor / Coach |
| 4 | Head of Property |
| 4 | Tax & Trusts Manager |
| 4 | Resourcer |
| 4 | Operational Trainer |
| 4 | Housing Options Officer |
| 4 | Stores Operative |
| 4 | Interpreter |
| 4 | Senior CRA - IQVIA Biotech |
| 3 | Business Services Senior |
| 3 | Training Manager |
| 3 | Civil Enforcement Officer |
| 3 | Commercial Analyst |
| 3 | Planner |
| 3 | Independent Living Officer |
| 3 | Category Insights Manager |

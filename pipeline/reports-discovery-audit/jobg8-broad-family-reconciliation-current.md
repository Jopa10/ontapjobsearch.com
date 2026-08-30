# JobG8 register-first broad-family reconciliation

Jobs reconciled: **10,000**
Jobs assigned first from an existing selected Ontap register: **673**
Original title-rule Other / Unclassified: **3,536**
Jobs resolved by description-majority pass: **69**
Remaining Other / Unclassified after register-first + title + description passes: **1,882**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Other / Unclassified | 1,882 | 18.8% |
| Sales / Business Development | 1,161 | 11.6% |
| IT / Data / Software | 1,029 | 10.3% |
| Admin / Customer Service | 933 | 9.3% |
| Professional Finance / Accountancy | 832 | 8.3% |
| Healthcare / Clinical | 670 | 6.7% |
| Engineering / Technical | 579 | 5.8% |
| Management / Team Leadership | 488 | 4.9% |
| Marketing / Digital / Creative | 298 | 3.0% |
| Operations / General Management | 297 | 3.0% |
| Care / Support Work | 286 | 2.9% |
| HR / Recruitment | 221 | 2.2% |
| Retail / Store | 203 | 2.0% |
| Legal / Conveyancing | 194 | 1.9% |
| Market Research / Field Interviewing | 175 | 1.8% |
| Construction / Trades / Property | 120 | 1.2% |
| Property / Housing / Planning | 75 | 0.8% |
| Financial Advice / Mortgages | 72 | 0.7% |
| Insurance / Claims | 70 | 0.7% |
| Compliance / Risk / Quality | 65 | 0.7% |
| Procurement / Buying / Supply Chain | 63 | 0.6% |
| Education / Teaching | 61 | 0.6% |
| Security / Emergency Services | 45 | 0.4% |
| Charity / Fundraising / Community | 40 | 0.4% |
| Driving / Warehouse / Logistics | 40 | 0.4% |
| Hospitality / Catering | 27 | 0.3% |
| Employment Support / Careers | 20 | 0.2% |
| Cleaning / Domestic / Facilities | 16 | 0.2% |
| Manufacturing / Production | 16 | 0.2% |
| Agriculture / Environment | 12 | 0.1% |
| Science / Laboratory | 10 | 0.1% |
| **TOTAL** | **10,000** | **100.0%** |

## Refined family totals by salary band

Salary uses the midpoint of the available structured minimum/maximum after annualising hourly, daily, weekly or monthly amounts. Five-figure values are treated as annual even when the source period is inconsistent. The first column combines genuinely sub-£20k jobs with missing or unusable salary so every family reconciles exactly to its total.

| Broad family | Below £20k / unknown | £20k–<£35k | £35k–£45k | Over £45k | Total |
|---|---:|---:|---:|---:|---:|
| Other / Unclassified | 729 | 327 | 240 | 586 | 1,882 |
| Sales / Business Development | 309 | 265 | 223 | 364 | 1,161 |
| IT / Data / Software | 386 | 31 | 134 | 478 | 1,029 |
| Admin / Customer Service | 203 | 623 | 77 | 30 | 933 |
| Professional Finance / Accountancy | 219 | 156 | 165 | 292 | 832 |
| Healthcare / Clinical | 427 | 47 | 82 | 114 | 670 |
| Engineering / Technical | 198 | 51 | 100 | 230 | 579 |
| Management / Team Leadership | 121 | 152 | 118 | 97 | 488 |
| Marketing / Digital / Creative | 105 | 47 | 74 | 72 | 298 |
| Operations / General Management | 132 | 11 | 39 | 115 | 297 |
| Care / Support Work | 129 | 119 | 22 | 16 | 286 |
| HR / Recruitment | 47 | 112 | 44 | 18 | 221 |
| Retail / Store | 72 | 89 | 28 | 14 | 203 |
| Legal / Conveyancing | 51 | 59 | 21 | 63 | 194 |
| Market Research / Field Interviewing | 145 | 30 | 0 | 0 | 175 |
| Construction / Trades / Property | 26 | 28 | 28 | 38 | 120 |
| Property / Housing / Planning | 18 | 17 | 16 | 24 | 75 |
| Financial Advice / Mortgages | 15 | 8 | 16 | 33 | 72 |
| Insurance / Claims | 38 | 10 | 12 | 10 | 70 |
| Compliance / Risk / Quality | 29 | 2 | 6 | 28 | 65 |
| Procurement / Buying / Supply Chain | 23 | 10 | 12 | 18 | 63 |
| Education / Teaching | 33 | 19 | 3 | 6 | 61 |
| Security / Emergency Services | 16 | 3 | 11 | 15 | 45 |
| Charity / Fundraising / Community | 33 | 3 | 4 | 0 | 40 |
| Driving / Warehouse / Logistics | 11 | 23 | 3 | 3 | 40 |
| Hospitality / Catering | 7 | 12 | 5 | 3 | 27 |
| Employment Support / Careers | 8 | 12 | 0 | 0 | 20 |
| Cleaning / Domestic / Facilities | 4 | 11 | 1 | 0 | 16 |
| Manufacturing / Production | 2 | 7 | 3 | 4 | 16 |
| Agriculture / Environment | 2 | 3 | 4 | 3 | 12 |
| Science / Laboratory | 2 | 1 | 3 | 4 | 10 |
| **TOTAL** | **3,540** | **2,288** | **1,494** | **2,678** | **10,000** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Sales / Business Development | 1,161 | 0 | 1,161 | 83 | 8 | 60 | 35 | 85 | London (156); Greater Manchester - Manchester & Salford (49); Hampshire (45); Hertfordshire (38); Kent (35) |
| IT / Data / Software | 1,029 | 0 | 1,029 | 68 | 6.0 | 40 | 27 | 79 | London (218); Hampshire (63); Greater Manchester - Manchester & Salford (63); Bristol & Bath (45); Kent (45) |
| Admin / Customer Service | 933 | 344 | 589 | 78 | 5.0 | 43 | 24 | 176 | London (147); Surrey (42); Hampshire (34); Kent (25); Leicestershire (25) |
| Professional Finance / Accountancy | 832 | 140 | 692 | 80 | 7.0 | 48 | 30 | 68 | London (121); Yorkshire - West (35); Yorkshire - North (24); Merseyside - Liverpool (24); Bristol & Bath (22) |
| Healthcare / Clinical | 670 | 0 | 670 | 81 | 3 | 35 | 16 | 66 | London (111); Surrey (40); Hampshire (36); Sussex (33); North East - Tyneside, Wearside & Northumberland (24) |
| Engineering / Technical | 579 | 0 | 579 | 63 | 5 | 35 | 19 | 44 | London (98); Greater Manchester - Manchester & Salford (39); Kent (28); Bristol & Bath (26); Hampshire (17) |
| Management / Team Leadership | 488 | 0 | 488 | 76 | 4.0 | 32 | 17 | 24 | London (43); Essex (21); Oxfordshire (20); Sussex (19); Hampshire (16) |
| Marketing / Digital / Creative | 298 | 0 | 298 | 52 | 2.5 | 16 | 4 | 29 | London (86); Greater Manchester - Manchester & Salford (14); Yorkshire - West (11); Hampshire (10); Surrey (9) |
| Operations / General Management | 297 | 0 | 297 | 55 | 4 | 22 | 6 | 18 | London (41); Oxfordshire (14); Hampshire (14); Bristol & Bath (12); Yorkshire - West (10) |
| Care / Support Work | 286 | 127 | 159 | 64 | 2.0 | 15 | 5 | 31 | London (42); Oxfordshire (19); Hampshire (15); Surrey (14); Somerset (10) |
| HR / Recruitment | 221 | 60 | 161 | 43 | 3 | 11 | 3 | 35 | London (33); Bristol & Bath (22); Hampshire (11); Yorkshire - West (9); Essex (6) |
| Retail / Store | 203 | 0 | 203 | 57 | 2 | 10 | 2 | 27 | London (21); Yorkshire - North (15); Wiltshire (9); Oxfordshire (9); Kent (9) |
| Legal / Conveyancing | 194 | 0 | 194 | 50 | 2.0 | 9 | 1 | 9 | London (57); Wiltshire (9); Yorkshire - South (8); Sussex (7); Greater Manchester - Manchester & Salford (7) |
| Market Research / Field Interviewing | 175 | 0 | 175 | 37 | 2 | 9 | 3 | 56 | Devon (12); Wiltshire (12); London (10); Scotland Central - Tayside (8); Berkshire (7) |
| Construction / Trades / Property | 120 | 0 | 120 | 40 | 2.0 | 4 | 1 | 10 | London (20); Bristol & Bath (5); Essex (5); Greater Manchester - Manchester & Salford (5); Nottinghamshire (4) |
| Property / Housing / Planning | 75 | 0 | 75 | 33 | 1 | 2 | 0 | 12 | London (8); Hertfordshire (5); Sussex (4); West Midlands - Coventry & Warwickshire (4); North East - Tyneside, Wearside & Northumberland (3) |
| Financial Advice / Mortgages | 72 | 0 | 72 | 32 | 2.0 | 1 | 0 | 3 | London (8); Wiltshire (4); Leicestershire (4); Greater Manchester - Manchester & Salford (4); Surrey (3) |
| Insurance / Claims | 70 | 0 | 70 | 21 | 1 | 2 | 1 | 9 | London (28); Norfolk (5); Essex (3); West Midlands - Birmingham & Solihull (3); East Midlands (2) |
| Compliance / Risk / Quality | 65 | 0 | 65 | 28 | 1.0 | 1 | 1 | 5 | London (15); Bristol & Bath (4); Greater Manchester - Manchester & Salford (4); West Midlands - Birmingham & Solihull (3); Scotland Central - Edinburgh & Lothians (3) |
| Procurement / Buying / Supply Chain | 63 | 0 | 63 | 25 | 1 | 1 | 1 | 11 | London (14); Essex (4); Yorkshire - West (4); Devon (3); Hampshire (3) |
| Education / Teaching | 61 | 0 | 61 | 22 | 1.0 | 2 | 1 | 9 | London (13); Cumbria - South (6); Lancashire - North (4); Wiltshire (3); Yorkshire - West (3) |
| Security / Emergency Services | 45 | 0 | 45 | 15 | 1 | 2 | 1 | 10 | London (10); Hampshire (6); Bristol & Bath (3); Berkshire (3); Nottinghamshire (2) |
| Charity / Fundraising / Community | 40 | 0 | 40 | 16 | 1.5 | 1 | 1 | 4 | London (11); Buckinghamshire (4); West Midlands - Birmingham & Solihull (3); Hampshire (2); Wales South - Gwent (2) |
| Driving / Warehouse / Logistics | 40 | 2 | 38 | 25 | 1 | 0 | 0 | 6 | London (4); Leicestershire (2); Worcestershire (2); Staffordshire (2); Buckinghamshire (2) |
| Hospitality / Catering | 27 | 0 | 27 | 12 | 1.5 | 1 | 0 | 4 | London (5); Norfolk (3); Gloucestershire (3); Oxfordshire (2); Sussex (2) |
| Employment Support / Careers | 20 | 0 | 20 | 12 | 1.0 | 0 | 0 | 2 | London (3); Yorkshire - North (3); Wales - Mid (2); Bristol & Bath (2); Surrey (1) |
| Cleaning / Domestic / Facilities | 16 | 0 | 16 | 10 | 1.0 | 0 | 0 | 3 | Northamptonshire (3); Bristol & Bath (2); London (1); Wiltshire (1); Yorkshire - South (1) |
| Manufacturing / Production | 16 | 0 | 16 | 11 | 1 | 0 | 0 | 2 | London (3); Gloucestershire (2); Suffolk (1); Worcestershire (1); Wiltshire (1) |
| Agriculture / Environment | 12 | 0 | 12 | 7 | 2 | 0 | 0 | 0 | London (3); Cheshire - Warrington & Halton (2); Kent (2); Sussex (2); Devon (1) |
| Science / Laboratory | 10 | 0 | 10 | 4 | 1.5 | 0 | 0 | 3 | London (3); Gloucestershire (2); Worcestershire (1); Yorkshire - West (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 5,836 |
| still_unclassified | 1,882 |
| title_rule_pass2 | 1,540 |
| existing_register:admin_service | 251 |
| existing_register:finance_accounts | 140 |
| existing_register:support_worker | 127 |
| existing_register:customer_service_contact_centre | 93 |
| description_majority | 69 |
| existing_register:hr_recruitment | 60 |
| existing_register:warehouse_logistics | 2 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 22 | Contracts Manager |
| 15 | Junior Network Analyst |
| 11 | Trainee Junior Network Consultant |
| 10 | Trainee Network Analyst |
| 10 | Customer Representative Field Based |
| 9 | Sub Agent |
| 7 | Aftersales Manager |
| 7 | Technical Lead |
| 7 | Bid Manager |
| 6 | Client Relationship Manager |
| 6 | Autocentre Manager |
| 6 | Social Impact & Community Enterprise Manager (Food Insecurity) - 6m FTC |
| 6 | Associate Director |
| 6 | Door to Door Canvasser |
| 6 | Customer Relations Manager |
| 6 | Housing Estates Officer |
| 5 | Tenancy Sustainment Officer |
| 5 | Contract Manager |
| 5 | Ward Manager |
| 5 | Productivity Manager |
| 5 | General Foreman |
| 5 | Implementation Consultant |
| 4 | Development Manager |
| 4 | Insolvency Manager |
| 4 | Planner |
| 4 | Property Valuer |
| 4 | Head of IT |
| 4 | Shift Manager |
| 4 | Partnerships Manager |
| 4 | Remote Game Tester |
| 4 | Cost & Productivity - Senior Manager |
| 4 | Head Installer |
| 4 | Subject Lead History and Politics |
| 3 | Property Officer |
| 3 | Installer Development Representative |
| 3 | Senior Cost Consultant |
| 3 | Senior Authorised Person |
| 3 | Head of Planning |
| 3 | Technical Manager |
| 3 | Hairdresser |
| 3 | Senior Contracts Manager |
| 3 | Pre-reg 2027 |
| 3 | Partnership Manager |
| 3 | Associate Director of Commercial Partnerships |
| 3 | Packaging Technologist |
| 3 | Media Measurement Lead |
| 3 | Cost & Productivity Senior Manager |
| 3 | Cost & Productivity Manager (TMT) |
| 3 | Contractual Advisor |
| 3 | Development Executive |
| 3 | Applications Specialist, Cardiology IT / PACS Systems |
| 3 | Vulnerability Researcher |
| 3 | Portfolio Manager |
| 3 | CRO Analyst |
| 3 | Data Architect |
| 3 | 2nd Line Support |
| 3 | Service Delivery Manager |
| 3 | Senior User Researcher |
| 3 | Butchery Manager |
| 3 | F5 SME |
| 2 | NCR Facilitator |
| 2 | Insight and Measurement Manager |
| 2 | Senior Analyst |
| 2 | Hire Desk Manager |
| 2 | Design Director |
| 2 | Corporate Senior Associate |
| 2 | Regional Quality/Safety Lead |
| 2 | Technical Advisor |
| 2 | Concession Manager |
| 2 | Senior Land Acquisition Manager |
| 2 | Senior Planner |
| 2 | Expeditions & Fieldwork Officer |
| 2 | Architectural Technologist |
| 2 | Group Reporting Manager |
| 2 | Personal Banker |

# JobG8 register-first broad-family reconciliation

Jobs reconciled: **10,000**
Jobs assigned first from an existing selected Ontap register: **784**
Original title-rule Other / Unclassified: **2,998**
Jobs resolved by description-majority pass: **115**
Remaining Other / Unclassified after register-first + title + description passes: **1,744**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Sales / Business Development | 1,794 | 17.9% |
| Other / Unclassified | 1,744 | 17.4% |
| Admin / Customer Service | 1,264 | 12.6% |
| IT / Data / Software | 842 | 8.4% |
| Professional Finance / Accountancy | 535 | 5.3% |
| Marketing / Digital / Creative | 530 | 5.3% |
| Engineering / Technical | 428 | 4.3% |
| Healthcare / Clinical | 413 | 4.1% |
| HR / Recruitment | 335 | 3.4% |
| Legal / Conveyancing | 332 | 3.3% |
| Management / Team Leadership | 231 | 2.3% |
| Care / Support Work | 225 | 2.2% |
| Retail / Store | 213 | 2.1% |
| Operations / General Management | 160 | 1.6% |
| Insurance / Claims | 150 | 1.5% |
| Construction / Trades / Property | 124 | 1.2% |
| Market Research / Field Interviewing | 120 | 1.2% |
| Financial Advice / Mortgages | 97 | 1.0% |
| Procurement / Buying / Supply Chain | 71 | 0.7% |
| Property / Housing / Planning | 65 | 0.7% |
| Compliance / Risk / Quality | 49 | 0.5% |
| Driving / Warehouse / Logistics | 48 | 0.5% |
| Charity / Fundraising / Community | 40 | 0.4% |
| Education / Teaching | 35 | 0.4% |
| Hospitality / Catering | 33 | 0.3% |
| Security / Emergency Services | 28 | 0.3% |
| Manufacturing / Production | 25 | 0.2% |
| Employment Support / Careers | 23 | 0.2% |
| Science / Laboratory | 20 | 0.2% |
| Cleaning / Domestic / Facilities | 14 | 0.1% |
| Agriculture / Environment | 12 | 0.1% |
| **TOTAL** | **10,000** | **100.0%** |

## Refined family totals by salary band

Salary uses the midpoint of the available structured minimum/maximum after annualising hourly, daily, weekly or monthly amounts. Five-figure values are treated as annual even when the source period is inconsistent. The first column combines genuinely sub-£20k jobs with missing or unusable salary so every family reconciles exactly to its total.

| Broad family | Below £20k / unknown | £20k–<£35k | £35k–£45k | Over £45k | Total |
|---|---:|---:|---:|---:|---:|
| Sales / Business Development | 617 | 361 | 299 | 517 | 1,794 |
| Other / Unclassified | 829 | 263 | 186 | 466 | 1,744 |
| Admin / Customer Service | 519 | 609 | 107 | 29 | 1,264 |
| IT / Data / Software | 494 | 35 | 84 | 229 | 842 |
| Professional Finance / Accountancy | 211 | 84 | 81 | 159 | 535 |
| Marketing / Digital / Creative | 188 | 80 | 134 | 128 | 530 |
| Engineering / Technical | 188 | 39 | 80 | 121 | 428 |
| Healthcare / Clinical | 286 | 25 | 39 | 63 | 413 |
| HR / Recruitment | 114 | 116 | 70 | 35 | 335 |
| Legal / Conveyancing | 136 | 74 | 34 | 88 | 332 |
| Management / Team Leadership | 72 | 51 | 46 | 62 | 231 |
| Care / Support Work | 114 | 60 | 15 | 36 | 225 |
| Retail / Store | 105 | 74 | 20 | 14 | 213 |
| Operations / General Management | 112 | 7 | 13 | 28 | 160 |
| Insurance / Claims | 92 | 9 | 20 | 29 | 150 |
| Construction / Trades / Property | 27 | 28 | 27 | 42 | 124 |
| Market Research / Field Interviewing | 106 | 14 | 0 | 0 | 120 |
| Financial Advice / Mortgages | 24 | 7 | 19 | 47 | 97 |
| Procurement / Buying / Supply Chain | 35 | 12 | 11 | 13 | 71 |
| Property / Housing / Planning | 14 | 9 | 17 | 25 | 65 |
| Compliance / Risk / Quality | 24 | 2 | 5 | 18 | 49 |
| Driving / Warehouse / Logistics | 15 | 21 | 7 | 5 | 48 |
| Charity / Fundraising / Community | 33 | 2 | 4 | 1 | 40 |
| Education / Teaching | 13 | 12 | 4 | 6 | 35 |
| Hospitality / Catering | 17 | 8 | 5 | 3 | 33 |
| Security / Emergency Services | 16 | 2 | 0 | 10 | 28 |
| Manufacturing / Production | 9 | 8 | 3 | 5 | 25 |
| Employment Support / Careers | 8 | 15 | 0 | 0 | 23 |
| Science / Laboratory | 4 | 1 | 8 | 7 | 20 |
| Cleaning / Domestic / Facilities | 9 | 4 | 1 | 0 | 14 |
| Agriculture / Environment | 2 | 3 | 4 | 3 | 12 |
| **TOTAL** | **4,433** | **2,035** | **1,343** | **2,189** | **10,000** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Sales / Business Development | 1,794 | 0 | 1,794 | 87 | 10 | 63 | 45 | 125 | London (277); Greater Manchester - Manchester & Salford (96); Hertfordshire (67); Hampshire (57); West Midlands - Birmingham & Solihull (55) |
| Admin / Customer Service | 1,264 | 532 | 732 | 78 | 8.0 | 52 | 34 | 191 | London (216); Surrey (53); Hampshire (49); North East - Tyneside, Wearside & Northumberland (46); Kent (38) |
| IT / Data / Software | 842 | 0 | 842 | 68 | 5.0 | 38 | 20 | 33 | London (256); Greater Manchester - Manchester & Salford (47); Hertfordshire (27); West Midlands - Birmingham & Solihull (26); Hampshire (25) |
| Professional Finance / Accountancy | 535 | 88 | 447 | 70 | 4.5 | 35 | 11 | 59 | London (123); Bristol & Bath (16); Yorkshire - West (16); Greater Manchester - Manchester & Salford (16); Yorkshire - North (15) |
| Marketing / Digital / Creative | 530 | 0 | 530 | 64 | 4.0 | 27 | 11 | 42 | London (132); Greater Manchester - Manchester & Salford (33); Yorkshire - West (21); Buckinghamshire (15); Hertfordshire (15) |
| Engineering / Technical | 428 | 0 | 428 | 62 | 3.5 | 25 | 8 | 32 | London (107); Greater Manchester - Manchester & Salford (26); West Midlands - Birmingham & Solihull (18); Berkshire (17); Surrey (13) |
| Healthcare / Clinical | 413 | 0 | 413 | 66 | 2.0 | 20 | 8 | 60 | London (99); Surrey (20); Hampshire (18); Sussex (12); Berkshire (12) |
| HR / Recruitment | 335 | 76 | 259 | 58 | 3.0 | 23 | 5 | 41 | London (53); Bristol & Bath (18); Yorkshire - West (15); Hampshire (14); Greater Manchester - Manchester & Salford (13) |
| Legal / Conveyancing | 332 | 0 | 332 | 58 | 3.0 | 20 | 7 | 9 | London (84); Greater Manchester - Manchester & Salford (16); Bristol & Bath (13); West Midlands - Birmingham & Solihull (13); Sussex (12) |
| Management / Team Leadership | 231 | 0 | 231 | 62 | 3.0 | 13 | 2 | 17 | London (27); Sussex (10); Kent (8); Bristol & Bath (8); Berkshire (7) |
| Care / Support Work | 225 | 87 | 138 | 56 | 2.0 | 11 | 4 | 30 | London (24); Hampshire (20); Berkshire (13); Surrey (10); Yorkshire - West (9) |
| Retail / Store | 213 | 0 | 213 | 58 | 2.0 | 12 | 1 | 26 | London (24); Sussex (9); Yorkshire - North (9); Kent (8); Oxfordshire (8) |
| Operations / General Management | 160 | 0 | 160 | 44 | 2.0 | 7 | 1 | 17 | London (41); Surrey (7); Bristol & Bath (7); Hampshire (6); Kent (6) |
| Insurance / Claims | 150 | 0 | 150 | 37 | 2 | 7 | 1 | 12 | London (47); Essex (8); Yorkshire - West (7); Norfolk (6); Kent (6) |
| Construction / Trades / Property | 124 | 0 | 124 | 42 | 2.0 | 2 | 1 | 11 | London (25); Essex (6); Bristol & Bath (4); Hampshire (4); Gloucestershire (4) |
| Market Research / Field Interviewing | 120 | 0 | 120 | 32 | 2.0 | 6 | 0 | 37 | London (9); Scotland Central - Tayside (8); Berkshire (6); Wiltshire (6); Scotland West - Ayrshire (5) |
| Financial Advice / Mortgages | 97 | 0 | 97 | 39 | 2 | 4 | 1 | 3 | London (12); Surrey (8); Kent (6); Bristol & Bath (6); Leicestershire (4) |
| Procurement / Buying / Supply Chain | 71 | 0 | 71 | 27 | 1 | 1 | 1 | 13 | London (16); Essex (4); Greater Manchester - South (4); Sussex (3); Devon (3) |
| Property / Housing / Planning | 65 | 0 | 65 | 30 | 1.0 | 1 | 0 | 12 | London (9); West Midlands - Coventry & Warwickshire (4); North East - Tyneside, Wearside & Northumberland (3); Surrey (3); Kent (3) |
| Compliance / Risk / Quality | 49 | 0 | 49 | 23 | 1 | 1 | 1 | 4 | London (16); Bristol & Bath (4); Hertfordshire (2); Cambridgeshire (2); Scotland Central - Edinburgh & Lothians (2) |
| Driving / Warehouse / Logistics | 48 | 1 | 47 | 26 | 1.0 | 1 | 0 | 5 | London (7); Greater Manchester - Manchester & Salford (3); Leicestershire (2); Staffordshire (2); East Midlands (2) |
| Charity / Fundraising / Community | 40 | 0 | 40 | 17 | 1 | 1 | 1 | 5 | London (10); Buckinghamshire (4); West Midlands - Birmingham & Solihull (3); Bristol & Bath (2); Surrey (2) |
| Education / Teaching | 35 | 0 | 35 | 16 | 1.0 | 1 | 1 | 2 | London (10); Yorkshire - West (3); Surrey (3); Midlothian (2); Buckinghamshire (2) |
| Hospitality / Catering | 33 | 0 | 33 | 15 | 1 | 1 | 0 | 3 | London (9); Sussex (3); Oxfordshire (2); Scotland Central - Edinburgh & Lothians (2); Devon (2) |
| Security / Emergency Services | 28 | 0 | 28 | 16 | 1.0 | 1 | 1 | 1 | London (10); Hampshire (2); Bedfordshire (2); Nottinghamshire (1); North East - Tyneside, Wearside & Northumberland (1) |
| Manufacturing / Production | 25 | 0 | 25 | 16 | 1.0 | 0 | 0 | 2 | London (4); Wiltshire (2); Gloucestershire (2); Yorkshire - West (2); Sussex (2) |
| Employment Support / Careers | 23 | 0 | 23 | 14 | 1.0 | 0 | 0 | 3 | Yorkshire - North (3); London (3); Wales - Mid (2); Bristol & Bath (2); Surrey (1) |
| Science / Laboratory | 20 | 0 | 20 | 10 | 1.0 | 1 | 0 | 4 | London (5); Gloucestershire (2); Nottinghamshire (2); Worcestershire (1); Derbyshire (1) |
| Cleaning / Domestic / Facilities | 14 | 0 | 14 | 9 | 1 | 0 | 0 | 3 | Essex (2); Yorkshire - South (2); London (1); Bristol & Bath (1); Cambridgeshire (1) |
| Agriculture / Environment | 12 | 0 | 12 | 7 | 2 | 0 | 0 | 0 | London (3); Cheshire - Warrington & Halton (2); Kent (2); Sussex (2); Devon (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 6,253 |
| still_unclassified | 1,744 |
| title_rule_pass2 | 1,104 |
| existing_register:admin_service | 323 |
| existing_register:customer_service_contact_centre | 209 |
| description_majority | 115 |
| existing_register:finance_accounts | 88 |
| existing_register:support_worker | 87 |
| existing_register:hr_recruitment | 76 |
| existing_register:warehouse_logistics | 1 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 19 | Bid Manager |
| 18 | Door to Door Canvasser |
| 12 | Account Handler |
| 9 | Sub Agent |
| 9 | Customer Representative Field Based |
| 8 | Aftersales Manager |
| 8 | Account Director |
| 7 | Client Relationship Manager |
| 7 | Customer Relations Manager |
| 7 | Paid Media Manager |
| 7 | Housing Estates Officer |
| 6 | Planner |
| 6 | Field Collections Agent |
| 6 | Technical Manager |
| 6 | Head of IT |
| 5 | Technical Lead (Full Stack Java) |
| 4 | Tenancy Sustainment Officer |
| 4 | Partnerships Manager |
| 4 | Technical Director |
| 4 | Videographer |
| 4 | Autocentre Manager |
| 4 | Remote Online Paid Research Panelist (Part-Time) - Data Entry Clerk Welcome |
| 4 | Data Architect |
| 4 | Accessibility Specialist |
| 3 | Installer Development Representative |
| 3 | Hire Desk Manager |
| 3 | Senior Authorised Person |
| 3 | Senior Planner |
| 3 | Insolvency Manager |
| 3 | Property Valuer |
| 3 | Pricing Manager |
| 3 | CRM Executive |
| 3 | Brand Ambassador |
| 3 | Canvasser |
| 3 | Contractual Advisor |
| 3 | Technical Author |
| 3 | Croupier |
| 3 | Development Technologist |
| 3 | Regional Customer Relationship Manager |
| 3 | Enforcement Agent |
| 3 | People Business Partner |
| 3 | Butchery Manager |
| 3 | IT Systems Manager |
| 3 | Data Governance Analyst |
| 3 | Land Agent |
| 3 | Senior Bid Manager |
| 3 | Head of Customer Care |
| 3 | Community Engagement Manager |
| 3 | IT Manager |
| 3 | IT Apprentice |
| 3 | Senior User Researcher |
| 3 | F5 SME |
| 3 | Brand Ambassadors In-Store Food & Drink Sampling |
| 2 | Design Director |
| 2 | Corporate Senior Associate |
| 2 | Regional Quality/Safety Lead |
| 2 | Tribunal Advocate |
| 2 | Architectural Technologist |
| 2 | Property Officer |
| 2 | Vehicle Recovery Lead |
| 2 | Cost Controller |
| 2 | Pensions Lead |
| 2 | Assistant Team Manager |
| 2 | Client Portfolio Manager |
| 2 | Site Services Manager |
| 2 | Case Manager |
| 2 | CRM Manager |
| 2 | Stock Assistant |
| 2 | Change Manager |
| 2 | Head of People |
| 2 | Computer Science Researcher (CompSci Researcher) |
| 2 | Associate Director of Commercial Partnerships |
| 2 | Senior Cost Consultant |
| 2 | Smart Metering Planner |
| 2 | Senior Customer Relations Executive |

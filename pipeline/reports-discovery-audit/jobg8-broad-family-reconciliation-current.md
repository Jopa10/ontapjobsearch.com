# JobG8 register-first broad-family reconciliation

Jobs reconciled: **10,000**
Jobs assigned first from an existing selected Ontap register: **858**
Original title-rule Other / Unclassified: **2,920**
Jobs resolved by description-majority pass: **114**
Remaining Other / Unclassified after register-first + title + description passes: **1,702**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Sales / Business Development | 1,828 | 18.3% |
| Other / Unclassified | 1,702 | 17.0% |
| Admin / Customer Service | 1,313 | 13.1% |
| IT / Data / Software | 850 | 8.5% |
| Professional Finance / Accountancy | 543 | 5.4% |
| Marketing / Digital / Creative | 515 | 5.1% |
| Engineering / Technical | 420 | 4.2% |
| Healthcare / Clinical | 413 | 4.1% |
| Legal / Conveyancing | 336 | 3.4% |
| HR / Recruitment | 325 | 3.2% |
| Care / Support Work | 219 | 2.2% |
| Management / Team Leadership | 218 | 2.2% |
| Retail / Store | 207 | 2.1% |
| Operations / General Management | 155 | 1.6% |
| Insurance / Claims | 146 | 1.5% |
| Market Research / Field Interviewing | 129 | 1.3% |
| Construction / Trades / Property | 128 | 1.3% |
| Financial Advice / Mortgages | 104 | 1.0% |
| Procurement / Buying / Supply Chain | 71 | 0.7% |
| Property / Housing / Planning | 64 | 0.6% |
| Compliance / Risk / Quality | 49 | 0.5% |
| Driving / Warehouse / Logistics | 48 | 0.5% |
| Charity / Fundraising / Community | 37 | 0.4% |
| Education / Teaching | 34 | 0.3% |
| Hospitality / Catering | 30 | 0.3% |
| Security / Emergency Services | 27 | 0.3% |
| Manufacturing / Production | 23 | 0.2% |
| Employment Support / Careers | 22 | 0.2% |
| Science / Laboratory | 20 | 0.2% |
| Cleaning / Domestic / Facilities | 12 | 0.1% |
| Agriculture / Environment | 12 | 0.1% |
| **TOTAL** | **10,000** | **100.0%** |

## Refined family totals by salary band

Salary uses the midpoint of the available structured minimum/maximum after annualising hourly, daily, weekly or monthly amounts. Five-figure values are treated as annual even when the source period is inconsistent. The first column combines genuinely sub-£20k jobs with missing or unusable salary so every family reconciles exactly to its total.

| Broad family | Below £20k / unknown | £20k–<£35k | £35k–£45k | Over £45k | Total |
|---|---:|---:|---:|---:|---:|
| Sales / Business Development | 724 | 342 | 279 | 483 | 1,828 |
| Other / Unclassified | 814 | 245 | 182 | 461 | 1,702 |
| Admin / Customer Service | 598 | 580 | 107 | 28 | 1,313 |
| IT / Data / Software | 503 | 36 | 83 | 228 | 850 |
| Professional Finance / Accountancy | 218 | 85 | 86 | 154 | 543 |
| Marketing / Digital / Creative | 183 | 80 | 128 | 124 | 515 |
| Engineering / Technical | 183 | 39 | 79 | 119 | 420 |
| Healthcare / Clinical | 278 | 26 | 39 | 70 | 413 |
| Legal / Conveyancing | 138 | 78 | 33 | 87 | 336 |
| HR / Recruitment | 109 | 115 | 65 | 36 | 325 |
| Care / Support Work | 117 | 54 | 15 | 33 | 219 |
| Management / Team Leadership | 68 | 48 | 43 | 59 | 218 |
| Retail / Store | 101 | 73 | 20 | 13 | 207 |
| Operations / General Management | 108 | 6 | 11 | 30 | 155 |
| Insurance / Claims | 89 | 8 | 21 | 28 | 146 |
| Market Research / Field Interviewing | 108 | 21 | 0 | 0 | 129 |
| Construction / Trades / Property | 29 | 29 | 28 | 42 | 128 |
| Financial Advice / Mortgages | 26 | 7 | 23 | 48 | 104 |
| Procurement / Buying / Supply Chain | 35 | 12 | 11 | 13 | 71 |
| Property / Housing / Planning | 12 | 11 | 16 | 25 | 64 |
| Compliance / Risk / Quality | 23 | 2 | 5 | 19 | 49 |
| Driving / Warehouse / Logistics | 15 | 22 | 6 | 5 | 48 |
| Charity / Fundraising / Community | 29 | 3 | 4 | 1 | 37 |
| Education / Teaching | 14 | 12 | 3 | 5 | 34 |
| Hospitality / Catering | 15 | 7 | 5 | 3 | 30 |
| Security / Emergency Services | 17 | 2 | 0 | 8 | 27 |
| Manufacturing / Production | 7 | 8 | 3 | 5 | 23 |
| Employment Support / Careers | 8 | 14 | 0 | 0 | 22 |
| Science / Laboratory | 1 | 2 | 10 | 7 | 20 |
| Cleaning / Domestic / Facilities | 8 | 4 | 0 | 0 | 12 |
| Agriculture / Environment | 2 | 3 | 4 | 3 | 12 |
| **TOTAL** | **4,580** | **1,974** | **1,309** | **2,137** | **10,000** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Sales / Business Development | 1,828 | 0 | 1,828 | 87 | 10 | 65 | 47 | 129 | London (279); North East - Tyneside, Wearside & Northumberland (103); Greater Manchester - Manchester & Salford (88); Hertfordshire (62); Yorkshire - West (53) |
| Admin / Customer Service | 1,313 | 604 | 709 | 76 | 8.0 | 51 | 31 | 195 | London (220); North East - Tyneside, Wearside & Northumberland (93); Surrey (53); Hampshire (49); Kent (37) |
| IT / Data / Software | 850 | 0 | 850 | 68 | 5.0 | 36 | 20 | 38 | London (257); Greater Manchester - Manchester & Salford (47); Hampshire (30); Hertfordshire (27); West Midlands - Birmingham & Solihull (26) |
| Professional Finance / Accountancy | 543 | 89 | 454 | 68 | 4.5 | 34 | 11 | 65 | London (130); Bristol & Bath (16); Yorkshire - West (16); Greater Manchester - Manchester & Salford (14); Yorkshire - North (14) |
| Marketing / Digital / Creative | 515 | 0 | 515 | 61 | 4 | 25 | 12 | 40 | London (131); Greater Manchester - Manchester & Salford (31); Yorkshire - West (21); Berkshire (16); Buckinghamshire (14) |
| Engineering / Technical | 420 | 0 | 420 | 59 | 4 | 24 | 8 | 31 | London (104); Greater Manchester - Manchester & Salford (27); Berkshire (17); West Midlands - Birmingham & Solihull (17); Surrey (12) |
| Healthcare / Clinical | 413 | 0 | 413 | 66 | 2.0 | 20 | 8 | 62 | London (99); Surrey (21); Hampshire (18); Sussex (13); Berkshire (13) |
| Legal / Conveyancing | 336 | 0 | 336 | 58 | 3.0 | 21 | 8 | 8 | London (87); Greater Manchester - Manchester & Salford (15); West Midlands - Birmingham & Solihull (14); Bristol & Bath (13); Sussex (12) |
| HR / Recruitment | 325 | 75 | 250 | 58 | 3.0 | 20 | 5 | 44 | London (53); Bristol & Bath (21); Hampshire (13); Yorkshire - West (13); Greater Manchester - Manchester & Salford (13) |
| Care / Support Work | 219 | 89 | 130 | 55 | 2 | 11 | 4 | 30 | London (25); Hampshire (17); Berkshire (12); Surrey (11); Yorkshire - West (8) |
| Management / Team Leadership | 218 | 0 | 218 | 59 | 3 | 14 | 1 | 14 | London (26); Kent (8); Sussex (8); Bristol & Bath (7); West Midlands - Coventry & Warwickshire (6) |
| Retail / Store | 207 | 0 | 207 | 58 | 2.0 | 9 | 1 | 28 | London (22); Sussex (9); Kent (8); Oxfordshire (8); Yorkshire - North (8) |
| Operations / General Management | 155 | 0 | 155 | 42 | 2.0 | 7 | 1 | 17 | London (40); Surrey (7); Bristol & Bath (7); Hampshire (6); West Midlands - Birmingham & Solihull (5) |
| Insurance / Claims | 146 | 0 | 146 | 37 | 2 | 7 | 1 | 12 | London (46); Essex (8); Kent (6); Yorkshire - West (6); Norfolk (5) |
| Market Research / Field Interviewing | 129 | 0 | 129 | 33 | 2 | 7 | 1 | 38 | London (10); Scotland Central - Tayside (8); Berkshire (6); Wiltshire (6); West Midlands - Birmingham & Solihull (6) |
| Construction / Trades / Property | 128 | 0 | 128 | 45 | 2 | 2 | 1 | 11 | London (28); Cambridgeshire (5); Bristol & Bath (4); Gloucestershire (4); Essex (4) |
| Financial Advice / Mortgages | 104 | 0 | 104 | 40 | 2.0 | 6 | 1 | 3 | London (13); Surrey (8); Kent (6); Bristol & Bath (6); Wiltshire (5) |
| Procurement / Buying / Supply Chain | 71 | 0 | 71 | 27 | 1 | 1 | 1 | 14 | London (16); Greater Manchester - South (4); Sussex (3); Devon (3); Greater Manchester - Manchester & Salford (3) |
| Property / Housing / Planning | 64 | 0 | 64 | 27 | 1 | 1 | 0 | 12 | London (9); West Midlands - Coventry & Warwickshire (4); North East - Tyneside, Wearside & Northumberland (3); Surrey (3); Kent (3) |
| Compliance / Risk / Quality | 49 | 0 | 49 | 23 | 1 | 1 | 1 | 4 | London (15); Bristol & Bath (4); Hertfordshire (2); Cambridgeshire (2); Scotland Central - Edinburgh & Lothians (2) |
| Driving / Warehouse / Logistics | 48 | 1 | 47 | 26 | 1.0 | 1 | 0 | 5 | London (7); Greater Manchester - Manchester & Salford (3); Leicestershire (2); Staffordshire (2); East Midlands (2) |
| Charity / Fundraising / Community | 37 | 0 | 37 | 15 | 1 | 1 | 1 | 4 | London (10); Buckinghamshire (4); West Midlands - Birmingham & Solihull (3); Bristol & Bath (2); Surrey (2) |
| Education / Teaching | 34 | 0 | 34 | 16 | 1.5 | 1 | 0 | 2 | London (9); Surrey (3); Yorkshire - West (2); Midlothian (2); Buckinghamshire (2) |
| Hospitality / Catering | 30 | 0 | 30 | 14 | 1.0 | 1 | 0 | 3 | London (7); Sussex (3); Lincolnshire (3); Scotland Central - Edinburgh & Lothians (2); Devon (2) |
| Security / Emergency Services | 27 | 0 | 27 | 15 | 1 | 1 | 1 | 1 | London (10); Hampshire (2); Bedfordshire (2); Nottinghamshire (1); North East - Tyneside, Wearside & Northumberland (1) |
| Manufacturing / Production | 23 | 0 | 23 | 15 | 1 | 0 | 0 | 2 | London (4); Wiltshire (2); Gloucestershire (2); Yorkshire - West (2); Worcestershire (1) |
| Employment Support / Careers | 22 | 0 | 22 | 13 | 1 | 0 | 0 | 3 | Yorkshire - North (3); London (3); Wales - Mid (2); Bristol & Bath (2); Surrey (1) |
| Science / Laboratory | 20 | 0 | 20 | 11 | 1 | 1 | 0 | 2 | London (5); Worcestershire (2); Gloucestershire (2); Nottinghamshire (2); Derbyshire (1) |
| Cleaning / Domestic / Facilities | 12 | 0 | 12 | 8 | 1.0 | 0 | 0 | 3 | Essex (2); London (1); Cambridgeshire (1); Yorkshire - North (1); Yorkshire - South (1) |
| Agriculture / Environment | 12 | 0 | 12 | 7 | 2 | 0 | 0 | 0 | London (3); Cheshire - Warrington & Halton (2); Kent (2); Sussex (2); Devon (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 6,257 |
| still_unclassified | 1,702 |
| title_rule_pass2 | 1,069 |
| existing_register:admin_service | 312 |
| existing_register:customer_service_contact_centre | 292 |
| description_majority | 114 |
| existing_register:support_worker | 89 |
| existing_register:finance_accounts | 89 |
| existing_register:hr_recruitment | 75 |
| existing_register:warehouse_logistics | 1 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 19 | Bid Manager |
| 17 | Door to Door Canvasser |
| 11 | Account Handler |
| 9 | Sub Agent |
| 9 | Customer Representative Field Based |
| 8 | Brand Ambassadors In-Store Food & Drink Sampling |
| 7 | Aftersales Manager |
| 7 | Field Collections Agent |
| 7 | Technical Manager |
| 7 | Account Director |
| 7 | Paid Media Manager |
| 7 | Housing Estates Officer |
| 6 | Head of IT |
| 5 | Client Relationship Manager |
| 5 | Planner |
| 5 | Customer Relations Manager |
| 5 | Technical Lead (Full Stack Java) |
| 4 | Tenancy Sustainment Officer |
| 4 | Insolvency Manager |
| 4 | Partnerships Manager |
| 4 | Technical Director |
| 4 | Autocentre Manager |
| 4 | Remote Online Paid Research Panelist (Part-Time) - Data Entry Clerk Welcome |
| 4 | Data Architect |
| 4 | Accessibility Specialist |
| 3 | Installer Development Representative |
| 3 | Senior Authorised Person |
| 3 | Senior Planner |
| 3 | Property Valuer |
| 3 | Pricing Manager |
| 3 | CRM Executive |
| 3 | Brand Ambassador |
| 3 | Stock Assistant |
| 3 | Videographer |
| 3 | Canvasser |
| 3 | Contractual Advisor |
| 3 | Development Technologist |
| 3 | Regional Customer Relationship Manager |
| 3 | Enforcement Agent |
| 3 | People Business Partner |
| 3 | Butchery Manager |
| 3 | IT Systems Manager |
| 3 | Data Governance Analyst |
| 3 | Land Agent |
| 3 | Head of Customer Care |
| 3 | Freelance Interpreter |
| 3 | IT Manager |
| 3 | IT Apprentice |
| 3 | F5 SME |
| 2 | Hire Desk Manager |
| 2 | Design Director |
| 2 | Corporate Senior Associate |
| 2 | Regional Quality/Safety Lead |
| 2 | Tribunal Advocate |
| 2 | Architectural Technologist |
| 2 | Property Officer |
| 2 | Vehicle Recovery Lead |
| 2 | Administrative Officer |
| 2 | Cost Controller |
| 2 | Pensions Lead |
| 2 | Assistant Team Manager |
| 2 | Client Portfolio Manager |
| 2 | Site Services Manager |
| 2 | Case Manager |
| 2 | CRM Manager |
| 2 | Change Manager |
| 2 | Head of People |
| 2 | Computer Science Researcher (CompSci Researcher) |
| 2 | Associate Director of Commercial Partnerships |
| 2 | Senior Cost Consultant |
| 2 | Smart Metering Planner |
| 2 | Senior Customer Relations Executive |
| 2 | Packaging Technologist |
| 2 | Design Manager |
| 2 | Paid Emails - Work From Home |

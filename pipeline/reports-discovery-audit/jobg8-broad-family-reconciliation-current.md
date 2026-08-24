# JobG8 register-first broad-family reconciliation

Jobs reconciled: **10,000**
Jobs assigned first from an existing selected Ontap register: **1,052**
Original title-rule Other / Unclassified: **3,018**
Jobs resolved by description-majority pass: **157**
Remaining Other / Unclassified after register-first + title + description passes: **1,392**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Admin / Customer Service | 1,496 | 15.0% |
| Other / Unclassified | 1,392 | 13.9% |
| Professional Finance / Accountancy | 1,292 | 12.9% |
| Legal / Conveyancing | 873 | 8.7% |
| Sales / Business Development | 780 | 7.8% |
| Healthcare / Clinical | 578 | 5.8% |
| HR / Recruitment | 497 | 5.0% |
| Management / Team Leadership | 357 | 3.6% |
| IT / Data / Software | 355 | 3.5% |
| Engineering / Technical | 341 | 3.4% |
| Care / Support Work | 327 | 3.3% |
| Financial Advice / Mortgages | 236 | 2.4% |
| Marketing / Digital / Creative | 231 | 2.3% |
| Retail / Store | 212 | 2.1% |
| Market Research / Field Interviewing | 159 | 1.6% |
| Insurance / Claims | 152 | 1.5% |
| Construction / Trades / Property | 143 | 1.4% |
| Operations / General Management | 117 | 1.2% |
| Property / Housing / Planning | 78 | 0.8% |
| Education / Teaching | 62 | 0.6% |
| Procurement / Buying / Supply Chain | 62 | 0.6% |
| Compliance / Risk / Quality | 57 | 0.6% |
| Driving / Warehouse / Logistics | 43 | 0.4% |
| Charity / Fundraising / Community | 41 | 0.4% |
| Employment Support / Careers | 36 | 0.4% |
| Hospitality / Catering | 18 | 0.2% |
| Science / Laboratory | 15 | 0.1% |
| Manufacturing / Production | 15 | 0.1% |
| Security / Emergency Services | 15 | 0.1% |
| Cleaning / Domestic / Facilities | 10 | 0.1% |
| Agriculture / Environment | 10 | 0.1% |
| **TOTAL** | **10,000** | **100.0%** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Admin / Customer Service | 1,496 | 595 | 901 | 86 | 8.5 | 53 | 40 | 206 | London (236); Surrey (77); Hampshire (53); Kent (41); Oxfordshire (38) |
| Professional Finance / Accountancy | 1,292 | 221 | 1,071 | 80 | 10.5 | 55 | 43 | 58 | London (188); Bristol & Bath (50); Yorkshire - West (43); Sussex (41); Kent (41) |
| Legal / Conveyancing | 873 | 0 | 873 | 66 | 5.5 | 34 | 21 | 12 | London (165); Essex (87); Suffolk (76); Norfolk (55); Yorkshire - West (31) |
| Sales / Business Development | 780 | 0 | 780 | 78 | 6.0 | 48 | 26 | 46 | London (120); Hampshire (33); Greater Manchester - Manchester & Salford (26); Hertfordshire (23); Yorkshire - West (23) |
| Healthcare / Clinical | 578 | 0 | 578 | 80 | 3.0 | 29 | 13 | 55 | London (92); Hampshire (31); Sussex (30); Surrey (26); Berkshire (21) |
| HR / Recruitment | 497 | 124 | 373 | 64 | 4.0 | 29 | 16 | 43 | London (76); Bristol & Bath (27); Hampshire (23); Yorkshire - West (19); Hertfordshire (15) |
| Management / Team Leadership | 357 | 0 | 357 | 77 | 3 | 27 | 7 | 25 | London (26); Oxfordshire (20); Kent (15); Sussex (12); Hampshire (10) |
| IT / Data / Software | 355 | 0 | 355 | 54 | 3.0 | 20 | 7 | 28 | London (75); Hampshire (39); Bristol & Bath (19); Greater Manchester - Manchester & Salford (14); Gloucestershire (12) |
| Engineering / Technical | 341 | 0 | 341 | 60 | 3.5 | 25 | 9 | 29 | London (43); Northamptonshire (21); Bristol & Bath (14); Hampshire (12); Gloucestershire (11) |
| Care / Support Work | 327 | 109 | 218 | 66 | 2.5 | 20 | 4 | 30 | London (34); Hampshire (29); Sussex (15); Surrey (13); Greater Manchester - Manchester & Salford (9) |
| Financial Advice / Mortgages | 236 | 0 | 236 | 54 | 2.5 | 18 | 5 | 5 | London (22); Bristol & Bath (14); Yorkshire - West (13); Essex (12); Hampshire (11) |
| Marketing / Digital / Creative | 231 | 0 | 231 | 54 | 2.0 | 10 | 2 | 18 | London (70); Surrey (10); Greater Manchester - Manchester & Salford (9); Kent (7); Yorkshire - North (7) |
| Retail / Store | 212 | 0 | 212 | 66 | 2.0 | 13 | 3 | 21 | London (15); Greater Manchester - Manchester & Salford (11); Yorkshire - North (10); Bristol & Bath (7); Wiltshire (7) |
| Market Research / Field Interviewing | 159 | 0 | 159 | 39 | 1 | 8 | 2 | 51 | Wiltshire (12); London (11); Worcestershire (9); North Scotland (6); Northamptonshire (5) |
| Insurance / Claims | 152 | 0 | 152 | 33 | 2 | 6 | 1 | 12 | London (50); Yorkshire - West (9); Merseyside - Liverpool (8); Essex (7); Norfolk (5) |
| Construction / Trades / Property | 143 | 0 | 143 | 42 | 2.0 | 6 | 1 | 10 | London (27); Greater Manchester - Manchester & Salford (9); Cambridgeshire (6); Essex (6); Devon (5) |
| Operations / General Management | 117 | 0 | 117 | 40 | 1.0 | 6 | 1 | 11 | London (23); Oxfordshire (9); Hampshire (7); Essex (6); Devon (6) |
| Property / Housing / Planning | 78 | 0 | 78 | 35 | 1 | 2 | 1 | 9 | London (12); Sussex (5); West Midlands - Coventry & Warwickshire (4); Hertfordshire (4); Cumbria - North (3) |
| Education / Teaching | 62 | 0 | 62 | 24 | 1.0 | 3 | 1 | 8 | London (12); Cumbria - South (6); Sussex (5); Lancashire - North (4); Surrey (4) |
| Procurement / Buying / Supply Chain | 62 | 0 | 62 | 28 | 1.0 | 2 | 0 | 11 | London (8); Essex (5); Surrey (3); Yorkshire - West (2); Buckinghamshire (2) |
| Compliance / Risk / Quality | 57 | 0 | 57 | 23 | 1 | 1 | 1 | 4 | London (18); Wiltshire (3); Bristol & Bath (3); West Midlands - Birmingham & Solihull (3); Scotland Central - Edinburgh & Lothians (3) |
| Driving / Warehouse / Logistics | 43 | 3 | 40 | 27 | 1 | 1 | 0 | 4 | London (5); Kent (2); West Midlands - Coventry & Warwickshire (2); West Midlands - Birmingham & Solihull (2); Berkshire (2) |
| Charity / Fundraising / Community | 41 | 0 | 41 | 17 | 1 | 1 | 1 | 3 | London (14); Buckinghamshire (4); Surrey (3); Yorkshire - West (2); Hampshire (2) |
| Employment Support / Careers | 36 | 0 | 36 | 16 | 1.0 | 1 | 1 | 2 | London (13); Wales - Mid (2); Hampshire (2); Cornwall (2); Yorkshire - North (2) |
| Hospitality / Catering | 18 | 0 | 18 | 8 | 1.5 | 2 | 0 | 0 | Gloucestershire (5); London (5); Lincolnshire (2); Oxfordshire (2); Essex (1) |
| Science / Laboratory | 15 | 0 | 15 | 8 | 1.0 | 0 | 0 | 3 | Gloucestershire (3); London (2); Oxfordshire (2); Worcestershire (1); Kent (1) |
| Manufacturing / Production | 15 | 0 | 15 | 12 | 1.0 | 0 | 0 | 1 | Worcestershire (2); Wiltshire (2); Norfolk (1); Hampshire (1); Suffolk (1) |
| Security / Emergency Services | 15 | 0 | 15 | 7 | 1 | 1 | 0 | 1 | London (5); Hampshire (3); Bristol & Bath (2); Greater Manchester - South (1); Cambridgeshire (1) |
| Cleaning / Domestic / Facilities | 10 | 0 | 10 | 7 | 1 | 0 | 0 | 1 | Northamptonshire (2); Hertfordshire (2); Dorset (1); London (1); Essex (1) |
| Agriculture / Environment | 10 | 0 | 10 | 5 | 2 | 0 | 0 | 1 | Cheshire - Warrington & Halton (3); London (2); Kent (2); Oxfordshire (1); Devon (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 5,992 |
| title_rule_pass2 | 1,407 |
| still_unclassified | 1,392 |
| existing_register:admin_service | 428 |
| existing_register:finance_accounts | 221 |
| existing_register:customer_service_contact_centre | 167 |
| description_majority | 157 |
| existing_register:hr_recruitment | 124 |
| existing_register:support_worker | 109 |
| existing_register:warehouse_logistics | 3 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 9 | Sub Agent |
| 6 | Functional Specialist |
| 6 | Social Impact & Community Enterprise Manager (Food Insecurity) - 6m FTC |
| 6 | Technical Lead |
| 6 | Theatre Scrub Practitioner - RN/ODP |
| 5 | Implementation Consultant |
| 5 | Tenancy Sustainment Officer |
| 5 | People Business Partner |
| 5 | Bid Manager |
| 5 | Contracts Manager |
| 5 | General Foreman |
| 4 | Property Valuer |
| 4 | Transaction Manager |
| 4 | Insolvency Manager |
| 4 | Productivity Manager |
| 4 | Technical Manager |
| 4 | Pensions Lead |
| 3 | Psychology Graduate |
| 3 | Senior Planner |
| 3 | Executive Search Consultant |
| 3 | Customer Representative Field Based |
| 3 | Senior Authorised Person |
| 3 | Technical Director |
| 3 | Media Measurement Lead |
| 3 | Property Officer |
| 3 | Installer Development Representative |
| 3 | Project Director |
| 3 | IT Manager |
| 3 | Aftersales Manager |
| 3 | Wealth Planner |
| 3 | Planner |
| 3 | Cost Manager |
| 3 | Case Manager |
| 3 | Research Officer |
| 3 | Remote Online Paid Research Panelist (Part-Time) - Data Entry Clerk Welcome |
| 3 | Personal Lines Account Handler |
| 3 | Contractual Advisor |
| 3 | Development Executive |
| 2 | Commercial Director |
| 2 | Treasurer |
| 2 | Principal Commercial Officer |
| 2 | Business Advisory |
| 2 | NCR Facilitator |
| 2 | Protection Advisor |
| 2 | Senior Quality Practitioner |
| 2 | Debt Advice Caseworker |
| 2 | Vulnerability Researcher |
| 2 | Senior Reward Analyst |
| 2 | SEMH Mentor |
| 2 | Placement & Brokerage Officer |
| 2 | Mammographer |
| 2 | Marine Sub Agent |
| 2 | Senior Analyst |
| 2 | Hire Desk Manager |
| 2 | Design Director |
| 2 | M&E Commercial Director |
| 2 | Corporate Senior Associate |
| 2 | Regional Quality/Safety Lead |
| 2 | Concession Manager |
| 2 | Senior Land Acquisition Manager |
| 2 | Housing Options Officer (temp: North London) |
| 2 | Tribunal Advocate |
| 2 | Associate Associate Director - Town Planning |
| 2 | Architectural Technologist |
| 2 | Senior Cost Consultant |
| 2 | Aspiring Child Counsellor |
| 2 | Health & Social Care Assessor |
| 2 | Head of Reward |
| 2 | Commercial Business Partner |
| 2 | Private Client Director |
| 2 | Chief Financial Officer |
| 2 | Telehandler |
| 2 | Stock Condition Manager |
| 2 | HSE Advisor |
| 2 | Dementia Adviser |

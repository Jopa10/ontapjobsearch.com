# JobG8 register-first broad-family reconciliation

Jobs reconciled: **5,354**
Jobs assigned first from an existing selected Ontap register: **466**
Original title-rule Other / Unclassified: **1,679**
Jobs resolved by description-majority pass: **100**
Remaining Other / Unclassified after register-first + title + description passes: **826**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| IT / Data / Software | 1,302 | 24.3% |
| Other / Unclassified | 826 | 15.4% |
| Admin / Customer Service | 744 | 13.9% |
| Healthcare / Clinical | 479 | 8.9% |
| Engineering / Technical | 426 | 8.0% |
| Sales / Business Development | 201 | 3.8% |
| Professional Finance / Accountancy | 179 | 3.3% |
| Operations / General Management | 152 | 2.8% |
| Marketing / Digital / Creative | 151 | 2.8% |
| HR / Recruitment | 139 | 2.6% |
| Market Research / Field Interviewing | 117 | 2.2% |
| Care / Support Work | 110 | 2.1% |
| Legal / Conveyancing | 104 | 1.9% |
| Retail / Store | 54 | 1.0% |
| Management / Team Leadership | 47 | 0.9% |
| Procurement / Buying / Supply Chain | 42 | 0.8% |
| Construction / Trades / Property | 42 | 0.8% |
| Security / Emergency Services | 42 | 0.8% |
| Property / Housing / Planning | 39 | 0.7% |
| Compliance / Risk / Quality | 39 | 0.7% |
| Insurance / Claims | 25 | 0.5% |
| Driving / Warehouse / Logistics | 22 | 0.4% |
| Education / Teaching | 17 | 0.3% |
| Financial Advice / Mortgages | 11 | 0.2% |
| Agriculture / Environment | 10 | 0.2% |
| Hospitality / Catering | 10 | 0.2% |
| Manufacturing / Production | 9 | 0.2% |
| Science / Laboratory | 6 | 0.1% |
| Cleaning / Domestic / Facilities | 4 | 0.1% |
| Charity / Fundraising / Community | 3 | 0.1% |
| Employment Support / Careers | 2 | 0.0% |
| **TOTAL** | **5,354** | **100.0%** |

## Refined family totals by salary band

Salary uses the midpoint of the available structured minimum/maximum after annualising hourly, daily, weekly or monthly amounts. Five-figure values are treated as annual even when the source period is inconsistent. The first column combines genuinely sub-£20k jobs with missing or unusable salary so every family reconciles exactly to its total.

| Broad family | Below £20k / unknown | £20k–<£35k | £35k–£45k | Over £45k | Total |
|---|---:|---:|---:|---:|---:|
| IT / Data / Software | 841 | 44 | 98 | 319 | 1,302 |
| Other / Unclassified | 446 | 114 | 58 | 208 | 826 |
| Admin / Customer Service | 161 | 496 | 66 | 21 | 744 |
| Healthcare / Clinical | 399 | 27 | 25 | 28 | 479 |
| Engineering / Technical | 244 | 32 | 49 | 101 | 426 |
| Sales / Business Development | 74 | 59 | 36 | 32 | 201 |
| Professional Finance / Accountancy | 55 | 53 | 23 | 48 | 179 |
| Operations / General Management | 109 | 2 | 13 | 28 | 152 |
| Marketing / Digital / Creative | 78 | 21 | 23 | 29 | 151 |
| HR / Recruitment | 27 | 72 | 25 | 15 | 139 |
| Market Research / Field Interviewing | 73 | 44 | 0 | 0 | 117 |
| Care / Support Work | 65 | 35 | 4 | 6 | 110 |
| Legal / Conveyancing | 27 | 32 | 14 | 31 | 104 |
| Retail / Store | 28 | 16 | 4 | 6 | 54 |
| Management / Team Leadership | 23 | 9 | 4 | 11 | 47 |
| Procurement / Buying / Supply Chain | 14 | 9 | 9 | 10 | 42 |
| Construction / Trades / Property | 6 | 10 | 12 | 14 | 42 |
| Security / Emergency Services | 28 | 1 | 2 | 11 | 42 |
| Property / Housing / Planning | 7 | 7 | 9 | 16 | 39 |
| Compliance / Risk / Quality | 20 | 2 | 4 | 13 | 39 |
| Insurance / Claims | 18 | 4 | 0 | 3 | 25 |
| Driving / Warehouse / Logistics | 2 | 18 | 1 | 1 | 22 |
| Education / Teaching | 8 | 8 | 1 | 0 | 17 |
| Financial Advice / Mortgages | 1 | 4 | 3 | 3 | 11 |
| Agriculture / Environment | 0 | 3 | 4 | 3 | 10 |
| Hospitality / Catering | 3 | 4 | 2 | 1 | 10 |
| Manufacturing / Production | 1 | 3 | 1 | 4 | 9 |
| Science / Laboratory | 2 | 1 | 2 | 1 | 6 |
| Cleaning / Domestic / Facilities | 2 | 2 | 0 | 0 | 4 |
| Charity / Fundraising / Community | 2 | 1 | 0 | 0 | 3 |
| Employment Support / Careers | 1 | 1 | 0 | 0 | 2 |
| **TOTAL** | **2,765** | **1,134** | **492** | **963** | **5,354** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| IT / Data / Software | 1,302 | 0 | 1,302 | 72 | 8.0 | 45 | 30 | 52 | London (402); Greater Manchester - Manchester & Salford (71); Hampshire (62); West Midlands - Birmingham & Solihull (46); Kent (39) |
| Admin / Customer Service | 744 | 315 | 429 | 72 | 4.0 | 31 | 14 | 169 | London (141); Surrey (42); Leicestershire (23); Hampshire (23); Kent (22) |
| Healthcare / Clinical | 479 | 0 | 479 | 62 | 2.5 | 23 | 10 | 72 | London (104); Hampshire (33); Surrey (27); Sussex (20); Kent (15) |
| Engineering / Technical | 426 | 0 | 426 | 59 | 4 | 22 | 9 | 26 | London (122); Greater Manchester - Manchester & Salford (25); West Midlands - Birmingham & Solihull (19); Kent (17); Berkshire (16) |
| Sales / Business Development | 201 | 0 | 201 | 41 | 2 | 6 | 1 | 44 | London (58); Hampshire (8); Hertfordshire (7); Sussex (6); West Midlands - Birmingham & Solihull (6) |
| Professional Finance / Accountancy | 179 | 47 | 132 | 40 | 2.0 | 4 | 1 | 38 | London (54); Bristol & Bath (7); Greater Manchester - Manchester & Salford (7); Northern Ireland - East (5); Surrey (4) |
| Operations / General Management | 152 | 0 | 152 | 42 | 1.5 | 6 | 1 | 18 | London (46); Surrey (7); Hampshire (7); Yorkshire - West (6); Bristol & Bath (5) |
| Marketing / Digital / Creative | 151 | 0 | 151 | 33 | 2 | 4 | 1 | 26 | London (58); Greater Manchester - Manchester & Salford (8); Surrey (7); Berkshire (5); Hampshire (4) |
| HR / Recruitment | 139 | 46 | 93 | 35 | 2 | 4 | 1 | 31 | London (31); Hampshire (6); Kent (5); Nottinghamshire (5); West Midlands - Coventry & Warwickshire (4) |
| Market Research / Field Interviewing | 117 | 0 | 117 | 24 | 2.0 | 6 | 2 | 29 | Somerset (18); Wiltshire (10); Devon (6); Berkshire (6); Scotland Central - Tayside (5) |
| Care / Support Work | 110 | 57 | 53 | 26 | 1.0 | 7 | 3 | 14 | London (24); Hampshire (12); Surrey (11); Berkshire (6); Oxfordshire (6) |
| Legal / Conveyancing | 104 | 0 | 104 | 32 | 2.0 | 3 | 1 | 6 | London (37); Yorkshire - South (7); Sussex (7); Greater Manchester - Manchester & Salford (4); Yorkshire - West (3) |
| Retail / Store | 54 | 0 | 54 | 23 | 1 | 1 | 1 | 13 | London (10); Kent (4); Sussex (3); Greater Manchester - Manchester & Salford (3); Wales - Mid (2) |
| Management / Team Leadership | 47 | 0 | 47 | 25 | 1 | 1 | 1 | 10 | London (10); Oxfordshire (2); Devon (2); Sussex (2); Bedfordshire (1) |
| Procurement / Buying / Supply Chain | 42 | 0 | 42 | 20 | 1.0 | 1 | 1 | 9 | London (13); Surrey (2); Berkshire (1); Derbyshire (1); Yorkshire - East (1) |
| Construction / Trades / Property | 42 | 0 | 42 | 16 | 1.0 | 1 | 1 | 9 | London (15); Kent (2); Essex (2); Bedfordshire (2); Nottinghamshire (1) |
| Security / Emergency Services | 42 | 0 | 42 | 13 | 1 | 1 | 1 | 1 | London (19); Hampshire (4); North East - Tyneside, Wearside & Northumberland (3); Berkshire (3); Merseyside - Liverpool (3) |
| Property / Housing / Planning | 39 | 0 | 39 | 18 | 1.0 | 1 | 0 | 10 | London (7); Surrey (3); Sussex (2); North East - Tyneside, Wearside & Northumberland (2); West Midlands - Coventry & Warwickshire (2) |
| Compliance / Risk / Quality | 39 | 0 | 39 | 18 | 1.0 | 1 | 1 | 3 | London (14); Bristol & Bath (3); Cambridgeshire (2); Kent (2); Yorkshire - West (2) |
| Insurance / Claims | 25 | 0 | 25 | 5 | 2 | 1 | 1 | 8 | London (11); Norfolk (2); Kent (2); Staffordshire (1); Greater Manchester - Manchester & Salford (1) |
| Driving / Warehouse / Logistics | 22 | 1 | 21 | 10 | 1.0 | 0 | 0 | 5 | London (4); West Midlands - Coventry & Warwickshire (3); Leicestershire (2); Staffordshire (2); Berkshire (1) |
| Education / Teaching | 17 | 0 | 17 | 8 | 1.0 | 1 | 0 | 1 | London (6); Surrey (3); Buckinghamshire (2); Midlothian (1); Sussex (1) |
| Financial Advice / Mortgages | 11 | 0 | 11 | 8 | 1.0 | 0 | 0 | 0 | London (4); Bristol & Bath (1); Surrey (1); Merseyside - St Helens & Knowsley (1); Berkshire (1) |
| Agriculture / Environment | 10 | 0 | 10 | 6 | 1.5 | 0 | 0 | 0 | London (3); Kent (2); Sussex (2); Devon (1); Cheshire - Warrington & Halton (1) |
| Hospitality / Catering | 10 | 0 | 10 | 4 | 1.0 | 0 | 0 | 4 | London (3); Oxfordshire (1); Sussex (1); Devon (1) |
| Manufacturing / Production | 9 | 0 | 9 | 5 | 1 | 0 | 0 | 2 | Dorset (2); London (2); Worcestershire (1); Gloucestershire (1); Derbyshire (1) |
| Science / Laboratory | 6 | 0 | 6 | 3 | 1 | 0 | 0 | 3 | Worcestershire (1); Gloucestershire (1); West Midlands - Birmingham & Solihull (1) |
| Cleaning / Domestic / Facilities | 4 | 0 | 4 | 3 | 1 | 0 | 0 | 1 | London (1); Yorkshire - South (1); West Midlands - Birmingham & Solihull (1) |
| Charity / Fundraising / Community | 3 | 0 | 3 | 2 | 1.5 | 0 | 0 | 0 | London (2); Buckinghamshire (1) |
| Employment Support / Careers | 2 | 0 | 2 | 1 | 1 | 0 | 0 | 1 | Surrey (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 3,236 |
| still_unclassified | 826 |
| title_rule_pass2 | 726 |
| existing_register:admin_service | 233 |
| description_majority | 100 |
| existing_register:customer_service_contact_centre | 82 |
| existing_register:support_worker | 57 |
| existing_register:finance_accounts | 47 |
| existing_register:hr_recruitment | 46 |
| existing_register:warehouse_logistics | 1 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 10 | Head of IT |
| 5 | Social Impact & Community Enterprise Manager (Food Insecurity) - 6m FTC |
| 5 | Technical Lead (Full Stack Java) |
| 5 | Data Architect |
| 5 | 2nd Line Support |
| 5 | IT Manager |
| 5 | Senior Product Analyst |
| 4 | Planner |
| 4 | 1st Line Support |
| 4 | Service Delivery Manager |
| 4 | Application Support Analyst |
| 3 | Pricing Manager |
| 3 | Pre-reg 2027 |
| 3 | SOC Manager |
| 3 | Enterprise Architect |
| 3 | IT Systems Manager |
| 3 | Junior Application Support Analyst |
| 3 | IT Apprentice |
| 3 | Delivery Manager |
| 3 | F5 SME |
| 2 | Design Director |
| 2 | Corporate Senior Associate |
| 2 | Regional Quality/Safety Lead |
| 2 | Senior Planner |
| 2 | Tribunal Advocate |
| 2 | Architectural Technologist |
| 2 | Property Officer |
| 2 | PMO Analyst |
| 2 | Pensions Lead |
| 2 | Associate Director of Commercial Partnerships |
| 2 | Packaging Technologist |
| 2 | Design Manager |
| 2 | Large Format Print All-Rounder |
| 2 | Media Measurement Lead |
| 2 | Senior Case Worker |
| 2 | Behaviour Support Assistant - Reading |
| 2 | Project Support Officer |
| 2 | Senior Acoustic Consultant |
| 2 | Applications Specialist, Cardiology IT / PACS Systems |
| 2 | SOC Shift Lead |
| 2 | SAP Business One consultant |
| 2 | Technical Consultant |
| 2 | Oracle EPM Manager Big 4 |
| 2 | Oracle EPM Senior Manager Big 4 |
| 2 | Technical Delivery Manager |
| 2 | IT Service Delivery Manager |
| 2 | Environmental Health Officer |
| 2 | AWS Architect |
| 2 | Customer Analyst |
| 2 | CRO Analyst |
| 2 | Support Analyst |
| 2 | Product Analyst |
| 2 | Technical Lead |
| 2 | Windows 11 Deployment Manager |
| 2 | Change Manager |
| 2 | BI Analyst |
| 2 | Business Systems Manager |
| 2 | Head of Technology |
| 2 | Business Systems Analyst |
| 2 | SOC Analyst |
| 2 | Data Delivery Lead |
| 2 | Senior ERP Consultant - Implementation & Customer Success - Field / Remote UK |
| 1 | Stock Conditions Assistant |
| 1 | Licensing & Enforcement Processing Officer |
| 1 | Lead Contract Support |
| 1 | Mid Weight Interior Architect |
| 1 | Smartsheet SME |
| 1 | Head of IT Operations |
| 1 | Administrators |
| 1 | Commercial Director - Food Sector - Exclusive Role |
| 1 | Residential Worker - Complex Needs |
| 1 | NCR Facilitator |
| 1 | Bid & Tender Co-ordinator |
| 1 | Request for Support Officer |
| 1 | Trainee Crewing and Travel Manager |

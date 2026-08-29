# JobG8 register-first broad-family reconciliation

Jobs reconciled: **10,000**
Jobs assigned first from an existing selected Ontap register: **680**
Original title-rule Other / Unclassified: **3,545**
Jobs resolved by description-majority pass: **73**
Remaining Other / Unclassified after register-first + title + description passes: **1,890**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Other / Unclassified | 1,890 | 18.9% |
| Sales / Business Development | 1,144 | 11.4% |
| IT / Data / Software | 1,016 | 10.2% |
| Admin / Customer Service | 930 | 9.3% |
| Professional Finance / Accountancy | 847 | 8.5% |
| Healthcare / Clinical | 691 | 6.9% |
| Engineering / Technical | 573 | 5.7% |
| Management / Team Leadership | 476 | 4.8% |
| Marketing / Digital / Creative | 298 | 3.0% |
| Care / Support Work | 287 | 2.9% |
| Operations / General Management | 282 | 2.8% |
| HR / Recruitment | 229 | 2.3% |
| Retail / Store | 208 | 2.1% |
| Legal / Conveyancing | 195 | 1.9% |
| Market Research / Field Interviewing | 174 | 1.7% |
| Construction / Trades / Property | 125 | 1.2% |
| Property / Housing / Planning | 79 | 0.8% |
| Financial Advice / Mortgages | 76 | 0.8% |
| Insurance / Claims | 69 | 0.7% |
| Compliance / Risk / Quality | 64 | 0.6% |
| Education / Teaching | 61 | 0.6% |
| Procurement / Buying / Supply Chain | 61 | 0.6% |
| Charity / Fundraising / Community | 41 | 0.4% |
| Security / Emergency Services | 41 | 0.4% |
| Driving / Warehouse / Logistics | 40 | 0.4% |
| Hospitality / Catering | 25 | 0.2% |
| Employment Support / Careers | 20 | 0.2% |
| Manufacturing / Production | 19 | 0.2% |
| Cleaning / Domestic / Facilities | 16 | 0.2% |
| Agriculture / Environment | 12 | 0.1% |
| Science / Laboratory | 11 | 0.1% |
| **TOTAL** | **10,000** | **100.0%** |

## Refined family totals by salary band

Salary uses the midpoint of the available structured minimum/maximum after annualising hourly, daily, weekly or monthly amounts. Five-figure values are treated as annual even when the source period is inconsistent. The first column combines genuinely sub-£20k jobs with missing or unusable salary so every family reconciles exactly to its total.

| Broad family | Below £20k / unknown | £20k–<£35k | £35k–£45k | Over £45k | Total |
|---|---:|---:|---:|---:|---:|
| Other / Unclassified | 736 | 327 | 245 | 582 | 1,890 |
| Sales / Business Development | 306 | 256 | 217 | 365 | 1,144 |
| IT / Data / Software | 377 | 30 | 130 | 479 | 1,016 |
| Admin / Customer Service | 204 | 623 | 73 | 30 | 930 |
| Professional Finance / Accountancy | 223 | 161 | 166 | 297 | 847 |
| Healthcare / Clinical | 438 | 46 | 75 | 132 | 691 |
| Engineering / Technical | 189 | 52 | 99 | 233 | 573 |
| Management / Team Leadership | 118 | 151 | 118 | 89 | 476 |
| Marketing / Digital / Creative | 109 | 43 | 74 | 72 | 298 |
| Care / Support Work | 133 | 117 | 24 | 13 | 287 |
| Operations / General Management | 121 | 10 | 37 | 114 | 282 |
| HR / Recruitment | 53 | 113 | 44 | 19 | 229 |
| Retail / Store | 74 | 89 | 30 | 15 | 208 |
| Legal / Conveyancing | 51 | 57 | 21 | 66 | 195 |
| Market Research / Field Interviewing | 145 | 29 | 0 | 0 | 174 |
| Construction / Trades / Property | 28 | 28 | 29 | 40 | 125 |
| Property / Housing / Planning | 16 | 18 | 20 | 25 | 79 |
| Financial Advice / Mortgages | 16 | 9 | 16 | 35 | 76 |
| Insurance / Claims | 39 | 9 | 11 | 10 | 69 |
| Compliance / Risk / Quality | 28 | 2 | 7 | 27 | 64 |
| Education / Teaching | 33 | 19 | 3 | 6 | 61 |
| Procurement / Buying / Supply Chain | 22 | 10 | 12 | 17 | 61 |
| Charity / Fundraising / Community | 34 | 3 | 4 | 0 | 41 |
| Security / Emergency Services | 15 | 3 | 11 | 12 | 41 |
| Driving / Warehouse / Logistics | 10 | 23 | 4 | 3 | 40 |
| Hospitality / Catering | 6 | 11 | 5 | 3 | 25 |
| Employment Support / Careers | 8 | 12 | 0 | 0 | 20 |
| Manufacturing / Production | 2 | 7 | 4 | 6 | 19 |
| Cleaning / Domestic / Facilities | 3 | 12 | 1 | 0 | 16 |
| Agriculture / Environment | 2 | 3 | 4 | 3 | 12 |
| Science / Laboratory | 2 | 1 | 4 | 4 | 11 |
| **TOTAL** | **3,541** | **2,274** | **1,488** | **2,697** | **10,000** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Sales / Business Development | 1,144 | 0 | 1,144 | 82 | 8.0 | 59 | 33 | 84 | London (158); Greater Manchester - Manchester & Salford (49); Hampshire (46); Hertfordshire (39); Kent (34) |
| IT / Data / Software | 1,016 | 0 | 1,016 | 68 | 6.5 | 41 | 26 | 78 | London (213); Hampshire (63); Greater Manchester - Manchester & Salford (61); Bristol & Bath (47); Kent (46) |
| Admin / Customer Service | 930 | 343 | 587 | 78 | 5.0 | 42 | 25 | 173 | London (146); Surrey (43); Hampshire (35); Leicestershire (26); Kent (25) |
| Professional Finance / Accountancy | 847 | 145 | 702 | 79 | 8 | 49 | 30 | 67 | London (126); Yorkshire - West (35); Yorkshire - North (25); Merseyside - Liverpool (24); Bristol & Bath (22) |
| Healthcare / Clinical | 691 | 0 | 691 | 80 | 3.0 | 34 | 17 | 69 | London (114); Hampshire (39); Surrey (38); Sussex (34); North East - Tyneside, Wearside & Northumberland (24) |
| Engineering / Technical | 573 | 0 | 573 | 65 | 5 | 33 | 19 | 45 | London (97); Greater Manchester - Manchester & Salford (38); Kent (27); Bristol & Bath (26); Hampshire (15) |
| Management / Team Leadership | 476 | 0 | 476 | 77 | 4 | 34 | 16 | 25 | London (38); Essex (21); Oxfordshire (19); Sussex (19); Kent (17) |
| Marketing / Digital / Creative | 298 | 0 | 298 | 50 | 3.0 | 17 | 4 | 30 | London (87); Greater Manchester - Manchester & Salford (13); Hampshire (10); Yorkshire - West (10); Buckinghamshire (9) |
| Care / Support Work | 287 | 127 | 160 | 64 | 2.0 | 15 | 5 | 31 | London (41); Oxfordshire (18); Hampshire (15); Surrey (13); Somerset (10) |
| Operations / General Management | 282 | 0 | 282 | 52 | 3.0 | 18 | 4 | 18 | London (42); Oxfordshire (14); Bristol & Bath (13); Hampshire (13); Devon (9) |
| HR / Recruitment | 229 | 63 | 166 | 44 | 3.0 | 12 | 3 | 36 | London (34); Bristol & Bath (22); Hampshire (11); Yorkshire - West (9); Essex (7) |
| Retail / Store | 208 | 0 | 208 | 58 | 2.0 | 9 | 3 | 29 | London (23); Yorkshire - North (15); Oxfordshire (10); Kent (9); Wiltshire (8) |
| Legal / Conveyancing | 195 | 0 | 195 | 50 | 2.0 | 9 | 1 | 10 | London (56); Wiltshire (9); Yorkshire - South (8); Greater Manchester - Manchester & Salford (8); Sussex (7) |
| Market Research / Field Interviewing | 174 | 0 | 174 | 37 | 2 | 9 | 3 | 56 | Devon (12); Wiltshire (12); London (10); Scotland Central - Tayside (8); Berkshire (7) |
| Construction / Trades / Property | 125 | 0 | 125 | 39 | 2 | 5 | 1 | 11 | London (20); Bristol & Bath (5); Cambridgeshire (5); Essex (5); Greater Manchester - Manchester & Salford (5) |
| Property / Housing / Planning | 79 | 0 | 79 | 32 | 1.0 | 2 | 0 | 12 | London (9); Hertfordshire (5); Sussex (4); West Midlands - Coventry & Warwickshire (4); Surrey (4) |
| Financial Advice / Mortgages | 76 | 0 | 76 | 34 | 2.0 | 1 | 0 | 3 | London (8); Wiltshire (4); Leicestershire (4); Greater Manchester - Manchester & Salford (4); Surrey (3) |
| Insurance / Claims | 69 | 0 | 69 | 20 | 1.0 | 2 | 1 | 9 | London (27); Norfolk (5); Essex (3); West Midlands - Birmingham & Solihull (3); Greater Manchester - Manchester & Salford (3) |
| Compliance / Risk / Quality | 64 | 0 | 64 | 27 | 1 | 2 | 1 | 5 | London (14); Greater Manchester - Manchester & Salford (5); West Midlands - Birmingham & Solihull (4); Bristol & Bath (3); Scotland Central - Edinburgh & Lothians (3) |
| Education / Teaching | 61 | 0 | 61 | 22 | 1.0 | 2 | 1 | 9 | London (13); Cumbria - South (6); Lancashire - North (4); Wiltshire (3); Yorkshire - West (3) |
| Procurement / Buying / Supply Chain | 61 | 0 | 61 | 23 | 1 | 1 | 1 | 11 | London (14); Essex (4); Yorkshire - West (4); Devon (3); Hampshire (3) |
| Charity / Fundraising / Community | 41 | 0 | 41 | 16 | 2.0 | 1 | 1 | 4 | London (11); Buckinghamshire (4); West Midlands - Birmingham & Solihull (3); Hampshire (2); Yorkshire - West (2) |
| Security / Emergency Services | 41 | 0 | 41 | 14 | 1.0 | 2 | 0 | 10 | London (8); Hampshire (6); Bristol & Bath (3); Berkshire (3); Nottinghamshire (2) |
| Driving / Warehouse / Logistics | 40 | 2 | 38 | 26 | 1.0 | 0 | 0 | 6 | London (3); Leicestershire (2); Worcestershire (2); Staffordshire (2); Buckinghamshire (2) |
| Hospitality / Catering | 25 | 0 | 25 | 12 | 1.0 | 1 | 0 | 4 | London (5); Lincolnshire (3); Oxfordshire (2); Gloucestershire (2); Sussex (2) |
| Employment Support / Careers | 20 | 0 | 20 | 12 | 1.0 | 0 | 0 | 2 | London (3); Yorkshire - North (3); Wales - Mid (2); Bristol & Bath (2); Surrey (1) |
| Manufacturing / Production | 19 | 0 | 19 | 13 | 1 | 0 | 0 | 2 | London (3); Gloucestershire (2); Sussex (2); Suffolk (1); Worcestershire (1) |
| Cleaning / Domestic / Facilities | 16 | 0 | 16 | 10 | 1.0 | 0 | 0 | 3 | Northamptonshire (3); Bristol & Bath (2); London (1); Wiltshire (1); Yorkshire - South (1) |
| Agriculture / Environment | 12 | 0 | 12 | 7 | 2 | 0 | 0 | 0 | London (3); Cheshire - Warrington & Halton (2); Kent (2); Sussex (2); Devon (1) |
| Science / Laboratory | 11 | 0 | 11 | 5 | 1 | 0 | 0 | 3 | London (3); Gloucestershire (2); Worcestershire (1); West Midlands - Coventry & Warwickshire (1); Yorkshire - West (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 5,820 |
| still_unclassified | 1,890 |
| title_rule_pass2 | 1,537 |
| existing_register:admin_service | 251 |
| existing_register:finance_accounts | 145 |
| existing_register:support_worker | 127 |
| existing_register:customer_service_contact_centre | 92 |
| description_majority | 73 |
| existing_register:hr_recruitment | 63 |
| existing_register:warehouse_logistics | 2 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 21 | Contracts Manager |
| 15 | Junior Network Analyst |
| 11 | Trainee Junior Network Consultant |
| 10 | Trainee Network Analyst |
| 10 | Customer Representative Field Based |
| 9 | Sub Agent |
| 8 | Associate Director |
| 7 | Aftersales Manager |
| 7 | Technical Lead |
| 7 | Bid Manager |
| 6 | Client Relationship Manager |
| 6 | Contract Manager |
| 6 | Autocentre Manager |
| 6 | Social Impact & Community Enterprise Manager (Food Insecurity) - 6m FTC |
| 6 | Door to Door Canvasser |
| 6 | Housing Estates Officer |
| 5 | Tenancy Sustainment Officer |
| 5 | Planner |
| 5 | Ward Manager |
| 5 | Productivity Manager |
| 5 | General Foreman |
| 5 | Customer Relations Manager |
| 5 | Implementation Consultant |
| 4 | Insolvency Manager |
| 4 | Property Valuer |
| 4 | Head of IT |
| 4 | Shift Manager |
| 4 | Partnerships Manager |
| 4 | Remote Game Tester |
| 4 | Cost & Productivity - Senior Manager |
| 4 | Contractual Advisor |
| 4 | Head Installer |
| 4 | Subject Lead History and Politics |
| 3 | Property Officer |
| 3 | Installer Development Representative |
| 3 | Development Manager |
| 3 | Senior Cost Consultant |
| 3 | Senior Authorised Person |
| 3 | Head of Planning |
| 3 | Team Manager |
| 3 | Technical Manager |
| 3 | Hairdresser |
| 3 | Senior Contracts Manager |
| 3 | Pre-reg 2027 |
| 3 | Partnership Manager |
| 3 | Associate Director of Commercial Partnerships |
| 3 | Packaging Technologist |
| 3 | Technical Director |
| 3 | Media Measurement Lead |
| 3 | Cost & Productivity Senior Manager |
| 3 | Cost & Productivity Manager (TMT) |
| 3 | ASB Officer |
| 3 | Applications Specialist, Cardiology IT / PACS Systems |
| 3 | Vulnerability Researcher |
| 3 | Account Director |
| 3 | Portfolio Manager |
| 3 | CRO Analyst |
| 3 | 2nd Line Support |
| 3 | Service Delivery Manager |
| 3 | Senior User Researcher |
| 3 | Butchery Manager |
| 3 | Head of Knowledge Management |
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

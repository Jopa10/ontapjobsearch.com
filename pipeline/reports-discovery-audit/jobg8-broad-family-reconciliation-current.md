# JobG8 register-first broad-family reconciliation

Jobs reconciled: **10,000**
Jobs assigned first from an existing selected Ontap register: **670**
Original title-rule Other / Unclassified: **3,075**
Jobs resolved by description-majority pass: **155**
Remaining Other / Unclassified after register-first + title + description passes: **1,683**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Other / Unclassified | 1,683 | 16.8% |
| Sales / Business Development | 1,063 | 10.6% |
| Admin / Customer Service | 986 | 9.9% |
| Legal / Conveyancing | 937 | 9.4% |
| HR / Recruitment | 769 | 7.7% |
| Professional Finance / Accountancy | 711 | 7.1% |
| Marketing / Digital / Creative | 507 | 5.1% |
| Construction / Trades / Property | 480 | 4.8% |
| Healthcare / Clinical | 434 | 4.3% |
| IT / Data / Software | 412 | 4.1% |
| Engineering / Technical | 306 | 3.1% |
| Insurance / Claims | 285 | 2.9% |
| Management / Team Leadership | 268 | 2.7% |
| Care / Support Work | 235 | 2.4% |
| Retail / Store | 179 | 1.8% |
| Market Research / Field Interviewing | 136 | 1.4% |
| Operations / General Management | 123 | 1.2% |
| Financial Advice / Mortgages | 101 | 1.0% |
| Procurement / Buying / Supply Chain | 64 | 0.6% |
| Compliance / Risk / Quality | 59 | 0.6% |
| Property / Housing / Planning | 52 | 0.5% |
| Charity / Fundraising / Community | 41 | 0.4% |
| Education / Teaching | 36 | 0.4% |
| Driving / Warehouse / Logistics | 30 | 0.3% |
| Hospitality / Catering | 21 | 0.2% |
| Science / Laboratory | 18 | 0.2% |
| Manufacturing / Production | 17 | 0.2% |
| Security / Emergency Services | 17 | 0.2% |
| Employment Support / Careers | 13 | 0.1% |
| Cleaning / Domestic / Facilities | 11 | 0.1% |
| Agriculture / Environment | 6 | 0.1% |
| **TOTAL** | **10,000** | **100.0%** |

## Refined family totals by salary band

Salary uses the midpoint of the available structured minimum/maximum after annualising hourly, daily, weekly or monthly amounts. Five-figure values are treated as annual even when the source period is inconsistent. The first column combines genuinely sub-£20k jobs with missing or unusable salary so every family reconciles exactly to its total.

| Broad family | Below £20k / unknown | £20k–<£35k | £35k–£45k | Over £45k | Total |
|---|---:|---:|---:|---:|---:|
| Other / Unclassified | 889 | 259 | 187 | 348 | 1,683 |
| Sales / Business Development | 387 | 232 | 179 | 265 | 1,063 |
| Admin / Customer Service | 324 | 532 | 103 | 27 | 986 |
| Legal / Conveyancing | 611 | 90 | 62 | 174 | 937 |
| HR / Recruitment | 380 | 117 | 157 | 115 | 769 |
| Professional Finance / Accountancy | 319 | 97 | 98 | 197 | 711 |
| Marketing / Digital / Creative | 241 | 70 | 99 | 97 | 507 |
| Construction / Trades / Property | 193 | 78 | 65 | 144 | 480 |
| Healthcare / Clinical | 290 | 31 | 43 | 70 | 434 |
| IT / Data / Software | 219 | 14 | 54 | 125 | 412 |
| Engineering / Technical | 127 | 41 | 64 | 74 | 306 |
| Insurance / Claims | 183 | 11 | 39 | 52 | 285 |
| Management / Team Leadership | 99 | 51 | 50 | 68 | 268 |
| Care / Support Work | 108 | 83 | 20 | 24 | 235 |
| Retail / Store | 82 | 69 | 20 | 8 | 179 |
| Market Research / Field Interviewing | 80 | 56 | 0 | 0 | 136 |
| Operations / General Management | 70 | 7 | 14 | 32 | 123 |
| Financial Advice / Mortgages | 25 | 9 | 24 | 43 | 101 |
| Procurement / Buying / Supply Chain | 22 | 14 | 14 | 14 | 64 |
| Compliance / Risk / Quality | 33 | 6 | 4 | 16 | 59 |
| Property / Housing / Planning | 8 | 15 | 11 | 18 | 52 |
| Charity / Fundraising / Community | 34 | 2 | 3 | 2 | 41 |
| Education / Teaching | 15 | 13 | 5 | 3 | 36 |
| Driving / Warehouse / Logistics | 6 | 16 | 5 | 3 | 30 |
| Hospitality / Catering | 6 | 6 | 4 | 5 | 21 |
| Science / Laboratory | 7 | 2 | 6 | 3 | 18 |
| Manufacturing / Production | 4 | 10 | 1 | 2 | 17 |
| Security / Emergency Services | 11 | 3 | 0 | 3 | 17 |
| Employment Support / Careers | 5 | 8 | 0 | 0 | 13 |
| Cleaning / Domestic / Facilities | 1 | 9 | 1 | 0 | 11 |
| Agriculture / Environment | 1 | 1 | 2 | 2 | 6 |
| **TOTAL** | **4,780** | **1,952** | **1,334** | **1,934** | **10,000** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Sales / Business Development | 1,063 | 0 | 1,063 | 81 | 6 | 50 | 30 | 71 | London (194); Greater Manchester - Manchester & Salford (50); Hertfordshire (41); Surrey (32); Hampshire (31) |
| Admin / Customer Service | 986 | 367 | 619 | 76 | 6.0 | 43 | 20 | 176 | London (224); North East - Tyneside, Wearside & Northumberland (56); Kent (31); Surrey (31); Hampshire (30) |
| Legal / Conveyancing | 937 | 0 | 937 | 73 | 7 | 45 | 24 | 32 | London (215); Greater Manchester - Manchester & Salford (55); West Midlands - Birmingham & Solihull (47); Yorkshire - West (45); Bristol & Bath (28) |
| HR / Recruitment | 769 | 107 | 662 | 72 | 6.0 | 41 | 21 | 73 | London (148); West Midlands - Birmingham & Solihull (36); Northern Ireland - East (36); Bristol & Bath (23); West Midlands - Coventry & Warwickshire (22) |
| Professional Finance / Accountancy | 711 | 112 | 599 | 73 | 5 | 38 | 15 | 75 | London (178); Yorkshire - West (27); Sussex (22); Greater Manchester - Manchester & Salford (21); Merseyside - Liverpool (18) |
| Marketing / Digital / Creative | 507 | 0 | 507 | 60 | 4.0 | 28 | 11 | 33 | London (153); Surrey (19); Yorkshire - West (17); Berkshire (16); Greater Manchester - Manchester & Salford (15) |
| Construction / Trades / Property | 480 | 0 | 480 | 59 | 4 | 28 | 10 | 30 | London (118); Sussex (28); Kent (27); Essex (25); Hertfordshire (20) |
| Healthcare / Clinical | 434 | 0 | 434 | 75 | 2 | 22 | 9 | 58 | London (82); Surrey (20); Hampshire (19); Sussex (18); Essex (10) |
| IT / Data / Software | 412 | 0 | 412 | 55 | 3 | 15 | 7 | 50 | London (121); Hampshire (30); Kent (22); Gloucestershire (20); Greater Manchester - Manchester & Salford (17) |
| Engineering / Technical | 306 | 0 | 306 | 59 | 3 | 19 | 3 | 25 | London (74); Greater Manchester - Manchester & Salford (14); Gloucestershire (11); Berkshire (9); Surrey (9) |
| Insurance / Claims | 285 | 0 | 285 | 48 | 3.0 | 14 | 4 | 30 | London (81); Greater Manchester - Manchester & Salford (16); Essex (15); Bristol & Bath (12); Yorkshire - West (9) |
| Management / Team Leadership | 268 | 0 | 268 | 62 | 2.0 | 18 | 3 | 28 | London (37); Sussex (15); Oxfordshire (10); Bristol & Bath (8); North East - County Durham & Darlington/Hartlepool (8) |
| Care / Support Work | 235 | 84 | 151 | 54 | 2.0 | 13 | 2 | 42 | London (36); Hampshire (18); Greater Manchester - Manchester & Salford (7); Cumbria - South (6); Sussex (6) |
| Retail / Store | 179 | 0 | 179 | 52 | 2.0 | 8 | 2 | 30 | London (25); Yorkshire - North (12); Oxfordshire (7); Bristol & Bath (6); Northern Ireland - West (6) |
| Market Research / Field Interviewing | 136 | 0 | 136 | 25 | 2 | 7 | 2 | 51 | Lincolnshire (11); Berkshire (10); Dorset (7); North Wales - East (6); Wiltshire (5) |
| Operations / General Management | 123 | 0 | 123 | 42 | 1.0 | 5 | 1 | 13 | London (35); Hampshire (8); Berkshire (5); West Midlands - Birmingham & Solihull (5); Yorkshire - West (5) |
| Financial Advice / Mortgages | 101 | 0 | 101 | 35 | 2 | 5 | 1 | 5 | London (12); Surrey (7); Essex (7); Hampshire (6); Leicestershire (6) |
| Procurement / Buying / Supply Chain | 64 | 0 | 64 | 26 | 1.0 | 1 | 1 | 14 | London (16); Kent (3); Northern Ireland - West (3); Surrey (2); Hertfordshire (2) |
| Compliance / Risk / Quality | 59 | 0 | 59 | 20 | 1.0 | 1 | 1 | 4 | London (27); Bristol & Bath (3); Sussex (3); Greater Manchester - Manchester & Salford (3); West Midlands - Birmingham & Solihull (2) |
| Property / Housing / Planning | 52 | 0 | 52 | 23 | 1 | 1 | 0 | 8 | London (9); Kent (4); Surrey (3); West Midlands - Coventry & Warwickshire (3); Devon (3) |
| Charity / Fundraising / Community | 41 | 0 | 41 | 18 | 1.5 | 1 | 1 | 3 | London (12); West Midlands - Birmingham & Solihull (3); Bedfordshire (2); Norfolk (2); Buckinghamshire (2) |
| Education / Teaching | 36 | 0 | 36 | 14 | 1.0 | 1 | 0 | 7 | London (8); Yorkshire - West (4); Sussex (4); Midlothian (2); Wales South - Valleys (2) |
| Driving / Warehouse / Logistics | 30 | 0 | 30 | 19 | 1 | 1 | 0 | 3 | London (6); Kent (3); Berkshire (2); Essex (1); Northamptonshire (1) |
| Hospitality / Catering | 21 | 0 | 21 | 10 | 1.0 | 1 | 0 | 2 | London (9); Hampshire (2); Gloucestershire (1); Sussex (1); Devon (1) |
| Science / Laboratory | 18 | 0 | 18 | 9 | 1 | 1 | 0 | 4 | London (5); Dorset (2); Worcestershire (1); Northamptonshire (1); West Midlands - Coventry & Warwickshire (1) |
| Manufacturing / Production | 17 | 0 | 17 | 12 | 1.0 | 0 | 0 | 1 | Gloucestershire (2); Hampshire (2); London (2); Buckinghamshire (2); Surrey (1) |
| Security / Emergency Services | 17 | 0 | 17 | 7 | 1 | 1 | 0 | 2 | London (8); Buckinghamshire (2); Berkshire (1); West Midlands - Coventry & Warwickshire (1); Surrey (1) |
| Employment Support / Careers | 13 | 0 | 13 | 11 | 1 | 0 | 0 | 1 | Yorkshire - North (2); Northamptonshire (1); Merseyside - Liverpool (1); Norfolk (1); Yorkshire - West (1) |
| Cleaning / Domestic / Facilities | 11 | 0 | 11 | 7 | 1 | 0 | 0 | 1 | London (4); Yorkshire - South (1); West Midlands - Birmingham & Solihull (1); Shropshire (1); Worcestershire (1) |
| Agriculture / Environment | 6 | 0 | 6 | 4 | 1.5 | 0 | 0 | 0 | Sussex (2); London (2); Bristol & Bath (1); Yorkshire - North (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 6,290 |
| still_unclassified | 1,683 |
| title_rule_pass2 | 1,202 |
| existing_register:admin_service | 253 |
| description_majority | 155 |
| existing_register:customer_service_contact_centre | 114 |
| existing_register:finance_accounts | 112 |
| existing_register:hr_recruitment | 107 |
| existing_register:support_worker | 84 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 16 | Senior Cash Operations Analyst |
| 16 | Senior Assistant - Cash Operations |
| 15 | Account Handler |
| 15 | Senior Working Capital Assistant |
| 15 | Senior Pitch Assistant |
| 12 | Property Lister |
| 11 | Pitch Executive (5.00pm - 1:30am) |
| 10 | Door to Door Canvasser |
| 10 | ER Advisor |
| 10 | Bid Manager |
| 10 | Aftersales Manager |
| 9 | Development Executive |
| 8 | Sub Agent |
| 8 | Client Relationship Manager |
| 7 | People Manager |
| 7 | Customer Representative Field Based |
| 7 | Mammographer |
| 7 | Lead Ophthalmology Scrub Practitioner |
| 6 | Housing Estates Officer |
| 5 | Senior Bid Manager |
| 5 | Autocentre Manager |
| 5 | Executive Search Consultant |
| 5 | Lead Operational Technology Specialist |
| 4 | CRM Manager |
| 4 | Design Manager |
| 4 | Insolvency Manager |
| 4 | Customer Relations Manager |
| 4 | Photographer |
| 4 | Service Delivery Manager |
| 4 | Associate Director |
| 4 | Specification Manager |
| 4 | Tenancy Fraud Manager |
| 4 | Site Services Manager |
| 4 | Dementia Adviser |
| 4 | Block Manager |
| 3 | Change Manager |
| 3 | Head of People |
| 3 | Partnerships Manager |
| 3 | Senior Cost Consultant |
| 3 | Technical Director |
| 3 | Property Valuer |
| 3 | Senior Authorised Person |
| 3 | Learning And Development Advisor |
| 3 | Events Manager |
| 3 | Event Manager |
| 3 | Paid Media Manager |
| 3 | People Business Partner |
| 3 | Research Consultant |
| 3 | Land Agent |
| 3 | Repairs Planner |
| 3 | Junior HRIS Analyst |
| 3 | F5 SME |
| 3 | Tribunal Advocate |
| 3 | Account Director |
| 3 | Brand Ambassadors In-Store Food & Drink Sampling |
| 3 | Canvasser |
| 3 | Treasurer |
| 3 | Hire Desk Manager |
| 3 | Head of GTM - Tax |
| 3 | Client Services Manager |
| 3 | Financial Planning Director |
| 3 | Service Transition Manager |
| 3 | Reward Analyst |
| 3 | Technical & Regulatory Information Officer |
| 3 | Letting Negotiator |
| 3 | Director of Quantitative Operations |
| 3 | Workforce Planning Business Partner |
| 3 | Freelance Interpreter |
| 2 | Client Portfolio Manager |
| 2 | Tenancy Sustainment Officer |
| 2 | Smart Metering Planner |
| 2 | Packaging Technologist |
| 2 | Customer Success Executive |
| 2 | Graduate Opportunities |
| 2 | Large Format Print All-Rounder |

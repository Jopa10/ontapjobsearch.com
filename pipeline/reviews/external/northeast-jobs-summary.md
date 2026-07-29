# North East Jobs ETL proof-of-concept review

Run generated: 2026-07-29T09:59:43+01:00
RSS input: https://www.northeastjobs.org.uk/RSSJobs.aspx?orgid=62 (retrieved through text renderer because local proxy rejected source TLS chain)
JobG8 comparison rows in target geographies: 103

## Funnel

- RSS vacancies read: 656
- Hard-pass title/teaser screen before detail requests: 589
- Detail candidates: 67
- Detail failures or unavailable snapshots: 0
- Outside the two target geographies: 2
- Tees Valley explicitly excluded: 11
- Target-geography candidates reviewed: 54

## Detail diagnostics

- No unresolved detail-page failures.

## Review outcomes

- HC: 17
- POSS: 36
- Hard pass: 1
- Confirmed JobG8 duplicates: 0
- Possible JobG8 duplicates: 0
- Likely unique to North East Jobs: 54
- Rows in possible within-source duplicate groups: 2

## HC and POSS roles

| Decision | Vacancy | Employer | Location | Closing | JobG8 | Source duplicate |
|---|---|---|---|---|---|---|
| HC | [Administration Assistant](https://www.northeastjobs.org.uk/job/Administration_Assistant/299480) | Durham County Council | Meadowfield Depot, Durham (hybrid working options available) | 09/08/2026 | No plausible match | NO |
| HC | [Administration Assistant](https://www.northeastjobs.org.uk/job/Administration_Assistant/300074) | Northumberland County Council | Northumberland (derived for filtering) | 31/07/2026 00:00 | No plausible match | NO |
| HC | [Administration Assistant](https://www.northeastjobs.org.uk/job/Administration_Assistant/300098) | Bishop Bewick Catholic Education Trust | St Benet Biscop Catholic Academy, Ridge Terrace, Bedlington, NE22 6ED | 17/08/2026 12:00 | No plausible match | NO |
| HC | [Administration Assistant](https://www.northeastjobs.org.uk/job/Administration_Assistant/299693) | Christ's College | Sunderland | 03/08/2026 09:00 | No plausible match | NO |
| HC | [Administrative Assistant](https://www.northeastjobs.org.uk/job/Administrative_Assistant/299277) | Durham County Council | Sacriston | 31/08/2026 | No plausible match | NO |
| HC | [Administrative Assistant](https://www.northeastjobs.org.uk/job/Administrative_Assistant/300057) | Newcastle City Council | Newcastle Upon Tyne | 05/08/2026 22:59 | No plausible match | NO |
| HC | [Business Support Assistant](https://www.northeastjobs.org.uk/job/Business_Support_Assistant/297597) | North Tyneside Council | North Tyneside | 07/08/2026 00:00 | No plausible match | NO |
| HC | [Business Support Assistant - Children's Social Care](https://www.northeastjobs.org.uk/job/Business_Support_Assistant_Children_s_Social_Care/300179) | Together for Children - Sunderland | Sunderland | 10/08/2026 | No plausible match | NO |
| HC | [Business Support Officer (Level 1)](https://www.northeastjobs.org.uk/job/Business_Support_Officer_Level_1/299898) | Darlington Borough Council | Town Hall | 09/08/2026 | No plausible match | NO |
| HC | [Business Support Officer, 32hpw](https://www.northeastjobs.org.uk/job/Business_Support_Officer_32hpw/300058) | South Tyneside Council | South Tyneside (derived for filtering) | 17/08/2026 12:00 | No plausible match | NO |
| HC | [Clerical Officer Receptionist](https://www.northeastjobs.org.uk/job/Clerical_Officer_Receptionist/299726) | Durham County Council | Annfield Plain, Greencroft | 29/07/2026 | No plausible match | NO |
| HC | [Clerical Officer Receptionist](https://www.northeastjobs.org.uk/job/Clerical_Officer_Receptionist/299508) | Durham County Council | Wheatley Hill | 02/08/2026 | No plausible match | NO |
| HC | [Customer Service Advisor](https://www.northeastjobs.org.uk/job/Customer_Service_Advisor/299796) | Hartlepool Borough Council | Highlight Active Wellbeing Hub | 31/08/2026 | No plausible match | NO |
| HC | [DBS01116/26 - Admin Assistant - Hazlewood Community Primary School](https://www.northeastjobs.org.uk/job/DBS01116_26_Admin_Assistant_Hazlewood_Community_Primary_School/299761) | North Tyneside Council | Hazlewood Community Primary School, Canterbury Way, Wideopen, Newcastle upon Tyne | 21/08/2026 12:00 | No plausible match | NO |
| HC | [Receptionist & Administrator (HR / School)](https://www.northeastjobs.org.uk/job/Receptionist_Administrator_HR_School/299953) | Talbot House Children's Charity | Newcastle upon Tyne | 09/08/2026 | No plausible match | NO |
| HC | [Receptionist and Events Co-ordinator at the Sjovoll Centre](https://www.northeastjobs.org.uk/job/Receptionist_and_Events_Co_ordinator_at_the_Sjovoll_Centre/299718) | Framwellgate School Durham | Durham (derived for filtering) | 10/08/2026 09:00 | No plausible match | NO |
| HC | [Receptionist/Student Services](https://www.northeastjobs.org.uk/job/Receptionist_Student_Services/299744) | Northern Leaders Trust | Studio West, West Denton Way, Newcastle upon Tyne, NE5 2SZ | 30/07/2026 09:00 | No plausible match | NO |
| POSS | [0.4 Lecturer Coordinator in Counselling & Psychotherapy Studies](https://www.northeastjobs.org.uk/job/0_4_Lecturer_Coordinator_in_Counselling_Psychotherapy_Studies/299764) | Bishop Auckland College | Bishop Auckland (derived for filtering) | 18/08/2026 | No plausible match | NO |
| POSS | [Administrative Assistant (HR)](https://www.northeastjobs.org.uk/job/Administrative_Assistant_HR/300042) | Newcastle City Council | Newcastle (derived for filtering) | 09/08/2026 22:59 | No plausible match | NO |
| POSS | [Attendance & Support Officer](https://www.northeastjobs.org.uk/job/Attendance_Support_Officer/299877) | Hartlepool Borough Council | The Horizon School, CETL, Brierton Lane, Hartlepool | 04/09/2026 12:00 | No plausible match | NO |
| POSS | [Attendance Officer](https://www.northeastjobs.org.uk/job/Attendance_Officer/299650) | The Duchess's Community High School | Alnwick | 31/07/2026 12:00 | No plausible match | NO |
| POSS | [Community Engagement Officer (Part Time)](https://www.northeastjobs.org.uk/job/Community_Engagement_Officer_Part_Time/299795) | Peterlee Town Council | Peterlee | 14/08/2026 | No plausible match | NO |
| POSS | [Customer Enabling Services Support Assistant (Payroll)](https://www.northeastjobs.org.uk/job/Customer_Enabling_Services_Support_Assistant_Payroll/299864) | Sunderland City Council | Sunderland (derived for filtering) | 02/08/2026 | No plausible match | NO |
| POSS | [Customer Enabling Services Support Assistant/Courier](https://www.northeastjobs.org.uk/job/Customer_Enabling_Services_Support_Assistant_Courier/299831) | Sunderland City Council | Sunderland (derived for filtering) | 02/08/2026 | No plausible match | NO |
| POSS | [Data and Exams Officer](https://www.northeastjobs.org.uk/job/Data_and_Exams_Officer/300012) | Walbottle Academy | Newcastle Upon Tyne | 24/08/2026 09:00 | No plausible match | NO |
| POSS | [Events Assistant](https://www.northeastjobs.org.uk/job/Events_Assistant/300044) | Darlington Borough Council | Darlington (derived for filtering) | 11/08/2026 | No plausible match | NO |
| POSS | [Facilities Coordinator](https://www.northeastjobs.org.uk/job/Facilities_Coordinator/300105) | The Bowes Museum | Barnard Castle | 24/08/2026 08:00 | No plausible match | NO |
| POSS | [Finance & Office Administrator (Maternity Cover) – Office based, Newcastle City Centre](https://www.northeastjobs.org.uk/job/Finance_Office_Administrator_Maternity_Cover_Office_based_Newcastle_City_Centre/299489) | Rape Crisis Tyneside & Northumberland | Newcastle upon Tyne | 30/07/2026 12:00 | No plausible match | NO |
| POSS | [Fundraising & Partnerships Coordinator](https://www.northeastjobs.org.uk/job/Fundraising_Partnerships_Coordinator/299556) | YMCA North Tyneside | North Tyneside | 03/08/2026 | No plausible match | NO |
| POSS | [Homeless Support Officer](https://www.northeastjobs.org.uk/job/Homeless_Support_Officer/300070) | North Tyneside Council | North Tyneside | 06/08/2026 00:00 | No plausible match | NO |
| POSS | [Housing Assistant](https://www.northeastjobs.org.uk/job/Housing_Assistant/298231) | Newcastle City Council | Newcastle (derived for filtering) | 04/08/2026 22:59 | No plausible match | NO |
| POSS | [Information Management and Data Services Officer](https://www.northeastjobs.org.uk/job/Information_Management_and_Data_Services_Officer/299570) | Durham County Council | Green Lane Council Offices, Spennymoor (Plus Hybrid Working) | 02/08/2026 | No plausible match | NO |
| POSS | [Local Area Coordinator – Primrose](https://www.northeastjobs.org.uk/job/Local_Area_Coordinator_Primrose/299943) | South Tyneside Council | Adult Social Care, South Tyneside | 28/08/2026 12:00 | No plausible match | NO |
| POSS | [MCR Pathways Programme Coordinator](https://www.northeastjobs.org.uk/job/MCR_Pathways_Programme_Coordinator/300079) | Gosforth Group | Callerton Academy, Bedeburn Road, Newcastle upon Tyne NE5 4JQ | 05/08/2026 09:00 | No plausible match | NO |
| POSS | [Participation and Engagement Officer (SEND), 29.6 hpw](https://www.northeastjobs.org.uk/job/Participation_and_Engagement_Officer_SEND_29_6_hpw/299890) | South Tyneside Council | South Tyneside (derived for filtering) | 10/08/2026 12:00 | No plausible match | NO |
| POSS | [PMO Secretariat](https://www.northeastjobs.org.uk/job/PMO_Secretariat/299845) | Gateshead Council | Gateshead | 02/08/2026 | No plausible match | NO |
| POSS | [PMO Support Officer](https://www.northeastjobs.org.uk/job/PMO_Support_Officer/299841) | Gateshead Council | Gateshead | 02/08/2026 | No plausible match | POSSIBLE_SOURCE_DUPLICATE |
| POSS | [PMO Support Officer](https://www.northeastjobs.org.uk/job/PMO_Support_Officer/299843) | Gateshead Council | Gateshead | 02/08/2026 | No plausible match | POSSIBLE_SOURCE_DUPLICATE |
| POSS | [Review Officer](https://www.northeastjobs.org.uk/job/Review_Officer/298685) | Durham County Council | Spectrum Business Park, Seaham (hybrid working options available) | 09/08/2026 | No plausible match | NO |
| POSS | [School Administrator](https://www.northeastjobs.org.uk/job/School_Administrator/256127) | First Class Supply & Training | County Durham | 31/08/2026 | No plausible match | NO |
| POSS | [School Administrator](https://www.northeastjobs.org.uk/job/School_Administrator/256124) | First Class Supply & Training | Gateshead (derived for filtering) | 31/08/2026 | No plausible match | NO |
| POSS | [School Administrator](https://www.northeastjobs.org.uk/job/School_Administrator/256125) | First Class Supply & Training | South Tyneside (derived for filtering) | 31/08/2026 | No plausible match | NO |
| POSS | [School Administrator](https://www.northeastjobs.org.uk/job/School_Administrator/256120) | First Class Supply & Training | Northumberland | 31/08/2026 | No plausible match | NO |
| POSS | [School Administrator](https://www.northeastjobs.org.uk/job/School_Administrator/256121) | First Class Supply & Training | North Tyneside | 31/08/2026 | No plausible match | NO |
| POSS | [School Administrator](https://www.northeastjobs.org.uk/job/School_Administrator/256122) | First Class Supply & Training | Newcastle upon Tyne | 31/08/2026 | No plausible match | NO |
| POSS | [School Administrator](https://www.northeastjobs.org.uk/job/School_Administrator/256126) | First Class Supply & Training | Sunderland | 31/08/2026 | No plausible match | NO |
| POSS | [SEND Review Coordinator](https://www.northeastjobs.org.uk/job/SEND_Review_Coordinator/299411) | South Tyneside Council | South Tyneside (derived for filtering) | 30/07/2026 12:00 | No plausible match | NO |
| POSS | [SEND Travel Needs Assessment Officer](https://www.northeastjobs.org.uk/job/SEND_Travel_Needs_Assessment_Officer/300099) | South Tyneside Council | South Tyneside (derived for filtering) | 14/08/2026 12:00 | No plausible match | NO |
| POSS | [Social Care Assessment Officer](https://www.northeastjobs.org.uk/job/Social_Care_Assessment_Officer/298838) | Newcastle City Council | Newcastle upon Tyne | 11/08/2026 22:59 | No plausible match | NO |
| POSS | [Street Works Permit Support Officer](https://www.northeastjobs.org.uk/job/Street_Works_Permit_Support_Officer/299906) | Gateshead Council | Gateshead | 09/08/2026 | No plausible match | NO |
| POSS | [Tenant Engagement Officer](https://www.northeastjobs.org.uk/job/Tenant_Engagement_Officer/299408) | Northumberland County Council | Eddie Ferguson House, Blyth, United Kingdom | 02/08/2026 | No plausible match | NO |
| POSS | [Virtual School Education Support Officer](https://www.northeastjobs.org.uk/job/Virtual_School_Education_Support_Officer/299780) | Northumberland County Council | County Hall MORPETH, United Kingdom | 06/08/2026 | No plausible match | NO |
| POSS | [Visitor Services Officer](https://www.northeastjobs.org.uk/job/Visitor_Services_Officer/299897) | Durham County Council | Bowlees Visitor Centre, Newbiggin | 10/08/2026 | No plausible match | NO |

## Hard passes

- [Application Support Officer (INTERNAL ONLY)](https://www.northeastjobs.org.uk/job/Application_Support_Officer_INTERNAL_ONLY/299809) — not open to external applicants.

## Safety boundary

- Review-only output; no Ontap publishable JSON is written.
- Only factual vacancy fields are retained; full descriptions are not stored.
- Detail pages are fetched only after a provisional title/teaser screen.
- North East Jobs terms require written permission for commercial reuse of site material.
- The source had no retrievable robots.txt (404) when the POC was designed.
- HC/POSS rules are provisional and do not amend Ontap's permanent selection policy.

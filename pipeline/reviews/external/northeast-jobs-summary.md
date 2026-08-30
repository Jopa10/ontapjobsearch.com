# North East Jobs ETL proof-of-concept review

review_date: 2026-08-30
review_fingerprint: 5c4071358d739c23a97378bd08de05875e76e44927b4349e7c82ba1165ad7159

Edit only the `action:` line in each editable block:

- For a POSS job, use `action: select` to add it or `action: exclude` to reject it.
- For a selected HC job, use `action: exclude` to remove it.
- Leave `action:` blank for no change.
- Commit the edit; the review workflow will remember the decision.
- Decisions are carried forward only while the same vacancy review facts remain unchanged.

Run generated: 2026-08-30T12:55:20+01:00
RSS input: https://www.northeastjobs.org.uk/RSSJobs.aspx?orgid=62
JobG8 comparison rows in target geographies: 256

## Funnel

- RSS vacancies read: 694
- Hard-pass title/teaser screen before detail requests: 643
- Detail candidates: 51
- Detail failures or unavailable snapshots: 1
- Outside the two target geographies: 3
- Tees Valley explicitly excluded: 10
- Target-geography candidates reviewed: 37

## Detail diagnostics

- 301018 — Business Support Assistant: TimeoutError

## Review outcomes

- HC: 13
- POSS: 22
- Hard pass: 2
- Final selected after remembered/manual actions: 29
- Final POSS awaiting decision: 0
- Manually excluded: 6
- Confirmed JobG8 duplicates: 0
- Possible JobG8 duplicates: 1
- Likely unique to North East Jobs: 36
- Rows in possible within-source duplicate groups: 0

- Manual review warning: manual review date 2026-08-29 is not 2026-08-30; old actions ignored

## SELECTED

---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Green Lane, Spennymoor, Durham | £15,434 per annum NMW in first year of apprenticeship | Apprentice Economic Development Administrator
employer: Durham County Council
closing_date: 06/09/2026
reason: clear transferable title: administrator
source_job_id: 301034
source_url: https://www.northeastjobs.org.uk/job/Apprentice_Economic_Development_Administrator/301034
---
---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Highlight Active Wellbeing Hub | £13.47 per hour | Customer Service Advisor
employer: Hartlepool Borough Council
closing_date: 31/08/2026
reason: clear transferable title: customer service advisor
source_job_id: 299796
source_url: https://www.northeastjobs.org.uk/job/Customer_Service_Advisor/299796
---
---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Sedgefield | Points 4-6, FTE £25,185 - £25,989 Actual £21,730 - £22,424 | SEN Administrator
employer: Sedgefield Community College
closing_date: 03/09/2026 12:00
reason: clear transferable title: administrator
source_job_id: 299750
source_url: https://www.northeastjobs.org.uk/job/SEN_Administrator/299750
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Prudhoe | SCP 2 - 5 (£24,413 - £25,583 (pro rata) depending upon qualifications and experience | Administrative Assistant
employer: Prudhoe Town Council
closing_date: 04/09/2026 12:00
reason: clear transferable title: administrative assistant
source_job_id: 300646
source_url: https://www.northeastjobs.org.uk/job/Administrative_Assistant/300646
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Gosforth Academy, Great North Road, Knightsbridge, Gosforth, Newcastle upon Tyne, NE3 2JH | £26,403 - £27,254 per annum. Actual Salary £22,646 - £23,376 | Administrative Assistant Level 3
employer: Gosforth Group
closing_date: 10/09/2026 09:00
reason: clear transferable title: administrative assistant
source_job_id: 301207
source_url: https://www.northeastjobs.org.uk/job/Administrative_Assistant_Level_3/301207
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Sacred Heart Catholic High School, Fenham Hall Drive, Fenham, Newcastle upon Tyne NE4 9YH | £26,403 - £27,254 per annum pro rata (Actual salary £22,671 - £23,401 per annum) | Administrative Assistant Level 3
employer: Bishop Bewick Catholic Education Trust
closing_date: 03/09/2026 09:00
reason: clear transferable title: administrative assistant
source_job_id: 300745
source_url: https://www.northeastjobs.org.uk/job/Administrative_Assistant_Level_3/300745
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Gateshead | £26,824 - £28,142 | Business Support Assistant
employer: Gateshead Council
closing_date: 02/09/2026
reason: clear transferable title: business support assistant
source_job_id: 300950
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Assistant/300950
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | North Tyneside | Grade 5 (£26,403 - £27,254) per annum | Business Support Assistant - Care point
employer: North Tyneside Council
closing_date: 04/09/2026 00:00
reason: clear transferable title: business support assistant
source_job_id: 301062
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Assistant_Care_point/301062
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Gateshead | £26,824 - £28,142 | Business Support Assistant - Family Hubs
employer: Gateshead Council
closing_date: 04/09/2026 14:50
reason: clear transferable title: business support assistant
source_job_id: 300531
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Assistant_Family_Hubs/300531
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Newcastle upon Tyne | £26,403- £27,254 per annum, pro-rata | Business Support Officer
employer: Newcastle City Council
closing_date: 04/09/2026 22:59
reason: clear transferable title: business support officer
source_job_id: 300710
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Officer/300710
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Newcastle upon Tyne | £26,403 - £27,254 per annum (£14,714 - £15,188 actual salary) | Customer Service Assistant
employer: Newcastle City Council
closing_date: 31/08/2026 22:59
reason: clear transferable title: customer service assistant
source_job_id: 300896
source_url: https://www.northeastjobs.org.uk/job/Customer_Service_Assistant/300896
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Longbenton High School Hailsham Ave, Newcastle upon Tyne NE12 8ER | £24,551 | DBS01122/26 - Business Administrator Apprentice - Longbenton High School
employer: North Tyneside Council
closing_date: 14/09/2026 12:00
reason: clear transferable title: administrator
source_job_id: 300866
source_url: https://www.northeastjobs.org.uk/job/DBS01122_26_Business_Administrator_Apprentice_Longbenton_High_School/300866
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | North Tyneside Council (derived for filtering) | £25,583 - £25,989 pro rata | DBS01125/26 - Receptionist - Norham High School
employer: North Tyneside Council
closing_date: 15/09/2026 12:00
reason: clear transferable title: receptionist
source_job_id: 301184
source_url: https://www.northeastjobs.org.uk/job/DBS01125_26_Receptionist_Norham_High_School/301184
---
## POSS — choose SELECT or EXCLUDE

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Sacriston | £24,796 - £25,185 (Pro Rata) | Administrative Assistant
employer: Durham County Council
closing_date: 31/08/2026
reason: possible JobG8 duplicate requires review
source_job_id: 299277
source_url: https://www.northeastjobs.org.uk/job/Administrative_Assistant/299277
---
---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | The Horizon School, CETL, Brierton Lane, Hartlepool | Band 7 £23,175 - £24,314 pa | Attendance & Support Officer
employer: Hartlepool Borough Council
closing_date: 04/09/2026 12:00
reason: transferable office/service title with specialist or borderline wording: attendance
source_job_id: 299877
source_url: https://www.northeastjobs.org.uk/job/Attendance_Support_Officer/299877
---
---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Annand House, Meadowfield | Grade 6 - £28,142- £31,022 (Pay award pending) | Business Services Co-ordination and Improvement Officer
employer: Durham County Council
closing_date: 06/09/2026
reason: annualised upper salary £31,022 exceeds North East review point £30,000
source_job_id: 300776
source_url: https://www.northeastjobs.org.uk/job/Business_Services_Co_ordination_and_Improvement_Officer/300776
---
---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | County Durham | £24,305.00 - £26,325.00 | Marketing & Events Assistant
employer: Connect Multi-Academy Trust
closing_date: 07/09/2026 12:00
reason: provisional transferable-office review
source_job_id: 300955
source_url: https://www.northeastjobs.org.uk/job/Marketing_Events_Assistant/300955
---
---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Town Hall, Darlington | £25,989 per annum (pay award pending) | PA Support Officer
employer: Darlington Borough Council
closing_date: 07/09/2026
reason: provisional transferable-office review
source_job_id: 300972
source_url: https://www.northeastjobs.org.uk/job/PA_Support_Officer/300972
---
---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Durham (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256127
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256127
---
---
action: exclude
POSS | North East - County Durham & Darlington/Hartlepool | Town Hall, Darlington | £39,152 - £41,771 per annum | Systems Administrator (Housing Services)
employer: Darlington Borough Council
closing_date: 31/08/2026
reason: transferable office/service title with specialist or borderline wording: housing
source_job_id: 300336
source_url: https://www.northeastjobs.org.uk/job/Systems_Administrator_Housing_Services/300336
---
---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Council Offices, Green Lane, Spennymoor | £30,024 to £33,699 p.a. (Grade 7) Pay Award pending | Technical and Support Officers
employer: Durham County Council
closing_date: 31/08/2026
reason: transferable office/service title with specialist or borderline wording: technical
source_job_id: 300579
source_url: https://www.northeastjobs.org.uk/job/Technical_and_Support_Officers/300579
---
---
action: exclude
POSS | North East - County Durham & Darlington/Hartlepool | Peterlee Depot (North) or Chilton Depot (South) | £29,071 - £32,046 | Waste Operations Support Officers
employer: Durham County Council
closing_date: 09/09/2026
reason: annualised upper salary £32,046 exceeds North East review point £30,000
source_job_id: 301232
source_url: https://www.northeastjobs.org.uk/job/Waste_Operations_Support_Officers/301232
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £29,540 - £32,061 | Annual Review Officer (SEND)
employer: Gateshead Council
closing_date: 10/09/2026
reason: transferable office/service title with specialist or borderline wording: send
source_job_id: 301235
source_url: https://www.northeastjobs.org.uk/job/Annual_Review_Officer_SEND/301235
---
---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle (derived for filtering) | Actual pro-rata salary is £27,703 - £29,601 per annum (pay award pending) | Attendance Officer
employer: North East Futures - UTC
closing_date: 08/09/2026 12:00
reason: transferable office/service title with specialist or borderline wording: attendance
source_job_id: 300632
source_url: https://www.northeastjobs.org.uk/job/Attendance_Officer/300632
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Culture House | Grade 4 (SCP 12 - 17) £28,598 - £31,022 pro rata | Digital Systems Administrator
employer: Sunderland City Council
closing_date: 02/09/2026
reason: annualised upper salary £31,022 exceeds North East review point £30,000
source_job_id: 300715
source_url: https://www.northeastjobs.org.uk/job/Digital_Systems_Administrator/300715
---
---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Sunderland (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256126
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256126
---
---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | School Administrators required, various roles available throughout South Tyneside (derived for filtering) | From £14.54 - £15.20per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256125
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256125
---
---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | School Administrators required, various roles available throughout Gateshead (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256124
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256124
---
---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256122
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256122
---
---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | North Tyneside (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256121
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256121
---
---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Northumberland (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256120
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256120
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Adult Social Care, Support Coordination Team, Town Hall and Civic Offices | £33,699 pa | Senior Support Coordinator
employer: South Tyneside Council
closing_date: 11/09/2026 12:00
reason: transferable office/service title with specialist or borderline wording: senior
source_job_id: 301056
source_url: https://www.northeastjobs.org.uk/job/Senior_Support_Coordinator/301056
---
---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £41,771 - £45,091 | Simpler Recycling Projects Coordinator
employer: Gateshead Council
closing_date: 06/09/2026
reason: annualised upper salary £45,091 exceeds North East review point £30,000
source_job_id: 300777
source_url: https://www.northeastjobs.org.uk/job/Simpler_Recycling_Projects_Coordinator/300777
---
---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Eddie Ferguson House, Blyth, United Kingdom | £32,578 - £35,570 | Tenant Engagement Officer
employer: Northumberland County Council
closing_date: 20/09/2026
reason: annualised upper salary £35,570 exceeds North East review point £30,000
source_job_id: 301243
source_url: https://www.northeastjobs.org.uk/job/Tenant_Engagement_Officer/301243
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £32,061 to £ 33,699 per annum + benefits (pay award pending) | Trauma Support Coordinator
employer: Tyne and Wear Fire and Rescue Service
closing_date: 02/09/2026 12:00
reason: annualised upper salary £33,699 exceeds North East review point £30,000
source_job_id: 301015
source_url: https://www.northeastjobs.org.uk/job/Trauma_Support_Coordinator/301015
---
## EXCLUDED BY REVIEW

- None.

## Hard passes

- [Apprenticeship Skills Coordinator - Technical Construction & Civil Engineering](https://www.northeastjobs.org.uk/job/Apprenticeship_Skills_Coordinator_Technical_Construction_Civil_Engineering/301194) — out-of-scope occupation: engineer.
- [Highways Technical Support Officer (INTERNAL ONLY)](https://www.northeastjobs.org.uk/job/Highways_Technical_Support_Officer_INTERNAL_ONLY/301268) — not open to external applicants.

## Safety boundary

- A normal run is review-only and writes no publishable JSON.
- Approved JSON requires an explicit PUBLISH confirmation and an exact same-day review-set match.
- Only factual vacancy fields are retained; full descriptions are not stored.
- Public role overviews are original Ontap text assembled from those factual fields.
- Detail pages are fetched only after a provisional title/teaser screen.
- North East Jobs terms require written permission for commercial reuse of site material.
- The source had no retrievable robots.txt (404) when the POC was designed.
- HC/POSS rules are provisional and do not amend Ontap's permanent selection policy.

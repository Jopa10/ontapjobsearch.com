# North East Jobs ETL proof-of-concept review

review_date: 2026-09-05
review_fingerprint: f64d7a6c46aded6c8af2bea4fb807bb13d293357cedb7b7b2a6683d1ee0df9aa

Edit only the `action:` line in each editable block:

- For a POSS job, use `action: select` to add it or `action: exclude` to reject it.
- For a selected HC job, use `action: exclude` to remove it.
- Leave `action:` blank for no change.
- Commit the edit; the review workflow will remember the decision.
- Decisions are carried forward only while the same vacancy review facts remain unchanged.

Run generated: 2026-09-05T11:34:55+01:00
RSS input: https://www.northeastjobs.org.uk/RSSJobs.aspx?orgid=62
JobG8 comparison rows in target geographies: 275

## Funnel

- RSS vacancies read: 594
- Hard-pass title/teaser screen before detail requests: 550
- Detail candidates: 44
- Detail failures or unavailable snapshots: 0
- Outside the two target geographies: 5
- Tees Valley explicitly excluded: 10
- Target-geography candidates reviewed: 29

## Detail diagnostics

- No unresolved detail-page failures.

## Review outcomes

- HC: 12
- POSS: 15
- Hard pass: 2
- Final selected after remembered/manual actions: 18
- Final POSS awaiting decision: 1
- Manually excluded: 8
- Confirmed JobG8 duplicates: 0
- Possible JobG8 duplicates: 0
- Likely unique to North East Jobs: 29
- Rows in possible within-source duplicate groups: 0

- Manual review warning: manual review date 2026-09-04 is not 2026-09-05; old actions ignored

## SELECTED

---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Age UK County Durham (derived for filtering) | £24,454 per annum, pro rata (£14,870.70) + pension contribution generous holidays | Administrator
employer: Age UK County Durham
closing_date: 30/09/2026 12:00
reason: clear transferable title: administrator
source_job_id: 301544
source_url: https://www.northeastjobs.org.uk/job/Administrator/301544
---
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
SELECTED | North East - County Durham & Darlington/Hartlepool | Corten House, Durham | Grade 4 (£26,427 - £27,709) | Passenger Transport Administration Assistant
employer: Durham County Council
closing_date: 16/09/2026
reason: clear transferable title: administration assistant
source_job_id: 301481
source_url: https://www.northeastjobs.org.uk/job/Passenger_Transport_Administration_Assistant/301481
---
---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Age UK County Durham (derived for filtering) | £24,454 per annum, pro rata (£14,870.70) + pension contribution generous holidays | Project Administrator
employer: Age UK County Durham
closing_date: 30/09/2026 12:00
reason: clear transferable title: administrator
source_job_id: 301543
source_url: https://www.northeastjobs.org.uk/job/Project_Administrator/301543
---
---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Spennymoor, DL16 7JB | £26,403 - £28,598 pro rata (pay award pending) | School Secretary
employer: Durham County Council
closing_date: 21/09/2026 12:00
reason: clear transferable title: secretary
source_job_id: 301524
source_url: https://www.northeastjobs.org.uk/job/School_Secretary/301524
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Sir Charles Parsons School, Westbourne Avenue, Walker, Newcastle upon Tyne, NE6 4ED | £27,274 - £28,153 per annum pro rata (Actual salary £22,786 - £23,520 per annum) | Administration Assistant Level 3
employer: Newcastle City Council
closing_date: 18/09/2026 12:00
reason: clear transferable title: administration assistant
source_job_id: 301513
source_url: https://www.northeastjobs.org.uk/job/Administration_Assistant_Level_3/301513
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Lemington Riverside, Rokeby Street, Newcastle upon Tyne, NE15 8RR | £25,185 per annum pro rata (Actual salary £21,187 per annum) | Administrative Assistant - Level 1
employer: Newcastle City Council
closing_date: 25/09/2026 12:00
reason: clear transferable title: administrative assistant
source_job_id: 301338
source_url: https://www.northeastjobs.org.uk/job/Administrative_Assistant_Level_1/301338
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
SELECTED | North East - Tyneside, Wearside & Northumberland | Sunderland | £26,427 - £26,847 per annum pro rata | Business Support Assistant - Children's Social Care
employer: Together for Children - Sunderland
closing_date: 20/09/2026
reason: clear transferable title: business support assistant
source_job_id: 301377
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Assistant_Children_s_Social_Care/301377
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | South Tyneside Council (derived for filtering) | £29,542 pa | Customer Service Advisor x 2 Posts
employer: South Tyneside Council
closing_date: 17/09/2026 12:00
reason: clear transferable title: customer service advisor
source_job_id: 301438
source_url: https://www.northeastjobs.org.uk/job/Customer_Service_Advisor_x_2_Posts/301438
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
action:
POSS | North East - County Durham & Darlington/Hartlepool | New College Durham - Framwellgate Moor | Support Grade F02 - F03; £32,012 to £32,975 per annum | Personal Development Coach Coordinator
employer: New College Durham
closing_date: 20/09/2026
reason: annualised upper salary £32,975 exceeds North East review point £30,000
source_job_id: 301004
source_url: https://www.northeastjobs.org.uk/job/Personal_Development_Coach_Coordinator/301004
---
---
action: exclude
POSS | North East - County Durham & Darlington/Hartlepool | Civic Centre, Hartlepool | £47,665 - £51,928 per annum | Practice Development Coordinator
employer: Hartlepool Borough Council
closing_date: 21/09/2026 12:00
reason: annualised upper salary £51,928 exceeds North East review point £30,000
source_job_id: 301368
source_url: https://www.northeastjobs.org.uk/job/Practice_Development_Coordinator/301368
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
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Sunderland City Council (derived for filtering) | Grade 5 (SCP 17-22) £31,022 - £33,699 | Active Sunderland Weight Management Support Officer
employer: Sunderland City Council
closing_date: 14/09/2026
reason: annualised upper salary £33,699 exceeds North East review point £30,000
source_job_id: 301079
source_url: https://www.northeastjobs.org.uk/job/Active_Sunderland_Weight_Management_Support_Officer/301079
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £30,515 - £33,119 | Annual Review Officer (SEND)
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
POSS | North East - Tyneside, Wearside & Northumberland | Kyloe House, Stannington, United Kingdom | £25,485.96 - £27,646.17 (equated salary quoted) | Behaviour Support Officer - Kyloe House
employer: Northumberland County Council
closing_date: 17/09/2026 00:00
reason: provisional transferable-office review
source_job_id: 301477
source_url: https://www.northeastjobs.org.uk/job/Behaviour_Support_Officer_Kyloe_House/301477
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Sunderland City Council (derived for filtering) | Grade 5 (SCP 17-22) £31,022 - £33,699 | Driving Assessment Officer
employer: Sunderland City Council
closing_date: 14/09/2026
reason: annualised upper salary £33,699 exceeds North East review point £30,000
source_job_id: 301282
source_url: https://www.northeastjobs.org.uk/job/Driving_Assessment_Officer/301282
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Sunderland City Council (derived for filtering) | 4 (SCP 12 - 17) £28,598 - £31,022 | Environmental Enforcement Support Officer
employer: Sunderland City Council
closing_date: 16/09/2026
reason: annualised upper salary £31,022 exceeds North East review point £30,000
source_job_id: 301401
source_url: https://www.northeastjobs.org.uk/job/Environmental_Enforcement_Support_Officer/301401
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
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £43,149 - £46,579 | Simpler Recycling Projects Coordinator
employer: Gateshead Council
closing_date: 08/09/2026
reason: annualised upper salary £46,579 exceeds North East review point £30,000
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

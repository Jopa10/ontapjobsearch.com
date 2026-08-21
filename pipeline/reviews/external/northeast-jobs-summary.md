# North East Jobs ETL proof-of-concept review

review_date: 2026-08-21
review_fingerprint: c6b4aca31483a6883975e791c1496f09afb1790426bbdf541331172e07bc0cc0

Edit only the `action:` line in each editable block:

- For a POSS job, use `action: select` to add it or `action: exclude` to reject it.
- For a selected HC job, use `action: exclude` to remove it.
- Leave `action:` blank for no change.
- Commit the edit; the review workflow will remember the decision.
- Decisions are carried forward only while the same vacancy review facts remain unchanged.

Run generated: 2026-08-21T08:09:10+01:00
RSS input: https://www.northeastjobs.org.uk/RSSJobs.aspx?orgid=62
JobG8 comparison rows in target geographies: 293

## Funnel

- RSS vacancies read: 688
- Hard-pass title/teaser screen before detail requests: 635
- Detail candidates: 53
- Detail failures or unavailable snapshots: 0
- Outside the two target geographies: 4
- Tees Valley explicitly excluded: 10
- Target-geography candidates reviewed: 39

## Detail diagnostics

- No unresolved detail-page failures.

## Review outcomes

- HC: 9
- POSS: 30
- Hard pass: 0
- Final selected after remembered/manual actions: 31
- Final POSS awaiting decision: 3
- Manually excluded: 5
- Confirmed JobG8 duplicates: 0
- Possible JobG8 duplicates: 4
- Likely unique to North East Jobs: 35
- Rows in possible within-source duplicate groups: 0

- Manual review warning: manual review date 2026-08-20 is not 2026-08-21; old actions ignored

## SELECTED

---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Framwellgate Moor | Support Grade B; £26,970 per annum | Administrator
employer: New College Durham
closing_date: 26/08/2026
reason: clear transferable title: administrator
source_job_id: 300512
source_url: https://www.northeastjobs.org.uk/job/Administrator/300512
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | North Tyneside | Grade 05 (£26,403 - £27,254) pro rata per annum | Admin Assistant
employer: North Tyneside Council
closing_date: 27/08/2026 00:00
reason: clear transferable title: admin assistant
source_job_id: 300537
source_url: https://www.northeastjobs.org.uk/job/Admin_Assistant/300537
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Berwick, United Kingdom | £13.26 | Admin Assistant - Staff Bank (Berwick)
employer: Northumberland County Council
closing_date: 23/08/2026 00:00
reason: clear transferable title: admin assistant
source_job_id: 300726
source_url: https://www.northeastjobs.org.uk/job/Admin_Assistant_Staff_Bank_Berwick/300726
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
source_job_id: 301018
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Assistant/301018
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
SELECTED | North East - Tyneside, Wearside & Northumberland | Newcastle upon Tyne | £26,403- £27,254 per annum, pro-rata | Business Support Officer
employer: Newcastle City Council
closing_date: 04/09/2026 22:59
reason: clear transferable title: business support officer
source_job_id: 300710
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Officer/300710
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Hazlewood Community Primary School, Canterbury Way, Wideopen, Newcastle upon Tyne | £21,683 - £22,421 | DBS01116/26 - Admin Assistant - Hazlewood Community Primary School
employer: North Tyneside Council
closing_date: 21/08/2026 12:00
reason: clear transferable title: admin assistant
source_job_id: 299761
source_url: https://www.northeastjobs.org.uk/job/DBS01116_26_Admin_Assistant_Hazlewood_Community_Primary_School/299761
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
## POSS — choose SELECT or EXCLUDE

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Bishop Auckland | £26,403 to £28,598 pro rata (pending pay award) | Admin Assistant – Finance/HR
employer: Durham County Council
closing_date: 28/08/2026 12:00
reason: transferable office/service title with specialist or borderline wording: finance, hr
source_job_id: 300742
source_url: https://www.northeastjobs.org.uk/job/Admin_Assistant_Finance_HR/300742
---
---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | CETL | £25,989 - £26,403 per annum | Administration Assistant
employer: Hartlepool Borough Council
closing_date: 21/08/2026
reason: possible JobG8 duplicate requires review
source_job_id: 300212
source_url: https://www.northeastjobs.org.uk/job/Administration_Assistant/300212
---
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
POSS | North East - County Durham & Darlington/Hartlepool | Framwellgate Moor Campus, Durham, DH1 5ES | Support Grade D; £28,980 per annum | Apprenticeship Support Officer
employer: New College Durham
closing_date: 26/08/2026
reason: provisional transferable-office review
source_job_id: 300505
source_url: https://www.northeastjobs.org.uk/job/Apprenticeship_Support_Officer/300505
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
POSS | North East - County Durham & Darlington/Hartlepool | Highlight Active Wellbeing Hub | £13.47 per hour | Customer Service Advisor
employer: Hartlepool Borough Council
closing_date: 31/08/2026
reason: possible JobG8 duplicate requires review
source_job_id: 299796
source_url: https://www.northeastjobs.org.uk/job/Customer_Service_Advisor/299796
---
---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Barnard Castle | £27,128.40 | Facilities Coordinator
employer: The Bowes Museum
closing_date: 24/08/2026 08:00
reason: transferable office/service title with specialist or borderline wording: facilities
source_job_id: 300105
source_url: https://www.northeastjobs.org.uk/job/Facilities_Coordinator/300105
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
closing_date: 31/08/2026
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
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Prudhoe | SCP 2 - 5 (£24,413 - £25,583 (pro rata) depending upon qualifications and experience | Administrative Assistant
employer: Prudhoe Town Council
closing_date: 04/09/2026 12:00
reason: possible JobG8 duplicate requires review
source_job_id: 300646
source_url: https://www.northeastjobs.org.uk/job/Administrative_Assistant/300646
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
POSS | North East - Tyneside, Wearside & Northumberland | North Tyneside | GRADE 5 SCP 7 (£26,403) - SCP 9 (£27,254) per annum | Claims Support Officer
employer: North Tyneside Council
closing_date: 28/08/2026 00:00
reason: provisional transferable-office review
source_job_id: 300592
source_url: https://www.northeastjobs.org.uk/job/Claims_Support_Officer/300592
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle Upon Tyne | SCP 23-25, FTE salary (£34,434.00 - £36,363.00) | Data and Exams Officer
employer: Walbottle Academy
closing_date: 24/08/2026 09:00
reason: annualised upper salary £36,363 exceeds North East review point £30,000
source_job_id: 300012
source_url: https://www.northeastjobs.org.uk/job/Data_and_Exams_Officer/300012
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
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Sunderland City Council (derived for filtering) | Grade 5 (SCP 17-22) £31,022.00-£33,699.00 | Driving Assessment Officer
employer: Sunderland City Council
closing_date: 27/08/2026
reason: annualised upper salary £33,699 exceeds North East review point £30,000
source_job_id: 300450
source_url: https://www.northeastjobs.org.uk/job/Driving_Assessment_Officer/300450
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Adult Social Care, South Tyneside | £41,771 pa | Local Area Coordinator – Primrose
employer: South Tyneside Council
closing_date: 28/08/2026 12:00
reason: annualised upper salary £41,771 exceeds North East review point £30,000
source_job_id: 299943
source_url: https://www.northeastjobs.org.uk/job/Local_Area_Coordinator_Primrose/299943
---
---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Various Locations | £25,989 pa pro rata (£13.47 per hour) | Receptionist – Various Posts
employer: South Tyneside Council
closing_date: 25/08/2026 12:00
reason: annualised upper salary £50,678,550 exceeds North East review point £30,000
source_job_id: 300662
source_url: https://www.northeastjobs.org.uk/job/Receptionist_Various_Posts/300662
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
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256122
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256122
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
POSS | North East - Tyneside, Wearside & Northumberland | School Administrators required, various roles available throughout South Tyneside (derived for filtering) | From £14.54 - £15.20per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256125
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256125
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
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £41,771 - £45,091 | Simpler Recycling Projects Coordinator
employer: Gateshead Council
closing_date: 06/09/2026
reason: annualised upper salary £45,091 exceeds North East review point £30,000
source_job_id: 300777
source_url: https://www.northeastjobs.org.uk/job/Simpler_Recycling_Projects_Coordinator/300777
---
---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Town Hall, South Shields | £28,598 pa | Technical Support Officer – Licensing
employer: South Tyneside Council
closing_date: 24/08/2026 12:00
reason: transferable office/service title with specialist or borderline wording: technical
source_job_id: 300614
source_url: https://www.northeastjobs.org.uk/job/Technical_Support_Officer_Licensing/300614
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

- None after geography and deduplication checks.

## Safety boundary

- A normal run is review-only and writes no publishable JSON.
- Approved JSON requires an explicit PUBLISH confirmation and an exact same-day review-set match.
- Only factual vacancy fields are retained; full descriptions are not stored.
- Public role overviews are original Ontap text assembled from those factual fields.
- Detail pages are fetched only after a provisional title/teaser screen.
- North East Jobs terms require written permission for commercial reuse of site material.
- The source had no retrievable robots.txt (404) when the POC was designed.
- HC/POSS rules are provisional and do not amend Ontap's permanent selection policy.

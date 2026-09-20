# Worcester admin and office jobs city-page review

- Parent regional page: `app/_city-pages/configured-slices/worcestershire/service-administrator-jobs.json`
- Live route: `/worcester/service-administrator-jobs`
- Mode: `publish`
- Minimum live-job threshold: 4
- Effective included jobs: 1
- Threshold currently met: no

## How to review
Edit only the `action:` line inside a job block.
Use `action: exclude` to remove a current include, or `action: select` to include a review/exclude job.
Leave `action:` blank to accept the automatic decision. A blank review remains omitted from the live page.
Jobs are grouped include first, review second and exclude last, then alphabetically by title.
JobG8 identifiers are prefixed `jobg8-` in review files only; live job IDs are unchanged.

## Counts
- automatic include: 1
- automatic review: 5
- automatic exclude: 0
- effective include: 1
- effective review: 5
- effective exclude: 0

## INCLUDE (1)

---
action: 
decision: include
automatic_decision: include
title: Exams Officer
company: Tudor Grange Academy Worcester
location: Worcester
source: Teaching Vacancies
job_id: teaching-vacancies-exams-officer-bce7ec54-a91f-4508-abf1-303d3191a779
reason: Exact approved Worcester workplace.
---

## REVIEW (5)

---
action: 
decision: review
automatic_decision: review
title: Administrative Assistant and Attendance
company: Walkwood Church of England Middle School
location: Redditch
source: Teaching Vacancies
job_id: teaching-vacancies-administrative-assistant-and-attendance
reason: No exact Worcester workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Administrator
company: Herefordshire and Worcestershire Health and Care NHS Trust
location: Droitwich, WR9 8RD
source: NHS Jobs
job_id: nhs-5604564
reason: No exact Worcester workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Administrator (SEND Department)
company: Tenbury High Ormiston Academy
location: Tenbury Wells
source: Teaching Vacancies
job_id: teaching-vacancies-administrator-send-department-tenbury-high-ormiston-academy
reason: No exact Worcester workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Group HR Co-ordinator
company: James Andrew Recruitment Solutions (JAR Solutions) - Agency - Permanent
location: Redditch
source: JobG8
job_id: jobg8-1928891
reason: No exact Worcester workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Onboarding Coordinator
company: Davies Group - Agency - Permanent
location: Worcestershire
source: JobG8
job_id: jobg8-1879674
reason: No exact Worcester workplace matched; local geographic review is required.
---

## EXCLUDE (0)

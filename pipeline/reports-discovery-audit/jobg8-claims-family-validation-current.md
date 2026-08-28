# JobG8 Claims Support family validation

Feed: **2026-08-28.xlsx**
Jobs in feed: **10,000**
Broad insurance/claims universe: **92** raw rows
IN after advert-level boundary rules: **10** raw rows
BORDERLINE: **0** raw rows
OUT: **82** raw rows
Content-unique IN jobs: **10** (removed **0** exact-content duplicate rows)

Diagnostic only: no LIVE slice, publishing rule or production family status is changed.

## Boundary now being tested

- IN: claims handlers, claims administrators/clerks/advisers/technicians and clearly claims-led customer/admin support.
- IN: senior claims handlers remain eligible when the advert is ordinary claims ownership and the salary is within scope.
- OUT: general insurance broking/account-handler/account-executive/sales roles.
- OUT: loss/claims adjusters, Lloyd's-market adjuster work, lawyers/solicitors, managers/team leaders and large/major-loss specialists.
- OUT: annualised salary maximum **over £50,000**. Exactly £50,000 is not excluded by salary alone.
- Legal-expenses/pre-litigation claims handling can remain IN; substantively litigated/legal file-handling is OUT.

## Decision breakdown

| Decision | Raw rows |
|---|---:|
| IN | 10 |
| BORDERLINE | 0 |
| OUT | 82 |

## Content-unique IN regional shape

| Jobs | Ontap region |
|---:|---|
| 2 | Kent |
| 2 | Staffordshire |
| 1 | Bristol & Bath |
| 1 | Oxfordshire |
| 1 | Norfolk |
| 1 | Northamptonshire |

## JobG8 classifications feeding content-unique IN jobs

| Jobs | JobG8 classification |
|---:|---|
| 3 | Insurance & Superannuation |
| 2 | Administration |
| 2 | Call Centre / CustomerService |
| 2 | Legal |
| 1 | Accounting |

## Recurring content-unique IN titles

| Jobs | Title |
|---:|---|
| 3 | Claims Handler |
| 1 | Insurance Administrator Friendly team + 25 days A/L |
| 1 | Legal Expenses Claims Handler |
| 1 | Insurance Coordinator |
| 1 | Senior Customer Service Adviser |
| 1 | Claims Administrator |
| 1 | Motor Claims Handler |
| 1 | Employer Liability and Public Liability Claims Handler (6 - Month FTC) |

## Salary guard check

Content-unique IN jobs with usable annualised maximum: **7**.
IN jobs still over £50k: **0** (must be zero).

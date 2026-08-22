# JobG8 Claims Support family validation

Feed: **2026-08-22.xlsx**
Jobs in feed: **10,000**
Broad insurance/claims universe: **184** raw rows
IN after advert-level boundary rules: **29** raw rows
BORDERLINE: **4** raw rows
OUT: **151** raw rows
Content-unique IN jobs: **29** (removed **0** exact-content duplicate rows)

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
| IN | 29 |
| BORDERLINE | 4 |
| OUT | 151 |

## Content-unique IN regional shape

| Jobs | Ontap region |
|---:|---|
| 6 | Merseyside - Liverpool |
| 3 | Staffordshire |
| 3 | Yorkshire - West |
| 3 | Bristol & Bath |
| 2 | Norfolk |
| 2 | Kent |
| 2 | Northamptonshire |
| 2 | Oxfordshire |
| 1 | Leicestershire |
| 1 | Cambridgeshire |
| 1 | Essex |
| 1 | Buckinghamshire |
| 1 | Gloucestershire |

## JobG8 classifications feeding content-unique IN jobs

| Jobs | JobG8 classification |
|---:|---|
| 22 | Insurance & Superannuation |
| 3 | Call Centre / CustomerService |
| 2 | Administration |
| 1 | Legal |
| 1 | Accounting |

## Recurring content-unique IN titles

| Jobs | Title |
|---:|---|
| 5 | Claims Handler |
| 2 | Senior Claims Handler |
| 2 | Legal Expenses Claims Handler |
| 1 | Experienced Motor Claims Handler |
| 1 | Third-Party Capture Claims Handler |
| 1 | Insurance Administrator Friendly team + 25 days A/L |
| 1 | Employer Liability and Public Liability Claims Handler (6 - Month FTC) |
| 1 | SENIOR MOTOR CLAIMS HANDLER -INTERVENTION |
| 1 | Claims Handler - Defendant Personal Injury (EL/PL) |
| 1 | Insurance Claims Advisor |
| 1 | EL/PL Claims Handler |
| 1 | Motor Claims Handler CH3 |
| 1 | Recoveries claims handler |
| 1 | Motor Claims Handler |
| 1 | Customer Service Advisor |
| 1 | Travel Claims Handler |
| 1 | Insurance Coordinator |
| 1 | Claims Handler CH1 |
| 1 | Senior Customer Service Adviser |
| 1 | Technical Claims Advisor |
| 1 | Motor claims handler |
| 1 | Experience Insurance Claims Clerk |
| 1 | Claims Administrator |

## Salary guard check

Content-unique IN jobs with usable annualised maximum: **19**.
IN jobs still over £50k: **0** (must be zero).

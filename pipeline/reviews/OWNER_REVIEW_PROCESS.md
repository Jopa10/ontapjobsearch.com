# Approved owner job-review process

Approved by John Bacon on 24 October 2026; confirmed and used on 26 October 2026.
This is the single maintained authority for the owner review presentation and response process. Read it before preparing any future review. Update this document in place only when the owner agrees a change; do not invent a new layout from chat memory.

## Preserve the approved Excel format

Use one Excel worksheet named Review, containing one continuous numbered list of undecided jobs. Retain the approved layout, column order, formatting, filters and frozen heading rows. Do not redesign, reorder, add or remove columns, or split the list into region/family tabs unless the owner requests it.

The accepted 26 October workbook is the reference example:
[Ontap-Review-2026-10-26.xlsx](https://chatgpt.com/library?file_id=libfile_eedea3bc27388191b419aede0a6a75fd&account_id=personal).

Columns in the approved workbook, in order:
1. Review No.
2. Job title
3. Location
4. Salary
5. Source
6. Reason for review
7. Region
8. Source job ID
9. Fingerprint

The first six columns are the primary owner view. Region and the two source identifiers preserve context and safe application of decisions. Keep the reason brief and factual; show missing salary as Not stated. Never infer part-time status or pay merely from a job title.

Above the table, state the review date, undecided count, source coverage and the response instruction. Exclude previously answered jobs from the undecided list and state their count separately. Clearly label a partial-source snapshot; a stale or missing source is not zero inventory.

## Fixed numbering and mapping

Review No. is a fixed integer value starting at 1, never a ROW formula. It must remain attached to the same source/job ID/fingerprint after sorting. Excel physical row numbers are not review numbers. Preserve the numbered snapshot and mapping for subsequent decisions; do not regenerate or renumber that issued list while the owner is responding.

## Owner response and application

The owner replies, for example: "Exclude 2, 4, 34; select the rest."
Only after that explicit instruction, exclude the named Review No. values and select the other undecided jobs in that exact issued snapshot. "Select all" selects that snapshot. Silence or failure to mention a job before the owner submits decisions is not approval.

Validate all numbers and source/job ID/fingerprint mappings against current review state before writing. Preserve existing decisions outside the snapshot. Do not apply old decisions to changed vacancies or silently expand approval to newly arrived jobs. Report any unmatched/changed jobs separately.

Use the existing master daily review and source fanout; do not create a parallel publication mechanism. Existing action: select/exclude and sel/exc remain supported. Explicit owner instructions override the default treatment of individual rows.

## Selection rules are a separate decision

Batch selections do not change automatic selection logic. Discuss proposed reusable rules with the owner and obtain agreement before implementing them. The 26 October approval of 103 jobs, including part-time Payroll/Finance Manager or Finance Lead opportunities, was a batch decision for assessing clicks, not a new blanket manager allowance. Accountant exclusions remain governed by the current selector rules.

## Publication and completion

Republish only when authorised. Use the existing Apply and publish Ontap daily review workflow and retain all existing source-isolation and publication-integrity safeguards. External-source failures must not block clean JobG8 inventory.

After the review is rebuilt, verify its actual unanswered count. Zero unanswered can coexist with answered rows still displayed; distinguish "0 awaiting a decision" from "0 total rows". Do not claim publication or deployment success merely because actions were saved or a workflow started. Respect an owner request not to chase deployment.

## Reuse instruction

"Prepare today's review using the approved process in the governance docs" means read this document and reuse the approved workbook format. No fresh design exercise is required.

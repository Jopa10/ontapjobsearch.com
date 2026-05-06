# Ontap JobG8 Pipeline

## Purpose

This pipeline converts raw JobG8 export files into validated Ontap JSON slice files for SSR-rendered job pages.

The process is designed to:
- maintain strict data consistency
- avoid fabricated values
- preserve full job descriptions
- enforce slice rules
- support daily manual publishing workflows

---

# Current Stable Version

Current known-good version:
`jobg8_pipeline_v7_working_2026-05-06.py`

Only promote a new version after successful:
- JSON generation
- validation checks
- render testing
- live page sanity review

---

# Pipeline Workflow

1. Download latest JobG8 export
2. Place source file into `/input`
3. Run Python pipeline
4. Review generated outputs
5. Check validation report
6. Upload approved JSON files
7. Verify live render on Ontap pages
8. Request indexing in Google Search Console if required

---

# Output Files

Typical outputs:
- west-yorkshire-support-worker.json
- south-yorkshire-support-worker.json
- validation-report.csv

---

# Core Slice Rules

## West Yorkshire
- target: 10–12 jobs
- Leeds-first ordering preferred
- support worker / care assistant family only
- no rows without apply_url

## South Yorkshire
- target: 6–10 jobs
- Sheffield-first ordering preferred
- same validation rules apply

---

# Data Rules

- Never fabricate values
- Preserve full job descriptions
- Clean encoding issues:
  - Â£ → £
  - malformed punctuation
- Prefer town/city locations
- Reject vague region-only locations
- Keep clean salary formatting
- Maintain exact schema ordering

---

# Validation Checklist

Before publish:
- correct job count
- no missing apply_url values
- salary rendering correct
- descriptions readable
- Leeds jobs prioritised
- JSON valid
- live render checked
- no duplicated jobs
- no wrong-region jobs

---

# Backup / Versioning Rules

- Never overwrite the last known-good script
- Keep dated working versions
- Store backups locally and on GitHub
- Only delete obsolete versions after newer versions are proven stable

---

# Future Expansion

Possible future additions:
- automated ingest
- scheduled validation
- multi-slice generation
- QA dashboards
- publish automation
- feed diff tracking

Do not add complexity until Phase-1 conversion/indexing signals justify it.

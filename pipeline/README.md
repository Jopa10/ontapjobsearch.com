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

---

# Compiler Module 1: Monthly Advertiser and Role Trends

Module 1 is an inspection report for archived monthly JobG8 supply. It does not publish live pages and does not modify the daily pipelines.

Default run:

```bash
python pipeline/scripts/jobg8_module_1_monthly_advertiser_report.py \
  --month 2026-06 \
  --input-dir pipeline/input-jobg8-archive/2026-06 \
  --output-dir pipeline/reports-module1 \
  --geo-lookup pipeline/geo/geo_lookup.xlsx \
  --registers-dir pipeline/registers
```

Authoritative inputs:
- `pipeline/input-jobg8-archive/<YYYY-MM>/` daily JobG8 Excel files
- `pipeline/geo/geo_lookup.xlsx`
- `pipeline/registers/*.csv`

Generated outputs:
- `pipeline/reports-module1/<YYYY-MM>-module1-advertiser-campaigns.csv`
- `pipeline/reports-module1/<YYYY-MM>-module1-role-trends.csv`

The role-trends report includes `top_advertiser_share_pct` as the only advertiser-concentration metric for now. Module 1 uses register-only title classification (`HIGH_CONFIDENCE` and `ELASTIC_FIT`) and has no local workstation path fallback or legacy `lookup.xlsx` discovery.

A manual GitHub Actions workflow, **Run Compiler Module 1**, can run the same report for a selected month and commit only the two Module 1 report outputs.

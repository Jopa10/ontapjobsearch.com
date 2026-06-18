# Geo Lookup Migration

## Scope

Branch/task scope: migrate the two live publishing pipelines to use `pipeline/geo/geo_lookup.xlsx` / `Sheet1` as the only `Area` -> `Cluster` mapping source:

- `pipeline/scripts/support_worker_pipeline.py`
- `pipeline/scripts/service_admin_pipeline.py`

The repository checkout used for this migration did **not** contain `pipeline/geo/geo_lookup.xlsx`, `pipeline/geo/lookup.xlsx`, or `pipeline/scripts/jobg8_feed_profiler_V3_2_register_based.py`. The code now fails fast when the authoritative workbook is missing, as required. Because the workbook was absent from this checkout, full successful pipeline execution and exact North East cluster inspection could not be completed locally.

## Files inspected

- Live pipelines:
  - `pipeline/scripts/support_worker_pipeline.py`
  - `pipeline/scripts/service_admin_pipeline.py`
- Every Python file under `pipeline/`:
  - `pipeline/jobg8_pipeline_v7_working_2026-05-06.py`
  - `pipeline/scripts/pandas.py`
  - `pipeline/scripts/support_worker_pipeline.py`
  - `pipeline/scripts/service_admin_pipeline.py`
  - `pipeline/scripts/geo_lookup.py` (new)
- GitHub Actions workflows:
  - `.github/workflows/run-full-jobg8-daily-process.yml`
  - `.github/workflows/run-service-admin-pipeline.yml`
  - `.github/workflows/run-support-worker-pipeline.yml`
- Geography workbook references found with `rg`.
- Hard-coded regional mappings and aliases in both live pipelines.
- Legacy snapshot pipeline `pipeline/jobg8_pipeline_v7_working_2026-05-06.py` was inspected as non-live legacy code and left unchanged.

## Files changed

- Added `pipeline/scripts/geo_lookup.py`.
- Updated `pipeline/scripts/support_worker_pipeline.py`.
- Updated `pipeline/scripts/service_admin_pipeline.py`.
- Added this migration note: `pipeline/GEO_LOOKUP_MIGRATION.md`.

## Obsolete workbook deletion

`pipeline/geo/lookup.xlsx` was not present and was not tracked in this checkout, so there was no obsolete workbook file to delete. No fallback, copy, rename, preservation, or comparison path was added.

## Old `lookup.xlsx` references removed

Active live-pipeline references to `pipeline/geo/lookup.xlsx` were removed from:

- `pipeline/scripts/support_worker_pipeline.py`
- `pipeline/scripts/service_admin_pipeline.py`

Remaining `lookup.xlsx` references, if any, are outside the migrated live scripts or in this documentation as historical notes.

## Sole mapping source

The sole live geography mapping source is now:

- Workbook: `pipeline/geo/geo_lookup.xlsx`
- Worksheet: `Sheet1`
- Required exact columns: `Area`, `Cluster`

Ignored workbook tabs for classification/publishing are not read by the shared loader.

## Shared loader behaviour

`pipeline/scripts/geo_lookup.py` now:

- Loads only `pipeline/geo/geo_lookup.xlsx`.
- Requires worksheet `Sheet1`.
- Requires exact columns `Area` and `Cluster`.
- Rejects a missing workbook.
- Rejects missing `Sheet1`.
- Rejects missing or renamed required columns.
- Rejects blank `Area` values.
- Rejects blank `Cluster` values.
- Detects duplicate normalized Areas mapped to conflicting exact Cluster values.
- Exposes `area_to_cluster`.
- Exposes `valid_clusters`.
- Emits `STOP:` errors designed to be clear in GitHub Actions logs.

No fallback to `lookup.xlsx` exists.

## Duplicated geography logic removed

Removed active live-pipeline regional alias dictionaries and cluster translation logic including old Yorkshire aliases, North East aliases/translations, Lancashire, Greater Manchester, Manchester, and Cumbria reinterpretation. Jobs whose Area is absent from the workbook remain unmapped and follow the existing reporting path; they are not assigned via aliases or town lists.

## Publishing configuration

Publishing configuration remains separate from the lookup workbook. It maps existing live output names to exact workbook Cluster values:

### Support worker

- West Yorkshire output: `Yorkshire - West`
- South Yorkshire output: `Yorkshire - South`

### Service admin

- West Yorkshire output: `Yorkshire - West`
- South Yorkshire output: `Yorkshire - South`
- Combined North East output currently configured to these existing exact cluster names from prior live configuration:
  - `North East - Tyneside, Wearside & Northumberland`
  - `North East - County Durham & Darlington/Hartlepool`
  - `North East - Tees Valley`

Because `pipeline/geo/geo_lookup.xlsx` was absent from this checkout, these North East names could not be re-confirmed against the new workbook locally. Startup validation will fail if any configured value is absent or obsolete.

## Startup validation added

Both live pipelines load and validate the shared geography configuration before processing job rows. They fail clearly when:

- `geo_lookup.xlsx` is missing.
- `Sheet1` is missing.
- `Area` or `Cluster` is missing.
- A lookup row has blank `Area` or `Cluster`.
- One normalized Area maps to conflicting exact Cluster values.
- A configured publishing Cluster is absent from the workbook.
- A configured publishing Cluster uses an obsolete alias or unknown value.

## Workflow findings

All workflows were inspected. No workflow path changes were required.

- Workflows already install `pandas` and `openpyxl`.
- The daily workflow runs from `pipeline` using:
  - `python -m scripts.service_admin_pipeline`
  - `python -m scripts.support_worker_pipeline`
- The daily workflow commits:
  - `pipeline/output-admin-service/*.json`
  - `pipeline/output-support-worker/*.json`
  - `pipeline/reports-daily`
- Artifact upload paths are preserved:
  - `pipeline/output-admin-service/`
  - `pipeline/output-support-worker/`
- No `.github/workflows/*.yml` file referenced `lookup.xlsx` or required migration.

## Commands used for tests and checks

- `find . -name AGENTS.md -print`
- `rg -n "lookup\.xlsx|geo_lookup\.xlsx|Yorkshire|North East|Lancashire|Cumbria|Cluster|Area|alias|normalis|normalize|town" pipeline .github/workflows -g '*.py' -g '*.yml' -g '*.yaml'`
- `find pipeline/geo -maxdepth 1 -type f -print`
- `git ls-files | rg 'lookup\.xlsx|geo_lookup\.xlsx' || true`
- `python -m py_compile pipeline/scripts/geo_lookup.py pipeline/scripts/support_worker_pipeline.py pipeline/scripts/service_admin_pipeline.py`
- `(cd pipeline && python -m scripts.service_admin_pipeline)`
- `(cd pipeline && PYTHONPATH=scripts python -m scripts.service_admin_pipeline)`
- `(cd pipeline && PYTHONPATH=scripts python -m scripts.support_worker_pipeline)`
- JSON/report inspection commands using Python `json` and `csv` modules.

## Pipeline test result

Full successful execution against `pipeline/input/Jobg8.xlsx` could not be completed in this checkout because `pipeline/geo/geo_lookup.xlsx` was absent. The updated startup validation correctly failed with:

```text
STOP: missing authoritative geography workbook: pipeline/geo/geo_lookup.xlsx
```

A plain module run also could not load `pandas` in this local container because network access to install packages was blocked and this environment lacks real `pandas`. GitHub Actions installs real `pandas` and `openpyxl`; local fallback testing used `PYTHONPATH=scripts` to expose the existing lightweight shim far enough to verify the missing-workbook failure.

## Before-and-after output comparison

Before-run checked-in output IDs were preserved by Git. Since the authoritative workbook is absent, no after-run outputs were generated, and no output files were modified.

| Output file | Before count | Before IDs | After count | Added IDs | Removed IDs | Explanation |
| --- | ---: | --- | ---: | --- | --- | --- |
| `pipeline/output-admin-service/west-yorkshire-admin-service.json` | 11 | `107241070`; `155ad04e-0dd2-4136-9720-a1a72144ecc6`; `4dfff604-ff55-4508-9cf4-a049ea862460`; `82ae9e09-447e-4f9b-ae9b-68474504990f`; `b6127a90-c08c-4010-9b17-081b893c6daa`; `c9ca3cfd-899c-4705-8d4e-084a4bda02f3`; `e18e7052-8c2b-48f7-b4ed-ba5c3a4f5278`; `201e220e-aa0a-422b-b756-19a810b1c8ec`; `ba59e49d-ab11-4637-ae56-7d0d787a942c`; `4daf9ef9-fe6d-4b4a-8e17-95ab7c8c3f68`; `107506827` | Not generated | Not generated | Not generated | Test blocked by missing authoritative workbook. |
| `pipeline/output-admin-service/south-yorkshire-admin-service.json` | 11 | `1f74cc6f-4e8b-458d-aeb6-f81b2d20ff31`; `6d141a8a-f55b-4e99-b930-7e97a4e0c326`; `98178ed7-801d-49d9-86c1-15def8995e52`; `8f194adc-4915-49ab-a454-d97355ec47c9`; `4499ecdd-06ff-4bf1-a429-db09e106917b`; `6cfd1576-3aa0-4156-b992-90e9d8fd9e49`; `d8ec77ff-1d1d-4723-9e52-90343c20eacc`; `316a637a-28b0-4ad0-a0ab-aca40781d90e`; `107425594`; `c1ef9a4d-533d-4ae8-b92a-041499009e4d`; `d1116cfc-c296-4c03-9f35-29c042182837` | Not generated | Not generated | Not generated | Test blocked by missing authoritative workbook. |
| `pipeline/output-admin-service/north-east-admin-service.json` | 6 | `94af153b-52b5-44ea-96e7-344f451c008b`; `963241c7-60ea-48cc-a8cb-6a367d4c2e40`; `507c7521-81a4-4ad5-8696-efa1945641b6`; `c8e62c68-317f-4c17-8b92-017a706f566a`; `40c401f3-5f4c-4934-867c-6fcbe4305085`; `3eecac21-b795-46e6-a5fe-31d39224dfae` | Not generated | Not generated | Not generated | Test blocked by missing authoritative workbook. |
| `pipeline/output-support-worker/west-yorkshire-support-worker.json` | 0 | none | Not generated | Not generated | Not generated | Test blocked by missing authoritative workbook. |
| `pipeline/output-support-worker/south-yorkshire-support-worker.json` | 0 | none | Not generated | Not generated | Not generated | Test blocked by missing authoritative workbook. |

## Filename and schema confirmation

Output filenames and directories were not changed in code:

- `pipeline/output-admin-service/west-yorkshire-admin-service.json`
- `pipeline/output-admin-service/south-yorkshire-admin-service.json`
- `pipeline/output-admin-service/north-east-admin-service.json`
- `pipeline/output-support-worker/west-yorkshire-support-worker.json`
- `pipeline/output-support-worker/south-yorkshire-support-worker.json`

Report filenames and directories were not changed in code:

- `pipeline/reports-daily/decision-report-admin-service.csv`
- `pipeline/reports-daily/validation-report-admin-service.csv`
- `pipeline/reports-daily/selection-summary-report-admin-service.csv`
- `pipeline/reports-daily/decision-report-support-worker.csv`
- `pipeline/reports-daily/validation-report-support-worker.csv`
- `pipeline/reports-daily/selection-summary-report-support-worker.csv`

Checked-in report schemas were inspected and not intentionally changed.

## Profiler legacy findings and future integration note

The requested profiler path `pipeline/scripts/jobg8_feed_profiler_V3_2_register_based.py` was not present in this checkout, so it could not be inspected directly. The non-live legacy snapshot `pipeline/jobg8_pipeline_v7_working_2026-05-06.py` still contains old duplicated geography logic, including old Yorkshire aliases and `build_lookup` Cluster remapping logic. It was not migrated, run, or deployed.

Future daily discovery profiler and monthly validation profiler work should import `scripts.geo_lookup`, use `pipeline/geo/geo_lookup.xlsx` / `Sheet1`, and emit publishing recommendations using exact workbook `Cluster` values only. Future profiler code must not maintain town lists, Area-to-region mappings, aliases, or fallback geography.

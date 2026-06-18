# Geo lookup migration test results

Date: 2026-06-18
Branch: `work`
Input file intended for live run: `pipeline/input/Jobg8.xlsx`
Geo lookup intended for verification: `pipeline/geo/geo_lookup.xlsx`

## Status

The requested live pipeline verification is **blocked in this task environment** because the environment cannot install the required real `pandas` and `openpyxl` dependencies from either PyPI or apt.

The pipelines were invoked only after attempting dependency installation, but they did not start because real `pandas` is not installed:

```text
ModuleNotFoundError: No module named 'pandas'
```

Because the two live pipelines did not complete successfully, no output or report artifacts were regenerated in this run, and no before/after selection comparison can be reported as a completed migration result.

## Commands attempted

```bash
python -m pip install --upgrade pandas openpyxl
```

Result: failed. The configured package proxy returned `403 Forbidden` for PyPI.

```bash
apt-get update && apt-get install -y python3-pandas python3-openpyxl
```

Result: failed. The configured package proxy returned `403 Forbidden` for Ubuntu apt repositories.

```bash
env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy python -m pip install pandas openpyxl
```

Result: failed. Direct PyPI access could not resolve `pypi.org` without the proxy.

```bash
python - <<'PY'
import sys
try:
 import pandas, openpyxl
 print('pandas', pandas.__version__, pandas.__file__)
 print('openpyxl', openpyxl.__version__, openpyxl.__file__)
except Exception as e:
 print(type(e).__name__, e)
 sys.exit(1)
PY
```

Result: failed. `pandas` is not installed.

```bash
cd pipeline && python -m scripts.service_admin_pipeline
```

Result: failed before pipeline execution with `ModuleNotFoundError: No module named 'pandas'`.

The support-worker command was not run after the dependency/import failure because it imports the same missing dependency at module import time.

## Requested verification checklist

| Check | Result |
| --- | --- |
| Service admin pipeline completes successfully | Blocked: missing real `pandas` |
| Support worker pipeline completes successfully | Blocked: missing real `pandas` |
| West Yorkshire uses `Yorkshire - West` | Not verified in a successful live run |
| South Yorkshire uses `Yorkshire - South` | Not verified in a successful live run |
| Combined North East output uses exact cluster names present in `geo_lookup.xlsx` | Not verified in a successful live run |
| Output filenames unchanged | Not verified by a successful live run |
| Report filenames unchanged | Not verified by a successful live run |
| Before/after selected job IDs for every output | Not available because outputs were not regenerated |
| Added or removed job IDs and why | Not available because outputs were not regenerated |
| Jobs lost solely because of geography migration | Not determinable because outputs were not regenerated |

## Next action needed

Run the requested commands in an environment where real `pandas` and `openpyxl` can be installed or are already available:

```bash
cd pipeline && python -m scripts.service_admin_pipeline
cd pipeline && python -m scripts.support_worker_pipeline
```

Then replace this blocked-run note with the successful pipeline results and the requested before/after job ID comparison.

"""Run the established service-admin pipeline with the approved Sussex slice enabled."""
from __future__ import annotations

from . import service_admin_pipeline as core
from . import service_admin_pipeline_education as education

core.REGION_MAP["sussex"] = "Sussex"
core.OUTPUT_FILES["Sussex"] = "sussex-admin-service.json"
core.PUBLISH_THRESHOLDS["Sussex"] = 6


def main() -> int:
    return education.main()


if __name__ == "__main__":
    raise SystemExit(main())

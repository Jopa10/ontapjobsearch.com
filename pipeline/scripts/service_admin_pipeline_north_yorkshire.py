"""Compatibility entry point for the config-driven live service-admin pipeline.

The daily workflow historically invokes this module. Keep that stable command
while moving region activation into the central slice register/catalog.
"""
from __future__ import annotations

from . import service_admin_pipeline_live_config as configured

# Compatibility exports retained for existing tests/callers.
live = configured.established
REGION = "Yorkshire - North"
ANCHOR_TOWN = "York"
OUTPUT_FILE = "north-yorkshire-admin-service.json"
load_anchor_towns = configured.load_anchor_towns
_manual_review_preview_rows = configured._manual_review_preview_rows
write_manual_review_markdown = configured.write_manual_review_markdown


def main() -> int:
    return configured.main()


if __name__ == "__main__":
    raise SystemExit(main())

"""Compatibility entry point for the config-driven verified publisher.

The workflow keeps its established command while the central slice register now
decides which additional verified destinations are active.
"""
from __future__ import annotations

from . import publish_verified_pages_live_config as configured

# Compatibility exports retained for existing tests/callers.
live = configured.established
NORTH_YORKSHIRE_MAPPING = configured.NORTH_YORKSHIRE_MAPPING


def main() -> int:
    return configured.main()


if __name__ == "__main__":
    raise SystemExit(main())

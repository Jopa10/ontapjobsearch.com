#!/usr/bin/env python3
"""Ontap Compiler Module 3: UK remote/work-from-home admin profiler."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
sys.path = [entry for entry in sys.path if Path(entry or ".").resolve() != SCRIPT_DIR]
sys.path.insert(0, str(REPO_ROOT))

from pipeline.module3.engine import parse_iso_date, run


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ontap Compiler Module 3 UK remote admin profiler.")
    parser.add_argument("--start-date", required=True, help="Inclusive date in YYYY-MM-DD format.")
    parser.add_argument("--end-date", required=True, help="Inclusive date in YYYY-MM-DD format.")
    parser.add_argument("--archive-root", default="pipeline/input-jobg8-archive")
    parser.add_argument("--output-dir", default="pipeline/reports-module3")
    parser.add_argument("--admin-register", default="pipeline/registers/admin_service_title_classification_register.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(parse_iso_date(args.start_date), parse_iso_date(args.end_date), Path(args.archive_root), Path(args.output_dir), Path(args.admin_register))


if __name__ == "__main__":
    main()

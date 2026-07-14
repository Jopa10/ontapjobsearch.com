#!/usr/bin/env python3
"""Run the existing Module 2 engine against isolated exploratory registers."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

import jobg8_module_2_monthly_category_profiler as module2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", required=True)
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--geo-lookup", required=True)
    parser.add_argument("--registers-dir", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    registers_dir = Path(args.registers_dir)
    manifest = registers_dir / "category_manifest.csv"
    manifest_df = pd.read_csv(manifest, dtype=str).fillna("")
    required = {"category", "register_file"}
    missing = required.difference(manifest_df.columns)
    if missing:
        raise ValueError(f"{manifest} missing columns: {sorted(missing)}")

    module2.REGISTER_SPECS = {
        row["category"]: [row["register_file"]]
        for _, row in manifest_df.iterrows()
        if row["category"] and row["register_file"]
    }
    module2.LIVE_SLICE_GROUPS = {}
    module2.run(
        input_dir=Path(args.input_dir),
        output_dir=Path(args.output_dir),
        month=args.month,
        geo_lookup_path=Path(args.geo_lookup),
        registers_dir=registers_dir,
    )


if __name__ == "__main__":
    main()

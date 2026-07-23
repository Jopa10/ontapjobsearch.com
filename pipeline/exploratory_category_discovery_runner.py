#!/usr/bin/env python3
"""Orchestrate isolated exploratory category discovery using existing Module 2.

This file deliberately lives outside pipeline/scripts so the repository's local
pandas compatibility shim cannot shadow the installed pandas package. It builds
temporary candidate registers, applies an evidence-led refinement layer, invokes
the existing Module 2 calculation engine, and creates the review shortlist. It
does not alter production registers, production reports, live pipelines or page
JSON files.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from types import ModuleType

import pandas as pd

PIPELINE_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = PIPELINE_DIR / "scripts"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(
    month: str,
    input_dir: Path,
    geo_lookup: Path,
    registers_dir: Path,
    reports_dir: Path,
) -> None:
    builder = load_module(
        "ontap_exploratory_register_builder",
        SCRIPTS_DIR / "build_exploratory_candidate_registers.py",
    )
    refiner = load_module(
        "ontap_exploratory_register_refiner",
        PIPELINE_DIR / "exploratory_candidate_register_refinement.py",
    )
    module2 = load_module(
        "ontap_module2_category_profiler",
        SCRIPTS_DIR / "jobg8_module_2_monthly_category_profiler.py",
    )
    summariser = load_module(
        "ontap_exploratory_summariser",
        SCRIPTS_DIR / "summarise_exploratory_category_discovery.py",
    )

    registers_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    classification_detail = (
        reports_dir / f"{month}-category-discovery-classification-detail.csv"
    )
    builder.run(
        input_dir=input_dir,
        output_dir=registers_dir,
        detail_output=classification_detail,
        month=month,
    )
    refiner.run(registers_dir)

    manifest_path = registers_dir / "category_manifest.csv"
    manifest = pd.read_csv(manifest_path, dtype=str).fillna("")
    required_manifest_columns = {"category", "register_file"}
    missing = required_manifest_columns.difference(manifest.columns)
    if missing:
        raise ValueError(
            f"{manifest_path} missing required columns: {sorted(missing)}"
        )

    module2.REGISTER_SPECS = {
        row["category"]: [row["register_file"]]
        for _, row in manifest.iterrows()
        if row["category"] and row["register_file"]
    }
    if len(module2.REGISTER_SPECS) != 6:
        raise ValueError(
            "Exploratory manifest must define exactly six candidate categories."
        )

    # Keep the existing geography and North East aggregate behaviour. Candidate
    # category keys do not overlap live categories, so every exploratory slice is
    # still correctly marked as not live.
    module2.run(
        input_dir=input_dir,
        output_dir=reports_dir,
        month=month,
        geo_lookup_path=geo_lookup,
        registers_dir=registers_dir,
    )

    validation_path = reports_dir / f"{month}-module2-category-validation.csv"
    summariser.run(
        validation_path=validation_path,
        shortlist_path=reports_dir / f"{month}-category-discovery-shortlist.csv",
        summary_path=reports_dir / f"{month}-category-discovery-summary.md",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run isolated July category discovery through existing Module 2."
    )
    parser.add_argument("--month", required=True)
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--geo-lookup", required=True)
    parser.add_argument("--registers-dir", required=True)
    parser.add_argument("--reports-dir", required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(
        month=args.month,
        input_dir=Path(args.input_dir),
        geo_lookup=Path(args.geo_lookup),
        registers_dir=Path(args.registers_dir),
        reports_dir=Path(args.reports_dir),
    )

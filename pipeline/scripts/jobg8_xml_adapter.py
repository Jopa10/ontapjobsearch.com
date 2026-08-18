from __future__ import annotations

import argparse
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from openpyxl import Workbook

REQUIRED = {
    "/Job/DisplayReference",
    "/Job/Position",
    "/Job/AdvertiserName",
    "/Job/AdvertiserType",
    "/Job/EmploymentType",
    "/Job/Area",
    "/Job/Location",
    "/Job/PostalCode",
    "/Job/ApplicationURL",
    "/Job/Description",
}


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def flatten(node: ET.Element, path: list[str], out: dict[str, str]) -> None:
    children = list(node)
    if not children:
        key = "/" + "/".join(path)
        value = (node.text or "").strip()
        if key not in out or not out[key]:
            out[key] = value
        return
    for child in children:
        flatten(child, path + [local(child.tag)], out)


def convert(zip_path: Path, output_path: Path, minimum: int, maximum: int) -> int:
    with zipfile.ZipFile(zip_path) as archive:
        candidates = [name for name in archive.namelist() if Path(name).name.lower() == "jobs.xml"]
        if len(candidates) != 1:
            raise RuntimeError(f"Expected one Jobs.xml, found {len(candidates)}")
        with archive.open(candidates[0]) as source:
            tree = ET.parse(source)

    rows: list[dict[str, str]] = []
    columns: list[str] = []
    seen: set[str] = set()

    for job in tree.getroot().iter():
        if local(job.tag).lower() != "job":
            continue
        row: dict[str, str] = {}
        for child in list(job):
            flatten(child, ["Job", local(child.tag)], row)
        if not row:
            continue
        rows.append(row)
        for key in row:
            if key not in seen:
                seen.add(key)
                columns.append(key)

    count = len(rows)
    if not minimum <= count <= maximum:
        raise RuntimeError(f"Job count {count} outside expected range {minimum}-{maximum}")

    missing = sorted(REQUIRED.difference(columns))
    if missing:
        raise RuntimeError("Missing required JobG8 fields: " + ", ".join(missing))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    workbook = Workbook(write_only=True)
    sheet = workbook.create_sheet(title="Jobs")
    sheet.append(columns)
    for row in rows:
        sheet.append([row.get(column, "") for column in columns])
    workbook.save(output_path)

    print(f"Converted {count} JobG8 jobs into {output_path}")
    print(f"Columns: {len(columns)}")
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--expected-min", type=int, default=5000)
    parser.add_argument("--expected-max", type=int, default=20000)
    args = parser.parse_args()
    convert(args.zip, args.output, args.expected_min, args.expected_max)


if __name__ == "__main__":
    main()

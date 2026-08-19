from __future__ import annotations

import argparse
from datetime import datetime
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


def _stamp_workbook_core_timestamp(path: Path, timestamp: datetime) -> None:
    """Make both XLSX core timestamps match the source Jobs.xml timestamp.

    openpyxl rewrites the workbook's modified timestamp at save time.  The
    selection pipeline deliberately uses that core date as the stable feed
    identity, so an archived raw feed restored tomorrow would otherwise look
    like a new feed.  Rewrite only docProps/core.xml after save and preserve all
    other workbook ZIP members unchanged.
    """
    replacement = path.with_name(f".{path.name}.restamp")
    with zipfile.ZipFile(path, "r") as source, zipfile.ZipFile(replacement, "w") as target:
        for info in source.infolist():
            data = source.read(info.filename)
            if info.filename == "docProps/core.xml":
                root = ET.fromstring(data)
                stamp = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
                found: set[str] = set()
                for element in root.iter():
                    field = local(element.tag)
                    if field in {"created", "modified"}:
                        element.text = stamp
                        found.add(field)
                if found != {"created", "modified"}:
                    raise RuntimeError(
                        "Generated XLSX core properties are missing created/modified timestamps"
                    )
                data = ET.tostring(root, encoding="utf-8", xml_declaration=True)
            target.writestr(info, data)
    replacement.replace(path)


def convert(zip_path: Path, output_path: Path, minimum: int, maximum: int) -> int:
    with zipfile.ZipFile(zip_path) as archive:
        candidates = [
            name for name in archive.namelist() if Path(name).name.lower() == "jobs.xml"
        ]
        if len(candidates) != 1:
            raise RuntimeError(f"Expected one Jobs.xml, found {len(candidates)}")
        source_name = candidates[0]
        source_timestamp = datetime(*archive.getinfo(source_name).date_time)
        with archive.open(source_name) as source:
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
    workbook.properties.created = source_timestamp
    workbook.properties.modified = source_timestamp
    sheet = workbook.create_sheet(title="Jobs")
    sheet.append(columns)
    for row in rows:
        sheet.append([row.get(column, "") for column in columns])
    workbook.save(output_path)
    _stamp_workbook_core_timestamp(output_path, source_timestamp)

    print(f"Converted {count} JobG8 jobs into {output_path}")
    print(f"Columns: {len(columns)}")
    print(f"Preserved JobG8 feed timestamp: {source_timestamp.isoformat()}")
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

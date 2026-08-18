from __future__ import annotations

import argparse
import gzip
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


def parse_feed(source_path: Path) -> tuple[ET.ElementTree, str]:
    """Parse JobG8 ZIP, gzip-compressed XML, or direct XML."""
    if zipfile.is_zipfile(source_path):
        with zipfile.ZipFile(source_path) as archive:
            candidates = [
                name
                for name in archive.namelist()
                if Path(name).name.lower() == "jobs.xml"
            ]
            if len(candidates) != 1:
                raise RuntimeError(f"Expected one Jobs.xml, found {len(candidates)}")
            with archive.open(candidates[0]) as source:
                return ET.parse(source), "zip"

    raw_prefix = source_path.read_bytes()[:256]
    if raw_prefix.startswith(b"\x1f\x8b"):
        try:
            with gzip.open(source_path, "rb") as source:
                return ET.parse(source), "gzip-xml"
        except (OSError, ET.ParseError) as exc:
            raise RuntimeError(
                "Downloaded JobG8 feed is gzip data but does not contain valid Jobs XML"
            ) from exc

    # Some JobG8 endpoints return Jobs.xml directly rather than wrapping it in a
    # ZIP. Accept that format, but reject HTML/auth/error pages with a clear stop.
    prefix = raw_prefix.lstrip()
    if not prefix.startswith(b"<"):
        magic = raw_prefix[:8].hex()
        raise RuntimeError(
            "Downloaded JobG8 feed is neither ZIP, gzip nor XML; refusing to parse it "
            f"(first 8 bytes: {magic})"
        )
    try:
        return ET.parse(source_path), "xml"
    except ET.ParseError as exc:
        raise RuntimeError(
            "Downloaded JobG8 feed looks like XML but is not valid Jobs XML"
        ) from exc


def convert(zip_path: Path, output_path: Path, minimum: int, maximum: int) -> int:
    tree, source_format = parse_feed(zip_path)

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

    print(f"JobG8 source format: {source_format}")
    print(f"Converted {count} JobG8 jobs into {output_path}")
    print(f"Columns: {len(columns)}")
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    # Keep --zip for workflow/backwards compatibility; the input is auto-detected.
    parser.add_argument("--zip", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--expected-min", type=int, default=5000)
    parser.add_argument("--expected-max", type=int, default=20000)
    args = parser.parse_args()
    convert(args.zip, args.output, args.expected_min, args.expected_max)


if __name__ == "__main__":
    main()

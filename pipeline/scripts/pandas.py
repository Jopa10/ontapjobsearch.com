"""Small local pandas-compatible shim for the JobG8 pipeline scripts.

The production scripts only need a tiny subset of pandas: reading CSV/XLSX
files as strings, iterating rows, checking columns, and replacing blanks.  This
shim keeps those scripts runnable in constrained environments where pandas and
openpyxl are unavailable.
"""
from __future__ import annotations

import csv
import re
import zipfile
from html import unescape
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree as ET


class ParserError(Exception):
    pass


class _Errors:
    ParserError = ParserError


errors = _Errors()


class Series(dict):
    pass


class DataFrame:
    def __init__(self, rows: Iterable[dict[str, Any]] | None = None, columns: Iterable[str] | None = None) -> None:
        self._rows = [dict(row) for row in (rows or [])]
        if columns is not None:
            self.columns = list(columns)
        elif self._rows:
            seen: list[str] = []
            for row in self._rows:
                for key in row:
                    if key not in seen:
                        seen.append(key)
            self.columns = seen
        else:
            self.columns = []

    def __len__(self) -> int:
        return len(self._rows)

    @property
    def empty(self) -> bool:
        return not self._rows

    def iterrows(self):
        for idx, row in enumerate(self._rows):
            yield idx, Series(row)

    def fillna(self, value: Any) -> "DataFrame":
        return DataFrame(
            [
                {key: (value if isna(cell) else cell) for key, cell in row.items()}
                for row in self._rows
            ],
            columns=self.columns,
        )


def isna(value: Any) -> bool:
    return value is None


def read_csv(path: str | Path, dtype: Any = None, nrows: int | None = None) -> DataFrame:
    del dtype
    try:
        with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            rows: list[dict[str, Any]] = []
            if nrows == 0:
                return DataFrame(rows, columns=columns)
            for row in reader:
                rows.append({key: (value or "") for key, value in row.items()})
                if nrows is not None and len(rows) >= nrows:
                    break
            return DataFrame(rows, columns=columns)
    except csv.Error as exc:
        raise ParserError(str(exc)) from exc


def read_excel(path: str | Path, dtype: Any = None, nrows: int | None = None) -> DataFrame:
    del dtype
    rows = _read_xlsx(Path(path), nrows=nrows)
    if not rows:
        return DataFrame([])
    columns = [str(cell or "") for cell in rows[0]]
    data_rows: list[dict[str, Any]] = []
    if nrows == 0:
        return DataFrame(data_rows, columns=columns)
    for row in rows[1:]:
        padded = row + [""] * max(0, len(columns) - len(row))
        data_rows.append({columns[idx]: (padded[idx] if idx < len(padded) else "") for idx in range(len(columns))})
        if nrows is not None and len(data_rows) >= nrows:
            break
    return DataFrame(data_rows, columns=columns)


def _read_xlsx(path: Path, nrows: int | None = None) -> list[list[str]]:
    with zipfile.ZipFile(path) as archive:
        shared_strings = _read_shared_strings(archive)
        sheet_path = _first_sheet_path(archive)
        root = ET.fromstring(archive.read(sheet_path))

    namespace = _namespace(root.tag)
    rows: list[list[str]] = []
    for row_node in root.findall(f".//{{{namespace}}}sheetData/{{{namespace}}}row"):
        row_values: list[str] = []
        for cell in row_node.findall(f"{{{namespace}}}c"):
            ref = cell.attrib.get("r", "")
            col_idx = _column_index(ref)
            while len(row_values) < col_idx:
                row_values.append("")
            row_values.append(_cell_value(cell, namespace, shared_strings))
        rows.append(row_values)
        if nrows == 0 and rows:
            break
        if nrows is not None and nrows > 0 and len(rows) > nrows:
            break
    return rows


def _read_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    namespace = _namespace(root.tag)
    strings: list[str] = []
    for item in root.findall(f"{{{namespace}}}si"):
        parts = [node.text or "" for node in item.findall(f".//{{{namespace}}}t")]
        strings.append(unescape("".join(parts)))
    return strings


def _first_sheet_path(archive: zipfile.ZipFile) -> str:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    workbook_ns = _namespace(workbook.tag)
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    rels_ns = _namespace(rels.tag)
    first_sheet = workbook.find(f"{{{workbook_ns}}}sheets/{{{workbook_ns}}}sheet")
    if first_sheet is None:
        raise ParserError("workbook has no sheets")
    rel_id = first_sheet.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
    for rel in rels.findall(f"{{{rels_ns}}}Relationship"):
        if rel.attrib.get("Id") == rel_id:
            target = rel.attrib["Target"]
            return target if target.startswith("xl/") else "xl/" + target.lstrip("/") if not target.startswith("/") else target.lstrip("/")
    raise ParserError("could not resolve first worksheet")


def _namespace(tag: str) -> str:
    match = re.match(r"\{([^}]+)\}", tag)
    return match.group(1) if match else ""


def _column_index(cell_ref: str) -> int:
    letters = re.match(r"([A-Z]+)", cell_ref or "")
    if not letters:
        return 1
    value = 0
    for char in letters.group(1):
        value = value * 26 + ord(char) - ord("A") + 1
    return value


def _cell_value(cell: ET.Element, namespace: str, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return unescape("".join(node.text or "" for node in cell.findall(f".//{{{namespace}}}t")))
    value_node = cell.find(f"{{{namespace}}}v")
    raw = value_node.text if value_node is not None else ""
    if cell_type == "s" and raw:
        idx = int(raw)
        return shared_strings[idx] if idx < len(shared_strings) else ""
    return raw or ""

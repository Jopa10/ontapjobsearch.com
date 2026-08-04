"""Canonical Teaching Vacancies review runner with visible-field fallbacks.

Teaching Vacancies' JobPosting JSON-LD does not always contain salary, even
when the public advert displays a Full time equivalent salary.  This runner
keeps the existing bounded POC behaviour, adds a visible-page salary fallback,
and blocks a review when an in-scope vacancy still has no salary.
"""
from __future__ import annotations

import sys
from html.parser import HTMLParser

from external_sources import teaching_vacancies_poc as poc

_BASE_PARSE_JOBPOSTING = poc.parse_jobposting
_BASE_PROCESS = poc.process


class VisibleTextParser(HTMLParser):
    """Collect visible text nodes in document order, excluding page machinery."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._ignored_depth = 0

    def handle_starttag(
        self,
        tag: str,
        _attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag.casefold() in {"script", "style", "noscript", "template"}:
            self._ignored_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if (
            tag.casefold() in {"script", "style", "noscript", "template"}
            and self._ignored_depth
        ):
            self._ignored_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._ignored_depth:
            return
        text = poc.clean(data)
        if text:
            self.parts.append(text)


def visible_label_value(document: str, label: str) -> str:
    """Return the visible value immediately following an exact page label."""
    parser = VisibleTextParser()
    parser.feed(document)
    target = poc.normalise(label)
    for index, part in enumerate(parser.parts):
        if poc.normalise(part) != target:
            continue
        for candidate in parser.parts[index + 1 : index + 5]:
            value = poc.clean(candidate)
            if value and poc.normalise(value) != target:
                return value
    return ""


def parse_jobposting(document: str, url: str) -> poc.Vacancy:
    """Parse JSON-LD, then recover salary from the visible advert if needed."""
    vacancy = _BASE_PARSE_JOBPOSTING(document, url)
    if not vacancy.salary_text:
        vacancy.salary_text = visible_label_value(
            document,
            "Full time equivalent salary",
        )
    return vacancy


def validate_core_fields(vacancies: list[poc.Vacancy]) -> None:
    """Block an accepted regional review when a core visible field is blank."""
    missing_salary = [
        vacancy.source_job_id or vacancy.title
        for vacancy in vacancies
        if vacancy.geography_status == "IN_SCOPE"
        and not poc.clean(vacancy.salary_text)
    ]
    if missing_salary:
        raise ValueError(
            "Teaching Vacancies field audit failed: in-scope adverts have no "
            "salary after structured and visible-page extraction: "
            + ", ".join(sorted(missing_salary))
        )


def process(
    vacancies: list[poc.Vacancy],
    jobg8: list[dict],
) -> list[poc.Vacancy]:
    reviewed = _BASE_PROCESS(vacancies, jobg8)
    validate_core_fields(reviewed)
    return reviewed


def install_patches() -> None:
    poc.parse_jobposting = parse_jobposting
    poc.process = process


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--report-csv" not in args:
        args.extend(
            [
                "--report-csv",
                "reviews/external/west-yorkshire-teaching-vacancies-review.csv",
            ]
        )
    if "--summary-md" not in args:
        args.extend(
            [
                "--summary-md",
                "reviews/external/west-yorkshire-teaching-vacancies-summary.md",
            ]
        )
    install_patches()
    return poc.main(args)


if __name__ == "__main__":
    raise SystemExit(main())

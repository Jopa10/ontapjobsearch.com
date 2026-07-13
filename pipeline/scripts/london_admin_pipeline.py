from __future__ import annotations

import csv
from pathlib import Path

from scripts import service_admin_pipeline as pipeline

REGION = "London"
CATEGORY = "admin_service"


def load_london_anchor(path: Path, category: str) -> dict[str, str]:
    if category != CATEGORY:
        raise SystemExit(f"STOP: unsupported London pipeline category: {category}")
    anchor_df = pipeline.read_xlsx_sheet(path, sheet_name="Anchor_towns")
    matches = []
    for _, row in anchor_df.iterrows():
        if pipeline.norm_key(row.get("category")) != CATEGORY:
            continue
        if pipeline.norm(row.get("region")) == REGION:
            matches.append(pipeline.norm(row.get("anchor_town")))
    if len(matches) != 1 or not matches[0]:
        raise SystemExit(
            "STOP: Anchor_towns must contain exactly one complete London / admin_service row."
        )
    return {REGION: matches[0]}


def configure() -> None:
    pipeline.REGION_MAP["london"] = REGION
    pipeline.OUTPUT_FILES = {REGION: "london-admin-service.json"}
    pipeline.PUBLISH_THRESHOLDS = {REGION: 6}
    pipeline.load_anchor_towns = load_london_anchor

    pipeline.REPORTS_DAILY_DIR = Path("reports-daily")
    pipeline.DECISION_REPORT_PATH = pipeline.REPORTS_DAILY_DIR / "decision-report-admin-service-london.csv"
    pipeline.MANUAL_DIR = Path("manual")
    pipeline.MANUAL_REVIEW_CSV_PATH = pipeline.MANUAL_DIR / "service-admin-london-review.csv"
    pipeline.MANUAL_REVIEW_MD_PATH = pipeline.MANUAL_DIR / "service-admin-london-review.md"
    pipeline.MANUAL_REVIEW_PATH = pipeline.MANUAL_REVIEW_CSV_PATH

    def london_preview(rows, preserved_action_rows=None):
        return [
            row for row in rows
            if str(row.get("region", "")) == REGION
            and str(row.get("selection_status", "")) in {"SELECTED", "POSSIBLE_SELECTION"}
        ]

    def london_markdown(path, rows, preserved_actions=None, preserved_action_rows=None):
        preserved_actions = preserved_actions or {}
        lines = [
            "# London service-admin manual review",
            "",
            "Edit only the `action:` line in each block:",
            "",
            "- For a selected job, use `action: exclude`.",
            "- For a possible job, use `action: select`.",
            "- Leave `action:` blank for no change.",
            "",
        ]
        for heading, status, label in (
            ("LONDON — SELECTED", "SELECTED", "SELECTED"),
            ("LONDON — POSSIBLES", "POSSIBLE_SELECTION", "POSS - LONDON"),
        ):
            lines.extend([f"## {heading}", ""])
            selected = [
                row for row in rows
                if str(row.get("region", "")) == REGION
                and str(row.get("selection_status", "")) == status
            ]
            if not selected:
                lines.extend(["_No jobs in this group._", ""])
                continue
            for row in selected:
                job_id = pipeline._markdown_value(row.get("job_id"))
                action = preserved_actions.get(job_id, "")
                summary = " | ".join([
                    label,
                    REGION,
                    pipeline._markdown_value(row.get("town")),
                    pipeline._markdown_value(row.get("salary_text")),
                    pipeline._markdown_value(row.get("title")),
                ])
                lines.extend([
                    "---",
                    f"action: {action}" if action else "action:",
                    summary,
                    f"job_id: {job_id}",
                    "---",
                    "",
                ])
        path.write_text("\n".join(lines), encoding="utf-8")

    pipeline._manual_review_preview_rows = london_preview
    pipeline.write_manual_review_markdown = london_markdown


if __name__ == "__main__":
    configure()
    raise SystemExit(pipeline.main())

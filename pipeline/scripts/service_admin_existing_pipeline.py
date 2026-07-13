from __future__ import annotations

from pathlib import Path

from scripts import service_admin_pipeline as pipeline

CATEGORY = "admin_service"


def load_existing_anchors(path: Path, category: str) -> dict[str, str]:
    if category != CATEGORY:
        raise SystemExit(f"STOP: unsupported existing admin pipeline category: {category}")

    anchor_df = pipeline.read_xlsx_sheet(path, sheet_name="Anchor_towns")
    anchors: dict[str, str] = {}
    for _, row in anchor_df.iterrows():
        if pipeline.norm_key(row.get("category")) != CATEGORY:
            continue
        region = pipeline.norm(row.get("region"))
        anchor_town = pipeline.norm(row.get("anchor_town"))
        if region not in pipeline.OUTPUT_FILES:
            continue
        if not anchor_town:
            raise SystemExit(
                f"STOP: Anchor_towns contains an incomplete row for {region} / {CATEGORY}."
            )
        if region in anchors:
            raise SystemExit(
                f"STOP: Anchor_towns contains duplicate rows for {region} / {CATEGORY}."
            )
        anchors[region] = anchor_town

    missing = sorted(set(pipeline.OUTPUT_FILES) - set(anchors))
    if missing:
        raise SystemExit(
            "STOP: Anchor_towns is missing required admin_service region(s): "
            + ", ".join(missing)
        )
    return anchors


if __name__ == "__main__":
    pipeline.load_anchor_towns = load_existing_anchors
    raise SystemExit(pipeline.main())

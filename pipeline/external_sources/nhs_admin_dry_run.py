from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path

from external_sources import nhs_admin_service as nhs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--review-csv", type=Path, required=True)
    parser.add_argument("--summary-md", type=Path, required=True)
    parser.add_argument("--composed-dir", type=Path, required=True)
    parser.add_argument("--report-json", type=Path, required=True)
    parser.add_argument("--report-md", type=Path, required=True)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    args = parser.parse_args(argv)

    payload = json.loads(args.inventory.read_text(encoding="utf-8"))
    vacancies = payload.get("rows", [])
    rows = nhs.review_rows(vacancies, today=args.today)
    nhs.write_review_csv(args.review_csv, rows)
    args.summary_md.parent.mkdir(parents=True, exist_ok=True)
    args.summary_md.write_text(nhs.review_summary(rows, today=args.today), encoding="utf-8")
    composition = nhs.compose_outputs(
        Path("output-admin-service"), rows, args.composed_dir, today=args.today
    )

    final_counts = Counter(row["final_decision"] for row in rows)
    switch_counts = Counter(row["switchability"] for row in rows)
    routed_live = sum(row["publish_eligible"] == "YES" for row in rows)
    selected_publishable = sum(
        row["final_decision"] == "SELECTED" and row["publish_eligible"] == "YES"
        for row in rows
    )
    missing_descriptions = sum(
        row["final_decision"] == "SELECTED"
        and row["publish_eligible"] == "YES"
        and not row["description"]
        for row in rows
    )
    report = {
        "review_date": args.today.isoformat(),
        "api_reported_total": int(payload.get("reported_total") or 0),
        "reviewed_open_rows": len(rows),
        "final_decisions": dict(sorted(final_counts.items())),
        "switchability": dict(sorted(switch_counts.items())),
        "routed_to_live_slices": routed_live,
        "selected_publishable_before_source_cap": selected_publishable,
        "selected_publishable_missing_description": missing_descriptions,
        "composition": composition,
        "safety": {
            "live_files_changed": False,
            "output_directory": str(args.composed_dir),
            "nhs_share_cap": nhs.MAX_NHS_SHARE,
        },
    }
    args.report_json.parent.mkdir(parents=True, exist_ok=True)
    args.report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# NHS service/admin publish-readiness dry run", "",
        f"- Review date: {args.today.isoformat()}",
        f"- NHS API Administrative & Clerical total: {report['api_reported_total']}",
        f"- Open rows reviewed: {len(rows)}",
        f"- Routed to current LIVE admin/service slices: {routed_live}",
        f"- Selected/publishable before NHS source cap: {selected_publishable}",
        f"- Selected rows still missing a reusable description: {missing_descriptions}", "",
        "## Decisions", "",
    ]
    for key, value in sorted(final_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Switchability", ""])
    for key, value in sorted(switch_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Regional composition", ""])
    for region, item in sorted(composition.get("regions", {}).items()):
        lines.append(
            f"- {region}: base {item['base']}; NHS candidate {item['nhs_selected']}; "
            f"accepted {item['nhs_accepted']}; deferred {item['deferred']}; total {item['total']}"
        )
    lines.extend([
        "", "## Boundary", "",
        "This report writes only dry-run composed JSON. It does not modify output-admin-service or app pages.",
    ])
    args.report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

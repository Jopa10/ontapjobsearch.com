#!/usr/bin/env python3
"""Maintain the human city-page approval review and promote approved READY cities.

Human workflow:
1. The generated Markdown review lists READY FOR APPROVAL city/category candidates.
2. Edit only `action:` and set it to `approve` for a city you want to launch.
3. Committing that file triggers the approval workflow.

The technical city-page register and route file are generated from the regional
opportunity-market definitions. They are not intended to be edited by hand.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from scripts.scan_city_opportunities import DEFAULT_MARKET_REGISTER, DEFAULT_REGISTER, normalise
from scripts.update_city_opportunity_history import (
    DEFAULT_HISTORY,
    DEFAULT_THRESHOLD,
    REQUIRED_QUALIFYING_RUNS,
    collect_candidates,
    lifecycle_status,
    load_history,
    recent_counts,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_APPROVAL_REVIEW = Path("pipeline/reviews/city-pages/city-page-approval-review.md")
VALID_ACTIONS = {"", "approve"}


def slugify(value: str) -> str:
    value = normalise(value)
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value


def public_slice(slice_key: str) -> str:
    if slice_key == "support-worker-jobs":
        return "support-worker"
    return slice_key


def category_label(slice_key: str) -> str:
    if slice_key == "service-administrator-jobs":
        return "admin and customer-service jobs"
    if slice_key in {"support-worker", "support-worker-jobs"}:
        return "support worker jobs"
    return slice_key.replace("-", " ")


def candidate_key_from_fields(region: str, slice_key: str, locality: str) -> str:
    return "|".join((normalise(region), normalise(slice_key), normalise(locality)))


def approval_key(row: dict[str, Any]) -> str:
    return candidate_key_from_fields(
        str(row.get("region", "")),
        str(row.get("slice", "")),
        str(row.get("locality", row.get("city", ""))),
    )


def parse_review(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []

    blocks: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if stripped == "---":
            if current is None:
                current = {}
            else:
                if current:
                    blocks.append(current)
                current = None
            continue
        if current is None or ":" not in stripped:
            continue
        field, value = stripped.split(":", 1)
        current[field.strip().casefold()] = value.strip()

    for block in blocks:
        action = block.get("action", "").casefold()
        if action not in VALID_ACTIONS:
            raise ValueError(
                f"invalid city approval action {action!r}; use `approve` or leave blank"
            )
    return blocks


def ready_candidates(root: Path) -> list[dict[str, Any]]:
    candidates = collect_candidates(root, root / DEFAULT_REGISTER, root / DEFAULT_MARKET_REGISTER)
    history = load_history(root / DEFAULT_HISTORY)
    ready: list[dict[str, Any]] = []
    for history_key, row in candidates.items():
        # The approval manager can only build a governed catchment from a
        # registered market. Exact-location fallback rows remain useful audit
        # signals, but must not be presented as directly actionable approvals.
        if not bool(row.get("registered_market", False)):
            continue
        counts = recent_counts(history, history_key)
        qualifying_runs = sum(value >= DEFAULT_THRESHOLD for value in counts)
        status = lifecycle_status(
            current=int(row.get("jobs", 0)),
            qualifying_runs=qualifying_runs,
            active=bool(row.get("active", False)),
            registered_market=bool(row.get("registered_market", False)),
        )
        if status != "READY FOR APPROVAL":
            continue
        ready.append(
            {
                **row,
                "status": status,
                "qualifying_runs": qualifying_runs,
                "history": counts,
            }
        )
    return sorted(
        ready,
        key=lambda row: (
            str(row.get("region", "")),
            str(row.get("slice", "")),
            normalise(row.get("locality", "")),
        ),
    )


def render_review(rows: list[dict[str, Any]], prior_blocks: list[dict[str, str]]) -> str:
    actions = {approval_key(block): block.get("action", "") for block in prior_blocks}
    lines = [
        "# City page approval review",
        "",
        "This is the human approval file for new city pages.",
        "",
        "## How to review",
        "Edit only the `action:` line inside a city block.",
        "Use `action: approve` to launch that city page, or leave `action:` blank to hold it.",
        "Do not edit the technical city-page register; it is generated from this approval.",
        "A city appears here only after the opportunity process marks it READY FOR APPROVAL.",
        "",
        f"## READY FOR APPROVAL ({len(rows)})",
        "",
    ]
    for row in rows:
        key = approval_key(row)
        history = ", ".join(str(value) for value in row.get("history", [])) or "—"
        lines.extend(
            [
                "---",
                f"action: {actions.get(key, '')}",
                "status: READY FOR APPROVAL",
                f"city: {row['locality']}",
                f"region: {row['region']}",
                f"slice: {row['slice']}",
                f"current_jobs: {row['jobs']}",
                f"qualifying_runs: {row['qualifying_runs']}/{REQUIRED_QUALIFYING_RUNS}",
                f"last_pipeline_runs: {history}",
                "---",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def load_markets(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("opportunity-market register must be an array")
    return [row for row in raw if isinstance(row, dict)]


def find_market(markets: list[dict[str, Any]], region: str, locality: str) -> dict[str, Any]:
    matches = [
        row
        for row in markets
        if normalise(row.get("region_key")) == normalise(region)
        and normalise(row.get("display_name")) == normalise(locality)
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one registered market for {region}/{locality}, found {len(matches)}")
    return matches[0]


def reason_for_include(locality: str, pattern: str) -> str:
    return f"The stated workplace matches the approved {locality} employment-market pattern `{pattern}`."


def build_config(
    *,
    region: str,
    slice_key: str,
    locality: str,
    market: dict[str, Any],
    all_markets: list[dict[str, Any]],
) -> dict[str, Any]:
    city_slug = slugify(locality)
    route_slice = public_slice(slice_key)
    key = f"{city_slug}-{route_slice}"
    include_patterns = [
        normalise(value) for value in market.get("include_patterns", []) if normalise(value)
    ]
    own_excludes = [
        normalise(value) for value in market.get("exclude_patterns", []) if normalise(value)
    ]

    other_market_patterns: list[str] = []
    for other in all_markets:
        if normalise(other.get("region_key")) != normalise(region):
            continue
        if normalise(other.get("display_name")) == normalise(locality):
            continue
        for value in other.get("include_patterns", []):
            pattern = normalise(value)
            if pattern and pattern not in include_patterns:
                other_market_patterns.append(pattern)

    exclude_patterns = list(dict.fromkeys(own_excludes + other_market_patterns))
    broad_region = normalise(region.replace("-", " "))
    review_patterns = list(
        dict.fromkeys(
            [
                broad_region,
                "regionwide",
                "home-based",
                "home based",
                "hybrid",
                "remote",
                "various locations",
            ]
        )
    )

    return {
        "city_key": key,
        "display_name": locality,
        "category_label": category_label(slice_key),
        "parent_page": f"app/{region}/{slice_key}.json",
        "review_csv": f"pipeline/reviews/city-pages/{key}-review.csv",
        "summary_md": f"pipeline/reviews/city-pages/{key}-summary.md",
        "output_json": f"app/_city-pages/{city_slug}/{route_slice}.json",
        "route": f"/{city_slug}/{route_slice}",
        "minimum_live_jobs": DEFAULT_THRESHOLD,
        "launch_minimum_live_jobs": DEFAULT_THRESHOLD,
        "lifecycle_state": "active",
        "retention_policy": "permanent",
        "mode": "publish",
        "include_rules": [
            {"pattern": pattern, "reason": reason_for_include(locality, pattern)}
            for pattern in include_patterns
        ],
        "review_rules": [
            {
                "pattern": pattern,
                "reason": f"The stated location is broader or less specific than the approved {locality} employment market and needs review.",
            }
            for pattern in review_patterns
            if pattern
        ],
        "exclude_rules": [
            {
                "pattern": pattern,
                "reason": f"The stated workplace belongs outside the approved {locality} employment market.",
            }
            for pattern in exclude_patterns
        ],
        "fallback_decision": "review",
        "fallback_reason": f"No approved {locality} employment-market rule matched the stated location; local geographic review is required.",
    }


def admin_training_source() -> str:
    return '''\nconst adminTraining = [\n  {\n    title: "Business Administration Level 2",\n    provider: "OpenLearn",\n    description: "Foundational office administration learning for scheduling, communication and records tasks.",\n    link: "https://www.open.edu/openlearn/money-business/business-studies/introduction-business-administration/content-section-0",\n  },\n  {\n    title: "Customer Service Skills",\n    provider: "Alison",\n    description: "Practical customer service training useful for service-administrator and front-office roles.",\n    link: "https://alison.com/course/customer-service-skills",\n  },\n  {\n    title: "Excel for Administrative Work",\n    provider: "Microsoft Learn",\n    description: "Build spreadsheet and reporting skills commonly required in office support roles.",\n    link: "https://learn.microsoft.com/training/",\n  },\n];\n'''


def page_source(config: dict[str, Any]) -> str:
    route = str(config["route"])
    locality = str(config["display_name"])
    category = str(config["category_label"])
    parent_page = str(config["parent_page"])
    parent_route = "/" + parent_page.removeprefix("app/").removesuffix(".json")
    if parent_route.endswith("/support-worker-jobs"):
        parent_route = parent_route.removesuffix("-jobs")
    is_admin = str(config.get("parent_page", "")).endswith("/service-administrator-jobs.json")
    title_category = "Admin & Customer Service Jobs" if is_admin else "Support Worker Jobs"
    training = admin_training_source() if is_admin else ""
    training_props = (
        '\n      trainingHeading="Boost your admin applications"\n      trainingSubheading="Useful online learning commonly requested for service-administrator and office support roles"\n      trainingItems={adminTraining}'
        if is_admin
        else ""
    )
    return f'''import type {{ Metadata }} from "next";\nimport {{ notFound }} from "next/navigation";\nimport JobSlicePage from "@/components/JobSlicePage";\nimport {{ getJobPageStatus }} from "@/config/job-page-status";\nimport {{ getCityPageDefinitionByRoute, isCityPageActive }} from "@/lib/city-page-data";\n\nconst route = "{route}";\nconst routeKey = route.slice(1);\nconst definition = getCityPageDefinitionByRoute(route);\nconst canonicalUrl = `https://www.ontapjobsearch.com${{route}}`;\n{training}\nexport const metadata: Metadata = {{\n  title: "{locality} {title_category} | Ontap Job Search",\n  description: "Browse current {category} across {locality} and its approved local employment market.",\n  alternates: {{ canonical: canonicalUrl }},\n}};\n\nexport default function Page() {{\n  if (!definition || !isCityPageActive(definition)) notFound();\n  const latestUpdate = getJobPageStatus(routeKey);\n\n  return (\n    <JobSlicePage\n      jsonPath={{[...definition.jsonPath]}}\n      region="{locality}"\n      title="{locality} {title_category}"\n      latestUpdate={{latestUpdate}}\n      introText={{`Current {category} across {locality} and its approved local employment market. Jobs are checked and updated daily. Latest update: ${{latestUpdate}} • Apply on employer sites`}}\n      anchorTown="{locality}"{training_props}\n      relatedPage={{{{\n        href: "{parent_route}",\n        prompt: "Looking across the wider region?",\n        label: "View all regional jobs",\n      }}}}\n    />\n  );\n}}\n'''


def apply_approvals(root: Path, approval_path: Path) -> int:
    blocks = parse_review(approval_path)
    approved = [block for block in blocks if block.get("action", "").casefold() == "approve"]
    if not approved:
        print("No city-page approvals to apply")
        return 0

    register_path = root / DEFAULT_REGISTER
    market_path = root / DEFAULT_MARKET_REGISTER
    register = json.loads(register_path.read_text(encoding="utf-8"))
    if not isinstance(register, list):
        raise ValueError("city-page register must be an array")
    markets = load_markets(market_path)
    candidates = collect_candidates(root, register_path, market_path)
    current_by_key = {approval_key(row): row for row in candidates.values()}
    existing_routes = {str(row.get("route", "")) for row in register if isinstance(row, dict)}
    existing_keys = {str(row.get("city_key", "")) for row in register if isinstance(row, dict)}

    added = 0
    for block in approved:
        if block.get("status") != "READY FOR APPROVAL":
            raise ValueError(f"{block.get('city', 'city')} is not marked READY FOR APPROVAL")
        key = approval_key(block)
        current = current_by_key.get(key)
        if not current:
            raise ValueError(f"approved city is not a current registered candidate: {key}")
        if int(current.get("jobs", 0)) < DEFAULT_THRESHOLD:
            raise ValueError(f"approved city has fallen below {DEFAULT_THRESHOLD} current jobs: {key}")
        if not bool(current.get("registered_market", False)):
            raise ValueError(f"approved city is not backed by a registered local market: {key}")

        region = block["region"]
        slice_key = block["slice"]
        locality = block["city"]
        market = find_market(markets, region, locality)
        config = build_config(
            region=region,
            slice_key=slice_key,
            locality=locality,
            market=market,
            all_markets=markets,
        )
        if config["route"] in existing_routes or config["city_key"] in existing_keys:
            print(f"Already active: {config['route']}")
            continue

        page_path = root / "app" / config["route"].strip("/") / "page.tsx"
        if page_path.exists():
            raise ValueError(f"refusing to overwrite existing route page: {page_path}")
        page_path.parent.mkdir(parents=True, exist_ok=True)
        page_path.write_text(page_source(config), encoding="utf-8")
        register.append(config)
        existing_routes.add(config["route"])
        existing_keys.add(config["city_key"])
        added += 1
        print(f"Approved city page: {config['route']}")

    if added:
        register_path.write_text(json.dumps(register, indent=2) + "\n", encoding="utf-8")
    print(f"New city pages configured: {added}")
    return added


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--refresh", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--approval-review", type=Path, default=DEFAULT_APPROVAL_REVIEW)
    args = parser.parse_args()

    root = args.repo_root.resolve()
    approval_path = args.approval_review if args.approval_review.is_absolute() else root / args.approval_review
    approval_path.parent.mkdir(parents=True, exist_ok=True)

    if args.refresh:
        prior = parse_review(approval_path)
        approval_path.write_text(render_review(ready_candidates(root), prior), encoding="utf-8")
        print(f"City-page approval review written to {approval_path}")
        return 0

    apply_approvals(root, approval_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

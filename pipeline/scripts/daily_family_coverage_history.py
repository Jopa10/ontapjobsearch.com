from __future__ import annotations

import json
from pathlib import Path
from typing import Any


HISTORY_PATH = Path("reports-daily/daily-family-coverage-history.json")
WINDOW_DAYS = 14
WATCH_THRESHOLD = 6
FAMILIES = (
    "service_admin",
    "support_worker",
    "customer_sales",
    "legal_assistant_paralegal",
    "marketing",
    "hr_recruitment",
)


def empty_history() -> dict[str, Any]:
    return {
        "version": 1,
        "window_days": WINDOW_DAYS,
        "threshold": WATCH_THRESHOLD,
        "snapshots": [],
    }


def load_history(path: Path = HISTORY_PATH) -> dict[str, Any]:
    if not path.is_file():
        return empty_history()
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise RuntimeError("Daily family coverage history must be a JSON object")
    snapshots = raw.get("snapshots", [])
    if not isinstance(snapshots, list):
        raise RuntimeError("Daily family coverage history snapshots must be a list")
    raw["version"] = 1
    raw["window_days"] = WINDOW_DAYS
    raw["threshold"] = WATCH_THRESHOLD
    raw["snapshots"] = snapshots
    return raw


def _snapshot_counts(
    regions: dict[str, dict[str, str]],
    admin_counts: dict[str, int],
    support_counts: dict[str, int],
    sales_counts: dict[str, int],
    legal_counts: dict[str, int] | None = None,
    marketing_counts: dict[str, int] | None = None,
    hr_counts: dict[str, int] | None = None,
) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for region in sorted(regions, key=str.casefold):
        counts[region] = {
            "service_admin": int(admin_counts[region]),
            "support_worker": int(support_counts[region]),
            "customer_sales": int(sales_counts[region]),
        }
        if legal_counts is not None:
            counts[region]["legal_assistant_paralegal"] = int(legal_counts[region])
        if marketing_counts is not None:
            counts[region]["marketing"] = int(marketing_counts[region])
        if hr_counts is not None:
            counts[region]["hr_recruitment"] = int(hr_counts[region])
    return counts


def record_snapshot(
    feed_date: str,
    regions: dict[str, dict[str, str]],
    admin_counts: dict[str, int],
    support_counts: dict[str, int],
    sales_counts: dict[str, int],
    legal_counts: dict[str, int] | None = None,
    marketing_counts: dict[str, int] | None = None,
    hr_counts: dict[str, int] | None = None,
    *,
    path: Path = HISTORY_PATH,
) -> dict[str, Any]:
    """Persist one snapshot per feed date, replacing same-date reruns.

    The file retains only the latest 14 feed dates. Every current assessable
    market/family count is stored so history remains continuous when a slice
    later changes LIVE status. Older three-family snapshots remain readable.
    """
    history = load_history(path)
    snapshots = [
        item
        for item in history.get("snapshots", [])
        if isinstance(item, dict) and str(item.get("feed_date") or "") != feed_date
    ]
    snapshots.append(
        {
            "feed_date": feed_date,
            "counts": _snapshot_counts(
                regions,
                admin_counts,
                support_counts,
                sales_counts,
                legal_counts,
                marketing_counts,
                hr_counts,
            ),
        }
    )
    snapshots.sort(key=lambda item: str(item.get("feed_date") or ""))
    history["snapshots"] = snapshots[-WINDOW_DAYS:]
    history["version"] = 1
    history["window_days"] = WINDOW_DAYS
    history["threshold"] = WATCH_THRESHOLD
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
    return history


def observed_values(
    history: dict[str, Any],
    region: str,
    family: str,
    *,
    as_of_date: str,
) -> list[int]:
    values: list[int] = []
    snapshots = [
        item
        for item in history.get("snapshots", [])
        if isinstance(item, dict)
        and str(item.get("feed_date") or "")
        and str(item.get("feed_date") or "") <= as_of_date
    ][-WINDOW_DAYS:]
    for snapshot in snapshots:
        counts = snapshot.get("counts", {})
        if not isinstance(counts, dict):
            continue
        regional = counts.get(region, {})
        if not isinstance(regional, dict) or family not in regional:
            continue
        try:
            values.append(int(regional[family]))
        except (TypeError, ValueError):
            continue
    return values


def format_metric(
    history: dict[str, Any],
    region: str,
    family: str,
    today: int,
    *,
    as_of_date: str,
) -> str:
    """Render Today / observed-window average / 6+ days for a NOT LIVE cell."""
    values = observed_values(history, region, family, as_of_date=as_of_date)
    if not values:
        values = [int(today)]
    average = sum(values) / len(values)
    qualifying = sum(value >= WATCH_THRESHOLD for value in values)
    return f"{int(today)} / {average:.1f} / {qualifying}/{len(values)}"

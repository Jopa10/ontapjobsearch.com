"""Resolve and persist the two idempotent JobG8 refresh cycles per UK day."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


LONDON = ZoneInfo("Europe/London")
CYCLES = {"morning", "evening"}
SCHEDULE_CYCLES = {"30 7 * * *": "morning", "30 15 * * *": "evening"}
DEFAULT_STATE_PATH = Path("pipeline/reports-daily/jobg8-daily-cycle-state.json")


def london_now(value: str | None = None) -> datetime:
    if value:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            raise ValueError("--now must include a timezone offset")
        return parsed.astimezone(LONDON)
    return datetime.now(LONDON)


def resolve_cycle(event_name: str, schedule: str, requested_cycle: str, now: datetime) -> str:
    if event_name == "schedule":
        try:
            return SCHEDULE_CYCLES[schedule]
        except KeyError as error:
            raise ValueError(f"unknown JobG8 schedule: {schedule!r}") from error
    if requested_cycle in CYCLES:
        return requested_cycle
    if requested_cycle != "auto":
        raise ValueError(f"unknown requested cycle: {requested_cycle!r}")
    return "morning" if now.hour < 12 else "evening"


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"schema_version": 1, "completed_cycles": {}}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("schema_version") != 1 or not isinstance(raw.get("completed_cycles"), dict):
        raise ValueError(f"invalid JobG8 daily cycle state: {path}")
    return raw


def completed(state: dict, date: str, cycle: str) -> bool:
    return cycle in state["completed_cycles"].get(date, {})


def mark_completed(state: dict, date: str, cycle: str, run_id: str, at: datetime) -> dict:
    state["completed_cycles"].setdefault(date, {})[cycle] = {
        "completed_at": at.isoformat(),
        "run_id": str(run_id),
    }
    # The marker only coordinates the current operational period; retain two days
    # for auditability without growing the normal daily commit indefinitely.
    state["completed_cycles"] = dict(sorted(state["completed_cycles"].items())[-2:])
    return state


def write_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("check", "mark"))
    parser.add_argument("--event-name", required=True)
    parser.add_argument("--schedule", default="")
    parser.add_argument("--requested-cycle", default="auto")
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE_PATH)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--now", help="ISO-8601 timestamp with offset; test use only")
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()

    now = london_now(args.now)
    cycle = resolve_cycle(args.event_name, args.schedule, args.requested_cycle, now)
    date = now.date().isoformat()
    state = load_state(args.state)
    should_run = not completed(state, date, cycle)

    if args.command == "mark":
        if not args.run_id:
            raise ValueError("--run-id is required when marking a completed cycle")
        write_state(args.state, mark_completed(state, date, cycle, args.run_id, now))
        should_run = False

    lines = [f"cycle={cycle}", f"date={date}", f"should_run={'true' if should_run else 'false'}"]
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")
    else:
        print("\n".join(lines))


if __name__ == "__main__":
    main()

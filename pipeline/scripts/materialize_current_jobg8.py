from __future__ import annotations

import argparse
import shutil
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

from jobg8_xml_adapter import convert


def download(feed_url: str, target: Path, attempts: int = 4, timeout: int = 180) -> None:
    if not feed_url.strip():
        raise RuntimeError("JOBG8_FEED_URL is not configured")

    target.parent.mkdir(parents=True, exist_ok=True)
    last_error: Exception | None = None
    request = Request(feed_url, headers={"User-Agent": "OntapJobG8Materializer/1.0"})

    for attempt in range(1, attempts + 1):
        try:
            with urlopen(request, timeout=timeout) as response, target.open("wb") as handle:
                shutil.copyfileobj(response, handle)
            if target.stat().st_size <= 0:
                raise RuntimeError("Downloaded JobG8 archive is empty")
            return
        except (OSError, URLError, RuntimeError) as exc:
            last_error = exc
            if target.exists():
                target.unlink()
            if attempt < attempts:
                time.sleep(5)

    raise RuntimeError(f"Could not download current JobG8 feed after {attempts} attempts") from last_error


def clear_pipeline_input(input_dir: Path) -> None:
    input_dir.mkdir(parents=True, exist_ok=True)
    for pattern in ("*.xlsx", "*.xls", "*.xlsm", "*.csv"):
        for path in input_dir.glob(pattern):
            path.unlink()


def materialize(
    feed_url: str,
    *,
    zip_path: Path,
    output_path: Path,
    expected_min: int = 5000,
    expected_max: int = 20000,
) -> int:
    download(feed_url, zip_path)
    clear_pipeline_input(output_path.parent)
    count = convert(zip_path, output_path, expected_min, expected_max)
    if not output_path.is_file() or output_path.stat().st_size <= 0:
        raise RuntimeError(f"Materialized JobG8 workbook is missing or empty: {output_path}")
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed-url", required=True)
    parser.add_argument("--zip", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--expected-min", type=int, default=5000)
    parser.add_argument("--expected-max", type=int, default=20000)
    args = parser.parse_args()

    count = materialize(
        args.feed_url,
        zip_path=args.zip,
        output_path=args.output,
        expected_min=args.expected_min,
        expected_max=args.expected_max,
    )
    print(f"Materialized current JobG8 feed: {count} jobs -> {args.output}")


if __name__ == "__main__":
    main()

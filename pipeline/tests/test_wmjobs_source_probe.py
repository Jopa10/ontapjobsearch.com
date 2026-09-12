import json
from pathlib import Path

from external_sources import wmjobs_source_probe as probe


def test_probe_is_bounded_to_official_hosts() -> None:
    hosts = {
        __import__("urllib.parse").parse.urlsplit(url).hostname
        for _name, url in probe.OFFICIAL_ENDPOINTS
    }
    assert hosts == {"www.wmjobs.co.uk", "solihull.wm-jobs.co.uk"}
    assert len(probe.OFFICIAL_ENDPOINTS) <= 10


def test_probe_contains_no_bypass_service() -> None:
    urls = " ".join(url for _name, url in probe.OFFICIAL_ENDPOINTS).casefold()
    assert "r.jina.ai" not in urls
    assert "googleusercontent" not in urls
    assert "proxy" not in urls


def test_run_writes_diagnostic_only(monkeypatch, tmp_path: Path) -> None:
    def fake_fetch(name: str, url: str, timeout: int = 25) -> probe.ProbeResult:
        return probe.ProbeResult(
            name=name,
            requested_url=url,
            final_url=url,
            status=200,
            content_type="text/html",
            byte_count=100,
            title="Public jobs",
            wmjobs_detail_links=2,
        )

    monkeypatch.setattr(probe, "fetch_once", fake_fetch)
    output = tmp_path / "probe.json"
    results = probe.run(output)
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert len(results) == len(probe.OFFICIAL_ENDPOINTS)
    assert payload["purpose"].endswith("assessment only")
    assert "publishing" in payload["safety"]
    assert not (tmp_path / "app").exists()

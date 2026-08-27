from pathlib import Path

import pytest

from reprosafe.models import ScanResult
from reprosafe.reports import bundle


def test_bundle_is_removed_when_generation_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    destination = tmp_path / "report"
    monkeypatch.setattr(bundle, "build_markdown", lambda *_: (_ for _ in ()).throw(RuntimeError()))

    with pytest.raises(RuntimeError):
        bundle.create_bundle(destination, [])

    assert not destination.exists()
    assert not list(tmp_path.glob(".report.*"))


def test_bundle_can_omit_machine_readable_diagnostics(tmp_path: Path):
    destination = tmp_path / "report"
    scan = ScanResult("app.log", "safe", 4, 1)

    bundle.create_bundle(destination, [scan], include_diagnostics_json=False)

    assert (destination / "report.md").is_file()
    assert (destination / "sanitized" / "app.log").read_text() == "safe"
    assert not (destination / "diagnostics.json").exists()

from pathlib import Path
from typer.testing import CliRunner
from reprosafe.cli import app
runner = CliRunner()
def test_version(): assert runner.invoke(app, ["version"]).stdout.strip() == "ReproSafe 0.1.0"
def test_scan_dry_run(tmp_path: Path):
    source = tmp_path / "a.log"; source.write_text("password=hunter2")
    result = runner.invoke(app, ["scan", str(source), "--dry-run"])
    assert result.exit_code == 0 and "No files written" in result.stdout and not (tmp_path / "a.safe.log").exists()
def test_bundle(tmp_path: Path):
    source = tmp_path / "a.log"; source.write_text("token=abcdefgh")
    output = tmp_path / "report"
    result = runner.invoke(app, ["bundle", "--output", str(output), "--file", str(source)])
    assert result.exit_code == 0 and "abcdefgh" not in (output / "report.md").read_text() and "abcdefgh" not in (output / "diagnostics.json").read_text()

"""Atomic-ish local report directory creation."""
from pathlib import Path
from reprosafe.collectors.system import collect_system
from reprosafe.collectors.tools import collect_tools
from reprosafe.models import ScanResult
from reprosafe.reports.json_report import build_json
from reprosafe.reports.markdown import build_markdown
from reprosafe.utils.files import FileSafetyError

def create_bundle(destination: Path, scans: list[ScanResult]) -> Path:
    if destination.exists(): raise FileSafetyError(f"Output already exists: {destination}")
    destination.mkdir(parents=True); sanitized = destination / "sanitized"; sanitized.mkdir()
    system, tools = collect_system(), collect_tools()
    (destination / "report.md").write_text(build_markdown(system, tools, scans), encoding="utf-8")
    (destination / "diagnostics.json").write_text(build_json(system, tools, scans), encoding="utf-8")
    for scan in scans: (sanitized / scan.source_name).write_text(scan.sanitized_text, encoding="utf-8")
    return destination

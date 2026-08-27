"""Transactional, private local report bundle creation."""
import os
import shutil
import tempfile
from dataclasses import replace
from pathlib import Path

from reprosafe.collectors.system import collect_system
from reprosafe.collectors.tools import collect_tools
from reprosafe.models import ScanResult
from reprosafe.reports.json_report import build_json
from reprosafe.reports.markdown import build_markdown
from reprosafe.utils.files import FileSafetyError

def _unique_scans(scans: list[ScanResult]) -> list[ScanResult]:
    """Give same-named inputs deterministic, non-overwriting bundle names."""
    used: set[str] = set()
    output: list[ScanResult] = []
    for scan in scans:
        source = Path(scan.source_name)
        candidate = source.name
        number = 2
        while candidate.casefold() in used:
            candidate = f"{source.stem}-{number}{source.suffix}"
            number += 1
        used.add(candidate.casefold())
        output.append(replace(scan, source_name=candidate))
    return output


def _write_private(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        # Some platforms do not implement POSIX permission bits.
        pass


def create_bundle(
    destination: Path,
    scans: list[ScanResult],
    *,
    include_diagnostics_json: bool = True,
) -> Path:
    """Build a complete bundle off to the side, then publish it in one rename."""
    destination = destination.absolute()
    if destination.exists():
        raise FileSafetyError(f"Output already exists: {destination}")

    parent = destination.parent
    parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{destination.name}.", dir=parent))
    try:
        temporary.chmod(0o700)
        sanitized = temporary / "sanitized"
        sanitized.mkdir(mode=0o700)
        system, tools = collect_system(), collect_tools()
        bundle_scans = _unique_scans(scans)
        _write_private(temporary / "report.md", build_markdown(system, tools, bundle_scans))
        if include_diagnostics_json:
            _write_private(
                temporary / "diagnostics.json", build_json(system, tools, bundle_scans)
            )
        for scan in bundle_scans:
            _write_private(sanitized / scan.source_name, scan.sanitized_text)
        os.rename(temporary, destination)
    except FileExistsError as exc:
        raise FileSafetyError(f"Output already exists: {destination}") from exc
    finally:
        if temporary.exists():
            shutil.rmtree(temporary, ignore_errors=True)
    return destination

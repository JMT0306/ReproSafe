"""GitHub-ready Markdown generation from sanitized inputs only."""
from typing import Any
from reprosafe.models import ScanResult
from reprosafe.scanners.errors import SUGGESTIONS

def build_markdown(system: dict[str, Any], tools: dict[str, Any], scans: list[ScanResult]) -> str:
    lines = ["# ReproSafe Diagnostic Report", "", "## Summary", "", f"Local diagnostics with {sum(s.replacement_count for s in scans)} sensitive value(s) removed.", "", "## Environment", "", "| Component | Value |", "|---|---|"]
    for key in ("os", "architecture", "cpu", "cpu_cores", "memory_total_gb", "disk_free_percent", "python", "cwd"):
        if key in system: lines.append(f"| {key.replace('_', ' ').title()} | {system[key]} |")
    lines += ["", "## Developer Tools", "", "| Tool | Version |", "|---|---|"]
    for name, version in tools.items(): lines.append(f"| {name} | {version or 'not detected'} |")
    lines += ["", "## Diagnostics", ""]
    for scan in scans: lines += [f"### `{scan.source_name}`", "", f"{scan.lines} lines; {scan.replacement_count} replacement(s).", ""]
    lines += ["## Detected Errors", ""]
    categories = sorted({item for scan in scans for item in scan.errors}); lines.append(", ".join(categories) if categories else "No known signatures detected.")
    lines += ["", "## Relevant Stack Traces", "", ", ".join(sorted({x for s in scans for x in s.stack_traces})) or "None detected.", "", "## Sanitization Summary", ""]
    totals: dict[str, int] = {}
    for scan in scans:
        for key, count in scan.redactions.items(): totals[key] = totals.get(key, 0) + count
    lines.extend(f"- {key.replace('_', ' ').title()}: {count}" for key, count in sorted(totals.items()))
    if not totals: lines.append("- No sensitive patterns detected.")
    lines += ["", "## Files Included", "", *(f"- `{s.source_name}` (sanitized copy only)" for s in scans), "", "## Suggested Checks", ""]
    suggestions = [tip for category in categories for tip in SUGGESTIONS.get(category, [])]
    lines.extend(f"{i}. {tip}" for i, tip in enumerate(dict.fromkeys(suggestions), 1))
    if not suggestions: lines.append("No deterministic suggestions available.")
    lines += ["", "## Privacy Notice", "", "This report was generated locally. It contains no raw environment-variable dump and no original secret values detected by ReproSafe. Review it before sharing; pattern-based detection can miss unusual sensitive data.", ""]
    return "\n".join(lines)

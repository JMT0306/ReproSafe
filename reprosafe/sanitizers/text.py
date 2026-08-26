"""Reusable local sanitization and analysis pipeline."""
from pathlib import Path
from reprosafe.config import Config
from reprosafe.models import ScanResult
from reprosafe.scanners.errors import classify_errors
from reprosafe.scanners.pii import redact_pii
from reprosafe.scanners.secrets import redact_secrets
from reprosafe.scanners.stacktrace import detect_stack_traces
from reprosafe.sanitizers.paths import sanitize_paths

def sanitize_text(text: str, source_name: str = "input", config: Config | None = None) -> ScanResult:
    cfg = config or Config(); counts: dict[str, int] = {}
    sanitized, found = redact_secrets(text)
    for key, value in found.items(): counts[key] = counts.get(key, 0) + value
    sanitized, found = redact_pii(sanitized, cfg.privacy)
    for key, value in found.items(): counts[key] = counts.get(key, 0) + value
    if cfg.privacy.redact_username:
        sanitized, found = sanitize_paths(sanitized)
        for key, value in found.items(): counts[key] = counts.get(key, 0) + value
    return ScanResult(Path(source_name).name, sanitized, len(text.encode("utf-8")),
                      len(text.splitlines()), counts, classify_errors(sanitized),
                      detect_stack_traces(sanitized),
                      sum("error" in line.lower() for line in sanitized.splitlines()),
                      sum("warning" in line.lower() or "warn" in line.lower() for line in sanitized.splitlines()))

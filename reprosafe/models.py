"""Typed data exchanged by ReproSafe's local pipeline."""
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Finding:
    category: str
    count: int

@dataclass
class ScanResult:
    source_name: str
    sanitized_text: str
    size_bytes: int
    lines: int
    redactions: dict[str, int] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    stack_traces: list[str] = field(default_factory=list)
    error_lines: int = 0
    warning_lines: int = 0

    @property
    def replacement_count(self) -> int:
        return sum(self.redactions.values())

    def safe_metadata(self) -> dict[str, Any]:
        """Return metadata only; source contents never enter JSON diagnostics."""
        return {"source_name": self.source_name, "size_bytes": self.size_bytes,
                "lines": self.lines, "redactions": dict(self.redactions),
                "errors": list(self.errors), "stack_trace_types": list(self.stack_traces),
                "error_lines": self.error_lines, "warning_lines": self.warning_lines}

@dataclass
class CommandResult:
    args: tuple[str, ...]
    returncode: int
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False

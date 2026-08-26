"""Machine-readable, content-free diagnostic schema."""
import json
from typing import Any
from reprosafe import __version__
from reprosafe.models import ScanResult

def build_json(system: dict[str, Any], tools: dict[str, Any], scans: list[ScanResult]) -> str:
    payload = {"schema_version": "1.0", "reprosafe_version": __version__, "system": system, "tools": tools,
               "findings": [scan.safe_metadata() for scan in scans],
               "privacy": {"redactions": {key: sum(s.redactions.get(key, 0) for s in scans) for key in sorted({k for s in scans for k in s.redactions})}}}
    return json.dumps(payload, indent=2, sort_keys=True)

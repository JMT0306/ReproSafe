# Architecture

```text
Explicit input
  ↓
Bounded reader / read-only collector
  ↓
Ordered secret and PII detection
  ↓
Path-aware sanitization
  ↓
Deterministic error and stack-family analysis
  ↓
Markdown / content-free JSON / sanitized copies
```

`utils.commands` is the sole subprocess boundary. `scanners` contains detection rules, while `sanitizers.text` composes them without CLI dependencies. `collectors` obtain minimized system/tool/Docker data. `reports` accepts typed scan results and never serializes raw input. `vision` defines a small optional OCR protocol and non-destructive region-redaction implementation for future CLI enablement.

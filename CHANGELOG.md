# Changelog

## Unreleased

- Make report bundle creation transactional and clean up incomplete output after failures.
- Use private permissions for bundle directories and files where the platform supports them.
- Preserve same-named input files with deterministic numbered names instead of overwriting them.
- Honor the `report.include_diagnostics_json` configuration setting.

## 0.1.0 — 2026-08-26

- Initial privacy-first doctor, inspect, scan, configuration, and bundle CLI.
- Local secret/PII/path sanitization, deterministic diagnostics, reports, tests, and CI.

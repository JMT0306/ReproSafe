# Contributing

Use Python 3.11+, create a focused branch, install `.[dev]`, and run `ruff check .`, `mypy reprosafe`, and `pytest`. New redaction behavior needs positive, false-positive, and end-to-end leak tests using synthetic values only. Do not put real secrets in commits, fixtures, issues, or pull requests. Changes should remain local-first, shell-free, typed, and cross-platform.

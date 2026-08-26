# ReproSafe

> **The black box recorder for software bugs.**

ReproSafe turns messy logs and local environment diagnostics into clean, privacy-safe bug reports. It is local-first: no account, telemetry, upload, AI, or network request.

[![CI](https://github.com/JMT0306/ReproSafe/actions/workflows/ci.yml/badge.svg)](https://github.com/JMT0306/ReproSafe/actions/workflows/ci.yml) ![Python](https://img.shields.io/badge/python-3.11%2B-blue) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

```text
$ reprosafe scan crash.log
PASS 782 lines processed
PASS 3 values redacted
PASS 1 stack trace type detected
Safe copy: crash.safe.log
```

## Why ReproSafe?

Bug reports need context, but logs routinely contain credentials, personal data, machine paths, and network addresses. ReproSafe builds useful evidence locally while minimizing accidental disclosure.

## Quick Start

```bash
python -m pip install -e .
reprosafe doctor
reprosafe inspect examples/sample-python-error.log
reprosafe scan examples/sample-python-error.log
reprosafe bundle --file examples/sample-python-error.log
```

Python 3.11 or newer is required. `python -m reprosafe` provides the same CLI.

## What gets redacted?

API keys, GitHub/AWS/Slack tokens, JWTs, authorization headers, generic token/password/key assignments, credential-bearing connection URLs, email addresses, private IP addresses, and Windows/macOS/Linux user-home paths. Public IP redaction is opt-in. Replacements preserve useful structure where practical.

Detection is pattern-based. **Always review generated material before sharing.**

## Commands

| Command | Behavior |
|---|---|
| `doctor` | Read-only system, developer tool, and narrow Docker diagnostics |
| `scan FILE` | Write a new sanitized text copy; supports `--output` and `--dry-run` |
| `inspect FILE` | Display counts without creating a file or revealing matches |
| `bundle [--file FILE]` | Generate Markdown, JSON, and sanitized copies |
| `config` | Show config location and active privacy defaults |
| `version` | Show the package version |

Supported text types are `.txt`, `.log`, `.json`, `.yaml`, `.yml`, `.env`, `.ini`, `.cfg`, `.conf`, and `.config`. Image extensions are recognized, but the current CLI reports the optional OCR installation requirement rather than risking an unsanitized copy.

Exit codes: `0` success, `1` generic failure, `2` invalid arguments, `3` file/process failure, `4` safety refusal.

## Privacy

ReproSafe never dumps the environment, reads container filesystems, uploads data, or runs subprocesses through a shell. Diagnostics call only bounded local version/read-only commands. See [privacy details](docs/privacy.md) and [security model](docs/security.md).

## Configuration

The platform-native config path is shown by `reprosafe config`. Example:

```toml
[privacy]
redact_emails = true
redact_private_ips = true
redact_public_ips = false
redact_hostname = true
redact_username = true

[scan]
max_file_size_mb = 20
```

## Examples

All files under [`examples/`](examples/) contain clearly marked synthetic values. See [example workflows](docs/examples.md).

## Roadmap

The next releases focus on reliable opt-in screenshot OCR/redaction and better structured stack-frame extraction. Later possibilities are explicit-scope recording, issue drafts, local AI, MCP, and editor integrations. See the [roadmap](docs/roadmap.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security-sensitive changes require regression tests.

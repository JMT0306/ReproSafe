# Privacy model

ReproSafe reads only files explicitly named by the user and local runtime/system metadata needed by `doctor` or `bundle`. It invokes a fixed set of local developer-tool version commands and narrow, read-only Docker status commands. It does not recursively scan directories, dump environment variables, inspect containers, read shell history, send telemetry, or upload reports.

Default sanitization covers common credentials, credential-bearing URLs, authorization headers, emails, private addresses, and user-home path prefixes. Hostname and username fields from system collection are replaced rather than emitted. Public IPs remain useful by default and can be redacted in configuration.

Detection is heuristic. False positives and false negatives are possible, encoded or fragmented secrets can evade patterns, and OCR is not enabled by default. Generated files must be reviewed before sharing. Originals are never overwritten: existing output paths and symlink inputs are refused.

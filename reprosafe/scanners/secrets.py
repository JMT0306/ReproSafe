"""Ordered credential redaction rules; matches are replaced, never retained."""
import re
from dataclasses import dataclass
from collections.abc import Callable

@dataclass(frozen=True)
class Rule:
    category: str
    pattern: re.Pattern[str]
    replacement: str | Callable[[re.Match[str]], str]

def _credential_url(match: re.Match[str]) -> str:
    return f"{match.group('scheme')}://[USER]:[REDACTED_PASSWORD]@[HOST]{match.group('port') or ''}{match.group('path') or ''}"

RULES = (
    Rule("connection_string", re.compile(r"(?P<scheme>postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqp|https?)://[^\s:/@]+:[^\s@]+@[^\s/:]+(?P<port>:\d+)?(?P<path>/[^\s\"']*)?", re.I), _credential_url),
    Rule("authorization", re.compile(r"(?i)(authorization\s*[:=]\s*)(?:bearer\s+|basic\s+)?[^\s,\"']+"), r"\1[REDACTED_TOKEN]"),
    Rule("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"), "[REDACTED_TOKEN]"),
    Rule("github_token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{8,}|github_pat_[A-Za-z0-9_]{8,})\b"), "[REDACTED_TOKEN]"),
    Rule("openai_api_key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{12,}\b"), "[REDACTED_API_KEY]"),
    Rule("aws_access_key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"), "[REDACTED_API_KEY]"),
    Rule("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), "[REDACTED_TOKEN]"),
    Rule("password", re.compile(r"(?i)([\"']?(?:password|passwd)[\"']?\s*[:=]\s*)[\"']?[^\s,}\"']+[\"']?"), r"\1[REDACTED_PASSWORD]"),
    Rule("api_key", re.compile(r"(?i)([\"']?(?:[A-Z0-9_]*api[_-]?key|access[_-]?key)[\"']?\s*[:=]\s*)[\"']?[^\s,}\"']+[\"']?"), r"\1[REDACTED_API_KEY]"),
    Rule("token", re.compile(r"(?i)([\"']?(?:[A-Z0-9_]*token|secret(?:_key)?)[\"']?\s*[:=]\s*)[\"']?[^\s,}\"']+[\"']?"), r"\1[REDACTED_TOKEN]"),
)

def redact_secrets(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for rule in RULES:
        text, count = rule.pattern.subn(rule.replacement, text)
        if count: counts[rule.category] = counts.get(rule.category, 0) + count
    return text, counts

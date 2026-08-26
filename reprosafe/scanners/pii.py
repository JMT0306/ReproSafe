"""Conservative email and IP redaction."""
import ipaddress
import re
from reprosafe.config import PrivacyConfig
EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w.-])")
IP_CANDIDATE = re.compile(r"(?<![\w:])(?:\d{1,3}\.){3}\d{1,3}(?![\w:])|(?<![\w:])(?:[0-9A-Fa-f]{1,4}:){2,7}[0-9A-Fa-f]{1,4}(?![\w:])")

def redact_pii(text: str, config: PrivacyConfig) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    if config.redact_emails:
        text, count = EMAIL.subn("[EMAIL]", text)
        if count: counts["email"] = count
    def replace_ip(match: re.Match[str]) -> str:
        try: address = ipaddress.ip_address(match.group())
        except ValueError: return match.group()
        category = "private_ip" if address.is_private or address.is_loopback else "public_ip"
        enabled = config.redact_private_ips if category == "private_ip" else config.redact_public_ips
        if not enabled: return match.group()
        counts[category] = counts.get(category, 0) + 1
        return "[PRIVATE_IP]" if category == "private_ip" else "[PUBLIC_IP]"
    return IP_CANDIDATE.sub(replace_ip, text), counts

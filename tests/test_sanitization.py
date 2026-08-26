from reprosafe.config import Config
from reprosafe.sanitizers.text import sanitize_text

def test_paths_email_and_ips():
    result = sanitize_text(r"C:\Users\John\project /home/jane/app a@example.com 10.0.0.8 8.8.8.8 2001:4860:4860::8888")
    assert r"[HOME]\project" in result.sanitized_text
    assert "[HOME]/app" in result.sanitized_text
    assert "[EMAIL]" in result.sanitized_text and "[PRIVATE_IP]" in result.sanitized_text
    assert "8.8.8.8" in result.sanitized_text

def test_public_ip_config():
    cfg = Config(); cfg.privacy.redact_public_ips = True
    assert "[PUBLIC_IP]" in sanitize_text("8.8.8.8", config=cfg).sanitized_text

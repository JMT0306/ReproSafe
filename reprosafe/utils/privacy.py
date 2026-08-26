"""Helpers that never return raw environment secrets."""
SENSITIVE_ENV_MARKERS = ("TOKEN", "SECRET", "PASSWORD", "PASS", "API_KEY", "PRIVATE_KEY", "ACCESS_KEY", "AUTH", "COOKIE", "SESSION", "CREDENTIAL")
def is_sensitive_env_name(name: str) -> bool:
    upper = name.upper()
    return any(marker in upper for marker in SENSITIVE_ENV_MARKERS)

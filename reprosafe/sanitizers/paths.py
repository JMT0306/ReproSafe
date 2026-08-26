"""Cross-platform home-path minimization."""
import re
WINDOWS_HOME = re.compile(r"(?i)\b[A-Z]:\\Users\\[^\\\s/:*?\"<>|]+")
UNIX_HOME = re.compile(r"(?<![\w])/(?:home|Users)/[^/\s]+")

def sanitize_paths(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    text, win = WINDOWS_HOME.subn("[HOME]", text)
    text, unix = UNIX_HOME.subn("[HOME]", text)
    if win + unix: counts["home_path"] = win + unix
    return text, counts

"""Best-effort stack trace family detection."""
import re
PATTERNS = {"python": r"Traceback \(most recent call last\):[\s\S]*?(?:\w+Error|\w+Exception):", "node": r"(?:\w*Error:.*\n)(?:\s+at .+\n)+", "java": r"(?:Exception|Error).*\n(?:\s+at [\w.$]+\(.+?:\d+\)\n)+", "dotnet": r"(?:System\.\w+Exception).*\n(?:\s+at .+\n)+", "go": r"panic:.*\n(?:goroutine \d+|\s+.+\.go:\d+)", "rust": r"thread '.+' panicked at"}
def detect_stack_traces(text: str) -> list[str]:
    return [language for language, pattern in PATTERNS.items() if re.search(pattern, text, re.M)]

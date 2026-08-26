"""Deterministic error signatures and cautious suggestions."""
import re
PATTERNS: dict[str, str] = {
 "permission": r"permission denied|access is denied", "dns": r"name or service not known|dns.*fail|getaddrinfo",
 "connection_refused": r"connection (?:was )?refused|ECONNREFUSED", "timeout": r"timed? out|ETIMEDOUT",
 "file_not_found": r"file not found|no such file or directory|ENOENT", "module_not_found": r"ModuleNotFoundError|Cannot find module",
 "port_in_use": r"address already in use|EADDRINUSE", "authentication": r"unauthorized|authentication failed|invalid credentials",
 "docker_daemon": r"cannot connect to the docker daemon", "out_of_memory": r"out of memory|MemoryError|OOMKilled",
 "disk_space": r"no space left on device|disk full", "syntax_error": r"SyntaxError|syntax error",
 "ssl_certificate": r"certificate verify failed|SSL.*certificate", "database_connection": r"(?:postgres|mysql|mongo|redis).*connect",
 "network": r"network is unreachable|ENETUNREACH",
}
SUGGESTIONS = {"connection_refused": ["Verify that the target service is running.", "Verify host and port configuration.", "Check whether a firewall may be blocking the connection."], "docker_daemon": ["Verify that Docker Desktop or Docker Engine is running.", "Check the current Docker context.", "Verify socket or named-pipe permissions."]}

def classify_errors(text: str) -> list[str]:
    return [name for name, pattern in PATTERNS.items() if re.search(pattern, text, re.I)]

"""Narrow, read-only Docker diagnostics (never container inspect)."""
import shutil
from typing import Any
from reprosafe.utils.commands import run_command

def collect_docker() -> dict[str, Any]:
    if shutil.which("docker") is None: return {"cli_installed": False, "daemon_reachable": False}
    version = run_command(("docker", "version", "--format", "{{.Client.Version}}"))
    info = run_command(("docker", "info", "--format", "{{.Name}}"))
    result: dict[str, Any] = {"cli_installed": True, "client_version": version.stdout or "detected", "daemon_reachable": info.returncode == 0}
    compose = run_command(("docker", "compose", "version", "--short")); result["compose_version"] = compose.stdout or None
    if info.returncode != 0: return result
    context = run_command(("docker", "context", "show")); result["context"] = context.stdout or "unknown"
    running = run_command(("docker", "ps", "-q")); stopped = run_command(("docker", "ps", "-aq", "--filter", "status=exited"))
    result["running_containers"] = len(running.stdout.splitlines()) if running.stdout else 0
    result["stopped_containers"] = len(stopped.stdout.splitlines()) if stopped.stdout else 0
    usage = run_command(("docker", "system", "df", "--format", "{{.Type}}: {{.Size}}")); result["disk_usage"] = usage.stdout.splitlines() if usage.returncode == 0 else []
    return result

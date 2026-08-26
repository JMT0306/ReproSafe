"""Read-only system diagnostics with identifying values minimized."""
import os
import platform
import shutil
import sys
from pathlib import Path

from reprosafe.sanitizers.paths import sanitize_paths


def _memory() -> tuple[float | str, float | str]:
    """Return Linux memory values when exposed; degrade safely elsewhere."""
    meminfo = Path("/proc/meminfo")
    if not meminfo.is_file():
        return "unknown", "unknown"
    values: dict[str, int] = {}
    for line in meminfo.read_text(encoding="ascii", errors="replace").splitlines():
        key, _, raw = line.partition(":")
        if raw.strip().split():
            values[key] = int(raw.strip().split()[0])
    return round(values.get("MemTotal", 0) / 1024**2, 1), round(
        values.get("MemAvailable", 0) / 1024**2, 1
    )


def collect_system() -> dict[str, str | int | float]:
    disk = shutil.disk_usage(Path.cwd())
    cwd, _ = sanitize_paths(str(Path.cwd()))
    total_memory, available_memory = _memory()
    cpu = platform.processor() or platform.machine() or "unknown"
    return {
        "os": f"{platform.system()} {platform.release()}",
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "hostname": "[HOSTNAME]",
        "cpu": cpu,
        "cpu_cores": os.cpu_count() or 0,
        "memory_total_gb": total_memory,
        "memory_available_gb": available_memory,
        "disk_free_percent": round(disk.free / disk.total * 100, 1),
        "python": platform.python_version(),
        "shell": Path(os.environ.get("SHELL", os.environ.get("COMSPEC", "unknown"))).name,
        "cwd": cwd,
        "username": "[USER]",
        "runtime": sys.implementation.name,
    }

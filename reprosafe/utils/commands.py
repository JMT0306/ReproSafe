"""Centralized, non-shell subprocess execution."""
import subprocess
from collections.abc import Sequence
from reprosafe.models import CommandResult

def run_command(args: Sequence[str], timeout: float = 5.0) -> CommandResult:
    safe_args = tuple(str(arg) for arg in args)
    try:
        process = subprocess.run(safe_args, capture_output=True, text=True, errors="replace",
                                 timeout=timeout, check=False, shell=False)
        return CommandResult(safe_args, process.returncode, process.stdout.strip(),
                             process.stderr.strip())
    except (FileNotFoundError, PermissionError) as exc:
        return CommandResult(safe_args, 127, stderr=type(exc).__name__)
    except subprocess.TimeoutExpired:
        return CommandResult(safe_args, 124, timed_out=True)

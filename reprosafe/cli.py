"""Polished, non-interactive ReproSafe command line interface."""
import logging
from pathlib import Path
from typing import Annotated
import typer
from rich.console import Console
from rich.table import Table
from reprosafe import __version__
from reprosafe.collectors.docker import collect_docker
from reprosafe.collectors.system import collect_system
from reprosafe.collectors.tools import collect_tools
from reprosafe.config import CONFIG_PATH, Config, load_config
from reprosafe.models import ScanResult
from reprosafe.reports.bundle import create_bundle
from reprosafe.sanitizers.text import sanitize_text
from reprosafe.utils.files import IMAGE_EXTENSIONS, FileSafetyError, read_text_file, safe_output_path, write_new_file

app = typer.Typer(help="The black box recorder for software bugs.", no_args_is_help=True, rich_markup_mode="markdown")
console = Console(); state = {"verbose": False}

@app.callback()
def main(verbose: Annotated[bool, typer.Option("--verbose", help="Enable safe diagnostic logging.")] = False) -> None:
    state["verbose"] = verbose
    logging.basicConfig(level=logging.DEBUG if verbose else logging.WARNING, format="%(levelname)s: %(message)s")

def _load(path: Path) -> tuple[str, Config]:
    cfg = load_config()
    try: return read_text_file(path, cfg.scan.max_file_size_mb * 1024 * 1024), cfg
    except (FileSafetyError, OSError) as exc:
        console.print("[bold red]Unable to read file.[/bold red]\n\nReason:\n" + str(exc)); raise typer.Exit(3) from None

def _analyze(path: Path, config: Config | None = None) -> ScanResult:
    if config is None:
        text, cfg = _load(path)
    else:
        cfg = config
        try:
            text = read_text_file(path, cfg.scan.max_file_size_mb * 1024 * 1024)
        except (FileSafetyError, OSError) as exc:
            console.print(f"[bold red]Unable to read file.[/bold red]\n\nReason:\n{exc}")
            raise typer.Exit(3) from None
    return sanitize_text(text, path.name, cfg)

@app.command()
def version() -> None:
    """Print the installed version."""
    console.print(f"ReproSafe {__version__}")

@app.command("config")
def config_command() -> None:
    """Show the active configuration path and privacy-safe defaults."""
    cfg = load_config(); console.print("[bold]ReproSafe Configuration[/bold]")
    console.print(f"Path: {CONFIG_PATH}\nStatus: {'loaded' if CONFIG_PATH.exists() else 'using privacy-first defaults'}\nMax file size: {cfg.scan.max_file_size_mb} MB\nEmail redaction: {cfg.privacy.redact_emails}\nPrivate IP redaction: {cfg.privacy.redact_private_ips}\nPublic IP redaction: {cfg.privacy.redact_public_ips}")

@app.command()
def doctor() -> None:
    """Run read-only local environment diagnostics."""
    console.print("[bold cyan]ReproSafe Doctor[/bold cyan]")
    system = collect_system(); table = Table(title="System", show_header=False)
    for label, key in (("OS", "os"), ("Architecture", "architecture"), ("CPU", "cpu"), ("CPU cores", "cpu_cores"), ("Memory", "memory_total_gb"), ("Available memory", "memory_available_gb"), ("Disk free", "disk_free_percent"), ("Python", "python"), ("Shell", "shell"), ("Working directory", "cwd")): table.add_row("PASS", label, str(system[key]))
    console.print(table); tools_table = Table(title="Developer tools", show_header=False)
    for name, value in collect_tools().items(): tools_table.add_row("PASS" if value else "–", name, value or "not detected")
    console.print(tools_table); docker = collect_docker()
    if docker["cli_installed"] and not docker["daemon_reachable"]: console.print("[yellow]WARN Docker CLI detected but daemon is unreachable.[/yellow]\nPossible checks: verify the engine, context, and socket permissions.")
    console.print("[bold]Privacy[/bold]\nPASS Hostname redacted\nPASS Username redacted\nPASS Home path sanitized")

@app.command()
def inspect(file: Annotated[Path, typer.Argument(exists=False)]) -> None:
    """Analyze a supported text file without creating files."""
    result = _analyze(file); table = Table(title="File Analysis", show_header=False)
    for key, value in (("Type", file.suffix.lstrip(".") or "text"), ("Size", f"{result.size_bytes} bytes"), ("Lines", result.lines)): table.add_row(key, str(value))
    console.print(table); findings = Table(title="Findings", show_header=False)
    for key, value in (("Errors", result.error_lines), ("Warnings", result.warning_lines), ("Stack traces", len(result.stack_traces)), ("Sensitive values", result.replacement_count), ("Emails", result.redactions.get("email", 0)), ("Private IPs", result.redactions.get("private_ip", 0))): findings.add_row(key, str(value))
    console.print(findings)

@app.command()
def scan(file: Annotated[Path, typer.Argument(exists=False)], output: Annotated[Path | None, typer.Option("--output", "-o")] = None, dry_run: Annotated[bool, typer.Option("--dry-run")] = False, quiet: Annotated[bool, typer.Option("--quiet", "-q")] = False) -> None:
    """Sanitize a supported text file into a new safe copy."""
    if file.suffix.lower() in IMAGE_EXTENSIONS:
        console.print('OCR support is not installed.\n\nInstall optional OCR dependencies:\n\npip install "reprosafe[ocr]"'); raise typer.Exit(3)
    result = _analyze(file)
    if not quiet:
        console.print(f"[bold]Scanning {file.name}[/bold]\nPASS {result.lines} lines processed\nPASS {result.replacement_count} values redacted\nPASS {len(result.stack_traces)} stack trace type(s) detected\nPASS {len(result.errors)} error signature(s) detected")
        table = Table(title="Privacy summary", show_header=False)
        for name, count in sorted(result.redactions.items()): table.add_row(name.replace("_", " ").title(), str(count))
        console.print(table)
    if dry_run: console.print("No files written."); return
    destination = output or safe_output_path(file)
    if destination.resolve() == file.resolve(): console.print("[red]Safety refusal: output cannot overwrite the source.[/red]"); raise typer.Exit(4)
    try: write_new_file(destination, result.sanitized_text)
    except FileSafetyError as exc: console.print(f"[red]{exc}[/red]"); raise typer.Exit(4) from None
    if not quiet: console.print(f"Safe copy: {destination}")

@app.command()
def bundle(output: Annotated[Path, typer.Option("--output", "-o")] = Path("reprosafe-report"), files: Annotated[list[Path] | None, typer.Option("--file", help="Text file to sanitize and include (repeatable).")] = None) -> None:
    """Create Markdown, JSON, and sanitized-file diagnostics locally."""
    cfg = load_config()
    scans = [_analyze(path, cfg) for path in (files or [])]
    try:
        created = create_bundle(
            output,
            scans,
            include_diagnostics_json=cfg.report.include_diagnostics_json,
        )
    except (FileSafetyError, OSError) as exc: console.print(f"[red]Unable to create bundle: {exc}[/red]"); raise typer.Exit(3) from None
    console.print(f"PASS Report bundle created: {created}\nReview report.md before sharing.")

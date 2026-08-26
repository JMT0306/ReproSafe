"""Developer tool discovery using safe version invocations."""
import shutil
from reprosafe.utils.commands import run_command
TOOLS: dict[str, tuple[str, ...]] = {"Git": ("git", "--version"), "Python": ("python", "--version"), "pip": ("pip", "--version"), "pipx": ("pipx", "--version"), "Node": ("node", "--version"), "npm": ("npm", "--version"), "pnpm": ("pnpm", "--version"), "yarn": ("yarn", "--version"), "Bun": ("bun", "--version"), "Java": ("java", "-version"), "Maven": ("mvn", "--version"), "Gradle": ("gradle", "--version"), "Go": ("go", "version"), "Rust": ("rustc", "--version"), "Cargo": ("cargo", "--version"), "Docker": ("docker", "--version"), "Docker Compose": ("docker", "compose", "version"), "Podman": ("podman", "--version"), "kubectl": ("kubectl", "version", "--client")}
def collect_tools() -> dict[str, str | None]:
    found: dict[str, str | None] = {}
    for name, command in TOOLS.items():
        if shutil.which(command[0]) is None: found[name] = None; continue
        result = run_command(command)
        output = result.stdout or result.stderr
        found[name] = output.splitlines()[0][:160] if result.returncode == 0 and output else "detected"
    return found

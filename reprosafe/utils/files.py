"""Bounded and conservative file operations."""
from pathlib import Path
TEXT_EXTENSIONS = {".txt", ".log", ".json", ".yaml", ".yml", ".env", ".ini", ".cfg", ".conf", ".config"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

class FileSafetyError(ValueError):
    pass

def read_text_file(path: Path, max_bytes: int) -> str:
    if not path.exists(): raise FileSafetyError("File does not exist.")
    if path.is_dir(): raise FileSafetyError("A directory cannot be scanned.")
    if path.is_symlink(): raise FileSafetyError("Symbolic links are refused by default.")
    if path.suffix.lower() not in TEXT_EXTENSIONS: raise FileSafetyError("Unsupported text file type.")
    if path.stat().st_size > max_bytes: raise FileSafetyError("File exceeds the configured size limit.")
    data = path.read_bytes()
    if b"\x00" in data: raise FileSafetyError("Binary content cannot be scanned as text.")
    return data.decode("utf-8", errors="replace")

def safe_output_path(source: Path) -> Path:
    return source.with_name(f"{source.stem}.safe{source.suffix}")

def write_new_file(path: Path, content: str) -> None:
    try:
        with path.open("x", encoding="utf-8", newline="") as handle: handle.write(content)
    except FileExistsError as exc:
        raise FileSafetyError(f"Output already exists: {path}") from exc

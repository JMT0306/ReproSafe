"""Privacy-first TOML configuration."""
from dataclasses import dataclass, field
from pathlib import Path
import tomllib
from platformdirs import user_config_path

@dataclass
class PrivacyConfig:
    redact_emails: bool = True
    redact_private_ips: bool = True
    redact_public_ips: bool = False
    redact_hostname: bool = True
    redact_username: bool = True

@dataclass
class ScanConfig:
    max_file_size_mb: int = 20

@dataclass
class ReportConfig:
    include_diagnostics_json: bool = True

@dataclass
class Config:
    privacy: PrivacyConfig = field(default_factory=PrivacyConfig)
    scan: ScanConfig = field(default_factory=ScanConfig)
    report: ReportConfig = field(default_factory=ReportConfig)

CONFIG_PATH = user_config_path("reprosafe") / "config.toml"

def load_config(path: Path | None = None) -> Config:
    target = path or CONFIG_PATH
    if not target.exists():
        return Config()
    try:
        raw = tomllib.loads(target.read_text(encoding="utf-8"))
        return Config(privacy=PrivacyConfig(**raw.get("privacy", {})),
                      scan=ScanConfig(**raw.get("scan", {})),
                      report=ReportConfig(**raw.get("report", {})))
    except (OSError, tomllib.TOMLDecodeError, TypeError):
        return Config()

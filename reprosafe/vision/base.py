"""Small OCR interface for optional backends."""
from dataclasses import dataclass
from typing import Protocol
@dataclass(frozen=True)
class OCRRegion:
    text: str
    box: tuple[int, int, int, int]
class OCRBackend(Protocol):
    def available(self) -> bool: ...
    def extract(self, path: str) -> list[OCRRegion]: ...

"""Non-destructive OCR-region redaction."""
from pathlib import Path
from reprosafe.sanitizers.text import sanitize_text
from reprosafe.vision.base import OCRBackend

def redact_image(source: Path, output: Path, backend: OCRBackend) -> int:
    from PIL import Image, ImageDraw  # type: ignore[import-not-found]
    regions = backend.extract(str(source)); sensitive = [r for r in regions if sanitize_text(r.text).replacement_count]
    image = Image.open(source).convert("RGB"); draw = ImageDraw.Draw(image)
    for region in sensitive: draw.rectangle(region.box, fill="black")
    image.save(output); return len(sensitive)

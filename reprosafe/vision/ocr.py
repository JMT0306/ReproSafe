"""Optional Tesseract adapter; imports occur only when requested."""
from reprosafe.vision.base import OCRRegion
class TesseractBackend:
    def available(self) -> bool:
        try:
            import PIL  # noqa: F401
            import pytesseract  # noqa: F401
            return True
        except ImportError:
            return False
    def extract(self, path: str) -> list[OCRRegion]:
        from PIL import Image
        import pytesseract
        data = pytesseract.image_to_data(Image.open(path), output_type=pytesseract.Output.DICT)
        return [OCRRegion(text, (data["left"][i], data["top"][i], data["left"][i] + data["width"][i], data["top"][i] + data["height"][i])) for i, text in enumerate(data["text"]) if text.strip()]

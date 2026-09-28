"""
OCR provider abstraction.

Real deployments would implement PaddleOCRProvider (Marathi-capable OCR model).
That dependency is heavy (torch/paddlepaddle) and not needed to demo the
product end-to-end, so this module ships:

  - PyMuPDFTextProvider: extracts real embedded text from digital PDFs
    (works today, no ML model needed).
  - DemoOCRProvider: returns clearly-labelled placeholder text for scanned/
    image-only PDFs when no OCR engine is installed, so the pipeline still
    runs end-to-end in DEMO_MODE.

Swap in a real PaddleOCRProvider later by implementing the same interface
and wiring it in `get_ocr_provider()`.
"""
from abc import ABC, abstractmethod
from typing import List, Dict
import fitz  # PyMuPDF


class OCRProvider(ABC):
    @abstractmethod
    def extract(self, file_path: str) -> List[Dict]:
        """Return a list of {page_number, raw_text, cleaned_text, confidence}."""
        raise NotImplementedError


class PyMuPDFTextProvider(OCRProvider):
    """Extracts embedded digital text directly (no OCR needed)."""

    def extract(self, file_path: str) -> List[Dict]:
        pages = []
        doc = fitz.open(file_path)
        for i, page in enumerate(doc):
            text = page.get_text("text").strip()
            pages.append({
                "page_number": i + 1,
                "raw_text": text,
                "cleaned_text": clean_text(text),
                "confidence": 1.0 if text else None,
            })
        doc.close()
        return pages


class DemoOCRProvider(OCRProvider):
    """Fallback used when a page has no embedded text (i.e. it's a scan)
    and no real OCR engine is configured. Clearly marks output as DEMO."""

    def extract(self, file_path: str) -> List[Dict]:
        doc = fitz.open(file_path)
        pages = []
        for i, page in enumerate(doc):
            pages.append({
                "page_number": i + 1,
                "raw_text": "[DEMO OCR] scanned page - no OCR engine configured",
                "cleaned_text": (
                    f"[DEMO OCR - page {i+1}] या पानावर मजकूर उपलब्ध नाही "
                    f"(OCR इंजिन कॉन्फिगर केलेले नाही). ही डेमो नोंद आहे."
                ),
                "confidence": None,
            })
        doc.close()
        return pages


def clean_text(text: str) -> str:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return "\n".join(lines)


def get_ocr_provider() -> OCRProvider:
    return PyMuPDFTextProvider()


def get_fallback_provider() -> OCRProvider:
    return DemoOCRProvider()


def process_pdf(file_path: str) -> List[Dict]:
    pages = get_ocr_provider().extract(file_path)
    if all(not p["raw_text"] for p in pages):
        pages = get_fallback_provider().extract(file_path)
    else:
        fallback = get_fallback_provider()
        for i, p in enumerate(pages):
            if not p["raw_text"]:
                demo_pages = fallback.extract(file_path)
                pages[i] = demo_pages[i]
    return pages

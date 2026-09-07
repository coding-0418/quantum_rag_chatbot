"""PDF text extraction using PyMuPDF."""

from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO


@dataclass(frozen=True)
class ExtractedPage:
    """Text and citation metadata extracted from one PDF page."""

    page_number: int
    text: str


class PDFIngestor:
    """Extract page-aware text from a PDF with PyMuPDF."""

    def extract_pages(self, source: str | Path | BinaryIO | bytes) -> list[ExtractedPage]:
        import fitz

        document_source: str | bytes
        if isinstance(source, (str, Path)):
            document_source = str(source)
            document = fitz.open(document_source)
        else:
            document_source = source.read() if hasattr(source, "read") else source
            document = fitz.open(stream=document_source, filetype="pdf")

        try:
            return [
                ExtractedPage(page_number=page_number, text=page.get_text("text").strip())
                for page_number, page in enumerate(document, start=1)
                if page.get_text("text").strip()
            ]
        finally:
            document.close()

    def extract(self, source: str | Path | BinaryIO | bytes) -> str:
        """Return all extracted page text for callers that do not need page metadata."""

        return "\n\n".join(page.text for page in self.extract_pages(source))
"""PDF text extraction boundary."""

from pathlib import Path


class PDFIngestor:
    """Extract text from a PDF without coupling callers to pypdf."""

    def extract(self, path: str | Path) -> str:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
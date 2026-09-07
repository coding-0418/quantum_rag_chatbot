"""Batch-ingest all .txt files in data/knowledge_base/ into the FAISS index.

Usage:
    python scripts/ingest_knowledge_base.py
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from app.services.knowledge_base import ingest_document  # noqa: E402

KB_DIR = pathlib.Path(__file__).resolve().parent.parent / "data" / "knowledge_base"


def main() -> None:
    txt_files = sorted(KB_DIR.glob("*.txt"))
    if not txt_files:
        print(f"No .txt files found in {KB_DIR}. See its README.md for expected sources.")
        return

    for path in txt_files:
        content = path.read_text(encoding="utf-8")
        title = path.stem.replace("_", " ").title()
        document_id, num_chunks = ingest_document(
            title=title, content=content, source=str(path.name)
        )
        print(f"Ingested '{title}' -> document_id={document_id}, chunks={num_chunks}")


if __name__ == "__main__":
    main()

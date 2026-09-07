"""Named embedding-pipeline entry point."""

from collections.abc import Sequence

import numpy as np

from app.rag.embeddings import embed_texts


class EmbeddingPipeline:
    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        return embed_texts(texts, model_name=self.model_name)
from functools import lru_cache
from collections.abc import Sequence

import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import get_settings


@lru_cache(maxsize=4)
def get_embedding_model(model_name: str | None = None) -> SentenceTransformer:
    settings = get_settings()
    return SentenceTransformer(model_name or settings.embedding_model)


def embed_texts(texts: Sequence[str], model_name: str | None = None) -> np.ndarray:
    if not texts:
        return np.empty((0, 0), dtype="float32")
    model = get_embedding_model(model_name)
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return embeddings.astype("float32")


def embed_query(query: str, model_name: str | None = None) -> np.ndarray:
    return embed_texts([query], model_name=model_name)[0]

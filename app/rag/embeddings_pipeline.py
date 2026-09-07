"""Named embedding-pipeline entry point."""

from app.rag.embeddings import embed_texts


class EmbeddingPipeline:
    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name

    def embed(self, texts: list[str]):
        # TODO: Inject the embedding model to avoid loading it per process boundary.
        return embed_texts(texts)
"""Neo4j knowledge graph construction boundary."""

from dataclasses import dataclass

from app.db.neo4j_client import link_concept, link_document_chunk


@dataclass(frozen=True)
class KnowledgeGraphBuilder:
    async def add_chunk(self, document_id: str, chunk_id: str, chunk_index: int) -> None:
        await link_document_chunk(document_id, chunk_id, chunk_index)

    async def add_concept(self, chunk_id: str, concept: str) -> None:
        await link_concept(chunk_id, concept)
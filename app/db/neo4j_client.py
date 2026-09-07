from neo4j import AsyncDriver, AsyncGraphDatabase

from app.core.config import get_settings

_driver: AsyncDriver | None = None


def get_driver() -> AsyncDriver:
    global _driver
    if _driver is None:
        settings = get_settings()
        _driver = AsyncGraphDatabase.driver(
            settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password)
        )
    return _driver


async def close_driver() -> None:
    global _driver
    if _driver is not None:
        await _driver.close()
        _driver = None


async def link_document_chunk(document_id: str, chunk_id: str, chunk_index: int) -> None:
    driver = get_driver()
    async with driver.session() as session:
        await session.run(
            """
            MERGE (d:Document {id: $document_id})
            MERGE (c:Chunk {id: $chunk_id})
            SET c.index = $chunk_index
            MERGE (d)-[:HAS_CHUNK]->(c)
            """,
            document_id=document_id,
            chunk_id=chunk_id,
            chunk_index=chunk_index,
        )


async def link_concept(chunk_id: str, concept: str) -> None:
    driver = get_driver()
    async with driver.session() as session:
        await session.run(
            """
            MERGE (co:Concept {name: $concept})
            MERGE (c:Chunk {id: $chunk_id})
            MERGE (co)-[:MENTIONED_IN]->(c)
            """,
            chunk_id=chunk_id,
            concept=concept,
        )


async def related_concepts(concept: str, limit: int = 10) -> list[str]:
    driver = get_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (co:Concept {name: $concept})-[:MENTIONED_IN]->(c:Chunk)<-[:MENTIONED_IN]-(other:Concept)
            WHERE other.name <> $concept
            RETURN DISTINCT other.name AS name
            LIMIT $limit
            """,
            concept=concept,
            limit=limit,
        )
        return [record["name"] async for record in result]

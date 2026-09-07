import json
from typing import Any

from redis.asyncio import Redis

from app.core.config import get_settings

_client: Redis | None = None


def get_redis() -> Redis:
    global _client
    if _client is None:
        settings = get_settings()
        _client = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            decode_responses=True,
        )
    return _client


async def cache_get(key: str) -> Any | None:
    client = get_redis()
    raw = await client.get(key)
    return json.loads(raw) if raw else None


async def cache_set(key: str, value: Any, ttl_seconds: int = 3600) -> None:
    client = get_redis()
    await client.set(key, json.dumps(value), ex=ttl_seconds)

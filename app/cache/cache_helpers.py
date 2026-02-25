import json
from typing import Any, Awaitable, Callable
from redis.asyncio.client import Redis

async def get_or_set_json(
    redis: Redis,
    key: str,
    ttl_seconds: int,
    factory: Callable[[], Awaitable[Any]],
) -> Any:
    cached = await redis.get(key)
    if cached is not None:
        return json.loads(cached)

    value = await factory()
    await redis.setex(key, ttl_seconds, json.dumps(value))
    return value
import os
import redis.asyncio as redis
from redis.asyncio.client import Redis

def get_redis_url() -> str:
    return os.getenv("REDIS_URL", "redis://localhost:6379/0")

def create_redis_client() -> Redis:
    return redis.Redis.from_url(get_redis_url(), decode_responses=True)
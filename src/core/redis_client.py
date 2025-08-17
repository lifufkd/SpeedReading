from redis import Redis as SyncRedis
from redis.asyncio import Redis as AsyncRedis

from src.core.config import redis_settings

sync_redis_client = SyncRedis.from_url(redis_settings.redis_url)
async_redis_client = AsyncRedis.from_url(redis_settings.redis_url, decode_responses=True)

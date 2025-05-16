from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from ..config.settings import settings
import redis

async def startup():
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        ssl=True
    )
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
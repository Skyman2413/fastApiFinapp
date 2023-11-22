import redis as redis
from fastapi_users.authentication import BearerTransport, RedisStrategy, AuthenticationBackend

from src.config import REDIS_HOST, REDIS_PORT

bearer_transport = BearerTransport(tokenUrl="auth/bearer/login")

redis = redis.asyncio.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)


def getRedisStrategy() -> RedisStrategy:
    return RedisStrategy(redis, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="bearer",
    transport=bearer_transport,
    get_strategy=getRedisStrategy
)


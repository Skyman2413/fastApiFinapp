import redis as redis
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, RedisStrategy, AuthenticationBackend

from auth.manager import get_user_manager
from auth.models import User
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

bearer_transport = BearerTransport(tokenUrl="auth/bearer/login")

redis = redis.asyncio.from_url(f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0", decode_responses=True)


def getRedisStrategy() -> RedisStrategy:
    return RedisStrategy(redis, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="bearer",
    transport=bearer_transport,
    get_strategy=getRedisStrategy
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()




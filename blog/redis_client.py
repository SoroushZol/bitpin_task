import redis
from django.conf import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    charset="utf-8",
    decode_responses=True
)

_key = f"post:{{}}:scores"


def get_redis_post_data(post_id: int):
    redis_key = _key.format(post_id)
    data = redis_client.hgetall(redis_key)
    return data if data and "sum" in data and "count" in data else None
